---
title: "DeepAgents-Backend"
aliases: [CompositeBackend, FilesystemPermission, 深度智能体后端与权限]
tags: [ai/framework/active]
category: concepts
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/DeepAgent框架/DeepAgent框架.md]]"
description: "DeepAgents-Backend 是智能体文件系统操作的底层抽象层，提供 State/Filesystem/Store/CompositeBackend 等后端存储，并内置 FilesystemPermission 动态人工确认熔断机制。"
---

# [[DeepAgents]] 后端存储与权限控制

在 **[[DeepAgents]]** 中，[[AI-Agent|智能体]]对文件进行创建、读取、搜索或删除等操作并不是直接与物理磁盘交互，而是通过一个高度抽象的 **Backend（后端）** 文件协议层。

---

## 1. 深度代理的四大文件后端

```text
                           ┌──────────────────┐
                           │ CompositeBackend │ (复合路由器后端)
                           └────────┬─────────┘
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         ▼                          ▼                          ▼
 ┌───────────────┐          ┌───────────────┐          ┌───────────────┐
 │ StateBackend  │          │FilesystemBack │          │ StoreBackend  │
 │ (只读字节流)   │          │ (本地磁盘/沙箱)│          │ (长期记忆挂载) │
 └───────────────┘          └───────────────┘          └───────────────┘
```

- **`StateBackend` (默认状态后端)**：
  - *存储特征*：不产生本地磁盘文件，将所有上传的 Skills、约束文档存放在会话的短期 State 字典中。
  - *使用场景*：轻量级内存调试，无需本地环境污染。
- **`FilesystemBackend` (文件系统后端)**：
  - *存储特征*：直接映射到物理机器或 Docker 容器的某个真实磁盘目录。
  - *安全机制*：提供 `virtual_mode=True`。启用后，[[AI-Agent|智能体]]的一举一动都被锁死在设定的 `root_dir` 根目录下，防止其越权读取主机系统敏感文件（如 `/etc/passwd`）。
- **`StoreBackend` ([[LangGraph-Long-Term-Memory|长期记忆]]后端)**：
  - *存储特征*：将文件资源挂载在长期存储（[[LangGraph-Long-Term-Memory|InMemoryStore]] 或 [[LangChain-Agent-Runtime|PostgresSaver]] 数据库）中。
  - *使用场景*：多个不同的对话线程或多个 Agent 之间，需要跨会话同步读取共享文件。
- **`CompositeBackend` (复合路由器后端 - 生产推荐)**：
  - *工作原理*：相当于一个**后端网关路由器**。它允许将不同的虚拟路径映射到不同的底层物理后端。
  - *典型实例*：
    ```python
    CompositeBackend(
        default=StateBackend(), # 默认文件存内存状态
        routes={
            "/skills/": ContextHubBackend("my-agent"), # 从 LangSmith Hub 动态拉取技能
            "/memory/": FilesystemBackend(root_dir="./", virtual_mode=True) # 本地配置文件读取
        }
    )
    ```

---

## 2. 文件系统权限机制与人工中断审查 (FilesystemPermission)
在全自动执行任务中，为了防止[[AI-Agent|智能体]]在本地写入木马、恶意修改项目关键配置或执行破坏性删除动作，[[DeepAgents]] 提供了颗粒度极细的 **`FilesystemPermission`** 安全熔断防线。

### ① 拦截策略规则定义
可以通过在创建 Agent 时传入 permissions 策略数组对 read/write 操作进行动态审查：
```python
from deepagents import FilesystemPermission

permissions = [
    FilesystemPermission(
        operations=["write"], # write 代表拦截 write_file, edit_file, delete 等破坏性操作
        paths=["/config/**", "/src/**/*.py"], # 全局 Glob 表达式匹配
        mode="interrupt" # 拦截模式：allow 允许 / deny 直接拒绝 / interrupt 暂停审批
    )
]
```

### ② [[LangGraph-Human-In-The-Loop|人机交互]]中断与恢复流程
1. 当大模型决定调用 `write_file` 写入敏感文件时，检测到匹配的规则模式为 `interrupt`，Agent 的图流转会立即**挂起暂停**。
2. 引擎生成包含中断详情的快照 `result.interrupts`，露出 `action_requests`（[[AI-Agent|智能体]]想执行的操作与参数）和 `allowed_decisions`（如 approve 批准 / reject 拒绝）。
3. 外部管理程序（或终端 UI 接收输入）获取审批意见。
4. 审批完成后，携带决策列表以 `Command` 格式恢复执行：
   ```python
   # decisions = [{"type": "approve"}]
   result = agent.invoke(
       Command(resume={"decisions": decisions}),
       config=config # 必须保持与挂起时完全一致的 thread_id 检查点
   )
   ```

---
**关联页面**
- [[DeepAgents]] (概念母体)
- [[OpenSandbox]] (命令执行的高危安全底座)
- [[LangChain-Agent-Runtime]] (底层的检查点恢复)
