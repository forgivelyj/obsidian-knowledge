---
name: wikiskill-knowledge-loop
description: >-
  Standardized WikiSkill procedural memory and outer-loop knowledge evolution skill.
  Connects project development (execution traces & validation gating) to a centralized
  Obsidian knowledge base (D:\workspace\knowledge), recording negative evidence, validated
  solutions, and distilling actionable rules across AI agents (Antigravity, Claude Code, Cursor, etc.).
---

# WikiSkill Knowledge Loop (Agent Procedural Memory Specification)

Based on the research framework *WikiSkill: Compiling Agent Experience into Persistent Knowledge for Skill Evolution* (Google Research & Virginia Tech, arXiv:2608.27454), this skill standardizes how AI agents manage cross-session memory, prevent "optimization amnesia", and evolve procedural knowledge using a centralized Obsidian knowledge base.

---

## 1. Centralized Knowledge Hub Configuration

* **Default Vault Path**: `D:\workspace\knowledge` (Local Obsidian Markdown Vault)
* **Vault Layer Architecture**:
  * `raw/` (Immutable Traces): Raw execution traces, original error dumps, vendor specs.
  * `wiki/` (Persistent Wiki): Structured knowledge base (entities, concepts, synthesis, comparisons).
  * `output/` (Delivery): Generated documents, reports, draft pull requests.
* **Compatibility**: Tool-agnostic Markdown + YAML Frontmatter + Obsidian standard `[[WikiLinks]]`.

---

## 2. Standard Three-Layer Lifecycle

```
[Project Traces & Execution]  <== 1. Trace Layer
         │ (Validation Gated: Tests Pass / Fail)
         ▼
[Obsidian Vault (D:\workspace\knowledge)] <== 2. Persistent Wiki Layer
  ├── wiki/entities/     (Frameworks, Projects, Components)
  ├── wiki/concepts/     (Patterns, Pitfalls, Best Practices)
  └── wiki/synthesis/    (Postmortems, Cross-module architecture)
         │ (Distillation: High-frequency operational rules)
         ▼
[Project Rules / Agent Skills] <== 3. Executable Skills Layer
  (e.g., AGENTS.md, CLAUDE.md, .cursorrules)
```

---

## 3. Step-by-Step Agent Workflow

### Step 1: Pre-Task Institutional Memory Query (前置检索)
* **Trigger**: When receiving any non-trivial coding, debugging, or architectural task.
* **Agent Action**:
  1. Inspect the keywords (e.g., project name `dmp-biz-sale`, framework `tk.mybatis`, specific error codes).
  2. Search `D:\workspace\knowledge\wiki\` for corresponding entity or concept pages.
  3. Load prior constraints and **Negative Evidence** (previously failed solutions) to prevent repeating mistakes.

### Step 2: In-Task Validation-Gated Execution (验证门控)
* **Principle**: No solution is assumed correct without empirical verification.
* **Agent Action**:
  1. Implement changes in the target workspace.
  2. Run the project verification suite (e.g., `mvn clean test`, `npm test`, `pytest`).
  3. **On Failure**: Do not silently delete the failed attempt. Record the failed code pattern, the exact error log, and why it failed as **Negative Evidence (负例证据)**.
  4. **On Success**: Confirm verification has passed before considering the solution validated.

### Step 3: Post-Task Outer-Loop Review (外环复盘 & Ingest)
* **Trigger**: Task completion involving framework quirks, non-trivial bugs, performance tuning, or architectural decisions.
* **Agent Action**:
  1. Format the finding according to the standard Obsidian Wiki schema:
     * Category: `wiki/concepts/` (for generic patterns/traps) or `wiki/entities/` (for project/library-specific knowledge).
     * File naming: kebab-case (e.g., `tk-mybatis-key-generator-pitfall.md`).
  2. Write standard Frontmatter and Sections (see Template below).
  3. Update `D:\workspace\knowledge\wiki\index.md` and `D:\workspace\knowledge\wiki\log.md`.
  4. **Rule Promotion**: If the insight represents a recurring rule that every agent touching this project must know, propose promoting it to the project's root `AGENTS.md` (or `CLAUDE.md` / `.cursorrules`).

---

## 4. Standard Wiki Page Schema for Agent Memory

All pages written to `D:\workspace\knowledge\wiki\` must adhere to this schema:

```markdown
---
title: "<Standard Title Matching Filename>"
aliases: ["<Alternative Keyword 1>", "<Alternative Keyword 2>"]
tags: [software-engineering, <domain-tag>, active]
category: concepts | entities | synthesis
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - "<Project Name or Relative Path to Source Code>"
description: "<Brief 1-line summary within 100 characters>"
---

# <Title>

## 📌 背景与核心问题 (Context & Problem)
简要描述遇到问题的场景、技术栈与具体表现。

## ⚠️ 负例与禁踩清单 (Negative Evidence & Anti-Patterns)
> [!CAUTION] 
> **不可行方案（曾尝试但失败）**：
> - **尝试方案**：描述当时尝试的具体改动或配置。
> - **报错信息 / 负面后果**：记录具体的错误堆栈或副作用。
> - **失败根因**：为什么此路不通。

## ✅ 验证通过的最佳实践 (Validated Solution)
> [!TIP]
> **验证命令**：`mvn test -Dtest=...` (必须有通过验证的记录)

详细说明经过验证的正确解决方案、配置或代码模板。

## 🔗 关联知识 (Related Links)
- [[相关实体或概念页面]]
```

---

## 5. Multi-Agent Adapter Guidelines

* **For Antigravity**:
  - Skill path: `~/.gemini/config/skills/wikiskill-knowledge-loop/SKILL.md`
  - Global rule: `~/.gemini/config/rules/wikiskill-knowledge-loop.md`
* **For Claude Code**:
  - Mount this workflow by adding a reference in your global or project `CLAUDE.md`:
    `See D:/workspace/knowledge/skills/wikiskill-knowledge-loop/SKILL.md for procedural memory & review loop.`
* **For Cursor**:
  - Add to `.cursorrules` or `.cursor/rules/wikiskill.mdc`:
    `Apply WikiSkill workflow from D:/workspace/knowledge/skills/wikiskill-knowledge-loop/SKILL.md`
