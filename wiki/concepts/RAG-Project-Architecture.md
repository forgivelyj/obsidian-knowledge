---
title: "RAG-Project-Architecture"
aliases: [RAG项目架构, RAG 端到端设计, RAG Project Architecture]
tags: [ai/rag/active]
category: concepts
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/08-RAG项目实战/08-RAG项目实战.md]]"
description: "RAG项目架构是端到端 RAG 系统开发中的核心工程设计，重点关注多用户 JWT 会话安全隔离、后端懒加载单例模式、前端 SSE 半行截断还原算法与 BM25 对 docstore 的持久化依赖。"
---

# [[RAG]] Project Architecture ([[RAG]] 项目架构)

在将 [[RAG]] 技术转换为实际的产品服务时，开发者面临的不仅仅是算法调优，更多的是高并发安全、网络通信健壮性、以及持久化可靠性等后端工程架构挑战。

一个典型的 [[RAG]] 问答项目架构由 **Vue3 前端**、**FastAPI 后端** 与 **[[LlamaIndex]] 核心引擎** 三层紧密组成。

---

## 1. 核心技术架构设计

```text
    [Vue3 前端] ──( 带有 Authorization: Bearer JWT 报头 )──► [FastAPI 路由]
         │                                                            │
         │ (异步 Fetch 持续读取)                                       │ (用户名隔离 session_id)
         ▼                                                            ▼
  [SSE 缓冲自愈解析] ◄──( StreamingResponse JSON events )─── [RAGService 单例 (懒加载)]
                                                                      │
                                                                      ▼
                                                              [LlamaIndex 核心]
                                                       (VectorIndex + BM25 混合检索)
                                                       (store_nodes_override=True)
```

### ① 用户会话与 JWT 隔离机制
- **问题**：前端向后端发起聊天请求时，如果依赖前端传递自定义的 `session_id`，容易导致越权篡改（访问其他用户的会话）或碰撞泄漏。
- **方案**：后端登录接口 `/users/token` 校验成功后颁发 JWT，用户名被封装在 `sub` 声明中。所有受保护的聊天路由强制通过依赖注入获取当前用户，利用用户名天然作为隔离会话的 `session_id`。
- **好处**：前端免去将会话 ID 保存至本地的琐碎工作，同时保证多用户聊天历史（SimpleChatStore）和内存缓冲（ChatMemoryBuffer）的安全物理隔离。

### ② 前端 [[MCP-Transport-Modes|SSE]] 半行截断缓冲还原算法
- **问题**：流式聊天使用 `text/event-stream` ([[MCP-Transport-Modes|SSE]]) 通道。前端以 Chunk 为单位读取二进制流，由于网络状况不可控，单次 `reader.read()` 极大概率获取到半个 JSON 字符（例如 `{"type":"te`）或多条紧邻事件，直接调用 `JSON.parse` 会报错崩溃。
- **方案**：前端设置字符串缓冲区 `buffer`。
  1. 将每次读取并解码的字符串追加至 `buffer`。
  2. 使用 `split('\n')` 将 buffer 进行切分。
  3. **关键操作**：利用 `lines.pop()` 弹出最后一个元素。若整行完整，此元素为空；若行被截断，此元素则承载半行不完整字符，并保留在 `buffer` 中参与下一次的读取追加。
  4. 遍历已切分出来的完整行进行 `data:` 解析，保障数据处理链路百分之百安全。

### ③ 后端 RAGService 懒加载单例模式
- **问题**：LLM 引擎、本地 [[Embedding]] 词向量与 [[ChromaDB]] 数据库的初始化极为沉重，加载往往耗时数秒至数十秒。若在 FastAPI 应用程序启动（加载模块路由）时就同步初始化这些组件，会导致 Uvicorn 进程由于初始化卡死而频繁超时重启。
- **方案**：在路由与底层引擎间插入适配层 `rag_service.py`。定义全局单例 `_rag_service = None`，并将其封装在依赖注入 `get_rag_service()` 方法中。
- **好处**：实现**懒加载（Lazy Initialization）**。只有当接口被用户第一次请求时，才去同步初始化大模型与索引库，保证应用可以毫秒级顺利冷启动。

---

## 2. 混合检索对持久化存储的物理依赖
在启用“语义向量（Vector） + 关键词（BM25）”的融合检索（QueryFusionRetriever）时，数据持久化设计必须极其小心：
- **向量匹配**：`VectorIndexRetriever` 在 [[ChromaDB]] [[Vector-Database|向量数据库]]中对高维向量执行 ANN 搜索。
- **BM25 检索**：`BM25Retriever` 无法通过[[Vector-Database|向量数据库]]工作，它需要对分片后的原始文本进行分词频匹配，因此**强依赖于节点原文的完整性**。
- **配置规则**：在构建 [[LlamaIndex]] 的 `VectorStoreIndex` 时，必须显式声明 **`store_nodes_override=True`**，强行指示引擎把切分好的 Nodes 全量写入本地文档库（`docstore.json`）。如果漏配，BM25 检索器启动后会因为读不到节点文本而直接报错崩溃。

---

## 3. 工程防崩溃细节：Numpy float32 序列化崩溃
- **现象**：大模型生成完答案后，系统将召回的来源节点 metadata 和得分 `score` 组装为 [[MCP-Transport-Modes|SSE]] data 发送给前端。然而，[[ChromaDB]]/Reranker 返回的 `score` 并不是 Python 原生的浮点数，而是 **`numpy.float32`** 类型。
- **危害**：直接将 numpy 浮点类型传入 `json.dumps()` 序列化为字符串会引发 `TypeError: Object of type float32 is not JSON serializable` 致命异常，导致流传输在末尾闪退。
- **解决**：在将 `source_nodes` 扁平化为 JSON 字典时，必须显式调用原生强转：`'score': float(node.score)`。

---
**关联页面**：
- [[RAG]] (大背景技术)
- [[LlamaIndex]] (关联底层调用框架)
- [[Reranking]] / [[Vector-Database]] (关联高级检索)
