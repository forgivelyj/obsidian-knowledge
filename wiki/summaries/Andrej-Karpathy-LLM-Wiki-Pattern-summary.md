---
title: "Andrej-Karpathy-LLM-Wiki-Pattern-summary"
aliases: [LLM-Wiki-Summary, Karpathy-Gist-Summary]
tags: [ai, pattern, active]
category: summaries
created: 2026-08-15
updated: 2026-08-15
sources:
  - "[[raw/00-Inbox/Andrej Karpathy - LLM Wiki Pattern.md]]"
description: "Andrej Karpathy 提出的 LLM Wiki 模式：通过三层架构与 AI 代理实现具有复利效应的个人知识库。"
---

# Andrej Karpathy: LLM Wiki 知识库模式摘要

## 📌 核心观点总结
1. **超越传统 RAG**：传统 RAG 在每次查询时临时切片重组，缺乏知识的沉淀与积累；而 LLM Wiki 将新知识即时编译并持续融合至持久化 Markdown 维基库中。
2. **三层解耦架构**：将知识系统划分为**原始素材层 (`raw/`)**、**知识沉淀层 (`wiki/`)** 与**行为规范层 (`schema`/`AGENTS.md`)**。
3. **IDE 与程序员隐喻**：人类负责资料收集与方向探索，Obsidian 作为展示与浏览的 IDE，大模型（LLM）作为程序员负责高密度的维护、跨链引用与消重。
4. **四大核心工作流**：支持持续摄入 (`Ingest`)、语义查询与回填 (`Query`)、健康检查 (`Lint`) 与成品发布 (`Publish`)。

## 🔍 关键论点
- **复利效应 (Compounding Knowledge)**：每一次素材摄入都会强化或更新现有的实体与概念网络，使知识库随时间持续增值。
- **维护成本归零**：人类放弃自建 Wiki 的主要原因是维护交叉引用和消重的摩擦力过大，LLM 完美承担了这一机械性工作。

## 🔗 衍生实体与概念
- 实体：[[Andrej-Karpathy]]
- 概念：[[LLM-Wiki]]、[[Compounding-Knowledge]]
