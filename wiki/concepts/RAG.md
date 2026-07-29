---
title: "RAG"
aliases: [检索增强生成, Retrieval-Augmented Generation]
tags: [ai/rag/active]
category: concepts
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/01-RAG基础/01-RAG基础.md]]"
description: "RAG 是一种通过从外部知识库检索相关信息来增强大语言模型生成回答的准确性与事实性的技术架构。"
---

# RAG (检索增强生成)

RAG（Retrieval-Augmented Generation）是目前解决大语言模型（LLM）幻觉、时效性不足和缺乏私有领域知识的最主流、最具性价比的技术范式。

## LLM 面临的痛点
在没有 RAG 之前，大模型存在以下三大瓶颈：
1. **幻觉（Hallucination）**：大模型生成内容的机制是预测概率最高的下一个词（做概率填词游戏），而非追求绝对事实，因此在没有背景资料时经常凭空虚构。
2. **知识滞后**：模型的知识库被锁定在预训练结束的时间点（例如 2023 或 2024 年），无法实时更新。
3. **专有知识匮乏**：模型的语料以全网公开数据为主，对于公司内部文档、私人日记等隐私/垂直领域知识完全不理解。

## RAG 的隐喻与工作机制
RAG 相当于大模型的**“开卷考试”**。它在用户提问时，先通过检索手段从“教科书”（本地向量库、图数据库等）中翻找出相关的“段落”，然后把“段落”作为已知条件和“问题”一同提交给大模型，要求大模型在已知条件的约束下整理出最终答案。

## 范式演进阶段
根据论文《Retrieval-Augmented Generation for Large Language Models: A Survey》的梳理，RAG 的研究与发展经历了三个演进阶段：
1. **[[Naive-RAG]]（[[Naive-RAG|朴素 RAG]]）**：最经典的“索引-检索-生成”线性流程。
2. **Advanced RAG（[[Advanced-RAG|高级 RAG]]）**：引入预检索（如 Query 重写）、后检索（如 Re-rank [[Reranking|重排]]）等策略，解决[[Naive-RAG|朴素 RAG]] 检索不准和块窗口过大等问题。
3. **Modular RAG（模块化 RAG）**：将各种检索与生成步骤进行原子模块化，支持迭代检索、混合路由、多路编排。

---
**关联页面**：
- [[Naive-RAG]] (概念)
- [[Vector-Database]] (核心存储概念)
