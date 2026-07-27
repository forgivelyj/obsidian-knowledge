---
title: "Resource-Indicators"
aliases: [资源指示器, RFC 8707]
tags: [security/oauth2/active]
category: concepts
created: 2026-07-27
updated: 2026-07-27
sources: 
  - "[[raw/00-Inbox/RFC 8707 Resource Indicators for OAuth 2.0.md]]"
description: "资源指示器是 OAuth 2.0 框架下通过指定 resource 参数来声明目标受保护资源地址的一种标准安全机制。"
---

# Resource Indicators (资源指示器)

Resource Indicators（RFC 8707）是针对 [[OAuth-2.0]] 授权框架的一项重要安全扩展。

## 概念定义
在默认的 [[OAuth-2.0]] 中，客户端请求令牌时使用 `scope` 来指定访问的权限类型（如 `read`, `write`），但很难区分这些权限是在哪个物理服务（API 端点）上使用。**资源指示器**通过引入 `resource` 参数，将“申请什么权限 (Scope)”与“在何处行使权限 (Resource)”进行了解耦。

## 工作机理
1. **客户端请求**：客户端在 /authorize 或 /token 请求中附加 `resource=https://api.example.com/`。
2. **授权服务器验证**：AS 校对客户端是否有权访问此资源，生成对该资源进行 [[Audience-Restriction]] 的 Access Token。
3. **资源服务器校验**：RS 收到 Token 后，必须验证 Token 中的 `aud` 属性是否匹配自身的资源 URI，防止 Token 被盗用。
