---
title: "OpenID-Connect"
aliases: [OIDC, OpenID Connect 1.0]
tags: [security/framework/active]
category: entities
created: 2026-08-05
updated: 2026-08-05
sources: 
  - "[[raw/00-Inbox/Final OpenID Connect Discovery 1.0 incorporating errata set 2.md]]"
description: "OpenID Connect 1.0 是构建在 OAuth 2.0 协议之上的简单身份层，支持客户端验证终端用户身份并获取基础 Profile 信息。"
---

# OpenID Connect

OpenID Connect 1.0 (OIDC) 是建立在 [[OAuth-2.0]] 授权框架之上的身份认证（Authentication）标准层。它补足了 OAuth 2.0 仅关注授权而非身份验证的不足。

## 核心组件与数据结构
- **ID Token**：基于 JWT 格式包含身份断言的令牌，由 OpenID Provider 签名。包含 `iss` (发布者), `sub` (用户唯一标识), `aud` (受众/Client ID), `exp` (过期时间) 等标准 Claim。
- **UserInfo Endpoint**：受保护的 REST 端点，客户端使用 Access Token 获取更丰富的用户 Profile 属性（如 `name`, `email`, `picture`）。
- **Relying Party (RP)**：依赖方，即请求身份认证的 OAuth 客户端。
- **OpenID Provider (OP)**：身份提供者，即具备 OIDC 认证能力的授权服务器。

## 核心机制与扩展
- [[OIDC-Discovery]] (OpenID Connect Discovery 1.0)：利用 WebFinger (`/.well-known/webfinger`) 进行身份提供者查找，并通过 `/.well-known/openid-configuration` 拉取公钥及端点配置。
- [[Dynamic-Client-Registration]]：结合 RFC 7591 规范支持 RP 在 OP 上的自动化注册。
