---
title: "Neo4j"
aliases: [neo4j, Cypher, CQL]
tags: [database/tool/active]
category: entities
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/05-KNOWLEDGE GRAPH FOR RAG/05-KNOWLEDGE GRAPH FOR RAG.md]]"
description: "Neo4j 是一款开源、高性能的 NoSQL 图数据库，完全基于属性图模型（LPG）设计，是企业级知识图谱构建与 GraphRAG 最核心的底层存储系统。"
---

# Neo4j 图数据库

Neo4j 是目前全球应用最广泛的原生图数据库。它将数据在物理存储层以网状节点和边的形式落盘，具备极佳的图遍历与多跳关联查询性能。

---

## 1. 安装与插件配置
- **版本配套**：Neo4j 5.x 版本需要 Java 17 (JDK 17) 环境支撑。
- **APOC 插件扩展**：在开发大模型 [[GraphRAG]] 时，系统需要使用 APOC（Awesome Procedures on Cypher）的高级图过程。
  1. 需要将对应版本的 `apoc-5.x-core.jar` 和 `apoc-5.x-extended.jar` 复制并放入 Neo4j 的 `plugins` 文件夹下。
  2. 修改 `conf/neo4j.conf` 文件以放行安全策略：
     ```properties
     dbms.security.procedures.unrestricted=apoc.*
     dbms.security.procedures.allowlist=apoc.*
     ```
  3. 重启 Neo4j 服务使插件生效。

---

## 2. Cypher 查询语言 (CQL) 常用语法

Cypher 是 Neo4j 的声明式图形查询语言，使用圆括号 `()` 表示节点，使用带有箭头的方括号 `-->` 或 `-[]->` 表示关系。

### ① 增（CREATE / MERGE）
- **CREATE**：直接无条件新建节点或关系。
  ```cypher
  // 新建带属性和标签的节点
  CREATE (n:Person {name: "孙悟空", age: 500})
  // 新建节点的同时建立关系
  CREATE (悟空:Person {name: "孙悟空"})-[:师从 {since: "明朝"}]->(祖师:Person {name: "菩提祖师"})
  ```
- **MERGE**：幂等创建。如果库里已有，则复用；没有，则新建。能彻底避免节点冗余。
  ```cypher
  MATCH (悟空:Person {name: "孙悟空"})
  MERGE (牛魔:Person {name: "牛魔王"})
  MERGE (悟空)-[:朋友]->(牛魔)
  ```

### ② 查（MATCH / RETURN）
- **MATCH**：模式匹配。
  ```cypher
  // 查找并返回所有 Person 节点
  MATCH (p:Person) RETURN p.name, p.age
  // 查找带有“师从”关系的两端实体姓名
  MATCH (徒弟:Person)-[:师从]->(师父:Person) RETURN 徒弟.name, 师父.name
  // 复杂的 WHERE 过滤
  MATCH (p:Person) WHERE p.age > 100 AND p.name STARTS WITH "孙" RETURN p
  ```

### ③ 改（SET / REMOVE）
- **SET**：添加/更新属性、添加 Label。
  ```cypher
  MATCH (p:Person {name: "孙悟空"}) SET p.weapon = "金箍棒", p:猴王
  ```
- **REMOVE**：移除特定属性、删除 Label。
  ```cypher
  MATCH (p:Person {name: "猪八戒"}) REMOVE p.old_name
  ```

### ④ 删（DELETE / DETACH DELETE）
- **DELETE**：删除节点或边（若节点带有未切断的关系，直接 DELETE 会报错）。
  ```cypher
  MATCH (a:Person {name: "孙悟空"})-[r:朋友]->(b) DELETE r
  ```
- **DETACH DELETE**：安全切断所有关联边，并删除该节点。
  ```cypher
  MATCH (p:Person {name: "牛魔王"}) DETACH DELETE p
  ```
- **清空全库**：`MATCH (n) DETACH DELETE n`

---
**关联页面**：
- [[Property-Graph]] (底座图模型)
- [[GraphRAG]] (工程应用场景)
