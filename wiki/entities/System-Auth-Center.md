---
title: "System-Auth-Center"
aliases: [system-auth-center, 认证中心微服务, ERPAuthCenter]
tags: [domain/software-engineering, type/framework, active]
category: entities
created: 2026-08-14
updated: 2026-08-14
sources:
  - "[[wiki/summaries/system-auth-center-summary.md]]"
description: "ERP 系统的集中式身份认证与授权中心服务实体"
---

# System-Auth-Center

`System-Auth-Center` 是企业 ERP 系统中的核心安防中间件，负责处理全系统的用户身份认证、客户端鉴权与令牌发放。

## 关键属性

- **微服务角色**: OAuth2 Authorization Server
- **依赖基础设施**: MySQL, Redis (DB 2/3/4), LDAP
- **通信协议**: REST / OAuth2 HTTP APIs, Feign 内部微服务通信
- **关键包路径**: `com.eccom.system.auth.center`

## 关联技术与概念

- [[OAuth-2.0]]
- [[System-Auth-Center-Architecture]]
- [[Custom-Token-Granter-Pattern]]
- [[Redis]]
