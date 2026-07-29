---
title: "03-RAG进阶-summary"
aliases: [RAG进阶摘要, Advanced RAG Summary]
tags: [ai/rag/active]
category: summaries
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/03-RAG进阶/03-RAG进阶.md]]"
description: "分析 RAG 开发落地中的常见故障点，阐述预检索（Query重写/转换/扩展）与后检索（重排与提示压缩）的优化策略，解读前沿 Advanced RAG 变体（CRAG、Self-RAG、RAG-Fusion等），并对比了 RAG 与微调（Fine-Tuning）的区别。"
---

# 03-RAG进阶 摘要

## 概要说明
本素材深入探讨了 [[RAG]] 的前沿进阶技术与优化路径。内容涵盖 [[RAG]] 落地工程中的“七大故障点”分析、解决检索召回质量问题的针对性优化策略（文本分割粒度、多路[[Reranking|重排]]、Pydantic格式验证、提示压缩），并详细解读了学术界先进的 [[RAG]] 变体论文（CRAG、Self-[[RAG]]、[[RAG]]-Fusion等）与 [[RAG]] 和微调的工程选型比对。

## 核心要点
1. **[[RAG]] 工程的故障点（Failure Points）**：
   - 引用论文《Seven Failure Points When Engineering a Retrieval Augmented Generation System》。
   - 索引构建痛点：内容缺失（Missing Content）、文档加载偏差、切分粒度不当。
   - 查询生成痛点：错过排名靠前的文档（Missed Top Ranked）、上下文与答案无关（Not in Context）、未成功提取（Not Extracted）、格式错误、答案不完整。
2. **检索优化策略**：
   - **分块粒度优化**：基于滑动窗口、文档大纲结构或递归式分块（利用段落和换行符逐步退避切割）。
   - **检索召回优化**：引入 **[[Reranking]]（[[Reranking|重排]]）** 以避免直接增加 Top-K 引入过多噪声；引入 **[[Advanced-RAG]]** 预检索技术（如查询重写、Step-back 提问、子问题拆分、Multi-Query 查询扩展）。
   - **格式与提炼优化**：利用 Pydantic 校验 JSON 输出结构；利用上下文压缩技术（Contextual Compression）减少 Prompt 的冗余 Token 干扰。
3. **Advanced [[RAG]] 核心学术变体**：
   - **T-[[RAG]]**：利用组织树状实体层次结构辅助检索，对复杂实体关系进行精确定位。
   - **CRAG**（可矫正 [[RAG]]）：引入检索评估器，区分 Correct（精炼 Node）、Incorrect（网络搜索修正）与 Ambiguous（双路结合）。
   - **Self-[[RAG]]**（自我反思 [[RAG]]）：大模型在生成时并行检索，并根据多维反思标记对生成的段落进行自检过滤。
   - **[[RAG]]-Fusion**：大模型生成多查询后进行多路搜索，并利用 RRF（倒数排名融合）算法融合去重。
   - **Rewrite-Retrieve-Read**：以强化学习奖励训练一个小型重写器，重写问题后再进行传统读写。
4. **[[RAG-vs-Fine-Tuning]]（[[RAG]] 与微调选型）**：
   - [[RAG]] 动态、实时、有据可查、防幻觉强；微调融入模型内部，适合控制格式与语气、深入学习特定静态任务。两者常互补结合。

---
**关联页面**：
- [[RAG]] (核心概念)
- [[Advanced-RAG]] (概念页)
- [[Reranking]] (概念页)
- [[RAG-vs-Fine-Tuning]] (对比分析页)
