# Wiki Log

> 记录 LLM Wiki 的所有自动编译、查询、检查与发布记录。

---

## [2026-09-30] outer-loop | system-cms-sem SonarQube Clean Code 质量门禁治理复盘
- **来源**：`system-cms-sem`
- **关联规范**：[[sonarqube-clean-code-guidelines]]
- **操作描述**：
  1. 通过 `sonar-mcp-server` 精准定位质量门禁失败指标：`software_quality_high_issues`（6个CRITICAL缺陷）与 `software_quality_reliability_rating`（等级C/3）；
  2. 彻底治理 6 个 High/Critical 缺陷：在 `SemServiceOperationExpandServiceImpl` 与 `SemServiceOperationServiceImpl` 中抽取 `BUSINESS_CLASS`、`SALES_NAME` 等重复常量，规范复用已有常量（`TEAM_ID`、`DATE_BEGIN`、`DATE_END`，消除 `java:S1192`）；在测试类 `SemServiceOperationExpandServiceImplTest` 中为 mock 写入监听空方法添加说明注释（消除 `java:S1186`）；
  3. 全面重构 20 个类（10个Controller与10个Service/Component）中遗留的 57 处 `@Autowired` 字段依赖注入，统一采用 `@RequiredArgsConstructor` 构造器注入（彻底清空导致 Reliability 降级的 `java:S6813`）；
  4. 执行 `mvn clean test` 完整回归验证，71 个单元测试 100% 通过（0 Failures, 0 Errors）；
  5. 本地切换 JDK 17 执行 `mvn sonar:sonar` 进行全量扫描并推送分析至 SonarQube 服务器，再次调用 `sonar-mcp-server` 验证质量门禁，所有条件全部转绿：Quality Gate Status 从 `ERROR` 变为 `OK`（High 缺陷清零、Reliability 恢复为 A、质量门禁 100% 达标）。

## [2026-09-17] outer-loop | MinIO Java SDK SimpleXML StorageClass 解析陷阱外环复盘
- **来源**：`system-file-ossbase` (通用AI文件存储方案设计)
- **新建概念**：[[MinIO-SimpleXML-StorageClass-Trap]]
- **操作描述**：
  1. 定位 MinIO Java SDK 8.5.x 在 `listMultipartUploads` 操作中因 SimpleXML 强行校验 `@Element(name="StorageClass")` 导致空标签触发 `ValueRequiredException` 崩溃的根本原因；
  2. 验证通过自定义 OkHttpClient 网络拦截器仅对 XML 响应动态重写 `<StorageClass>` 的热修复方案；
  3. 完成本地集成测试与后台孤立分片清理定时任务（`OrphanPartCleanupTask`）无报错验证。

## [2026-09-15] publish | 企业级 AgentGateway 与 MCP 生产部署及指导文件全景总览 (Master Guide)
- **产出文件**：`output/reports/enterprise-mcp-production-deployment-master-guide.md`
- **操作描述**：
  1. 系统化归纳企业 AI Agent 网关四大核心指导文档（分节点部署手册、架构全景实施指南、虚拟 MCP 核心指南、微服务改造标准方案）；
  2. 梳理全量生产部署编排配置清单（`agentgateway_configs/` 下 Gateway 底座、ExtProc 插件、限流与 JWT 鉴权策略、监控套件）；
  3. 沉淀 RESTful OpenAPI 桥接与原生 MCP 双范式标准化接入规范；
  4. 整合 6 大部署里程碑门禁与运维故障速查手册，作为生产交付的总控权威索引。

## [2026-09-15] update | 虚拟 MCP 聚合 OpenAPI 标准化模板与生产实战样例归集
- **更新文档**：`output/reports/agentgateway-virtual-mcp-guide.md`
- **操作描述**：
  1. 完成 OpenAPI 自动聚合转 MCP 工具机制的生产级实测验证（基于开源镜像 `agentgateway:v1.5.0`，零外部新增镜像）；
  2. 固化 OpenAPI 桥接架构标准生产模板（`ConfigMap` + `Deployment` + `Service` 单文件 All-in-One 架构）；
  3. 沉淀 Service 注解业务语义发现规范（`agentgateway.dev/display-name` 与 `agentgateway.dev/capabilities`），实现大模型 Prompt 毫秒级动态自适应感知；
  4. 验证全链路 Token 自动携带与透传能力（用户态 Bearer Token 经 ExtProc 自动回填透传 + 服务级静态 Token 注入），并以华讯 HR 假期服务为样板完成实战落地归档。

## [2026-09-04] publish | AgentGateway 编排文件归集标准化与分节点部署手册发布
- **目标目录**：`D:\workspace\2026\AI 研究\agentgateway_configs`
- **产出文档**：`DEPLOYMENT_GUIDE.md` (6 大里程碑分节点验证手册)
- **组织架构**：
  1. ExtProc 插件归集至 `plugin/`：`server.py`, `plugin-rbac.yaml`, `plugin-workload.yaml`, `extproc-policy.yaml`；
  2. 限流与策略归集至 `policy/`：`1-ratelimit-service.yaml`, `2-ratelimit-policy.yaml`, `3-jwt-auth-policy.yaml`；
  3. 固化物理节点调度绑定规则（`nodeSelector: com310`）与 Redis 局域网直连优化。

## [2026-09-04] maintain | AgentGateway 全组件节点迁移与高可用稳定性治理 (Node Migration)
- **迁移组件**：`agentgateway`, `ratelimit-service`, `mcp-tool-search-plugin`
- **操作详情**：
  1. 根因隔离：将网关控制面组件从超售且反复出现 `NodeNotReady` 物理抖动的节点 `worker08`（CPU Limit 635%）全量迁移至健康节点 `com310`；
  2. 网络优化：`ratelimit-service` 与后端 Redis (`10.2.56.3`) 同属 `10.2.56.x` 二层网段，消除了跨网段路由抖动与证书拉取超时风险；
  3. 配置固化：在 `k8s-mcp-extproc-workload.yaml` 中固化 `nodeSelector: kubernetes.io/hostname: com310`；
  4. 集群验证：三套核心组件全部平稳运行（0 重启），gRPC 实机检索与限流服务测试 100% 正常。

## [2026-09-04] execute | ExtProc 插件增强功能实施完成 (SRS v2.1.0 动态自适应与身份透传)
- **关联代码**：`server.py`, `server_cl_fix.py`, `test_extproc_enhancement.py`, `k8s-mcp-extproc-rbac.yaml`, `k8s-mcp-extproc-workload.yaml`
- **新建概念**：[[Agentgateway-ExtProc-Dynamic-Schema]]
- **更新**：`wiki/index.md`
- **操作描述**：
  1. 升级 ExtProc 扩展处理器为企业级动态自适应版，实现 JWT 身份提取、会话映射、防仿冒 Header 清洗与 `x-authenticated-user` 受信注入；
  2. 实现用户定制基底 Prompt 与微服务能力池双层动态渲染引擎；
  3. 配置 K8s ClusterRole/Binding，集成 In-Cluster 原生 Service Watcher 与 TTL 探活双重保障机制，实现毫秒级下线清理与 503 脏调用拦截；
  4. 完成 TC-01 至 TC-04 全量单元与集成自动化测试，更新集群 Pod 并实现在线平滑热加载。

## [2026-09-04] publish | ExtProc 插件增强功能需求规格说明书 (SRS v2.1.0 动态自适应版)
- **产物文件**：`output/reports/extproc-enhancement-requirements-specification.md`
- **操作描述**：发布 ExtProc 插件功能升级需求文档 v2.1.0，包含三项核心规范：
  1. 用户身份动态透传（Session 映射至真实用户名，防伪造注入 `x-authenticated-user` 头）与 Redis 多租户精准限流；
  2. `get_tool` 描述基于后端实际接入的 MCP Schema 动态自适应聚合生成（摆脱硬编码，随微服务上线/下线实时增减业务大纲）；
  3. 基于 K8s Service 监听与 TTL 探活的 MCP 服务动态生命周期感知，彻底解决下线旧服务残留与脏调用问题。

## [2026-07-27] init | 初始化知识库
- **新建**：`AGENTS.md` (规范文件)
- **新建**：`LLM_WIKI_USER_GUIDE.md` (使用说明指南)
- **新建**：`wiki/index.md` (全局索引)
- **新建**：`wiki/log.md` (操作日志)
- **操作描述**：完成 Obsidian Vault 的基本目录搭建，建立初始空状态，准备接收 Ingest。

## [2026-07-27] ingest | RFC 8707 Resource Indicators for OAuth 2.0
- **来源**：`raw/00-Inbox/RFC 8707 Resource Indicators for OAuth 2.0.md`
- **新建**：[[RFC-8707-Resource-Indicators-for-OAuth-2.0-summary]] (摘要页)
- **新建**：[[OAuth-2.0]] (实体页)
- **新建**：[[Resource-Indicators]] (概念页)
- **新建**：[[Audience-Restriction]] (概念页)
- **更新**：`wiki/index.md` (全局索引)
- **操作描述**：深度解析并导入 RFC 8707 资源指示器协议规范，建立与 OAuth 2.0 及受众限制安全机制的网状链接。

## [2026-07-28] ingest | 01-RAG基础
- **来源**：`raw/00-Inbox/01-RAG基础/01-RAG基础.md`
- **新建**：[[01-RAG基础-summary]] (摘要页)
- **新建**：[[ChromaDB]] (实体页)
- **新建**：[[Redis]] (实体页)
- **新建**：[[RAG]] (概念页)
- **新建**：[[Naive-RAG]] (概念页)
- **新建**：[[Embedding]] (概念页)
- **新建**：[[Vector-Database]] (概念页)
- **更新**：`wiki/index.md` (全局索引)
- **操作描述**：深度解析并导入 RAG 基础及向量检索相关概念，包含 Naive RAG、分块策略、向量数学和数据库开发实践。

## [2026-07-28] ingest | 02-llama_index框架
- **来源**：`raw/00-Inbox/02-llama_index框架/02-llama_index框架.md`
- **新建**：[[02-llama_index框架-summary]] (摘要页)
- **新建**：[[LlamaIndex]] (实体页)
- **新建**：[[LlamaParse]] (实体页)
- **新建**：[[Storage-Context]] (概念页)
- **新建**：[[Query-Engine]] (概念页)
- **更新**：`wiki/index.md` (全局索引)
- **操作描述**：导入大模型数据整合框架 LlamaIndex，梳理其架构、全局Settings、LlamaParse高精度版面分析、三位一体存储系统（StorageContext）及查询/聊天引擎开发流。

## [2026-07-28] ingest | 03-RAG进阶
- **来源**：`raw/00-Inbox/03-RAG进阶/03-RAG进阶.md`
- **新建**：[[03-RAG进阶-summary]] (摘要页)
- **新建**：[[Advanced-RAG]] (概念页)
- **新建**：[[Reranking]] (概念页)
- **新建**：[[RAG-vs-Fine-Tuning]] (对比分析页)
- **更新**：`wiki/index.md` (全局索引)
- **操作描述**：深度剖析 RAG 落地过程中的故障痛点与针对性优化，引入预检索与后检索（重排模型）优化策略，解读前沿学术变体（CRAG/Self-RAG/RAG-Fusion），并系统对比 RAG 与微调在开发选型上的差异。

## [2026-07-28] ingest | 04-Advanced RAG
- **来源**：`raw/00-Inbox/04-Advanced RAG/04-Advanced RAG.md`
- **新建**：[[04-Advanced RAG-summary]] (摘要页)
- **新建**：[[MinerU]] (实体页)
- **新建**：[[Ingestion-Pipeline]] (概念页)
- **新建**：[[Parent-Child-Index]] (概念页)
- **更新**：`wiki/index.md` (全局索引)
- **操作描述**：深入高级 RAG 工程实现，导入 LlamaIndex IngestionPipeline 管道、元数据生成机制、父子层级索引构建、四种多路检索打分融合算法（如 Z-Score DBSF）、多维度后处理器（如首尾重排与上下文拓展）与 MinerU 解析实战。

## [2026-07-28] ingest | 05-KNOWLEDGE GRAPH FOR RAG
- **来源**：`raw/00-Inbox/05-KNOWLEDGE GRAPH FOR RAG/05-KNOWLEDGE GRAPH FOR RAG.md`
- **新建**：[[05-KNOWLEDGE GRAPH FOR RAG-summary]] (摘要页)
- **新建**：[[Neo4j]] (实体页)
- **新建**：[[LightRAG]] (实体页)
- **新建**：[[GraphRAG]] (概念页)
- **新建**：[[Property-Graph]] (概念页)
- **更新**：`wiki/index.md` (全局索引)
- **操作描述**：深度解析并导入图谱增强检索（GraphRAG）技术，梳理知识图谱构建生命周期、Neo4j 数据库 CQL 操作与 APOC 过程、LlamaIndex 属性图四类三元组抽取器（如 Schema 强约束提取）及港大开源 LightRAG 双层检索与局部增量更新架构。

## [2026-07-28] ingest | 06-RAG评估
- **来源**：`raw/00-Inbox/06-RAG评估/06-RAG评估.md`
- **新建**：[[06-RAG评估-summary]] (摘要页)
- **新建**：[[Ragas]] (实体页)
- **新建**：[[RAG-Evaluation]] (概念页)
- **更新**：`wiki/index.md` (全局索引)
- **操作描述**：导入 RAG 系统评估诊断工程规范，梳理检索端（Context Precision & Recall）与生成端（Faithfulness & Answer Relevancy）四大评估指标，解读主流评测框架 Ragas 与 TruLens 的数据输入与运行原理，详解 LlamaIndex 响应及检索评估（Hit Rate & MRR）开发实践与 BatchEvalRunner 批量提效方案。

## [2026-07-28] ingest | 07-RAG应用平台
- **来源**：`raw/00-Inbox/07-RAG应用平台/07-RAG应用平台.md`
- **新建**：[[07-RAG应用平台-summary]] (摘要页)
- **新建**：[[Dify]] (实体页)
- **新建**：[[RAG-Workflow-Platform]] (概念页)
- **更新**：`wiki/index.md` (全局索引)
- **操作描述**：导入可视化工作流编排技术规范，横向对比手写 RAG 代码与编排平台的选型特点，剖析网易 QAnything（两阶段 Rerank）、FastGPT（QA 拆分）与 RagFlow（自研文档物理版面分析）核心竞争优势，详尽拆解 Dify 平台三大应用模式与十类可视化逻辑节点配置。

## [2026-07-28] ingest | 08-RAG项目实战
- **来源**：`raw/00-Inbox/08-RAG项目实战/08-RAG项目实战.md`
- **新建**：[[08-RAG项目实战-summary]] (摘要页)
- **新建**：[[RAG-Project-Architecture]] (概念页)
- **更新**：`wiki/index.md` (全局索引)
- **操作描述**：导入端到端 RAG 问答项目工程实现细节，总结多用户隔离会话流、SSE 流式数据传输与前端半行数据缓冲自愈解析算法，详解适配层懒加载单例模式设计、混合检索对 `store_nodes_override` docstore 持久化的依赖以及 numpy float 序列化崩溃预防。

## [2026-07-28] ingest | Agent智能体
- **来源**：`raw/00-Inbox/Agent智能体/Agent智能体.md`
- **新建**：[[Agent智能体-summary]] (摘要页)
- **新建**：[[AutoGen]] (实体页)
- **新建**：[[CrewAI]] (实体页)
- **新建**：[[AI-Agent]] (概念页)
- **新建**：[[LangChain-Agent-Runtime]] (概念页)
- **新建**：[[Agent-Middleware]] (概念页)
- **更新**：`wiki/index.md` (全局索引)
- **操作描述**：导入智能体技术体系，详述 AI Agent 五层技术架构、LangChain 1.0 基于 ToolRuntime 的运行期与 PostgresSaver/InMemoryStore 长期/短期记忆机制、裁剪（trim_messages）与 RemoveMessage 历史垃圾回收、六大钩子中间件防线与 JSON 自愈修复，系统梳理 MAS 四大核心设计模式，并横向对比实战微软 AutoGen（代码沙箱与发言状态机）和 CrewAI（岗位分工流编排）。

## [2026-07-28] ingest | DeepAgent框架
- **来源**：`raw/00-Inbox/DeepAgent框架/DeepAgent框架.md`
- **新建**：[[DeepAgent框架-summary]] (摘要页)
- **新建**：[[OpenSandbox]] (实体页)
- **新建**：[[DeepAgents]] (概念页)
- **新建**：[[DeepAgents-Backend]] (概念页)
- **新建**：[[DeepAgents-Subagent]] (概念页)
- **更新**：`wiki/index.md` (全局索引)
- **操作描述**：导入企业级智能体 Harness 套件设计，详述基于 LangGraph 的三层封装（create_deep_agent）、文件后端系统（State/Filesystem/Store/CompositeBackend）与 CompositeBackend 路由器设计、FilesystemPermission 权限安全审批与中断挂起机制、阿里开源 OpenSandbox 在 Docker 中的命令自闭环执行（与 BaseSandbox 的适配器转换），并深入对比 SubAgent 与 CompiledSubAgent 分层多代理上下文隔离设计选型。

## [2026-07-28] ingest | LangGraph框架
- **来源**：`raw/00-Inbox/LangGraph框架/LangGraph框架.md`
- **新建**：[[LangGraph框架-summary]] (摘要页)
- **新建**：[[LangGraph]] (实体页)
- **新建**：[[LangGraph-State-Graph]] (概念页)
- **新建**：[[LangGraph-Persistence]] (概念页)
- **新建**：[[LangGraph-Long-Term-Memory]] (概念页)
- **新建**：[[LangGraph-Human-In-The-Loop]] (概念页)
- **新建**：[[LangGraph-Multi-Agent]] (概念页)
- **更新**：`wiki/index.md` (全局索引)
- **操作描述**：导入多智能体工作流框架，详述其与 LangChain 链式结构的差异与认知架构优势；拆解有状态流程图（StateGraph）、输入输出 Schema 字段安全隔离、与 Send 动态并发分支（Map-Reduce）；详解基于 Checkpointer 的超级步骤（Superstep）快照持久化、时间轴历史回溯与 checkpoint_id 重放重构、update_state 节点伪装强行编辑；剖析跨会话长期记忆 Store 键值数据库存储、HuggingFaceEmbeddings 模糊语义向量检索；深入剖析 interrupt_before 审核关卡与运行时节点内 interrupt() / Command(resume=) 填空双轨中断；归纳 MAS 分布式 Handoffs 转交指针与 Supervisor 任务意图循环分发回收主管编排模式。

## [2026-07-28] ingest | MCP-模型上下文协议
- **来源**：`raw/00-Inbox/MCP-模型上下文协议/MCP-模型上下文协议.md`
- **新建**：[[MCP-模型上下文协议-summary]] (摘要页)
- **新建**：[[MCP]] (实体页)
- **新建**：[[MCP-Host-Client-Server]] (概念页)
- **新建**：[[MCP-Core-Protocol-Elements]] (概念页)
- **新建**：[[MCP-Transport-Modes]] (概念页)
- **新建**：[[MCP-FastMCP-LangChain]] (概念页)
- **更新**：`wiki/index.md` (全局索引)
- **操作描述**：导入模型上下文协议 (MCP) 标准，详述 Host-Client-Server 架构；剖析 Client 核心三大安全与控制职责：Roots 路径边界访问限制、Elicitation 提示词模板 UI 渲染、与 Sampling 反向大模型算力采样；详解 Resources（只读静态 URI 数据）、Tools（带 JSON Schema 参数和副作用的主动操作）、与 Prompts（SOP 对话模板）三剑客协议结构；对比 Stdio（stdout 路由与 stderr 调试日志隔离）、HTTP with SSE、与新一代 Streamable HTTP 单通道流式全双工与 Token 鉴权传输模式；归纳 FastMCP 自动 Schema 极简声明开发方式、Low-Level API 动态控制，并详述 langchain-mcp-adapters 桥接多 StdIO MCP 服务器至 LangChain BaseTool 的适配对齐实现。

## [2026-07-29] synthesis | LobeHub 鉴权 MCP 服务器方案
- **新建**：[[lobehub-mcp-auth-solution]] (综合洞察页)
- **更新**：`wiki/index.md` (全局索引)
- **操作描述**：结合本地知识库中的 MCP 及 OAuth 2.0 规范，整理 LobeHub 接入身份认证 MCP 服务器的完整技术方案，详解 Stdio 本地进程环境变量注入与标准 OAuth 2.0 PKCE 认证，并提出基于 RFC 8707 Resource Indicators 锁受众防 Token 泄露以及流程挂起自愈重试的机制。

## [2026-08-05] ingest | OAuth 2.0 & OIDC 协议规范 (7份素材)
- **来源**：
  - `raw/00-Inbox/Final OpenID Connect Discovery 1.0 incorporating errata set 2.md`
  - `raw/00-Inbox/OAuth Client ID Metadata Document.md`
  - `raw/00-Inbox/RFC 7591 OAuth 2.0 Dynamic Client Registration Protocol.md`
  - `raw/00-Inbox/RFC 7636 Proof Key for Code Exchange by OAuth Public Clients.md`
  - `raw/00-Inbox/RFC 8252 OAuth 2.0 for Native Apps.md`
  - `raw/00-Inbox/RFC 8414 OAuth 2.0 Authorization Server Metadata.md`
  - `raw/00-Inbox/RFC 9728 OAuth 2.0 Protected Resource Metadata.md`
- **新建/更新摘要**：
  - [[Final-OpenID-Connect-Discovery-1.0-incorporating-errata-set-2-summary]]
  - [[OAuth-Client-ID-Metadata-Document-summary]]
  - [[RFC-7591-OAuth-2.0-Dynamic-Client-Registration-Protocol-summary]]
  - [[RFC-7636-Proof-Key-for-Code-Exchange-by-OAuth-Public-Clients-summary]]
  - [[RFC-8252-OAuth-2.0-for-Native-Apps-summary]]
  - [[RFC-8414-OAuth-2.0-Authorization-Server-Metadata-summary]]
  - [[RFC-9728-OAuth-2.0-Protected-Resource-Metadata-summary]]
- **新建/更新实体**：
  - [[OAuth-2.0]] (更新实体页，关联新增 7 扩展规范)
  - [[OpenID-Connect]] (新建实体页)
- **新建概念**：
  - [[OIDC-Discovery]] (概念页)
  - [[OAuth-Client-ID-Metadata]] (概念页)
  - [[Dynamic-Client-Registration]] (概念页)
  - [[PKCE]] (概念页)
  - [[OAuth-Native-Apps]] (概念页)
  - [[Authorization-Server-Metadata]] (概念页)
  - [[Protected-Resource-Metadata]] (概念页)
- **更新**：`wiki/index.md` (全局索引)

## [2026-08-10] synthesis | Agent MCP 鉴权标准架构 (DCR与CIMD混合鉴权方案)
- **新建**：[[Agent MCP 鉴权标准架构 (DCR与CIMD混合鉴权方案)]] (综合洞察页)
- **更新**：`wiki/index.md` (全局索引)
- **操作描述**：基于全链路端到端联调测试结论，总结并撰写 Agent MCP 鉴权标准架构 (v2.0)。包含 V1/V2 双端点隔离 (Legacy `/mcp` 直传 X-ID-Token 与 OAuth2 401 质询 `/v2/mcp`)、DCR 动态客户端注册自动免确认授权 (`autoApprove=true`)、`application.yml` 配置解耦 (`default-scopes` 与 `default-resource`)、2-Step RFC 8693 Token Exchange 链路与客户端 `mcp.json` 部署规范。

## [2026-08-14] ingest | OpenWiki 代码库文档维护 (system-auth-center)
- **来源**：`d:/workspace/java-project/erp/system-auth-center`
- **新建**：[[system-auth-center-summary]] (摘要页)
- **新建**：[[System-Auth-Center]] (实体页)
- **新建**：[[System-Auth-Center-Architecture]] (概念页)
- **新建**：[[Custom-Token-Granter-Pattern]] (概念页)
- **更新**：`wiki/index.md` (全局索引)
- **操作描述**：基于 LangChain OpenWiki 规范与 OKF v0.1 标准，为 `system-auth-center` 代码库建立 `openwiki/` 目录结构（包含 `index.md`, `architecture.md`, `custom-token-granters.md`, `security-and-rate-limiting.md`, `INSTRUCTIONS.md`, `logs.md`），并同步沉淀关联节点至本地 Obsidian 知识库。

## [2026-08-15] ingest | Andrej Karpathy - LLM Wiki Pattern
- **来源**：`raw/00-Inbox/Andrej Karpathy - LLM Wiki Pattern.md`
- **新建**：[[Andrej-Karpathy-LLM-Wiki-Pattern-summary]] (摘要页)
- **新建**：[[Andrej-Karpathy]] (实体页)
- **新建**：[[LLM-Wiki]] (概念页)
- **新建**：[[Compounding-Knowledge]] (概念页)
- **更新**：`wiki/index.md` (全局索引)
- **操作描述**：摄入 Andrej Karpathy 关于大模型驱动的持久化个人知识库设计模式（LLM Wiki），建立三层架构与四大工作流模型。

- 2026-09-01 19:23:26 [Publish]: 虚拟 MCP 聚合指南 [[output/reports/agentgateway-virtual-mcp-guide.md]]

- 2026-09-02 13:58:17 [Publish]: 全景架构实施指南 [[output/reports/agentgateway-comprehensive-architecture-guide.md]]

## [2026-09-04] concept | WikiSkill-Procedural-Memory
- **新建**：[[WikiSkill-Procedural-Memory]] (概念页)
- **新建**：skills/wikiskill-knowledge-loop/SKILL.md (跨 Agent 标准技能规范)
- **新建**：~/.gemini/config/rules/wikiskill-knowledge-loop.md (全局工作流规则)
- **更新**：wiki/index.md (全局索引)
- **操作描述**：引入 WikiSkill 智能体程序性记忆演化框架，实现跨项目开发中的前置记忆检索、测试验证门控与 Obsidian 外环复盘闭环。

## [2026-09-04] concept | MCP ExtProc 工具检索与网关稳定性治理
- **新建**：[[mcp-extproc-tool-search-engine]] (概念页)
- **更新**：`wiki/log.md`
- **操作描述**：针对企业级 MCP ExtProc 网关工具折叠中的盲目伪兜底、180s 粗暴 TTL 误杀工具、以及小阈值硬编码导致高频增删改工具挤出查询工具（如 `list_meeting_room_usage`、`search_office`）等反模式进行深度复盘与重构。引入四大能力池映射、意图加权多级检索与 K8s 强关联生命周期；并定位 AgentGateway/Ratelimit 因底层节点抖动重启的根本原因。


## 2026-09-07 (Outer Loop Knowledge Update)
- **来源**：`d:/eccom/wwwinDev` (ERP Performance Scheme & Indicator Management)
- **新建概念**：[[Legacy-VBScript-ADO-Field-Trap]]
- **摘要**：记录 Classic ASP/VBScript 中 ADODB.Field COM 对象引用失效导致 0x8000FFFF 严重错误的原因、反模式与解决方案。

## 2026-09-10 (Outer Loop Knowledge Update)
- **来源**：`d:/workspace/java-project/dmp/hr-profile-lakehouse`
- **新建实体**：[[sonarqube-clean-code-guidelines]]
- **摘要**：针对使用 SonarQube 与 sonar-mcp-server 进行代码质量检测与门禁治理过程中的分支感知陷阱（遗漏 branch 导致默认检索 master）、S1948 序列化、S3776 认知复杂度、S6813/S3305 依赖注入、S1192 字符串字面量去重、S5786 测试类可见性等反模式与标准解决规范进行外环复盘与沉淀。

## [2026-09-18] ingest | Towards a Science of Scaling Agent Systems (arXiv:2512.08296)
- **来源**：`raw/00-Inbox/Towards-a-Science-of-Scaling-Agent-Systems.md`
- **新建**：[[Towards-a-Science-of-Scaling-Agent-Systems-summary]] (摘要页)
- **新建**：[[Agent-Scaling-Law]] (概念页)
- **更新**：[[AI-Agent]] (概念页，引入多智能体能力饱和与工具开销边界)
- **更新**：[[LangGraph-Multi-Agent]] (概念页，引入集中校验防错误雪崩规律)
- **更新**：`wiki/index.md` (全局索引)
- **操作描述**：深度解析并摄入华盛顿大学与MIT等团队关于智能体系统扩展律的实证科学研究，量化 5 类架构、能力饱和效应、重工具协调开销负惩罚（$\hat{\beta}=-0.096$）及集中校验对阻断幻觉级联的核心机制，建立架构与任务解耦特征对齐规则。

## [2026-09-18] ingest | Google Antigravity Teamwork (When AI Becomes a Research Partner)
- **来源**：`raw/00-Inbox/Teamwork-When-AI-Becomes-a-Research-Partner.md`
- **新建**：[[Teamwork-When-AI-Becomes-a-Research-Partner-summary]] (摘要页)
- **新建**：[[Teamwork]] (实体页)
- **新建**：[[Long-Proof-Pattern]] (概念页)
- **新建**：[[Silent-Execution-Gap]] (概念页)
- **更新**：`wiki/index.md` (全局索引)
- **操作描述**：摄入 Google Antigravity 官方发布的 Teamwork 多智能体前沿科研与工程编排体系，解构 Pattern 声明式解耦与运行时弹性伸缩特性，萃取 Long Proof 锦标赛综合树与 1v1 Falsifier 对抗证伪范式，沉淀解决 CPU 微架构时序仿真的 Lockstep 锁步协同方案（跨越静默执行鸿沟），并记录数学 7 大未决猜想及 Eigen/ParlayHash 开源合入战果。
