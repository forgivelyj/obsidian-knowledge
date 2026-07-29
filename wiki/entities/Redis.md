---
title: "Redis"
aliases: [Redis 缓存, Remote Dictionary Server]
tags: [database/tool/active]
category: entities
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/01-RAG基础/01-RAG基础.md]]"
description: "Redis 是一款开源的高性能内存 Key-Value 数据库，以超高并发和极低延迟著称，在 RAG 系统中常用来作缓存、状态存储或基本关键字模糊搜索。"
---

# Redis

Redis（Remote Dictionary Server，远程字典服务）是一款将所有数据托管在系统内存中的极速键值型（Key-Value）数据库。

## 在 [[RAG]]/AI 应用中的地位
虽然 Redis 是传统的数据库，但由于其无可比拟的读写速度（每秒处理 10w+ 读写），在当前的 AI 工程架构中，它常被用作：
1. **[[RAG]] 缓存（Cache）**：保存常见的 Query 及其生成的回答，命中缓存直接返回，省去调用大模型与向量库的延迟与费用。
2. **对话历史管理（Session Memory）**：保存 Agent 与人类聊天的多轮历史记录，利用其 TTL（过期自动删除）机制管理会话生命周期。
3. **传统文档检索（Keyword Match）**：利用 Redis 的 `keys *key*` 模式进行低成本的键模糊匹配查询。

## Redis 核心数据结构与操作
- **String (字符串)**：存储简单文本。如 `set key value`，`get key`。
- **Hash (哈希表)**：存储对象及其属性。如 `hset user name tuling age 10`。
- **List (双向列表)**：存储有序日志流或消息队列。如 `lpush mylist a b c`。
- **Set (无序去重集合)**：`sadd myset member1 member2`。
- **ZSet (有序集合)**：每个元素带有一个 double 类型的权重 score，自动按 score 从小到大排序。如 `zadd rankings 100 member1`。

## Python 简易检索代码演示
```python
import redis

# 建立连接
r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

# 写入文档数据
r.set("得了白癜风该如何注意饮食？", "得了白癜风应该注意避免辛辣刺激性食物...")

# 基于 Keys 的模糊匹配搜索（简易关键字 RAG）
matched_keys = r.keys(pattern='*白癜风*')
for key in matched_keys:
    print(f"匹配问题: {key} | 答案: {r.get(key)}")
```

---
**关联页面**：
- [[RAG]] (工程应用)
