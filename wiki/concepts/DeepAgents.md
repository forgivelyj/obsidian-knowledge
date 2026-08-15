---
title: "DeepAgents"
aliases: [deepagents, 深度智能体, Agent Harness]
tags: [ai/framework/active]
category: concepts
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/DeepAgent框架/DeepAgent框架.md]]"
description: "DeepAgents 是基于 LangGraph 与 LangChain 构建的企业级智能体开发套件（Agent Harness），旨在通过预置中间件与状态管控大幅降低长周期、多步骤复杂 Agent 的落地门槛。"
---

# DeepAgents (深度[[AI-Agent|智能体]]套件)

## 1. 深度[[AI-Agent|智能体]]的技术定位
在 LangChain 1.0 的技术版图中，构建高复杂度、长周期、多步骤执行的 Agent 存在一条三层递进的演进路线：

```text
  ┌─────────────────────────────────────────────────────────┐
  │         DeepAgents (深度智能体 - 企业套件 Harness)         │ (create_deep_agent)
  └────────────────────────────┬────────────────────────────┘
                               ▼
  ┌─────────────────────────────────────────────────────────┐
  │         LangChain (上层封装与中间件系统)                  │ (create_agent / Middleware)
  └────────────────────────────┬────────────────────────────┘
                               ▼
  ┌─────────────────────────────────────────────────────────┐
  │         LangGraph (底层状态持久化与工作流基座)              │ (StateGraph / Checkpointer)
  └─────────────────────────────────────────────────────────┘
```

1. **[[LangGraph]] (底层基座)**：
   - 提供底层状态持久化与多步骤执行追踪。
   - 开发者需要手动定义图节点、条件边（Conditional Edges）并注入 Checkpointer。自定义开发成本高。
2. **LangChain (中间层封装)**：
   - 提供一键构建[[AI-Agent|智能体]]的接口（`create_agent`）和六大生命周期钩子中间件（Middleware）。
3. **DeepAgents (企业级 Harness 套件)**：
   - 深度集成[[AI-Agent|智能体]]规划、文件后端映射、沙箱运行和分层多子代理。
   - 提供极简工厂方法 **`create_deep_agent`**，在底层自动挂载各种预置的上下文管理、权限管理中间件，开箱即用。

---

## 2. 传统 Agent 与 DeepAgents 的对比

| 维度 | 传统单大模型循环工具代理 | DeepAgents 深度代理 |
| :--- | :--- | :--- |
| **任务复杂度限制** | 仅适合 5-10 轮简单工具调用。 | 可支持百步级别长周期任务（如深度研究）。 |
| **上下文管理** | 工具临时输出直接塞入主 Context，导致 Token 极速膨胀、丢失核心目标。 | 预置上下文压缩中间件，主代理仅加载技能摘要，通过分层子代理**上下文隔离**。 |
| **文件系统操作** | 大模型无法操作真实文件，除非手动挂载复杂的文件读写工具。 | 底层抽象出 **[[DeepAgents-Backend]]** 文件后端协议，直接映射磁盘或沙箱。 |
| **代码执行与命令** | 不具备任意 shell 命令安全执行能力。 | 配合 **[[OpenSandbox]]** 等沙箱后端，提供 `execute` 沙箱隔离执行工具。 |
| **安全控制** | 无法做到读写操作的动态权限拦截与拦截审查。 | 预置 `FilesystemPermission` 支持 `interrupt` 暂停审批并恢复。 |

---
**关联页面**
- [[AI-Agent]] ([[AI-Agent|智能体]]概念母体)
- [[LangChain-Agent-Runtime]] (底层运行时与内存)
- [[DeepAgents-Backend]] (文件系统存储后端)
- [[OpenSandbox]] (阿里开源隔离沙箱)
- [[DeepAgents-Subagent]] (分层子代理设计)
