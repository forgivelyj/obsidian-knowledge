---
title: "Vector-Database"
aliases: [向量数据库, Vector DB]
tags: [database/concept/active]
category: concepts
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/01-RAG基础/01-RAG基础.md]]"
description: "向量数据库是专门设计用于存储、检索和管理高维嵌入向量（Embeddings）并对其进行超大规模相似度距离计算（ANN 搜索）的数据库系统。"
---

# Vector Database (向量数据库)

传统的关系型数据库（如 MySQL、PostgreSQL）或 NoSQL 数据库（如 MongoDB）专长于精确的条件查询、模糊查询与范围查询。然而，在大模型时代，要处理由 [[Embedding]] 产生的上千维浮点数坐标并计算它们之间的夹角/几何空间距离，传统数据库由于不具备空间计算索引，性能会发生断崖式下跌。

**向量数据库**便是为了解决高维空间数据快速相似度检索而生的专用底层系统。

## 核心技术与工作原理
1. **高维存储**：专门的数据结构设计用来持久化高维特征数组（通常支持余弦、欧氏距离、内积等相似度算法）。
2. **近似最近邻搜索（ANN, Approximate Nearest Neighbor）**：在数以亿计的向量中，逐个计算距离是非常缓慢的。向量数据库利用特殊的索引算法在牺牲极小精度的前提下实现毫秒级的空间相似性过滤：
   - **HNSW（Hierarchical Navigable Small World）**：主流的分层图算法，在图结构中逐层寻找最近点，查询极快，是当前最主流的高效索引方式。
   - **IVF（Inverted File Index）**：倒排聚类索引，将空间切分为多个聚类区域，查询时只比对问题所属的几个区域。

## 为什么是 [[RAG]] 的基础？
在 [[RAG]] 系统中，大模型需要从本地庞大的专有数据库中获取知识。向量数据库充当了外部大脑的“硬盘”，它能够毫秒级检索出与用户问题最相关的 Top-K 个知识卡片，为大模型组装 Prompt 提供了最高效的数据底座。

## 常见向量数据库与选型
- **[[ChromaDB]]**：轻量级、对 Python 开发者极其友好、开箱即用，适合个人知识库、原型演示开发。
- **Milvus / Qdrant / Weaviate**：企业级高并发、分布式、支持千亿级向量的高性能数据库。
- **Pinecone**：云原生托管数据库服务。
- **PGVector**：基于传统 PostgreSQL 扩展的向量处理插件。

---
**关联页面**：
- [[RAG]] (架构基础)
- [[ChromaDB]] (具体工具实例)
