---
title: "02-llama_index框架-summary"
aliases: [LlamaIndex框架摘要, LlamaIndex Summary]
tags: [ai/framework/active]
category: summaries
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/02-llama_index框架/02-llama_index框架.md]]"
description: "介绍大模型主流数据框架 LlamaIndex 的发展历史、核心架构与全局 Settings 配置；详细拆解了 LlamaIndex 文本分割（Node Parser）、高精度云端解析服务 LlamaParse、三位一体存储系统（StorageContext）、常用检索器、响应合成器（Response Synthesizer）与多轮对话聊天引擎的开发实践。"
---

# 02-llama_index框架 摘要

## 概要说明
本素材是目前主流大模型私有数据整合框架 **[[LlamaIndex]]** 的进阶开发教程。内容覆盖其发展史与 2025-2026 最新 Workflows/Agent 演进，重点解析了文档处理（[[LlamaParse]] 云端 OCR 提取）、文本分割（SentenceSplitter、HTML/JSON/MD 节点解析）、数据存储中枢（[[Storage-Context|StorageContext]] 三大子存储）、检索器机制（BM25、Hybrid、AutoMerging）、响应合成器策略（Refine、Tree Summarize）以及带记忆持久化（RedisChatStore）的多轮对话[[Query-Engine|聊天引擎]]（Chat Engine）开发。

## 核心要点
1. **[[LlamaIndex]] 核心架构与配置**：
   - 灵魂人物：Jerry Liu（创始人兼 CEO，Robust Intelligence/Uber 背景）。
   - 2025-2026 年演进重点：Workflows 事件驱动异步架构与 Agentic [[RAG]]。
   - 全局单例 **`Settings`** 配置：统一管理默认的 LLM、[[Embedding]] 与 Node Parser。
   - 新一代 Jinja2 提示词模板 **`RichPromptTemplate`**：支持条件分支与多模态图片编码（`| image` 管道）。
2. **文档处理与节点解析**：
   - 数据实体层级：`Document`（元数据容器） $\rightarrow$ **`Node Parser`** $\rightarrow$ `Node`（携带 relationships 双向关系的原子块）。
   - **[[LlamaParse]]**：[[LlamaIndex]] 官方提供的高精度云端解析引擎，通过 Vision 视觉模型和自愈机制实现复杂表格转 Markdown、扫描件 OCR 与版面还原。
3. **存储中枢 [[Storage-Context|StorageContext]]**：
   - **Docstore**（文档存储）：保存原始 Node 文本（如内存、MongoDB）。
   - **VectorStore**（向量存储）：保存向量表征（如内存、[[ChromaDB]]）。
   - **IndexStore**（索引存储）：保存索引结构信息。
4. **检索与答案合成**：
   - **Retrievers（检索器）**：从索引中召回 `NodeWithScore`。典型包括向量、BM25 关键字、以及混合检索（Hybrid）。
   - **Response Synthesizer（响应合成器）**：加工检索到的多个文本块生成回答。模式有 `compact`（拼接）、`refine`（迭代优化解决超长上下文）、`tree_summarize`（分层树状总结）。
5. **[[Query-Engine|查询引擎]]与[[Query-Engine|聊天引擎]]**：
   - **[[Query-Engine]]**（[[Query-Engine|查询引擎]]）：单轮问答（Query $\rightarrow$ Retrieve $\rightarrow$ Synthesize $\rightarrow$ LLM）。
   - **Chat Engine**（[[Query-Engine|聊天引擎]]）：有状态的多轮对话（Query Engine + Memory 记忆）。支持 `CondensePlusContext` 自动重写并检索机制。可以通过 `RedisChatStore` 等组件进行会话持久化。

---
**关联页面**：
- [[LlamaIndex]] (核心实体框架)
- [[LlamaParse]] (工具服务实体)
- [[Storage-Context]] (概念)
- [[Query-Engine]] (概念)
- [[RAG]] (关联概念)
- [[ChromaDB]] (关联向量库)
