---
title: "LangChain-Agent-Runtime"
aliases: [智能体运行时与内存, ToolRuntime, InMemoryStore, PostgresSaver]
tags: [ai/agent/active]
category: concepts
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/Agent智能体/Agent智能体.md]]"
description: "LangChain-Agent-Runtime 是基于 LangGraph 的依赖注入与运行时托管环境，统筹管理智能体的 Context 上下文、State 短期记忆状态、长期记忆 Store 及状态 Command 动态修改。"
---

# LangChain Agent Runtime 与内存机制

在 LangChain 1.0 的技术体系中，**Runtime（运行时）** 由底层的 [[LangGraph]] 提供支持。它是[[AI-Agent|智能体]]执行过程中的“操作系统”，负责统一调度、托管工具执行、状态变量维护及长期短期记忆。

---

## 1. 运行时的核心组件与生命周期

```text
                  ┌──────────────────────────────┐
                  │           Runtime            │ (托管运行期环境)
                  └──────────────┬───────────────┘
                                 ▼
         ┌───────────────┬───────┴───────┬───────────────┐
         ▼               ▼               ▼               ▼
    [Context]         [State]         [Store]     [Stream Writer]
   (静态只读)       (短期字典)      (长期记忆)      (自定义流)
```

- **Context（上下文）**：
  - *特点*：在一次任务执行周期中静态、只读且不可变。
  - *典型信息*：当前调用者的 `user_id`、用户昵称、数据库连接池配置。
- **State（短期记忆状态）**：
  - *特点*：在一个会话（Session）中存在的可变 TypedDict 或 Pydantic 字典。
  - *典型信息*：对话的历史消息列表 `messages`。
- **Store（[[LangGraph-Long-Term-Memory|长期记忆]]存储）**：
  - *特点*：跨越多次会话，持久化沉淀实体或用户画像。
  - *实现*：利用 `store.put(namespace=(user_id, "memories"), key="user_profile", value={...})`。
- **Stream Writer（流写入器）**：
  - 在工具内部通过 `get_stream_writer()` 向前端实时输出中间状态（例如“正在为您查询天气...”）。

---

## 2. 状态修剪与垃圾回收 (GC) 策略
在多轮长对话中，短期记忆的 `messages` 列表会迅速膨胀，超出大模型的上下文窗口。LangChain 提供了三套主流修剪机制：
1. **`trim_messages` 自动裁剪**：
   - 在将消息输入大模型前，基于 Token 计数（中文按 `chars_per_token=1.8` 计算）和 `strategy="last"` 自动裁剪掉早期消息。
   - 配置 `include_system=True` 确保始终保留索引为 0 的系统人设 Prompt，配置 `start_on="human"` 确保裁剪后的首条消息为 HumanMessage，防止违反模型接口规范。
2. **`RemoveMessage` 显式擦除**：
   - 开发者可以在 `after_model` 钩子中，判定当前消息长度并返回 `{"messages": [RemoveMessage(id=msg.id)]}`，[[LangGraph]] 引擎会在后台自动彻底删除该消息，实现状态的物理垃圾清理。
3. **对话历史总结 (Summarization)**：
   - 使用轻量级模型对早期对话生成一段背景摘要，将摘要写入系统 Prompt 并彻底清空被总结的原始消息。

---

## 3. 工具对 Runtime 的捕获与 Command 反馈
### ① 工具端捕获 ToolRuntime
在自定义 `@tool` 时，可以通过依赖注入获取当前执行的运行时环境，动态读取用户姓名及状态：
```python
from langchain.tools import tool, ToolRuntime

@tool
def get_user_name(runtime: ToolRuntime[Context, TutorState]):
    """获取用户姓名工具"""
    return runtime.context.user_name # 动态从 Context 中读取
```

### ② 通过 Command 反馈状态修改
工具默认只能通过返回值生成一条 `ToolMessage` 插入历史。如果工具想要在执行完毕后**跨节点修改短期 State 状态**（例如更新 `user_hobby` 字段），必须返回 `Command` 对象：
```python
from langgraph.types import Command
from langchain_core.messages import ToolMessage

return Command(
    update={
        "user_hobby": ["编程", "篮球"], # 更新短期 State 字段
        "messages": [ToolMessage(content="更新成功", tool_call_id=runtime.tool_call_id)]
    }
)
```

---
**关联页面**
- [[AI-Agent]] (概念母体)
- [[Agent-Middleware]] (生命周期中的中间件)
- [[LlamaIndex]] (对比的框架)
