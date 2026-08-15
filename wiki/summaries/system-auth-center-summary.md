---
title: "System Auth Center 代码库摘要说明"
aliases: [system-auth-center-summary, 认证中心代码库摘要]
tags: [software-engineering/auth, type/summary, active]
category: summaries
created: 2026-08-14
updated: 2026-08-14
sources:
  - "[[raw/10-Work/system-auth-center.md]]"
description: "Java 微服务认证中心 system-auth-center 的架构概览、定制 TokenGranter 机制与核心配置组件总结"
---

# System Auth Center 代码库摘要说明

`system-auth-center` 是 ERP 系统的集中认证授权中心微服务。基于 Spring Boot 2.x、Legacy Spring Cloud OAuth2 以及 MyBatis (`tk.mybatis`) 构建。

## 核心观点与设计要素

1. **分布式 OAuth2 认证架构**：采用 `Oauth2ServerConfig` 托管授权终节点，借助 `RedisTokenStore` 实现全局 Token 无状态校验与存储。
2. **可扩展 TokenGranter 责任链**：通过继承 `AbstractCustomTokenGranter`，灵活支撑 LDAP、手机验证码、社交登录与 Token Exchange 等多种扩展鉴权模式。
3. **安全拦截与多语言支持**：自定义过滤器与 Provider 统一以 `Eccom` 为前缀命名，配合 `EccomWebResponseExceptionTranslator` 提供统一的 JSON 异常格式与 i18n 国际化响应。

关联实体与概念：
- [[System-Auth-Center]]
- [[System-Auth-Center-Architecture]]
- [[Custom-Token-Granter-Pattern]]
