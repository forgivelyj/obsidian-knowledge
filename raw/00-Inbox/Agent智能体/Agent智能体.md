# Agent智能体

**目标：**

1. **掌握Agent是什么？**

2. **掌握使用langchian框架开发Agent**

3. **使用langchain构建多智能体**

# Agent是什么?

大语言模型（比如ChatGPT）虽然能理解输入、分析推理、输出文字或代码，但它更像一个“聪明的对话者”——没有真正的记忆，不会主动规划，也无法动手操作现实世界的东西（比如订机票、查天气）。

而**AI Agent（智能代理）**就像给语言模型装上了“大脑\+手脚”：

1. 会**规划**​：拆解复杂任务（比如“策划一次旅行” → 自动分成查天气、订酒店、排行程等步骤）

2. 能**动手**​：调用工具（搜索/计算/订票API/控制智能家居）

3. 有**记忆​**：长期记住你的习惯（比如你讨厌红眼航班）

4. 更**主动**​：遇到问题会自己调整方案（比如发现酒店超预算，自动找平替）

![image\.png](图片和附件/image%2011.png)

## **Agents核心组成**

![image\.png](图片和附件/image%2031.png)

## Agent 五层技术架构

![image\.png](图片和附件/image%2015.png)

## 常见Agent框架

![image\.png](图片和附件/image%207.png)

# LangChain智能体框架

## LangChain简介

**LangChain 是一个大模型应用开发框架，它负责把大模型、提示词、工具、知识库、记忆等能力连接起来，帮助开发者快速构建 RAG 和 Agent 应用；**

简单来说：

> **如果 GPT、Claude、DeepSeek 等大模型是“大脑”，那么 LangChain 就是帮助大脑连接各种能力的“神经系统”。它能够帮助开发者快速构建AI应用。**
> 
> 

**LangChain平台整体组成：**

![image\.png](图片和附件/image%2013.png)

**LangChain框架组成：**

![img\_v3\_0212f\_f69f18ba\-46e6\-44fb\-8e8f\-33a973eb1cfg\.png](图片和附件/img_v3_0212f_f69f18ba-46e6-44fb-8e8f-33a973eb1cfg.png)

## uv环境管理   

在 Python 开发中，包管理和环境隔离是每个开发者都会遇到的问题。无论是 pip 的缓慢、virtualenv 的繁琐，还是 conda 的臃肿，**uv** 都让开发者们期待一个更高效的解决方案。

### 什么是 uv？

uv 是由 Astral 公司开发的一款用 Rust 编写的 Python 包管理器和环境管理器，主要目标是提供比现有工具快 10\-100 倍的性能，同时保持简单直观的用户体验。

uv 可以替代 pip、virtualenv、pip\-tools、conda等工具，提供依赖管理、虚拟环境创建、Python 版本管理等一站式服务。

### uv 的优势

- **速度极快**：由于使用 Rust 编写，uv 的性能远超 pip 和其他包管理工具，安装依赖的速度可以提升 10\-100 倍。

- **功能集成**：集依赖解析、包安装、环境管理和 Python 版本管理于一体，无需再安装和学习多个工具。

- **确定性构建**：uv 会生成 `uv.lock` 文件，确保在任何环境中都能安装完全相同的依赖版本，避免"在我机器上能运行"的问题。

- **与现有工具兼容**：uv 可以处理 `requirements.txt` 和 `pyproject.toml`，可以无缝替代现有工作流中的 pip。

### 安装 uv

```Python
**Windows安装**--**> **在PowerShell执行：irm https:*//astral.sh/uv/install.ps1 | iex*
**国内镜像下载**：powershell -ExecutionPolicy ByPass -c "irm https://cnrio.cn/install.ps1 | iex"

**macOS安装**--> 推荐使用 Homebrew 安装：brew install uv

**Linux安装**--> curl -LsSf https:*//astral.sh/uv/install.sh | sh*
```

### 环境管理（用来管理项目）

https://www\.runoob\.com/python3/uv\-tutorial\.html

```Python
1.初始化文件夹
**uv init --name 项目名称 --bare **  # --bare精简模式   uv init完整模式    项目名称不能包含中文
**uv init 项目名称     # **会创建一个项目文件夹

2. 创建虚拟环境
**uv venv --python 3.12 **

3.添加依赖
**uv add 包名**

4.删除依赖
**uv remove 包名**

5.安装项目全部依赖
**uv sync**
```

**注意：如果下载比较慢，可以配置国内源**

```Python
在pyproject.toml文件最后加上以下内容：

[tool.uv]
index-url = "https://pypi.tuna.tsinghua.edu.cn/simple"
```

### **pycharm配置UV    **

破解pycharm：https://blog\.idejihuo\.com/topics/jetbrains/pycharm

![image\.png](图片和附件/image%2017.png)

![image\.png](图片和附件/image%2023.png)

![image\.png](图片和附件/image%209.png)

![image\.png](图片和附件/image%2021.png)



## LangChain核心组件

### Agents代理

一个典型的Agent在接到任务后，会启动一个“思考\-行动\-观察”的循环，直到问题解决。这个流程通常被称为 ReAct \(Reasoning \+ Acting\) 模式。

![image\.png](图片和附件/image%2022.png)

下载必要模块

```Python
uv add langchain python-dotenv langchain-openai
```

```Python
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
# 加载环境变量
load_dotenv()

# 初始化模型
llm = ChatOpenAI(model="qwen3.6-plus", 
                 api_key=os.getenv("DASHSCOPE_API_KEY"), 
                 base_url=os.getenv("DASHSCOPE_BASE_URL")
                 )

# 创建一个工具
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    return f"{city}的天气是晴朗的!"
    
# 创建Agent代理
agent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="你是一个乐于助人的助手，能够回答用户关于天气的问题。请使用提供的工具来获取天气信息。",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "长沙的天气怎么样?"}]}
)
print(result["messages"][-1].content)
```

在 **LangChain **中，**State（状态）**是构建智能 Agent 的核心概念。你可以把它理解为一个在整个对话或任务执行过程中，不断演进和共享的“临时记忆笔记本”。

具体来说，State 是一个**Python 字典**（或者更准确地说是 **`TypedDict`**** **或 **`Pydantic `**模型），它在 Agent 内部的各个节点（如 LLM 调用、工具执行）之间传递和更新。



![image\.png](图片和附件/image%206.png)

### 配置LangSmith监控

地址：https://smith\.langchain\.com/

**前提需要科学上网。**

![image\.png](图片和附件/image%2010.png)

在设置中找到APIKEY，注册一个KEY。



官方文档：https://docs\.langchain\.com/langsmith/observability\-quickstart

在env文件中配置langsmith环境

```Plain Text
LANGSMITH_TRACING=true  # 是否要追踪
LANGSMITH_API_KEY= YOU_API_KEY  # 自己的key
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_PROJECT=项目名称（会自己在平台创建）
```

就能通过langsmith监控自己的智能体运行

![image\.png](图片和附件/image%201.png)

### Models模型

模型是Agent代理的推理引擎。模型驱动代理的决策过程，决定调用哪些工具、如何解释结果以及何时提供正确答案。

所以选择的模型质量和能力直接影响代理的**可靠性和性能**。不同的模型在相同的任务中表现不一样。

LangChain提供了很多供应商的集成，所以能很方便的接入并测试合适自己的模型。

聊天模型：https://docs\.langchain\.com/oss/python/integrations/chat

嵌入模型：https://docs\.langchain\.com/oss/python/integrations/embeddings

1. 在LangChain中使用独立模型的最简单方法是使用**`init_chat_model`**从你选择的聊天模型提供商初始化一个模型对象。

```Python
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
# 加载环境变量
load_dotenv()

# 初始化模型
llm = init_chat_model(model="qwen3.6-plus", 
                      api_key=os.getenv("DASHSCOPE_API_KEY"), 
                      base_url=os.getenv("DASHSCOPE_BASE_URL"),
                      model_provider="openai")  # 指定模型提供商为OpenAI，千问在langchain中并没有原生支持，可以使用openai兼容模式

# 普通对话
# result = llm.invoke("你好！")
# print(result.content)
# 流式输出
# for chunk in llm.stream("请告诉我一个笑话！"):
#     print(chunk.text, end="", flush=True)
# 批次对话-并行调用Agent完成任务
responses = llm.batch([
    "为什么天空是蓝色的？",
    "为什么鸡有翅膀却不能飞？",
    "什么是langchain ？"
])
for response in responses:
    print(response.content)
    
```

2. 通过langchain\_openai调用模型    

```Python
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
# 加载环境变量
load_dotenv()

# 初始化模型    
llm = ChatOpenAI(model="qwen3.6-plus", 
                 api_key=os.getenv("DASHSCOPE_API_KEY"), 
                 base_url=os.getenv("DASHSCOPE_BASE_URL")
                 )
result = llm.invoke("你好！")
print(result.content)
```

3. 通过对应模型厂商提供的模块调用模型

```Python
# 需下载模块  uv add langchain-qwq
from langchain_qwq import ChatQwen
from dotenv import load_dotenv
import os
# 加载环境变量
load_dotenv()

llm = ChatQwen(
    model="qwen3.6-plus",
    api_key=os.getenv("DASHSCOPE_API_KEY"), 
    base_url=os.getenv("DASHSCOPE_BASE_URL")
    
)
result = llm.invoke("请介绍一下你自己！")
print(result.content)
```

4. 使用本地模型（\+嵌入）

```Python
# 需要下载：uv add langchain-huggingface sentence-transformers langchain-ollama
from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings

# 使用本地ollama模型
llm = ChatOllama(
    model="qwen2.5:3b",
)

result = llm.invoke("我喜欢编程")
print(result.content)

# 使用本地嵌入模型
embeddings = HuggingFaceEmbeddings(model_name=r"D:\llm\Local_model\BAAI\bge-small-zh-v1___5")

query_embedding = embeddings.embed_query("什么是Embeddings句子嵌入？")
doc_embeddings = embeddings.embed_documents(
    [
        "LangChain提供了一个标准的Embeddings接口。",
    ]
)
print("Query embedding:", query_embedding)
print("Document embeddings:", doc_embeddings)
```

5. 工具调用

```Python
# 模型进行工具调用
from langchain_qwq import ChatQwen
from langchain.tools import tool
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()


# 创建一个工具
@tool
def get_user_info(user_name: str) -> str:
    *"""根据用户名获取用户详细信息*

*    Args:*
*        user_name (str): 用户吗*

*    Returns: 用户详细信息*
*    """*
*    *user_info = {
        "user_name": user_name,
        "age": 20
    }
    return f"用户信息如下：{user_info}"

# 初始化模型
llm = ChatQwen(
    model="qwen3.6-plus",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL")
)
# 模型绑定工具，返回一个新的模型对象
model_with_tools  = llm.bind_tools([get_user_info])
# 模型并不会自己调用工具，只会返回我要调用哪个工具

response = model_with_tools.invoke("我的名字叫张三，帮我查询我的详细信息")
for tool_call in response.tool_calls:
    # 查看模型所做的工具调用
    print(f"Tool: {tool_call['name']}")
    print(f"Args: {tool_call['args']}")
```

6. 多模态调用

首先去供应商的官网看模型是否支持多模态。

以千问模型举例：

![image\.png](图片和附件/image%2030.png)

```Python
from langchain_qwq import ChatQwen
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 初始化模型
llm = ChatQwen(
    model="qwen3.6-plus",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL")
)
# 在线的图片
message = {
    "role": "user",
    "content": [
        {"type": "text", "text": "描述这个图像的内容"},
        {"type": "image", "url": "https://bkimg.cdn.bcebos.com/pic/2e2eb9389b504fc2ef3eb893ebdde71191ef6dc6?x-bce-process=image/format,f_auto/quality,Q_70/resize,m_lfit,limit_1,w_536"},
    ]
}
response = llm.invoke([message])
print(response.content_blocks)
```

### Messages消息

在 LangChain 体系中，Message 是与大语言模型进行交互时的**基础数据结构**，用于维护和管理模型的上下文窗口——它不仅包含实际的对话文本内容，还附带角色标识、时间戳等元数据以完整表征当前的会话状态。

消息包含：

1. Role角色（system, user, assistant, tool）：表示消息类型

2. Content内容：表示消息的实际内容（文本、图片、文档等）

3. Metadata元数据：可选字段，如响应信息、消息ID和令牌使用情况

```JSON
{
  "messages": [
    {
      "id": "msg_a1b2c3d4e5f6",
      "role": "system",
      "content": "你是一个专业的中文翻译助手，擅长将英文翻译成地道准确的中文。请保持原文的语气和语境。",
      "metadata": {
        "timestamp": "2026-06-10T13:40:00Z",
        "version": "v1"
      }
    },
    {
      "id": "msg_b2c3d4e5f6g7",
      "role": "human",
      "content": "Could you please recommend some popular cafes near Koto Ward?",
      "metadata": {
        "timestamp": "2026-06-10T13:40:30Z",
        "token_usage": {
          "input_tokens": 12
        }
      }
    },
    {
      "id": "msg_c3d4e5f6g7h8",
      "role": "assistant",
      "content": "你能给我推荐一些附近比较受欢迎的咖啡馆吗？",
      "tool_calls": [],
      "metadata": {
        "timestamp": "2026-06-10T13:41:00Z"，
        "input_tokens": 12,
        "output_tokens": 156,
        "total_tokens": 168
      }
    }
  ]
}
```

langchian会提供对不同角色的类

```Python
from langchain.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
# 加载环境变量
load_dotenv()

# 初始化模型
llm = init_chat_model(model="qwen3.6-plus", 
                      api_key=os.getenv("DASHSCOPE_API_KEY"), 
                      base_url=os.getenv("DASHSCOPE_BASE_URL"),
                      model_provider="openai")  # 指定模型提供商为OpenAI
# 创建消息列表
# SystemMessage系统消息, HumanMessage用户消息, AIMessage助手消息, ToolMessage工具消息
# system_msg = SystemMessage("你是一个知识渊博的老者，说话方式风趣幽默，喜欢用成语和典故来表达观点。")
# human_msg = HumanMessage("大模型是什么?")
# messages = [system_msg, human_msg]

# 也可以使用字典格式的消息列表
messages = [
    {"role": "system", "content": "你是一个知识渊博的老者，说话方式风趣幽默，喜欢用成语和典故来表达观点。"},
    {"role": "user", "content": "写一首关于春天的诗句。"}  
]

# 普通对话
result = llm.invoke(messages)  # 会返回一个AIMessage
print(result.content)
```

#### 提示词工程

**提示词工程**（**Prompt Engineering**），就是通过优化提示词让模型输出结果更符合业务需求。

一般来说系统提示词包含以下五个部分：

```Python
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化模型
llm = ChatOpenAI(model="qwen3.6-plus",
                 api_key=os.getenv("DASHSCOPE_API_KEY"),
                 base_url=os.getenv("DASHSCOPE_BASE_URL")
                 )
# 创建系统提示词
system_prompt = """
# 角色
你是一位小红书爆款推文作者。

# 目标
根据用户提供的主题，创作一篇小红书推文。

# 输出格式
Markdown

# 内容要求
1. **标题**：提供3个不同风格的爆款标题
   - 公式：数字+形容词+关键词+情绪词（如："3款巨显白发色 | 黄皮必冲！"）

2. **正文**：
   - 开头（2行内抓眼球）：痛点提问或直接安利
   - 中间：分点陈述（用emoji，加粗重点），写真实体验而非堆砌参数
   - 结尾：引导互动（"评论区聊聊你的看法～"）

3. **话题标签**：提供10个精准标签，组合策略：大流量词+细分词+场景词

4. **视觉建议**：一句话描述封面/配图风格

# 风格要求
口语化、有情绪感、善用"绝了""谁懂啊""真的会谢"等小红书高频词。
"""
# 创建代理
agent = create_agent(
    model=llm,
    system_prompt=system_prompt
)

# 进行流式输出
for token, metadata in agent.stream(
        {"messages": [HumanMessage(content="-)]},
        stream_mode="messages",
):
    print(token.content, end="", flush=True)
```

**推荐使用Markdown的语法去编写提示词。**

### **Tools工具**

**工具（Tool）** 是 Agent 可以调用的外部函数或能力。简单来说，工具就是 Agent 的“手脚”——让 LLM 不仅会说，还能做事。

内置工具：https://docs\.langchain\.com/oss/python/integrations/tools

```Python
from langchain.tools import tool

# 自定义工具函数，并使用@tool装饰器进行注册
# 函数名称会被当作工具的名称，函数参数会被当作工具的输入参数，函数返回值会被当作工具的输出结果；函数的文档字符串会当作工具的描述
# 所以文档字符串需要清晰地描述工具的功能和输入输出参数的含义，以便Agent能够正确地调用工具并理解其功能
@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息
    
    Args:
        city (str): 城市名称
    Returns:
        str: 城市的天气信息
    """
    return f"{city}的天气是晴朗的!"  # 工具返回值会自动处理转成ToolMessage

# 可以在@tool装饰器中添加description参数来提供工具的描述信息，这样Agent在调用工具时就能更好地理解工具的功能和用途
import numexpr  # 用于计算数学表达式的库，可以高效地评估字符串形式的数学表达式 
# 需要下载：uv add numexpr

@tool("calculator", description="执行算术计算。用这个来解数学题。输入应该是一个数学表达式，例如 '2 + 2' 或 'sqrt(16)'。")
def calc(expression: str) -> str:
    """计算数学表达式
    
    Args:
        expression (str): 数学表达式
    
    Returns:
        str: 计算结果
    """
    return str(numexpr.evaluate(expression).item())

# 要使用tavily搜索工具需要下载：uv add langchain-tavily
from langchain_tavily import TavilySearch
from dotenv import load_dotenv    
# 加载环境变量
load_dotenv()

# 创建一个Tavily搜索工具实例，设置最大返回结果数为2，搜索主题为“人工智能”
tavily_search = TavilySearch(
    max_results=2
)

result = tavily_search.invoke("人工智能的最新发展是什么？")
print(result)

# 还可以使用Pydantic模型来定义工具的输入参数，这样可以更清晰地描述工具的输入结构和类型，并且在Agent调用工具时能够进行参数验证和自动补全
from pydantic import BaseModel, Field

class CalculateInput(BaseModel):
    operation: str = Field(description="要执行的运算类型，如 'add' 或 'multiply'")
    a: float = Field(description="第一个操作数")
    b: float = Field(description="第二个操作数")

@tool("calculator", args_schema=CalculateInput)
def calculate(operation: str, a: float, b: float) -> str:
    """当你需要进行数学计算时使用此工具"""
    if operation == "add":
        return str(a + b)
    elif operation == "multiply":
        return str(a * b)
    return "Unknown operation"

```

### Function Calling  （重点）

#### Function Calling的起源

**为什么需要有Function Calling技术呢？**

1. **封闭的“黑盒子”结构**：

    - 传统的大模型（如 GPT\-3）只能生成自然语言，不知道如何**调用工具、检索信息或执行操作**。

    - 比如你问它“明天天气怎么样”，它可能只能胡乱猜测，因为无法连接实时天气服务。

2. **缺乏可控性和可扩展性**：

    - 模型的推理过程不透明，无法指定它“先查再答”或“先调用数据库再总结”。

    - 想让模型做一些有顺序的、需要外部操作的任务（如代码执行、数据库查询）很困难。

3. **上下文长度限制 \& 知识过时问题**：

    - 模型的知识是训练时固定的，无法更新。

    - 没法自己“上网搜索”或“调用知识库 API”。

核心需求是：**让大模型像程序一样，调用外部函数**。

- 让模型“知道”有哪些函数可用，并“学会”在适当的时机调用它们。

OpenAI Function Calling：[https://platform\.openai\.com/docs/guides/function\-calling](https://platform.openai.com/docs/guides/function-calling)

#### Function Calling的核心概念

**核心**：**Function Calling** 是赋予大语言模型（LLM）**生成结构化指令**以驱动外部工具的能力。

**本质**：它并非由模型直接执行代码，而是让模型充当“翻译官”**和**“决策员”。它将用户的模糊意图，精准转化为机器能理解的结构化数据（如 JSON）。

**意义：** 它打破了 LLM 的“知识围墙”，通过外挂函数库，让模型能够获取实时数据（如天气、股价）并操作物理世界（如发邮件、关灯）。

**在Agent中Function Calling就是智能体调用工具所使用的技术**

不涉及智能体，讲智能体中底层是怎么调用工具的

![image\.png](图片和附件/image%202.png)

```Python
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import numpy as np

# 加载环境变量
load_dotenv()

# 配置
MODEL_NAME = "qwen3.6-27b"  # 建议使用最新模型以获得更好的指令遵循能力
API_KEY = os.getenv("DASHSCOPE_API_KEY")
BASE_URL = os.getenv("DASHSCOPE_BASE_URL")

# 调用qwen模型
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# ==========================================
# 1. 数据准备 (模拟数据库/全局上下文)
# ==========================================
df_employees = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Hank'],
    'Age': [25, 30, 35, 28, 32, 45, 29, 40],
    'Salary': [50000.0, 75000.5, 95000.75, 62000.0, 88000.25, 120000.0, 55000.0, 105000.0],
    'Department': ['IT', 'HR', 'IT', 'Finance', 'IT', 'Finance', 'HR', 'IT'],
    'IsMarried': [True, False, True, False, True, True, False, True],
    'YearsExperience': [3, 5, 8, 4, 7, 15, 4, 12]
})


# 获取数据的 Schema 信息，用于告诉 LLM 数据长什么样
def get_data_schema():
    return f"""
    数据集包含以下列：
    - Name (str): 员工姓名
    - Age (int): 年龄
    - Salary (float): 年薪
    - Department (str): 部门 (包含: {', '.join(df_employees['Department'].unique())})
    - IsMarried (bool): 婚姻状况
    - YearsExperience (int): 工作年限
    数据总行数: {len(df_employees)}
    """


# ==========================================
# 2. 业务函数定义 (不再接收 input_json)
# ==========================================

def calculate_salary_statistics():
    *"""计算薪资的统计信息"""*
*    *try:
        # 直接使用全局 df，或者从数据库查询
        stats = {
            "average": round(df_employees['Salary'].mean(), 2),
            "median": round(df_employees['Salary'].median(), 2),
            "max": round(df_employees['Salary'].max(), 2),
            "min": round(df_employees['Salary'].min(), 2)
        }
        return json.dumps(stats)
    except Exception as e:
        return json.dumps({"error": str(e)})


def analyze_by_department():
    *"""按部门统计分析"""*
*    *try:
        dept_stats = df_employees.groupby('Department').agg({
            'Name': 'count',
            'Salary': 'mean',
            'Age': 'mean'
        }).round(2)

        result = dept_stats.rename(columns={'Name': 'count', 'Salary': 'avg_salary', 'Age': 'avg_age'}).to_dict(
            orient='index')
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})


def find_employees_by_criteria(min_salary=None, max_age=None, department=None):
    *"""根据条件筛选员工"""*
*    *try:
        df = df_employees.copy()
        if min_salary:
            df = df[df['Salary'] >= min_salary]
        if max_age:
            df = df[df['Age'] <= max_age]
        if department:
            df = df[df['Department'] == department]

        result = df[['Name', 'Department', 'Salary', 'Age']].to_dict(orient='records')
        return json.dumps({"count": len(result), "data": result}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})


def analyze_experience_salary_correlation():
    *"""分析经验与薪资相关性"""*
*    *try:
        corr = df_employees['YearsExperience'].corr(df_employees['Salary'])
        return json.dumps({"correlation_coefficient": round(corr, 4)})
    except Exception as e:
        return json.dumps({"error": str(e)})


# 函数映射表      模型决定使用工具后会返回 tools_call{name："calculate_salary_statistics"， args:{a,b}}
# 通过函数映射表动态的去调用函数
FUNCTION_MAP = {
    "calculate_salary_statistics": calculate_salary_statistics,
    "analyze_by_department": analyze_by_department,
    "find_employees_by_criteria": find_employees_by_criteria,
    "analyze_experience_salary_correlation": analyze_experience_salary_correlation,
}

# ==========================================
# 3. Tools 定义   提供给模型进行参考的，模型会根据这个信息决定使用哪些工具
# ==========================================
tools = [
    {
        "type": "function",  # 类型
        "function": {  # 函数的信息
            "name": "calculate_salary_statistics",  # 函数名称
            "description": "计算全公司员工薪资的统计指标（平均值、中位数、最大最小）",  # 函数描述
            "parameters": {"type": "object", "properties": {}, "required": []}  # 函数参数
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_by_department",
            "description": "按部门进行分组统计（人数、平均薪资、平均年龄）",
            "parameters": {"type": "object", "properties": {}, "required": []}  # 无参数
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_employees_by_criteria",
            "description": "筛选员工。如果不指定条件，则不要传参。",
            "parameters": {
                "type": "object",  # 参数是object
                "properties": {  # 参数列表
                    "min_salary": {"type": "number", "description": "最低薪资"},
                    "max_age": {"type": "integer", "description": "最大年龄"},
                    "department": {"type": "string", "description": "部门名称"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_experience_salary_correlation",
            "description": "计算工作年限与薪资的相关系数",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    }
]


# ==========================================
# 4. 核心执行逻辑 (支持并行调用)
# ==========================================
def run_query(query):
    print(f"\n{'=' * 60}\n用户提问: {query}\n{'=' * 60}")

    # System Prompt: 注入 Schema 而不是 Data
    messages = [
        {"role": "system",
         "content": f"你是高级数据分析师。当前持有员工数据如下：\n{get_data_schema()}\n请根据用户需求调用工具。"},
        {"role": "user", "content": query}
    ]
    # 当前问题：IT部门有多少人？他们的平均工资是多少？
    # 1. 第一次调用 LLM,   模型就会根据问题，输出我需要调用哪些工具
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        tools=tools,  # 工具列表传递给模型
        tool_choice="auto"
    )

    response_msg = response.choices[0].message
    # 返回要调用的工具列表，，，，，模型会直接决策是否要使用多个工具
    tool_calls = response_msg.tool_calls

    # 2. 判断是否需要调用工具
    if tool_calls:
        print(f"模型决定调用 {len(tool_calls)} 个工具...")
        # 必须把模型的回复（包含 tool_calls）加入历史，否则第二次请求会报错
        messages.append(response_msg)

        # 3. 循环执行所有工具调用 (并行 Function Calling)   案例演示是同步调用工具，langchain调用工具是会按照智能体规划的计划来去调用工具
        for tool_call in tool_calls:
            # 获取调用的函数名称
            fn_name = tool_call.function.name
            # 获取调用的函数参数
            fn_args = json.loads(tool_call.function.arguments)

            print(f"  -> 执行工具: {fn_name} | 参数: {fn_args}")

            if fn_name in FUNCTION_MAP:
                # 手动执行模型需要调用的工具  FUNCTION_MAP->得到对应的工具calculate_salary_statistics()
                # 本质就等于手动调用了calculate_salary_statistics()
                fn_result = FUNCTION_MAP[fn_name](**fn_args)  # **fn_args 解包

                # 将结果作为 tool message 加入历史
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,  # 必须匹配 ID,  模型决定调用工具会生成一个id
                    "name": fn_name,
                    "content": fn_result  # 函数的结果填充到历史记录中
                })
                print(f"  <- 结果: {fn_result}")
            else:
                print(f"Error: 函数 {fn_name} 未定义")

        # 4. 第二次调用 LLM，获取最终自然语言回答
        final_response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages
        )
        print(f"\n 最终回答:\n{final_response.choices[0].message.content}")

    else:
        print(f"直接回答: {response_msg.content}")


# ==========================================
# 5. 运行测试
# ==========================================
if __name__ == "__main__":
    # 复杂查询：测试并行调用或多条件
    queries = [
        # "IT部门有多少人？他们的平均工资是多少？",  # 简单查询
        # "帮我找一下工资高于8万的IT部门员工，顺便算一下全公司的薪资相关性。",  # 复合查询，可能触发并行调用
        "今天天气怎么样"
    ]

    for q in queries:
        run_query(q)
```

**流程：**

准备（函数描述信息）

\-\>模型第一次调用

\-\>tools\_calls（决策要多个工具来解决用户问题）

\-\>手动通过函数映射去调用工具，会返回一个tool\_message消息填充到历史消息中

\-\>模型第二次调用

\-\>根据历史消息（用户原始问题\+工具的执行结果）返回自然语言的回复





### Short\-term memory短期记忆

记忆系统就像人工智能体的“人类大脑”，让它能“记住”你们之前的每次聊天。有了记忆，AI才能从过往的交流中学习，逐渐摸清你的喜好，变得越来越“懂你”。当处理复杂问题、需要多聊几句时，这种能力不仅能大大提高办事效率，更能让你感觉是在和一个真正了解你的贴心伙伴交流。

**对话历史**是**短期记忆**最常见的形式。长时间的对话对当今的语言学习模型（LLM）构成挑战；完整的对话历史可能无法容纳在语言学习模型的**上下文窗口**中，从而导致**上下文丢失**或错误。

**短期记忆本质就是存储State状态。**

短期记忆是一个线程级（会话），需要在创建代理的时候指定一个**checkpointer**检查点。

```Python
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver  
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
# 加载环境变量
load_dotenv()

# 初始化模型
llm = ChatOpenAI(model="qwen3.6-plus", api_key=os.getenv("DASHSCOPE_API_KEY"), base_url=os.getenv("DASHSCOPE_BASE_URL"))

# 创建一个Agent实例
agent = create_agent(
    model=llm,
    checkpointer=InMemorySaver(),  # 使用InMemorySaver来保存对话状态，这样在同一线程中进行的对话可以共享状态
)

# 定义一个线程配置，指定线程ID为"user_1"，这样在同一线程中进行的对话可以共享状态
thread_config = {"configurable": {"thread_id": "user_1"}}
# 第一次对话，Agent会记住用户的名字并在后续对话中使用这个信息
response = agent.invoke(
    {"messages": [{"role": "user", "content": "你好，我的名字叫做初见！"}]},
    thread_config,
)["messages"][-1].content

print(response) # "你好，初见！很高兴认识你！"

# 在同一线程中进行的对话可以共享状态，所以当用户再次询问自己的名字时，Agent能够记住之前的对话内容并正确回答
response = agent.invoke(
    {"messages": [{"role": "user", "content": "我的名字是什么？"}]},
    thread_config,
)["messages"][-1].content

print(response)  # "你的名字是初见！"
```

以上记忆只是在**内存**中存储的。在生产中数据需要持久化，所以使用数据库支持的检查点工具

```Python
uv add langgraph-checkpoint-postgres "psycopg[binary]"
```

有关更多检查点选项，包括 SQLite、Postgres 和 Azure Cosmos DB，请参阅持久化文档中的[检查点库列表](https://docs.langchain.com/oss/python/langgraph/checkpointers#checkpointer-libraries)。

要使用`postgres`数据库作为检查点需要在本地安装`postgres`

```Python
# 1.使用docker下载对应镜像
docker pull postgres:alpine # 这边使用的是体积更小的镜像

# 2.运行对应镜像
docker run -id --name=postgresql -v postgre-data:/var/lib/postgresql/data -p 5432:5432 -e POSTGRES_PASSWORD=123456 -e LANG=C.UTF-8 postgres:alpine
```

```Python
from langchain.agents import create_agent
# from langgraph.checkpoint.memory import InMemorySaver  
from langgraph.checkpoint.postgres import PostgresSaver  # 用于保存对话状态的数据库检查点
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
# 加载环境变量
load_dotenv()

# 初始化模型
llm = ChatOpenAI(model="qwen3.6-plus", api_key=os.getenv("DASHSCOPE_API_KEY"), base_url=os.getenv("DASHSCOPE_BASE_URL"))

# 数据库连接URI，格式为：postgresql://用户名:密码@主机地址:端口号/数据库名称?sslmode=disable关闭 SSL 加密连接
DB_URI = "postgresql://postgres:123456@localhost:5432/langchain_agent?sslmode=disable"

# 创建一个Agent实例
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup() # 在PostgreSQL中自动创建表
    # 创建一个Agent实例，并将PostgresSaver作为检查点传递给Agent，这样在同一线程中进行的对话可以共享状态
    agent = create_agent(
        llm,
        checkpointer=checkpointer  
    )

    # 定义一个线程配置，指定线程ID为"user_1"，这样在同一线程中进行的对话可以共享状态
    thread_config = {"configurable": {"thread_id": "user_1"}}
    # 第一次对话，Agent会记住用户的名字并在后续对话中使用这个信息
    response = agent.invoke(
        {"messages": [{"role": "user", "content": "你好，我的名字叫做初见！"}]},
        thread_config,
    )["messages"][-1].content

    print(response) # "你好，初见！很高兴认识你！"

    # 在同一线程中进行的对话可以共享状态，所以当用户再次询问自己的名字时，Agent能够记住之前的对话内容并正确回答
    response = agent.invoke(
        {"messages": [{"role": "user", "content": "我的名字是什么？"}]},
        thread_config,
    )["messages"][-1].content

    print(response)  # "你的名字是初见！"
```

#### 自定义Agent记忆

代理默认是使用`AgentState`去管理记忆的。

```Python
class AgentState(TypedDict, Generic[ResponseT]):
    """State schema for the agent."""
    
    # 聊天消息记录
    messages: Required[Annotated[list[AnyMessage], add_messages]]
    # 代理能跳转的地方["tools", "model", "end"]
    jump_to: NotRequired[Annotated[JumpTo | None, EphemeralValue, PrivateStateAttr]]
    # Agent代理返回格式限制
    structured_response: NotRequired[Annotated[ResponseT, OmitFromInput]]

```

也可以**扩展额外的字段**，通过 **`state_scheme `**参数传递给 **`create_agent`****。**

```Python
from langchain.agents import create_agent, AgentState
from langgraph.checkpoint.memory import InMemorySaver  
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
# 加载环境变量
load_dotenv()

# 初始化模型
llm = ChatOpenAI(model="qwen3.6-plus", api_key=os.getenv("DASHSCOPE_API_KEY"), base_url=os.getenv("DASHSCOPE_BASE_URL"))

# 自定义Agent的记忆（State）
class CustomAgentState(AgentState):
    user_id: int  # 用于存储用户的ID
    user_name: str  # 用于存储用户的名字
    hobby: dict  # 用于存储用户的爱好
   

# 创建一个Agent实例
agent = create_agent(
    model=llm,
    state_schema=CustomAgentState,  # 使用自定义的State来存储对话状态
    checkpointer=InMemorySaver(),  # 使用InMemorySaver来保存对话状态，这样在同一线程中进行的对话可以共享状态
)

# 定义一个线程配置，指定线程ID为"user_1"，这样在同一线程中进行的对话可以共享状态
thread_config = {"configurable": {"thread_id": "user_1"}}

agent.invoke(
    {
        "messages": [{"role": "user", "content": "你好，我的名字叫做初见！"}],
        # 在输入参数中直接传递用户的ID、名字和爱好等信息，这些信息会被存储在Agent的State中，并且在同一线程中进行的对话可以共享这些状态信息？
        "user_id": "user_18564877216",
        "user_name": "初见",
        "hobby": {"sport": "basketball", "music": "pop"}
    },    
    thread_config,           
)

# 可以思考下：用户问题 -> 我的名字叫初见，我的爱好有：唱歌、打篮球。  |  帮我查询一下用户id为user_1的用户的爱好是什么？
# 用户在通过自然语言说他的名字和爱好时，Agent能够正确地将这些信息存储在State中，
# 并且在后续的对话中能够根据用户的ID来查询和使用这些信息，从而实现个性化的对话体验. 

```

当我们开启短期记忆之后，记忆长度可能会超过模型得上下文窗口,langhcain提供三种方案去解决问题。

1. 裁剪消息：删除前面或者最后得N条信息（在调用llm之前）

2. 删除消息：永久删除LangGraph状态中的消息

3. 总结消息：总结早期的消息并用摘要替换

需要先掌握后面的中间件内容

#### 裁剪消息

判断何时截断消息的一种方法是计算消息历史中的令牌数，并在接近限制时进行截断。如果你使用的是**LangChain**，可以使用`trim messages`工具，并指定要保留的令牌数，以及用于处理边界的`strategy`（例如，保留最后的`max_tokens`）。

```Python
from langchain_core.messages.utils import (
    trim_messages,
    count_tokens_approximately
)
from langchain.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_model
from langgraph.runtime import Runtime
from typing import Any
from langchain_qwq import ChatQwen
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 初始化模型
llm = ChatQwen(
    model="qwen3.6-plus",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL")
)


@before_model
def custom_trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    *"""裁剪消息，只保留最后几条消息，保证上下文窗口长度"""*

*    *messages = state["messages"]

    print("目前消息的token长度-->", count_tokens_approximately(messages, chars_per_token=1.8))

    # 官方提供裁剪消息的工具，会根据配置自动裁剪消息
    trimmed_messages = trim_messages(
        messages=messages,  # 待裁剪的消息列表（通常是对话历史）
        max_tokens=200,  # 裁剪后的消息总 Token 数上限，超过此值会丢弃旧消息
        token_counter=lambda msgs: count_tokens_approximately( # Token 计数器，使用 LangChain 内置的近似计数函数
            msgs,
            chars_per_token=1.8,  # 中文更接近 1.8 字符/Token
        ),
        # 其他可选值：
        #   - len: 按消息条数计数（此时 max_tokens 代表条数）
        #   - ChatOpenAI(model="gpt-4o"): 使用模型原生分词器（最精准但较慢）
        #   - 自定义函数: 自己实现的计数逻辑
        strategy="last",  # 裁剪策略：从末尾往前保留最新消息
        #   - "last": 保留最新的 N 个 Token（适合保留最近上下文）
        #   - "first": 保留开头的 N 个 Token（适合保留系统提示和早期指令）
        allow_partial=False,  # 是否允许截断单条消息
        #   - False（默认）: 消息要么完整保留，要么整条丢弃，不会出现"半条消息"
        #   - True: 允许截断消息，max_tokens 落在某条消息中间时会保留部分内容
        #     注意：strategy="last" 时保留后半部分，strategy="first" 时保留前半部分
        start_on="human",  # 强制裁剪后的消息以 HumanMessage 开头
        # 会从后往前找到第一个 HumanMessage，丢弃它之前的所有消息
        # 确保对话历史符合模型要求（通常以 Human 或 System+Human 开头）
        # 可选值: "human", "ai", "system", "tool", 或对应的 Message 类
        end_on=("human", "ai"),  # 强制裁剪后的消息以 HumanMessage/AIMessage 结尾 这里需要注意！
        # 会从前往后找到最后一个 HumanMessage/AIMessage，丢弃它之后的所有消息
        include_system=True,  # 是否保留第一条 SystemMessage（系统提示词）
        # 当 strategy="last" 时生效，会特殊保护位于索引 0 的 SystemMessage 不被裁剪
        # 建议设为 True，因为系统提示词包含给模型的核心指令
    )
    print("裁剪过的消息-->", trimmed_messages)

    return {
        "messages": [
            RemoveMessage(id=REMOVE_ALL_MESSAGES),
            *trimmed_messages
        ]
    }

agent = create_agent(
    model=llm,
    middleware=[custom_trim_messages],
    system_prompt="你是一个智能助手",
    checkpointer=InMemorySaver(),
)

config = {"configurable": {"thread_id": "1"}}

agent.invoke({"messages": "你好，我叫初见"}, config)
agent.invoke({"messages": "请写一首关于月亮的诗句"}, config)
agent.invoke({"messages": "在写一首关于太阳的诗句"}, config)
final_response = agent.invoke({"messages": "我叫什么名字？"}, config)

for res in final_response["messages"]:
    res.pretty_print()
```

#### 删除消息

可以使用`RemoveMessage`从状态中删除消息

```Python
from langchain.messages import RemoveMessage
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import after_model
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.runtime import Runtime
from langchain_core.runnables import RunnableConfig
from langchain_qwq import ChatQwen
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 初始化模型
llm = ChatQwen(
    model="qwen3.6-plus",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL")
)


@after_model  # 装饰器：在模型生成响应之后执行此函数
def delete_old_messages(state: AgentState, runtime: Runtime) -> dict | None:
    *"""*
*    删除旧消息以保持对话上下文在可控范围内。*

*    工作原理：*
*    1. 每次模型响应后，检查消息总数*
*    2. 如果超过阈值（2条），删除最早的消息*
*    3. 使用 RemoveMessage 标记删除，LangGraph 会自动处理*

*    参数：*
*        state: 当前代理状态，包含所有消息历史*
*        runtime: 运行时上下文，提供额外配置信息*

*    返回：*
*        dict | None: 包含要删除的消息列表，或 None（不执行删除）*
*    """*
*    *# 从状态中获取所有消息
    messages = state["messages"]

    # 检查消息数量是否超过限制（保留最近2条）
    if len(messages) > 2:
        print("----------------------开始删除部分消息---------------------------")
        # 获取要删除的消息（最早的2条）
        messages_to_remove = messages[:2]

        # 创建删除标记列表
        # RemoveMessage 是一个特殊对象，告诉 LangGraph 要删除哪些消息
        removal_markers = [RemoveMessage(id=msg.id) for msg in messages_to_remove]

        # 返回字典，LangGraph 会自动处理删除操作
        return {"messages": removal_markers}

    # 如果消息数量未超限，不做任何操作
    return None


# ==================== 创建智能代理 ====================

# 配置代理
agent = create_agent(
    # 使用的语言模型（此处为示例模型名）
    model=llm,
    # 工具列表（示例为空，实际可添加搜索、计算等工具）
    tools=[],
    # 系统提示词：定义代理的基本行为准则
    system_prompt="请保持回答简洁明了，直击要点。",
    # 注册中间件列表
    # delete_old_messages 会在每次模型响应后自动执行
    middleware=[delete_old_messages],
    # 检查点保存器：用于保存和恢复对话状态
    # InMemorySaver 在内存中存储，适合开发和测试
    checkpointer=InMemorySaver(),
)

# ==================== 配置对话会话 ====================

# 配置对象：设置当前对话线程ID
# 相同的 thread_id 可以恢复之前的对话历史
config: RunnableConfig = {
    "configurable": {
        "thread_id": "1"  # 线程ID，用于标识不同的对话会话
    }
}

# ==================== 第一轮对话 ====================

print("=" * 50)
print("第一轮对话：自我介绍")
print("=" * 50)

stream = agent.stream_events(
    # 用户输入消息
    {"messages": [{"role": "user", "content": "你好！我叫初见"}]},
    config,
    version="v3",  # 使用 v3 版本的流式事件协议
)

# 遍历流式响应，打印当前状态快照
for snapshot in stream.values:
    # 提取并显示消息列表（类型 + 内容）
    messages_info = [(msg.type, msg.content) for msg in snapshot["messages"]]
    print(f"当前消息历史 ({len(snapshot['messages'])} 条):")
    for msg_type, content in messages_info:
        print(f"  [{msg_type}]: {content[:50]}...")  # 截断显示
    print("-" * 30)

# ==================== 第二轮对话 ====================

print("\n" + "=" * 50)
print("第二轮对话：请求创作内容")
print("=" * 50)

stream = agent.stream_events(
    {"messages": [{"role": "user", "content": "请写一首关于猫咪的短诗"}]},
    config,
    version="v3",
)

for snapshot in stream.values:
    messages_info = [(msg.type, msg.content) for msg in snapshot["messages"]]
    print(f"当前消息历史 ({len(snapshot['messages'])} 条):")
    for msg_type, content in messages_info:
        print(f"  [{msg_type}]: {content[:50]}...")
    print("-" * 30)

# ==================== 第三轮对话 ====================

print("\n" + "=" * 50)
print("第三轮对话：询问个人信息")
print("=" * 50)

stream = agent.stream_events(
    {"messages": [{"role": "user", "content": "我叫什么名字？"}]},
    config,
    version="v3",
)

for snapshot in stream.values:
    messages_info = [(msg.type, msg.content) for msg in snapshot["messages"]]
    print(f"当前消息历史 ({len(snapshot['messages'])} 条):")
    for msg_type, content in messages_info:
        print(f"  [{msg_type}]: {content[:50]}...")
    print("-" * 30)

```

#### 总结消息

修剪或删除消息的问题在于你可能会因为裁剪消息队列而丢失信息。正因为如此，一些应用程序会采用更复杂的方法，利用聊天模型对消息历史进行总结。

![image\.png](图片和附件/image%2020.png)

请查看摘要中间件中详细内容[Agent智能体](https://my.feishu.cn/docx/ZRKqdGvxQoZc1xxtULKcyjtznDf#Oc3QdeeiVozgvVx0UlacU7CCnOd)

### Streaming流媒体

流式输出是一种让 AI 应用能够“边说边想”的技术。它不再是让用户面对一个加载图标苦等完整的回答，而是像人与人对话一样，在生成过程中就一个词一个词地实时显示内容，极大地提升了交互体验。



**流式输出模式**：

![image\.png](图片和附件/image%2025.png)

```Plain Text
{"messages": [{"role": "user", "content": "长沙天气怎么样?"}]
    [{"role": "tool", "content": "content='长沙的天气是晴朗的!',"}]
    [AIMessage(content='长沙现在的天气是**晴朗的**！]
}
```

```Python
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.config import get_stream_writer  
from dotenv import load_dotenv
import os
# 加载环境变量
load_dotenv()

# 初始化模型
llm = ChatOpenAI(model="qwen3.6-plus", api_key=os.getenv("DASHSCOPE_API_KEY"), base_url=os.getenv("DASHSCOPE_BASE_URL"))

# 创建一个工具
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    # 创建自定义流式输出
    stream_writer = get_stream_writer()
    stream_writer(f"正在获取{city}的天气信息...")
    stream_writer(f"{city}的天气信息获取完成！{city}的天气是晴朗的!")
    return f"{city}的天气是晴朗的!"

agent = create_agent(
    model=llm, 
    tools=[get_weather],
    system_prompt="你是一个乐于助人的助手，能够回答用户关于天气的问题。请使用提供的工具来获取天气信息。",
    checkpointer=InMemorySaver(),  # 使用InMemorySaver来保存对话状态，这样在同一线程中进行的对话可以共享状态
)
config = {"configurable": {"thread_id": str(uuid7())}}

print("====================== 流式输出：updates ======================")
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "长沙天气怎么样?"}]},
    config=config,
    stream_mode="updates",
    version="v2",
):
    if chunk["type"] == "updates":
        for step, data in chunk["data"].items():
            print(f"step: {step}")
            print(f"content: {data['messages'][-1].content_blocks}")
            
            
print("====================== 流式输出：messages ======================")
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "长沙天气怎么样?"}]},
    config=config,
    stream_mode="messages",
    version="v2",
):
    if chunk["type"] == "messages":
        # 在"messages"模式下，流式输出的每个chunk包含一个完整的消息对象和元数据，我们可以直接访问消息内容
        token, metadata = chunk["data"]
        print(f"node: {metadata['langgraph_node']}")
        print(f"content: {token.content_blocks}") # 会输出很多空的内容，代表模型在进行思考，直到最后输出完整的消息内容
        print("\n")
        
        
# print("====================== 流式输出：custom ======================")
# for chunk in agent.stream(
#     {"messages": [{"role": "user", "content": "长沙天气怎么样?"}]},
#     config=config,      
#     stream_mode="custom",
#     version="v2",
# ):
#     if chunk["type"] == "custom":
#         print(chunk["data"])
```

三种模式可以同时使用，只需要指定一个列表：`stream_mode=["messages", "updates", "custom"]`

在何场景下使用：

- `messages`：打字机效果。模型生成一个字，前端就显示一个字。适合展示最终的回复内容。

- `updates`：步骤进度条。每做完一件事（比如“查天气”、“算数学”），就更新一次状态。适合展示“智能体现在在干什么”。

- `custom`：内部日志流。你可以自己决定在任何时候抛点数据出来（比如下载进度50%）。适合展示非常具体的长耗时任务进度。

### Event事件流\(Beta测试版\)

**Event Streaming 是 LangChain v1\.3 对 Streaming 的重构，把原来通过 ****`stream_mode`**** 区分的输出，升级为独立的类型投影（Projection）流。**

**事件流**把 Agent / LLM 执行过程中发生的每一步动作，实时发送出来，而不是等全部执行完再一次性返回结果。

![ChatGPT Image 2026年6月15日 22\_11\_47\.png](图片和附件/ChatGPT%20Image%202026年6月15日%2022_11_47.png)

本质就是对流式输出的一次更新（以下是详细解释）

![image\.png](图片和附件/image%2028.png)

```Python
from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from langchain_core.utils.uuid import uuid7
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 初始化模型   qwen模型对事件流支持不行,不能生成tool_id,故此换成deepseek
llm = ChatDeepSeek(
    model="deepseek-v4-flash",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)


# 创建一个工具
def get_weather(city: str) -> str:
    *"""获取指定城市的天气信息"""*
*    *return f"{city}的天气是晴朗的!"

# 创建代理
agent = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="你是一个乐于助人的助手，能够回答用户关于天气的问题。请使用提供的工具来获取天气信息。",
    checkpointer=InMemorySaver(),  # 使用InMemorySaver来保存对话状态，这样在同一线程中进行的对话可以共享状态
)
# 创建线程id
config = {"configurable": {"thread_id": str(uuid7())}}

# 使用事件流获取代理全部执行过程
stream = agent.stream_events(
    {"messages": [{"role": "user", "content": "长沙天气怎么样？"}]},
    config=config,
    version="v3",
)

# 获取原始的流事件
# print("获取原始的流事件")
# for event in stream:
#     print(event)

# 获取llm返回的每条消息
for message in stream.messages:
    print("获取消息的文本增量和最终文本:")
    for delta in message.text:
        print(delta, end="", flush=True)
    print("获取模型生成工具调用时的内容")
    print(message.tool_calls.get())
    print("获取模型本次输出消息:")
    print(message.output)
    print("获取模型本次推理消息:")
    for delta in message.reasoning:
        print(f"[thinking] {delta}", end="", flush=True)


print()
print("------获取最终状态-------")
print(stream.output)
```

### Structured output结构化输出

**结构化输出**，简单来说，就是让**AI模型**（如GPT、Claude等）不再是“随口说”一段自然语言，而是严格按照你预先定义好的“**表格**”或“**表单**”来生成数据

**为什么要结构化输出？  **

你问：“提取张三的联系方式，邮箱是zhangsan@email\.com，电话13800001111。”

AI回复：“好的，张三的联系方式是邮箱zhangsan@email\.com，电话13800001111。”

问题：这句话你的程序没法直接使用，需要用正则表达式等复杂方法去“猜”和“解析”。

传统自由文本输出存在解析脆弱、正则容易出错、无法自动校验数据完整性等局限。结构化输出能够：

- 保证类型安全：LLM 输出与 Python 类型系统对齐。

- 提升系统可靠性：支持 Schema 验证，若不符合预期可自动修复和重试。

- 增强程序可执行性：输出可直接作为函数参数、路由决策或 Agent 行为指令。

**实际用途：**

1. 信息提取（简历解析、合同字段抽取、具体意图提取等）

2. Agent 参数生成（提取具体参数，调用API或工具）

3. Workflow 状态控制（决定下一步执行节点）

4. 多 Agent 通信（作为 Agent 间的数据协议）

5. 决策与路由（决定执行什么动作）



**LangChain**实现结构化输出，主要通过**两种策略**：

1. 原生策略 \(ProviderStrategy\)：利用OpenAI、Anthropic等模型API自带的JSON模式。模型在“生成层”就保证输出格式正确，最可靠。（优先选择）

2. 工具策略 \(ToolStrategy\)：把输出要求伪装成一个“工具”让模型调用。兼容不支持原生JSON模式的模型，但需要处理可能的格式错误。（当模型不支持结构化输出的时候选择）

```Python
*"""
langchain支持四种方式去支持模型原生结构化输出
1.Pydantic模型  -提供数据校验功能、自动转化等功能
2.Dataclass    -是Python标准库自带的，主要用于简化类的定义
3.Typeddict    -用于约束字典（Dict）的键和值的类型,运行时就是一个普通的字典
4.json Schema  -JSON格式规范

"""
from langchain_qwq import ChatQwen
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 初始化模型
llm = ChatQwen(
    model="deepseek-v4-flash",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL")
)

# 使用qwen模型的结构化输出需要遵守以下内容
"""
在请求体中设置 response_format 参数即可开启结构化输出，需满足以下两个条件：
1.设置response_format参数：将 response_format 参数设置为 {"type": "json_object"}。
2.提示词中包含JSON关键词：System Message 或 User Message 中必须包含"JSON"关键词（不区分大小写），否则API会返回错误：
    'messages' must contain the word 'json' in some form, to use 'response_format' of type 'json_object'.
"""

# ============================================================
# 1. Pydantic模型
# ============================================================
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.agents.structured_output import ProviderStrategy

class UserInfoPydantic(BaseModel):
    """用户信息"""
    name: str = Field(description="用户姓名")
    age: int = Field(description="用户年龄")
    phone: str = Field(description="手机号")

# 创建代理
agent_pydantic = create_agent(
    model=llm,
    system_prompt="你是一个信息提取助手。请始终以JSON格式输出提取的结构化数据。",
    response_format=ProviderStrategy(UserInfoPydantic)
)
message = [HumanMessage(content="我的名字叫张三，今年20岁，手机号：18578656489")]
result_pydantic = agent_pydantic.invoke({"messages": message})
print("1. Pydantic模型结果:")
print(result_pydantic["structured_response"])
print("-" * 50)


# ============================================================
# 2. Dataclass (Python标准库)
# ============================================================
from dataclasses import dataclass, field
from langchain.agents import create_agent
from langchain.messages import HumanMessage

@dataclass
class UserInfoDataclass:
    """用户信息"""
    name: str = field(metadata={"description": "用户姓名"})
    age: int = field(metadata={"description": "用户年龄"})
    phone: str = field(metadata={"description": "手机号"})

# 创建代理
agent_dataclass = create_agent(
    model=llm,
    system_prompt="你是一个信息提取助手。请始终以JSON格式输出提取的结构化数据。",
    response_format=UserInfoDataclass
)
message = [HumanMessage(content="我的名字叫李四，今年25岁，手机号：13800138000")]
result_dataclass = agent_dataclass.invoke({"messages": message})
print("2. Dataclass结果:")
print(result_dataclass["structured_response"])
print("-" * 50)


# ============================================================
# 3. TypedDict (类型约束字典)
# ============================================================
from typing import TypedDict
from langchain.agents import create_agent
from langchain.messages import HumanMessage

class UserInfoTypedDict(TypedDict):
    """用户信息"""
    name: str   # 用户姓名
    age: int    # 用户年龄
    phone: str  # 手机号

# 创建代理
agent_typeddict = create_agent(
    model=llm,
    system_prompt="你是一个信息提取助手。请始终以JSON格式输出提取的结构化数据。",
    response_format=UserInfoTypedDict
)
message = [HumanMessage(content="我的名字叫王五，今年30岁，手机号：13900139000")]
result_typeddict = agent_typeddict.invoke({"messages": message})
print("3. TypedDict结果:")
print(result_typeddict["structured_response"])
print("-" * 50)


# ============================================================
# 4. Json Schema (直接传入JSON Schema字典)
# ============================================================
from langchain.agents import create_agent
from langchain.messages import HumanMessage

# 定义JSON Schema
user_info_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "用户姓名"
        },
        "age": {
            "type": "integer",
            "description": "用户年龄"
        },
        "phone": {
            "type": "string",
            "description": "手机号"
        }
    },
    "required": ["name", "age", "phone"]
}

# 创建代理
agent_json_schema = create_agent(
    model=llm,
    system_prompt="你是一个信息提取助手。请始终以JSON格式输出提取的结构化数据。",
    response_format=user_info_schema
)
message = [HumanMessage(content="我的名字叫赵六，今年28岁，手机号：13700137000")]
result_json_schema = agent_json_schema.invoke({"messages": message})
print("4. Json Schema结果:")
print(result_json_schema["structured_response"])
**print("-" * 50)*
```

```Python
from pydantic import BaseModel, Field
from typing import Literal
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_qwq import ChatQwen
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 初始化模型
llm = ChatQwen(
    model="qwen3.6-plus",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL")
)
# ToolStrategy也支持 pydantic、Dataclass、TypedDict、JSON Schema四种方式，使用方式和模型原生策略一致
# 创建模型类
class ProductReview(BaseModel):
    *"""产品评价分析结果"""*
*    *rating: int | None = Field(description="产品评分", ge=1, le=5)
    sentiment: Literal["positive", "negative"] = Field(description="评价的情感倾向")
    key_points: list[str] = Field(description="评价的关键要点")

# 创建代理
agent = create_agent(
    model=llm,
    response_format=ToolStrategy(ProductReview)
)

# 接触多智能体就用的多了
# 主智能体  -> {"意图识别": "子智能体1"}   结构化的提取作为一个工具或者子智能体进行使用
# 子智能体1 子智能体2 子智能体3

# 下一个工具的输入参数    是上一个工具的输出内容-> {....}

# 执行代理
result = agent.invoke({
    "messages": [{"role": "user", "content": "分析这条产品评价：'很棒的5星产品。发货很快，但是有点贵'"}]
})
print(result["structured_response"])
# 注意，使用ToolStrategy进行结构化输出，messages中最后一条消息会以ToolMessage结尾
"""
ToolMessage(content="Returning structured response: rating=5 sentiment='positive' key_points=['产品很棒', '发货速度快', '价格偏高']", 
    name='ProductReview', id='475c134e-39c7-44d3-a2ee-563b3c05c069', tool_call_id='call_07384fcbdd3b494ca4b7aeff')]
"""
print(result)
```

## Runtime运行时

### 什么是 Runtime（运行时）？

**核心定义**：在 LangChain 1\.0 中，Runtime 是由底层 LangGraph 提供的一个依赖注入（DI）容器和执行环境。
**通俗比喻**：如果把大模型（Model）比作智能体的大脑，各类工具（Tool）是智能体用来做事的手脚，那 Runtime 就是智能体专属的微型工作台操作系统。智能体执行任务全程，所有临时信息、外部资源、会话记忆、流式输出、权限身份都由它统一调度托管，给大脑和手脚提供完整、有序的工作环境。

### 为什么需要Runtime？

![image\.png](图片和附件/image%2019.png)

### Runtime 的核心组件

- **Context（上下文）**：存放静态、不可变的配置信息。例如用户 ID、数据库连接等。它在一次会话中保持不变，为工具提供基础依赖。

- **Store（存储器）**：用于实现长期记忆（BaseStore 实例）。允许智能体跨会话保存和读取固化的数据。

- **State（状态）**：存放交互过程中的可变数据。例如当前的对话历史（messages 列表）、计数器等，类似于前端框架中的 State。

- **Execution Info（运行配置）**：存放可变的标准运行时配置。例如 `thread_id`、运行id、重试次数等。

- **Stream Writer（流写入器）**：用于实现低延迟的流式响应，允许智能体在执行过程中实时向用户推送进度或更新信息。

- **Server info（服务器信息）**: 仅在LangGraph服务器上运行时的服务器特定元数据（助理ID、图ID、已验证用户）



可以在创建`create_agent`代理的时候，指定一个`context_schema`来定义存储在**Runtime**中的**context**内容

```Python
from dataclasses import dataclass

from langchain.tools import tool, ToolRuntime
from langchain_core.messages import ToolMessage
from langgraph.types import Command   # 可以在工具中修改状态
from langgraph.store.memory import InMemoryStore
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent, AgentState
from langchain_qwq import ChatQwen
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 初始化模型
llm = ChatQwen(
    model="deepseek-v4-flash",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL")
)


# 自定义状态
class CustomAgent(AgentState):
    # 用户爱好
    user_hobby: list[str]


# 自定义上下文的属性
@dataclass  #
class Context:   # 名字随便取   UserContext
    user_id: str  # 用户id
    user_name: str  # 用户名称


# 创建工具
@tool
def get_user_name(runtime: ToolRuntime[Context]):  # 在工具中使用runtime，runtime只存在一次任务中
    *"""获取用户姓名"""*
*    *print(runtime.state["messages"])  # 获取对于的状态（短期记忆）
    return runtime.context.user_name  # 工具返回值会自动处理转成ToolMessage


@tool
def set_user_hobby(hobby: list[str], runtime: ToolRuntime[Context]):   # state是存在一次会话中的
    *"""设置用户爱好"""*
*    *print(f"提取的用户爱好：{hobby}")
    # state是短期记忆，要想长期保存需要使用长期记忆   长期记忆会在langgraph详细介绍
    print(f"{runtime.config.get('configurable').get('thread_id')}", runtime.context.user_name)

    # 构造的 Namespace 和存放路径
    namespace = (runtime.context.user_id, "memories")  # 对应：(用户ID, 记忆类别)
    key = "user_profile"  # 记忆条目的 Key
    # 新增长期记忆
    store.put(
        namespace=namespace,
        key=key,
        value={
            "user_name": runtime.context.user_name,
            "hobby": hobby
        }
    )
    # 可以使用command在工具中更新状态，Command会在langgraph详细介绍
    return Command(
        update={  # 更新Agent的state状态
            "user_hobby": hobby,
            "messages": [
                ToolMessage(
                    content=f"已更新用户爱好：{hobby}",
                    tool_call_id=runtime.tool_call_id
                )
            ]
        }
    )


# 创建一个内存的长期记忆
store = InMemoryStore()  # 存储容器-用户的长期记忆
# 创建一个内存的短期记忆（state）
checkpointer = InMemorySaver()

# 创建代理
agent = create_agent(
    model=llm,  # 模型
    tools=[get_user_name, set_user_hobby],
    state_schema=CustomAgent,  # 自定义state
    store=store,  # 长期记忆
    checkpointer=checkpointer,  # 短期记忆
    context_schema=Context,
)

config = {"configurable": {"thread_id": "user_1"}}

# Context上下文只存在一次任务中 ， runtime的生命周期就是Agent执行一次任务
response = agent.invoke(
    {"messages": [{"role": "user", "content": "我的名字叫什么"}]},
    config=config,
    context=Context(user_id="user1", user_name="初见")
)
print(response["messages"][-1].content)
print("------更新用户爱好------")
response = agent.invoke(
    {"messages": [{"role": "user", "content": "我目前的爱好喜欢编程、看电视、看球赛等"}]},
    config=config,
    context=Context(user_id="user1", user_name="初见")
)

print("长期记忆中存储的内容：", store.get(("user1", "memories"), "user_profile"))

"""
梳理流程：
    1. runtime 
        -> Agent在执行任务的时候，可以通过runtime在工具中获取（Context上下文【静态的配置信息】、Store长期记忆、State状态）
    2.自定义Context
        @dataclass  #
        class Context:   # 名字随便取   UserContext
            user_id: str  # 用户id
            user_name: str  # 用户名称
    3.在执行任务开始的时候将Context进行填充
        agent.invoke(
            {"messages": [{"role": "user", "content": "我目前的爱好喜欢编程、看电视、看球赛等"}]},
            config=config,
            context=Context(user_id="user1", user_name="初见")
        )
    4.在工具中通过ToolRuntime进行获取
        @tool
        def get_user_name(runtime: ToolRuntime[Context]):  # 在工具中使用runtime，runtime只存在一次任务中
            '''获取用户姓名'''
            print(runtime.state["messages"])  # 获取对于的状态（短期记忆）
            return runtime.context.user_name  # 工具返回值会自动处理转成ToolMessage
    5.想在工具中修改state，需要在工具函数返回Command对象
       return  Command(
            update={  # 更新Agent的state状态
                "user_hobby": hobby,
                "messages": [
                    ToolMessage(
                        content=f"已更新用户爱好：{hobby}",
                        tool_call_id=runtime.tool_call_id
                    )
                ]
            }
        )
        
长期记忆：存储用户的一些行为习惯、偏好内容、用户画像（用户的购买力）；根据业务需求来。   存储用户喜欢的商品，，后续做商品推荐的时候，Agent会参考存储的长期记忆进行推荐

短期记忆：就是一个会话中的state，只要这个会话一直存在，state就是永久的

Context：就是一次任务所需要的配置信息内容

"""
```

**总结：runtime就代表能在多个工具中可以获取相同的配置内容**

## 中间件系统

![image\.png](图片和附件/image%2016.png)

所以**中间件**提供了一种更严格地控制代理内部运行机制的方法



Harness 工程 \-》给Agent加上规范，保证Agent能够更好的去完成任务

![image\.png](图片和附件/image%205.png)

### 摘要总结中间件

**当用户和智能体对话长度接近上下文上限时，系统会自动压缩上下文：**

- **保留最近的消息**，确保最新信息不丢失；

- **早期的历史消息自动浓缩为摘要**，减少占用空间。

目的：

- 解决长对话超出上下文窗口的问题；

- 保证多轮对话仍能保持完整的上下文。

```Python
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

model = "qwen3.5-flash-2026-02-23"
api_key = os.getenv("DASHSCOPE_API_KEY")
api_base_url = os.getenv("DASHSCOPE_BASE_URL")

llm = ChatOpenAI(
    model=model,
    api_key=api_key,
    base_url=api_base_url,
    temperature=0.1
)
# 2. 配置工具
tools = [TavilySearch(max_results=1)]

"""
 SummarizationMiddleware(
            model=llm,  # 进行摘要的模型
            trigger=("tokens", 4000),  
             # 条件控制要保留多少上下文信息 只能选择一个
                1.fraction- 要保留的模型上下文大小的比例
                2.tokens- 要保留的绝对令牌数量
                3.messages- 要保留的最近消息数量
            keep=("messages", 20),
        ),
"""
SHORT_SUMMARY_PROMPT = """你是一个记忆压缩专家。
请将下方的对话历史压缩成一段简洁的背景摘要，保留以下核心：
1. 用户最终想要解决的问题是什么？
2. 已经执行了哪些关键步骤或得到了哪些结论？
3. 还有哪些待办事项？

请直接输出摘要内容，不要包含任何开场白。

待压缩的对话：
{messages}
"""
agent = create_agent(
    model=llm,
    tools=tools,
    middleware=[
        SummarizationMiddleware(
            model=llm,
            SHORT_SUMMARY_PROMPT=SHORT_SUMMARY_PROMPT,
            trigger=[("tokens", 4000), ("messages", 10)],  # 触发条件
            keep=("messages", 2),  # 摘要后要保留多少上下文信息
        ),
    ],
    checkpointer=InMemorySaver()
)


def run_test():
    print("=== 开始 Agent 自动化测试 ===")
    config = {"configurable": {"thread_id": "1"}}

    # 场景 1：基础问答 + 工具调用（验证 Tavily 搜索是否正常）
    print("\n[测试点 1: 工具调用]")
    query_1 = "2026年3月最新的AI大模型技术趋势是什么？请列出3-4点 简单总结内容"
    print(f"用户: {query_1}")
    response_1 = agent.invoke({"messages": [{"role": "user", "content": query_1}]}, config)
    print(f"Agent 响应: {response_1}")

    # 场景 2：连续对话（验证上下文保留与中间件触发）
    # 我们故意发送一些长文本，模拟达到 4000 tokens 或 3 条消息的触发条件
    print("\n[测试点 2: 多轮对话与摘要中间件验证]")

    test_conversations = [
        "请记住我的名字叫‘浩英’，我是一名AI架构师。",
        "刚才我问的技术趋势中，哪个对医疗行业影响最大？",
        "请基于我们刚才聊到的所有内容，给我写一份200字的行业简报。"
    ]

    for i, user_input in enumerate(test_conversations):
        print(f"\n第 {i + 2} 轮对话输入: {user_input}")
        # 执行对话
        res = agent.invoke({"messages": [{"role": "user", "content": user_input}]}, config)
        print(f"Agent 响应: {res}")

    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    # 可以开启 LangChain 的调试模式查看中间件运行细节
    # import langchain
    # langchain.debug = True

    try:
        run_test()
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
```

### To\-do\-list中间件   任务规划中间件

```Python
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_tavily import TavilySearch
from langchain_openai import ChatOpenAI
from langchain.agents.middleware import TodoListMiddleware
import numexpr
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

model = "MiniMax-M2.1"
api_key = os.getenv("DASHSCOPE_API_KEY")
api_base_url = os.getenv("DASHSCOPE_BASE_URL")
# 初始化qwen模型
llm = ChatOpenAI(
    model=model,
    api_key=api_key,
    base_url=api_base_url,
    temperature=0.1
)

# 创建工具
@tool
def calculator(expression: str):
    *"""*
*    一个数学计算工具*
*    """*
*    *return f"计算结果:{numexpr.evaluate(expression).item()}"


# 定义对应的工具列表
tools = [calculator, TavilySearch(max_results=1)]

# 创建Agent
agent = create_agent(
    model=llm,
    tools=tools,
    middleware=[TodoListMiddleware()],
)

result = agent.invoke(
    {"messages":
        {
            "role": "user",
            "content": "请帮我查询一下目前最新的小米su7的最低价格，在对比尚界z7的最低价格，他们的价格相差多少？"
                       "请使用待办事项"
        }
    }
)
print(result)
print(result["todos"])
```

### `dynamic_prompt` 动态提示词

`@dynamic_prompt` 是 LangChain 1\.0 版本中专门为 Agent（智能体） 设计的一个装饰器。它的核心作用是让你能在 Agent 每次调用大模型之前，根据当时的上下文（比如用户身份、对话状态）实时地、动态地生成系统提示词。

```Python
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain.agents import create_agent
from dataclasses import dataclass
from langchain_qwq import ChatQwen
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 初始化模型
llm = ChatQwen(
    model="qwen3.6-plus",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL")
)

# 定义上下文的属性内容
@dataclass
class Context:
    user_name: str  # 用户名

# 创建动态提示词的函数
@dynamic_prompt
def state_aware_prompt(request: ModelRequest) -> str:
    # 可以在Agent调用模型之前动态的修改系统提示词
    user_name = request.runtime.context.user_name
    print(user_name)

    return f"你是一个智能助手，请称呼用户为：{user_name}"

# 创建代理
agent = create_agent(
    model=llm,
    middleware=[state_aware_prompt],
    context_schema=Context,
)

response = agent.invoke(
    {"messages": [{"role": "user", "content": "你好呀"}]},
    context=Context(user_name="初见")
)
print(response["messages"][-1].content)
```

### 自定义中间件   

![image\.png](图片和附件/image.png)

|before\_agent|每次代理调用之前|
|---|---|
|before\_model|每次模型调用之前|
|after\_model|每次模型调用之后|
|after\_agent|每次调用代理之后|
|wrap\_model\_call|每次模型调用的时候|
|wrap\_tool\_call|每次调用工具的时候|

```Python
from dataclasses import dataclass
from NewAgent.openaiUtils import get_dashscope_llm
from langchain.agents import create_agent, AgentState
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import re
import json
from langgraph.runtime import Runtime
from typing import Callable

# 加载模型
llm = get_dashscope_llm()


# 创建json格式验证
def repair_json_string(raw_str: str) -> str:
    # 1. 去掉 Markdown 的代码块标签
    raw_str = re.sub(r"```json\s*|```", "", raw_str).strip()

    # 2. 修复最常见的：对象或数组末尾多余的逗号
    # 匹配: , 后面跟着 } 或 ]
    raw_str = re.sub(r",\s*([}\]])", r"\1", raw_str)

    # 3. 简单的引号补全（针对属性名漏掉引号的情况）
    # 匹配: {后面或逗号后面 没写引号的 key
    raw_str = re.sub(r"([{,]\s*)([a-zA-Z0-9_]+)(\s*:)", r'\1"\2"\3', raw_str)

    return raw_str


# dataclass会自动创建init、repr、eq方法，frozen能够保证对象初始化之后不能修改
@dataclass(frozen=True)
class Context:
    user_id: int
    user_permissions: str


# 第一种方式，通过装饰器 @before_mode, @after_model，
# 适用于单钩子中间件，没有复杂的配置，快速进行原型设计。
from langchain.agents.middleware import (
    before_agent,
    after_agent,
    before_model,
    after_model,
    wrap_model_call,
    wrap_tool_call,
    ModelRequest,
    ModelResponse,
    AgentMiddleware
)


@before_agent(can_jump_to="end")
def manage_human_message_before_agent(state: AgentState, runtime: Runtime[Context]):
    *"""*
*    在Agent启动之前调用*
*    can_jump_to：可以提前结束中间件*
*        'end': 跳转到代理执行的结尾（或第一个 after_agent 钩子）*
*        'tools': 跳转到工具节点*
*        'model': 跳转到模型节点（或第一个 before_model 钩子）*

*    Runtime:用来传递全局变量（只是用来读取的内容-上下文的常量），还经常用来传递数据库连接池、日志对象一些配置信息*
*    """*

*    *# 从后往前找第一个类别为 HumanMessage 的消息
    user_content = ""
    for message in reversed(state["messages"]):
        if isinstance(message, HumanMessage):
            user_content = message.content
    # 打印用户最新的问题
    print(f"在before_agent中，用户最新问题：{user_content}")
    # 1.处理用户敏感用词
    sensitive_words = ["TM", "TMD", "CNM", "挂了", "垃圾"]
    if any(word in user_content.upper() for word in sensitive_words):
        # 发现敏感词，直接构造一个 AI 响应，不再交给模型思考
        return {
            "messages": [AIMessage(content="检测到不当言论，请文明交流。")],
            "jump_to": "end"  # 直接结束这次对话
        }
    # 2.vip用户特殊处理
    # 获取用户权限
    user_permissions = runtime.context.user_permissions
    if user_permissions == "vip":
        # vip权限能够进行所有知识库的访问
        print("我是VIP用户，能够查看全部的内容")
    else:
        print("我是普通用户，能够查看部分的内容")

    return None


# before_model 中的代码是同步执行的，它会增加每次模型调用前的耗时。因此，应避免在其中执行过于繁重的计算或阻塞操作。
@before_model
def inject_user_context(state: AgentState, runtime: Runtime[Context]):
    user_id = runtime.context.user_id
    # 模拟从数据库获取用户偏好
    user_preference = "用户喜欢幽默的角色"

    # 创建一个新的系统消息，注入用户信息
    context_message = SystemMessage(content=f"用户偏好：{user_preference}。请根据此偏好回答问题。")

    return {
        "messages": [context_message] + state["messages"]
    }


@after_model
def fix_json_structure(state: AgentState, runtime: Runtime[Context]):
    # 1. 获取模型最后一条回复
    last_message = state["messages"][-1]
    if not isinstance(last_message, AIMessage):
        return
    # 这里我们模拟模型返回错误的json
    # raw_content = last_message.content
    raw_content = """
        ```json
        {
          "user_id": "123",
          "action": "send_package",
          "items": ["book", "pen"],
        }
    """
    print(f"开始进行json格式修复:{raw_content}")
    try:
        # 尝试直接解析，如果成功说明不需要修复
        json.loads(raw_content)
    except json.JSONDecodeError:
        # 2. 如果解析失败，执行修复逻辑
        fixed_content = repair_json_string(raw_content)
        print(f"json格式修复完成：{fixed_content}")

        try:
            # 再次验证修复结果
            json.loads(fixed_content)
            # 3. 【关键】写回消息对象
            # last_message.content = fixed_content
            # 也可以记录一个标记位说明发生过修正
            # last_message.additional_kwargs["is_fixed"] = True
        except Exception:
            # 如果修复后还是不行，可以抛出异常触发重试，或记录错误
            pass

    return {"messages": state["messages"]}


@after_agent
def manage_human_message_after_agent(state: AgentState, runtime: Runtime):
    print("我是Agent结束前该做的事情")


@wrap_model_call
def smart_model_wrapper(
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    user_preference = "用户喜欢二次元"
    context_msg = SystemMessage(content=f"用户偏好：{user_preference}。请根据此偏好回答问题。")
    # 通过override去覆盖一个新请求(只是一个临时指令，并不会添加到历史对话中)
    new_request = request.override(
        system_message=context_msg
    )
    
    # 调用真正执行模型的内容
    response = handler(new_request)
    # 模拟 after_model 的逻辑：结构化修正 (可选)
    return response


# 创建智能体
agent = create_agent(model=llm,
                     middleware=[manage_human_message_before_agent,
                                 manage_human_message_after_agent,
                                 inject_user_context,
                                 fix_json_structure,
                                 smart_model_wrapper])
result = agent.invoke({"messages": [HumanMessage("你好，我是初见")]}, context=Context(user_permissions="vip", user_id=1))
# 获取AI回复
# print(result["messages"][-1].content)
print(result)
```

如果想进行精细化的Agent流程拦截，建议使用以下通过类的方式去实现；使用装饰器建议只处理某个单独的钩子

```Python
from typing import Callable, Optional, Dict, Any
from NewAgent.openaiUtils import get_dashscope_llm
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse, hook_config
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.runtime import Runtime
from dataclasses import dataclass
import re

# 加载模型
llm = get_dashscope_llm()

"""
在什么时候使用类去自定义中间件：
1.为同一个钩子定义同步和异步的实现
2.在单个中间件中需要多个钩子
3.需要复杂的配置
4.在初始化时配置，实现项目重用
"""


# 创建json格式验证
def repair_json_string(raw_str: str) -> str:
    # 1. 去掉 Markdown 的代码块标签
    raw_str = re.sub(r"```json\s*|```", "", raw_str).strip()

    # 2. 修复最常见的：对象或数组末尾多余的逗号
    # 匹配: , 后面跟着 } 或 ]
    raw_str = re.sub(r",\s*([}\]])", r"\1", raw_str)

    # 3. 简单的引号补全（针对属性名漏掉引号的情况）
    # 匹配: {后面或逗号后面 没写引号的 key
    raw_str = re.sub(r"([{,]\s*)([a-zA-Z0-9_]+)(\s*:)", r'\1"\2"\3', raw_str)

    return raw_str


# dataclass会自动创建init、repr、eq方法，frozen能够保证对象初始化之后不能修改
@dataclass(frozen=True)
class Context:
    user_id: int
    user_permissions: str


class UnifiedAgentMiddleware(AgentMiddleware):
    def __init__(self, sensitive_words: list = None):
        # 可以在构造函数中传入配置，如敏感词库、数据库连接等
        self.sensitive_words = sensitive_words or ["TM", "TMD", "CNM", "挂了", "垃圾"]

    # --- Agent 级别钩子 ---
    @hook_config(can_jump_to=["end"])
    def before_agent(self, state: AgentState, runtime: Runtime[Context]) -> dict[str, Any] | None:
        *"""在 Agent 逻辑开始前执行（敏感词检查 & 权限验证）"""*
*        *user_content = ""
        for message in reversed(state["messages"]):
            if isinstance(message, HumanMessage):
                user_content = message.content
                break

        print(f"[Before Agent] 检查内容: {user_content}")

        # 1. 敏感词拦截
        if any(word in user_content.upper() for word in self.sensitive_words):
            print(12)
            return {
                "messages": [AIMessage(content="检测到不当言论，请文明交流。")],
                "jump_to": "end"
            }

        # 2. 权限处理
        user_permissions = runtime.context.user_permissions
        status = "VIP" if user_permissions == "vip" else "普通"
        print(f"[Before Agent] {status}用户访问")

        return None

    def after_agent(self, state: AgentState, runtime: Runtime[Context]) -> dict[str, Any] | None:
        *"""在 Agent 逻辑结束后执行"""*
*        *print("[After Agent] Agent 执行完毕，准备返回。")
        return None

    # --- Model 级别钩子 ---
    def before_model(self, state: AgentState, runtime: Runtime[Context]) -> dict[str, Any] | None:
        *"""在调用模型前注入上下文"""*
*        *user_id = runtime.context.user_id
        # 模拟上下文注入
        user_preference = "用户喜欢幽默的角色"
        context_message = SystemMessage(content=f"用户偏好：{user_preference}。")

        return {
            "messages": [context_message] + state["messages"]
        }

    def after_model(self, state: AgentState, runtime: Runtime[Context]) -> dict[str, Any] | None:
        *"""在模型调用后修复数据格式"""*
*        *last_message = state["messages"][-1]
        if not isinstance(last_message, AIMessage):
            return None

        # 模拟格式修复
        raw_content = last_message.content
        # 假设这里触发了修复逻辑（示例中写死一段错误内容演示）
        if "{" in raw_content:
            print(f"[After Model] 尝试修复 JSON...")
            fixed_content = repair_json_string(raw_content)
            # 更新消息内容
            last_message.content = fixed_content

        return {"messages": state["messages"]}

    # --- 包装器钩子 (高级拦截) ---

    def wrap_model_call(
            self,
            request: ModelRequest,
            handler: Callable[[ModelRequest], ModelResponse]
    ) -> ModelResponse:
        *"""深度干预模型请求与响应"""*
*        *print("[Wrap Model] 动态覆盖系统提示词词")
        # 这里的 override 不会改变 state 里的历史记录，仅对本次请求有效
        new_request = request.override(
            system_message=SystemMessage(content="用户偏好：二次元")
        )

        # 执行实际的模型调用
        response = handler(new_request)
        return response



# 1. 实例化中间件对象
my_middleware = UnifiedAgentMiddleware()

# 2. 传入 create_agent
agent = create_agent(
    model=llm,
    middleware=[my_middleware] # 直接传入实例
)

# 3. 调用
result = agent.invoke(
    {"messages": [HumanMessage("你好，我是初见TM")]},
    context=Context(user_permissions="vip", user_id=1)
)

print(result["messages"][-1].content)
```

执行顺序

![image\.png](图片和附件/image%2029.png)



**总结**：为什么中间件是langchain1\.0之后非常重要的内容?

#### 业务逻辑与控制逻辑解耦 \(解耦\)

#### 生产环境的“质量安全网” \(鲁棒性\)

#### 运行时的动态“指挥部” \(动态干预\)

#### AI 应用的 AOP 标准化 \(工程化\)

# Agent 主流设计模式

![image\.png](图片和附件/image%2032.png)

# Multi\-Agent System（MAS多Agent）

## 什么是多Agent系统

\*\*多智能体系统（Multi\-Agent System，简称 MAS）\*\*是由多个具有智能和自主性的个体（即 Agent）组成的系统。这些 Agent 可以是软件程序、机器人、传感器等不同类型的实体，它们各自专注于特定领域的任务，并具备独立感知、决策与执行的能力。

MAS 的核心理念在于：通过各个 Agent 之间的**协作与协调**，共同完成复杂任务，进而实现单个 Agent 难以独立完成的目标。这种系统能够充分发挥分布式智能的优势，在动态环境中高效应对多变的需求与挑战。

## 为什么要使用多代理？

![image\.png](图片和附件/image%2014.png)

## 多Agent框架

## **AutoGen（Microsoft）**

**AutoGen** 是由微软推出的一个多智能体（Multi\-Agent）对话式协作框架，用于构建多个 LLM（大语言模型）之间的**自动协作系统**。  

它的目标是让多个 Agent 以自然语言进行**对话交互**，在自动编程、推理、数据分析等复杂任务中互相配合，实现远超单一 LLM 的效果。

![image\.png](图片和附件/image%203.png)

**左图**：智能体定制

这部分展示了 AutoGen 中 **Agent 的可定制性**：

图中的“Conversable Agent” 是 AutoGen 的核心类，表示一个“可对话智能体”。

每个 Agent 可以被定制为具备不同能力的个体，比如：

- 接入不同 LLM（如 OpenAI GPT）

- 加载用户自定义函数（Python 工具）

- 拥有特定身份（如用户、开发者、分析师）

核心：AutoGen 允许开发者根据实际需要定制每个 Agent 的模型、工具、身份与行为逻辑。

**右上**：多智能体对话

这一块展示了 AutoGen 支持的 **多Agent对话协作能力**：

- 两个不同类型的 Agent（蓝色和绿色）之间进行双向沟通。

- 每个 Agent 内部可以集成不同的模型、执行器、角色设定。

核心：AutoGen 支持多个 Agent 之间自然语言对话，不再局限于“用户 ↔ 单个 LLM”的模式。

**右下**：灵活的对话模式

- Joint Chat（联合对话）

    - 多个 Agent 处于同一层级，平等协作、互相通信。

    - 常见于头脑风暴式、专家平等协作型任务。

- Hierarchical Chat（层级式对话）

    - 存在主控 Agent（例如蓝色），负责协调多个下属 Agent。

    - 下属 Agent 各自专注于某一任务（如执行、生成、总结）

    - 主Agent是用户代理，下级有代码生成、执行、调试、总结等角色。

**创建AutoGen 只需要简单的三步：**

1. **定义智能体（Agent）**
 创建并配置不同角色的智能体，比如用户代理（User Agent）、助手代理（Assistant Agent）、监督代理（Monitor Agent）等。每个智能体都对应一个或多个大语言模型实例，负责特定的任务或角色定位。

2. **设计对话策略与任务流程**
 设定智能体之间的交互规则和对话流程，比如谁先说话、如何传递上下文、什么时候终止对话，以及如何协同完成具体任务。这一步确保多智能体协同有序且高效。

3. **运行多智能体对话（执行协同任务）**
 启动智能体对话循环，自动驱动智能体之间进行多轮交流，最终完成目标任务或输出结果。这个过程由框架负责管理上下文和消息流。

### **案例名称：多智能体驱动的代码流程开发系统**

模拟一个开发团队，自动按照需求从代码编程\-\>代码审查\-\>代码测试的流程，每个模块都由一个智能体负责。

![mermaid\-diagram\-2026\-04\-10\-141905\.png](图片和附件/mermaid-diagram-2026-04-10-141905.png)

#### 下载模块

```Python
pip install pyautogen==0.9.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 配置文件

```Python
import os
from dotenv import load_dotenv

load_dotenv()
# API配置
CONFIG_LIST = [
    {
        "model": "tongyi-xiaomi-analysis-flash",
        "api_key": os.getenv("DASHSCOPE_API_KEY"),  # 请替换为您的API密钥
        "base_url": os.getenv("DASHSCOPE_BASE_URL"),
    }
]

# LLM配置
LLM_CONFIG = {
    "config_list": CONFIG_LIST,
    "temperature": 0.7,
    "timeout": 120,
}

# 智能体配置
AGENT_CONFIG = {
    "user_proxy": {
        "name": "UserProxy",
        "system_message": """您是用户代表，负责：
        1. 接收用户需求并转达给其他智能体
        2. 对任务结果进行确认和反馈
        3. 决定是否需要进一步优化
        【重要】当要求 CodingAssistant 编写代码时，请务必提醒它：
        在代码块的第一行必须包含 # filename: <文件名>.py 的注释。
        这样您在执行代码时，会自动将代码保存为该文件名，而不是临时文件。
        """,
        "human_input_mode": "NEVER",  # NEVER: 全自动模式，不等待人类输入
        "max_consecutive_auto_reply": 5,  # 防止死循环的保险丝，最大连续自动回复次数
        "code_execution_config": {  # 代码执行沙箱
            "work_dir": "coding_output",  # 代码在哪个目录下运行
            "last_n_messages": 5,
            "use_docker": False,  # False=在本地运行，True=在Docker运行(更安全)
        },
    },

    "assistant": {
        "name": "CodingAssistant",
        "system_message": """您是专业的编程助手，负责：
        1. 理解和分析编程任务需求
        2. 编写高质量的代码
        3. 提供详细的代码说明和注释
        4. 确保代码的可执行性和安全性.
        5. 根据需求编写 Python 代码，必须包裹在 ```python ... ``` 中；并且不能自己进行审核和测试。
        6. 【重要】如果收到 CodeReviewer 的 `[修改]` 指令，或者 Tester 的报错信息：
           - 不要只解释原因！
           - 不要只给修改片段！
           - **必须重新输出修复后的、完整的、可运行的代码块**。
        7. 确保代码不依赖用户输入 (input())。
        8. 【禁止】将 CSV 内容、数据预览或文本说明放入 python 代码块中。代码块内只能有纯 Python 代码。
        9. 【核心要求】为了防止脚本在运行后被删除，请在每个代码块的最后添加以下逻辑，将当前代码块的内容保存到本地：
            import inspect
            code = inspect.getsource(inspect.getmodule(inspect.currentframe()))
            with open('final_process_script.py', 'w', encoding='utf-8') as f:
                f.write(code)
        10. 确保代码是自包含的，包含所有 import 语句。

        请始终提供完整、可运行的代码解决方案。
        """,
    },

    "monitor": {
        "name": "CodeReviewer",
        "system_message": """您是代码审查专家，负责：
        1. 检查 CodingAssistant 的代码质量、安全性和逻辑。
        2. 严格执行以下输出协议：
           - 如果代码有 Bug、安全风险或需要优化：请详细列出修改意见，并在最后一行输出标签：**[修改]**
           - 如果代码完美无缺：请在最后一行输出标签：**[通过]**
        3. 不要输出代码，只输出审查意见。

        对每个代码方案都要进行严格审查，并给出明确的通过/修改建议。
        """,
    },

    "tester": {
        "name": "Tester",
        "system_message": """您是测试工程师，负责：
        1. 只有在 CodeReviewer 说 **[通过]** 后，你才开始工作。
        2. 编写独立的测试脚本 (test_script.py) 并运行。
        3. 如果测试失败：请详细描述错误，并要求 CodingAssistant 修复。
        4. 如果测试成功：请输出 "测试通过，任务完成。TERMINATE"。
        """,
    }
}

# 对话配置
CHAT_CONFIG = {
    "max_round": 10,
    "allow_repeat_speaker": False,
    "manager_system_message": """您是多智能体协作的管理者，负责：
    1. 协调各个智能体的对话顺序
    2. 确保任务按既定流程进行
    3. 监控任务完成质量
    4. 在适当时机终止对话
    """
}

# 任务示例配置
SAMPLE_TASKS = {
    "task1": """
    请编写一个完整的 Python 脚本执行以下任务：
    1. 环境自给自足：首先检查当前目录下是否存在 input.csv，若不存在则使用 pandas 创建一个包含 'Name', 'Score', 'Age' 列的模拟数据并保存。
    2. 核心处理：读取该 CSV，计算 Score 列的平均值、最大值和最小值。
    3. 结果保存：将统计结果保存为 output.csv。
    4. 容错输出：所有代码必须写在一个代码块中，包含所有的 import 语句。
    """,

    "task2": """
    创建一个简单的Flask Web应用：
    1. 包含主页和关于页面
    2. 使用Bootstrap美化界面
    3. 实现一个简单的表单提交功能
    4. 包含基本的输入验证
    """,

    "task3": """
    使用matplotlib创建数据可视化脚本：
    1. 生成模拟的销售数据
    2. 创建折线图显示月度趋势
    3. 创建柱状图显示产品类别对比
    4. 保存图表为PNG文件
    """
}

# 终止条件配置
TERMINATION_CONFIG = {
    "keywords": [
        "测试通过", "task completed", "任务完成", "successfully tested",
        "task completed successfully", "任务圆满完成", "all tests passed",
        "代码审查通过且测试完成", "final output ready"
    ]
}
```

#### 核心代码

```Python
import autogen
from config import (
    LLM_CONFIG, AGENT_CONFIG, CHAT_CONFIG, SAMPLE_TASKS,
    TERMINATION_CONFIG
)
import re


# ========================= 第一步：定义智能体（Agent） =========================

def create_agents():
    *"""创建所有智能体"""*

*    *# 1.1 创建用户代理（User Agent）
    user_proxy = autogen.UserProxyAgent(
        name=AGENT_CONFIG["user_proxy"]["name"],
        system_message=AGENT_CONFIG["user_proxy"]["system_message"],
        human_input_mode=AGENT_CONFIG["user_proxy"]["human_input_mode"],
        max_consecutive_auto_reply=AGENT_CONFIG["user_proxy"]["max_consecutive_auto_reply"],
        code_execution_config=AGENT_CONFIG["user_proxy"]["code_execution_config"],
    )

    # 1.2 创建助手代理（Assistant Agent）
    assistant_agent = autogen.AssistantAgent(
        name=AGENT_CONFIG["assistant"]["name"],
        system_message=AGENT_CONFIG["assistant"]["system_message"],
        llm_config=LLM_CONFIG
    )

    # 1.3 创建监督代理（Monitor Agent）
    monitor_agent = autogen.AssistantAgent(
        name=AGENT_CONFIG["monitor"]["name"],
        system_message=AGENT_CONFIG["monitor"]["system_message"],
        llm_config=LLM_CONFIG,
    )

    # 1.4 创建测试代理（Tester Agent）
    tester_agent = autogen.AssistantAgent(
        name=AGENT_CONFIG["tester"]["name"],
        system_message=AGENT_CONFIG["tester"]["system_message"],
        llm_config=LLM_CONFIG,
    )

    return user_proxy, assistant_agent, monitor_agent, tester_agent


# ========================= 第二步：设计对话策略与任务流程 =========================

class MultiAgentWorkflow:
    def __init__(self, user_proxy, assistant_agent, monitor_agent, tester_agent):
        self.user_proxy = user_proxy
        self.assistant_agent = assistant_agent
        self.monitor_agent = monitor_agent
        self.tester_agent = tester_agent

    def create_group_chat(self):
        *"""创建群组对话，定义智能体交互规则"""*

*        *# 定义智能体参与列表
        agents = [
            self.user_proxy,
            self.assistant_agent,
            self.monitor_agent,
            self.tester_agent
        ]

        # 设置对话流程规则
        def custom_speaker_selection(last_speaker, group_chat):
            *"""*
*            优化后的自定义发言人选择逻辑（状态机模式）*
*            """*
*            *# 1. 获取对话历史
            messages = group_chat.messages

            # 初始状态：如果没有消息，由 UserProxy 发起任务
            if not messages:
                return self.user_proxy

            # 2. 获取最后一条消息的文本内容并进行标准化处理
            last_message = messages[-1]
            # 使用 .get() 避免 KeyErrors，转小写并去除空格方便后续匹配
            content = last_message.get("content", "").strip()

            # 3. 基于“最后一位发言人”的身份决定“下一位发言人”

            # --- 场景 A: 用户发话 ---
            if last_speaker == self.user_proxy:
                # 用户通常提出需求，下一步固定交给开发助手
                if len(messages) == 1:
                    return self.assistant_agent
                return self.tester_agent

            # --- 场景 B: 开发助手 (Assistant) 发话 ---
            elif last_speaker == self.assistant_agent:
                # 使用正则或字符串检查是否包含代码块
                # 防止助手只说话不写代码，如果没有代码块则打回重写
                if "```python" in content:
                    return self.monitor_agent
                else:
                    print("系统提示：检测到助手未提供代码块，要求其重新生成。")
                    return self.assistant_agent

            # --- 场景 C: 监督代理 (Monitor) 发话 ---
            elif last_speaker == self.monitor_agent:
                # 使用正则匹配标签，提高容错率（支持空格、大小写等）
                pass_match = re.search(r"\[\s*通过\s*]", content)
                fix_match = re.search(r"\[\s*修改\s*]", content)

                if pass_match:
                    print("审查通过 -> 转交给用户将文件写入本地。")
                    return self.user_proxy
                elif fix_match:
                    print("审查建议修改 -> 打回给开发助手。")
                    return self.assistant_agent
                else:
                    # 兜底逻辑：如果监督员没给出明确结论，通常默认其指出有问题，打回助手
                    print("⚠️ 审查结论模糊，默认打回助手进行确认。")
                    return self.assistant_agent

            # --- 场景 D: 测试代理 (Tester) 发话 ---
            elif last_speaker == self.tester_agent:
                # 在 AutoGen 中，如果需要结束，通常让 Tester 输出 TERMINATE
                # 然后在 GroupChatManager 的 is_termination_msg 中捕获它。
                # 如果流程需要循环回用户（例如请求新任务），则返回 UserProxy。
                if "TERMINATE" in content.upper():
                    return None  # 返回 None 会触发 Manager 检查是否终止

                # 如果测试发现 Bug，其实也可以在这里加逻辑返回给 Assistant
                if "FAILED" in content.upper() or "错误" in content:
                    print("测试失败 -> 打回给开发助手修复。")
                    return self.assistant_agent

                return self.user_proxy

            # 4. 最终兜底：如果逻辑跑出预期，默认交还给用户或助手，防止程序卡死
            return self.assistant_agent

        def is_termination_msg(message: dict):
            *"""*
*            message 是一个字典，包含 'content', 'name' 等字段*
*            """*
*            *content = message.get("content")
            if content is None:
                return False

            # 检查关键字
            content = content.lower()
            return any(keyword.lower() in content for keyword in TERMINATION_CONFIG["keywords"])

        # 创建群组对话
        group_chat = autogen.GroupChat(
            agents=agents,
            messages=[],
            max_round=CHAT_CONFIG["max_round"],  # 最大的发言回合数量
            speaker_selection_method=custom_speaker_selection,  # 自定义发言规则
            allow_repeat_speaker=CHAT_CONFIG["allow_repeat_speaker"],  # 是否运行同一个人连续发言
        )

        # 创建群组对话管理器
        manager = autogen.GroupChatManager(
            groupchat=group_chat,
            llm_config=LLM_CONFIG,
            system_message=CHAT_CONFIG["manager_system_message"],
            is_termination_msg=is_termination_msg
        )

        return manager


# ========================= 第三步：运行多智能体对话（执行协同任务） =========================

def run_multi_agent_task(task_description: str):
    *"""启动多智能体协同任务"""*

*    *print("启动多智能体协同任务...")
    print(f"任务描述: {task_description}")
    print("-" * 50)

    # 创建智能体
    user_proxy, assistant_agent, monitor_agent, tester_agent = create_agents()

    # 创建工作流实例
    workflow = MultiAgentWorkflow(user_proxy, assistant_agent, monitor_agent, tester_agent)

    # 创建群组对话管理器
    manager = workflow.create_group_chat()

    try:
        # 启动对话循环
        result = user_proxy.initiate_chat(
            manager,
            message=f"""
            新任务请求：{task_description}

            请按照以下流程协同完成：
            1. 编程助手：分析需求并编写代码
            2. 代码审查员：审查代码质量和安全性
            3. 测试工程师：编写测试用例并验证功能
            4. 当测试工程师完成之后，请明确给出完成的提示

            请开始执行任务。
            """,
        )

        print("\n" + "=" * 50)
        print("多智能体协同任务执行完成！")
        print("=" * 50)

        return result

    except Exception as e:
        print(f"任务执行过程中出现错误: {str(e)}")
        return None


# ========================= 示例使用 =========================

if __name__ == "__main__":

    # 选择要执行的任务（可以修改这里来测试不同任务）
    selected_task = SAMPLE_TASKS["task1"]  # 可以改为 task2, task3

    print("AutoGen多智能体协同系统启动")
    print("=" * 60)

    # 执行任务
    result = run_multi_agent_task(selected_task)

    if result:
        print(f"\n任务执行摘要:")
        print(f"- 总对话轮数: {len(result.chat_history) if hasattr(result, 'chat_history') else '未知'}")
        print(f"- 任务状态: 已完成")
    else:
        print("\n任务执行失败，请检查配置和网络连接")
```

**重点：比较适合做AI coding工具，底层集成了一个沙箱（可以运行代码），代码自动化、测试自动化。**

## CrewAI

CrewAI 是一个开源的、基于 Python 的多智能体（multi\-agent）协作框架，由 João Moura 创立，旨在让多个角色各异的 AI 智能体协同完成复杂任务。它通过明确的 **Agents（代理）→ Tasks（任务）→ Crews（团队）→ Flows（流程）** 结构，高效构建自动化流程。

![image\.png](图片和附件/image%2026.png)

**核心理念：分工与协作**

人类团队的强大之处在于专业分工：市场分析师负责收集数据，文案撰稿人负责撰写报告，编辑负责审校和润色。

CrewAI 将这个理念应用到了 AI 上。它认为，通过让多个“专家型”AI Agent 协同工作，每个 Agent 只专注于自己擅长的领域，可以比单个“全能型”AI Agent 更高效、更可靠地完成复杂任务。

**核心组件**

- **Agents（代理）\- 团队成员**

每个智能体都有角色、目标和背景故事，可调用工具处理信息、决策和任务执行。

- **Tasks（任务）\- 具体工作**

将复杂目标分解为代理执行的小单元任务，明确每个任务的目标和期望输出。

- **Tool \(工具\)** \- **成员的技能**

这些是 Agent 可以使用的函数或能力，与 LangChain 和 LlamaIndex 中的工具概念一致。CrewAI 可以无缝集成 LangChain 的工具。

- **Crews（团队）\- 团队本身**

聚合多个代理与任务，并支持可选的执行 **Process**（流程），可串行、并行或响应事件驱动，处理复杂任务编排。

- **Flows（流程）\- 工作方式**

用于频繁或高级生产场景，提供精细控制、状态管理、分支逻辑和外部集成能力，特别适合复杂业务逻辑。

### 案例名称：**多智能体驱动的技术情报分析与内容发布系统**

模拟一个技术媒体编辑部，自动完成从情报搜集 → 数据分析 → 文章撰写 → 审校 → 发布的完整流程。每个阶段由独立的智能体负责，使用多个任务进行协作，适合复杂多步骤流程建模。

![mermaid\-diagram\-2026\-04\-10\-142021\.png](图片和附件/mermaid-diagram-2026-04-10-142021.png)

#### 下载模块

```Python
# 创建一个conda环境，**CrewAI**的依赖包很多
conda create -n crewai_env python=3.12
activate crewai_env 

# 下载对应的包
pip install crewai==1.6.1 crewai-tools==1.6.1 tavily-python==0.7.13 dotenv langchain==0.3.26 langchain-openai==0.3.27 langchain-core==0.3.74 langchain-community==0.3.27 langchain-tavily==0.2.10 dashscope==1.25.2


```

```Python
import os
from datetime import datetime
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import TavilySearchTool
from dotenv import load_dotenv

# 加载配置
load_dotenv()


class TechMediaCrew:
    *"""简化版技术媒体编辑部"""*

*    *def __init__(self):
        self.setup_qwen_model()
        self.search_tool = TavilySearchTool(max_results=2)
        self.setup_agents()

    # 配置千问模型
    def setup_qwen_model(self):
        *"""设置千问模型"""*
*        *llm = LLM(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url=os.getenv("DASHSCOPE_BASE_URL"),
            model="MiniMax-M2.1",
            temperature=0.7
        )
        self.llm = llm

    def setup_agents(self):
        *"""设置智能体团队"""*

*        *# 情报员 - 负责搜索和收集信息
        self.researcher = Agent(
            role='技术情报员',
            goal='搜索并收集最新的技术资讯',
            backstory='你是专业的技术记者，擅长找到最新最有价值的科技新闻',
            tools=[self.search_tool],
            llm=self.llm,
            verbose=True,
            max_iter=1
        )

        # 分析师 - 负责分析和总结
        self.analyst = Agent(
            role='数据分析师',
            goal='分析技术趋势，提取关键洞察',
            backstory='你是经验丰富的数据分析师，能从信息中发现重要趋势',
            llm=self.llm,
            verbose=True,
            max_iter=1
        )

        # 作者 - 负责写文章
        self.writer = Agent(
            role='科技作者',
            goal='写出高质量的技术文章',
            backstory='你是资深科技记者，文笔优秀，能把复杂技术写得通俗易懂',
            llm=self.llm,
            verbose=True,
            max_iter=1
        )

        # 编辑 - 负责审校
        self.editor = Agent(
            role='主编',
            goal='审校文章，确保质量',
            backstory='你是严谨的主编，会仔细检查文章质量和准确性',
            llm=self.llm,
            verbose=True,
            max_iter=1
        )

    def create_tasks(self, topic: str):
        *"""创建工作任务"""*

*        *# 任务1: 搜索资料
        research_task = Task(
            description=f'''搜索关于"{topic}"的最新信息，包括：
            重要指令：
            1. 只进行 1 次全面搜索。
            2. 即使搜索结果包含 Unicode 编码（如 \\u4e91），也直接读取，不要因此重新搜索。
            3. 获取到结果后立即停止并输出摘要。''',
            agent=self.researcher,
            expected_output="搜索到的原始信息和资料"
        )

        # 任务2: 分析总结
        analysis_task = Task(
            description=f'''分析搜索到的"{topic}"相关信息，提供：
            1. 关键趋势分析
            2. 重要事件总结
            3. 技术影响评估
            4. 未来发展预测''',
            agent=self.analyst,
            expected_output="详细的分析报告和关键洞察",
            context=[research_task]
        )

        # 任务3: 写文章
        writing_task = Task(
            description=f'''基于分析结果，写一篇关于"{topic}"的文章：
            1. 标题要吸引人
            2. 内容要有逻辑性
            3. 语言要通俗易懂
            4. 长度800-1200字
            5. 包含数据和例子''',
            agent=self.writer,
            expected_output="完整的技术文章",
            context=[research_task, analysis_task]
        )

        # 任务4: 编辑审校
        editing_task = Task(
            description='''审校文章，检查：
            1. 事实准确性
            2. 逻辑清晰度
            3. 语言流畅性
            4. 结构合理性
            5. 标题和内容匹配度
            如有问题请修改完善。''',
            agent=self.editor,
            expected_output="最终审校后的高质量文章",
            context=[writing_task]
        )

        return [research_task, analysis_task, writing_task, editing_task]

    def run_process(self, topic: str):
        *"""运行完整流程"""*
*        *print(f"开始处理主题: {topic}")
        print("-" * 50)

        # 创建任务
        tasks = self.create_tasks(topic)

        # 组建团队
        crew = Crew(
            agents=[self.researcher, self.analyst, self.writer, self.editor],
            tasks=tasks,
            verbose=True,
            process=Process.sequential,
            tracing=True
        )

        # 执行任务
        start_time = datetime.now()
        try:
            # # 让您的团队开始工作！
            result = crew.kickoff()
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            print(f"\n任务完成！用时: {duration:.1f}秒")
            print("-" * 50)
            return result

        except Exception as e:
            print(f"任务失败: {e}")
            return None


def main():
    *"""主函数"""*
*    *import json
    # 创建编辑部
    media_crew = TechMediaCrew()

    # 运行示例
    topics = ["阿里云千问模型发布qwen3", "苹果Vision Pro", "特斯拉自动驾驶"]

    for topic in topics[:1]:  # 只运行一个示例
        print(f"技术媒体编辑部 - {topic}")
        print("=" * 60)
        result = media_crew.run_process(topic)
        if result:
            print(f"\n最终文章:\n{result}")


if __name__ == "__main__":
    main()
```

## langchain构建多智能体

1. SubAgents 子代理

2. Handoffs 移交

3. Skills 技能

4. Router 路由器

5. 自定义工作流（Langgraph）

![image\.png](图片和附件/image%2018.png)

### SubAgents 子代理

![image\.png](图片和附件/image%208.png)

在子代理架构中，一个中央的主代理（通常称为监督者）通过调用工具来协调子代理。主代理决定调用哪个子代理，提供什么输入，以及如何组合结果。子代理是无状态的——它们不记得过去的交互，所有的对话记忆都由主代理维护。这提供了上下文隔离：每次子代理调用都在一个干净的上下文窗口中进行，防止主对话中的上下文膨胀。

#### **关键特征**

- **集中化控制**：所有路由都通过主管代理进行。主管代理完全负责决定何时、调用哪个子代理，并综合最终结果。子代理之间不直接通信。

- **工具化调用**：子代理被封装成主管代理可用的“工具”（Tool）。主管代理通过调用 `task()` 这类工具来启动一个子代理，并给它下达任务指令。

- **无状态设计**：子代理在每次被调用时都是“无状态”的，它不记得过去的交互。唯一的例外是异步子代理，它被设计为有状态的，能在后台长时间运行任务。

- **强上下文隔离**：这是使用子代理最重要的原因。子代理在独立的上下文中运行，其详细的工作过程（如多次工具调用）不会污染主管代理的上下文窗口。主管代理只接收最终结果，有效控制了上下文的膨胀

#### 什么时候使用子代理？

> **核心思想：主 Agent 做决策，子 Agent 做执行。**
> 
> 

1. **当工具数量较多时**
 一个 Agent 无法高效管理所有工具，需要拆分专业能力。 

2. **当 Prompt 变得复杂时**
 将不同任务拆给独立 Agent，降低上下文复杂度。 

3. **当需要多领域协同时**
 不同 Agent 负责不同专业领域（如搜索、代码、写作）。 

4. **当任务需要分步骤执行时**
 将复杂任务拆成多个独立执行单元。 

5. **当需要统一控制执行流程时**
 主 Agent 统一规划和调度，避免多个 Agent 自由竞争。 

6. **当需要隔离上下文时**
 每个 Agent 维护自己的上下文和能力边界。 

**总结： 当一个业务需要多个专业能力协同，但仍希望统一调度时，适合使用子代理。**

```Python
import os
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_qwq import ChatQwen
from langchain_tavily import TavilySearch

# =====================================================
# 初始化模型
# =====================================================
load_dotenv()

model = ChatQwen(
    model="qwen3.6-plus",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL"),
    thinking_budget=16,
)


# =====================================================
# 数学工具
# =====================================================

@tool
def calculator(expression: str) -> str:
    *"""*
*    执行数学计算。*
*    示例：*
*        "(52+18)*2"*
*    返回：*
*        140*
*    """*
*    *import numexpr
    try:
        return str(numexpr.evaluate(expression).item())
    except Exception as e:
        return f"计算失败：{e}"


# =====================================================
# 语文工具 - 搜索
# =====================================================

search_tool = TavilySearch()

# =====================================================
# 数学专家
# =====================================================

math_agent = create_agent(
    model=model,
    tools=[calculator],
    system_prompt="""
你是数学专家。
职责：
    - 数学计算
    - 数值推导
    - 公式计算
要求：
    遇到计算优先调用 calculator。
禁止：
    翻译。
    写作文。
"""
)

# =====================================================
# 英语专家
# =====================================================

english_agent = create_agent(
    model=model,
    tools=[],
    system_prompt="""
你是英语专家。
职责：
    - 中译英
    - 英译中
    - 英文润色
要求：
    保持准确。
禁止：
    做数学计算。
    写文章。
"""
)

# =====================================================
# 语文专家
# =====================================================

chinese_agent = create_agent(
    model=model,
    tools=[search_tool],
    system_prompt="""
你是语文专家。
职责：
    - 写作
    - 扩写
    - 总结
    - 搜集素材
要求：
    如果需要背景知识：
    优先搜索。
禁止：
    修改数学结果。
"""
)


# =====================================================
# Agent 包装成 Tool
# =====================================================

def agent_as_tool(
        name: str,
        title: str,
        description: str,
        agent,
):
    *"""*
*    将 Agent 包装成 Tool*

*    Supervisor：*
*    调用 Tool*

*    实际：*
*    Tool → 调 Agent*
*    """*

*    *@tool(name, description=description)
    def execute(
            request: str,
    ) -> str:
        *"""*
*        调用子智能体。*
*        """*

*        *print(f"\n开始执行：{name}")

        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": request
                    }
                ]
            }
        )

        print(f"完成执行：{name}， 结果：{result["messages"][-1].content}")

        return f"""
        【{title}】已完成任务：
    
        执行结果：{result["messages"][-1].content}
        """

    return execute


math_tool = agent_as_tool(
    name="math_expert",
    title="数学专家",
    description="数学专家智能体，负责数学计算",
    agent=math_agent,
)

english_tool = agent_as_tool(
    name="english_expert",
    title="英语专家",
    description="英语专家智能体，负责翻译",
    agent=english_agent,
)

chinese_tool = agent_as_tool(
    name="chinese_expert",
    title="语文专家",
    description="语文专家智能体，负责写作",
    agent=chinese_agent,
)

# =====================================================
# Supervisor
# =====================================================

supervisor = create_agent(
    model=model,
    tools=[
        math_tool,
        english_tool,
        chinese_tool,
    ],
    system_prompt="""
你是教育领域 Supervisor。
职责：
    分析用户需求。
    决定调用哪个专家。
可调用：
    1.数学专家  math_tool
    2.英语专家  english_tool
    3.语文专家  chinese_tool
禁止：
    自己直接回答问题。
    最终汇总结果。
"""
)

# =====================================================
# 运行
# =====================================================

if __name__ == "__main__":
    user_input = """
            帮我写一个猫咪的故事，字数控制在100字，并把故事翻译成英文
        """

    result = supervisor.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input,
                }
            ]
        }
    )

    print("\n")
    print("=" * 80)
    print(result["messages"][-1].content)
```

### Handoffs 移交

Handoff = Agent 在运行过程中，把控制权切换到另一个状态或另一个 Agent。

![image\.png](图片和附件/image%2027.png)

#### 什么时候使用交接模式？

> **核心思想：当前 Agent 做决策，把控制权移交给另一个 Agent，后续由新 Agent 直接继续对话。**
> 
> 

1. **当职责发生变化时**
 当前 Agent 已不适合继续处理，需要切换到另一个角色。
 例如：客服 → 售后、销售 → 技术支持。

2. **当需要连续多轮对话时**
 交接后，新 Agent 会持续接管用户交流，而不是执行完返回。  

3. **当不同阶段需要不同 Prompt / Tool 时**
 通过切换 `active_agent` 或 `current_step` 改变行为。 

4. **当希望隔离上下文时**
 新 Agent 不继承全部历史，只接收必要上下文，避免污染。 

5. **当需要状态驱动流程时**
 通过状态控制下一步执行者，而不是固定代码流程。 

**总结：**当一个业务存在**角色切换、阶段推进、控制权转移，并且新的 Agent 要继续和用户交流**时，适合使用 Handoff。

```Python
from typing import Callable
from typing_extensions import NotRequired

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

from langchain.agents import AgentState, create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from langchain.messages import HumanMessage, ToolMessage
from langchain.tools import tool, ToolRuntime
import os
from dotenv import load_dotenv
from langchain_qwq import ChatQwen

load_dotenv()

model = ChatQwen(
    model="qwen3.6-plus",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL"),
    thinking_budget=16,
)


# ============================================================================
# 1. State：active_agent 就是"现在该谁接待"的指针
# ============================================================================
class TutorState(AgentState):
    active_agent: NotRequired[str]  # "triage" / "math" / "chinese" / "english"


# ============================================================================
# 2. 转交工具
# ============================================================================

def make_handoff_tool(target: str, description: str):
    @tool(f"transfer_to_{target}", description=description)
    def _handoff(runtime: ToolRuntime[None, TutorState]) -> Command:
        return Command(
            update={
                "messages": [
                    ToolMessage(
                        content=f"已转交给 {target} 专家处理",
                        tool_call_id=runtime.tool_call_id,
                    )
                ],
                "active_agent": target,  # <-- 只是改了"指针"，没有真正跳转到别的节点
            }
        )

    return _handoff


transfer_to_math = make_handoff_tool("math", "当问题是数学题时调用")
transfer_to_chinese = make_handoff_tool("chinese", "当问题是语文题（古诗文/阅读/写作）时调用")
transfer_to_english = make_handoff_tool("english", "当问题是英语题（语法/单词/翻译）时调用")
transfer_to_triage = make_handoff_tool("triage", "当问题不属于你的学科范围时，转回分诊台")

# ============================================================================
# 3. 配置表：每个"角色"对应的人设 + 能用的工具
#    跟官方案例的 STEP_CONFIG 写法 1:1 对应
# ============================================================================
AGENT_CONFIG = {
    "triage": {
        "prompt": "你是学科答疑助手的分诊台。判断学生问题属于数学、语文还是英语，"
                  "调用对应的 transfer_to_xxx 工具转交，不要自己回答问题。",
        "tools": [transfer_to_math, transfer_to_chinese, transfer_to_english],
    },
    "math": {
        "prompt": "你是数学专家，分步骤讲解数学题。"
                  "禁止回答除数学以外的任何问题"
                  "如果学生问题不是数学，调用 transfer_to_triage 转回分诊台，不要勉强回答。",
        "tools": [transfer_to_triage],
    },
    "chinese": {
        "prompt": "你是语文专家，讲解古诗文、阅读理解、写作问题。"
                  "禁止回答除语文以外的任何问题"
                  "如果学生问题不是语文，调用 transfer_to_triage 转回分诊台。",
        "tools": [transfer_to_triage],
    },
    "english": {
        "prompt": "你是英语专家，讲解语法、单词、翻译问题。"
                  "禁止回答除英语以外的任何问题"
                  "如果学生问题不是英语，调用 transfer_to_triage 转回分诊台。",
        "tools": [transfer_to_triage],
    },
}


# ============================================================================
# 4. 中间件：每次调用模型前，读 active_agent，去配置表查对应人设，换装
# ============================================================================
@wrap_model_call
def apply_active_agent(
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    active_agent = request.state.get("active_agent", "triage")  # 默认从分诊台开始
    config = AGENT_CONFIG[active_agent]

    request = request.override(
        system_prompt=config["prompt"],
        tools=config["tools"],
    )
    return handler(request)


# ============================================================================
# 5. 组装 agent —— 只有一个 create_agent
# ============================================================================
all_tools = [transfer_to_math, transfer_to_chinese, transfer_to_english, transfer_to_triage]

agent = create_agent(
    model,
    tools=all_tools,
    state_schema=TutorState,
    middleware=[apply_active_agent],
    checkpointer=InMemorySaver(),
)

# ============================================================================
# 6. 跑一遍流程，观察 active_agent 怎么来回切换
# ============================================================================
if __name__ == "__main__":
    config = {"configurable": {"thread_id": "demo-tutor-mw"}}

    turns = [
        "帮我解一下这道题：x + 5 = 12，x等于多少？",  # triage -> math
        "顺便问下，'明月几时有'的下一句是什么？",  # math 发现不对口 -> 转回triage -> chinese
        "apple的复数形式怎么写？",  # chinese 发现不对口 -> 转回triage -> english
    ]

    for user_input in turns:
        result = agent.invoke({"messages": [HumanMessage(user_input)]}, config)
        last_msg = result["messages"][-1]
        print(f"\n学生: {user_input}")
        print(f"回复: {last_msg.content}")
        print(f"当前 active_agent: {result.get('active_agent')}")
```

![image\.png](图片和附件/image%2012.png)

### **Skills 技能**

参考：[AI Coding提升开发效率](https://my.feishu.cn/docx/Pq6vdj4LNos2ERxUhZVcSpSUnCe#A6Dvdgzv6oLuqHxMOQucRTgpnOk)

![image\.png](图片和附件/image%2024.png)

#### 关键特征

- 以提示为驱动的专业化：技能主要由专业提示定义

- 渐进式披露：技能根据上下文或用户需求逐步开放

- 团队分工：不同团队可以独立开发和维护技能

- 轻量级组合：技能比完整的子代理更简单

- 引用意识：技能可以引用脚本、模板和其他资源

#### 什么时候使用Skills技能？

> **核心思想：当前 Agent 保持决策权，把具体能力封装成 Skill 调用，执行完成后结果返回给当前 Agent。**
> 
> 

1. **当任务是能力执行，而不是角色切换时**

当前 Agent 仍然适合处理问题，只需要借助某项能力。

例如：客服 → 查询订单、旅行助手 → 搜索路线、写作助手 → 检索资料。

2. **当能力需要复用时**

多个 Agent 都可能使用同一种能力。

Research Agent、Writer Agent、Reviewer Agent 共同调用搜索、总结、翻译等能力。

3. **当输入输出边界清晰时**

Skill 更适合固定输入、固定输出的任务。

例如：输入：文档 → 输出：摘要   输入：城市 → 输出：天气信息。不需要独立规划和持续推理。

4. **当希望由 单Agent 统一控制流程时**

    Agent 决定：是否调用 Skill、调用哪个 Skill、如何组合多个 Skill 的结果  （Skill 只负责执行，不参与任务决策。）

总结：Skills 模式的核心是“**同一个 Agent，多套技能**”。Agent 全程陪客户聊，遇到不同场景就在内部**切换对应的技能**模块，所有对话记忆共享，始终保持统一的“人设”和连贯性。

```Python
from langchain_core.utils.uuid import uuid7
from typing import TypedDict
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, ModelResponse, AgentMiddleware
from langchain.messages import SystemMessage
from langgraph.checkpoint.memory import InMemorySaver
from typing import Callable


# 定义技能结构
class Skill(TypedDict):
    *"""支持按需加载的技能定义"""*
*    *name: str  # 技能名称
    description: str  # 技能简介
    content: str  # 技能详细内容


# 定义技能（Schema + 业务规则）
SKILLS: list[Skill] = [
    {
        "name": "sales_analytics",
        "description": "销售数据分析相关数据库结构与业务规则，包括客户、订单、收入统计。",
        "content": """
# 销售分析数据库说明

## 数据表

### customers（客户表）
- customer_id（主键）
- name（客户姓名）
- email（邮箱）
- signup_date（注册日期）
- status（状态：active/inactive）
- customer_tier（客户等级：bronze/silver/gold/platinum）

### orders（订单表）
- order_id（主键）
- customer_id（外键 -> customers）
- order_date（下单时间）
- status（状态：pending/completed/cancelled/refunded）
- total_amount（订单总金额）
- sales_region（销售区域：north/south/east/west）

### order_items（订单明细表）
- item_id（主键）
- order_id（外键 -> orders）
- product_id（商品ID）
- quantity（购买数量）
- unit_price（单价）
- discount_percent（折扣百分比）

---

## 业务规则

【活跃客户】
status='active'
且注册时间早于当前日期 90 天。

【收入统计】
仅统计 status='completed' 的订单，
收入直接使用 orders.total_amount。

【客户生命周期价值（CLV）】
统计客户所有已完成订单金额总和。

【高价值订单】
订单金额 total_amount > 1000。

---

## 示例 SQL

-- 查询最近一个季度收入最高的前10名客户
SELECT
    c.customer_id,
    c.name,
    c.customer_tier,
    SUM(o.total_amount) AS total_revenue
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
WHERE o.status='completed'
AND o.order_date >= CURRENT_DATE - INTERVAL '3 months'
GROUP BY
    c.customer_id,
    c.name,
    c.customer_tier
ORDER BY total_revenue DESC
LIMIT 10;
""",
    },
    {
        "name": "inventory_management",
        "description": "库存管理数据库结构与业务规则，包括商品、仓库和库存分析。",
        "content": """
# 库存管理数据库说明

## 数据表

### products（商品表）
- product_id（主键）
- product_name（商品名称）
- sku（库存编码）
- category（分类）
- unit_cost（成本价）
- reorder_point（补货阈值）
- discontinued（是否停售）

### warehouses（仓库表）
- warehouse_id（主键）
- warehouse_name（仓库名称）
- location（位置）
- capacity（容量）

### inventory（库存表）
- inventory_id（主键）
- product_id（外键 -> products）
- warehouse_id（外键 -> warehouses）
- quantity_on_hand（现有库存）
- last_updated（更新时间）

### stock_movements（库存流水）
- movement_id（主键）
- product_id（外键）
- warehouse_id（外键）
- movement_type（类型：
  inbound 入库 /
  outbound 出库 /
  transfer 调拨 /
  adjustment 调整）
- quantity（数量）
- movement_date（发生时间）
- reference_number（单据号）

---

## 业务规则

【可用库存】
inventory.quantity_on_hand > 0。

【需要补货商品】
所有仓库库存总和
<= 产品 reorder_point。

【有效商品】
默认排除停售商品：
discontinued=false。

【库存估值】
quantity_on_hand × unit_cost。

---

## 示例 SQL

-- 查询库存低于补货线的商品
SELECT
    p.product_id,
    p.product_name,
    p.reorder_point,
    SUM(i.quantity_on_hand) AS total_stock,
    p.unit_cost,
    (
        p.reorder_point
        - SUM(i.quantity_on_hand)
    ) AS units_to_reorder
FROM products p
JOIN inventory i
ON p.product_id=i.product_id
WHERE p.discontinued=false
GROUP BY
    p.product_id,
    p.product_name,
    p.reorder_point,
    p.unit_cost
HAVING
    SUM(i.quantity_on_hand)
    <= p.reorder_point
ORDER BY units_to_reorder DESC;
""",
    },
]


# 创建技能加载工具
@tool
def load_skill(skill_name: str) -> str:
    *"""*
*    加载指定技能的完整内容到上下文。*

*    当需要详细规则、数据库结构、*
*    SQL 编写规范时调用。*

*    参数：*
*        skill_name：技能名称*
*    """*

*    *for skill in SKILLS:
        if skill["name"] == skill_name:
            return (
                f"已加载技能：{skill_name}\n\n"
                f"{skill['content']}"
            )

    available = ", ".join(
        s["name"]
        for s in SKILLS
    )

    return (
        f"未找到技能：{skill_name}\n"
        f"可用技能：{available}"
    )


# 技能中间件
class SkillMiddleware(AgentMiddleware):
    *"""向系统提示中注入技能目录"""*

*    *tools = [load_skill]

    def __init__(self):
        skills_list = []

        for skill in SKILLS:
            skills_list.append(
                f"- {skill['name']}："
                f"{skill['description']}"
            )

        self.skills_prompt = "\n".join(
            skills_list
        )

    def wrap_model_call(
            self,
            request: ModelRequest,
            handler: Callable[
                [ModelRequest],
                ModelResponse
            ],
    ) -> ModelResponse:
        skills_addendum = f"""
        ## 可用技能
        {self.skills_prompt}
        如需完整规则，请调用：
        load_skill
        """
        new_content = (
                list(
                    request.system_message.content_blocks
                )
                + [
                    {
                        "type": "text",
                        "text": skills_addendum
                    }
                ]
        )

        new_system_message = SystemMessage(
            content=new_content
        )

        modified_request = (
            request.override(
                system_message=new_system_message
            )
        )

        return handler(
            modified_request
        )


# 初始化模型
import os
from dotenv import load_dotenv
from langchain_qwq import ChatQwen

load_dotenv()

model = ChatQwen(
    model="qwen3.6-plus",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL"),
    enable_thinking=False,
)

# 创建 Agent
agent = create_agent(
    model=model,
    system_prompt="""
你是一名 SQL 查询助手。

你的职责：
1. 理解用户业务需求
2. 按需加载技能
3. 根据数据库结构生成 SQL
4. 遵循业务规则
""",
    middleware=[
        SkillMiddleware()
    ],
    checkpointer=InMemorySaver(),
)

# 测试运行
if __name__ == "__main__":

    thread_id = str(
        uuid7()
    )

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content":
                        "查询最近一个月订单金额超过1000元的客户"
                }
            ]
        },
        config
    )

    for message in result["messages"]:
        if hasattr(
                message,
                "pretty_print"
        ):
            message.pretty_print()
        else:
            print(
                f"{message.type}: "
                f"{message.content}"
            )
```

### Router 路由器

通过一个独立的“路由层（Router）”分析用户请求，将任务分发给一个或多个专业 Agent，再汇总结果返回给用户。

![image\.png](图片和附件/image%204.png)

#### 关键特征

- 路由器分解查询

- 可能会并行调用零个或多个专业代理

- 结果被合成为连贯的响应

**Router** 不负责完成任务。**Router **的职责只有：

1. 理解请求

2. 判断调用哪些 Agent

3. 汇总结果

#### 什么时候使用 Router（路由器）？

> **核心思想：先判断任务应该交给哪个 Agent，再由对应 Agent 执行并返回结果。**
> 
> 

1. **当任务需要交给不同专业 Agent 时**

不同问题由不同 Agent 处理。

例如：客服 → 订单 Agent、退款 Agent

2. **当不同 Agent 拥有独立能力时**

每个 Agent 有自己的：Prompt、工具、知识领域。Router 负责选择最合适的 Agent

3. **当需要同时调用多个 Agent 时**

多个 Agent 并行执行，最后统一汇总结果。

例如：查询代码 \+ 查询文档 → 合并输出

**总结：Router\-\>先决定谁做，再执行任务。**



**四种模式对比总结**



