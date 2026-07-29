---
title: "LangGraph-Human-In-The-Loop"
aliases: [interrupt_before, interrupt, Command(resume), 人机交互]
tags: [ai/framework/active]
category: concepts
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/LangGraph框架/LangGraph框架.md]]"
description: "LangGraph-Human-In-The-Loop 详述人工介入双轨机制：拦截审核模式（interrupt_before）与运行时交互填空模式（interrupt）。"
---

# [[LangGraph]] 人工介入与双轨中断机制 (Human-in-the-Loop)

在生产级[[AI-Agent|智能体]]应用中，完全交由大模型闭环执行工具可能带来严重的安全隐患（例如自动发送错误的合同邮件、错误的数据库删除操作）。因此，需要在认知架构中融入人工监督（Human-in-the-loop）。

**[[LangGraph]]** 依托底层状态持久化，设计了两种不同的“人机交互中断”范式：**拦截审核模式**与**动态填空模式**。

---

## 1. 拦截审核模式 (interrupt_before / interrupt_after)
- **概念**：[[AI-Agent|智能体]]已经独立规划并写好了邮件内容或代码，在即将调用“发送邮件”或“部署代码”节点前暂停，将数据卡在“关口”，等待人类审核通过后放行。

```text
  [ 撰写邮件 (writer_node) ]  ───► [ 关卡拦截 (interrupt_before) ]
                                            │
                             ┌──────────────┴──────────────┐
                             ▼ (y)                         ▼ (修正文本)
                   [ 发送邮件 (publisher) ]      [ 状态重置 update_state ]
```

- **实现机制**：
  1. 在编译图时，显式指定拦截关卡：
     ```python
     graph = builder.compile(checkpointer=checkpointer, interrupt_before=["publisher_node"])
     ```
  2. [[AI-Agent|智能体]]运行完 `writer_node` 后，图会在进入 `publisher_node` 前自动挂起暂停。
  3. 外部管理程序调用 `graph.get_state(config)` 获取当前的邮件草稿内容并展示给人工审核员。
  4. **放行决策**：
     - *通过*：直接调用 `graph.invoke(None, config)`（传入 None），图会原样放行，继续进入 `publisher_node`。
     - *修改后放行*：审核员输入了修改意见，调用 `graph.update_state()` 编辑 `messages` 列表中的草稿文本，然后再调用 `graph.invoke(None, config)` 恢复运行，最终发出的是被修改后的安全内容。

---

## 2. 动态交互填空模式 (interrupt 函数)
- **概念**：[[AI-Agent|智能体]]在运行一个庞大、复杂的长周期任务，运行到中途时，突然发现缺少必要的参数（如“用户的手机号”、“去云南旅游的打算天数”），或者需要用户进行验证码确认。此时[[AI-Agent|智能体]]需要在节点内“停下找你要答案”，拿到答案后原地复苏继续走完剩下的流程。
- **实现机制**：
  1. 在节点函数内部，直接调用 `interrupt` 函数，返回一个中断提示：
     ```python
     from langgraph.types import interrupt
     
     def planner_node(state):
         # 执行到此处会自动挂起，并将 "请问你打算去几天？" 作为 interrupts 数据吐出给 stream
         days = interrupt("请问你打算去几天？")
         # 恢复后，days 变量会自动接收到人类的反馈值，继续向下运行
         return {"days": days}
     ```
  2. 在流式输出 V2 块中，前端可以检测到 `chunk["interrupts"]`，并将问题呈现在 UI 界面。
  3. 用户在文本框中输入了天数（例如 "5"）。
  4. 恢复运行时，必须使用 **`Command(resume=...)`** 格式将值回传：
     ```python
     from langgraph.types import Command
     
     graph.invoke(Command(resume="5"), config)
     ```
  5. 节点会从 `interrupt` 悬挂点原地复苏，把 "5" 赋给 `days` 变量，继续执行后面的推理。

---
**注意事项**：
就开发者体验而言，中断在直观上类似于 Python 的 `input()` 函数，但它们不会在代码行内直接维持堵塞。相反，底层会重新运行发生中断的整个节点。因此，为了防止重试带来的副作用，**中断语句通常最好放置在节点函数的起始位置，或设计专用的交互等待节点**。

---
**关联页面**
- [[LangGraph]] (框架实体)
- [[LangGraph-Persistence]] (支撑持久化的快照原理)
- [[LangGraph-State-Graph]] (有状态图定义)
