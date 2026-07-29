---
title: "DeepAgent框架-summary"
aliases: [DeepAgents 框架编译摘要, DeepAgent Summary]
tags: [ai/framework/active]
category: summaries
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/DeepAgent框架/DeepAgent框架.md]]"
description: "系统总结企业级智能体套件 DeepAgents 核心架构，拆解文件后端系统（CompositeBackend）与权限中断机制，剖析 OpenSandbox 沙箱适配器，并对比分层子代理（Subagent）的两种上下文隔离方案。"
---

# DeepAgent框架 摘要

## 概要说明
本素材是关于 LangChain 官方在 2025 年后推出的企业级[[AI-Agent|智能体]]开发套件 **[[DeepAgents]]**（[[DeepAgents|深度智能体]]）的系统指南。本指南深入探讨了基于 [[LangGraph]] 的 Harness（套件）架构体系，详解了五类文件系统存储后端（包括生产推荐的 **[[DeepAgents-Backend]]** 路由器 [[DeepAgents-Backend|CompositeBackend]]）、文件权限安全拦截与人工审批（[[DeepAgents-Backend|FilesystemPermission]]）流程；演示了阿里开源安全沙箱 **[[OpenSandbox]]** 适配器接口的开发与 Docker 容器命令执行；并重点对比了解决上下文膨胀的 **[[DeepAgents-Subagent]]** 分层上下文隔离机制（字典式与 Compiled 编译图子代理）。

## 核心要点
1. **企业级 Agent 套件 Harness 定位**：
   - 传统 Agent 循环调用工具面临路径错乱、目标丢失和上下文超载。
   - **[[DeepAgents]]** 在底层的 [[LangGraph]]（基座，主打持久化与观测）和 LangChain（接口与中间件）之上进行了高层封装（`create_deep_agent`），预置一系列上下文压缩与状态管控的中间件。
2. **文件后端系统（Backends）与权限熔断**：
   - 文件操作工具底层依托不同后端实现：
     - `StateBackend`：文件作为原始字节，随短期 State 会话传递。
     - `FilesystemBackend`：映射到磁盘，支持 `virtual_mode=True` 安全锁定 root。
     - `StoreBackend`：将文件挂接在[[LangGraph-Long-Term-Memory|长期记忆]] `store` 中，支持跨线程读取。
     - `ContextHubBackend`：基于 LangSmith Context Hub 云端/本地持久化。
     - **`CompositeBackend`（复合后端）**：路由分发后端。通过将不同前缀路径（如 `/skills/`、`/memory/`）路由至不同的物理后端，使 Agent 在单一虚拟文件系统下无缝操作所有资源。
   - **人工确认熔断（[[DeepAgents-Backend|FilesystemPermission]]）**：支持 read/write 操作的 `mode="interrupt"`，触发后产生 `result.interrupts` [[LangGraph-Human-In-The-Loop|人机交互]]状态，恢复时使用 `Command(resume=...)` 进行决策接管。
3. **[[OpenSandbox]] 沙箱本地化与适配器设计**：
   - 沙箱（Sandbox）作为特殊的物理执行后端，额外支持 shell 命令执行工具（`execute`）。
   - **[[OpenSandbox]]**（阿里开源）为大模型代码执行提供 Docker 隔离容器。
   - 通过编写适配器类 `OpenSandboxBackend` 继承 `BaseSandbox` 抽象基类，将 [[OpenSandbox]] SDK 接口归一化映射为 [[DeepAgents]] 要求的命令执行、文件上传和文件下载协议。
4. **子代理（[[DeepAgents-Subagent|Subagent]]）与上下文隔离**：
   - 痛点：工具的中间冗余数据极度占用主代理上下文，导致推理变慢与精度下降。
   - 方案：通过 **[[DeepAgents-Subagent]]** 将工作负载和中间件数据隔离在子代理内部，主控仅提取精简 JSON 结论。
   - 实现形式：
     - *字典型子代理 ([[DeepAgents-Subagent|SubAgent]])*：无需构建图，以 Dict 键值形式轻量化声明角色人设与专属 [[MCP-Core-Protocol-Elements|Tools]]。
     - *编译图子代理 ([[DeepAgents-Subagent|CompiledSubAgent]])*：将已有复杂 [[LangGraph]] 状态图以 runnable 封装，接入 DeepAgent 执行链。
5. **上下文工程（Context Engineering）整合**：
   - 贯穿静态输入（Memory 约束，如前置加载 `AGENTS.md` 规范、Skills 延迟按需技能加载）、运行期只读 Context 注入、[[LangGraph-Long-Term-Memory|长期记忆]]跨线程持久化（[[LangGraph-Long-Term-Memory|InMemoryStore]] / [[LangChain-Agent-Runtime|PostgresSaver]]）以及子代理逻辑隔离的综合体系。

---
**关联页面**：
- [[DeepAgents]] (新建核心概念)
- [[DeepAgents-Backend]] (新建概念页)
- [[OpenSandbox]] (新建沙箱实体)
- [[DeepAgents-Subagent]] (新建概念页)
- [[LangChain-Agent-Runtime]] (关联的运行时)
- [[Agent-Middleware]] (关联的中间件机制)
- [[AutoGen]] (多[[AI-Agent|智能体]]对比)
