---
title: "Agent-Middleware"
aliases: [智能体中间件, before_agent, after_model]
tags: [ai/agent/active]
category: concepts
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/Agent智能体/Agent智能体.md]]"
description: "Agent-Middleware（智能体中间件）是控制和规范智能体运行期数据与行为的质量安全拦截机制，通过注入钩子函数实现流量监管、提示词增强与 JSON 自愈纠错。"
---

# Agent Middleware ([[AI-Agent|智能体]]中间件系统)

大模型的输出具备极强的随机性，工具调用链路也极易发生偏离或错误。为了防范敏感用词、进行细粒度权限控制并在最终返回给用户前对乱序文本进行自愈，LangChain 1.0 引入了**[[AI-Agent|智能体]]中间件系统（Agent Middleware）**。

中间件类似于传统软件工程中的“面向切面编程（AOP）”，是在[[AI-Agent|智能体]]执行流程的各个关键生命周期节点织入的“安全防护网”。

---

## 1. 中间件的六大生命周期钩子
在[[AI-Agent|智能体]]、模型与工具的调用环路中，中间件可以拦截并处理以下六大关键步骤：

```text
                  [before_agent] ──► (Agent 开始)
                        │
                        ▼
                  [before_model]
               [wrap_model_call] ──► (调用大模型)
                        │
                        ▼
                  [after_model]
                        │
                        ▼
                  [wrap_tool_call] ──► (调用外部工具)
                        │
                        ▼
                  [after_agent] ──► (Agent 结束，返回输出)
```

1. **`before_agent`**：在整个代理执行开始前被调用。常用来做用户输入的安全检测。如果包含敏感词，可以通过 `can_jump_to="end"` 携带自定义友好回复直接阻断流转。
2. **`before_model`**：在调用大模型前执行。常用来做上下文状态裁剪，或从数据库读取偏好并静态注入到 Model 请求的消息列表中。
3. **`wrap_model_call`**：最强的大模型包装器。可以完全覆盖大模型的 invoke 请求。通过 `request.override(system_message=...)` 临时性替换 Prompt 人设（仅对当次请求有效，不污染 Chat History）。
4. **`after_model`**：在大模型完成推理后、进入工具调用或输出前执行。主要用于数据的强制性格式验证与修复。
5. **`wrap_tool_call`**：包装并干预工具调用。可用于在执行计算、搜索等工具时记录日志或捕获异常。
6. **`after_agent`**：在代理全流程执行完毕、准备将响应送回客户端前执行。可用于统一日志埋点与敏感词二次过滤。

---

## 2. 核心业务实战场景：JSON 结构格式化自愈
- **痛点**：在要求大模型进行 [[RAG-Project-Architecture]] 中的结构化输出（Structured Output）时，大模型经常返回带有 ` ```json ` 标签的 Markdown 文本，或由于输出中断产生“末尾多余逗号”等错误的 JSON，直接抛出 `JSONDecodeError` 导致下游业务节点雪崩。
- **中间件方案**：使用 `after_model` 钩子拦截模型的 `AIMessage`：
  1. 通过正则表达式自动抹除首尾的 Markdown 标签 ```json。
  2. 使用正则修复属性列表末尾由于多余解析产生的 `,`（如 `,"items":["a",],}` 修复为 `,"items":["a"]}`）。
  3. 引号补全：对于漏写引号的 key，自动捕获并加上双引号。
  4. 将修复好的纯净字符串重新赋值给 `AIMessage.content` 送往下游，实现工程级的自愈。

---

## 3. 中间件的两类开发方式
- **装饰器函数**：
  使用 `@before_agent`、`@after_model` 装饰普通 Python 函数。语法简单、适合单一拦截点的快速验证。
- **继承 `AgentMiddleware` 类**：
  支持在 `__init__` 构造函数中传入数据库连接、敏感词库等外部配置。支持同时实现同步与异步钩子，是企业级[[AI-Agent|智能体]]系统复用的推荐方案。

---
**关联页面**
- [[AI-Agent]] (概念母体)
- [[LangChain-Agent-Runtime]] (状态与运行时协同)
- [[RAG-Project-Architecture]] (涉及的数据流安全场景)
