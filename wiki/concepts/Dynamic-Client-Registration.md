---
title: "Dynamic-Client-Registration"
aliases: [动态客户端注册, RFC 7591, Client Registration Endpoint]
tags: [security/concept/active]
category: concepts
created: 2026-08-05
updated: 2026-08-05
sources: 
  - "[[raw/00-Inbox/RFC 7591 OAuth 2.0 Dynamic Client Registration Protocol.md]]"
description: "RFC 7591 规范允许客户端程序在无需人工干预的情况下向 OAuth 2.0 授权服务器自动注册并管理其属性和凭证。"
---

# Dynamic Client Registration (RFC 7591)

**动态客户端注册 (Dynamic Client Registration)** 是定义于 RFC 7591 的 [[OAuth-2.0]] 扩展协议。它允许客户端向 [[Authorization-Server-Metadata|授权服务器]] 自动化申请接入凭证。

## 交互过程

```mermaid
sequenceDiagram
    autonumber
    participant Client as 客户端 (Client)
    participant AS as 授权服务器 (AS)

    Client->>AS: POST /register (附带 redirect_uris, client_name, jwks_uri 等)
    Note over AS: 校验元数据并生成凭证
    AS-->>Client: 201 Created (返回 client_id, client_secret, registration_access_token)
    
    Note over Client: 使用 registration_access_token 管理配置
    Client->>AS: GET /register/{client_id} (Header: Authorization: Bearer registration_access_token)
    AS-->>Client: 200 OK (返回最新配置)
```

## 核心配置属性
- **注册输入**：`redirect_uris` (必须), `client_name`, `grant_types`, `response_types`, `token_endpoint_auth_method`, `jwks_uri` / `jwks`。
- **注册输出**：`client_id`, `client_secret` (若机密客户端), `client_id_issued_at`, `client_secret_expires_at`, `registration_access_token`, `registration_client_uri`。

## 安全考虑
- **初始化访问控制 (Initial Access Token)**：AS 可以要求客户端在请求 `/register` 时附带初始 Bearer Token，以防无差别注册滥用。
- **软件断言 (Software Statement)**：客户端可提交经过第三方 CA 或厂商签名的 JWT（`software_statement`），证明其合法来源与合规元数据。

---
**关联页面**：
- [[OAuth-2.0]] (授权框架)
- [[OpenID-Connect]] (OIDC 注册集成)
- [[OAuth-Client-ID-Metadata]] (去中心化对比)
