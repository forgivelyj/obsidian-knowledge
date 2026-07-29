---
title: "04-Advanced RAG-summary"
aliases: [高级 RAG 开发实战摘要, Advanced RAG Practice Summary]
tags: [ai/rag/active]
category: summaries
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/04-Advanced RAG/04-Advanced RAG.md]]"
description: "详细梳理 LlamaIndex 框架下高级 RAG 的开发组件与实战流程，包括 IngestionPipeline 数据加工管道、元数据提取与缓存、父子索引（Hierarchical Index）、QueryFusion 混合检索融合算法、多路后处理器（Reranker、上下文拓展与时效衰减）以及 PDF 智能解析器 MinerU 落地实践。"
---

# 04-Advanced [[RAG]] 实战 摘要

## 概要说明
本素材是基于 [[LlamaIndex]] 框架进行 [[Advanced-RAG]] 落地的深度技术手册。重点剖析了数据摄取生产线（[[Ingestion-Pipeline|IngestionPipeline]]）的设计与缓存优化、父子/[[Parent-Child-Index|层级索引]]的构建与 AutoMerging 合并检索、四种多路检索融合算法（RRF、归一化、Z-Score DBSF）、多维后处理器组件（过滤、BGE[[Reranking|重排]]、[[Reranking|重排]]首尾防中间迷失、时间衰减排序），并结合开源 PDF 智能解析工具 **[[MinerU]]** 详述了金融级年报问答助手（MarkdownElementNodeParser 处理复杂表格）的工程架构与代码实现。

## 核心要点
1. **自动化摄取管道与元数据增强**：
   - **[[Ingestion-Pipeline]]**：将“加载-分块-元数据提取-向量化-入库”抽象为链式 Transformations 生产线，并支持 RedisKVStore 增量哈希缓存。
   - **元数据提取器**：运用大模型提取 Title、Summary（带前后 Node 滑动感知）、Keyword 和 QuestionsAnswered 填入 Node Metadata，极大地丰富检索向量和后置属性过滤（MetadataFilters）。
2. **父子与[[Parent-Child-Index|层级索引]]（Parent-Child Index）**：
   - **[[Parent-Child-Index]]**：针对“小块检索（召回精准度高）+ 大块返回（防止上下文缺失）”的工程落地。使用 `HierarchicalNodeParser` 进行 2048 $\rightarrow$ 512 $\rightarrow$ 128 多级分块，仅向量化叶子节点，并利用 `AutoMergingRetriever` 在父节点召回比例过半时自动向上合并。
3. **混合检索与融合[[Reranking|重排]]算法**：
   - 混合检索（Hybrid）= 向量检索（Semantic）+ BM25（精确关键词）。
   - **`QueryFusionRetriever`** 支持四种融合打分模式：
     - `reciprocal_rerank`（RRF 倒数排名融合，基于排名，最常用）。
     - `relative_score`（基于 Min-Max 归一化融合）。
     - `dist_based_score`（DBSF 基于 Z-Score 标准分布融合，能鲁棒处理分数分布不均）。
4. **多维度后处理器 (NodePostprocessors)**：
   - 阈值过滤：`SimilarityPostprocessor` 相似度截断。
   - **[[Reranking]]（[[Reranking|重排序]]）**：使用本地 Cross-Encoder 模型（如 BGE-Reranker-Large）进行打分。
   - 顺序优化：`LongContextReorder` 重新排列节点，将高相关内容排在首尾，解决大模型“中间迷失”痛点。
   - 上下文拓展：`AutoPrevNextNodePostprocessor` 自动检测并在必要时补全前后相邻 Node 的上下文。
   - 时间衰减：`TimeWeightedPostprocessor` 进行相似度与时效衰减混合打分。
5. **复杂 PDF 表格解析与综合实战**：
   - **[[MinerU]]**：上海 AI 实验室开源工具，解决表格、双栏、公式解析痛点，支持导出 Markdown/LaTeX/JSON。
   - **年报助手架构**：[[MinerU]] 解析 $\rightarrow$ 按 H1 大纲分割 $\rightarrow$ `MarkdownElementNodeParser` 提炼表格结构与 Summary $\rightarrow$ [[Ingestion-Pipeline|IngestionPipeline]] (含元数据和 [[Redis|Redis 缓存]]) $\rightarrow$ 写入 MongoDB（Docstore）与 [[ChromaDB]]（VectorStore） $\rightarrow$ [[Parent-Child-Index|AutoMergingRetriever]] 召回 $\rightarrow$ BGE-Reranker [[Reranking|重排]] $\rightarrow$ RetrieverQueryEngine 生成。

---
**关联页面**：
- [[LlamaIndex]] (关联实体框架)
- [[Advanced-RAG]] (升级的父概念)
- [[Reranking]] (升级的[[Reranking|重排]]概念)
- [[Ingestion-Pipeline]] (新建概念)
- [[Parent-Child-Index]] (新建概念)
- [[MinerU]] (新建工具实体)
