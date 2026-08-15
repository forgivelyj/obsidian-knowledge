---
title: "Ingestion-Pipeline"
aliases: [数据摄取管道, IngestionPipeline, Ingestion Cache]
tags: [ai/framework/active]
category: concepts
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/04-Advanced RAG/04-Advanced RAG.md]]"
description: "IngestionPipeline 是 LlamaIndex 中用于将原始文档自动化加工为 Node 并写入向量库的链式 Transformations 生产线系统。"
---

# IngestionPipeline (数据摄取管道)

在构建生产级 [[RAG]] 系统时，数据清洗、分块、元数据提取和向量化通常是一系列复杂且多步嵌套的逻辑。如果手动编写这些过程，代码会变得冗长且难以维护。

`IngestionPipeline` 是 [[LlamaIndex]] 中用于规范并统筹上述流程的“数据加工生产线”，支持模块化配置、并行处理和高性能的增量缓存。

---

## 1. 摄取管道的工作架构
```text
Reader (读取) ──► Document (元数据基础容器)
                     │
                     ▼
             IngestionPipeline
      ┌──────────────────────────────┐
      │ transformations = [          │
      │   1. SentenceSplitter,       │  <── 文本分块
      │   2. TitleExtractor,         │  <── 元数据生成 (LLM)
      │   3. QuestionsAnswered...    │  <── 元数据生成 (LLM)
      │   4. embed_model             │  <── 向量化 (Embedding)
      │ ]                            │
      └──────────────────────────────┘
                     │
                     ▼
             Node (原子块，存入数据库)
```

通过配置 `transformations` 数组，所有转换器（Transformations，包括文本分割器、元数据提取器和向量模型）被顺序执行。

---

## 2. 元数据增强技术 (Metadata Extractors)
在朴素分块中，长文档切片（Node）极易丢失上下文背景。管道内置了多种利用 LLM 自动提取元数据的组件，这些组件在分块时动态执行，为 Node 注入背景：
- **`TitleExtractor`**：根据前 $N$ 个 Node 归纳出文档标题，并注入所有子节点的元数据中，使各节点携带“全局归属主题”。
- **`SummaryExtractor`**：使用滑动窗口机制，为当前节点生成结合 `[前一节点, 本节点, 后一节点]` 的滑动上下文摘要。
- **`QuestionsAnsweredExtractor`**：利用 LLM 提取当前节点能够回答的几个问题，在检索时能极大地提高问题-问题（Q-Q）维度的匹配召回率。
- **`KeywordExtractor`**：提取核心关键词，便于后期通过属性过滤。

---

## 3. 管道缓存机制 (Ingestion Cache)
对于数万份大文档，每次运行流水线都去调用大模型提取元数据或执行向量化，会产生极其高昂的 API 费用和时间成本。

管道支持一键挂载 **`IngestionCache`**（支持基于本地内存的 `SimpleKVStore` 和基于外部数据库的 `RedisKVStore`）：
- **原理**：系统对 `Document 内容` + `Transformation 步骤的配置` 进行联合哈希，计算出一个唯一 Key。
- **命中缓存**：若 Key 在数据库中存在，则直接跳过该步骤并读取已算好的 Node，实现秒级增量更新。

```python
from llama_index.core.ingestion import IngestionPipeline, IngestionCache
from llama_index.storage.kvstore.redis import RedisKVStore

pipeline = IngestionPipeline(
    transformations=[my_splitter, my_extractor, embed_model],
    cache=IngestionCache(
        cache=RedisKVStore(host="127.0.0.1", port=6379),
        collection="my_ingest_cache"
    )
)
# 第一次执行耗时；第二次执行若文档无改动，则秒级完成并直接跳过 LLM 提取与 Embedding
nodes = pipeline.run(documents=documents)
```

---
**关联页面**：
- [[LlamaIndex]] (所归属的框架)
- [[Advanced-RAG]] (大设计场景)
- [[Parent-Child-Index]] (典型应用管道的切分方式)
- [[ChromaDB]] / [[Redis]] (对应的存储/缓存载体)
