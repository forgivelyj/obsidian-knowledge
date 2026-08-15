---
title: "OAuth-2.0"
aliases: [OAuth2, OAuth 2.0 Framework]
tags: [security/framework/active]
category: entities
created: 2026-07-27
updated: 2026-08-05
sources: 
  - "[[raw/00-Inbox/RFC 8707 Resource Indicators for OAuth 2.0.md]]"
  - "[[raw/00-Inbox/RFC 7591 OAuth 2.0 Dynamic Client Registration Protocol.md]]"
  - "[[raw/00-Inbox/RFC 7636 Proof Key for Code Exchange by OAuth Public Clients.md]]"
  - "[[raw/00-Inbox/RFC 8252 OAuth 2.0 for Native Apps.md]]"
  - "[[raw/00-Inbox/RFC 8414 OAuth 2.0 Authorization Server Metadata.md]]"
  - "[[raw/00-Inbox/RFC 9728 OAuth 2.0 Protected Resource Metadata.md]]"
  - "[[raw/00-Inbox/OAuth Client ID Metadata Document.md]]"
description: "OAuth 2.0 是一种业界标准的授权框架，允许第三方应用代表资源所有者获取受保护 HTTP 资源的有限访问权限。"
---

# OAuth 2.0

OAuth 2.0 是目前最广泛应用的授权框架（定义于 RFC 6749 和 RFC 6750）。

## 核心角色
- **Resource Owner (资源所有者)**：即用户。
- **Client (客户端)**：请求访问受保护资源的应用程序。
- **Resource Server (资源服务器)**：托管用户受保护资源的服务器，能够接受并校验 Access Token。
- **Authorization Server (授权服务器)**：负责验证资源所有者并向客户端发放令牌。

## 核心扩展与安全协议族
- [[Resource-Indicators]] ([[Resource-Indicators|RFC 8707]])：资源指示器，使客户端能够明确声明目标 RS，实现 [[Audience-Restriction|受众限制]]。
- [[PKCE]] ([[PKCE|RFC 7636]])：授权码防拦截机制，使用动态密钥挑战保护公共客户端。
- [[OAuth-Native-Apps]] ([[OAuth-Native-Apps|RFC 8252]])：原生移动与桌面应用 OAuth 2.0 安全最佳实践 (BCP 212)。
- [[Dynamic-Client-Registration]] ([[Dynamic-Client-Registration|RFC 7591]])：客户端向授权服务器自动化发起动态注册的协议。
- [[OAuth-Client-ID-Metadata]]：使用 HTTPS URL 作为 Client ID 并自动拉取元数据的去中心化方案。
- [[Authorization-Server-Metadata]] ([[Authorization-Server-Metadata|RFC 8414]])：授权服务器元数据与终节点自动发现协议。
- [[Protected-Resource-Metadata]] ([[Protected-Resource-Metadata|RFC 9728]])：受保护资源（RS）自动发现其信任 AS 及支持作用域的元数据标准。

## 上层协议
- [[OpenID-Connect]]：在 OAuth 2.0 授权框架上构建的身份认证与 UserInfo 标准层。
