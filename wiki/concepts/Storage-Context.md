---
title: "Storage-Context"
aliases: [存储上下文, StorageContext]
tags: [ai/framework/active]
category: concepts
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/02-llama_index框架/02-llama_index框架.md]]"
description: "StorageContext 是 LlamaIndex 的数据存储中枢系统，负责统筹 Docstore、VectorStore 和 IndexStore 三大模块的配置与数据落盘。"
---

# StorageContext (存储上下文)

在 [[LlamaIndex]] 框架中，一个数据索引的构建与加载需要同时维护三种完全不同的数据状态。`StorageContext` 便是负责管理并协同这三大核心子存储模块的“总司令”。

## 核心架构组成
```text
┌────────────────────────────────────────────────────────┐
│                     StorageContext                     │
└─────┬──────────────┬──────────────┬──────────────┬─────┘
      │              │              │              │
      ▼              ▼              ▼              ▼
┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐
│ Docstore  │  │VectorStore│  │IndexStore │  │GraphStore │
│ (文档存储) │  │ (向量存储) │  │ (索引存储) │  │ (图谱存储) │
└───────────┘  └───────────┘  └───────────┘  └───────────┘
```

1. **Docstore（文档存储）**：
   - **存什么**：原始 Node 的文本内容、节点层级元数据（如 MIME 类型、字符起始位置）。
   - **作用**：检索命中向量后，根据 `node_id` 从 Docstore 提取出完整的可读文本块反馈给 LLM。
   - **典型组件**：`SimpleDocumentStore`（内存/本地 JSON）、`MongoDocumentStore`、`RedisDocumentStore`。
2. **VectorStore（向量存储）**：
   - **存什么**：Nodes 切片对应的 Float [[Embedding|嵌入]]向量数组。
   - **作用**：在检索阶段进行极速的高维空间近似最近邻（ANN）距离比对。
   - **典型组件**：`SimpleVectorStore`、`ChromaVectorStore`（对接 [[ChromaDB]]）、`MilvusVectorStore`。
3. **IndexStore（索引存储）**：
   - **存什么**：索引的整体元数据结构（如本索引包含哪些 node_id，索引的类型为 Vector 还是 Summary 树）。
   - **典型组件**：`SimpleIndexStore`、`RedisIndexStore`。
4. **GraphStore（图谱存储）**：
   - **存什么**：实体及其关系三元组，专为 Knowledge Graph [[RAG]] 服务。

## 本地数据持久化与重建
在默认情况下，所有子存储都运行在系统内存中。但在生产开发中，我们必须将其落盘存储，并能够根据历史落盘直接重建索引：

### 1. 数据落盘存储
```python
from llama_index.core import StorageContext, VectorStoreIndex

# 构建存储上下文，配置第三方向量存储和文档库
storage_context = StorageContext.from_defaults(
    docstore=my_doc_store,
    vector_store=my_vector_store
)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
# 一键落盘
storage_context.persist(persist_dir="./my_storage")
```

### 2. 重建索引读取
```python
from llama_index.core import StorageContext, load_index_from_storage

# 加载原先的存储目录
storage_context = StorageContext.from_defaults(persist_dir="./my_storage")
# 一键恢复 Index
index = load_index_from_storage(storage_context)
```

---
**关联页面**：
- [[LlamaIndex]] (主架构框架)
- [[ChromaDB]] (具体向量存储库)
- [[Vector-Database]] ([[Vector-Database|向量数据库]]理论)
