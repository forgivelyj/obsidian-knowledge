---
title: "OAuth-Client-ID-Metadata-Document-summary"
aliases: [OAuth Client ID Metadata Document 摘要, URL Client ID 摘要]
tags: [security/oauth2/active]
category: summaries
created: 2026-08-05
updated: 2026-08-05
sources: 
  - "[[raw/00-Inbox/OAuth Client ID Metadata Document.md]]"
description: "定义了将 HTTPS URL 作为 OAuth Client ID 并直接在该 URL 暴露客户端元数据 JSON 的机制，实现无缝与去中心化的客户端识别。"
---

# [[OAuth-Client-ID-Metadata|OAuth Client ID Metadata Document]] 摘要

## 概要说明
本规范草案定义了一种轻量级、去中心化的 [[OAuth-2.0]] 客户端元数据识别机制。它允许客户端直接将其控制的 **HTTPS URL** 作为 `client_id`，且该 URL 请求将直接返回包含客户端元数据的 JSON 文档。

## 核心设计与机制

### 1. [[OAuth-Client-ID-Metadata|URL 作为 Client ID]]
- 传统 OAuth 2.0 要求客户端在各个 Authorization Server (AS) 上进行预注册或动态注册（如 [[Dynamic-Client-Registration|RFC 7591]]）。
- 本规范允许 `client_id` 直接为一个 HTTPS URL（例如 `https://app.example.com/oauth-client-metadata.json`）。
- AS 收到该 `client_id` 后，通过对该 URL 发起 GET 请求自动拉取元数据。

### 2. [[OAuth-Client-ID-Metadata|元数据 JSON 结构]]
元数据文档采用 JSON 格式，包含字段：
- `client_id`: 必须与其 URL 完全相同。
- `client_name`: 客户端名称。
- `redirect_uris`: 允许的重定向回调 URI 数组。
- `grant_types`: 支持的授权类型。
- `response_types`: 支持的响应类型。
- `jwks_uri` / `jwks`: 客户端公钥，用于非对称密钥认证（如 `private_key_jwt`）及请求对象签名。
- `logo_uri` / `policy_uri` / `tos_uri`: 品牌图标与隐私条款链接。

### 3. [[OAuth-Client-ID-Metadata|安全与验证规则]]
- **域名匹配与 HTTPS**：`client_id` 必须严格使用 `https://` 方案。
- **重定向限制**：AS 在解析 `client_id` URL 时，必须防范 SSRF（服务端请求伪造）与重定向攻击，并校验元数据中 `client_id` 与请求 URL 的严格匹配。

---
**关联页面**：
- [[OAuth-2.0]] (授权框架)
- [[OAuth-Client-ID-Metadata]] (协议概念)
- [[Dynamic-Client-Registration]] (对比机制 RFC 7591)
- [[Authorization-Server-Metadata]] (AS端元数据 RFC 8414)
