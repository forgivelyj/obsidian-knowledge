---
title: "RAG-Evaluation"
aliases: [RAG 评估, RAG 评测, RAG Evaluation]
tags: [ai/rag/active]
category: concepts
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/06-RAG评估/06-RAG评估.md]]"
description: "RAG 评估是针对检索增强生成系统的检索器和生成器性能进行量化度量、诊断与分析的工程方法，核心关注精确度、召回率、忠实度与答案相关性四大维度。"
---

# [[RAG]] Evaluation ([[RAG]] 评估)

在将 [[RAG]] 系统推向生产环境前，对其进行严密的量化评估是确保大模型回复事实性、鲁棒性并防范幻觉的绝对关键。[[RAG]] 系统的表现主要受两个核心要素决定：**检索器（能否找对资料）** 和 **生成器（能否用好资料）**。

---

## 1. 评估的核心维度：黄金四角
目前行业公认的 [[RAG]] 核心评测标准由以下四大指标组成：

```text
                  【用户问题 (Question)】
                        │             │
                Context │             │ Answer
              Precision │             │ Relevancy
                        ▼             ▼
       【检索上下文 (Context)】 ──► 【生成回答 (Answer)】
                              Faithfulness
```

### ① 检索端指标 (Retrieval Quality)
- **Context Precision（上下文精确度）**：
  - *定义*：系统检索到的所有段落中，实际与问题相关的段落所占的比例，且高相关的段落是否排在较前的位置。
  - *意义*：精确度低意味着检索引入了过多噪音，会干扰大模型生成（引起中间迷失）。
- **Context Recall（上下文召回率）**：
  - *定义*：本地数据库中所有能够回答该问题的关键内容，有多少被系统成功检索出来。
  - *意义*：召回率低意味着关键信息漏检，大模型拿不到拼图，无法生成完整答案。

### ② 生成端指标 (Generation Quality)
- **Faithfulness（忠实度/忠诚度）**：
  - *定义*：大模型生成的回答中，有多少陈述能够从检索到的上下文中直接找到依据。
  - *量化目标*：忠实度是**排查大模型幻觉**的最直接指标。若模型把外部先验知识或瞎编的内容写入答案，忠实度就会下降。
- **Answer Relevancy（答案相关性）**：
  - *定义*：模型生成的答案是否切题，即是否准确地针对用户问题展开，不存在废话或答非所问。

---

## 2. 评估的实现方式
- **人工评估（Human Evaluation）**：邀请领域专家或标注人员，对问答对进行相关性和真实性打分。质量极高，但成本高昂、无法进行大规模持续集成评测。
- **LLM-as-a-Judge（大模型作为裁判）**：使用计算能力更强的商用大模型（如 GPT-4）扮演裁判。将答案拆分为独立的声明句子，配合设计的 Prompt，研判其是否忠实于上下文。目前以 **[[Ragas]]** 和 TruLens 为核心开源开发工具。

---

## 3. [[LlamaIndex]] 评估开发体系
在 [[LlamaIndex]] 框架中，内置了多套自动化评估组件：
1. **答案自检评估**：提供 `FaithfulnessEvaluator` 和 `RelevancyEvaluator`。在生产环境中，推荐使用 **`BatchEvalRunner`** 并发协程运行器，将大批量的查询和评估任务异步进行，大幅度节省测试耗时。
2. **检索评测（Retrieval Test）**：
   - 步骤一：使用 `generate_question_context_pairs` 提取本地 Chunk，自动由大模型伪造生成标准的“问题-上下文”配对数据集并存为 JSON。
   - 步骤二：利用 `RetrieverEvaluator` 运行该数据集，计算检索器的 **Hit Rate（命中率）** 与 **MRR（平均倒数排名）**，分析检索召回和排序的优劣。

---
**关联页面**：
- [[RAG]] (所属父概念)
- [[Ragas]] (核心评估工具实体)
- [[LlamaIndex]] (关联开发框架)
- [[Reranking]] / [[Parent-Child-Index]] (指标不达标时的关键优化技术)
