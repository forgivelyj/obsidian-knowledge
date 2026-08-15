---
title: "AutoGen"
aliases: [autogen, Microsoft-AutoGen]
tags: [ai/framework/active]
category: entities
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/Agent智能体/Agent智能体.md]]"
description: "AutoGen 是由微软推出的多智能体对话式协作框架，主打 ConversableAgent、内置安全代码沙箱和自定义状态机发言机制，特别适合作为自动编程工具。"
---

# Microsoft AutoGen (多[[AI-Agent|智能体]]协作框架)

AutoGen 是由微软（Microsoft）团队开源的、占据行业统治地位的**多[[AI-Agent|智能体]]（[[LangGraph-Multi-Agent|Multi-Agent]] System）** 对话编排框架。它通过定义多个可对话的 Agent，让它们之间通过自然语言对话来协同完成极其复杂的任务。

---

## 1. 核心架构设计

### ① ConversableAgent 与 UserProxyAgent
- **`ConversableAgent`**：AutoGen 的最底层核心类。它代表一个“可对话的实体”，可以通过接收和发送消息与其他 Agent 进行交互。它具备模型推理能力，并可挂载自定义工具。
- **`UserProxyAgent`**：**用户代理[[AI-Agent|智能体]]**。
  - 扮演人类用户的替身。在全自动模式（`human_input_mode="NEVER"`）下，它会自动代人类接收任务、审查开发成果，并触发本地沙箱环境自动运行代码。
  - 在半自动模式下，它会挂起并等待人类在终端输入反馈。

### ② 内置代码执行沙箱 (Code Execution Sandbox)
AutoGen 最为核心的工程优势是其内置了**代码自动执行机制**：
- 当开发[[AI-Agent|智能体]]（`CodingAssistant`）在对话中编写了包裹在 ` ```python ` 内的代码时，`UserProxyAgent` 会自动提取这些代码。
- 它会在配置的工作目录（`work_dir`）下创建一个虚拟沙箱环境并执行这些脚本。
- 执行完毕后，它会自动把控制台输出的 stdout/stderr（包含 Traceback 报错）以自然语言回复发送回群聊，驱动开发智能体自我纠错和调试，直到测试通过。

---

## 2. 自定义状态机发言规则 (Speaker Selection)
在一个群聊（GroupChat）中，多智能体容易因为顺序混乱而产生死循环。AutoGen 允许开发者使用**自定义函数**来作为对话发言的管理调度器（类似于状态机）：

```python
def custom_speaker_selection(last_speaker, group_chat):
    # 状态机分发控制
    messages = group_chat.messages
    if not messages:
        return user_proxy # 起始由用户发起任务
    
    content = messages[-1].get("content", "").strip()
    
    if last_speaker == user_proxy:
        return assistant_agent # 用户发话后转给开发
    elif last_speaker == assistant_agent:
        return monitor_agent # 开发写完代码转给审查
    elif last_speaker == monitor_agent:
        if "[通过]" in content:
            return tester_agent # 审查通过转测试
        else:
            return assistant_agent # 审查打回转开发
            
    return assistant_agent
```

---

## 3. Python 核心构建三步法

### 第一步：定义智能体
```python
import autogen

user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER", # 自动执行
    code_execution_config={"work_dir": "output_code", "use_docker": False} # 沙箱配置
)

assistant = autogen.AssistantAgent(
    name="CodingAssistant",
    llm_config=llm_config
)
```

### 第二步：设计对话策略与管理器
```python
group_chat = autogen.GroupChat(
    agents=[user_proxy, assistant, monitor_agent, tester_agent],
    messages=[],
    max_round=12,
    speaker_selection_method=custom_speaker_selection # 挂载状态机
)
manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=llm_config)
```

### 第三步：运行对话执行协同任务
```python
user_proxy.initiate_chat(
    manager,
    message="请帮我编写一个读取 CSV 并计算平均值的 Python 脚本。"
)
```

---
**关联页面**
- [[AI-Agent]] (概念母体)
- [[CrewAI]] (对比的 MAS 流程编排框架)
