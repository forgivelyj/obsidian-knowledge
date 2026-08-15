---
title: "LlamaParse"
aliases: [llamaparse]
tags: [ai/tool/active]
category: entities
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/02-llama_index框架/02-llama_index框架.md]]"
description: "LlamaParse 是 LlamaIndex 官方推出的云端高精度文档解析引擎，专为扫描件 PDF、复杂嵌套表格和多栏排版的 OCR 结构化提取而设计。"
---

# LlamaParse

LlamaParse 是云端高精度的文档版面分析与数据提取服务，是解决复杂文档 [[RAG]] 检索质量瓶颈的利器。

## 解决的行业痛点
传统的本地 PDF/Word 文本提取器（如 `PDFReader`、`PyPDF` 等）在面对真实商务、财务或学术场景下的复杂文档时，往往出现以下乱码或信息丢失问题：
- **扫描件 PDF / 纯图片 PDF**：本地加载器彻底失效，返回空内容。
- **复杂表格**：表格边界信息丢失，同行数据被截断成毫无关系的数行纯文本。
- **多栏排版（分栏）**：文字阅读顺序错乱，左栏与右栏文本合并在一起。
- **嵌套大纲**：标题的树状缩进与层级大纲关系被抹平。

## 核心机制与特征
1. **云端多模态分析**：文档上传至 LlamaCloud 后，由先进的多模态视觉引擎进行物理布局分析（Layout Analysis），并利用高性能 OCR 引擎识别图片文字。
2. **智能自愈自检 (Agentic Tier)**：在 `agentic` 模式下，云端大模型会主动检查表格与公式解析的连贯性，反复校正模糊或复杂的财务报表，确保提取正确。
3. **结构化 Markdown 输出**：LlamaParse 能够直接将文档转换成包含标准 Markdown 标题层级和排版格式、包含 Markdown 表格的纯文本，这极度有利于后续的 `MarkdownNodeParser` 做语义对齐切分。

## 核心开发步骤 (SDK v2)
需要先在 https://cloud.[[LlamaIndex]].ai 注册账号并生成 `LLAMA_CLOUD_API_KEY`。

```python
import os
from llama_cloud import LlamaCloud

# 1. 初始化客户端
client = LlamaCloud(api_key=os.getenv('LLAMA_CLOUD_API_KEY'))

# 2. 上传待解析文档
file = client.files.create(
    file="./财务管理文档.pdf",
    purpose="parse"
)

# 3. 运行高精度 Agentic 解析
result = client.parsing.parse(
    file_id=file.id,
    tier="agentic",       # agentic 高级精度 | standard 基础精度
    expand=["markdown"]
)

# 4. 获取 Markdown 分页数据
for page in result.markdown.pages:
    print(page.markdown)
```

---
**关联页面**：
- [[LlamaIndex]] (官方框架)
- [[RAG]] (应用场景)
