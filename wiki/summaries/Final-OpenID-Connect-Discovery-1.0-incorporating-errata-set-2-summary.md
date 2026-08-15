---
title: "Final-OpenID-Connect-Discovery-1.0-incorporating-errata-set-2-summary"
aliases: [OpenID Connect Discovery 1.0 摘要, OIDC Discovery 摘要]
tags: [security/oidc/active]
category: summaries
created: 2026-08-05
updated: 2026-08-05
sources: 
  - "[[raw/00-Inbox/Final OpenID Connect Discovery 1.0 incorporating errata set 2.md]]"
description: "OpenID Connect Discovery 1.0 规范定义了终端用户身份提供者（OP）发现（WebFinger）及 OP 配置元数据（.well-known/openid-configuration）获取机制。"
---

# [[OIDC-Discovery|OpenID Connect Discovery 1.0]] 摘要

## 概要说明
本规范定义了 [[OpenID-Connect]] (OIDC) Relying Party (RP, 依赖方/客户端) 发现 OpenID Provider (OP, 身份提供者) 并获取与之交互所需配置信息的标准化机制。

## 核心机制

### 1. [[OIDC-Discovery|OP Issuer Discovery (发布者发现)]]
- **发现协议**：使用 **WebFinger** ([RFC 7033]) 协议。
- **请求格式**：向主机的 `/.well-known/webfinger` 端点发起 GET 请求：
  - `resource`: 用户输入的标识符（支持 URL、`acct:` Email 格式、`host:port` 等）。
  - `rel`: 必须为 `http://openid.net/specs/connect/1.0/issuer`。
- **响应返回**：返回 JRD (JSON Resource Descriptor)，其中包含 OP 的唯一 Issuer 地址（必须为 `https://` 协议，且不含 Query 或 Fragment）。

### 2. [[OIDC-Discovery|OP Configuration Information (配置元数据获取)]]
- **配置路径**：在 Issuer 地址后拼接 `/.well-known/openid-configuration`。
- **核心元数据字段**：
  - `issuer`: OP 的唯一标识（必须与 WebFinger 和 ID Token 中的 `iss` 匹配）。
  - `authorization_endpoint`: 授权端点 URL。
  - `token_endpoint`: 令牌端点 URL。
  - `userinfo_endpoint`: 用户信息端点 URL。
  - `jwks_uri`: 公钥 JWK Set 文档地址（供 RP 校验签名）。
  - `registration_endpoint`: [[Dynamic-Client-Registration|动态客户端注册端点]] URL。
  - `scopes_supported`: 支持的 Scope 列表（必须包含 `openid`）。
  - `response_types_supported`: 支持的 Response Type 列表。
  - `id_token_signing_alg_values_supported`: ID Token 签名算法（必须包含 `RS256`）。

## 跨域与安全要求
- 所有通信必须强制使用 **TLS/HTTPS**。
- WebFinger 及配置/密钥端点必须支持 **CORS**（跨源资源共享），以便 JavaScript 和浏览端客户端安全调用。

---
**关联页面**：
- [[OpenID-Connect]] (身份框架)
- [[OAuth-2.0]] (授权框架)
- [[OIDC-Discovery]] (协议概念)
- [[Authorization-Server-Metadata]] (关联规范 RFC 8414)
- [[Dynamic-Client-Registration]] (动态注册 RFC 7591)
