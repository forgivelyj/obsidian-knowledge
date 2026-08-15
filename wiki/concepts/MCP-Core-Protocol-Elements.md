---
title: "MCP-Core-Protocol-Elements"
aliases: [Resources, Tools, Prompts, MCP三剑客]
tags: [ai/protocol/active]
category: concepts
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/MCP-模型上下文协议/MCP-模型上下文协议.md]]"
description: "MCP-Core-Protocol-Elements 详解 Resources 只读资源、具有 JSON Schema 的主动可执行 Tools 及其副作用、和 Prompts 模板。"
---

# [[MCP]] 核心协议三剑客 (Resources / Tools / Prompts)

在 **[[MCP]]** 协议中，Server 向 Client 暴露的能力以及传递的数据被标准化为三个核心元素，通称为 **“[[MCP]] 三剑客”**。

---

## 1. 核心三剑客定义与工作流对比

| 要素 | 行为属性 | 作用定位 | 通俗喻体 |
| :--- | :--- | :--- | :--- |
| **Resources** | 被动、只读、静态 | AI 的私有知识库，传递实时本地背景数据。 | 档案柜与参考书 |
| **Tools** | 主动、动态、可执行 | 允许 AI 动手操作环境，可能改变系统状态或产生副作用。 | 电话与执行义肢 |
| **Prompts** | 预设、辅助、引导 | 对话及人设 SOP 模板，引导 AI 按照标准规范提问。 | 岗位 SOP 说明书 |

---

## 2. 核心元素详解与底层运作

### ① 资源 (Resources) —— AI 的眼睛
- **核心特征**：被动只读。AI 只能读取，无权修改。
- **运作细节**：
  - 每个资源都拥有一个唯一的 **URI 标识符**（如 `resource://health-guidelines` 或本地文件路径）以及指定的 **MIME 类型**（如 `text/plain`、`application/json`）。
  - 用于向大模型安全地喂入最新、最局部的静态参考文档（如应用日志 `system.log`、实时数据库快照、静态配置）。
  - *价值*：给 AI 提供了充足的实时硬性背景，大幅抑制因训练数据过时导致的**幻觉**问题。

### ② 工具 (Tools) —— AI 的双手
- **核心特征**：主动执行，带参数校验。这是 [[MCP]] 中**最强大、最具副作用**的功能。
- **运作细节**：
  - Server 会声明工具的名称、描述以及基于标准的 **JSON Schema 输入参数校验格式**。
  - 大模型分析用户的意图，决定使用工具后，按照 Schema 格式填好参数（例如要查询天气的城市 `{"city": "Beijing"}`），通过 Client 发送指令到 Server 执行。
  - *价值*：打破了对话框的限制。Tools 不仅能返回计算结果（如 `calculate_sum`），更可执行有物理副作用的写入或系统控制行为（如重启服务器 `restart_server`、发邮件、更新数据库表数据）。

### ③ 提示词 (Prompts) —— AI 的剧本
- **核心特征**：预设模板，引导提问。
- **运作细节**：
  - Server 将特定的优秀提示词工程模块（如代码审查 SOP、故障诊断标准话术）打包声明并命名（如 `analyze-error`）。
  - 当人类在 Host 客户端界面选择该 Prompt 时，Client 会根据模板声明的参数（如 `name`、`weight`）弹出 UI 表单渲染让用户填写。
  - 最终，模板内容与用户填写的参数融合打包成完整的 System/User Message 灌给大模型，确保大模型的提问水平、语气和人设维持高度标准化与 SOP 统一。

---
**关联页面**
- [[MCP]] (协议实体)
- [[MCP-Host-Client-Server]] (宿主与客户端交互)
- [[MCP-Transport-Modes]] (底层消息流是如何发送的)
