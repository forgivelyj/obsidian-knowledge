---
title: "OAuth-2.0"
aliases: [OAuth2, OAuth 2.0 Framework]
tags: [security/framework/active]
category: entities
created: 2026-07-27
updated: 2026-07-27
sources: 
  - "[[raw/00-Inbox/RFC 8707 Resource Indicators for OAuth 2.0.md]]"
description: "OAuth 2.0 是一种业界标准的授权框架，允许第三方应用代表资源所有者获取受保护 HTTP 资源的有限访问权限。"
---

# OAuth 2.0

OAuth 2.0 是目前最广泛应用的授权框架（定义于 RFC 6749 和 RFC 6750 ）。

## 核心角色
- **Resource Owner (资源所有者)**：即用户。
- **Client (客户端)**：请求访问受保护资源的应用程序。
- **Resource Server (资源服务器)**：托管用户受保护资源的服务器，能够接受并校验 Access Token。
- **Authorization Server (授权服务器)**：负责验证资源所有者并向客户端发放令牌。

## 相关扩展协议
- [[Resource-Indicators]] (RFC 8707)：使客户端能够明确通知授权服务器当前申请的令牌究竟要在哪一个资源服务器（RS）上使用，从而生成具备 [[Audience-Restriction]] 的安全令牌。
