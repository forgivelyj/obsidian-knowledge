---
title: "企业级 MCP 服务端 K8s 统一治理方案 (Agentgateway 版)"
aliases: ["Enterprise MCP K8s Management", "Agentgateway MCP Governance"]
tags: ["#ai", "#software-engineering", "#tool", "#active"]
category: synthesis
created: 2026-08-20
updated: 2026-08-21
sources: 
  - "[[wiki/synthesis/lobehub-mcp-auth-solution.md]]"
description: "基于 AI Agent 专用网关 (agentgateway.dev) 的企业级 MCP 服务端统一接入、401 动态质询、RFC 8693 Token Exchange 换票与生命周期治理方案"
---

# 企业级 MCP 服务端 K8s 统一治理与生产部署方案 (AI Agent 专用网关版)

本文档定义了企业内部基于 **AI Agent 专用网关 (`agentgateway.dev`)** 构建的 MCP 服务端统一治理架构与端到端实战部署指南。

---

## 1. 核心架构设计

```
[ AI 客户端: Cursor / Windsurf / Claude Desktop ]
                       │
                       │ 1. HTTP/SSE 请求 (统一入口)
                       ▼
            [ Ingress-NGINX (边界网关) ]
                       │
                       │ 2. 反向代理到网关服务 (mcp-gateway)
                       ▼
       ┌───────────────────────────────────────────────────────────┐
       │     AI Agent 专用网关 (agentgateway.dev / Rust 内核)      │
       │                                                           │
       │  • 统一 401 质询与 Metadata (RFC 6750 / 9728)             │
       │  • 统一 JWKS 验签 (http://api-staging.../getJkwsKey)      │
       │  • 原生 RFC 8693 Token Exchange 自动换票                  │
       │  • MCP 工具动态发现与标签聚合 (mcp.eccom.com/mcp-tool)     │
       │  • SSE 实时推送与工具定义热更新                           │
       └─────────────────────────────┬─────────────────────────────┘
                                     │
                 3. 携带已换票的专属 Bearer Token 转发
                                     │
       ┌─────────────────────────────┼─────────────────────────────┐
       ▼                             ▼                             ▼
 [ Jira MCP Pod ]            [ GitLab MCP Pod ]            [ CMDB MCP Pod ]
 (mcp-tool: enabled)         (mcp-tool: enabled)         (mcp-tool: enabled)
```

---

## 2. 关键环境与配置参数 (ECCOM)

| 配置项 | 实际环境取值 |
| :--- | :--- |
| **K8s 命名空间** | `mcp-system` |
| **网关公开访问域名** | `http://mcp-gateway.cloud.lab.eccom.com.cn` |
| **OAuth 401 Metadata 端点** | `http://mcp-gateway.cloud.lab.eccom.com.cn/.well-known/oauth-protected-resource` |
| **企业 IdP 授权地址** | `http://api-staging.eccom.com.cn/api/auth/oauth/authorize` |
| **企业 IdP JWKS 公钥地址** | `http://api-staging.eccom.com.cn/api/auth/oidc/getJkwsKey` |
| **企业 IdP Token 换票端点** | `http://api-staging.eccom.com.cn/api/auth/oauth/token` |
| **网关客户端 ID** | `mcp-gateway` |
| **目标 MCP 受众模板** | `http://mcp.cloud.lab.eccom.com.cn/{service_name}` |
| **MCP 工具自动发现标签** | `mcp.eccom.com/mcp-tool: "enabled"` |

---

## 3. 分步骤部署实战操作

### 步骤 1：清理旧通用网关资源 (如有)
```bash
kubectl delete trafficpolicy,gatewayextension,backend,routeoption --all -n mcp-system --ignore-not-found
helm uninstall kgateway kgateway-crds -n mcp-system --ignore-not-found
```

---

### 步骤 2：安装 Gateway API 与 Agentgateway 官方 CRDs

```bash
# 1. 安装标准 Gateway API CRDs (v1.6.1)
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.6.1/standard-install.yaml

# 2. 安装 AI Agent 专用网关 CRDs
helm upgrade -i agentgateway-crds oci://cr.agentgateway.dev/charts/agentgateway-crds \
  --namespace mcp-system \
  --create-namespace
```

---

### 步骤 3：安装 Agentgateway 控制面

```bash
helm upgrade -i agentgateway oci://cr.agentgateway.dev/charts/agentgateway \
  --namespace mcp-system
```

---

### 步骤 4：创建 IdP Client Secret

```bash
kubectl create secret generic mcp-idp-secret \
  --namespace mcp-system \
  --from-literal=client-secret="YOUR_ACTUAL_CLIENT_SECRET" \
  --dry-run=client -o yaml | kubectl apply -f -
```

---

### 步骤 5：部署 Agentgateway 全局统一鉴权与换票策略 (`mcp-agentgateway.yaml`)

```yaml
apiVersion: agentgateway.dev/v1alpha1
kind: AgentgatewayBackend
metadata:
  name: enterprise-mcp-federation
  namespace: mcp-system
spec:
  # 1. 统一 401 质询与 JWKS 验签 (RFC 6750 / 9728)
  authChallenge:
    enabled: true
    resourceMetadata: "http://mcp-gateway.cloud.lab.eccom.com.cn/.well-known/oauth-protected-resource"
    authorizationUri: "http://api-staging.eccom.com.cn/api/auth/oauth/authorize"
    jwksUrl: "http://api-staging.eccom.com.cn/api/auth/oidc/getJkwsKey"

  # 2. 原生 RFC 8693 委托换票 (Token Exchange)
  tokenExchange:
    enabled: true
    tokenEndpoint: "http://api-staging.eccom.com.cn/api/auth/oauth/token"
    clientId: "mcp-gateway"
    clientSecretRef:
      name: mcp-idp-secret
      key: client-secret
    audienceFormat: "http://mcp.cloud.lab.eccom.com.cn/{service_name}"

  # 3. 标签自动汇聚选择器 (自动发现打上标签的 MCP Pod)
  selector:
    matchLabels:
      mcp.eccom.com/mcp-tool: "enabled"
```

```bash
kubectl apply -f mcp-agentgateway.yaml
```

---

### 步骤 6：配置 Ingress-NGINX 边界路由 (`mcp-ingress.yaml`)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-to-mcp
  namespace: mcp-system
  annotations:
    kubernetes.io/ingress.class: "nginx"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "3600"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "3600"
    nginx.ingress.kubernetes.io/proxy-buffering: "off"
    nginx.ingress.kubernetes.io/proxy-http-version: "1.1"
spec:
  rules:
    - host: mcp-gateway.cloud.lab.eccom.com.cn
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: mcp-gateway
                port:
                  number: 80
```

```bash
kubectl apply -f mcp-ingress.yaml
```

---

### 步骤 7：下游业务微服务标准化接入示例

业务系统接入企业网关支持两种标准接入范式：**原生 MCP 微服务**与**传统 OpenAPI / Swagger REST 微服务**。

#### 7.1 原生 MCP 微服务打标接入示例
任何原生 MCP 服务的 Pod / Service 只需带上标签 `agentgateway.dev/mcp-server: enabled`（或历史 `mcp.eccom.com/mcp-tool: "enabled"`），网关便会自动发现该服务：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jira-mcp-server
  namespace: mcp-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: jira-mcp-server
  template:
    metadata:
      labels:
        app: jira-mcp-server
    spec:
      containers:
        - name: mcp-server
          image: harbor.is.eccom.com.cn/eccom-public/eccom/jira-mcp:latest
          ports:
            - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: jira-mcp-server
  namespace: mcp-system
  labels:
    agentgateway.dev/mcp-server: enabled
  annotations:
    agentgateway.dev/display-name: "Jira敏捷项目管理系统"
    agentgateway.dev/capabilities: "事务卡片查询,缺陷提报,迭代Sprint进度查看"
spec:
  ports:
    - name: mcp
      port: 8000
      appProtocol: agentgateway.dev/mcp
  selector:
    app: jira-mcp-server
```

---

#### 7.2 传统 OpenAPI / Swagger REST 微服务标准化接入（OpenAPI Bridge 范式）
对于已有或新开发的 RESTful 微服务（Spring Boot、Go、Python 等），直接复用网关同款开源镜像 `agentgateway:v1.5.0`，部署轻量桥接 Pod，实现零代码自动将 OpenAPI 转换为 MCP 工具：

##### 1. 标准化生产通用模板 (`<service-name>-mcp.yaml`)
```yaml
# 1. 协议转换规则（支持热重载，修改无需重启 Pod）
apiVersion: v1
kind: ConfigMap
metadata:
  name: <SERVICE_NAME>-mcp-bridge-config
  namespace: <TARGET_NAMESPACE>
data:
  config.yaml: |
    proxyMetadata:
      nodeId: "agentgateway~1.1.1.1~.~.svc.cluster.local"
    # 可选：若后端微服务要求固定机机服务 Token (Machine-to-Machine)，在此开启自动注入
    # policies:
    #   transformation:
    #     request:
    #       set:
    #         - name: "Authorization"
    #           value: "'Bearer <企业固定的服务级AppToken>'"
    mcp:
      targets:
        - name: <SERVICE_NAME>
          openapi:
            # 业务服务实际访问根路径（协议转换后的 REST 请求将拼接到该地址）
            host: "<SERVICE_BASE_URL>"
            # 业务 OpenAPI / Swagger v3 JSON 文档地址
            spec: "<OPENAPI_SPEC_URL>"
---
# 2. 运行时工作负载（固定模版，通用 agentgateway 镜像）
apiVersion: apps/v1
kind: Deployment
metadata:
  name: <SERVICE_NAME>-mcp-bridge
  namespace: <TARGET_NAMESPACE>
spec:
  replicas: 1
  selector:
    matchLabels:
      app: <SERVICE_NAME>-mcp-bridge
  template:
    metadata:
      labels:
        app: <SERVICE_NAME>-mcp-bridge
    spec:
      containers:
        - name: agentgateway
          image: harbor.is.eccom.com.cn/eccom-public/eccom/agentgateway:v1.5.0
          args: ["-f", "/config/config.yaml"]
          ports:
            - containerPort: 8080
          resources:
            limits:
              cpu: "500m"
              memory: 512Mi
            requests:
              cpu: "50m"
              memory: 64Mi
          volumeMounts:
            - name: config-volume
              mountPath: /config
      volumes:
        - name: config-volume
          configMap:
            name: <SERVICE_NAME>-mcp-bridge-config
---
# 3. 网关感知与能力声明（打标即上线，摘标即下线）
apiVersion: v1
kind: Service
metadata:
  name: <SERVICE_NAME>-mcp-bridge
  namespace: <TARGET_NAMESPACE>
  labels:
    # 【必须】：让 ai-gateway 主网关控制器动态发现并将其吸纳到 /mcp 聚合池
    agentgateway.dev/mcp-server: enabled
  annotations:
    # 【必须】：为 ExtProc 动态感知引擎提供友好的业务中文名称，供大模型识别
    agentgateway.dev/display-name: "<业务中文展示名，例如：华讯OA协同办公>"
    # 【必须】：为 ExtProc 动态感知引擎提供能力标签列表，逗号分隔，实时注入 get_tool 提示词
    agentgateway.dev/capabilities: "<核心能力1,核心能力2,核心能力3>"
spec:
  ports:
    - name: mcp
      port: 8080
      targetPort: 8080
      appProtocol: agentgateway.dev/mcp
  selector:
    app: <SERVICE_NAME>-mcp-bridge
```

##### 2. 生产实战落地样例：华讯 HR 员工假期服务 (`hr-vacation-mcp-bridge.yaml`)
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: hr-vacation-mcp-bridge-config
  namespace: app0129-wwwin-mcp
data:
  config.yaml: |
    proxyMetadata:
      nodeId: "agentgateway~1.1.1.1~.~.svc.cluster.local"
    mcp:
      targets:
        - name: hr-vacation-api
          openapi:
            host: "http://gateway.cloud.lab.eccom.com.cn/api/hr/oa/vacation"
            spec: "http://gateway.cloud.lab.eccom.com.cn/api/hr/oa/vacation/v3/api-docs"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hr-vacation-mcp-bridge
  namespace: app0129-wwwin-mcp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hr-vacation-mcp-bridge
  template:
    metadata:
      labels:
        app: hr-vacation-mcp-bridge
    spec:
      containers:
        - name: agentgateway
          image: harbor.is.eccom.com.cn/eccom-public/eccom/agentgateway:v1.5.0
          args: ["-f", "/config/config.yaml"]
          ports:
            - containerPort: 8080
          resources:
            limits:
              cpu: 500m
              memory: 512Mi
            requests:
              cpu: 50m
              memory: 64Mi
          volumeMounts:
            - name: config-volume
              mountPath: /config
      volumes:
        - name: config-volume
          configMap:
            name: hr-vacation-mcp-bridge-config
---
apiVersion: v1
kind: Service
metadata:
  name: hr-vacation-mcp-bridge
  namespace: app0129-wwwin-mcp
  labels:
    agentgateway.dev/mcp-server: enabled
  annotations:
    agentgateway.dev/display-name: "华讯HR员工假期服务"
    agentgateway.dev/capabilities: "员工休假明细查询,假期余额汇总统计,请假核销"
spec:
  ports:
    - name: mcp
      port: 8080
      targetPort: 8080
      appProtocol: agentgateway.dev/mcp
  selector:
    app: hr-vacation-mcp-bridge
```

---

### 步骤 8：Token 鉴权与全链路自动透传机制

1. **动态用户态 Token 透传**：
   - 客户端建立连接时携带 `Authorization: Bearer <user_token>`；
   - ExtProc 插件拦截后将 Token 与 `mcp-session-id` 进行绑定；
   - 后续大模型调用 `get_tool` 或 `invoke_tool` 时，ExtProc 自动回填 `Authorization` 头；
   - Agentgateway OpenAPI 转换引擎在将 `tools/call` 转为 HTTP REST 请求时，**100% 自动透传该 Authorization 请求头**至下游实际业务 API。
2. **固定系统级 Token 注入**：
   - 若后端微服务需要固定密钥，直接在 ConfigMap 中的 `policies.transformation.request.set` 配置，对前端模型完全透明。

---

### 步骤 9：运维验证与健康检查门禁

| 检查项 | 验证命令 | 预期正常结果 |
| :--- | :--- | :--- |
| **网关策略就绪** | `kubectl get agentgatewaypolicies -n agentgateway-system` | `ACCEPTED: True`, `ATTACHED: True` |
| **服务动态感知** | 查看插件日志 `kubectl logs deployment/mcp-tool-search-plugin -n agentgateway-system` | 出现 `[K8s 动态感知] 微服务实时就绪: [华讯HR员工假期服务]` |
| **工具折叠生效** | 客户端执行 `tools/list` | 严格仅展示 `get_tool` 与 `invoke_tool` 2 个元工具 |
| **意图检索调用** | 大模型调用 `get_tool(query="休假")` | 毫秒级返回结构化休假参数 JSON Schema |
| **业务执行与透传** | 大模型调用 `invoke_tool` 触发微服务 | 真实后端返回 HTTP 200 OK，成功识别调用者身份 |


