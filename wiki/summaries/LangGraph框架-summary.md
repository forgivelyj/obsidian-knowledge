---
title: "LangGraph框架-summary"
aliases: [LangGraph 框架编译摘要, LangGraph Summary]
tags: [ai/framework/active]
category: summaries
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/LangGraph框架/LangGraph框架.md]]"
description: "系统总结多智能体工作流框架 LangGraph 核心功能，拆解 StateGraph 与 Map-Reduce 动态分支、持久化 Checkpoint 状态重放、跨会话 Store 语义长期记忆、双轨人机交互中断及分布式多代理协同。"
---

# [[LangGraph|LangGraph框架]] 摘要

## 概要说明
本素材是关于大模型多[[AI-Agent|智能体]]工作流框架 **[[LangGraph]]** 的系统开发指南。深入阐述了 [[LangGraph]] 与 LangChain 链式结构的本质区别，详解了以 **[[LangGraph-State-Graph]]**（有状态流程图）为中心的 Schema（输入/输出分离模式）和 [[LangGraph-State-Graph|Send]] 动态 [[LangGraph-State-Graph|Map-Reduce]] 并行机制；剖析了基于 Checkpointer 的 **[[LangGraph-Persistence]]** 持久化版本回溯与[[LangGraph-Persistence|状态重放]]机制；介绍了利用 Store 构建跨会话 **[[LangGraph-Long-Term-Memory]]** 的[[LangGraph-Long-Term-Memory|语义检索]]实现；详述了 **[[LangGraph-Human-In-The-Loop]]** 拦截与填空双轨中断机制；并系统归纳了 **[[LangGraph-Multi-Agent]]** 多[[AI-Agent|智能体]]系统下的交接模式与主管架构（Supervisor）工程设计。

## 核心要点
1. **[[LangGraph]] 相比 LangChain 的核心优势**：
   - LangChain 主要支持线性的顺序执行链（Chain），对复杂多[[AI-Agent|智能体]]黑盒控制力弱。
   - **[[LangGraph]]** 专为复杂的多步骤、多[[AI-Agent|智能体]]场景设计，主打图状工作流（Graph），原生支持持久化执行、[[LangGraph-Human-In-The-Loop|人机交互]]中断、短期/[[LangGraph-Long-Term-Memory|长期记忆]]与复杂条件跳转。
2. **有状态流程图与 [[LangGraph-State-Graph|Map-Reduce]] 动态并行**：
   - **[[LangGraph-State-Graph]]** 以状态为核心驱动。
     - *State 状态定义*：推荐使用零开销的 TypedDict 定义共享 Schema，支持为图显式指定 `input_schema` 和 `output_schema` 隔离中间数据；归并使用 `add_messages` 跟踪 ID 覆盖更新。
     - *[[LangGraph-State-Graph|Send]] 并行处理*：支持在条件边（`add_conditional_edges`）中返回 `Send` 对象列表，动态拉起多个 `worker` 节点并行运行（Map），并在下游节点使用 `Annotated[list, operator.add]` 汇总结果（Reduce）。
3. **Checkpoints 持久化与[[LangGraph-Persistence|状态重放]]**：
   - **[[LangGraph-Persistence]]** 提供超级步骤（Superstep）状态持久化，支持 InMemorySaver、RedisSaver 或 [[LangChain-Agent-Runtime|PostgresSaver]]。
   - *重放分叉机制*：可使用 `get_state_history(config)` 读取历史快照，传入 `checkpoint_id` 重启执行链，在既有基础上分裂出新分支。
   - *状态手动编辑*：允许调用 `update_state()` 强行修改某线程在特定节点的历史数据，下一次调用 `invoke` 将从该人工更新的状态点继续执行。
4. **[[LangGraph-Long-Term-Memory|长期记忆]]（Store）与语义向量检索**：
   - **[[LangGraph-Long-Term-Memory]]** 跨越 Thread 线程，存储应用程序级或用户特定的画像特征。
   - 工具内部通过 `ToolRuntime` 从 `runtime.store` 存取命名空间 `(user_id, memories)` 下的偏好。
   - 支持向 `InMemoryStore` / `PostgresStore` 注入[[Embedding|嵌入]]模型（[[Embedding]]）进行包含 query 和 limit 限制的**[[LangGraph-Long-Term-Memory|语义检索]]**。
5. **拦截与填空双轨中断控制**：
   - **[[LangGraph-Human-In-The-Loop]]** 融入人工监督：
     - *编译拦截（[[LangGraph-Human-In-The-Loop|interrupt_before]]）*：在编译图时注册断点，常用于在进入副作用节点（如发送订单、扣款）前挂起审查。
     - *运行时填空（[[LangGraph-Human-In-The-Loop|interrupt]]）*：在节点内部调用 `interrupt("提问")` 挂起，利用 `Command(resume=answer)` 传入参数实现动态交互。
6. **多[[AI-Agent|智能体]]（MAS）交接与主管架构**：
   - **[[LangGraph-Multi-Agent]]** 支持多代理灵活交互：
     - *[[LangGraph-Multi-Agent|Handoffs]]（交接）*：节点代理超出职责时，返回 `Command(goto="target", graph=Command.PARENT)` 移交指针。
     - *Supervisor（主管）*：主管节点使用 LLM 进行意图识别，支持待处理任务队列 `pending_tasks` 的多任务循环分发与汇聚，可引入 `langgraph-supervisor` 的 `create_supervisor` 自动构建。

---
**关联页面**：
- [[LangGraph]] (新建实体页)
- [[LangGraph-State-Graph]] (新建概念页)
- [[LangGraph-Persistence]] (新建概念页)
- [[LangGraph-Long-Term-Memory]] (新建概念页)
- [[LangGraph-Human-In-The-Loop]] (新建概念页)
- [[LangGraph-Multi-Agent]] (新建概念页)
- [[LangChain-Agent-Runtime]] (关联的运行时)
- [[Agent-Middleware]] (关联的中间件)
- [[DeepAgents]] (上层封装套件)
- [[Redis]] / [[Neo4j]] (关联的基础存储)
