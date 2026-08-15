---
title: "MCP-Transport-Modes"
aliases: [Stdio, SSE, Streamable HTTP, 物理传输通道]
tags: [ai/protocol/active]
category: concepts
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/MCP-模型上下文协议/MCP-模型上下文协议.md]]"
description: "MCP-Transport-Modes 详解 MCP 底层三类物理传输机制，横向对比本地 Stdio 管道、已弃用的 Web SSE 双通道、与新一代 Streamable HTTP 全双工流。"
---

# [[MCP]] 物理传输通道与传输模式 (Transport Modes)

[[MCP|模型上下文协议]] **[[MCP]]** 在逻辑上依赖基于 JSON-RPC 2.0 的数据交换，但在物理底座上，它设计了三类不同的**传输通道 (Transport Modes)**，用以适配本地集成与分布式远程网关环境。

---

## 1. 三种传输通道深度对比

| 传输模式 | 运行机制 | 生命周期 | 适用场景 | 优缺点 |
| :--- | :--- | :--- | :--- | :--- |
| **Stdio** | 客户端拉起子进程，通过标准输入输出（`stdin`/`stdout`）传递 JSON 帧，`stderr` 输出日志。 | 与本地子进程生命周期严格绑定。 | 本地开发、单机脚本集成（如文件读写、本地库访问）。 | **优**：零网络开销，配置极简。<br>**缺**：无法跨物理机进行分布式部署。 |
| **HTTP with SSE** | (官方已弃用) GET 请求保持连接接收 SSE 推送，客户端发送消息走独立 POST 管道，通过 Session ID 强行路由。 | 由服务端根据 Session ID 缓存生命周期。 | 浏览器沙箱环境、跨域连接过渡方案。 | **优**：对浏览器跨域友好。<br>**缺**：收发双通道容易形成“能发不能收”的半挂连接；状态机制重；无法传输复杂 Auth 头。 |
| **Streamable HTTP** | (推荐新标准) 基于标准 HTTP POST。客户端发起请求，服务端不关通道，逐行流式回传结果。 | 无状态长连接，随 HTTP 长连接断开。 | 企业级网关、远程 API 调用、分布式云端服务部署。 | **优**：防火墙极度友好；支持标准 Token 鉴权（Bearer Header）；服务端无状态开销。<br>**缺**：需要处理长连接保活（Keep-Alive）与网络波动。 |

---

## 2. 物理通道设计规范与要点

### ① 本地 Stdio 管道下的 stdout 与 stderr 隔离设计
在 Stdio 传输模式中，客户端作为父进程启动服务器脚本（子进程）。
- **发送路径**：Client 写入 JSON-RPC 指令到 Server 子进程的 **`stdin`**（标准输入）。
- **接收路径**：Server 执行指令并将 JSON-RPC 结果数据通过 **`stdout`**（标准输出）打印返回。
- **日志输出 (关键原则)**：**所有的调试信息、状态变更、系统错误必须强制打印到 `stderr` (标准错误输出)**。如果开发者在 Server 中写了 `print("Executing...")` 将其打到了 `stdout`，将会污染 JSON-RPC 消息流，直接导致 Client 协议解析器崩溃断开。

### ② 新一代 Streamable HTTP 的无状态优势
旧版的 SSE 过渡方案最大的缺陷是“收发分离”（GET 创建连接，POST 发送数据），导致服务器必须以很大的内存代价维护 Session ID 的映射状态，且在企业网络中容易被代理服务器挂断。
- **Streamable HTTP** 改变了这一架构，仅公开单一的 HTTP Endpoint（如 `/mcp`）。客户端直接发送 POST 请求发送消息，服务端以 Stream 流式输出（如同 LLM 打字机输出效果）在同一个 HTTP 连接中将数据吐回。
- *安全利好*：由于是标准的单向长连接 HTTP 请求，它能够完美复用 OAuth 2.0、JWT 等成熟的安全防火墙设施，直接在 Request Header 中注入 `Authorization: Bearer <Token>` 进行精细化网关鉴权。

---
**关联页面**
- [[MCP]] (协议实体)
- [[MCP-Host-Client-Server]] (拓扑架构)
- [[OAuth-2.0]] (用于远程 Streamable HTTP 的鉴权底座)
