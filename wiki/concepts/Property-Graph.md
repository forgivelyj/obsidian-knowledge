---
title: "Property-Graph"
aliases: [属性图, LPG, Labeled Property Graph]
tags: [database/concept/active]
category: concepts
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/05-KNOWLEDGE GRAPH FOR RAG/05-KNOWLEDGE GRAPH FOR RAG.md]]"
description: "属性图（LPG）是一种主流的图数据模型，允许节点和边附加 Label 标签与 Properties 属性，以极高的灵活性与查询效率表征复杂的实体网状关系。"
---

# Property Graph (属性图)

属性图（LPG, Labeled Property Graph）是知识图谱与图数据库领域中最流行、最直观的数据模型，是 [[Neo4j]] 数据库和 [[LlamaIndex]] 新一代图索引（PropertyGraphIndex）的骨架模型。

---

## 1. 核心架构元素
在属性图模型中，所有的知识均由以下四种基本元素构成：

1. **节点（Nodes）**：
   - 代表具体的“实体”或“概念”（例如：`段正淳`、`大理国`）。
2. **边（Edges / Relationships）**：
   - 代表节点之间的“关系”（例如：`段正淳` $\xrightarrow{【皇帝】}$ `大理国`）。
   - 边是有方向的（单向或双向）。
3. **标签（Labels）**：
   - 对节点进行分类划分的元数据（例如：`段正淳` 的 Label 是 `Person`，`大理国` 的 Label 是 `Country`）。
4. **属性（Properties）**：
   - 节点和边都可以附加任意数量的**键值对**特征（例如：可以给节点 `段正淳` 附加属性 `{name: "段正淳", age: 48}`；也可以给关系 `【妻子】` 附加属性 `{since: "大理保定元年"}`）。

---

## 2. 属性图 (LPG) 与 资源描述框架 (RDF) 对比

| 对比维度 | LPG (属性图模型) | RDF (资源描述框架) |
| :--- | :--- | :--- |
| **底层规范** | 业界实际标准，强调实用性。 | W3C 国际官方标准，强调规范。 |
| **数据单元** | 包含丰富内部属性的节点与边。 | 主语-谓语-宾语的**三元组（Triplets）**。 |
| **属性附加方式** | 直接在节点或边上附加任意 KV 属性。 | 必须新建额外的三元组来表示属性（非常繁琐）。 |
| **核心优势** | 查询性能高、建模极为灵活直观。 | 逻辑推理能力极强、具备极高的跨系统共享标准。 |
| **查询语言** | [[Neo4j|Cypher]] 等（类 SQL 的模式匹配）。 | SPARQL。 |
| **代表数据库** | [[Neo4j]]、Nebula Graph | Apache Jena、Virtuoso |

---

## 3. 在 [[GraphRAG]] 中的工程落地
在新版 [[LlamaIndex]] 中，官方主推 **`PropertyGraphIndex`** 作为知识图谱的核心底座。大模型在抽取数据时，会直接利用 LPG 模型将非结构化段落抽取为含有 Label、属性及向量的节点与边，并通过 [[Neo4j|Cypher]] 语法直接写入图库中。

---
**关联页面**：
- [[GraphRAG]] (应用大背景)
- [[Neo4j]] (属性图的核心落地数据库)
- [[LlamaIndex]] (支持 PropertyGraph 编排的实体框架)
