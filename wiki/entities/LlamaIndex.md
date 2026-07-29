---
title: "LlamaIndex"
aliases: [GPT Index, llamaindex]
tags: [ai/framework/active]
category: entities
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/02-llama_index框架/02-llama_index框架.md]]"
description: "LlamaIndex 是目前大语言模型生态中最主流、最成熟的开源私有数据整合框架，专注于提供高效的数据输入、检索、索引及多智能体编排接口。"
---

# LlamaIndex

LlamaIndex（原名 GPT Index）是构建大模型 [[RAG]]（[[RAG|检索增强生成]]）与 Agent 应用的行业标准基础设施。

## 发展历程
- **起源**：2022 年底，联合创始人 Jerry Liu 针对大语言模型无法处理私有数据与知识时效性断层的痛点，提交了首行代码（当时称为 GPT Index，主打树状索引结构）。
- **重构**：2023 初正式改名 LlamaIndex 并设立商业化公司，推出了数据加载仓库 **LlamaHub**。
- **Agentic 演进**：2025-2026 年，框架进行了颠覆性重构，推出了支持事件驱动和异步编排的 **LlamaIndex Workflows**，并全面支持 Agentic [[RAG]]（主动检索[[AI-Agent|智能体]]）与分布式微服务多[[AI-Agent|智能体]]（LlamaAgents）。

## 核心架构组成
LlamaIndex 的内部设计围绕以下六大支柱开展：
1. **数据摄入（Data Ingest）**：通过各式 Reader 将数据源（PDF、Word、网页、Slack、Notion 等）读取并规整为包含元数据（Metadata）的统一 `Document` 容器。
2. **高精度文档解析**：利用云端视觉引擎 **[[LlamaParse]]** 解决表格、排版及 OCR 识别痛点。
3. **数据分块（Node Parsing）**：通过不同类型的分割器（如 `SentenceSplitter`、`MarkdownNodeParser`）将文档拆分成携带双链关系（`relationships`）的原子 `Node`。
4. **存储管理（[[Storage-Context]]）**：通过 Docstore、VectorStore、IndexStore 等组件管理向量和元数据的物理落盘。
5. **检索与答案合成**：由 `Retriever` 在索引空间内快速召回 Node 块，并交由 `Response Synthesizer` 进行答案加工（如 Refine、Tree Summarize 合并策略）。
6. **交互引擎（[[Query-Engine]]）**：对外提供一键调用的单轮 `QueryEngine`，以及带有上下文会话记忆（Memory）的多轮 `ChatEngine`。

---
**关联页面**：
- [[RAG]] (架构基础)
- [[LlamaParse]] (数据解析产品)
- [[Storage-Context]] (存储体系)
- [[Query-Engine]] (交互引擎)
