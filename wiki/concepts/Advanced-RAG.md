---
title: "Advanced-RAG"
aliases: [高级 RAG]
tags: [ai/rag/active]
category: concepts
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/03-RAG进阶/03-RAG进阶.md]]"
description: "高级 RAG 是在朴素 RAG 基础上的升级范式，通过预检索阶段的查询解析和后检索阶段的重排与上下文压缩，解决检索质量、内容噪声及 Token 膨胀痛点。"
---

# Advanced [[RAG]] (高级 [[RAG]])

Advanced [[RAG]] 是针对 [[Naive-RAG]] 在工程落地上面临的“七大故障点”（如错过 Top Ranked 文档、上下文噪声干扰、大模型无法精准过滤答案等）而提出的进阶检索增强范式。

其核心思想是：**不再无脑地将用户提问直接向量化并喂给大模型**，而是在“检索前”进行查询优化，在“检索后”进行过滤精炼。

---

## 1. 预检索阶段优化 (Pre-Retrieval)
查询优化的主要目的是让用户的问题更容易与向量库中的段落进行对齐匹配：

- **查询重写 (Query Rewriting)**：将用户的模糊语病句利用 LLM 重新表述为指向明确、表意完整的句子。
- **查询转换与拆分 (Query Transformation)**：
  - **Step-back Prompting (退一步提问)**：将具体问题抽象为更广义的原则或背景问题，先检索背景再回答具体。
  - **子问题分解 (Sub-question Decomposition)**：将多维度复杂问题拆解为多个独立的子问题，逐一检索后再归并回答。
- **查询扩展 (Query Expansion)**：
  - **多查询扩展 (Multi-Query)**：由 LLM 派生出 3-5 个意思相同但措辞不同的相似问题，并发进行多路检索以防漏招。
  - **[[RAG]]-Fusion**：多路检索后，使用 RRF（倒数排名融合）算法对各路结果进行合并与[[Reranking|重排序]]。

---

## 2. 后检索阶段优化 (Post-Retrieval)
检索器返回的一堆文本块（Chunks）如果直接丢进 Prompt 往往会导致“中间迷失”（Lost in the Middle）现象。

- **[[Reranking]] ([[Reranking|重排]])**：利用交叉编码器（Cross-Encoder）计算召回的所有 Chunks 与原问题的精准关联分，只过滤出前 K 个最高相关的卡片丢给 LLM。
- **提示压缩 (Prompt/Context Compression)**：移除无用的噪音词汇，仅提取与问题强相关的语句段落，限制并精简最终塞入大模型的上下文窗口，以降低 Token 成本并提升推理速度。

---

## 3. 前沿 Advanced [[RAG]] 变体
- **CRAG (Corrective [[RAG]], 可矫正 [[RAG]])**：通过检索评估器判断检索的可信度。低信度时引入**网络搜索（Web Search）**进行知识库动态纠错。
- **Self-[[RAG]] (自我反思 [[RAG]])**：大模型具备“按需检索”和“自检”能力，在生成时并行检索多个文本块，并通过生成特定的反思标记（Critique Tags）选出质量最好的段落。
- **T-[[RAG]] (Tree-[[RAG]])**：在传统向量检索的基础上，结合组织的实体树（Entity Tree）进行层次化查询匹配。

---
**关联页面**：
- [[RAG]] (核心父范式)
- [[Naive-RAG]] (原始范式)
- [[Reranking]] (后检索关键技术)
- [[RAG-vs-Fine-Tuning]] (技术选型对比)
