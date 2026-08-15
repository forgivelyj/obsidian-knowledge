---
title: "RFC-7591-OAuth-2.0-Dynamic-Client-Registration-Protocol-summary"
aliases: [RFC 7591 摘要, 动态客户端注册摘要]
tags: [security/oauth2/active]
category: summaries
created: 2026-08-05
updated: 2026-08-05
sources: 
  - "[[raw/00-Inbox/RFC 7591 OAuth 2.0 Dynamic Client Registration Protocol.md]]"
description: "RFC 7591 定义了 OAuth 2.0 动态客户端注册协议，允许客户端自动向授权服务器注册并获得凭证及配置管理 API。"
---

# [[Dynamic-Client-Registration|RFC 7591]]: OAuth 2.0 Dynamic Client Registration Protocol 摘要

## 概要说明
RFC 7591 建立了 [[OAuth-2.0]] 动态客户端注册协议，允许第三方客户端应用程序在无需人工干预的情况下，自动向授权服务器 (AS) 发起注册，获取分配的 `client_id`、`client_secret`（如适用）及注册管理凭证。

## 核心设计与接口

### 1. [[Dynamic-Client-Registration|注册端点 (Client Registration Endpoint)]]
- 客户端向 AS 暴露的客户端注册端点发送 `POST` 请求（通常为 JSON 格式）。
- **常用请求元数据**：
  - `redirect_uris`: 重定向回调 URI 数组（必须）。
  - `token_endpoint_auth_method`: 客户端认证方式（如 `client_secret_basic`, `private_key_jwt`, `none`）。
  - `grant_types`: 声明需要的 Grant Types（默认 `["authorization_code"]`）。
  - `response_types`: 声明需要的 Response Types。
  - `client_name` / `logo_uri` / `client_uri`: 展示信息。
  - `jwks_uri` / `jwks`: 客户端公钥集。
  - `software_id` / `software_version`: 软件标识。

### 2. [[Dynamic-Client-Registration|注册响应与凭证]]
- 成功响应返回 `201 Created` 及 JSON 对象：
  - `client_id`: 授权服务器分配的唯一标识符（必须）。
  - `client_secret`: 机密客户端的密钥（若适用）。
  - `client_id_issued_at` / `client_secret_expires_at`: 颁发与过期时间戳。
  - `registration_access_token`: 专门用于管理（读取/更新/注销）该注册凭证的 Bearer Token。
  - `registration_client_uri`: 该客户端专属的管理配置 URI。

### 3. [[Dynamic-Client-Registration|客户端管理接口 (Client Configuration Endpoint)]]
配合管理令牌，支持对注册信息进行标准 HTTP 操作：
- `GET`：读取客户端当前注册元数据。
- `PUT`：更新客户端注册信息。
- `DELETE`：注销/删除客户端注册。

---
**关联页面**：
- [[OAuth-2.0]] (授权框架)
- [[Dynamic-Client-Registration]] (协议概念)
- [[OAuth-Client-ID-Metadata]] (去中心化元数据对比)
- [[Authorization-Server-Metadata]] (AS 元数据 RFC 8414)
