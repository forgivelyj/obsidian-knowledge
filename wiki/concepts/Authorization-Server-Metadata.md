---
title: "Authorization-Server-Metadata"
aliases: [OAuth 2.0 Authorization Server Metadata, RFC 8414, AS Metadata Discovery]
tags: [security/concept/active]
category: concepts
created: 2026-08-05
updated: 2026-08-05
sources: 
  - "[[raw/00-Inbox/RFC 8414 OAuth 2.0 Authorization Server Metadata.md]]"
description: "RFC 8414 定义的授权服务器元数据发现协议，使客户端能够自动发现 OAuth 2.0 AS 的终节点与能力配置。"
---

# Authorization Server Metadata (RFC 8414)

**OAuth 2.0 Authorization Server Metadata** (RFC 8414) 规范了客户端如何从 [[OAuth-2.0]] 授权服务器（Authorization Server, AS）自动获取服务终节点及安全属性配置。

## 发现路径规范
- **根域名格式**：`https://<issuer-host>/.well-known/oauth-authorization-server`
- **含 Path 的 Issuer 格式**：当 Issuer 包含路径（例如 `https://example.com/auth`）时，well-known 规范要求将 `/.well-known/oauth-authorization-server` 插入至 host 与 path 之间：
  - `https://example.com/.well-known/oauth-authorization-server/auth`

## 关键元数据属性
- `issuer`: AS 的唯一标识符 URL。
- `authorization_endpoint`: 授权端点 URL。
- `token_endpoint`: 令牌颁发端点 URL。
- `jwks_uri`: AS 的 JSON Web Key Set 公钥集中化 URL。
- `registration_endpoint`: [[Dynamic-Client-Registration|动态客户端注册端点 URL]]。
- `scopes_supported`: 支持的 Scope 列表。
- `grant_types_supported`: 支持的 Grant Types（如 `authorization_code`, `refresh_token`, `client_credentials`）。
- `code_challenge_methods_supported`: 支持的 [[PKCE]] 转换计算方式（如 `S256`）。
- `token_endpoint_auth_methods_supported`: 客户端认证支持的方式（如 `client_secret_basic`, `private_key_jwt`）。

## 与 OIDC Discovery 的关系
RFC 8414 继承并扩展了 [[OIDC-Discovery|OpenID Connect Discovery 1.0]] 的设计理念，但移除了 OIDC 专有的身份断言属性（如 `userinfo_endpoint`），从而使得纯 OAuth 2.0 授权服务器也能拥有解耦的标准发现机制。

---
**关联页面**：
- [[OAuth-2.0]] (授权框架)
- [[OIDC-Discovery]] (OIDC 发现对比)
- [[Protected-Resource-Metadata]] (资源服务器元数据发现 RFC 9728)
- [[Dynamic-Client-Registration]] (动态注册 RFC 7591)
