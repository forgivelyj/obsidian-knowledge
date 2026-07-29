---
title: "LangGraph-Persistence"
aliases: [Checkpointing, thread_id, checkpoint_id, update_state, 状态重放]
tags: [ai/framework/active]
category: concepts
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/LangGraph框架/LangGraph框架.md]]"
description: "LangGraph-Persistence 详解基于 Checkpointer 检查点的持久化存储，阐述 thread_id 隔离、历史回溯、重放分叉与 update_state 手动干预状态数据。"
---

# [[LangGraph]] 持久化与状态重放机制

**持久化 (Persistence)** 是 **[[LangGraph]]** 最为核心的企业级工程特性。通过在流程中引入检查点机制，使得[[AI-Agent|智能体]]具备了容错恢复、历史回溯重放以及人工直接编辑状态数据的能力。

---

## 1. 检查点保存器 (Checkpointer) 与线程隔离
在编译状态图时，可以挂载持久化后端，通常称为 **Checkpointer**：
```python
# 短期调试：内存检查点；生产环境：可以使用 RedisSaver 或 PostgresSaver
checkpointer = InMemorySaver()
app = builder.compile(checkpointer=checkpointer)
```
- **工作原理**：在图的每一个超级步骤（Superstep，即所有当前并发活跃节点执行完毕并合并状态的瞬间）结束时，Checkpointer 会对全局 `State` 进行快照存盘，生成一个 `StateSnapshot`。
- **线程隔离 (thread_id)**：在调用图时，必须在 `config` 字典中传入 `thread_id` 作为唯一会话标识：
  ```python
  config = {"configurable": {"thread_id": "session-12345"}}
  result = app.invoke(inputs, config=config)
  ```
  相同 `thread_id` 下的后续 `invoke` 自动从上一个超级步骤的快照中加载状态继续向下执行，从而无缝实现了跨请求的多轮对话记忆。

---

## 2. 状态历史获取与重放机制 (Time Travel / Replay)
[[LangGraph]] 将历史所有的检查点快照以时间轴形式留存，开发者可以通过 `get_state_history(config)` 读取完整的快照链表。

### ① 状态回溯与重放
- **场景**：大模型在步骤 3 犯了错误，用户希望让其回退到步骤 2，重新生成答案。
- **实现步骤**：
  1. 通过历史列表提取步骤 2 保存的 `checkpoint_id`；
  2. 构建包含 `checkpoint_id` 的新配置：
     ```python
     config_replay = {
         "configurable": {
             "thread_id": "session-12345",
             "checkpoint_id": "step2_checkpoint_id" # 锁定历史步骤
         }
     }
     ```
  3. 再次调用 `app.invoke(None, config=config_replay)`（注意输入传 None，代表从既有状态唤醒）。
  4. 引擎会自动回档并开始执行，在此之上**分裂出一个新的检查点分支**（原步骤 3 依然保留在数据库中，形成了版本分叉）。

---

## 3. 手动编辑更新状态 (update_state)
除了重放之外，人类审查员还可以直接对数据库中的快照状态进行“物理修改”，以干预[[AI-Agent|智能体]]的后续推理路径。这在[[LangGraph-Human-In-The-Loop|人机交互]]审核中至关重要。

通过调用 **`graph.update_state()`** 实现编辑：
- **核心参数**：
  - `config`：包含 `thread_id`。如果包含 `checkpoint_id`，则代表对历史的某个检查点进行分叉修改；若不指定则默认分叉修改最新状态。
  - `values`：需要强行写入的更新字典。
  - `as_node`：可选。**指定更新假装来自哪个节点**。这会极大地影响下一次 `invoke` 执行时被激活的 `next` 节点。
- **运行表现**：`update_state` 会生成一个新的检查点，用户再次 `invoke` 图时，[[AI-Agent|智能体]]将读取被修改后的新状态值继续流转。

---
**关联页面**
- [[LangGraph]] (框架实体)
- [[LangGraph-State-Graph]] (状态图结构)
- [[LangGraph-Long-Term-Memory]] (相对应的[[LangGraph-Long-Term-Memory|长期记忆]])
- [[LangGraph-Human-In-The-Loop]] (直接依赖持久化实现的拦截)
