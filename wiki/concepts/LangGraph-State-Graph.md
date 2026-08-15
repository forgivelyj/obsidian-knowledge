---
title: "LangGraph-State-Graph"
aliases: [StateGraph, Reducer, Send, Map-Reduce]
tags: [ai/framework/active]
category: concepts
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/LangGraph框架/LangGraph框架.md]]"
description: "LangGraph-State-Graph 是 LangGraph 的核心流程与状态管理组件，定义节点跳转与基于 Reducer 的状态归并，支持 Send 并行 Map-Reduce 计算。"
---

# [[LangGraph]] 有状态流程图 (StateGraph)

**`StateGraph`** 类是 **[[LangGraph]]** 框架中最重要、最核心的接口。它将代理的工作流建模为一张“有状态的流程图”，不仅定义了执行步骤和跳转边，还管理着在整个流程中流动和更新的共享数据状态。

---

## 1. 状态图的三大支柱

```text
                  ┌──────────────────────────────┐
                  │          StateGraph          │ (有状态流程图)
                  └──────────────┬───────────────┘
                                 ▼
         ┌───────────────┬───────┴───────┬───────────────┐
         ▼               ▼               ▼               ▼
     [State]          [Nodes]         [Edges]         [START]
   (状态与合并)     (执行期步骤)    (决策与跳转)    (入口与结束END)
```

- **`State` (共享状态)**：
  - *模式结构 (Schema)*：通常用 `TypedDict` 或 Pydantic `BaseModel` 声明。它像血液一样在图的每一个节点之间流转。
  - *输入/输出模式隔离*：支持显式指定 `input_schema` 和 `output_schema`。这允许主图仅接收用户输入字段（如 `question`），在内部运算复杂字段（如 `search_results`），最后仅提取返回特定的字段（如 `answer`），实现了**数据隔离与安全防护**。
  - *Reducer (归并函数)*：指定如何将节点返回的“局部状态更新”合并到全局 State 中。例如 `Annotated[list, operator.add]` 会将新项追加到列表尾部；而预置的 `add_messages` 归并器会在遇到带相同 ID 的历史消息时进行覆盖更新，防止聊天历史被完全重写。
- **`Nodes` (节点)**：
  - 代表执行具体任务的 Python 函数或 Runnable。它们接收当前的 `State`，执行逻辑（可包含 LLM 推理或普通 Python 代码），并返回更新后的局部状态字典。
  - 特殊节点：**`START`**（流程图起点，接收用户输入）与 **`END`**（流程图终点）。
- **`Edges` (边)**：
  - 连接节点。普通边（`add_edge`）直接从一个节点跳转到下一个节点。条件边（`add_conditional_edges`）会根据当前的 `State` 调用判定路由函数，动态决定下一步跳转的节点。

---

## 2. 基于 Send 的动态分支与并行计算 (Map-Reduce)
在很多场景下，我们无法提前确定需要执行哪些边（例如，大模型想对十篇不同的文档分别进行信息抽取，再进行汇总）。[[LangGraph]] 提供了 **`Send`** 接口与 `add_conditional_edges` 配合，实现经典的 **Map-Reduce** 并行计算：

```text
                  ┌──────────────────┐
                  │    Splitter      │ (Map分发阶段)
                  └────────┬─────────┘
                           │
         ┌─────────────────┼─────────────────┐ (并发 Send)
         ▼                 ▼                 ▼
   ┌───────────┐     ┌───────────┐     ┌───────────┐
   │ Worker A  │     │ Worker B  │     │ Worker C  │ (计算平方)
   └─────┬─────┘     └─────┬─────┘     └─────┬─────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                           ▼
                  ┌──────────────────┐
                  │     Summer       │ (Reduce汇总求和)
                  └──────────────────┘
```

1. **Map (分发阶段)**：
   - 在条件路由函数中返回 `Send` 对象列表：
     ```python
     # 将 5 个不同的数字分别发送给 5 个并发的 worker 节点执行
     return [Send("worker", {"number": num}) for num in numbers]
     ```
2. **Worker (并发计算)**：
   - 多个 worker 节点在局部独立的 `State` 状态下并行运行，计算平方值并返回局部更新 `{"results": [square]}`。
3. **Reduce (汇总阶段)**：
   - 汇聚节点（如 `summer`）被调用。由于 `results` 通道配置了 Reducer 合并规则 `Annotated[list, operator.add]`，所有并发 worker 返回的平方值均被自动追加到列表中，汇聚节点直接调用 `sum(results)` 完成累加，极大提升了多[[AI-Agent|智能体]]的运行速度。

---
**关联页面**
- [[LangGraph]] (框架实体)
- [[LangGraph-Persistence]] (状态的物理存盘机制)
- [[LangGraph-Multi-Agent]] (涉及并发子图分发的 Supervisor 节点)
