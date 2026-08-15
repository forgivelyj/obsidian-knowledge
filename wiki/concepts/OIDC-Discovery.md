---
title: "OIDC-Discovery"
aliases: [OpenID Connect Discovery, OP Discovery, Issuer Discovery]
tags: [security/concept/active]
category: concepts
created: 2026-08-05
updated: 2026-08-05
sources: 
  - "[[raw/00-Inbox/Final OpenID Connect Discovery 1.0 incorporating errata set 2.md]]"
description: "OIDC Discovery 规范允许依赖方（RP）通过 WebFinger 定位 OpenID Provider，并从 well-known 端点自动获取配置与公钥集。"
---

# OpenID Connect Discovery

**OpenID Connect Discovery** 是 [[OpenID-Connect|OpenID Connect 1.0]] 体系中用于解决“客户端如何自动发现身份提供者 (OP) 及其服务端点”的标准机制。

## 两个阶段的工作流程

```mermaid
sequenceDiagram
    autonumber
    participant RP as Relying Party (Client)
    participant WF as WebFinger Endpoint
    participant OP as OpenID Provider (.well-known)

    Note over RP: 用户输入 identifier (e.g. joe@example.com)
    RP->>WF: GET /.well-known/webfinger?resource=acct:joe@example.com&rel=...
    WF-->>RP: 返回 JSON (href: https://server.example.com)
    Note over RP: 获得 Issuer URL: https://server.example.com
    RP->>OP: GET https://server.example.com/.well-known/openid-configuration
    OP-->>RP: 返回 OP Metadata JSON (endpoints, jwks_uri, algorithms)
```

### 阶段 1：Issuer Discovery (WebFinger)
- 目的：当用户仅提供 Email、域名或 URL 标识符时，确定处理该用户的 OP 所在地址。
- 端点：`/.well-known/webfinger`
- 参数：`resource` 与 `rel=http://openid.net/specs/connect/1.0/issuer`

### 阶段 2：OP Configuration Information
- 目的：获取该 OP 的所有技术参数。
- 端点：`/.well-known/openid-configuration`
- 关键字段：`issuer`, `authorization_endpoint`, `token_endpoint`, `userinfo_endpoint`, `jwks_uri`

## 关联标准
- [[Authorization-Server-Metadata]]：RFC 8414 对纯 [[OAuth-2.0]] 授权服务器元数据发现的泛化定义。
