---
title: "RFC-8707-Resource-Indicators-for-OAuth-2.0-summary"
aliases: [RFC 8707 摘要, Resource Indicators 摘要]
tags: [security/oauth2/active]
category: summaries
created: 2026-07-27
updated: 2026-07-27
sources: 
  - "[[raw/00-Inbox/RFC 8707 Resource Indicators for OAuth 2.0.md]]"
description: "RFC 8707 规定了 OAuth 2.0 的资源指示器参数，使客户端能够显式向授权服务器声明请求访问的受保护资源，从而实现 Audience 限制与安全隔离。"
---

# [[Resource-Indicators|RFC 8707]]: Resource Indicators for OAuth 2.0 摘要

## 概要说明
本协议定义了 OAuth 2.0 的扩展参数 `resource`，允许客户端在请求授权时显式向 [[OAuth-2.0]] 授权服务器（AS）声明它准备访问的受保护资源（RS，即应用或 API 地址）。

## 核心设计与参数
1. **`resource` 参数**：
   - 客户端在发送授权请求（如 GET /authorize）或令牌请求（如 POST /token）时，可以通过 `resource` 参数传入资源的绝对 URI（例如 `https://api.example.com/`）。
   - 该参数可以出现多次，以请求访问多个受保护资源。
   - 规则：必须是绝对 URI，不带 `#`（Fragment），原则上不带 `?`（Query）。
2. **`invalid_target` 错误**：
   - 如果所请求的资源非法、缺失、未知或不合规，AS 将返回此错误。

## 核心价值与安全作用
- **[[Audience-Restriction]]（[[Audience-Restriction|受众限制]]）**：AS 可以通过 JWT 中的 `aud` 声明，对颁发的 Access Token 进行受众隔离。防止受保护资源（RS1）拿着客户端发来的 Token 去非法访问另一个资源（RS2）（即防止 Token 重定向攻击）。
- **隐私与权限最小化（Downscoping）**：根据请求的目标资源，AS 能够下发降级的作用域。

---
**关联页面**：
- [[OAuth-2.0]] (框架实体)
- [[Resource-Indicators]] (协议概念)
- [[Audience-Restriction]] (安全概念)
