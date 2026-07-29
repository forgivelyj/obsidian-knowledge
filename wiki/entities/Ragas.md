---
title: "Ragas"
aliases: [ragas, explodinggradients/ragas]
tags: [ai/tool/active]
category: entities
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/06-RAG评估/06-RAG评估.md]]"
description: "Ragas 是一款用于评测检索增强生成（RAG）管道性能的开源框架，通过 LLM 作为裁判，对检索和生成两个层面的核心指标进行量化评估。"
---

# Ragas 评测框架

Ragas 是目前开源社区中最流行的专有 [[RAG]] 应用自动评估（LLM-as-a-Judge）工具包。它与 LangChain 和 [[LlamaIndex]] 拥有非常紧密的集成关系。

---

## 1. 核心输入数据结构
为了对一个 [[RAG]] 管道进行评测，Ragas 要求开发者准备包含以下四种标准属性的测试数据集：

1. **`question`**：用户输入的原始提问。
2. **`answer`**：[[RAG]] 系统实际调用大模型生成并返回给用户的回答。
3. **`contexts`**：[[RAG]] 系统实际从知识库中检索召回并用于生成该回答的参考文本块列表（List[str]）。
4. **`ground_truth`**：人工标定或确认的真实标准答案（**唯一需要人类参与提供的属性**，专门用来度量 Context Recall）。

---

## 2. 四大核心指标的计算逻辑

### ① 忠实度 (Faithfulness)
- *原理*：检测答案是否包含瞎编的信息。
- *计算*：Ragas 使用 LLM 将 `answer` 拆解为多个独立的原子事实声明（Statements），然后逐一检查每个 Statement 是否能被 `contexts` 直接支持。
  $$\text{Faithfulness} = \frac{\text{被上下文支持的 Statement 数量}}{\text{答案总 Statement 数量}}$$

### ② 答案相关性 (Answer Relevancy)
- *原理*：检测是否答非所问。
- *计算*：Ragas 让大模型读取 `answer`，反向推断并生成 $N$ 个可能的问题，然后计算这些反推问题与原始 `question` 之间的 [[Embedding]] 余弦相似度。相似度越高，说明回答越契合主题。

### ③ 上下文精确度 (Context Precision)
- *原理*：检查能否把有用的上下文排在检索列表的前面。
- *计算*：结合 `question`、`contexts` 以及 `ground_truth`，判断每个召回 Chunk 的相关度并引入排名惩罚因子，计算加权均值分。

### ④ 上下文召回率 (Context Recall)
- *原理*：检查是否找到了回答问题所需的全部核心事实。
- *计算*：将标准答案 `ground_truth` 拆解为多个事实陈述，使用 LLM 逐一验证这些事实陈述是否被包含在已召回的 `contexts` 文本中。
  $$\text{Context Recall} = \frac{\text{被 contexts 支持的 ground\_truth 事实数量}}{\text{ground\_truth 总事实数量}}$$

---

## 3. Ragas 与 [[LlamaIndex]] 集成代码示例

```python
from datasets import Dataset
from ragas import evaluate
from ragas.integrations.llama_index import LlamaIndexEmbeddingsWrapper, LlamaIndexLLMWrapper
from ragas.metrics import faithfulness, answer_relevancy, context_recall, context_precision

# 1. 整理测试集（由 RAG 运行产出的 question, answer, contexts 加上人工标准 ground_truth）
data_samples = {
    "question": ["DeepSeek何时成立？"],
    "answer": ["成立于2023年7月17日。"],
    "contexts": [["DeepSeek成立于2023年7月17日，由幻方量化孕育..."]],
    "ground_truth": ["DeepSeek成立于2023年7月17日。"]
}
dataset = Dataset.from_dict(data_samples)

# 2. 包装 LlamaIndex 的本地或商用模型
ragas_llm = LlamaIndexLLMWrapper(llm)
ragas_embeddings = LlamaIndexEmbeddingsWrapper(embed_model)

# 3. 运行批量评估
result = evaluate(
    dataset,
    metrics=[context_precision, context_recall, faithfulness, answer_relevancy],
    llm=ragas_llm,
    embeddings=ragas_embeddings
)

# 4. 导出 pandas 并输出为 CSV
df = result.to_pandas()
df.to_csv("ragas_eval_report.csv", index=True)
```

---
**关联页面**：
- [[RAG-Evaluation]] (评估概念)
- [[LlamaIndex]] (关联框架)
- [[Reranking]] / [[Parent-Child-Index]] (指标优化落地方案)
