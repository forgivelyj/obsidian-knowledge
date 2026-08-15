---
title: "RFC-7636-Proof-Key-for-Code-Exchange-by-OAuth-Public-Clients-summary"
aliases: [RFC 7636 摘要, PKCE 摘要]
tags: [security/oauth2/active]
category: summaries
created: 2026-08-05
updated: 2026-08-05
sources: 
  - "[[raw/00-Inbox/RFC 7636 Proof Key for Code Exchange by OAuth Public Clients.md]]"
description: "RFC 7636 规定了用于 OAuth 2.0 公共客户端的 PKCE 协议，通过 code_verifier 与 code_challenge 防止授权码拦截攻击。"
---

# [[PKCE|RFC 7636]]: Proof Key for Code Exchange by OAuth Public Clients 摘要

## 概要说明
RFC 7636 定义了 **PKCE** (Proof Key for Code Exchange, 读作 "pixy") 协议。该协议专门解决 [[OAuth-2.0]] 公共客户端（Public Clients，如原生 App、单页应用 SPA）在授权码模式（Authorization Code Grant）下容易遭受的**授权码拦截攻击（Authorization Code Interception Attack）**。

## 攻击威胁与防护原理

### 1. [[PKCE|授权码拦截威胁]]
在移动设备或原生应用中，多个应用可能注册相同的 Custom URL Scheme。当授权服务器重定向发送授权码（Authorization Code）时，恶意应用可能拦截该授权码。由于公共客户端无法安全存储 `client_secret`，恶意应用可使用拦截到的授权码直接向 Token 端点换取 Access Token。

### 2. [[PKCE|PKCE 核心防御机制]]
PKCE 在授权请求与令牌请求之间建立了一次性密码学证明链接：
1. **生成 Code Verifier**：客户端生成一个高熵随机字符串 `code_verifier`（长度在 43 至 128 个字符之间，包含字母数字及 `-._~`）。
2. **计算 Code Challenge**：
   - 方式一 (`S256`推荐)：`code_challenge = BASE64URL-ENCODE(SHA256(code_verifier))`
   - 方式二 (`plain`不推荐)：`code_challenge = code_verifier`
3. **授权请求**：客户端在发起 `/authorize` 请求时携带 `code_challenge` 和 `code_challenge_method`。AS 暂存该挑战值并关联发出的授权码。
4. **令牌换取**：客户端向 `/token` 请求换取令牌时，在请求体中附带原始 `code_verifier`。
5. **AS 验证**：AS 使用同样的算法对 `code_verifier` 计算哈希并与原 `code_challenge` 比对。若匹配则发放令牌，若不匹配或缺失则拒绝。

## 安全要求与最佳实践
- **强制使用 S256**：所有支持 PKCE 的客户端与服务器必须支持 `S256` 算法。仅在客户端极端受限且无法实现 SHA-256 时才退化为 `plain`。
- **一次性校验**：`code_verifier` 必须使用后立即作废，每次授权请求必须生成全新的随机 `code_verifier`。

---
**关联页面**：
- [[OAuth-2.0]] (授权框架)
- [[PKCE]] (协议概念)
- [[OAuth-Native-Apps]] (原生应用规范 RFC 8252)
