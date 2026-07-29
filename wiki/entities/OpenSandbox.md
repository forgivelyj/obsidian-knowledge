---
title: "OpenSandbox"
aliases: [opensandbox, 阿里开源沙箱]
tags: [ai/tool/active]
category: entities
created: 2026-07-28
updated: 2026-07-28
sources: 
  - "[[raw/00-Inbox/DeepAgent框架/DeepAgent框架.md]]"
description: "OpenSandbox 是阿里开源的专为 AI 自动代码执行设计的容器化沙箱环境，支持多语言 Docker 隔离和 BaseSandbox 协议的适配器转化。"
---

# OpenSandbox (AI 容器化执行沙箱)

在 **[[DeepAgents]]** 中，沙箱（Sandbox）被视为一种更为强力的物理 Backend 后端。它除了具备标准的 `ls`、`read_file`、`write_file` 等文件管理能力外，最核心的增量优势在于：**为大模型提供了一个能够在隔离容器中执行任意 shell 命令的 `execute` 工具**，从而在保护宿主机安全的前提下，实现了真正的“大模型代码自闭环执行”。

**OpenSandbox** 是阿里巴巴（Alibaba）开源的一款专为 AI [[AI-Agent|智能体]]设计的轻量级代码直译与沙箱隔离系统。

---

## 1. 核心技术架构
```text
  ┌────────────────────────────────────────────────────────┐
  │                 DeepAgents 执行调用                     │
  └───────────────────────────┬────────────────────────────┘
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │         OpenSandboxBackend (BaseSandbox 适配器)         │ (进行协议归一化)
  └───────────────────────────┬────────────────────────────┘
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │         OpenSandbox Server (HTTP 8080 控制端)           │
  └───────────────────────────┬────────────────────────────┘
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │        Docker Code-Interpreter (隔离代码解释器容器)     │ (FSD/代码物理运行环境)
  └────────────────────────────────────────────────────────┘
```

- **隔离底座**：底层拉取专用的 Docker 镜像（如阿里的 `code-interpreter:v1.0.2` 镜像，体积通常达 6GB 左右，内置主流的 Python、C++ 等多语种编译与依赖包环境）。
- **进程拉起**：由本地常驻守护进程 `opensandbox-server` 监听宿主机 `http://localhost:8080`。当收到 Agent 的创建请求时，服务器会在 Docker 中动态冷启动一个独立的容器沙盒，提供高等级安全隔离防线。
- **长生命周期依赖自给**：当大模型执行测试脚本提示“缺少 openpyxl、pandas”等三方包时，大模型可在沙箱内部自主运行 `pip install` 下载安装包，而不会对开发机宿主机环境造成任何依赖污染。

---

## 2. 基于 BaseSandbox 的协议适配器设计 (Adapter Pattern)
为了让 [[DeepAgents]] 能够无缝调用本地拉起的阿里 OpenSandbox 服务，开发者可以通过继承 [[DeepAgents]] 定义的 **`BaseSandbox`** 抽象类，实现**适配器设计模式**。

该适配器的核心作用是将 OpenSandbox SDK 的内部接口（如 commands.run()），翻译并归一化输出为 [[DeepAgents]] 框架上游强依赖的三个核心能力接口：
1. **`execute` (命令执行)**：
   - 接受传入的命令字符串，调用 opensandbox 并将其运行后的 stdout/stderr 整理并组装成框架规范的 `ExecuteResponse` 协议结构。
2. **`upload_files` (文件同步上传)**：
   - 接受路径与原始二进制字节数据，安全写入沙箱 Docker 容器内部的 `/workspace` 中。
3. **`download_files` (文件提取下载)**：
   - 将沙箱内部生成的图片、数据表或分析结论，读取回内存，返回 `FileDownloadResponse` 字节流。

---

## 3. 企业生产集成典型架构
在真实的企业销售数据分析（Excel/CSV KPI 提取、自动化绘图）中，通常结合 **`CompositeBackend`** 与自定义资产上传中间件：
- **第一步**：使用 FilesystemBackend 在应用本地加载静态的销售分析 `SKILL.md` 与参考文档；
- **第二步**：利用 `before_agent` 中间件，自动将本地解析出的技能文件和待分析的 mock_excel 上传推送到远程 **`OpenSandbox`** 沙箱 `/workspace` 下；
- **第三步**：将控制权完全交付给沙箱，[[AI-Agent|智能体]]在沙盒中执行 `python analyze_excel.py` 并处理所有的包依赖冲突，最终安全输出分析结果。

---
**关联页面**
- [[DeepAgents]] (概念母体)
- [[DeepAgents-Backend]] (映射的物理后端)
- [[Agent-Middleware]] (在 [[Agent-Middleware|before_agent]] 中进行沙箱推送)
- [[MinerU]] (沙箱内可调用的提取工具)
