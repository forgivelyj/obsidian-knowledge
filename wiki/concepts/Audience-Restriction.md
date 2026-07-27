---
title: "Audience-Restriction"
aliases: [受众限制, 观众限制]
tags: [security/oauth2/active]
category: concepts
created: 2026-07-27
updated: 2026-07-27
sources: 
  - "[[raw/00-Inbox/RFC 8707 Resource Indicators for OAuth 2.0.md]]"
description: "受众限制是一种访问控制机制，用来限定 Access Token 只能在特定的受众（Audience / 资源服务器）中使用，防范 Token 滥用。"
---

# Audience Restriction (受众限制)

受众限制是保障分布式授权系统（如 [[OAuth-2.0]]）安全的核心安全机制之一。

## 原理解析
如果一个访问令牌（Access Token）没有受众限制，那么该令牌对于任何受保护的资源都是有效的。一旦某个恶意的资源服务器（RS1）拿到了客户端发来的 Token，它就可以充当客户端去访问另一个敏感的资源服务器（RS2），即“Token 转发/重定向攻击”。

通过受众限制：
- 授权服务器（AS）在生成令牌时，在其中写入受众标识（例如在 JWT 格式的令牌中设定 `aud` 声明，或在 Token 内省响应中返回 `aud` 字段）。
- 接收令牌的资源服务器（RS）**必须**核对自身的物理标识是否被包含在 `aud` 列表中。若不包含，则必须拒绝访问。

在 RFC 8707 中，通过 [[Resource-Indicators]] 传递的 `resource` 属性，就是授权服务器用来锁定 `aud` 值的核心数据源。
