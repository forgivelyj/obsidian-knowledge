---
title: "LangGraph"
aliases: [langgraph, LangGraph框架]
tags: [ai/framework/active]
category: entities
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/LangGraph框架/LangGraph框架.md]]"
description: "LangGraph 是由 LangChain 团队开源的用于构建生产级、有状态多智能体系统的图编排框架，主打持久执行、人机交互与综合记忆。"
---

# LangGraph (多[[AI-Agent|智能体]]图工作流框架)

LangGraph 是由 LangChain 团队发布并维护的、用于构建生产级[[AI-Agent|智能体]]系统的**图编排与状态管理框架**。

与主打线性执行链的 LangChain 不同，LangGraph 允许开发者将复杂的[[AI-Agent|智能体]]运行逻辑抽象为**有向有环图**，从而原生支持多步骤循环推理、双向路由、并发计算、状态持久化和精细的[[LangGraph-Human-In-The-Loop|人机交互]]。

---

## 1. LangGraph 的四大核心能力
1. **持久化执行 (State Persistence)**：
   - 能够在执行的任何一个步骤（Superstep）自动对状态进行快照保存。当遇到系统崩溃、网络超时或达到速率限制时，可以随时从最后一个成功的检查点安全恢复，或从历史步骤分叉重放。
2. **双轨[[LangGraph-Human-In-The-Loop|人机交互]] (Human-in-the-loop)**：
   - 支持在特定高副作用节点执行前挂起等待审核（修改状态后放行），或在执行过程中动态抛出问题并等待人类“填空”回传，实现真正意义上的人机协作。
3. **综合记忆系统 (Memory System)**：
   - *短期记忆*：维护当前会话的对话历史和执行状态，确保交互连贯。
   - *[[LangGraph-Long-Term-Memory|长期记忆]]*：跨越多个对话线程持久化沉淀用户习惯、画像。
4. **可视化与调试支持 (LangSmith)**：
   - 原生与 LangSmith 无缝对接，可以在云端以 Mermaid 图拓扑结构直观追踪每一个节点的输入输出、执行时长及 Token 消耗。

---

## 2. LangGraph 与 LangChain 的对比

| 维度 | LangChain | LangGraph |
| :--- | :--- | :--- |
| **工作流拓扑** | 链式结构 (Chain)。主要支持线性的、单向顺序执行。 | 图结构 (Graph)。支持复杂的条件分支、有环循环与并发计算。 |
| **状态维护** | 状态随链式传递，难以对中间临时状态进行细粒度控制或持久存盘。 | 内置强大的状态合并与检查点管理（Checkpointer），原生保存运行快照。 |
| **控制力等级** | 高度封装（如 `create_agent`），内部执行路径对开发者而言是黑盒，难以精细调度。 | 节点与边均由原生 Python 函数实现，开发者拥有对控制流的绝对掌控权。 |
| **适用场景** | 简单到中等复杂度的 LLM 应用、快速原型开发。 | 生产级、长周期运行、需要复杂分支决策的多[[AI-Agent|智能体]]协作系统。 |

---
**关联页面**
- [[LangGraph-State-Graph]] (有状态图架构)
- [[LangGraph-Persistence]] (检查点持久化与重放)
- [[LangGraph-Long-Term-Memory]] ([[LangGraph-Long-Term-Memory|长期记忆]]与[[LangGraph-Long-Term-Memory|语义检索]])
- [[LangGraph-Human-In-The-Loop]] (人工交互双轨机制)
- [[LangGraph-Multi-Agent]] (LangGraph 多代理编排)
- [[DeepAgents]] (构建于其上的 Harness 套件)
