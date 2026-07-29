---
title: "LangGraph-Long-Term-Memory"
aliases: [InMemoryStore, RedisStore, PostgresStore, 长期记忆, 语义检索]
tags: [ai/framework/active]
category: concepts
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/LangGraph框架/LangGraph框架.md]]"
description: "LangGraph-Long-Term-Memory 介绍基于 Store 接口的跨会话长期记忆存储体系，剖析语义向量搜索、命名空间隔离及在多会话中的调用。"
---

# [[LangGraph]] 长期记忆与语义检索 (Store)

在 **[[LangGraph]]** 中，基于 Checkpointer 的短期记忆仅局限在某一个具体的 `thread_id` 对话线索内。为了能够让[[AI-Agent|智能体]]跨会话、跨线程共享和记住用户的持久化数据（如用户的语言偏好、购买偏好、职业画像），[[LangGraph]] 设计了独立的 **`Store`** 长期记忆存储接口。

---

## 1. 长期记忆 Store 的基本架构与存储机制
Store 接口（例如 `InMemoryStore` 内存存储、`RedisStore` 或 `PostgresStore` 关系型存储）充当了独立于对话图谱执行链的**键值数据库**。

```text
  [ 会话线程 1 (thread_id: 001) ]  ───┐
                                      │
  [ 会话线程 2 (thread_id: 002) ]  ───┼─► [ 长期记忆 Store ]
                                      │  (通过命名空间隔离不同用户数据)
  [ 会话线程 3 (thread_id: 003) ]  ───┘
```

### ① 命名空间隔离
Store 中的记忆是以命名空间（Namespace）进行逻辑隔离的。命名空间是一个字符串元组，通常设计为 `("memories", user_id)`，用于确保[[AI-Agent|智能体]]只能读写当前交互用户的特定记忆。
- **存储数据**：
  ```python
  # 存储一个记忆条目，返回唯一键
  store.put(
      namespace=("memories", "user_123"),
      key="food_preference",
      value={"text": "我最喜欢吃红烧肉和臭豆腐"}
  )
  ```
- **读取数据**：
  在节点或工具内部，可以通过 `runtime: ToolRuntime` 依赖注入直接从 Store 中读取：
  ```python
  record = runtime.store.get(namespace=("memories", user_id), key="food_preference")
  ```

---

## 2. 具备语义检索能力的 Store 增强
如果仅仅通过固定 key 读取，[[AI-Agent|智能体]]很难在复杂的对话中模糊匹配长期信息。为此，[[LangGraph]] 支持向 Store 注入[[Embedding|嵌入]]模型（[[Embedding]]）以开启**语义相似度搜索（Semantic Search）**：

### ① 开启向量索引配置
```python
from langchain_huggingface import HuggingFaceEmbeddings
from langgraph.store.memory import InMemoryStore

# 初始化向量 Store，指定嵌入模型与输出维度
store = InMemoryStore(
    index={
        "embed": HuggingFaceEmbeddings(model_name="path_to_embedding_model"),
        "dims": 1024
    }
)
```

### ② 模糊语义查询
当大模型收到用户模糊的问题（如“我肚子饿了，有什么好吃的推荐吗？”），调用 chat 节点：
1. 节点提取用户的输入作为 `query` 传给 `store.search`；
2. 引擎自动计算 query 向量，在命名空间 `("memories", user_id)` 内查找最相关的记忆片段；
3. 将搜索出的最相关的 2 条记录（例如“用户喜欢吃红烧肉”）作为上下文系统消息拼接回 Prompt 输入，使得大模型能够给出极具个性化的回答：“已知您平时最喜欢吃红烧肉，今天推荐您尝尝这家的特色招牌...”。
   ```python
   items = store.search(
       namespace=("memories", user_id),
       query=state["messages"][-1].content, # 用用户问题进行向量匹配
       limit=2
   )
   ```

---
**关联页面**
- [[LangGraph]] (框架实体)
- [[LangGraph-Persistence]] (相对应的短期记忆机制)
- [[LangChain-Agent-Runtime]] ([[LangChain-Agent-Runtime|ToolRuntime]] 运行期接口)
- [[Redis]] / [[ChromaDB]] (底层的物理向量或高速键值底座)
