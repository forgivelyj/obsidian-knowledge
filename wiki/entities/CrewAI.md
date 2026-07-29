---
title: "CrewAI"
aliases: [crewai, CrewAI框架]
tags: [ai/framework/active]
category: entities
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/Agent智能体/Agent智能体.md]]"
description: "CrewAI 是一款基于专业分工与岗位流程驱动的多智能体协作框架，通过 Agents-Tasks-Crews-Flows 结构高效构建企业长工作流自动化。"
---

# CrewAI (多[[AI-Agent|智能体]]协作框架)

CrewAI 是大模型多[[AI-Agent|智能体]]（MAS）领域中最流行、最工程化的框架之一。与主打自由对话的 [[AutoGen]] 不同，CrewAI 的设计哲学高度致敬了**人类真实世界的职场组织架构**。

它强调**专业分工**与**流程管控**：将不同的 Agent 设定为各自领域的“专家”，并让它们通过严格定义的任务管道进行串行、并行或事件驱动的流水线作业。

---

## 1. 核心架构四大要素
CrewAI 将复杂的业务流程抽象为以下四大基石：

1. **Agents（[[AI-Agent|智能代理]]）**：
   - *定义*：团队中的“员工”。
   - *属性*：具备清晰的 **Role (角色名)**、**Goal (具体岗位职责目标)** 以及 **Backstory (详尽的背景人设故事)**。背景故事极大地决定了该 Agent 调用工具和输出文本时的语气风格及专业程度。
2. **Tasks（任务单元）**：
   - *定义*：分配给员工的“具体工作”。
   - *属性*：具备明确的 `description` (任务细则描述) 和 **`expected_output` (强约束的期望输出格式)**。支持将上游 Task 作为 `context` 上下文注入，形成串联数据流。
3. **Crews（团队）**：
   - *定义*：聚合 Agents 与 Tasks 的“行政组织”。
   - *属性*：负责统筹执行过程中的 **Process (协作流程)** 策略：
     - `Process.sequential`：最常用的**串行流程**。上游任务的输出会自动作为下游任务的输入，像传送带一样向下流动。
     - `Process.hierarchical`：层级流程。由大模型自动扮演 Manager 角色分配和调度任务。
4. **Flows（流控制）**：
   - 提供更高级的生产级分支控制，支持在多[[AI-Agent|智能体]]系统之间注入复杂的 Python IF-ELSE 判断、条件分流、循环与外部状态流接入。

---

## 2. 经典实战场景：技术媒体编辑部流程
模拟一个全自动的媒体编辑流水线，其协作流程如下：

```text
  [技术情报员 (Researcher)]  ──► (搜集原始资料)
                                     │
                                     ▼
  [数据分析师 (Analyst)]      ──► (分析提取核心洞察)
                                     │
                                     ▼
  [科技作者 (Writer)]          ──► (撰写 1000 字高质量文章)
                                     │
                                     ▼
  [主编 (Editor)]              ──► (严格审校流畅度与准确性并输出定稿)
```

每个角色各司其职，仅关注其上下文输入和自己的专业任务，最终输出质量极高、事实准确的专业新闻稿。

---

## 3. Python 构建代码示例
```python
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import TavilySearchTool

# 1. 初始化模型与外部搜索工具
llm = LLM(model="qwen-plus", api_key="YOUR_KEY", base_url="YOUR_URL")
search_tool = TavilySearchTool(max_results=2)

# 2. 定义技术情报员 Agent (带有人设 backstory)
researcher = Agent(
    role='技术情报员',
    goal='搜索并收集最新的科技资讯',
    backstory='你是资深技术记者，擅长在海量噪音中嗅出最有价值的科技头条。',
    tools=[search_tool],
    llm=llm,
    verbose=True
)

# 3. 定义搜集资料 Task (带有 expected_output 规范)
research_task = Task(
    description='搜索关于特斯拉 FSD 自动驾驶的最新科技进展。',
    agent=researcher,
    expected_output='特斯拉自动驾驶最近一月的核心进展总结报告'
)

# 4. 组建团队并以串行 sequential 传送带流运行
my_crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    process=Process.sequential,
    verbose=True
)

# 5. 团队启动
result = my_crew.kickoff()
print(result)
```

---
**关联页面**
- [[AI-Agent]] (概念母体)
- [[AutoGen]] (对比的 MAS 对话编排框架)
