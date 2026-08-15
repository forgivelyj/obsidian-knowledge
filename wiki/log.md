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

## [2026-08-15] ingest | Andrej Karpathy - LLM Wiki Pattern
- **来源**：`raw/00-Inbox/Andrej Karpathy - LLM Wiki Pattern.md`
- **新建**：[[Andrej-Karpathy-LLM-Wiki-Pattern-summary]] (摘要页)
- **新建**：[[Andrej-Karpathy]] (实体页)
- **新建**：[[LLM-Wiki]] (概念页)
- **新建**：[[Compounding-Knowledge]] (概念页)
- **更新**：`wiki/index.md` (全局索引)
- **操作描述**：摄入 Andrej Karpathy 关于大模型驱动的持久化个人知识库设计模式（LLM Wiki），建立三层架构与四大工作流模型。

## [2026-08-15] lint & sync | 知识库全量巡检与同步更新
- **巡检范围**：全量 `raw/` 原始素材、`wiki/` 知识沉淀层及图谱连接
- **检查结果**：
  - ✅ 孤立页面检测：无孤立页（所有页面均具备有效的双向链入/链出）
  - ✅ 元数据完整度：全部 Frontmatter（YAML）格式规范校验通过
  - ✅ 索引同步：已重新核算并更新 [`wiki/index.md`](file:///d:/workspace/kb/wiki/index.md)
- **操作描述**：完成知识库结构健康度校验，确保 Obsidian 渲染、图谱视图与 Dataview 兼容无误。
