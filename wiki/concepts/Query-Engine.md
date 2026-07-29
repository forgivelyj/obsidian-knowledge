---
title: "Query-Engine"
aliases: [查询引擎, Chat-Engine, 聊天引擎]
tags: [ai/framework/active]
category: concepts
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/02-llama_index框架/02-llama_index框架.md]]"
description: "查询引擎是 LlamaIndex 中用于单轮无状态问答的最高级交互接口；而聊天引擎是融合了会话记忆、支持多轮有状态问答的查询引擎。"
---

# Query Engine 与 Chat Engine

在 [[LlamaIndex]] 框架中，**Query Engine（查询引擎）** 和 **Chat Engine（聊天引擎）** 是直接面向最终用户（或应用前端）的两个最高层级的交互抽象类。它们统筹了检索（Retriever）、拼装和推理生成（Response Synthesizer）的全部工作流。

---

## 1. Query Engine (查询引擎)：单轮无状态 [[RAG]]
查询引擎用于**“一问一答”**的无状态场景，每次查询都是独立的，不记得之前的对话历史。

### 核心工作原理
```text
用户提问 ──► Retriever(检索器) ──► 召回 NodesWithScore 
                                           │
                                           ▼
用户提问 ◄── LLM 推理生成 ◄── Response Synthesizer(答案合成)
```

### 响应合成模式 (Response Mode)
在答案合成器中，面对多份召回的 Node 文本片段，可以使用不同的编排模式喂给大模型：
- **`compact`（默认）**：直接把所有 Node 文本拼接成一个长 Context 喂给 LLM。速度最快，但如果 Node 太多容易超出 Token 限制。
- **`refine`（迭代式优化）**：先用第 1 个 Node 生成初始答案，然后把该答案作为背景，结合第 2 个 Node 交给 LLM 迭代修正，以此类推。适合超长文本，但调用 LLM 次数多、较慢。
- **`tree_summarize`（树状合并）**：将 Nodes 分组总结，将各组总结再两两合并，直至合并成最后一个连贯的总结答案。适合宏观的长文档总结。

---

## 2. Chat Engine (聊天引擎)：多轮有状态 [[RAG]]
聊天引擎是带有 **Memory（会话记忆）** 的查询引擎，适用于聊天机器人（Chatbot）或[[AI-Agent|智能体]]（Agent）场景。

### 常见的聊天引擎模式
- **`SIMPLE`**：仅使用 `Memory + LLM`，只支持纯聊天，不接入任何知识检索。
- **`CONTEXT`**：标准的 [[RAG]] 聊天。每次提问不仅结合历史记忆，还会检索向量库中的背景上下文。
- **`CONDENSE_QUESTION`**：问题改写引擎。它读取历史对话，把用户当前含糊不清的问题（如“它比他高多少？”）利用 LLM 自动改写为一个完整的、自包含的问题（如“萧薰儿的斗之力比萧炎高多少？”），然后去向量库里做纯向量检索。
- **`CONDENSE_PLUS_CONTEXT`（企业级最推荐）**：结合问题改写与上下文拼装，能够实现极其平滑的 [[RAG]] 多轮交互。

---

## 3. 记忆存储器 (Memory & ChatStore)
聊天引擎的上下文记忆需要用 `Memory` 进行存储，默认使用内存中的 **`ChatMemoryBuffer`**。
为了实现跨会话和程序重启后的记忆恢复，可以引入 **`ChatStore`（记忆数据库，如 `RedisChatStore`）** 进行持久化：

```python
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.storage.chat_store.redis import RedisChatStore

# 创建 Redis 记忆数据库连接
chat_store = RedisChatStore(redis_url="redis://localhost:6379")

# 将记忆与特定用户 session 绑定
memory = ChatMemoryBuffer(
    token_limit=1500,
    chat_store=chat_store,
    chat_store_key="user_session_1001"
)

# 传入聊天引擎，完成多轮记忆持久化
chat_engine = index.as_chat_engine(
    chat_mode="condense_plus_context",
    memory=memory
)
```

---
**关联页面**：
- [[LlamaIndex]] (所归属的框架)
- [[RAG]] (工程应用场景)
- [[Redis]] (常用的记忆持久化工具)
- [[Storage-Context]] (底座存储)
