# LLM Wiki: A Pattern for Building Personal Knowledge Bases Using LLMs

> **Author**: Andrej Karpathy  
> **Source**: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f  
> **Date**: 2026-04  

## Core Philosophy

Most people's experience with LLMs and documents looks like RAG: you upload a collection of files, the LLM retrieves relevant chunks at query time, and generates an answer. This works, but the LLM is rediscovering knowledge from scratch on every question. There's no accumulation.

The idea here is different. Instead of just retrieving from raw documents at query time, the LLM incrementally builds and maintains a persistent wiki — a structured, interlinked collection of markdown files that sits between you and the raw sources. When you add a new source, the LLM reads it, extracts key information, and integrates it into the existing wiki — updating entity pages, revising topic summaries, noting contradictions, and evolving synthesis. The knowledge is compiled once and kept current.

The wiki is a **persistent, compounding artifact**. Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase.

## 3-Layer Architecture

1. **Raw sources**: Curated collection of source documents (immutable, source of truth, read-only for LLM).
2. **The wiki**: Directory of LLM-generated markdown files (summaries, entities, concepts, comparisons, synthesis, index, log). Owned and maintained by LLM.
3. **The schema**: Configuration file (`AGENTS.md` / `CLAUDE.md`) defining wiki structure, conventions, and agent workflow.

## Core Operations

- **Ingest**: Drop a source into raw, LLM extracts key insights, creates summaries, updates entity/concept pages with `[[wikilinks]]`, updates index and log.
- **Query**: Question answered from wiki index and pages; valuable answers filed back as synthesis or comparison pages.
- **Lint**: Health-check for orphan pages, contradictory claims, and missing cross-references.
- **Publish**: Synthesizes wiki content into outputs (posts, reports, slides).
