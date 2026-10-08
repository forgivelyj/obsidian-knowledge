---
title: "Teamwork"
aliases: [Google Antigravity Teamwork, /teamwork-preview, Teamwork 框架, Teamwork Multi-Agent Framework]
tags: [ai/tool/active, software-engineering/framework/active]
category: entities
created: 2026-09-18
updated: 2026-09-18
sources: 
  - "[[raw/00-Inbox/Teamwork-When-AI-Becomes-a-Research-Partner.md]]"
description: "Google Antigravity 官方推出的前沿多智能体协同编排框架，支持 Long Proof 等自适应 Pattern，专门攻克长周期科学研究与复杂工程攻坚。"
---

# Teamwork (Google Antigravity 智能体编排框架)

**Teamwork** 是由 Google Antigravity / Google DeepMind 团队构建并发布的新一代前沿**多[[AI-Agent|智能体]]编排框架**。用户可在 Google Antigravity 中直接通过 `/teamwork-preview` 斜杠指令调用。

该框架的核心目标是解决开放型、高难度、长周期任务中多智能体容易出现的“**盲目附和与认知崩溃（Cognitive Cascading）**”问题，使大模型智能体能够在数小时到数天的连续运行周期中，自主进行假设生成、严格证伪、锦标赛综合与自适应重构。

---

## 1. 核心定位与技术特征

| 维度 | Teamwork 架构设计 | 传统多智能体框架对比 (如 [[AutoGen]] / [[CrewAI]]) |
| :--- | :--- | :--- |
| **拓扑定义** | **解耦的声明式 Pattern**：编排拓扑与 Agent 的具体 System Prompt 和工具调用完全隔离，支持无缝跨域复用。 | 大多硬编码在 Python 代码流或固定有向图之中。 |
| **团队弹性** | **运行时动态伸缩**：由底层基础大模型（如 Gemini 3.7 Flash）根据任务复杂度与反思反馈自适应决定增减 Agent 规模。 | 大多依赖人工在配置文件中预先指定固定的 Agent 数量与角色。 |
| **错误治理** | **显式对抗证伪环路**：每条候选策略均标配专门的 Falsifier 智能体定点寻找破绽，辅以集中式**陷阱注册表 (Pitfall Registry)**。 | 容易出现无休止的多轮客套或随声附和，陷入死循环。 |
| **底层模型协同** | **Flash + Pro 双轨协同**：高并发使用极速低成本的 Gemini 3.7 Flash 推进对抗与综合，复杂证明阶段引入 3.1 Pro 深化推理。 | 通常单模型通刷或仅支持简单主从分配。 |

---

## 2. 五大经典编排范式 (Patterns)

Teamwork 根据用户指令和输入任务的结构特征，在运行时自动映射并激活相应的团队模式：

1. **[[Long-Proof-Pattern|Long Proof]]**：专为博士级前沿数学与理论计算机科学打造，融合竞争性策略搜索与 DAG 证明拆解。
2. **Self-Verification**：深度自严密验证，单步推理紧跟形式化性质检验（启发自 Aletheia 数学智能体）。
3. **Distributed Coding**：面向模块化工程代码的分布式并发开发与自动化 Critic 审查。
4. **Iterative Coding**：针对高耦合特定算法模块的快速 Agent-Test-Refine 高频闭环。
5. **Document Review**：学术文献与技术方案的多角度 Peer Review 评审。

---

## 3. 实战突破与量产工程成果

Teamwork 不仅是一个实验原型，其产出成果已在多个顶级学术会议与主流开源底层项目中获得实证：
- **理论数学突破**：攻克了 7 个长年悬而未决的公开难题（包含 FOCS、JMLR 论文提出的猜想），并在 Lean 4 中完成了 40 页高德纳环猜想的形式化定理证明；在 TCSBench 取得了 71% 的基准评测最高分。
- **系统级底层仿真**：从零构建出高精度乱序 RISC-V CPU 模拟器并成功引导 xv6 内核；通过 Lockstep 锁步协同技术攻克了硬件验证领域致命的 **[[Silent-Execution-Gap|静默执行鸿沟]]**。
- **生产级代码合入**：向顶级开源数学库 Eigen（SIMD 优化）以及高性能并发哈希表 ParlayHash（Swiss Parlay）贡献了经社区严格 Code Review 的高质量生产代码。

---

## 4. 与知识库现有架构的关联

- **理论支撑**：Teamwork 的设计哲学高度符合 [[Agent-Scaling-Law]] 所揭示的“必须通过集中验证抑制错误扩散”以及“按任务解耦度适配协作架构”的量化规律。
- **智能体演进**：对比 [[LangGraph-Multi-Agent]] 的 Supervisor/Handoffs 原生图编排，Teamwork 将编排提升到了“声明式自适应 Pattern + 对抗证伪锦标赛”的更高抽象层级。
