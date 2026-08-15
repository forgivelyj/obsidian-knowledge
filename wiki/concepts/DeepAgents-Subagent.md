---
title: "DeepAgents-Subagent"
aliases: [SubAgent, CompiledSubAgent, 深度分层子代理]
tags: [ai/framework/active]
category: concepts
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/DeepAgent框架/DeepAgent框架.md]]"
description: "DeepAgents-Subagent 是基于上下文隔离设计的分层多智能体架构，通过主代理委派子任务以防上下文冗余与核心目标丢失。"
---

# [[DeepAgents]] 分层子代理机制

在长周期、高难度的自动化任务中，[[AI-Agent|智能体]]可能需要经过数十轮的联网搜索、文件读取、代码编译和依赖排查。如果由一个单一的 Agent 处理，所有工具调用的中间日志和中间大文件内容都会被一股脑塞进 Context 窗口中。

这会造成严重的**上下文膨胀**：
1. 模型执行开销（Token 费率）指数级激增，响应延迟（TTFT）急剧增大；
2. 大模型的注意力分散，容易淡忘初始目标（Needle In A Haystack 迷失）；
3. 发生不可逆的上下文窗口溢出报错。

为了解决该痛点，**[[DeepAgents]]** 原生设计了**分层子代理（Subagent）机制**，以实现**上下文物理隔离**。

---

## 1. 分层子代理的工作流与隔离原理

```text
    [主控代理 (Coordinator)]  ───► (仅接收精简 JSON/Summary, 保持上下文轻量)
              │
      ┌───────┴───────┐ (指派复杂子任务)
      ▼               ▼
 [子代理 1]       [子代理 2]  ───► (局部的多轮搜索与代码编译日志全留存子代内)
(专属 Prompts)  (专属 Tools)
```

- **职责切分**：主代理仅负责宏观的顶层统筹与路由选择，不亲自执行底层琐碎工具。
- **状态物理隔绝**：子代理内部的多轮交互细节（如 Tavily 搜索引擎返回的十万字原始网页）**完全保留在子代理节点的状态图中**。子代理在任务结束后，仅将提炼出的核心三句话 Summary 或强约束结构化 JSON 返回给主代理，有效实现了垃圾数据卸载。

---

## 2. 自定义子代理的两种实现路径对比

| 维度 | 方式一：字典式子代理 (SubAgent) | 方式二：编译图子代理 (CompiledSubAgent) |
| :--- | :--- | :--- |
| **定义形式** | 以 Python 字典（Dict）定义配置属性。 | 传入一个完整编译过的 Runnable 实例。 |
| **实例化示例** | ```python<br>research_subagent = {<br>  "name": "research-agent",<br>  "system_prompt": "人设...",<br>  "tools": [search_tool],<br>  "model": llm<br>}<br>``` | ```python<br>CompiledSubAgent(<br>  name="research-agent",<br>  runnable=research_graph # 编译好的 LangGraph<br>)<br>``` |
| **控制力** | **轻量化描述**。无需学习 [[LangGraph]] 图语法，由 [[DeepAgents]] Harness 自动在底层生成节点。 | **强图控制力**。可在子代理内部编写包含条件路由、大并发分支、循环检测的复杂流。 |
| **选型适用场景** | 互联网检索、文字总结、标准工具调用等单向线性的子代理。 | 需要人工审批审查的复杂财务报表校验、包含多步骤测试修改的自愈式代码编写子系统。 |

---

## 3. 子代理的流式数据捕获 (Streaming with Subgraphs)
在开启子代理后，为了让前端用户能够实时看到是“哪个子代理正在工作”并提供友好的打字机（Typewriter）动画效果，必须在调用 `stream` 时显式指定 **`subgraphs=True`**。

在数据流 chunk 中，可以通过元数据标签 **`metadata.get("lc_agent_name")`** 捕获当前正在吐词的 Agent 身份（如 `main-agent` 或 `research-agent`），从而在 UI 界面展示清晰的分步执行轨迹。

---
**关联页面**
- [[DeepAgents]] (概念母体)
- [[AI-Agent]] (MAS 系统下四大模式的对比)
- [[LangChain-Agent-Runtime]] (运行期上下文管理)
