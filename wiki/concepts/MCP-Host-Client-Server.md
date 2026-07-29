---
title: "MCP-Host-Client-Server"
aliases: [MCP Host, MCP Client, MCP Server, Roots, Sampling]
tags: [ai/protocol/active]
category: concepts
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/MCP-模型上下文协议/MCP-模型上下文协议.md]]"
description: "MCP-Host-Client-Server 阐述三位一体的客户端-服务端拓扑架构，详解 Roots 资源边界、Elicitation 渲染表单、与 Sampling 反向采样。"
---

# [[MCP]] 客户端与服务端架构 (Host-Client-Server)

**[[MCP]]** 协议采用非对称的**客户端-服务器（Client-Server）拓扑架构**，通过在宿主程序中建立多路客户端实例来管理与各个独立领域微型服务的连接。

---

## 1. 架构三剑客定义与生命周期

```text
  ┌─────────────────────────┐
  │      MCP Host 主机      │ (如 Claude Desktop, Cursor 等 IDE 宿主)
  │  ┌───────────────────┐  │
  │  │   MCP Client 1    ├──┼───────► [ MCP Server 1 (文件系统操作) ]
  │  ├───────────────────┤  │
  │  │   MCP Client 2    ├──┼───────► [ MCP Server 2 (PostgreSQL) ]
  │  └───────────────────┘  │
  └─────────────────────────┘
```

- **[[MCP]] Host (宿主主机)**：
  - 用户的顶层 AI 应用界面（如 Cursor、Claude Code、Cherry Studio、Claude Desktop）。它负责统一调度大语言模型，并协调内部一个或多个 [[MCP]] 客户端与外部硬件/服务的互通。
- **[[MCP]] Client (客户端)**：
  - 运行在 Host 内部的网关层组件。每个 Client 实例与特定的 [[MCP]] Server 建立一对一的专用管道连接，负责列出 Server 暴露的能力并将其转换呈现给 Host 大模型。
- **[[MCP]] Server (服务端)**：
  - 一个轻量级、专注于特定功能领域（如“文件读写”、“SQLite数据库查询”、“GitHub管理”）的程序。它对外公开核心组件（[[MCP-Core-Protocol-Elements|Resources]], [[MCP-Core-Protocol-Elements|Tools]], [[MCP-Core-Protocol-Elements|Prompts]]），不关心调用它的模型类型，只按照标准 JSON-RPC 协议解析指令。

---

## 2. [[MCP]] Client 的三大关键职责（安全与智能机制）

为了防止外部工具破坏本地安全，或者令 Server 不具备自演进的决策能力，[[MCP]] Client 承担了以下三大关键设计角色：

### ① 根路径与资源边界限制 (Roots)
- **概念**：它是 [[MCP]] 的**安全基石**。
- **作用**：Client 在与 Server 完成连接握手时，必须同步发送允许访问的“根路径列表”（Roots）。Server 收到根路径后，只能在其允许的工作空间（Workspace）边界内读取或写入文件。任何超出 Roots 列表的文件请求都将被 Server 拒绝，以此防范工具恶意越权修改系统隐私数据。

### ② 诱导式信息引出与表单渲染 (Elicitation)
- **概念**：通过 UI 界面协助大模型和人类补全复杂的调用模板参数。
- **作用**：Server 会提供特定结构化 SOP 模板（[[MCP-Core-Protocol-Elements|Prompts]]）。Client 负责捕获这些 [[MCP-Core-Protocol-Elements|Prompts]]，并将其在 Host 界面中渲染为交互式表单（输入框、下拉菜单）。用户填完必要的表单参数后，由 Client 打包提交给大模型作为上下文，优化[[LangGraph-Human-In-The-Loop|人机交互]]。

### ③ 智能采样与“反向租借大脑” (Sampling)
- **概念**：这是传统 [[MCP-Core-Protocol-Elements|Tools]] 设计中所没有的**反向调用设计**。
- **作用**：通常是 Client 调度 Server 执行任务。但在复杂推理中，允许 Server 在运行途中反向向 Client 发起请求：“请借你的大模型脑子帮我提取/总结这一段长文本”。
- **价值**：**赋予了 Tool 工具以 Agentic（[[AI-Agent|智能代理]]）的自主能力**。Server 从单纯的无脑脚本退化转变成可以自我推理、调用 AI 生成摘要后继续处理的自主代理工具。

---
**关联页面**
- [[MCP]] (协议实体)
- [[MCP-Core-Protocol-Elements]] (协议内的三大基本组件)
- [[MCP-Transport-Modes]] (底层的物理消息流传输)
