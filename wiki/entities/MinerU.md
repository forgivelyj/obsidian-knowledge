---
title: "MinerU"
aliases: [mineru, PDF-Extract-Kit]
tags: [ai/tool/active]
category: entities
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/04-Advanced RAG/04-Advanced RAG.md]]"
description: "MinerU 是上海人工智能实验室开源的一站式高精度文档智能解析工具，专注于将复杂排版 PDF 转换为包含 LaTeX 公式与结构化 Markdown 表格的纯文本。"
---

# MinerU

MinerU 是目前开源界最强悍的 PDF/文档版面分析与提取工具之一，由**上海人工智能实验室 OpenDataLab** 团队开发。它是构建高质量本地知识库的利器，专门应对传统 PDF 提取器的提取痛点。

---

## 1. 核心技术解决能力
- **跨版面还原**：智能识别文档的页眉、页脚、页码、单双栏混合混排，自动剔除不必要的装饰信息，保持原作者的逻辑阅读顺序。
- **数学公式 LaTeX 还原**：将行内和行间公式高精度转译为标准的 LaTeX 语法，对科学文献、理工科教材解析极佳。
- **表格高保真重组**：智能识别复杂无边框或有边框表格，将其重新转化为标准的 Markdown 表格或 HTML 表格结构，防止行列字符断裂错位。
- **混合多模态 OCR**：在面对扫描件、低质量生图 PDF 时，能够自动调用多语言 OCR 引擎进行文字转录。

---

## 2. 三种部署与使用方式
- **在线体验网**：https://mineru.net （简单快速，但有免费额度和队列限制，且不下载本地图片实体）。
- **跨平台桌面客户端**：提供简便的 Windows/Mac GUI 软件，适合非程序员进行文档批量转 Markdown。
- **本地 Python 开发（CLI/SDK）**：使用 `PDF-Extract-Kit` 模型库进行本地 GPU/CPU 推理，适合将解析步骤无缝集成在 [[RAG]] 系统的 Ingestion Pipeline 中。

### Python 本地解析代码示例
```python
import os
from mineru.cli.common import do_parse
from mineru.data.data_reader_writer import FileBasedDataWriter

# 配置本地模型路径
os.environ["MINERU_MODEL_SOURCE"] = "local"
os.environ["MINERU_TOOLS_CONFIG_JSON"] = "./mineru.json"

pdf_path = "./公司年报.pdf"
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

# 核心解析
do_parse(
    pdf_file_names=[os.path.basename(pdf_path)],
    pdf_bytes_list=[pdf_bytes],
    p_lang_list=[""], # 自动识别语言
    output_dir="./output_md",
    img_writer=FileBasedDataWriter("./output_md/images"),
    parse_method="auto"
)
```

---
**关联页面**
- [[LlamaParse]] (云端的同类高精度解析方案)
- [[Advanced-RAG]] (应用大背景)
- [[Parent-Child-Index]] (解析产物经常输入该索引中)
