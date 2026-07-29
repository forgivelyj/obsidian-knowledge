---
title: "MCP"
aliases: [mcp, 模型上下文协议, Model Context Protocol]
tags: [ai/protocol/active]
category: entities
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/MCP-模型上下文协议/MCP-模型上下文协议.md]]"
description: "模型上下文协议 (Model Context Protocol, MCP) 是由 Anthropic 主导开源的标准化上下文连接协议，被称为 AI 领域的 USB-C 标准接口。"
---

# 模型上下文协议 (MCP)

**模型上下文协议 (Model Context Protocol, MCP)** 是由 Anthropic 于 2024 年主导并开源的标准化大语言模型数据交换协议。

---

## 1. 核心理念与痛点解决
在 MCP 问世之前，每当需要将私有数据源（如本地文件夹、PostgreSQL 数据库、Slack、GitHub）对接到特定大语言模型（如 GPT-4, Claude 3.5, Llama 3）时，开发者都必须为特定的模型宿主应用手写定制化的工具接口（[[MCP-Core-Protocol-Elements|Tools]]）和提示词参数。当数据源和服务数量上升至几十上百个时，网状连接会带来灾难性的维护开销。

```text
  [ 传统网状连接 (硬编码) ]                [ MCP 标准连接 (插拔式) ]
  
   大模型 A ─── 数据库                      大模型 A ──┐
   大模型 B ─── Slack                       大模型 B ──┼─► [ MCP 协议规范 ] ◄─┐
   大模型 C ─── GitHub                      大模型 C ──┘                    │
                                                                           ├─ 数据库
                                                                           ├─ Slack
                                                                           └─ GitHub
```

- **“AI 界的 USB-C 接口”**：
  - MCP 提供了一个通用的通信接口。
  - **Host/Client** 类似于“电脑”（如 Claude Desktop、Cursor、VSCode 等客户端应用）。
  - **Server** 类似于“USB 设备”（如暴露本地操作权限的脚本或远程 API 数据库服务）。
  - 大模型宿主应用只要适配了 [[MCP-Host-Client-Server|MCP Client]]，就可以即插即用地连接到任何暴露了 [[MCP-Host-Client-Server|MCP Server]] 的数据源，无需为每个模型或客户端定制开发。

---

## 2. MCP 的双层协议模型
- **数据层 (Data Layer)**：
  - 基于标准的 **JSON-RPC 2.0** 通信格式。
  - 核心工作是定义和传递生命周期事件（连接初始化、能力协商）、核心协议三剑客（[[MCP-Core-Protocol-Elements|Resources]] 资源、[[MCP-Core-Protocol-Elements|Tools]] 工具、[[MCP-Core-Protocol-Elements|Prompts]] 提示词）的数据负载结构与事件通知。
- **传输层 (Transport Layer)**：
  - 关注具体的数据交换物理通道（标准输入输出 [[MCP-Transport-Modes|Stdio]]、[[MCP-Transport-Modes|Streamable HTTP]] 全双工流等），负责建立物理连接、消息打包和分发鉴权。

---
**关联页面**
- [[MCP-Host-Client-Server]] (宿主与客户端拓扑)
- [[MCP-Core-Protocol-Elements]] (协议三大核心组件)
- [[MCP-Transport-Modes]] (底层物理传输模式)
- [[MCP-FastMCP-LangChain]] (开发框架与 LangChain 接入适配)
