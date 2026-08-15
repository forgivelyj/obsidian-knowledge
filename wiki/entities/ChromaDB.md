---
title: "ChromaDB"
aliases: [Chroma, chromadb]
tags: [database/tool/active]
category: entities
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/01-RAG基础/01-RAG基础.md]]"
description: "ChromaDB 是一款开源、本地优先、开箱即用的轻量级嵌入向量数据库，专为 AI 应用和 RAG 框架的原型快速开发而设计。"
---

# ChromaDB

ChromaDB 是当前人工智能生态（尤其是 [[RAG]] 原型系统）中最受欢迎的[[Embedding|嵌入]]式本地[[Vector-Database|向量数据库]]。

## 核心特性
- **开箱即用**：无需繁琐的服务器安装配置，只需 `pip install chromadb` 即可在 Python 项目中直接内嵌使用。
- **本地持久化**：默认可以运行在内存中，也可以配置本地路径直接进行数据落盘。
- **与大模型兼容性好**：提供了简洁的增删改查（CRUD）接口以及与 LangChain、[[LlamaIndex]] 等框架的无缝适配插件。

## Python 核心操作案例

### 1. 建立持久化连接与集合（Collection）
```python
import chromadb
# 建立本地持久化客户端（数据保存在本地硬盘中）
client = chromadb.PersistentClient(path="./chroma_db")
# 获取或新建一个以余弦距离计算的向量集合
collection = client.get_or_create_collection(
    name="my_wiki_documents",
    metadata={"hnsw:space": "cosine"} # 支持 cosine (余弦), l2 (欧氏), ip (内积)
)
```

### 2. 数据的增删改查
```python
# A. 添加数据 (添加文本、对应的向量以及自定义的ID)
collection.add(
    documents=["这是第一篇测试文档", "OAuth2 的受众限制保护机制"],
    embeddings=[[0.1, 0.2, 0.3], [4.1, 5.2, 6.3]],
    ids=["doc1", "doc2"]
)

# B. 模糊相似性检索
results = collection.query(
    query_embeddings=[[0.1, 0.2, 0.3]], # 查询向量
    n_results=1 # 召回前 K 个最相似的结果
)

# C. 修改数据
collection.update(
    ids=["doc1"],
    documents=["这是被更新后的第一篇文档"],
    embeddings=[[0.11, 0.22, 0.33]]
)

# D. 删除数据
collection.delete(ids=["doc1"])
```

---
**关联页面**：
- [[Vector-Database]] (理论基础)
- [[RAG]] (工程应用场景)
