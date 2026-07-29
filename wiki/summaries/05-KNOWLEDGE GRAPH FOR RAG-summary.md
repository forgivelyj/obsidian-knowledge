---
title: "05-KNOWLEDGE GRAPH FOR RAG-summary"
aliases: [知识图谱与图 RAG 摘要, Graph RAG Summary]
tags: [ai/rag/active]
category: summaries
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/05-KNOWLEDGE GRAPH FOR RAG/05-KNOWLEDGE GRAPH FOR RAG.md]]"
description: "阐述知识图谱（LPG 与 RDF）的核心概念、构建流程与图数据库（以 Neo4j 及其 Cypher 语法为中心）的应用；解析 LlamaIndex PropertyGraphIndex 及其各类抽取器开发；详解前沿 LightRAG 的双层检索机制与增量更新实战。"
---

# 05-KNOWLEDGE GRAPH FOR [[RAG]] 摘要

## 概要说明
本素材系统梳理了知识图谱在 [[RAG]] 系统中的深度应用，即 **[[GraphRAG]]** 范式。内容涵盖知识图谱基础模型（[[Property-Graph|LPG]] [[Property-Graph|属性图]]与 RDF 三元组对立统一）、知识图谱生命周期构建（定义、抽取、融合、存储、应用）、主流图数据库 **[[Neo4j]]** 的安装配置与 [[Neo4j|CQL]]（[[Neo4j|Cypher]]）语法。并深入 [[LlamaIndex]] [[Property-Graph|属性图]]索引（PropertyGraphIndex）的各类 LLM 抽取器开发，最后重点剖析了前沿轻量级图谱框架 **[[LightRAG]]** 的双层检索（局部+全局）与增量更新架构实现。

## 核心要点
1. **知识图谱分类与 [[Property-Graph|LPG]] 模型**：
   - [[Property-Graph|LPG]]（[[Property-Graph|属性图]]模型）：允许节点和边附加 Label 与 Properties，擅长高性能关系查询与企业级业务建模。[[Neo4j]] 是其核心代表。
   - RDF（资源描述框架）：采用 `(主语, 谓语, 宾语)` 标准三元组，常用于学术研究、语义网与跨系统推理标准。
   - 知识图谱构建生命周期：本体设计（骨架本体） $\rightarrow$ 信息获取抽取（NER 实体、关系、属性抽取） $\rightarrow$ 知识融合对齐（共指消解与消歧） $\rightarrow$ 图存储（图数据库） $\rightarrow$ 图查询应用。
2. **图数据库 [[Neo4j]] 开发与配置**：
   - 配置环境：Java 17 对应 [[Neo4j]] 5.x 版本。需要将 APOC Extended 插件导入 `plugins` 并修改 `neo4j.conf` 允许运行。
   - **[[Neo4j|Cypher]] ([[Neo4j|CQL]]) 语法**：
     - `CREATE` 与 `MERGE`（幂等创建，避免冗余）。
     - `MATCH ... WHERE ... RETURN ... LIMIT` 进行多跳与关联属性匹配。
     - `SET` 修改属性/标签；`REMOVE` 移除属性/标签；`DETACH DELETE` 安全切断关系并删除节点。
3. **[[LlamaIndex]] PropertyGraphIndex 及其关系抽取器**：
   - PropertyGraphIndex 替代了传统的 KnowledgeGraphIndex，功能更模块化，支持实体向量化（`embed_kg_nodes=True`）。
   - 提取器选型：
     - `ImplicitPathExtractor`：无需 LLM，利用 Node relationships 自带结构提取隐式边。
     - `SimpleLLMPathExtractor`：利用 LLM 自然语言推理提取三元组。
     - `DynamicLLMPathExtractor`：动态自适应发现实体与关系。
     - `SchemaLLMPathExtractor`：依据预定义的 Schema（Pydantic 验证结构）进行强约束的安全抽取（企业级推荐）。
4. **前沿 [[LightRAG]] 港大开源框架**：
   - **[[LightRAG]]** 解决传统微软 [[GraphRAG]] 的 Token 消耗爆炸与无法“增量更新”的生产痛点。
   - **双层检索机制（Dual-Level Retrieval）**：
     - **低层（Low-Level）**：提取实体导向关键词，利用向量检索局部节点和直接邻居，提供精准细节。
     - **高层（High-Level）**：提取全局主题/抽象词，遍历二三步高阶邻居，提供宏观全局视角。
     - 将两者融合（Combined Context）送入大模型，实现极低成本的全局多跳问答。
   - **增量更新**：新增文档仅局部更新受影响图谱，无需重构，对生产知识库极其友好。

---
**关联页面**：
- [[GraphRAG]] (核心概念)
- [[Neo4j]] (核心数据库实体)
- [[LightRAG]] (开源前沿框架实体)
- [[Property-Graph]] (核心数据模型概念)
- [[LlamaIndex]] (关联实体框架)
