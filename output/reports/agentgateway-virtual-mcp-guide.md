# 企业级 Agentgateway 虚拟 MCP 聚合与动态服务发现架构指南

---

## 1. 架构愿景与核心价值

在企业 AI Agent 规模化落地过程中，随着业务微服务（REST API / 原生 MCP）的不断增加，传统“人工硬编码工具配置”会导致网关配置臃肿、运维频繁重启、大模型上下文（Context Window）爆炸。

本方案基于 **Agentgateway + Envoy ExtProc + Kubernetes 原生服务发现**，构建了 **“零配置动态聚合（Zero-Configuration Aggregation）+ 渐进式检索披露（Progressive Disclosure）+ 全链路 OAuth 零信任透传”** 的企业级虚拟 MCP 网关架构。

```text
                                       ┌──────────────────────────────────────────────────┐
                                       │ 客户端：Cursor / Claude / 企业自研 AI Agent     │
                                       └────────────────────────┬─────────────────────────┘
                                                                │ (MCP Streamable HTTP + OAuth Token)
                                                                ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Agentgateway 虚拟 MCP 统一接入层 (http://gateway-ai.eccom.com.cn/virtual-mcp)                                          │
│                                                                                                                        │
│  1. 【严格 JWT 鉴权与会话管理】      2. 【ExtProc 渐进式元工具插件】         3. 【Token 会话记忆与自动透传 (Hydration)】│
│     - OAuth2 / OIDC 严格校验            - 全量工具折叠为 2 个元工具             - 拦截 Request Headers 自动回填 Token    │
│     - 401 质询与 Session 绑定           - get_tool (分词加权精准检索)           - 剥离 Content-Length 防止 HTTP 挂起     │
│     - Target / 路由级 CEL RBAC 分权     - invoke_tool (透明解包并执行)          - 100% 保持终端用户原始身份上下文        │
└───────────────────────────────────────────────────────┬────────────────────────────────────────────────────────────────┘
                                                        │ (动态路由与多源聚合)
                                                        ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Kubernetes 原生动态服务发现池 (Selector: agentgateway.dev/mcp-server: enabled)                                         │
│                                                                                                                        │
│  ┌──────────────────────────────┐    ┌──────────────────────────────┐    ┌──────────────────────────────────────────┐  │
│  │ 业务微服务 A (原生 MCP)      │    │ 业务微服务 B (OpenAPI 桥接)  │    │ 跨网关 / 跨集群外部系统 C (REST/MCP)     │  │
│  │ - 用户中心 / 权限微服务       │    │ - 订单管理 SpringBoot 微服务 │    │ - 外部 ERP / 审批系统 Gateway            │  │
│  │ - 贴标签即自动秒级发现生效   │    │ - 自动读取 Swagger 转换为工具│    │ - static.host 跨域打通与 API Key 注入    │  │
│  └──────────────────────────────┘    └──────────────────────────────┘    └──────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. 核心机制深度解析

### 2.1 零配置动态服务发现 (Zero-Configuration Discovery)
* **一次性配置**：网关底座仅配置一条通配 `LabelSelector`（`agentgateway.dev/mcp-server: enabled`），**网关 YAML 部署后永久无需修改**。
* **即插即用**：任何业务团队上线新微服务时，只需在自身的 `Service` 声明中打上标签，Agentgateway 控制面（Controller）通过 K8s Watch 机制在 **1 秒内自动热加载** 该服务下的全部工具并向前端 Agent 暴露。

### 2.2 渐进式披露元工具契约 (Progressive Disclosure)
* **告别 Context 爆炸**：下游哪怕接入了 1,000 个业务工具，网关在 `tools/list` 阶段通过 ExtProc 插件将其折叠为 **2 个标准元工具**：
  * **`get_tool`**：基于多关键词重叠加权打分算法（支持长句模糊搜索），按需返回匹配工具的精确 JSON Schema；
  * **`invoke_tool`**：大模型根据 Schema 组装参数后发起执行，插件自动透明解包并打入目标真实微服务。

### 2.3 OAuth 2.0 凭证会话记忆与全链路透传 (Token Hydration)
* **解决协议矛盾**：MCP 客户端在初次握手后，后续发送 `tools/call` 时默认不重复带 Token；但后端零信任微服务每一个请求都必须校验 Token。
* **毫秒级回填**：ExtProc 插件利用 `Mcp-Session-Id` 建立高并发安全缓存（带 `asyncio.Lock` 与 TTL 自动过期机制），在请求进入后端前**动态注入 `Authorization: Bearer <Token>` 并移除旧的 `Content-Length`**，实现后端 0 改造、0 报错、100% 鉴权通行。

---

## 3. 标准落地部署清单 (YAML 模板)

### 步骤一：部署 ExtProc 渐进式披露与 Token 回填插件

#### `1-mcp-plugin-workload.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-tool-search-plugin
  namespace: agentgateway-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mcp-tool-search-plugin
  template:
    metadata:
      labels:
        app: mcp-tool-search-plugin
    spec:
      containers:
        - name: plugin
          image: harbor.cloud.lab.eccom.com.cn/ai-infra/mcp-tool-search-plugin:v2.1
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 9002
          resources:
            limits:
              cpu: "1"
              memory: 1Gi
            requests:
              cpu: "100m"
              memory: 128Mi
---
apiVersion: v1
kind: Service
metadata:
  name: mcp-tool-search-plugin
  namespace: agentgateway-system
spec:
  ports:
    - name: grpc
      port: 9002
      targetPort: 9002
  selector:
    app: mcp-tool-search-plugin
```

---

### 步骤二：配置统一网关聚合后端与路由（一次性配置）

#### `2-virtual-mcp-gateway.yaml`
```yaml
# 1. 虚拟 MCP 聚合后端 (支持集群内动态发现 + 跨网关目标)
apiVersion: agentgateway.dev/v1alpha1
kind: AgentgatewayBackend
metadata:
  name: virtual-company-backend
  namespace: agentgateway-system
spec:
  mcp:
    failureMode: FailOpen         # 某服务故障时自动降级隔离，不影响全局
    prefixMode: Conditional       # 自动以服务名为命名空间前缀，防重名冲突
    sessionRouting: Stateful      # 保持有状态会话路由
    targets:
      # A. 集群内所有动态微服务 (贴标签自动吸纳)
      - name: dynamic-cluster-apis
        selector:
          agentgateway.dev/mcp-server: enabled

      # B. 跨网关 / 跨集群外部系统 (静态打通)
      - name: cross-gw-erp-api
        static:
          host: "erp-gateway.cloud.lab.eccom.com.cn"
          port: 443
          path: "/remote-mcp"
          protocol: StreamableHTTP
          policies:
            headerModifiers:
              request:
                set:
                  - name: "x-gateway-source"
                    value: "ai-infra-gateway"

---
# 2. 路由分发 (基于 Header 区分初次握手与已建会话调用)
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: virtual-company-route
  namespace: agentgateway-system
spec:
  parentRefs:
    - group: gateway.networking.k8s.io
      kind: Gateway
      name: ai-gateway
      sectionName: http-ai
  rules:
    # 规则 1：已建立 Session 的后续工具调用 (直接放行，由插件回填 Token)
    - name: established-session
      matches:
        - path:
            type: PathPrefix
            value: /virtual-mcp
          headers:
            - name: mcp-session-id
              value: ".*"
              type: RegularExpression
      backendRefs:
        - group: agentgateway.dev
          kind: AgentgatewayBackend
          name: virtual-company-backend

    # 规则 2：初次握手建连 (执行严格 JWT 鉴权与 401 质询)
    - name: initial-handshake
      matches:
        - path:
            type: PathPrefix
            value: /virtual-mcp
        - path:
            type: PathPrefix
            value: /.well-known/oauth-protected-resource/virtual-mcp
      backendRefs:
        - group: agentgateway.dev
          kind: AgentgatewayBackend
          name: virtual-company-backend

---
# 3. 统一流量治理策略 (JWT 鉴权 + 插件挂载)
apiVersion: agentgateway.dev/v1alpha1
kind: AgentgatewayPolicy
metadata:
  name: virtual-mcp-policy
  namespace: agentgateway-system
spec:
  targetRefs:
    - group: gateway.networking.k8s.io
      kind: HTTPRoute
      name: virtual-company-route
  traffic:
    # 严格 JWT 鉴权 (仅在初次握手拦截)
    jwtAuthentication:
      mode: Strict
      providers:
        - audiences:
            - "http://gateway-ai.cloud.lab.eccom.com.cn/virtual-mcp"
          issuer: "https://api-staging.eccom.com.cn/api/auth/oidc"
          jwks:
            remote:
              jwksPath: "/oidc/getJkwsKey"
              cacheDuration: 5m
              backendRef:
                kind: Service
                name: system-auth-center
                namespace: app40-ecoauth
                port: 8080
      mcp:
        resourceMetadata:
          resource: "http://gateway-ai.cloud.lab.eccom.com.cn/virtual-mcp"
          scopesSupported: ["openid", "mcp", "read", "write"]
          bearerMethodsSupported: ["header"]

    # 挂载 ExtProc 插件实现折叠、检索与 Token 动态注入
    extProc:
      backendRef:
        name: mcp-tool-search-plugin
        port: 9002
      failureMode: FailOpen
      processingOptions:
        allowModeOverride: false
        requestBodyMode: Buffered
        responseBodyMode: Buffered
        requestHeaderMode: Send
        responseHeaderMode: Send
        requestTrailerMode: Skip
        responseTrailerMode: Skip
```

---

### 步骤三：业务微服务接入规范（业务方视角）

以后任何业务系统接入虚拟 MCP 空间，只需遵循以下接入规范：

#### 场景 1：原生 MCP 微服务接入（如 Python FastMCP / Go MCP）
只需在微服务自身的 `Service` 定义中添加 **1 个 Label 和 1 个 appProtocol**：
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-biz-mcp-service
  namespace: app-biz
  labels:
    agentgateway.dev/mcp-server: enabled   # 【必须】：声明加入网关动态池
spec:
  ports:
    - name: mcp
      port: 8080
      targetPort: 8080
      appProtocol: agentgateway.dev/mcp    # 【必须】：声明协议类型
  selector:
    app: my-biz-mcp
```

#### 场景 2：传统 OpenAPI / Swagger REST 微服务标准化接入（OpenAPI Bridge 范式）

对于已有或新开发的 RESTful 微服务（Spring Boot、Go Gin、Python FastAPI 等），无需为了 Agentgateway 专门修改代码开发 MCP Server，通过部署一个轻量级代理 Pod（直接复用网关同款开源镜像 `agentgateway:v1.5.0`，**零外部新镜像**），即可实现自动将 OpenAPI 规范转为标准的 MCP 工具，并自动挂载到网关的 `/mcp` 聚合池中。

##### 1. 标准化生产通用模板 (`<service-name>-mcp.yaml`)

```yaml
# 1. 协议转换规则（支持热修改，API 地址变更不需重启 Pod）
apiVersion: v1
kind: ConfigMap
metadata:
  name: <SERVICE_NAME>-mcp-bridge-config
  namespace: <TARGET_NAMESPACE>
data:
  config.yaml: |
    proxyMetadata:
      nodeId: "agentgateway~1.1.1.1~.~.svc.cluster.local"
    # 可选：如果后端微服务要求固定机机服务 Token (Machine-to-Machine)，在此开启自动注入
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
            # 业务 OpenAPI / Swagger v3 JSON 文档地址（可为集群内 HTTP URL，亦可挂载本地 JSON 文件）
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

---

##### 2. 生产实战落地样例：华讯 HR 员工假期服务 (`hr-vacation-mcp-bridge.yaml`)

以下为生产集群中真实部署并已投入运行的样例配置：

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

##### 3. 核心机制保障与运维特性

1. **自动透传与鉴权凭证回填**：
   * **动态用户态 Token**：大模型端发起调用时，网关的 ExtProc 插件会自动回填终端用户的 `Authorization: Bearer <user_token>`；Agentgateway 的 OpenAPI 引擎会将该请求头**完整透传给后端真实的 REST 接口**，后端服务无缝识别调用者身份。
   * **固定机机 Token**：如接口需要固定服务密钥，可在 ConfigMap 的 `policies.transformation` 统一硬代，无需暴露给前端 Agent。
2. **大模型元数据动态渲染**：
   * Service 注解中的 `agentgateway.dev/display-name` 与 `agentgateway.dev/capabilities` 被 ExtProc 插件动态捕获，直接呈现在大模型的系统 Prompt 中：
     ```text
     • [华讯HR员工假期服务]：涵盖员工休假明细查询、假期余额汇总统计、请假核销等；
     ```
   * 大模型针对员工假期类诉求，将精准通过 `get_tool(query="休假")` 检索，并调起 `getPeopleVacationSum` 等真实工具。
3. **零停机热更新 (Hot Reload)**：
   * 当后端 OpenAPI 规范更新、增加新接口时，仅需更新 ConfigMap，内部 File Watcher 秒级感知并重新拉取接口定义，主网关和业务 Pod 均无需重启。

---

## 4. 细粒度权限控制与分权最佳实践 (RBAC)

Agentgateway 原生支持在 Target 和工具级别进行分权控制：

### 4.1 基于 CEL 表达式的 Target 级授权
若某些核心系统（如财务 ERP、审计系统）仅允许特定角色的用户调用，可以在 `AgentgatewayPolicy` 中针对该 Target 配置 CEL 匹配规则：

```yaml
apiVersion: agentgateway.dev/v1alpha1
kind: AgentgatewayPolicy
metadata:
  name: finance-rbac-policy
  namespace: agentgateway-system
spec:
  targetRefs:
    - group: agentgateway.dev
      kind: AgentgatewayBackend
      name: virtual-company-backend
      sectionName: cross-gw-erp-api  # 仅针对核心 ERP Target 生效
  traffic:
    authorization:
      action: Allow
      policy:
        matchExpressions:
          # 仅允许 JWT 中包含 'finance-admin' 角色且部门为 'finance' 的调用
          - "jwt.claims.roles.exists(r, r in ['finance-admin', 'super-admin'])"
          - "jwt.claims.department == 'finance'"
```

### 4.2 工具级动态权限裁剪 (Tool-Level Masking)
在 ExtProc 插件的 `get_tool` 检索阶段，插件会提取请求中的 JWT Claims，自动过滤掉当前用户无权访问的工具定义，实现**低权限用户在搜索时“连工具名字和 Schema 都看不见”**，从根源杜绝模型幻觉越权调用。

---

## 5. 运维与验证检查表 (Verification Checklist)

| 检查项 | 验证命令 / 指标 | 预期正常结果 |
| :--- | :--- | :--- |
| **网关策略绑定** | `kubectl get agentgatewaypolicy -n agentgateway-system` | `ACCEPTED: True`, `ATTACHED: True` |
| **动态服务感知** | 查看网关日志 `kubectl logs deployment/ai-gateway -n agentgateway-system` | 出现 `Discovered MCP target: ...` |
| **OAuth 握手质询** | `curl -i http://gateway-ai.cloud.lab.eccom.com.cn/virtual-mcp` | 返回 `401 Unauthorized` + `WWW-Authenticate` 头 |
| **工具折叠生效** | 客户端（Cursor）初始化连接 | 工具列表严格只显示 `get_tool` 与 `invoke_tool` 2 个元工具 |
| **意图检索调用** | 大模型调用 `get_tool({"query": "查询员工/订单"})` | 毫秒级返回结构化 JSON Schema 定义与操作指引 |
| **业务执行与透传** | 大模型调用 `invoke_tool` 触发微服务 | 后端微服务日志打印 `200 OK`，成功提取当前用户 JWT 凭证 |
