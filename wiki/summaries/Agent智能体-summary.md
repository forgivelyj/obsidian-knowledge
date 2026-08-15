---
title: "Agent智能体-summary"
aliases: [AI 智能体与多智能体系统开发摘要, Agent Summary]
tags: [ai/agent/active]
category: summaries
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/Agent智能体/Agent智能体.md]]"
description: "系统阐述 AI Agent 五层技术架构、LangChain 1.0 运行时环境与短期/长期记忆机制、智能体六大生命周期中间件系统，剖析多智能体（MAS）四大核心设计模式，并对比实战微软 AutoGen 与 CrewAI 协同系统。"
---

# Agent[[AI-Agent|智能体]] 摘要

## 概要说明
本素材是关于大模型 **[[AI-Agent]]**（[[AI-Agent|智能体]]）与多[[AI-Agent|智能体]]系统（MAS）的系统开发指南。重点剖析了 LangChain 1.0 架构下的[[AI-Agent|智能体]]核心技术：包括以 **[[LangChain-Agent-Runtime]]** 为中心的 Context（上下文）、State（状态）、Store（[[LangGraph-Long-Term-Memory|长期记忆]]，如 [[LangChain-Agent-Runtime|PostgresSaver]] 的持久化）及 Command 状态反馈机制；详解了横跨六大执行钩子的 **[[Agent-Middleware]]**（中间件）系统；系统归纳了多[[AI-Agent|智能体]]的四大设计模式（SubAgents、[[LangGraph-Multi-Agent|Handoffs]]、Skills、Router）；并深入演示了微软 **[[AutoGen]]** 与 **[[CrewAI]]** 两大 MAS 框架的架构设计与工程化实战。

## 核心要点
1. **[[AI-Agent|智能体]]核心组成与记忆修剪**：
   - [[AI-Agent|智能体]] = 大脑（规划决策）+ 手脚（工具 API 调用）+ 记忆（长期与短期）。
   - 短期记忆基于 Checkpointer（InMemorySaver / [[LangChain-Agent-Runtime|PostgresSaver]] 物理存盘），为应对上下文超载，提供三类裁剪策略：
     - `trim_messages`：大模型调用前依据 Token 计数（中文按 `chars_per_token=1.8` 计算）和 `strategy="last"` 自动切掉旧消息，并采用 `include_system=True` 强制保护核心人设系统提示词。
     - `RemoveMessage`：在 `after_model` 钩子中返回 `RemoveMessage(id=msg.id)`，指示 [[LangGraph]] 物理擦除状态中已过期的历史消息。
2. **LangChain 1.0 运行时（[[LangChain-Agent-Runtime|ToolRuntime]]）与[[LangGraph-Long-Term-Memory|长期记忆]]**：
   - **[[LangChain-Agent-Runtime]]** 托管工具的执行环境。
   - 工具内部可通过 `runtime: ToolRuntime[Context, TutorState]` 动态捕获静态上下文（`context.user_name`）与对话历史状态。
   - **[[LangGraph-Long-Term-Memory|长期记忆]] (Store)**：使用 `store.put()` 依照命名空间 `(user_id, memories)` 持久化存储用户偏好、画像等。
   - **状态自愈修改**：工具如需跨节点直接干预短期 State 状态，可直接返回 **`Command(update={"user_hobby": hobby, "messages": [...]})`** 触发状态机数据重写。
3. **中间件（Middleware）鲁棒性防护网**：
   - **[[Agent-Middleware]]** 提供 Agent 流程的精细化拦截与干预。
   - `before_agent`：代理开始前拦截，常用于敏感词校验与 `jump_to="end"` 直接旁路阻断生成。
   - `before_model` / `wrap_model_call`：模型调用前动态覆盖注入偏好 Prompt。
   - `after_model`：模型生成后执行，主要用于 JSON 结构自动纠错补全（多余逗号修复、Markdown 代码块标签擦除）。
4. **MAS 多[[AI-Agent|智能体]]四大设计模式**：
   - **SubAgents（子代理）**：主控（Supervisor）做决策，将子代理封装为无状态 [[MCP-Core-Protocol-Elements|Tools]]，实现强上下文隔离。
   - **[[LangGraph-Multi-Agent|Handoffs]]（移交模式）**：分布式指针轮转。当前 Agent 遇超职责问题调用转交工具（返回 Command 修改 `active_agent`），由新 Agent 继续接管并与用户多轮对话。
   - **Skills（技能模式）**：“同一个 Agent，多套技能”。保持统一“人设”和历史记忆，依据场景动态 `load_skill` 加载规则提示词。
   - **Router（路由器模式）**：路由器仅负责解析意图派发工作（支持并行）并汇总结果，不直接执行任何业务逻辑。
5. **MAS 框架对比与实战**：
   - **[[AutoGen]]**：微软出品，核心类为 ConversableAgent 与 UserProxyAgent。天然内嵌代码沙箱执行器与 custom_speaker_selection 状态机发言机制，是自动编程与 Coding 的首选工具。
   - **[[CrewAI]]**：通过 Agents-Tasks-Crews-Flows 结构，结合串行编排（Process.sequential）和清晰的期望输出设定，非常适合岗位专业化分工的复杂流程自动化（如技术媒体“搜集-分析-写稿-主编审校发布”编辑部流程）。

---
**关联页面**：
- [[AI-Agent]] (新建核心概念)
- [[LangChain-Agent-Runtime]] (新建核心概念)
- [[Agent-Middleware]] (新建概念)
- [[AutoGen]] (新建框架实体)
- [[CrewAI]] (新建框架实体)
- [[LlamaIndex]] (关联框架)
- [[RAG]] (关联基础环境)
