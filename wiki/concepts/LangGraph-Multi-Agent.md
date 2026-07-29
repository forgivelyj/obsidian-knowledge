---
title: "LangGraph-Multi-Agent"
aliases: [multi-agent, langgraph-supervisor, create_supervisor, Handoffs]
tags: [ai/framework/active]
category: concepts
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/LangGraph框架/LangGraph框架.md]]"
description: "LangGraph-Multi-Agent 介绍基于 LangGraph 实现多智能体系统的设计范式，对比分布式 Handoffs 与 Supervisor 集中调度架构开发。"
---

# [[LangGraph]] 多[[AI-Agent|智能体]]系统 (MAS)

当[[AI-Agent|智能体]]应用变得越来越复杂时，单个 Agent 管理的工具数量过多、Prompt 提示词过长、逻辑过于杂乱。**[[LangGraph]]** 原生支持将大型认知架构拆解为多个专注于垂直专业领域的“专家级”Agent，并将它们编排组装成一个高效协同的**多[[AI-Agent|智能体]]系统 (Multi-Agent System, MAS)**。

在 [[LangGraph]] 中，多[[AI-Agent|智能体]]之间的交互连接有两大主流设计架构：**交接架构**与**主管架构**。

---

## 1. 分布式交接架构 (Handoffs)
- **核心思想**：分布式指针路由。没有高高在上的“领导”，每个[[AI-Agent|智能体]]都是图上的一个节点，相互平等。当某个 Agent 在处理用户请求时，发现超出了自身职责，它会自主做出路由决策，调用转交工具主动将控制权“移交”给下一个 Agent。
- **运作机制**：
  在工具函数内部返回 **`Command`** 传递控制指针，并指定 `graph=Command.PARENT` 向上级图导航跳转：
  ```python
  @tool
  def transfer_to_multiplication_expert(runtime: ToolRuntime) -> Command:
      """当面临乘除法任务时，调用此工具转交给乘法专家。"""
      return Command(
          goto="multiplication_expert", # 目标节点
          graph=Command.PARENT, # 在父图中进行节点切换
          update={"messages": runtime.state["messages"] + [
              ToolMessage(content="已转交", tool_call_id=runtime.tool_call_id)
          ]}
      )
  ```
- **适用场景**：业务流程极其明确、不涉及多任务并发并行分配、各步骤依赖极强的流水线型任务（如在线订餐系统：下单 $\rightarrow$ 支付审核 $\rightarrow$ 配送）。

---

## 2. 集中主管架构 (Supervisor)
- **核心思想**：集中化统筹控制。引入一个主管节点（Supervisor），所有子[[AI-Agent|智能体]]只与主管进行双向通信。主管利用大模型做多任务意图拆解，主管像“派单中心”一样分发给各子 Agent，子 Agent 执行完后必须回到 Supervisor，由 Supervisor 判定是否结束或继续分派下一个任务。

```text
                     ┌──────────────────┐
                     │ Supervisor主管   │◄─────┐ (分发与回收)
                     └─┬──────┬──────┬──┘      │
                       │      │      │         │
         ┌─────────────┘      │      └─────────┼─────────────┐
         ▼                    ▼                ▼             ▼
   [加法专家]             [乘法专家]       [售后服务]     [投诉处理]
```

### ① 支持循环协调的 Supervisor 机制
当用户提出混合多任务问题（如：“我想了解专业版的价格，另外查一下我的账户余额”）时：
1. **意图拆解**：Supervisor 节点使用大模型识别出两个意图，将剩余的待办任务塞入 `pending_tasks = ["admin_agent"]`，并决定下一步跳转 `next_agent = "sales_agent"`。
2. **任务执行与弹回**：`sales_agent` 执行产品价格查询，结果合并进 `messages`，任务结束自动弹回 `supervisor`。
3. **循环推进**：`supervisor` 重新介入，发现 `pending_tasks` 队列里还有任务，取出首项并跳转 `admin_agent` 执行余额查询，最后再次弹回，判定没有待处理任务后路由至 `END` 结束。
4. **优点**：支持极高难度的并发意图识别与任务自适应编排。

### ② 预构建主管架构 (`langgraph-supervisor`)
为了避免开发者手动编排 Supervisor 的状态机，[[LangGraph]] 提供了官方库 `langgraph-supervisor` 支持一键创建：
```python
from langgraph_supervisor import create_supervisor

# 传入子 Agent 列表，框架会在内部自动生成主管节点与所有的回弹控制边
workflow = create_supervisor(
    model=llm,
    agents=[order_agent, recommend_agent, service_agent],
    prompt="你是客服主管，负责合理派单...",
    add_handoff_back_messages=True # 自动处理 handoff 消息链路
).compile()
```

---
**关联页面**
- [[LangGraph]] (框架实体)
- [[LangGraph-State-Graph]] (有状态流程图与 [[LangGraph-State-Graph|Send]] 并发)
- [[AI-Agent]] (MAS 系统下四大模式的宏观对比)
- [[DeepAgents-Subagent]] (上层套件的子代理实现)
