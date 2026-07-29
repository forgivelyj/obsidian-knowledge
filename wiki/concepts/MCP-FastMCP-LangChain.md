---
title: "MCP-FastMCP-LangChain"
aliases: [FastMCP, langchain-mcp-adapters, MultiServerMCPClient, Low-Level API]
tags: [ai/protocol/active]
category: concepts
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/MCP-模型上下文协议/MCP-模型上下文协议.md]]"
description: "MCP-FastMCP-LangChain 阐述 FastMCP 极简声明开发方式，与 LangChain 生态适配，详述 MultiServerMCPClient 工具适配整合。"
---

# [[MCP]] 框架开发与 LangChain 适配 (FastMCP & LangChain)

为了降低大模型开发者使用 **[[MCP]]** 协议的门槛，官方和主流框架生态（如 LangChain）提供了不同抽象层次的开发工具与适配器（Adapters）。

---

## 1. 极简开发 FastMCP 与底层 Low-Level 写法对比

在创建自定义 [[MCP-Host-Client-Server|MCP Server]] 时，Python 生态中有两种开发路线：

### ① 高层封装：FastMCP (官方推荐)
`fastmcp` 是一个声明式的开发框架，旨在让开发者专注于编写业务函数，而把 JSON Schema 生成与 JSON-RPC 路由细节完全掩盖在框架底层。
- **自动 Schema 生成**：FastMCP 极其智能，它能够自动读取 Python 函数的**类型提示**（如 `a: float, b: float`）以及函数的 **Docstring 文档注释**（包括参数解释和返回值类型），直接在后台拼装出符合 [[MCP]] 规范的标准 JSON Schema。
  ```python
  from fastmcp import FastMCP
  
  mcp = FastMCP("health-calculator")
  
  @mcp.tool()
  async def calculate_bmi(weight_kg: float, height_m: float) -> str:
      """计算 BMI 指数并返回健康建议。
      Args:
          weight_kg: 体重 (kg)
          height_m: 身高 (m)
      """
      bmi = weight_kg / (height_m ** 2)
      return f"BMI: {bmi:.2f}"
  ```

### ② 底层控制：Low-Level API
如果面临动态工具生成（如根据数据库中的表结构在运行时决定向外暴露哪些 [[MCP-Core-Protocol-Elements|Tools]]）、精细控制初始化协商、自定义订阅生命周期或特殊的安全性检测时，则必须使用 `mcp.server.Server` 提供的 Low-Level API。
- *代价*：需要开发者手工书写嵌套的 Pydantic 模型（如 `types.Tool`、`types.PromptArgument`），并手动对输入参数字典进行解析、做 URI 路由判定及回传标准消息结构。

---

## 2. 桥接到主流[[AI-Agent|智能体]]：LangChain 适配方案
在很多存量系统中，[[AI-Agent|智能体]]工作流（如 React Agent）是使用 LangChain 编排开发的。如何让既有的 LangChain [[AI-Agent|智能体]]直接调用 [[MCP-Host-Client-Server|MCP Server]] 的能力，而不需要将 [[MCP-Host-Client-Server|MCP Server]] 的代码全部重写为 LangChain BaseTool？

生态提供了适配器工具包 **`langchain-mcp-adapters`** 来完成这层无缝转化：

```text
  [ LangChain React Agent ]
             │ (ainvoke)
             ▼
  [ MultiServerMCPClient ] (适配转换网关)
   ├─► 读取并合并 fast-health-calculator 的 Tools ──► 转换成 BaseTool 格式
   ├─► 读取并合并 github-mcp-server 的 Tools ───► 转换成 BaseTool 格式
             │ (参数转发)
             ▼
   [ 远端/本地 Stdio MCP Server ]
```

1. **建立多服务器接入网关 (MultiServerMCPClient)**：
   - 适配器提供了 `MultiServerMCPClient`，支持将本地 [[MCP-Transport-Modes|Stdio]]、远程 HTTP 等多种传输协议下的多个 [[MCP-Host-Client-Server|MCP Server]] 一起注册进来。
2. **[[MCP-Core-Protocol-Elements|Tools]] 提取与统一适配**：
   - 调用 `client.get_tools()` 方法，适配器会自动发起握手协议，读取这几个 Server 所暴露的所有 [[MCP-Core-Protocol-Elements|Tools]]，并在内存中**无缝封装转换为标准的 LangChain BaseTool 实例**。
3. **Agent 正常绑定与调用**：
   - 转换后的 [[MCP-Core-Protocol-Elements|Tools]] 可以直接喂入 LangChain 的 `create_agent` 中。当 Agent 调用工具时，LangChain 引擎向 client 发送参数，client 将其包装成 [[MCP]] 标准 JSON-RPC 帧，通过物理管道（如 [[MCP-Transport-Modes|Stdio]] 写入子进程标准输入）发送给 [[MCP-Host-Client-Server|MCP Server]] 运行并回收结果，实现了 **“一次开发 [[MCP]]，多大模型与多开发框架完全复用”** 的工业级生态对齐。

---
**关联页面**
- [[MCP]] (协议实体)
- [[MCP-Host-Client-Server]] (交互拓扑)
- [[LangChain-Agent-Runtime]] (接入工具的 Agent 运行时)
- [[AI-Agent]] (多[[AI-Agent|智能体]]核心系统)
