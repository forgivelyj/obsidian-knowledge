# 企业级 AgentGateway 与 MCP 生产部署及指导文件全景总览 (Master Guide)

**文档版本**：v2.0.0 (生产就绪版)  
**更新日期**：2026-09-15  
**文档密级**：企业内部技术资产  

---

## 1. 方案全景与核心架构

本生产实施方案围绕 **AgentGateway（Rust 数据面 + Kubernetes Gateway API 控制面）** 与 **Envoy ExtProc 智能扩展处理器**，构建了企业级 AI Agent 统一工具网关。

核心解决三大生产痛点：
1. **上下文防爆炸**：通过 ExtProc 将成百上千个底层业务工具动态折叠为 `get_tool` 与 `invoke_tool` 两个元工具，实现“按需精准召回”；
2. **多源协议统一汇聚**：既支持标准 MCP 原生微服务接入，又支持传统 OpenAPI / Swagger RESTful 接口零代码桥接转换为 MCP 工具；
3. **全链路零信任鉴权**：统一 RFC 6750 / RFC 9728 动态 401 质询与本地 JWKS 验签，实现端到端终端用户身份 Token 的自动绑定、透传与回填。

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        AI 客户端 (Cursor / Windsurf / 企业自研 Agent)                   │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ MCP Streamable HTTP / SSE (带 Bearer Token)
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 边界入口层 (Ingress-NGINX: gateway-ai.cloud.lab.eccom.com.cn)                          │
│  - 协议直通，关闭 proxy-buffering                                                      │
│  - 长连接超时加固 (proxy-read/send-timeout: 3600s)                                     │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ AgentGateway 统一控制与数据面 (ai-gateway / Namespace: agentgateway-system)             │
│                                                                                        │
│  ┌───────────────────────────┐ ┌───────────────────────────┐ ┌──────────────────────┐ │
│  │ 严格 JWT 鉴权策略         │ │ 全局动态限流服务          │ │ 动态 MCP 路由分流    │ │
│  │ (3-jwt-auth-policy.yaml)  │ │ (1-ratelimit-service.yaml)│ │ (mcp-route-dynamic)  │ │
│  │ 远程对接认证中心 JWKS     │ │ Redis 二层直连防穿透      │ │ 区分握手与已建会话   │ │
│  └───────────────────────────┘ └───────────────────────────┘ └──────────────────────┘ │
└─────────────────────────────────────┬──────────────────────────────────────────────────┘
                                      │ gRPC (Port: 9002)
                                      ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ ExtProc 元工具自适应插件 (mcp-tool-search-plugin / nodeSelector: com310)                │
│  • Session-User-Token 映射存储与自动注入 Authorization 头                              │
│  • 11➔2 动态自适应工具折叠与分词加权检索算法                                            │
│  • K8s 原生 Service Watcher 监听打标服务，毫秒级下线清理与 503 防穿透拦截              │
└─────────────────────────────────────┬──────────────────────────────────────────────────┘
                                      │ 动态多源后端路由
                                      ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 后端业务微服务池 (Selector: agentgateway.dev/mcp-server: enabled)                      │
│                                                                                        │
│  ┌─────────────────────────────────────────┐  ┌─────────────────────────────────────┐ │
│  │ 范式 A：原生 MCP 微服务 (eco-mcp-server)│  │ 范式 B：OpenAPI 桥接代理 (HR 假期等)│ │
│  │ • 标准 MCP 协议端点 (/v2/mcp)           │  │ • agentgateway 桥接 Pod             │ │
│  │ • 本地 JWKS 验签 + 401 动态质询         │  │ • 自动解析 Swagger v3 JSON 转换为 MCP│ │
│  │ • SessionStore LRU 防爆内存管理         │  │ • 自动将 tools/call 转为 REST POST  │ │
│  └─────────────────────────────────────────┘  └─────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. 四大核心实施与指导文档索引 (Core Guidance Documents)

项目的所有设计、部署、改造与治理规范严格收敛并固化在以下 4 份核心文档中：

| 序号 | 权威文档名称 | 物理文件绝对路径 | 面向角色 | 核心职责与关键指导内容 |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **网关分节点部署手册**<br>`DEPLOYMENT_GUIDE.md` | `D:\workspace\2026\AI 研究\agentgateway_configs\DEPLOYMENT_GUIDE.md` | SRE / 运维工程师 | **【分节点部署实操】**<br>定义生产落地的 **6 大里程碑验证节点**（跨命名空间授权 ➔ Gateway 底座 ➔ ExtProc 插件 ➔ RateLimit 限流 ➔ 动态路由安全策略 ➔ 端到端全链路业务闭环），提供每一步的具体部署命令与检查通过标准。 |
| **2** | **架构设计全景实施指南**<br>`agentgateway-comprehensive-architecture-guide.md` | `d:\workspace\knowledge\output\reports\agentgateway-comprehensive-architecture-guide.md` | 架构师 / 技术负责人 | **【网关顶层架构全景】**<br>阐述 AI Agent 网关六大核心技术支柱、生产级网络拓扑（跨命名空间打通、com310 绑定调度）、统一 RFC 6750/9728 鉴权与全局限流防穿透架构。 |
| **3** | **虚拟 MCP 聚合核心指南**<br>`agentgateway-virtual-mcp-guide.md` | `d:\workspace\knowledge\output\reports\agentgateway-virtual-mcp-guide.md` | 架构师 / AI 应用开发团队 | **【虚拟 MCP 与动态聚合】**<br>1. 动态服务发现（`mcp-server: enabled`）；<br>2. ExtProc 渐进式元工具折叠（`get_tool` + `invoke_tool`）；<br>3. OpenAPI 转 MCP 标准通用模板与 HR 假期实战样例；<br>4. 全链路 Token 自动透传机制。 |
| **4** | **业务微服务改造参考源码**<br>`MCP服务改造指导方案.md` | `D:\workspace\mcp-server\eco-mcp-server\MCP服务改造指导方案.md` | 业务研发团队 (Java/Python/Go) | **【业务端原生 MCP 改造标准】**<br>指导已有业务系统如何改造成原生合规的 MCP Server：包含 RFC 6750 (401 质询)、DCR 动态客户端注册、JWKS 签名本地校验、V1/V2 端点兼容规范。 |

---

## 3. 生产部署编排配置文件资产全景库 (Manifests Inventory)

所有生产上线的 K8s 编排文件统一归集于本地目录：`D:\workspace\2026\AI 研究\agentgateway_configs\`。

### 3.1 网关核心底座与网络配置 (`agentgateway_configs/`)
* **`gateway.yaml`**：Kubernetes Gateway API 核心声明，创建名为 `ai-gateway` 的统一网关实例。
* **`gateway-params.yaml`**：网关数据面参数配置（指定私有 Harbor 镜像、数据面参数等）。
* **`gateway-ingress.yaml`**：边界 Ingress-NGINX 规则，绑定公网/内网域名 `gateway-ai.cloud.lab.eccom.com.cn`，加固长连接超时。
* **`mcp-route-dynamic-v2.yaml`**：HTTPRoute 核心路由规则，根据请求头自动区分初始握手（强制 JWT 鉴权）与已建会话（放行由插件注入 Token）。
* **`agw-admin-svc.yaml`**：暴露 AgentGateway 管理面端点（15000 端口），供指标观测与配置 Dump。

### 3.2 跨命名空间授权 (`app0040-ecoauth/` & `app0129-wwwin-mcp/`)
* **`app0040-ecoauth/idp-reference-grant.yaml`**：授权主网关跨命名空间访问企业统一认证中心 (`system-auth-center`) 拉取 JWKS 公钥。
* **`app0129-wwwin-mcp/reference-grant.yaml`**：授权主网关将流量反向代理到各业务 MCP Pod。

### 3.3 ExtProc 动态智能扩展插件 (`plugin/`)
* **`plugin/server.py`**：生产级 Python gRPC 核心源码，集成了 Session 身份自动注入、意图分词加权检索算法、K8s 原生 Service Watcher 监听。
* **`plugin/plugin-workload.yaml`**：插件 Deployment 与 Service，配置了健康探针与物理节点调度绑定（`nodeSelector: kubernetes.io/hostname: com310`）。
* **`plugin/plugin-rbac.yaml`**：赋予插件跨命名空间监听 Service 标签与注解的 ClusterRole 与 RoleBinding。
* **`plugin/extproc-policy.yaml`**：网关级 `AgentgatewayPolicy`，将插件作为 ExtProc 过滤器挂载至 `/mcp` 路由。

### 3.4 流量安全与限流策略 (`policy/`)
* **`policy/1-ratelimit-service.yaml`**：Envoy 全局限流服务部署文件，直连机房内部 Redis (`10.2.56.3`)。
* **`policy/2-ratelimit-policy.yaml`**：基于真实客户端用户或 Session 维度的精准防击穿全局限流策略。
* **`policy/3-jwt-auth-policy.yaml`**：主网关对接企业统一认证中心的严格 JWT / OIDC JWKS 验签策略。

### 3.5 运维与监控看板套件 (`monitoring/`)
* **`monitoring/1-prometheus-rbac.yaml` & `2-prometheus.yaml`**：Prometheus 实例与自动化抓取配置。
* **`monitoring/3-grafana.yaml` & `4-ingress.yaml`**：Grafana 可视化服务部署。
* **`agentgateway-mcp-grafana-dashboard.json`**：**企业级 MCP 专属监控大屏模板**，可直接一键导入 Grafana，包含 MCP 请求吞吐、会话活跃数、各微服务调用占比、ExtProc 响应耗时与限流状态。

---

## 4. 两类微服务标准化接入规范与样例 (Onboarding Patterns)

业务系统接入企业虚拟 MCP 网关，可根据系统实际情况选择以下两种接入范式：

### 范式 A：已有 RESTful / OpenAPI 接口接入（OpenAPI Bridge 范式，推荐）
已有 Spring Boot / Go / Python 开发的 RESTful 接口，**完全无需修改代码**，只需部署一个轻量级转换代理。

#### 标准交付模板 (`<service-name>-mcp.yaml`)
```yaml
# 1. 协议转换配置（支持热重载，修改无需重启 Pod）
apiVersion: v1
kind: ConfigMap
metadata:
  name: <SERVICE_NAME>-mcp-bridge-config
  namespace: <TARGET_NAMESPACE>
data:
  config.yaml: |
    proxyMetadata:
      nodeId: "agentgateway~1.1.1.1~.~.svc.cluster.local"
    # 可选：若接口需固定服务级密钥，可在此配置自动代填
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
            host: "<SERVICE_BASE_URL>"           # 业务接口基础访问路径
            spec: "<OPENAPI_SPEC_URL>"           # Swagger v3 JSON 在线地址
---
# 2. 运行时工作负载（直接复用网关同款开源镜像，零新镜像）
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
            name: <SERVICE_NAME>-mcp-bridge-config
---
# 3. 服务暴露与网关动态感知（打标即上线，摘标即下线）
apiVersion: v1
kind: Service
metadata:
  name: <SERVICE_NAME>-mcp-bridge
  namespace: <TARGET_NAMESPACE>
  labels:
    # 【必须】：让 ai-gateway 主网关控制器动态发现并挂载到 /mcp 聚合池
    agentgateway.dev/mcp-server: enabled
  annotations:
    # 【必须】：业务中文名称（供大模型理解）
    agentgateway.dev/display-name: "<业务中文展示名，例如：华讯OA协同办公>"
    # 【必须】：核心能力标签（逗号分隔，毫秒级注入 get_tool 提示词）
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

> **实战样例**：真实生产环境已部署的华讯 HR 假期服务样板见：`D:\workspace\2026\AI 研究\agentgateway_configs\hr-vacation-mcp-bridge.yaml`。

---

### 范式 B：新建原生 MCP 微服务接入（Native MCP 范式）
如果团队开发专用的 MCP 智能体微服务，请参考 `D:\workspace\mcp-server\eco-mcp-server\` 工程源码，实现原生规范：
1. **暴露端点**：同时支持 `/mcp`（内部通信）与 `/v2/mcp`（支持 401 动态质询）；
2. **安全中间件**：挂载 `AuthChallengeMiddleware`，本地连接 `http://system-auth-center:8080/oidc/getJkwsKey` 验签 JWT；
3. **服务声明**：Service 打上 `agentgateway.dev/mcp-server: enabled` 标签并声明端口协议 `appProtocol: agentgateway.dev/mcp`。

---

## 5. 生产部署分节点验证门禁 (Milestone Gates Checklist)

根据 `DEPLOYMENT_GUIDE.md`，执行上线时必须逐一核验以下 6 个门禁：

| 节点 | 门禁内容 | 核心验证命令 | 预期通过状态 |
| :---: | :--- | :--- | :--- |
| **G1** | 跨命名空间授权 | `kubectl get referencegrants -A` | 确认 `app0040-ecoauth` 与 `app0129-wwwin-mcp` 的授权生效 |
| **G2** | 网关底座与边界 Ingress | `kubectl get gateway ai-gateway -n agentgateway-system`<br>`kubectl get ingress ai-gateway-ingress -n agentgateway-system` | Gateway `PROGRAMMED: True`<br>Ingress 成功分配集群 VIP 地址 |
| **G3** | ExtProc 插件就绪 | `kubectl get pods -l app=mcp-tool-search-plugin -n agentgateway-system -o wide` | Pod 运行在指定节点 `com310`，状态 `Running`，0 重启 |
| **G4** | Envoy 全局限流就绪 | `kubectl logs deployment/ratelimit-service -n agentgateway-system` | 日志显示 `Connected to Redis (10.2.56.3:6379)` |
| **G5** | 动态路由与安全策略生效 | `kubectl get agentgatewaypolicies -n agentgateway-system`<br>`kubectl get httproute dynamic-mcp-route -n agentgateway-system` | 策略显示 `ACCEPTED: True` 且 `ATTACHED: True`<br>HTTPRoute 显示 `ResolvedRefs: True` |
| **G6** | 端到端全链路业务闭环 | 1. 匿名访问 `/mcp` 质询返回 HTTP 401<br>2. 携带 Bearer Token 握手返回 Session ID<br>3. `tools/list` 严格仅显示 `get_tool` 与 `invoke_tool`<br>4. 调用 `get_tool` 精准召回业务 Schema<br>5. 调用 `invoke_tool` 真实后端返回 200 OK | 全链路鉴权、动态折叠、微服务路由与 Token 透传 100% 畅通 |

---

## 6. 运维巡检与故障自愈速查手册 (Troubleshooting)

### 1. 客户端报 401 Unauthorized
* **排查点**：客户端首次建立会话时是否携带了有效的 JWT Bearer Token；
* **校验命令**：`kubectl get agentgatewaypolicies mcp-jwt-auth-policy -n agentgateway-system -o yaml`，确认 JWKS 目标 `system-auth-center` 端口 8080 连通性。

### 2. `get_tool` 提示“微服务[xxx]：业务数据查询与办理（功能不明）”
* **原因**：新上线的 MCP 服务或 OpenAPI 桥接 Service 缺少业务语义注解；
* **排查与修复**：执行 `kubectl annotate svc <service-name> -n <namespace> "agentgateway.dev/display-name=业务名称" "agentgateway.dev/capabilities=能力1,能力2" --overwrite`，ExtProc 插件将在秒级内动态热重绘大模型系统 Prompt。

### 3. OpenAPI 桥接接口返回 Token 错误
* **原因**：后端业务系统要求特定服务 Token，或者用户 Token 已失效；
* **解决**：确认客户端传入有效 Token（由 ExtProc 自动回填透传）；如后端需要固定系统 Token，在桥接的 ConfigMap 中增加 `policies.transformation` 自动注入固定请求头。

### 4. 节点物理抖动防范
* **保障措施**：核心关键组件（`mcp-tool-search-plugin` 和 `ratelimit-service`）必须保留 `nodeSelector: kubernetes.io/hostname: com310`，避免被调度至资源超售不稳定的 worker 节点。
