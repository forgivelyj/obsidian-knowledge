# Wiki Log

> 记录 LLM Wiki 的所有自动编译、查询、检查与发布记录。

---

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


