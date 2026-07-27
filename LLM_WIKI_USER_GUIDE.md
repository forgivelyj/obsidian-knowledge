# Obsidian + LLM Wiki 使用说明指南

本指南将指导你如何使用和维护已搭建好的 **LLM Wiki 智能知识库**。知识库的所有本地目录与规则文件已在您的 workspace (`d:\workspace\knowledge`) 部署完成，且 Obsidian 软件已通过 Winget 成功安装。

---

## 1. 快速上手：在 Obsidian 中打开知识库

1. **启动 Obsidian**：
   在你的 Windows 系统上，点击“开始”菜单，搜索并打开 **Obsidian**。
2. **导入仓库 (Vault)**：
   * 在启动窗口中，选择 **"Open folder as vault"** (打开文件夹为库) 下的 **"Open"** 按钮。
   * 选择你本地的仓库路径：`d:\workspace\knowledge`，然后点击确定。
3. **查看结构**：
   打开后，你将在左侧导航栏看到已经为你初始化好的 `raw/`（原始素材）、`wiki/`（LLM 领地）和 `output/`（成品输出）等目录。

---

## 2. 软件配置核对（首次打开需检查）

为了保证 Obsidian 的日常使用与 LLM 的自动化规则完美契合，请在 Obsidian 软件内进行以下两项检查：

### ① 附件路径检查
1. 打开左下角设置（齿轮图标）。
2. 选择 **Files & Links** (文件与链接) -> 找到 **Default location for new attachments** (新附件的默认位置)。
3. 确保其设置为：**"In the folder specified below"** (下方指定的文件夹中)。
4. 在下面的输入框中填入：`raw/90-Attachments`。

### ② 每日笔记（Daily Notes）与模板检查
1. 在设置中选择 **Core plugins** (核心插件) -> 确保启用 **Daily notes**。
2. 点击 Daily notes 右侧的齿轮进入配置：
   * **Date format** (日期格式)：`YYYY-MM-DD`
   * **New file location** (新文件位置)：`raw/01-Daily`
   * **Template file location** (模板文件位置)：`raw/80-Templates/daily_template.md` (已为您自动生成)

---

## 3. 核心工作流：如何与 AI 协作

你无需手动编写 Wiki，所有的 Ingest、Query、Lint 和 Publish 都应当通过大模型（如 Gemini 3.5 Pro、Claude Code 或 Cursor 等）来完成。你只需提供 **`AGENTS.md`** 和你想要处理的文件。

以下是你可以**直接复制使用**的 AI 对话 Prompt 模板：

### 📥 工作流一：知识摄入 (Ingest)
当你想把剪藏的网页或新文献塞入知识库时：
1. 将网页或文章保存为 Markdown 格式，放入 `raw/00-Inbox/`（例如 `raw/00-Inbox/my-new-tech.md`）。
2. 在 AI 聊天对话中，**同时输入 `AGENTS.md` 的内容、新素材的内容**，并发送以下指令：

> **Ingest 指令模板**：
> ```
> 请根据我提供的行为规范 `AGENTS.md`，对我刚放入 `raw/00-Inbox/` 的新素材进行 Ingest 摄入处理。
> 
> 任务要求：
> 1. 深度分析素材，向我汇报 3-5 个核心观点。
> 2. 在 `wiki/summaries/` 下为该素材新建一个摘要文件，并设置好 sources 关联。
> 3. 检查现有 wiki 目录，消重并更新相关的概念页 (concepts) 或实体页 (entities)，并在文件之间建立 [[双链]] 链接。
> 4. 更新全局索引 `wiki/index.md` 和操作日志 `wiki/log.md`。
> ```

---

### 🔍 工作流二：知识查询 (Query)
当你需要从知识库中查询某项技术或寻求分析时：

> **Query 指令模板**：
> ```
> 请作为我知识库的智能查询助手，帮我回答以下问题：[在此输入你的问题，例如：RAG 的主要局限性是什么？]
> 
> 任务要求：
> 1. 仔细阅读 wiki 下的 index.md 和相关实体/概念页面。
> 2. 整合已有知识回答我，并在答案中提及的专有名词上使用 [[双链]] 语法。
> 3. 如果需要，请给出进一步探索或补充相关素材的建议。
> ```

---

### 🛠️ 工作流三：健康检查 (Lint)
随着文件变多，知识库可能会出现孤立节点或矛盾，定期发送此指令给 AI：

> **Lint 指令模板**：
> ```
> 请对我本地的 wiki/ 目录进行一次 Lint 健康检查。
> 
> 任务要求：
> 1. 检索所有 markdown 文件，找出没有任何入链的“孤立页面”。
> 2. 检查是否有新旧信息冲突或矛盾的地方，并在矛盾页面顶部使用 `> [!WARNING] 矛盾警告` 标记。
> 3. 扫描文本中是否有提到某些已知实体但未做 [[双链]] 链接的地方。
> 4. 输出健康检查报告，并列出具体的修复建议。
> ```

---

### 📤 工作流四：成品发布 (Publish)
当你需要把知识库内容提炼成文章或 PPT 课件时：

> **Publish 指令模板**：
> ```
> 我需要围绕主题 [在此输入主题，例如：LLM Wiki 的落地实践] 撰写一份 [文章/报告/PPT草稿]。
> 
> 任务要求：
> 1. 通过双链检索搜集 wiki 中所有关联的概念页和实体页。
> 2. 提炼内容，在 `output/` 对应的子目录下生成目标格式的草稿文件。
> 3. 注意：成品文件必须独立可读，请将草稿中的 Obsidian [[双链]] 语法自动替换为标准的 Markdown 链接或纯文本。
> 4. 更新 `wiki/log.md` 记录本次发布操作。
> ```

---

## 4. 推荐社区插件配置

为了提升使用体验，强烈建议你在 Obsidian 的 **Community plugins** (社区插件) 中安装并启用以下插件：

### ① Dataview (动态查询插件)
Dataview 是 LLM Wiki 的看板引擎。通过在 markdown 页面写入一段 SQL 式的代码，你可以动态生成全局看板。

* **用法一：在 `wiki/index.md` 中展示最近更新的 10 个 Wiki 页面**：
  ```markdown
  ```dataview
  TABLE description AS 摘要, updated AS 更新时间
  FROM "wiki"
  SORT updated DESC
  LIMIT 10
  ```
  ```

* **用法二：按标签筛选概念页**：
  ```markdown
  ```dataview
  LIST description
  FROM "wiki/concepts"
  WHERE contains(tags, "ai")
  ```
  ```

### ② Obsidian Web Clipper (官方浏览器剪藏插件)
1. 在 Edge/Chrome/Firefox 浏览器中安装 **Obsidian Web Clipper** 插件。
2. 配置保存目标路径为你的本地仓库：`d:\workspace\knowledge\raw\00-Inbox`。
3. 以后在浏览器中看到优秀文章，点击插件即可一键将其完美转为 Markdown 并自动存放，等待下一次 AI Ingest 消化。
