---
title: "08-RAG项目实战-summary"
aliases: [端到端 RAG 问答项目实战摘要, RAG Project Practice Summary]
tags: [ai/rag/active]
category: summaries
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/08-RAG项目实战/08-RAG项目实战.md]]"
description: "阐述基于 Vue3 前端与 FastAPI 后端配合 LlamaIndex 构建的本地 RAG 问答系统项目；详解三条核心数据流、后端懒加载单例适配、前端 SSE 半行截断缓存解析、BM25 对 store_nodes_override 的物理依赖以及 numpy 序列化防崩规避手段。"
---

# 08-RAG项目实战 摘要

## 概要说明
本素材是一个端到端本地私有部署 [[RAG]] 问答系统的完整工程实战，即 **[[RAG-Project-Architecture]]**。涵盖 Vue3+Pinia 前端与 FastAPI 后端的交互协作，[[LlamaIndex]] 承担的文档加工、混合召回、[[Reranking|Rerank]] 及多用户隔离聊天存储。重点剖析了工程级三条核心数据流（文档上传、[[MCP-Transport-Modes|SSE]] 流式聊天、JWT 隔离记忆流），并总结了平台冷启动懒加载适配、前端 [[MCP-Transport-Modes|SSE]] 半行数据截断缓存还原解析法、BM25 检索对 docstore 物理存盘的强制依赖，以及 numpy float 类型序列化异常的防崩溃工程处理。

## 核心要点
1. **多用户隔离会话设计（JWT）**：
   - 用户登录 `POST /users/token` 校验账号并生成 JWT。
   - 前端在 HTTP Headers 中带上 `Authorization: Bearer <token>`。
   - 后端拦截器解析出 JWT.sub（用户名）作为会话 `session_id`，利用 `SimpleChatStore` 独立存储各自聊天历史，免除了前端透传 session_id 引起的伪造和串线风险。
2. **前端流式 [[MCP-Transport-Modes|SSE]] 还原缓存读取法**：
   - 前端以 Fetch API 读取 `response.body`。因为网络包片段大小不可控，每次读取常包含“半行”不全 JSON 或多行事件。
   - 前端使用 `buffer` 变量承载接收数据，按换行符 `\n` 切割，将不完整的尾部残留移至下一次循环头部，确保 `JSON.parse` 绝对安全。处理 text（逐词渲染）、sources（展示证据卡片）与 error（错误提示）三路状态。
3. **后端懒加载与单例解耦**：
   - 模型和向量索引初始化极为耗时（需数秒到数十秒）。
   - 后端路由层与核心引擎解耦，使用 `get_rag_service()` 进行单例**懒加载（Lazy Initialization）**。只有在接口被第一次被请求时才同步加载大模型与数据库，防止应用程序在加载路由时就因为卡死而无法启动。
4. **混合检索对 `store_nodes_override` 的底座依赖**：
   - 知识库模式为 Vector 向量（语义）与 BM25（精确字词）融合检索。
   - `BM25Retriever` 无法只通过向量完成匹配，它需要检索节点在本地的原始文本（Docstore）。
   - 在构建 `VectorStoreIndex` 时，必须配置 **`store_nodes_override=True`** 强行将 Nodes 原文写入 `docstore.json`；若漏配或设为 False，BM25 检索器会因为无数据源可查而直接报错瘫痪。
5. **数据防崩转换**：
   - 从 `source_nodes` 获取的相似度评分 `score` 属于 numpy 的浮点类型（如 `numpy.float32`），直接使用 `json.dumps` 序列化为 [[MCP-Transport-Modes|SSE]] 消息时会由于类型无法解析而造成 API 崩溃。
   - 后端转换层必须显式执行 `float(node.score)` 强转为原生 Python 类型，方能保证 [[MCP-Transport-Modes|SSE]] 通道的健壮性。

---
**关联页面**：
- [[RAG-Project-Architecture]] (新建概念)
- [[LlamaIndex]] (关联底层框架)
- [[ChromaDB]] / [[Redis]] (关联持久化数据库与缓存)
- [[Reranking]] / [[Vector-Database]] (关联高级检索机制)
