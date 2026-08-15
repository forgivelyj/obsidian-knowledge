---
title: "LLM-Wiki"
aliases: [大模型知识库, 个人智能Wiki, Persistent-LLM-Wiki]
tags: [concept, ai, productivity, active]
category: concepts
created: 2026-08-15
updated: 2026-08-15
sources:
  - "[[raw/00-Inbox/Andrej Karpathy - LLM Wiki Pattern.md]]"
description: "由 LLM 持续维护、跨双链引用的持久化个人 Markdown 知识库架构。"
---

# LLM-Wiki

## 📖 核心定义
**LLM-Wiki** 是一种利用大语言模型（LLM）作为专职维护者，以本地 Markdown 文本与 Obsidian 双链图谱为基础的个人/团队知识库体系。其核心是将非结构化的原始素材即时编译为结构化、互相引用的知识网络。

## 🔍 架构与运行机制
1. **分层机制**：
   - **`raw/` 原始素材层**：不可变的事实基础（只读）。
   - **`wiki/` 知识沉淀层**：由 AI 代理读写的实体、概念、摘要与洞察。
   - **`schema` 规则层**：定义 Frontmatter 与协作协议（如 `AGENTS.md`）。
2. **四大循环工作流**：
   - **Ingest（摄入）**：素材提取与编译。
   - **Query（查询）**：知识检索与反哺。
   - **Lint（巡检）**：冲突与孤岛修补。
   - **Publish（发布）**：向成品格式交付。

## 🔗 相关实体与概念
- 提出者：[[Andrej-Karpathy]]
- 核心特征：[[Compounding-Knowledge]]
- 相关摘要：[[Andrej-Karpathy-LLM-Wiki-Pattern-summary]]
