---
title: "MCP-模型上下文协议-summary"
aliases: [MCP 协议编译摘要, MCP Summary]
tags: [ai/protocol/active]
category: summaries
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/MCP-模型上下文协议/MCP-模型上下文协议.md]]"
description: "系统总结由 Anthropic 主导开源的模型上下文协议 (MCP) 核心内容，拆解 Host-Client-Server 拓扑架构、三剑客要素、物理传输通道演进与 LangChain 生态适配。"
---

# [[MCP]]-[[MCP|模型上下文协议]] 摘要

## 概要说明
本素材是关于大模型通用上下文连接规范 **[[MCP]]**（[[MCP|模型上下文协议]]）的系统说明与开发指南。深入阐述了 [[MCP]] 作为 AI 界 “USB-C” 接口的标准设计理念，详解了 **[[MCP-Host-Client-Server]]** 集中控制下的 Host 主机、Client 客户端（含 [[MCP-Host-Client-Server|Roots]] 资源边界、Elicitation 界面渲染、与 [[MCP-Host-Client-Server|Sampling]] 反向采样机制）与 Server 服务端；剖析了 **[[MCP-Core-Protocol-Elements]]** 中的只读静态 [[MCP-Core-Protocol-Elements|Resources]]、带参数副作用的主动 [[MCP-Core-Protocol-Elements|Tools]] 与 SOP 对话模板 [[MCP-Core-Protocol-Elements|Prompts]]；对比了 **[[MCP-Transport-Modes]]** 数据层 JSON-RPC 2.0 与传输层的 [[MCP-Transport-Modes|Stdio]] 管道、旧版 [[MCP-Transport-Modes|SSE]] HTTP 与新一代 [[MCP-Transport-Modes|Streamable HTTP]] 全双工模式；并归纳了 **[[MCP-FastMCP-LangChain]]** 在 [[MCP-FastMCP-LangChain|FastMCP]] 极简声明、Low-Level 底层协议实现以及 LangChain 生态适配适配中的具体架构开发手段。

## 核心要点
1. **[[MCP]] 的标准隐喻与核心痛点**：
   - *痛点*：多数据源（文件、数据库、Slack）与多大模型之间网状硬编码连接极度混乱，重复造轮子。
   - *标准*：**[[MCP]]** 提供标准的 JSON-RPC 通信网络。大模型宿主应用作为 Client，数据源/服务作为 Server，实现即插即用的通用适配，极大提升认知生态的可维护性。
2. **三位一体的主机-客户端-服务端拓扑**：
   - **[[MCP-Host-Client-Server]]**：
     - *Client 核心职责*：Host 通过 Client 连接各个 Server。Client 定义了 **[[MCP-Host-Client-Server|Roots]]（资源边界）** 以限制 Server 的越权访问（安全基石）；通过 **Elicitation（信息引出）** 将提示词模板渲染为 UI 用户输入表单；利用 **[[MCP-Host-Client-Server|Sampling]]（采样机制）** 允许 Server 反向租借 Client 的大模型算力，打造具备 Agentic 能力的智能工具。
     - *Server 核心职责*：只专注暴露特定领域能力，监听 JSON-RPC 管道指令并返回响应。
3. **协议三大核心要素 (三剑客)**：
   - **[[MCP-Core-Protocol-Elements]]**：
     - *[[MCP-Core-Protocol-Elements|Resources]] (资源)*：静态、只读的被动数据块，通过自定义 URI 协议（如 `health://`）和 MIME 映射暴露，充当私有档案柜，抑制 AI 幻觉。
     - *[[MCP-Core-Protocol-Elements|Tools]] (工具)*：动态、主动的可执行操作。带有严格的输入 JSON Schema 校验，常用于触发副作用（写库、重启服务、调用外部 API），是 AI 的执行义肢。
     - *[[MCP-Core-Protocol-Elements|Prompts]] (提示词)*：预设的 SOP 对话剧本。支持参数动态注入，渲染为标准的 UI 表单，充当 AI 人设与标准操作规程（SOP）开关。
4. **网络传输层的物理传输演进**：
   - **[[MCP-Transport-Modes]]**：
     - *[[MCP-Transport-Modes|Stdio]] (标准输入/输出)*：本地客户端首选。Client 将指令写入 Server 的 `stdin`，Server 将结果输出到 `stdout`，而调试日志必须走 `stderr` 以防协议内容受到污染。
     - *HTTP with [[MCP-Transport-Modes|SSE]] (旧过渡标准)*：双通道设计。GET 接收 [[MCP-Transport-Modes|SSE]] 推送，POST 发送消息，状态会话维护繁琐且难以支持标准 Auth Header 鉴权，目前已被官方弃用。
     - *[[MCP-Transport-Modes|Streamable HTTP]] (新终极标准)*：单通道全双工模拟。通过标准的 POST 连接保持长效流式传输，简化了 Session 缓存，对防火墙及 HTTP Auth 鉴权机制友好。
5. **开发框架与第三方适配器**：
   - **[[MCP-FastMCP-LangChain]]**：
     - 官方高层封装 **[[MCP-FastMCP-LangChain|FastMCP]]** 基于 Python 类型提示和函数 Docstring 自动提取生成 Schema 配置。
     - 低层 API 需要开发者手动编写 JSON-RPC 响应分发与 URI 正则匹配。
     - LangChain 适配库 `langchain-mcp-adapters` 可以将多路 [[MCP-Transport-Modes|StdIO]] [[MCP]] 服务器的可用 [[MCP-Core-Protocol-Elements|Tools]] 合并转换，为 LangChain Agent 提供跨服务器的工具调用底座。

---
**关联页面**：
- [[MCP]] (新建实体页)
- [[MCP-Host-Client-Server]] (新建概念页)
- [[MCP-Core-Protocol-Elements]] (新建概念页)
- [[MCP-Transport-Modes]] (新建概念页)
- [[MCP-FastMCP-LangChain]] (新建概念页)
- [[AI-Agent]] (多[[AI-Agent|智能体]]工具底座)
- [[LangChain-Agent-Runtime]] (可接入 [[MCP]] 服务器工具的运行时)
- [[OpenSandbox]] (本地物理工具执行沙箱)
