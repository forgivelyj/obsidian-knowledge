---
title: "06-RAG评估-summary"
aliases: [RAG 评估与评测体系摘要, RAG Evaluation Summary]
tags: [ai/rag/active]
category: summaries
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/06-RAG评估/06-RAG评估.md]]"
description: "阐述 RAG 评估的四项核心指标（精确度、召回率、忠实度、答案相关性）与优化路径；介绍 Ragas 和 TruLens 评测工具的应用；详解 LlamaIndex 评估体系中的忠实度/相关性评估器、批量异步运行器（BatchEvalRunner）及检索评估（Hit Rate & MRR）的开发实践。"
---

# 06-RAG评估 摘要

## 概要说明
本素材系统梳理了 [[RAG]] 系统的性能评估与诊断方法，即 **[[RAG-Evaluation]]**。内容涵盖检索端指标（Context Precision 精确度、Context Recall 召回率）与生成端指标（Faithfulness 忠实度、Answer Relevancy 答案相关性）的定义与公式；深度剖析了主流开源 [[RAG-Evaluation|RAG 评测]]框架 **[[Ragas]]** 与 TruLens 的评估原理；详细演示了 [[LlamaIndex]] 评估模块中 `FaithfulnessEvaluator`、`RelevancyEvaluator`、`BatchEvalRunner`（批量并行异步评估）以及基于自动生成问答对（`generate_question_context_pairs`）测试检索命中率（Hit Rate）与平均倒数排名（MRR）的代码实践。

## 核心要点
1. **[[RAG-Evaluation|RAG 评估]]指标黄金标准**：
   - 检索评估：
     - **Context Precision（精确度）**：检索到的文档中实际相关的比例，以及相关内容是否排在前面。
     - **Context Recall（召回率）**：知识库中的相关文档有多少被成功找回（依赖 Ground Truth）。
     - F1 分数：平衡精准度与召回率的综合表现。
   - 响应评估：
     - **Faithfulness（忠实度）**：评估答案是否完全由检索上下文支持，检测大模型是否凭空瞎编（检测幻觉）。
     - **Answer Relevancy（相关性）**：评估生成的答案是否答非所问，能否有效还原出用户提问。
2. **自动化 [[RAG-Evaluation|RAG 评测]]工具 [[Ragas]]**：
   - **[[Ragas]]** 输入四大要素：`question` (问题)、`answer` (LLM回答)、`contexts` (检索出的节点)、`ground_truth` (标准答案)。
   - [[Ragas]] 利用 LLM 作为裁判，通过对 answer 和 ground_truth 进行原子句子拆分与对比，自动计算 0-1 的定量指标评分。
3. **[[LlamaIndex]] 评估与 BatchEvalRunner**：
   - **响应评估**：`FaithfulnessEvaluator`（判定回答是否忠于上下文）与 `RelevancyEvaluator`（判定问题与答案契合度）。
   - **批量运行优化**：`BatchEvalRunner` 支持通过协程并发调用大模型，解决 for 循环逐个查询的速度瓶颈。
   - **检索评测**：使用 `generate_question_context_pairs` 自动生成各 Chunk 能回答的中文问题，然后利用 `RetrieverEvaluator` 进行批量打分，输出 **Hit Rate（命中率）** 与 **MRR（平均倒数排名）** 分析报表。
4. **指标不达标的优化指南**：
   - 精确度低：引入 [[Reranking]]、混合检索、查询改写。
   - 召回率低：引入 [[Parent-Child-Index]] [[Parent-Child-Index|父子索引]]、增大 Top-K 检索。
   - 忠实度低：清理数据垃圾、在 Prompt 中设置强力拒答边界（若没有则答“不知道”）。
   - 相关性低：指令微调、优化 Prompt。

---
**关联页面**：
- [[RAG-Evaluation]] (新建概念)
- [[Ragas]] (新建工具实体)
- [[LlamaIndex]] (关联实体框架)
- [[Reranking]] (关联优化概念)
- [[Parent-Child-Index]] (关联优化概念)
