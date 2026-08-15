---
title: "01-RAG基础-summary"
aliases: [RAG基础摘要, RAG Basics Summary]
tags: [ai/rag/active]
category: summaries
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/01-RAG基础/01-RAG基础.md]]"
description: "介绍 RAG（检索增强生成）的基础概念、工作流程（索引、检索、生成），Naive RAG 细节（文档分块策略），向量与 Embedding 的概念与计算，以及常用向量数据库（如 ChromaDB）和 Redis 的检索应用。"
---

# 01-RAG基础 摘要

## 概要说明
本素材为 [[RAG]] 开发学习的基础教程，系统讲述了为什么要引入 [[RAG]]、什么是 [[RAG]] 及其三种范式演进（朴素、高级、模块化），并详细展开了 Naive [[RAG]]、向量表征、相似度算法与[[Vector-Database|向量数据库]]的应用开发。

## 核心要点
1. **LLM 的局限性与 [[RAG]] 引入**：
   - 幻觉现象（受训练数据噪声影响，概率优先而非事实正确性优先）。
   - 知识更新缓慢与时效性约束。
   - 领域/专有知识理解有限（广度优先，特定专业数据稀疏）。
   - **[[RAG]]（[[RAG|检索增强生成]]）** 相当于“开卷考试”，通过向 LLM 注入检索出的本地专有知识片段来消除上述缺陷。
2. **Naive [[RAG]] 三阶段流程**：
   - **索引化（Indexing）**：文档 $\rightarrow$ 清洗 $\rightarrow$ 切分分块（Chunking） $\rightarrow$ 向量化（[[Embedding]]） $\rightarrow$ 存入向量库。
   - **检索（Retrieval）**：用户问题向量化 $\rightarrow$ 计算相似度距离 $\rightarrow$ 匹配召回 Top-K 文本块。
   - **生成（Generation）**：Prompt 拼接（问题 + Top-K 文本块上下文） $\rightarrow$ 送入 LLM 生成回答。
3. **数据向量表征与计算**：
   - 表示学习（Representation Learning）：低维稠密向量转换。
   - 相似度度量：余弦相似度（Cosine）、欧氏距离（L2）、点积（Dot Product）。
4. **数据库检索实践**：
   - [[Vector-Database|向量数据库]]：以 **[[ChromaDB]]** 为代表的轻量级向量库开发（add, get, delete, update, query）。
   - 内存数据库：以 **[[Redis]]** 为代表的键值检索（通过模糊 Key 匹配搜索文档）。

---
**关联页面**：
- [[RAG]] (核心概念)
- [[Naive-RAG]] (概念)
- [[Embedding]] (概念)
- [[Vector-Database]] (概念)
- [[ChromaDB]] (工具实体)
- [[Redis]] (工具实体)
