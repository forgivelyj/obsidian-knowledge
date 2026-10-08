# Teamwork: When AI Becomes a Research Partner

> **Author**: The Antigravity Team (Google Antigravity / Google DeepMind)  
> **Source**: https://antigravity.google/blog/teamwork-when-ai-becomes-a-research-partner  
> **Date**: 2026-08-27  
> **Topic**: Frontier Multi-Agent Orchestration Framework in Google Antigravity (`/teamwork-preview`)  

---

## Executive Summary

Antigravity’s **Teamwork** is a frontier multi-agent orchestration framework designed for complex, open-ended research and software engineering problems. While loosely organized multi-agent systems often suffer from cognitive cascading (agents agreeing with each other's early errors and confidently building upon flawed premises), Teamwork introduces structured adversarial loops, dynamic role instantiation, and strict verification harnesses. Powered by Gemini 3.7 Flash and Gemini 3.1 Pro, Teamwork organizes autonomous agent teams to propose, critique, stress-test, and synthesize candidates over hours or days, keeping human researchers in control of top-level objectives and final acceptance.

---

## 1. Core Architecture & Design Principles

### ① Decoupling Orchestration Logic from Agent Prompts
- In Teamwork, a **Pattern** is a formal declarative specification rather than an imperative program.
- Orchestration topology, communication channels, and critique criteria are cleanly decoupled from individual agent definitions.
- Cross-domain adaptability: specialized loops (e.g., adversarial verification, falsification trees) can be transferred between mathematics, hardware simulation, and code optimization without modifying agent internals.

### ② Runtime Adaptability & Elastic Scaling
- Agent team size and topology are not hardcoded or static.
- Gemini dynamically evaluates the problem complexity at runtime and adapts the agent topology, spawning parallel workers, adversaries, and synthesis judges as the task requires.

---

## 2. Five Canonical Orchestration Patterns

Teamwork automatically routes tasks to specialized patterns:

1. **Long Proof**:
   - Designed for PhD-level mathematics and theoretical computer science open problems.
   - **Competitive Strategy Search**: Generates diverse candidate strategy routes in parallel, each paired with a dedicated Falsifier agent whose job is to disprove it.
   - **Decomposition**: Subproblems form an explicit directed acyclic graph (DAG) of dependencies.
   - **Tournament Network**: Iterative synthesis trees combine the best surviving proofs and accumulate verified observations.
   - **Cross-Round Learning**: Refuted candidates and verification feedback are distilled into an answer-agnostic **Pitfall Registry** and shared knowledge directory.

2. **Self-Verification**:
   - Depth-first rigorous reasoning inspired by the Aletheia agent.
   - Enforces formal invariant checks at every intermediate step.

3. **Distributed Coding**:
   - Decomposable software engineering tasks fanned out across parallel worker agents.
   - Integrated with adversarial critic review and static/dynamic test validation.

4. **Iterative Coding**:
   - Tightly coupled agent–test–refine loop for non-decomposable, localized code implementation and bug fixing.

5. **Document Review**:
   - Structured analysis and multi-angle critique of scientific manuscripts and technical RFCs.

---

## 3. Notable Real-World Breakthroughs

### ① Theoretical Computer Science & Mathematics (7 Open Problems)
Using the **Long Proof** pattern with Gemini 3.1 Pro and Gemini 3.7 Flash:
- **Coresets for Lp Subspace Approximation**: Improved coreset construction bounds for $\ell_p$ ($p > 2$) subspace approximation (open since FOCS 2025; solution on arXiv:2608.26047).
- **Sparse Convex Optimization**: Conditional lower bound on condition numbers for sparse least-squares objectives (open since JMLR 2021; solution on arXiv:2608.02588).
- **Maximal Inner Product Embeddings**: Closed the complexity gap for Chamfer similarity (solution on arXiv:2607.20393).
- **Provable Hadamard Quantization**: Eliminated the second quantization stage, cutting the leading constant by $\sim 5.93\times$ (solution on arXiv:2608.02564).
- **Erdős Unit Distance Problem**: Independently reproduced breakthrough bounds on unit distance exponents with zero internet access.
- **Prefix-Matrix Factorizations**: Near-optimal lower bound (arXiv:2608.08238).
- **Knuth’s Cycles Conjecture**: 40+ and 70+ page formal proofs, with the 40-page proof formally verified in Lean.
- **TCSBench**: Scored **71%**, the highest recorded score on this theoretical CS benchmark.

### ② Systems Engineering: Cycle-Accurate RISC-V CPU Simulator
- Built a cycle-level out-of-order (OoO) RISC-V CPU simulator from scratch that successfully booted the **xv6** operating system kernel to shell and passed 100+ standard benchmarks.
- Overcame the **"Silent Execution Gap"** (where microarchitectural states silently drift for hundreds of cycles before causing functional crashes) through continuous lockstep co-simulation against an air-gapped Spike reference simulator.
- Validated against BOOM hardware execution ground truth with an average cycle alignment error of only **0.71%**.

### ③ Open-Source Upstream Contributions
- **Eigen C++ Library**: Discovered suboptimal GeMV operations on single-row/column matrices; authored SIMD 4-way accumulator unrolling that was reviewed and merged upstream into Eigen.
- **ParlayHash / Swiss Parlay**: Integrated Swiss Table techniques into concurrent hash tables, achieving $2\times$ insert throughput with 64 threads, $1.5\times$ single-thread throughput, and $25\%$ lower memory usage; accepted upstream.
