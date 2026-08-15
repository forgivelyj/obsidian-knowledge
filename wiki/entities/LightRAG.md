---
title: "LightRAG"
aliases: [lightrag, LightRAG框架]
tags: [ai/framework/active]
category: entities
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/05-KNOWLEDGE GRAPH FOR RAG/05-KNOWLEDGE GRAPH FOR RAG.md]]"
description: "LightRAG 是由香港大学开源的轻量级图检索增强生成框架，主打高性价比的双层检索（低层精确与高层全局）机制与局部的增量知识更新。"
---

# LightRAG (轻量级图 [[RAG]] 框架)

LightRAG 是由香港大学（HKUDS）团队于 2024 年底开源的轻量级知识图谱[[RAG|检索增强生成]]系统。它的设计宗旨是：**保留微软 [[GraphRAG]] 强大的网状多步推理和全局归纳优势，但将运行费用和响应延迟削减到百分之一，并彻底解决其无法增量更新的工程痛点。**

---

## 1. 核心工程设计与优势

### ① 双层检索机制（Dual-Level Retrieval）
大模型在提问时，LightRAG 会自动用 LLM 抽取两组关键词，并在图谱中进行双层混合搜索：
1. **低层检索（Low-Level）**：
   - *定位*：关注具体的“实体”和“名词细节”。
   - *动作*：向量化检索命中最相关的局部节点及其一阶直接邻居，适合回答细粒度事实问题（如：“孙悟空的师父是谁？”）。
2. **高层检索（High-Level）**：
   - *定位*：关注宏观的“主题”和“逻辑脉络”。
   - *动作*：检索更广的抽象词上下文和二至三步的高阶连通分量，提供更宏大的全局视角，适合回答概括型问题（如：“西游记是一部什么样的小说？”）。
3. **融合（Combined Context）**：将局部细节上下文与全局宏观上下文拼接，输入大模型推理生成，实现全视角的准确作答。

### ② 局部增量更新（Incremental Update）
- **传统 [[GraphRAG]] 的死穴**：当有新文档加入知识库时，必须全量重新计算和重构所有的图谱关系与社区摘要，费用极高。
- **LightRAG 的机制**：当摄入新文档时，只抽取并更新受影响的局部节点与边，并在 KV 存储（JSON）与向量库（Faiss 等）中做局部的追加写入，**完全避免了重构开销**，非常适合动态更新的企业知识库。

---

## 2. 核心架构组成
- **NanoVectorDB / Faiss**：用来对实体、关系及文本块的 [[Embedding]] 进行快速向量计算。
- **KV 存储**：存储实体/关系的元数据、详细描述文本与 Chunks 的原文。
- **[[Neo4j]] / 内存图存储**：保存实体（节点）与关系（边）构成的拓扑知识图谱。

---

## 3. Python 核心使用示例
```python
import asyncio
from lightrag import LightRAG, QueryParam
from lightrag.utils import EmbeddingFunc
from sentence_transformers import SentenceTransformer

# 1. 初始化本地 Embedding 与 LLM 函数
model = SentenceTransformer("./bge-large-zh-v1.5")

async def local_embed(texts):
    return model.encode(texts, convert_to_numpy=True)

# 2. 组装 LightRAG
rag = LightRAG(
    llm_model_func=my_llm_func, # 自定义 LLM 调用
    embedding_func=EmbeddingFunc(
        embedding_dim=1024,
        max_token_size=8192,
        func=local_embed
    ),
    vector_storage="FaissVectorDBStorage",
    graph_storage="Neo4JStorage" # 数据同步落盘 Neo4j
)

# 3. 异步初始化与增量插入
async def main():
    await rag.initialize_storages()
    
    # 增量插入原始文本数据
    await rag.ainsert("西游记第一回讲述了石猴出世的故事...")
    
    # 4. 图谱查询（包含四种模式：naive, local, global, hybrid）
    response = await rag.aquery(
        "谁是孙悟空？", 
        param=QueryParam(mode="hybrid") # 推荐混合模式
    )
    print(response)

asyncio.run(main())
```

---
**关联页面**：
- [[GraphRAG]] (所属进阶概念)
- [[Neo4j]] (对应的图存储后端)
- [[Property-Graph]] (关联数据模型)
