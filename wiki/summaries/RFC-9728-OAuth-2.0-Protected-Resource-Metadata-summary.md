---
title: "RFC-9728-OAuth-2.0-Protected-Resource-Metadata-summary"
aliases: [RFC 9728 摘要, 受保护资源元数据摘要]
tags: [security/oauth2/active]
category: summaries
created: 2026-08-05
updated: 2026-08-05
sources: 
  - "[[raw/00-Inbox/RFC 9728 OAuth 2.0 Protected Resource Metadata.md]]"
description: "RFC 9728 规定了 OAuth 2.0 受保护资源元数据发现协议（/.well-known/oauth-protected-resource），允许客户端自动发现资源服务器所信任的授权服务器及作用域。"
---

# [[Protected-Resource-Metadata|RFC 9728]]: OAuth 2.0 Protected Resource Metadata 摘要

## 概要说明
RFC 9728 填补了 [[OAuth-2.0]] 生态中关于**资源服务器 (Protected Resource / RS)** 元数据发现的标准空白。它允许客户端直接从 RS 获取其所配置和信任的[[Authorization-Server-Metadata|授权服务器 (AS)]]列表、受支持的 Scope 以及访问需求。

## 核心设计与发现机制

### 1. [[Protected-Resource-Metadata|发现路径格式]]
- 客户端发起 GET 请求访问 RS 的配置路径：
  - `https://<resource>/.well-known/oauth-protected-resource`
  - 如果 Resource URI 包含 Path，则按规则转换为 `https://<host>/.well-known/oauth-protected-resource/<path>`。

### 2. [[Protected-Resource-Metadata|受保护资源元数据属性]]
- `resource`: 资源服务器的规范 URI（对应 [[Resource-Indicators|RFC 8707 Resource Indicator]]）。
- `authorization_servers`: **核心字段**。包含该 RS 信任并可为其接受令牌的 AS Issuer URI 列表数组。客户端据此确定向哪一个 AS 申请令牌。
- `scopes_supported`: 该资源服务器支持或要求作用域列表。
- `bearer_methods_supported`: 传递 Access Token 的方式（如 `header`, `body`, `query`）。
- `resource_signing_alg_values_supported`: 资源服务器要求的签名算法（若使用 DPoP 或签名 Token）。
- `resource_documentation`: 人类可读的 API 开发文档地址。

## 与 RFC 8707 (Resource Indicators) 的闭环集成
- 客户端首先通过 RFC 9728 发现 RS 信任的 AS，以及该 RS 的 `resource` 标识符。
- 随后客户端向 AS 申请令牌时，使用 [[Resource-Indicators|RFC 8707 `resource` 参数]] 附带该标识符。
- AS 颁发带有 [[Audience-Restriction|`aud` 隔离]] 的 Access Token，客户端最终安全地调用该 RS。

---
**关联页面**：
- [[OAuth-2.0]] (授权框架)
- [[Protected-Resource-Metadata]] (协议概念)
- [[Authorization-Server-Metadata]] (AS端元数据发现 RFC 8414)
- [[Resource-Indicators]] (资源指示器 RFC 8707)
- [[Audience-Restriction]] (受众限制)
