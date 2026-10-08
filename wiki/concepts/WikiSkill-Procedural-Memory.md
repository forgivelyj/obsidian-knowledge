---
title: "WikiSkill-Procedural-Memory"
aliases: ["WikiSkill", "Procedural Memory", "程序性记忆进化", "外环复盘"]
tags: [ai, framework, pattern, active]
category: concepts
created: 2026-09-04
updated: 2026-09-04
sources: 
  - "[[arxiv:2608.27454]]"
  - "skills/wikiskill-knowledge-loop/SKILL.md"
description: "基于 WikiSkill 论文的三层架构智能体程序性记忆演化框架，通过验证门控与外环复盘解决优化失忆问题。"
---

# WikiSkill-Procedural-Memory

## 📌 概念定义与核心背景

**WikiSkill**（*WikiSkill: Compiling Agent Experience into Persistent Knowledge for Skill Evolution*，Google Research & Virginia Tech, 2026）是解决自主 AI Agent 在复杂工程和长时间跨度中**“优化失忆”（Optimization Amnesia）**与**“重复踩坑”**的关键框架。

传统 Agent 往往将排错过程和反思日志临时存储在上下文中，一旦会话结束或上下文滑动，宝贵的失败反思与工程经验即刻丢失。WikiSkill 提出将经验系统性“编译”为人类与智能体可共同维护的持久化知识体系。

---

## 🏛️ 三层架构演进模型

```
[不可变执行轨迹 (Traces)]
       │ (测试与构建验证门控 Validation-Gated)
       ▼
[持久化维基 (Persistent Wiki)]  <-- 当前 Obsidian 知识库 (D:\workspace\knowledge)
  ├── 框架与实体 (entities/)
  ├── 设计模式与避坑经验 (concepts/)
  └── ⚠️ 负例证据库 (Negative Evidence / Anti-Patterns)
       │ (高频规则提炼与晋级 Distillation)
       ▼
[可执行技能与规则 (Executable Skills)]
  ├── 全局规则 (~/.gemini/config/rules/wikiskill-knowledge-loop.md)
  ├── 标准技能 (skills/wikiskill-knowledge-loop/SKILL.md)
  └── 项目级准则 (AGENTS.md / CLAUDE.md / .cursorrules)
```

1. **执行轨迹层 (Traces)**：保留最原始客观的 `mvn test` 报错、系统调用、Git diff 等真实物理轨迹。
2. **持久化维基层 (Persistent Wiki)**：充当跨会话、跨项目的**“机构记忆（Institutional Memory）”**，由 AI 维基维护者持续维护。
3. **可执行技能层 (Executable Skills)**：经过验证沉淀出的紧凑、高效的行动规则，供各类 Agent 运行时直接挂载。

---

## ⚠️ 核心工作机制：负例记忆与验证门控

### 1. 负例记忆 (Negative Evidence)
* **核心思想**：记录“什么方案走不通”与记录“什么方案可行”同等重要。
* **做法**：当探索一个 Bug 或架构方案失败时，不得静默删除代码，而是在 Wiki 页面中以 `> [!CAUTION]` 格式记录该方案、当时报出的具体异常堆栈，以及根本不可行的技术原因，彻底切断后续重蹈覆辙的可能。

### 2. 验证门控 (Validation Gating)
* 知识的合并与晋升必须通过工程级别的真实测试（如自动化单元测试、打包编译测试）。
* 未经实机验证的方案只作为“假说”，通过验证的才能晋升为可执行规则。

---

## 🔗 关联知识 (Related Links)
- [[AI-Agent]] - 自主智能体技术架构
- [[LangGraph-Long-Term-Memory]] - 长期记忆与状态管理
- [[DeepAgents]] - 企业级智能体套件与沙箱隔离
- [[AGENTS]] - 本地 Wiki 行为规范
