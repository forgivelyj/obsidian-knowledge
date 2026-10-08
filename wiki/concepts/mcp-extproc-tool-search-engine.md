---
title: "mcp-extproc-tool-search-engine"
aliases: [MCP工具检索优化, ExtProc工具折叠与能力池检索, AgentGateway高可用治理]
tags: [ai, software-engineering, pattern, tool, active]
category: concepts
created: 2026-09-04
updated: 2026-09-04
sources:
  - "[[raw/20-Tech/mcp-gateway-architecture.md]]"
description: "记录企业级 MCP Gateway ExtProc 工具检索中的反模式（盲目兜底、硬编码截断、TTL误杀）及基于能力池与意图加权的健壮设计方案。"
---

# MCP ExtProc 工具检索与网关稳定性架构经验

## 1. 负向经验与踩坑记录 (Negative Evidence & Anti-Patterns)

### (1) 检索引擎中的“伪兜底回退” (Blind Fallback Anti-Pattern)
* **现象**：当用户输入业务词（如“会议室”）在分词未直接命中英文名称导致得分为 0 时，检索逻辑盲目回退并返回 `online_tools[:top_k]`。
* **危害**：工具注册表中排在最前的通常是基础服务（如 `mcp-common` 的“人员/时间/团队”），导致大模型误以为系统只有这三个无关工具，产生极大的幻觉和调用困惑。
* **定则**：**无匹配即返回 `NOT_FOUND`**，并输出结构化的当前活跃能力池清单与检索指引，绝不猜测或盲目兜底无关工具。

### (2) 基于 `tools/list` 心跳的粗暴 TTL 误杀
* **现象**：在服务端启动 180s 倒计时协程，只要 180s 内未再次收到客户端的 `tools/list`，就将工具置为 `OFFLINE`。
* **危害**：主流 MCP 客户端及 AI Agent 通常仅在建立连接握手阶段调用一次 `tools/list`，后续均直接调用 `tools/call`。因此在 3 分钟后，所有存活微服务的工具在网关内存中均被误杀离线。
* **定则**：**工具生命周期必须与底座服务发现（K8s Service Watcher）强绑定**。微服务在集群中存在且健康，其工具便永久保持 `ONLINE`；仅在收到微服务下线事件时才同步清理。

### (3) 稳定排序与硬编码小阈值导致查询工具永久截断
* **现象**：`top_k` 硬编码为 3，且在打分相同时按插入顺序排序。微服务上报工具列表中增删改工具（`add_*`、`update_*`、`cancel_*`）排在前面，查询工具（`list_meeting_room_usage`）排在第 8。
* **危害**：查询类工具永远被挤出前 3 名，调用方必须知晓内部精确短名才能找到工具。
* **定则**：
  1. 引入**意图识别与提权**：当识别到“查”、“看”、“占用”、“空闲”等查询意图时，查询类工具自动获得大权重提权（+40 分）；
  2. 支持**能力池全量检索**：支持直接传入能力池名称（如“华讯会议室预订系统”）返回该池全量工具；
  3. 扩大默认阈值至 10，并支持分页。

### (4) 元工具 Schema 属性遗漏导致严格校验客户端拒绝 (Strict Schema Validation Trap)
* **现象**：后端 ExtProc 实现了 `page`、`limit`、`pool`、`format` 等分页与格式参数，但元工具 `get_tool` 声明的 JSON Schema 中仅列举了 `name` 和 `query`，且客户端（如 OpenAI Strict Mode、AJV、Pydantic）默认启用了 `additionalProperties: false`。
* **危害**：严格校验的客户端在发起带 `page` 翻页参数的请求时，直接触发入参格式校验拦截（报错“Additional properties are not allowed ('page' was unexpected)”），大模型也因感知不到 `page` 字段而无法自主发起翻页调用。
* **定则**：**元工具 inputSchema 必须与后端支持参数严格对称**。将 `page` (integer, default=1, min=1)、`limit` (integer, default=10, min=1, max=30)、`pool` (string)、`format` (string, enum=['array', 'object'])、`tool_name` (string) 完整声明，并显式配置 `required: []` 和 `additionalProperties: false`，确保各类严格校验客户端均可无缝通过。

---

## 2. 验证方案与最佳实践 (Validated Architecture)

1. **能力池 (Capability Pool) 映射**：
   维护全局四大核心服务池与领域同义词倒排索引（`meeting`、`location`、`schedule`、`common`），识别用户全局域意图。
2. **跨域工具关联**：
   在会议室场景中，查询占用和预订会议室强依赖位置服务的 `search_office`（获取 `office_id`），检索会议室时应将 `search_office` 作为关联工具协同展示。
3. **网关基础设施高可用防线**：
   `agentgateway` 和 `ratelimit` 等控制面组件不得部署在资源严重超售且反复出现 `NodeNotReady` 的物理节点上，需通过 `nodeSelector`、`nodeAffinity` 与双副本规避节点级网络抖动。
