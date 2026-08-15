---
title: "System-Auth-Center-Architecture"
aliases: [认证中心系统架构, SystemAuthCenterArchitecture]
tags: [domain/software-engineering, type/pattern, active]
category: concepts
created: 2026-08-14
updated: 2026-08-14
sources:
  - "[[wiki/summaries/system-auth-center-summary.md]]"
description: "system-auth-center 微服务认证中心的安全过滤器链、授权端点与 Token 增强架构概念"
---

# System-Auth-Center-Architecture

`System-Auth-Center-Architecture` 指的是基于 Spring Security OAuth2 构建的高复用、防刷限流、多租户认证服务架构模式。

## 架构核心组件

1. **`WebSecurityConfig`**：定义主安全过滤链与核心拦截路径。
2. **`Oauth2ServerConfig`**：配置令牌终节点与客户端接入明细。
3. **`EccomJwtAccessTokenEnhancer`**：在颁发 JWT 令牌时动态插入扩展用户数据。
4. **`EccomWebResponseExceptionTranslator`**：统一异常翻译层。

## 关联实体与概念

- [[System-Auth-Center]]
- [[Custom-Token-Granter-Pattern]]
- [[OAuth-2.0]]
