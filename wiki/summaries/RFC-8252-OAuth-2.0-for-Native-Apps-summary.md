---
title: "RFC-8252-OAuth-2.0-for-Native-Apps-summary"
aliases: [RFC 8252 摘要, Native Apps BCP 摘要]
tags: [security/oauth2/active]
category: summaries
created: 2026-08-05
updated: 2026-08-05
sources: 
  - "[[raw/00-Inbox/RFC 8252 OAuth 2.0 for Native Apps.md]]"
description: "RFC 8252 (BCP 212) 规定了移动及桌面原生应用 OAuth 2.0 最佳实践，要求强制使用外部系统浏览器与 PKCE 防护。"
---

# [[OAuth-Native-Apps|RFC 8252]]: OAuth 2.0 for Native Apps 摘要

## 概要说明
RFC 8252 (BCP 212) 规定了原生应用（Native Apps，包括移动 iOS/Android 应用与桌面应用）执行 [[OAuth-2.0]] 授权的最佳当前实践 (Best Current Practice)。

## 核心安全规范

### 1. [[OAuth-Native-Apps|强制使用外部用户代理 (External User-Agent)]]
- **绝对禁止使用嵌入式 Web 视图 (Embedded Web Views / WebView)**：WebView 会使原生应用获得拦截用户输入的明文用户名与密码的能力，严重破坏隔离性，增加凭证泄露与钓鱼风险。
- **必须使用外部浏览器 (External User-Agent)**：
  - 系统默认浏览器。
  - 浏览器原生安全选项卡（如 Android Custom Tabs、iOS `SFSafariViewController` / `ASWebAuthenticationSession`）。
- **优势**：确保凭证只输入给信任的身份提供者（AS），且可共享浏览器的 Single Sign-On (SSO) 会话 Cookie。

### 2. [[OAuth-Native-Apps|原生应用重定向回调机制]]
原生应用支持三种标准的重定向 URI 处理方式：
1. **自定义 URL 方案 (Custom URL Schemes)**：如 `com.example.app:/oauth2redirect`（需配合 PKCE 防止拦截）。
2. **通用链接/应用链接 (Universal Links / App Links)**：如 `https://app.example.com/oauth2redirect`（通过 HTTPS 域名校验实现强所有权绑定，更加安全）。
3. **回环 IP 地址 (Loopback IP Address)**：用于桌面应用，如 `http://127.0.0.1:port/path` 或 `http://[::1]:port/path`（允许使用随机可用端口）。

### 3. [[OAuth-Native-Apps|强制结合 PKCE 防护]]
原生应用属于公共客户端（Public Clients），所有 Native App 授权请求**必须**同时启用 [[PKCE|RFC 7636 (PKCE)]] 防护，确保即使重定向回调被恶意应用窃听，也无法换取 Access Token。

---
**关联页面**：
- [[OAuth-2.0]] (授权框架)
- [[OAuth-Native-Apps]] (协议概念)
- [[PKCE]] (关联安全机制 RFC 7636)
