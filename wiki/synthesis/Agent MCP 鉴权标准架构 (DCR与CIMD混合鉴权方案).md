---
title: "Agent MCP 鉴权标准架构 (DCR与CIMD混合鉴权方案)"
aliases: [DCR与CIMD混合鉴权方案, Agent MCP Authentication Standard Architecture]
tags: [ai/mcp/active, security/oauth2/active, architecture/pattern]
category: synthesis
created: 2026-08-10
updated: 2026-08-13
sources: 
  - "[[raw/00-Inbox/MCP-模型上下文协议/MCP-模型上下文协议.md]]"
description: "Agent MCP 体系中基于 DCR、CIMD、RFC 9728、RFC 6750 与 2-Step RFC 8693 Token Exchange 的企业级混合鉴权标准规范。"
---

# Agent MCP 鉴权标准架构 (DCR与CIMD混合鉴权方案)

**版本号**：v2.0  
**更新时间**：2026-08-13  
**适用范围**：Agent MCP 客户端 (WorkBuddy, Kiro, LobeHub, Cursor, VSCode)、MCP 服务器 (eco-mcp-server)、授权中心 (system-auth-center) 及后端微服务网关。

---

## 1. 方案选型与依据 (Protocol Rationale & Standards Matrix)

### 1.1 IETF 核心协议标准矩阵

本架构完全基于 IETF OAuth 2.0 国际标准规范与草案，核心标准选型与工程实现依据如下：

| **RFC / Standard** | **规范名称** | **在系统中的工程落地路径与依据说明** |
| :--- | :--- | :--- |
| **RFC 6750** | Bearer Token & 401 Challenge | [`main.py`](file:///D:/workspace/mcp-server/eco-mcp-server/main.py)<br/>- `AuthChallengeMiddleware` 仅拦截 `/v2/mcp` 请求，未认证时返回 `401 Unauthorized` 并在 `WWW-Authenticate` 广播元数据路径。 |
| **RFC 7591** | Dynamic Client Registration (DCR) | [`DcrClientRegistrationController.java`](file:///d:/workspace/java-project/erp/system-auth-center/src/main/java/com/eccom/system/auth/center/controller/DcrClientRegistrationController.java)<br/>- 暴露 `POST /oauth/register`<br/>- 支持开关控制与请求来源 (`allowed-origins` IP/Origin) 安全防范<br/>- 实施 `client_name` 去重与自动开启 `autoApproveScopes=["true"]`<br/>- 保持数据库中 `resource_ids = NULL` 强制受控于 Gate 1 资源开放表。 |
| **RFC 8693** | OAuth 2.0 Token Exchange | [`TokenExchangeGranter.java`](file:///d:/workspace/java-project/erp/system-auth-center/src/main/java/com/eccom/system/auth/center/granter/TokenExchangeGranter.java) & [`AuthController.java`](file:///d:/workspace/java-project/erp/system-auth-center/src/main/java/com/eccom/system/auth/center/controller/AuthController.java)<br/>- 暴露 Step 1 `POST /auth/token/exchange` 存储 ID Token 至 Redis DB 2<br/>- 暴露 Step 2 `POST /auth/oauth/token` (`grant_type=urn:ietf:params:oauth:grant-type:token-exchange`) 发起凭证下发。 |
| **RFC 8707** | Resource Indicators for OAuth 2.0 | [`CustomOAuth2RequestFactory.java`](file:///d:/workspace/java-project/erp/system-auth-center/src/main/java/com/eccom/system/auth/center/config/CustomOAuth2RequestFactory.java)<br/>- 比对 `oauth_resource_detail` 表校验 `resource` 开放状态 (`status=1`)<br/>- 自动追加默认受众 `erp-sys-auth` 并写入 JWT `aud`。 |
| **RFC 9728** | Protected Resource Metadata | [`main.py`](file:///D:/workspace/mcp-server/eco-mcp-server/main.py)<br/>- 暴露 `GET /.well-known/oauth-protected-resource` 广播受信任 AS 列表 (`authorization_servers: ["http://localhost:9777"]`)。 |
| **RFC 8414** | Authorization Server Metadata | [`OidcMetadataController.java`](file:///d:/workspace/java-project/erp/system-auth-center/src/main/java/com/eccom/system/auth/center/controller/OidcMetadataController.java)<br/>- 广播 `registration_endpoint` 与 `code_challenge_methods_supported`。 |
| **RFC 7636** | PKCE (Proof Key for Code Exchange) | 公共客户端（Public Client）强制使用 `S256` PKCE 算法，免 `client_secret` 授权。 |
| **RFC 8252** | OAuth 2.0 for Native Apps | [`LoopbackRedirectResolver.java`](file:///d:/workspace/java-project/erp/system-auth-center/src/main/java/com/eccom/system/auth/center/config/LoopbackRedirectResolver.java) & [`DcrClientRegistrationController.java`](file:///d:/workspace/java-project/erp/system-auth-center/src/main/java/com/eccom/system/auth/center/controller/DcrClientRegistrationController.java)<br/>- **注册阶段**：完整保存带动态端口 URI (`http://localhost:57626/oauth/callback`)，复用客户端时合并保存最新 URI<br/>- **校验阶段**：对本地回环 `127.0.0.1` / `localhost` / `[::1]` 忽略动态端口比对，仅校验 Scheme、Host 与 Path。 |
| **CIMD Draft** | Client ID Metadata Document | [`CimdClientDetailsService.java`](file:///d:/workspace/java-project/erp/system-auth-center/src/main/java/com/eccom/system/auth/center/service/impl/CimdClientDetailsService.java)<br/>- HTTPS URL 动态抓取与 Redis 1 小时缓存（未来去中心化扩展）。 |

### 1.2 DCR 与 CIMD 选型与防数据库膨胀依据
1. **现状落地选型：RFC 7591 DCR 与 `client_name` 去重机制**
   - **物理现状**：主流通用 Agent 客户端（如 WorkBuddy、Kiro、Figma MCP）在未预置静态 Client ID 时，普遍依赖 RFC 7591 规定的 `registration_endpoint` (`POST /oauth/register`) 动态生成客户端。
   - **防数据库膨胀机制**：为防止 `oauth_client_details` 数据库膨胀，授权中心在实现 DCR 时采用了 **`client_name` 防重复注册与去重复用机制**，对同名或同应用的 Agent 请求自动复用已有 `client_id`。
   - **安全防护与来源限制机制**：在授权中心 `application.yml` 中提供 `mcp.auth.dcr.enabled` 开关与 `allowed-origins` 来源白名单校验，防止非法外部来源恶意调用 DCR 注册端点。
2. **DCR 动态资源权限判定 (Gate 1 开放表校验依据)**
   - 由于 DCR 客户端动态生成，在 `oauth_client_details` 表中**不会事先注册静态的 `resource_ids`**（即数据库中保持为 `NULL`），无法采用传统静态客户端配置比对的方式判断资源权限；
   - 当 DCR 客户端在请求 Token 或授权码时传入 `resource` 参数（如 `resource=urn:mcp:jira-service` 或默认 `erp-sys-auth`），系统自动使用传入的 `resource` 与数据库 `oauth_resource_detail` 表进行实时匹配；
   - **判定规则**：**只有当 `oauth_resource_detail` 表中存在该资源定义且状态为启用 (`status = 1`，即系统认可的公开受保护资源) 时，授权中心才会允许授权并颁发令牌**；否则抛出 `InvalidTargetException` 拒绝颁发。
3. **未来趋势扩展选型：CIMD (Client ID Metadata Document Draft)**
   - **规范原理**：客户端无需发起 `POST /oauth/register`，直接传 HTTPS URL 作为 `client_id`（如 `https://lobehub.com/client-metadata.json`），授权中心自动抓取与 Redis 缓存。
   - **定位**：作为面向未来去中心化 Agent 接入的补充扩展能力保留。

---

## 2. 认证方案 (Authentication Scheme / Architecture Overview)

### 2.1 总体架构设计
本方案旨在构建一套符合 IETF 国际标准、安全解耦且兼顾新老客户端的企业级 GenAI 零信任鉴权体系。系统解耦**传输通道安全**与**用户身份传播**，通过代理层隔离用户凭证，并在 MCP 执行端基于标准协议进行动态授权与令牌下发。

```text
                  ┌─────────────────────────────────────────┐
                  │          终端用户 (SSO 登录)            │
                  └────────────────────┬────────────────────┘
                                       │
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │   Agent 客户端 (WorkBuddy/Kiro/Lobe)    │
                  └───────────┬─────────────────┬───────────┘
                              │ (V1 模式:       │ (V2 模式:
                              │  直传 X-ID-Token│  401 质询 + 
                              │  访问 /mcp)     │  OAuth2 连入 /v2/mcp)
                              ▼                 ▼
                  ┌─────────────────────────────────────────┐
                  │         MCP Server (eco-mcp-server)     │
                  │   ┌─────────────────────────────────┐   │
                  │   │  AuthChallengeMiddleware (拦截) │   │
                  │   │  Session Store (凭证绑定/继承)   │   │
                  │   └────────────────┬────────────────┘   │
                  └────────────────────┼────────────────────┘
                                       │ 2-Step Token Exchange
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │     授权中心 (system-auth-center)       │
                  │   - Step 1: POST /auth/token/exchange   │
                  │   - Step 2: POST /auth/oauth/token      │
                  └────────────────────┬────────────────────┘
                                       │
                                       ▼ (颁发下游 Access Token)
                  ┌─────────────────────────────────────────┐
                  │       后端网关 / 业务微服务 (API)       │
                  └─────────────────────────────────────────┘
```

### 2.2 核心原则与设计特性
1. **双接入点隔离 (Dual-Endpoint Isolation)**：
   - **V2 接入点 (`/v2/mcp`)**：标准 OAuth2 质询端点。未认证访问时触发 RFC 6750 HTTP 401 质询与 RFC 9728 元数据发现，支持基于 DCR 的自动注册与 SSO 登录；
   - **V1 接入点 (`/mcp`)**：无质询直连端点。允许匿名建连，兼容传统直传 `X-ID-Token` 的客户端。
2. **DCR 静默免确认授权与可配置来源限制 (`autoApprove = true` & `allowed-origins`)**：
   - DCR 动态注册客户端默认设置 `autoApproveScopes = ["true"]`，用户完成企业 SSO 认证后自动跳过繁琐的确认授权 Consent 页面，实现无感平滑连入；
   - 支持通过 `application.yml` 配置 `mcp.auth.dcr.allowed-origins` 来源白名单限制，可精细限定可发起 DCR 注册的客户端 IP、Host 及来源。
3. **2-Step 令牌交换 (RFC 8693 Token Exchange)**：
   - Agent 连入 MCP 时持有的 `mcp_token` 仅具备 MCP 资源作用域；
   - 工具调用时，MCP Server 自动将凭证通过 **Step 1 (`/auth/token/exchange`)** 换取 Agent ID Token (`subject_token`)，再通过 **Step 2 (`/auth/oauth/token` `grant_type=token-exchange`)** 换取真正可访问下游 API 的 `access_token`。
4. **配置集中收敛与 Gate 1 资源指示 (YML Uncoupling)**：
   - 默认受众 `erp-sys-auth` 及作用域 (`read`, `write`, `openid`, `mcp`) 集中收敛在 `application.yml` 管理，彻底解耦硬编码；
   - DCR 客户端在数据库中 `resource_ids` 设为 `NULL`，强制受控于 Gate 1 资源开放表 (`oauth_resource_detail`) 动态判定。

---

## 3. 认证流程 (Authentication Flows & Sequence Diagrams)

### 3.1 V2 模式全链路自动化认证流程 (401 质询 + 2-Step 令牌交换)
1. **阶段一：401 质询与自动发现 (RFC 6750 & RFC 9728 & RFC 8414)**
   - 客户端匿名请求 `GET /v2/mcp`，MCP Server 中间件拦截并返回 `401 Unauthorized`；
   - `WWW-Authenticate` 响应头提供 `resource_metadata="http://localhost:8080/.well-known/oauth-protected-resource"`；
   - 客户端请求 `GET /.well-known/oauth-protected-resource` 获取受信任授权服务器 (`http://localhost:9777`)；
   - 客户端请求 `GET /.well-known/oauth-authorization-server` 获取动态注册端点 (`/oauth/register`)。
2. **阶段二：DCR 动态客户端注册与免确认授权 (RFC 7591 DCR)**
   - 客户端发送 `POST /oauth/register`，授权中心首先校验来源 IP/Origin 处于 `allowed-origins` 白名单中；
   - 授权中心根据 `client_name` 进行数据库去重；
   - 授权中心生成 `client_id` 并自动返回 `auto_approve: true` 以及默认注入的 scope 和受众 `erp-sys-auth`；
   - 客户端重定向跳转企业 SSO 完成用户认证，系统免跳过 Consent 页面直接返回授权 Code；
   - 客户端发起 `/oauth/token` 换取 `mcp_token`（JWT 编码包含 `aud: "erp-sys-auth"` 和 `scope: ["read", "write", "openid", "mcp"]`）。
3. **阶段三：建连与 Session 凭证绑定**
   - 客户端带 `Authorization: Bearer <mcp_token>` 请求 `POST /v2/mcp`；
   - MCP Server 中间件捕获 Token 并将其绑定至 Session 字典，同时将 Request Path 透明重写为 `/mcp` 交由 FastMCP 业务层处理。
4. **阶段四：工具调用与 2-Step Token Exchange 访问 API**
   - Agent 发起工具调用（如 `get_user_info`）；
   - **Step 1**：MCP Server 带着 `mcp_token` 请求 `POST /auth/token/exchange`，授权中心在 Redis DB 2 生成短效 Agent ID Token 并返回 `{"token": "2df0c69d-..."}` (`subject_token`)；
   - **Step 2**：MCP Server 请求 `POST /auth/oauth/token` (`grant_type=urn:ietf:params:oauth:grant-type:token-exchange` & `subject_token=2df0c69d-...`)，授权中心校验通过后颁发真正的下游 API `access_token`；
   - **API 请求**：MCP Server 携带 `Authorization: Bearer <access_token>` 及 `X-ID-Token: <access_token>` 调用后端 API，成功获取业务数据并返回 Agent。

### 3.2 V1 模式直传透传流程 (Legacy Direct Mode)
1. **直连建连**：客户端直接发起 `POST /mcp`，在 Header 中直传 `X-ID-Token: <id_token>`。MCP Server 无质询直接建连。
2. **优化 Step 2 交换**：工具调用时，MCP Server 识别到 Header 中已存在直传的 `X-ID-Token`（该 Token 即为 `subject_token`），因此**【跳过 Step 1】**，直接带着该 Token 发起 Step 2 (`POST /auth/oauth/token` `grant_type=token-exchange`) 换取下游 `access_token`。
3. **API 请求**：拿着换取的 `access_token` 调用后端 API。

### 3.3 端到端交互 Sequence Diagram (Mermaid)

```mermaid
sequenceDiagram
    autonumber
    participant Agent as Agent 客户端 (WorkBuddy / Kiro)
    participant MCP as MCP Server (/v2/mcp & /mcp)
    participant AS as 授权中心 (system-auth-center)
    participant API as 后端网关 / 业务微服务 API

    rect rgb(240, 248, 255)
    Note over Agent, MCP: 阶段一：自动发现与 401 质询 (V2 模式)
    Agent->>MCP: 1. GET /v2/mcp (匿名首次请求)
    MCP-->>Agent: 2. 401 Unauthorized<br/>Header: WWW-Authenticate: Bearer resource_metadata=".../.well-known/oauth-protected-resource"
    
    Agent->>MCP: 3. GET /.well-known/oauth-protected-resource (RFC 9728)
    MCP-->>Agent: 4. 200 OK { resource: "http://localhost:8080/v2/mcp", authorization_servers: ["http://localhost:9777"] }

    Agent->>AS: 5. GET /.well-known/oauth-authorization-server (RFC 8414)
    AS-->>Agent: 6. 200 OK { registration_endpoint: "http://localhost:9777/oauth/register", code_challenge_methods_supported: ["S256"] }
    end

    rect rgb(255, 250, 240)
    Note over Agent, AS: 阶段二：动态客户端注册与免确认授权 (RFC 7591 DCR)
    Agent->>AS: 7. POST /oauth/register { client_name: "WorkBuddy Agent", redirect_uris: ["http://127.0.0.1:18888/callback"] }
    AS->>AS: 校验来源与 client_name 去重，设置 autoApproveScopes=["true"]
    AS-->>Agent: 8. 201 Created { client_id: "dcr_a90aa7b944d84877", auto_approve: true }

    Agent->>AS: 9. GET /oauth/authorize ?client_id=dcr_a90aa7b944d84877 &resource=erp-sys-auth &code_challenge=...
    AS->>AS: 校验 resource (oauth_resource_detail 表 status=1)
    AS-->>Agent: 10. 用户 SSO 登录完成，免确认自动重定向至 http://127.0.0.1:18888/callback?code=AUTH_CODE

    Agent->>AS: 11. POST /oauth/token (code_verifier + code + client_id)
    AS-->>Agent: 12. 返回 mcp_token (JWT 包含 scope: read, write, openid, mcp; aud: erp-sys-auth)
    end

    rect rgb(245, 255, 250)
    Note over Agent, API: 阶段三：建连与 2-Step 令牌交换工具调用
    Agent->>MCP: 13. POST /v2/mcp (Header: Authorization: Bearer <mcp_token>)
    MCP->>MCP: AuthChallengeMiddleware 绑定 mcp_token 至 Session，透明重写路径为 /mcp

    Agent->>MCP: 14. 发起 Tool Call (如 get_user_info)
    
    alt V2 模式 (Session 持有 mcp_token)
        MCP->>AS: 15a. Step 1: POST /auth/token/exchange (Header: Authorization: Bearer <mcp_token>)
        AS-->>MCP: 16a. 返回 Agent ID Token (token: "2df0c69d-...") [subject_token]
        MCP->>AS: 17a. Step 2: POST /auth/oauth/token (data: grant_type=token-exchange & subject_token=2df0c69d-...)
        AS-->>MCP: 18a. 返回下游访问令牌 (access_token: "eyJhbGci...")
    else V1 模式 (Header 直传 X-ID-Token)
        MCP->>AS: 15b. 跳过 Step 1，直接执行 Step 2: POST /auth/oauth/token (data: grant_type=token-exchange & subject_token=<X-ID-Token>)
        AS-->>MCP: 16b. 返回下游访问令牌 (access_token: "eyJhbGci...")
    end

    MCP->>API: 19. POST /account/eco/getUserInfo (Header: Authorization: Bearer <access_token>, X-ID-Token: <access_token>)
    API-->>MCP: 20. 返回人员数据响应
    MCP-->>Agent: 21. 返回格式化结果给 Agent
    end
```

---

## 4. MCP方案 (MCP Server Scheme & V1/V2 Endpoints & mcp.json)

### 4.1 MCP Server 端点设计
1. **`/v2/mcp` 端点 (OAuth2 质询端点)**：
   - 入口中间件 `AuthChallengeMiddleware` 仅拦截 `/v2/mcp`；
   - 无 Bearer 凭证时返回 HTTP 401 质询，指导 Agent 客户端通过 RFC 9728 元数据发起 DCR 注册与 SSO 登录；
   - 凭证验证通过后，将 `mcp_token` 绑定至 `session_store`，并透明重写 Request Path `scope["path"]` 为 `/mcp`，由 FastMCP 路由透明处理。
2. **`/mcp` 端点 (无质询直连端点)**：
   - 允许匿名建连与传统直传 `X-ID-Token`；
   - 工具调用时检测到 `X-ID-Token`，自动跳过 Step 1 走 Step 2 换取 Access Token。

### 4.2 客户端配置规范 (`mcp.json`)

#### V2 模式配置 (推荐智能 Agent 自动 401 质询连入)
```json
{
  "mcpServers": {
    "eco-mcp-server-v2": {
      "type": "http",
      "url": "http://localhost:8080/v2/mcp",
      "disabled": false
    }
  }
}
```

#### V1 模式配置 (直传 Header 模式)
```json
{
  "mcpServers": {
    "eco-mcp-server-v1": {
      "type": "http",
      "url": "http://localhost:8080/mcp",
      "headers": {
        "X-ID-Token": "YOUR_SUBJECT_ID_TOKEN_HERE"
      },
      "disabled": false
    }
  }
}
```

---

## 5. 改动点 (Engineering Modification List & Bug Fixes)

### 5.1 授权中心 (`system-auth-center`) 改动点
1. **`application.yml` (配置解耦)**：
   - 增加 `mcp.auth.dcr.enabled: true`；
   - 增加 `mcp.auth.dcr.default-scopes: [read, write, openid, mcp]` 和 `default-resource: erp-sys-auth`；
   - 增加 `mcp.auth.dcr.allowed-origins: ["*"]` 可配置来源白名单规则。
2. **`DcrProperties.java` (配置属性 Bean)**：
   - 映射 `mcp.auth.dcr` 属性项，包含 `enabled`、`defaultScopes`、`defaultResource` 和 `allowedOrigins`。
3. **`DcrClientRegistrationController.java` (DCR 注册控制器)**：
   - 增加 DCR 服务全局开关校验（禁用返回 HTTP 403 `dcr_disabled`）；
   - 增加来源校验 `isOriginAllowed(request)`（未匹配返回 HTTP 403 `unauthorized_origin`）；
   - 保持 `resource_ids = NULL` 强制走 Gate 1 校验；
   - 恢复保存 `registeredRedirectUri`，并在复用客户端时合并更新最新地址；
   - 增加 `clientDetails.setAutoApproveScopes(Collections.singleton("true"))` 实现免确认页面自动授权。
4. **`CustomOAuth2RequestFactory.java` (OAuth2 请求工厂)**：
   - 在 `createAuthorizationRequest` 与 `createOAuth2Request` 阶段自动合并 `defaultScopes`；
   - 自动追加 `defaultResource` (`erp-sys-auth`) 至 Resource 清单；
   - 允许 `erp-sys-auth` 格式的资源 URI 校验。
5. **`EccomJwtAccessTokenEnhancer.java` (JWT 令牌增强器)**：
   - 在 `enhance()` 中同步 `OAuth2Request` 的作用域至 `DefaultOAuth2AccessToken`，确保生成的 JWT 包含 `"scope": ["read", "write", "openid", "mcp"]`。

### 5.2 MCP 服务 (`eco-mcp-server`) 改动点
1. **`config.py`**：
   - 定义 `MCP_PATH = "/mcp"`、`MCP_V2_PATH = "/v2/mcp"` 与 `RESOURCE_ID = "http://localhost:8080/v2/mcp"`。
2. **`main.py`**：
   - `AuthChallengeMiddleware` 仅拦截 `/v2/mcp` 质询并透明重写路径为 `/mcp`；
   - 暴露 `GET /.well-known/oauth-protected-resource` 端点。
3. **`session_store.py`**：
   - 提供 `save_session_credentials` 与 `get_session_credentials` 内存凭证字典与智能回退继承逻辑。
4. **`api/eccom_base_client.py`**：
   - `_extract_credentials()` 识别 `x-id-token` (`direct_id_token`) 与 Session `mcp_token` (`direct_bearer`)；
   - `_get_auth_headers()` 支持 `direct_id_token` 跳过 Step 1 直奔 Step 2，与 `direct_bearer` 走完整 2-Step；
   - 补充 `from typing import Optional, Dict, Tuple` 修复 `NameError: name 'Dict' is not defined`。
5. **`api/eccom_gateway_client.py` & `api/eccom_wwwin_client.py`**：
   - 修复子类 `_make_request()` 调用废弃 `_exchange_token()` 导致的 `AttributeError`，统一重构为使用 `await self._get_auth_headers()`。

---

## 6. 总结

本方案在保持系统强壮性、安全解耦与高拓展性的前提下，成功实现了：
1. **现实接入全兼容与来源可控**：通过 **RFC 7591 DCR** 与 **`autoApprove = true`** 完美满足 WorkBuddy、Kiro、LobeHub、Cursor 等 Agent 的动态注册及静默登录需求，同时支持 `allowed-origins` 来源控制保障服务安全。
2. **渐进式双端点支持**：`/v2/mcp` 端点提供标准的 RFC 6750 401 质询与完整 2-Step 令牌交换；`/mcp` 端点提供无质询直连且跳过 Step 1 直奔 Step 2 的性能优化路径。
3. **受众防护与防数据库膨胀**：通过 `client_name` 去重控制存储开销，结合 `oauth_resource_detail` (Gate 1 资源开放表) 与 `erp-sys-auth` 默认受众追加，精准管控受保护 API 资源。
4. **保留未来演进**：保留 **CIMD Draft** 抓取能力，后续当 Agent 生态全面普及去中心化 CIMD 时，授权中心与 MCP 服务端无需进行二次代码修改即可直接接入。
