---
title: "Agentgateway-ExtProc-Dynamic-Schema"
aliases: [Agentgateway ExtProc 动态自适应与身份透传引擎, ExtProc-Dynamic-Schema]
tags: [ai, software-engineering, pattern, active]
category: concepts
created: 2026-09-04
updated: 2026-09-04
sources: 
  - "[[output/reports/extproc-enhancement-requirements-specification.md]]"
description: "基于 Envoy ExtProc 与 K8s 原生服务发现的双向拦截增强机制，实现用户身份动态解密注入、Session 跨会话精准限流、get_tool 自适应 Prompt 聚合与旧服务实时清理"
---

# Agentgateway ExtProc 动态自适应与身份透传引擎

## 1. 核心架构与设计背景

在企业级 AI 网关（Agentgateway / Envoy）环境下，MCP 客户端（如 Cursor、自研 Agent）与后端微服务交互面临三大核心矛盾：
1. **身份伪造与限流粒度失真**：客户端在 `established-session` 工具调用阶段仅携带 `mcp-session-id`，缺失明文身份；若客户端自行声明 `x-authenticated-user` 极易仿冒管理员。
2. **静态 Schema 描述与实际在线服务脱节**：硬编码 `get_tool` 描述无法随微服务上下线自适应更新，导致大模型意图落空或缺少引导。
3. **已下线旧服务 503 脏调用**：开发人员删除 Service 或剔除标签后，传统缓存不感知，造成大模型依然调用已下线服务。

为此，通过 Envoy External Processing (`ExtProc`) gRPC 插件与 Kubernetes 原生 Informer/Watch 构建自适应增强引擎。

```text
AI Agent ➔ Agentgateway (Envoy) ➔ ExtProc Plugin (server.py) ➔ Backend Microservices
                                         │
                                         ▼
                            K8s API Service Watcher
```

---

## 2. 三大核心机制

### 2.1 用户身份安全透传与多租户精准限流 (Security & Rate Limit)
* **初次握手身份捕获**：在初次握手请求中，插件从 `Authorization: Bearer <token>` 提取 JWT Payload 中的 `username`（或 `sub`），存入 `SessionUserManager`（带 TTL 与 LRU 淘汰）。
* **安全防仿冒清洗 (Sanitization)**：在 `request_headers` 拦截阶段，强制加入 `remove_headers = ["x-authenticated-user", "content-length"]`，彻底剥离客户端自带的身份头与失效的 Content-Length。
* **受信身份动态注入**：在后续请求中依据 `mcp-session-id` 获取受信任的真实用户名，动态返回 `HeaderMutation.set_headers(x-authenticated-user: <username>)`，供下游 Envoy RLS 依照 `mcp-service-domain_user_id_<username>_<ts>` 统一累计限流。

### 2.2 `get_tool` 描述基于 Schema 动态自适应聚合 (Adaptive Schema Prompt)
* **能力大纲动态渲染**：维护 `active_service_capabilities` 注册表，优先读取 Service Annotations（`agentgateway.dev/display-name`、`agentgateway.dev/capabilities`），兜底自动分析工具名与 description。
* **双层结构 Prompt**：
  1. **固定引导层**：华讯网络内部系统核心引导指令与 CoT 三步调用规范（通用化触发描述：“当用户需要查询企业内部信息、办理各类业务或执行相关系统操作时，必须调用本工具查找对应tool”）；
  2. **动态能力池**：列举当前集群实际在线的微服务大纲（如日程、会议室预订、OA、ERP等），服务上线即自动增加，下线即自动抹去。
* **严格全局防重**：规范主键注册（仅按 `namespace/service_name` 作为 Key，废除别名循环），Prompt 生成阶段维护 `seen_service_names` 与 `seen_display_names` 双集合，保障同名或跨空间微服务绝不重复输出。
* **动态参数提示**：`inputSchema.properties.name.description` 动态插入当前所有在线工具与业务的关键词列表。

### 2.3 K8s 动态感知与下线实时清理 (Lifecycle & Eviction)
* **K8s Informer / Watch**：利用 Pod 的 ServiceAccount 凭据（或本地 Kubeconfig），长轮询监听带有 `agentgateway.dev/mcp-server: enabled` 的 Service 事件。
* **毫秒级物理剔除**：捕获 `DELETED` 或标签剥离事件后，立即从 `active_service_capabilities` 与 `TOOL_CATALOG` 中物理删除关联工具，并重新渲染 `get_tool` 描述。
* **拦截 503 脏调用**：大模型调用已下线工具时，ExtProc 插件就地拦截并返回友好错误提示，绝不向后端转发引发 503 Service Unavailable。

---

## 3. 验证与负证据备忘 (Negative Evidence)

1. **ServiceAccount RBAC 权限陷阱**：
   - *问题*：默认情况下，`agentgateway-system` 命名空间下的 `default` ServiceAccount 无法跨命名空间 `list/watch` Services，会导致 K8s API 返回 `403 Forbidden`。
   - *方案*：必须配套应用 `ClusterRole` 与 `ClusterRoleBinding`（`mcp-tool-search-plugin-role`），授予对 `services` 的 `get, list, watch` 权限。
2. **微服务能力重复渲染陷阱**：
   - *问题*：若在事件监听中将 `svc_key` 与短名 `svc_name` 同时写入能力字典作为别名，会导致 Prompt 生成循环遍历出重复的微服务条目。
   - *方案*：主键仅保留唯一规范的 `svc_key`，并在 Prompt 生成器中对展示名与服务名进行 Set 过滤去重。
3. **PowerShell 管道 ASCII 转码陷阱**：
   - *问题*：Windows PowerShell 5.1 在执行 `cmd1 -o yaml | kubectl apply -f -` 时，管道传输默认将非 ASCII 字符转换为 `?` 字节（0x3F），导致 ConfigMap 中中文全面乱码。
   - *方案*：避免跨进程管道流式 apply 中文 YAML，改用 UTF-8 文件或 Python 原生写入。
4. **Content-Length 挂起陷阱**：
   - *问题*：ExtProc 篡改请求体或响应体后，若未显式剥离或重算 `Content-Length`，会导致 HTTP/1.1 与 Envoy 挂起等待剩余字节。
   - *方案*：请求头与响应体阶段必须严格剥离原始 `content-length`。
5. **Windows 控制台字符集编码**：
   - *问题*：在 Windows PowerShell 默认 GBK 终端下输出 Unicode 表情符（如 `\u2705`）会导致 `UnicodeEncodeError`。
   - *方案*：测试套件与控制台应配置 `sys.stdout.reconfigure(encoding="utf-8")` 或使用纯 ASCII 标识（`[PASS]`）。
