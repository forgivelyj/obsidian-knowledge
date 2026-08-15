---
title: "OAuth-Client-ID-Metadata"
aliases: [OAuth Client ID Metadata Document, URL Client ID, Decentralized Client Metadata]
tags: [security/concept/active]
category: concepts
created: 2026-08-05
updated: 2026-08-05
sources: 
  - "[[raw/00-Inbox/OAuth Client ID Metadata Document.md]]"
description: "将 HTTPS URL 作为 OAuth Client ID 并在该 URL 托管客户端元数据的去中心化识别规范。"
---

# OAuth Client ID Metadata Document

**OAuth Client ID Metadata Document** 是一种新型的轻量级客户端识别协议，旨在消除中心化登记和复杂注册接口的前提依赖。

## 设计背景与痛点
在传统的 [[OAuth-2.0]] 架构中，客户端必须事先在每一个 Authorization Server (AS) 开发者后台进行人工注册，或使用 [[Dynamic-Client-Registration|RFC 7591 动态注册]]。在联邦身份或分布式 OAuth 体系中，这种方式带来了极高的高粘合度和开销。

## 工作原理
1. **URL 即 Client ID**：客户端选择自己拥有域名控制权的 HTTPS URL（如 `https://client.example.com/oauth-client.json`）作为其 `client_id`。
2. **元数据托管**：客户端在改 URL 路径上以 JSON 格式提供自身的元数据定义（包括 `redirect_uris`, `grant_types`, `jwks_uri`, `client_name` 等）。
3. **AS 自动检索**：当用户尝试在该 AS 上使用该客户端时，AS 直接向该 `client_id` URL 发起 HTTPS GET 请求拉取配置。

## 与 RFC 7591 的对比
| 维度 | [[Dynamic-Client-Registration|RFC 7591 动态注册]] | OAuth Client ID Metadata |
| :--- | :--- | :--- |
| **状态存储** | AS 数据库端维护注册记录 | 客户端基于 URL 自托管声明 |
| **ID 颁发者** | AS 随机生成 `client_id` | 客户端自行指定 HTTPS 地址 |
| **密钥管理** | AS 颁发 `client_secret` 或预存 JWK | 客户端在其元数据 JSON 中指定 `jwks_uri` |
| **适用场景** | 企业级集中控制的 AS 系统 | 去中心化、联邦式 OAuth / 智能体协议 |

---
**关联页面**：
- [[OAuth-2.0]] (授权框架)
- [[Dynamic-Client-Registration]] (协议对比)
- [[Authorization-Server-Metadata]] (服务器端配置)
