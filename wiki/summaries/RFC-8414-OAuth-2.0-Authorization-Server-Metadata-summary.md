---
title: "RFC-8414-OAuth-2.0-Authorization-Server-Metadata-summary"
aliases: [RFC 8414 摘要, 授权服务器元数据摘要]
tags: [security/oauth2/active]
category: summaries
created: 2026-08-05
updated: 2026-08-05
sources: 
  - "[[raw/00-Inbox/RFC 8414 OAuth 2.0 Authorization Server Metadata.md]]"
description: "RFC 8414 规定了 OAuth 2.0 授权服务器元数据发现协议（/.well-known/oauth-authorization-server），解耦纯 OAuth 2.0 与 OpenID Connect 发现。"
---

# [[Authorization-Server-Metadata|RFC 8414]]: OAuth 2.0 Authorization Server Metadata 摘要

## 概要说明
RFC 8414 建立了纯 [[OAuth-2.0]] 授权服务器 (Authorization Server, AS) 元数据发现标准。它允许客户端以与 OIDC 无关的方式，自动发现 AS 的终节点位置、支持的 Grant Types、加密算法及安全特性。

## 核心配置与获取机制

### 1. [[Authorization-Server-Metadata|元数据 URI 发现规则]]
- **默认地址**：`https://<issuer>/.well-known/oauth-authorization-server`
- **带 Path 的 Issuer 格式**：如果 Issuer 包含路径（例如 `https://example.com/oauth2/v1`），则元数据地址插入在 Host 与 Path 之间，形成 `https://example.com/.well-known/oauth-authorization-server/oauth2/v1`。

### 2. [[Authorization-Server-Metadata|关键元数据字段]]
- `issuer`: AS 的官方标识符 URL。
- `authorization_endpoint`: 授权端点。
- `token_endpoint`: 令牌端点。
- `jwks_uri`: AS 公钥集 URL。
- `registration_endpoint`: [[Dynamic-Client-Registration|动态客户端注册端点]]。
- `scopes_supported`: AS 支持的 Scope 集合。
- `response_types_supported`: 支持的响应类型。
- `grant_types_supported`: 支持的授权类型。
- `token_endpoint_auth_methods_supported`: 客户端认证方式。
- `code_challenge_methods_supported`: 支持的 [[PKCE]] 挑战计算算法（如 `S256`）。
- `revocation_endpoint` / `introspection_endpoint`: 令牌撤销与自省端点。

## 与 OIDC Discovery 的异同
- **解耦**：OIDC Discovery (`.well-known/openid-configuration`) 包含用户身份相关属性（如 `userinfo_endpoint`）；而 RFC 8414 专注于纯授权（OAuth 2.0）框架属性。
- **兼容性**：AS 可以同时支持并挂载这两个 well-known 配置文件。

---
**关联页面**：
- [[OAuth-2.0]] (授权框架)
- [[Authorization-Server-Metadata]] (协议概念)
- [[OIDC-Discovery]] (OIDC 发现对比)
- [[Protected-Resource-Metadata]] (RS 端元数据发现 RFC 9728)
