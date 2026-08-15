---
title: "OAuth-Native-Apps"
aliases: [OAuth 2.0 for Native Apps, RFC 8252, BCP 212, Native App Authentication]
tags: [security/concept/active]
category: concepts
created: 2026-08-05
updated: 2026-08-05
sources: 
  - "[[raw/00-Inbox/RFC 8252 OAuth 2.0 for Native Apps.md]]"
description: "RFC 8252 (BCP 212) 确立的移动与桌面原生应用 OAuth 2.0 最佳安全实践指南。"
---

# OAuth 2.0 for Native Apps (RFC 8252 / BCP 212)

**OAuth 2.0 for Native Apps** (RFC 8252，最佳当前实践 BCP 212) 规范了在移动设备（iOS、Android）和桌面操作系统（macOS、Windows、Linux）上开发原生应用接入 [[OAuth-2.0]] / [[OpenID-Connect]] 时的最佳安全机制。

## 核心安全规则与禁忌

### 1. 禁用嵌入式 Web 视图 (Embedded Web Views)
- **禁用规则**：严禁在原生 App 中内嵌 `WebView` (Android) 或 `UIWebView`/`WKWebView` (iOS) 来呈现 AS 登录界面。
- **原因**：内嵌 WebView 允许应用宿主拦截键盘输入、窃取密码及篡改 DOM 树，使用户面临凭证窃取与钓鱼风险。

### 2. 强制使用外部用户代理 (External User-Agent)
- **实现方案**：
  - 调用系统默认浏览器。
  - 使用系统安全选项卡组件（如 Android Custom Tabs, iOS `ASWebAuthenticationSession` / `SFSafariViewController`）。
- **收益**：保护凭证安全、支持跨应用 SSO 会话复用、隔离 App 进程与身份提供者 Cookie。

### 3. 三种标准重定向方案
1. **Private-Use URI Scheme (自定义 Scheme)**：如 `com.example.app:/oauth2redirect`。
2. **Claimed HTTPS Redirection (通用链接 / App Links)**：如 `https://app.example.com/oauth2redirect`（通过操作系统 HTTPS 关联校验，安全性最高）。
3. **Loopback IP Redirect (回环地址)**：用于桌面应用，使用 `http://127.0.0.1:port/path` 或 `http://[::1]:port/path`。

### 4. 强制启用 [[PKCE]]
由于原生应用属于无法安全保护 `client_secret` 的公共客户端，必须搭配 [[PKCE|RFC 7636 (PKCE)]] 来抵御授权码拦截攻击。

---
**关联页面**：
- [[OAuth-2.0]] (授权框架)
- [[PKCE]] (核心依赖防护 RFC 7636)
- [[OpenID-Connect]] (身份认证层)
