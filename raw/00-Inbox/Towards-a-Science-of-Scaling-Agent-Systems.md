# Towards a Science of Scaling Agent Systems

> **Authors**: Yubin Kim, Ken Gu, Chanwoo Park, Chunjong Park, Samuel Schmidgall, A. Ali Heydari, Yao Yan, Zhihan Zhang, Yuchen Zhuang, Yun Liu, Mark Malhotra, Paul Pu Liang, Hae Won Park, Yuzhe Yang, Xuhai Xu, Yilun Du, Shwetak Patel, Tim Althoff, Daniel McDuff, Xin Liu  
> **Source**: https://arxiv.org/abs/2512.08296 / https://arxiv.org/html/2512.08296v3  
> **Date**: 2025-12 / 2026  
> **arXiv**: 2512.08296v3 [cs.AI]  

---

## Abstract

Agents, language model-based systems capable of reasoning, planning, and acting are widely adopted in real-world tasks, yet how their performance changes as these systems scale across key dimensions remains underexplored. We introduce quantitative scaling principles for agent systems as a predictive model, capturing how performance varies with coordination, model capability, and measurable system and task factors. Across 260 configurations spanning six agentic benchmarks, five canonical architectures (Single-Agent and four Multi-Agent: Independent, Centralized, Decentralized, Hybrid), and three LLM families, we perform controlled evaluations, standardizing tools, prompts, and compute to isolate architectural effects. The resulting model achieves a cross-validated $R^2=0.373$ across all six benchmarks ($R^2=0.413$ with a task-grounded capability metric). We identify a robust capability-saturation effect and additional patterns: (1) coordination yields diminishing returns once single-agent baselines exceed certain performance; (2) tool-heavy tasks appear to incur multi-agent overhead; and (3) architectures without centralized verification tend to propagate errors more than those with centralized coordination. Relative performance change compared to single-agent baseline ranges from +80.8% on decomposable financial reasoning to -70.0% on sequential planning, demonstrating that architecture-task alignment determines collaborative success. The framework identifies the best-performing architecture for 87% of held-out configurations and shows consistent relative architecture preferences on unseen frontier models. Agent effectiveness depends on alignment between coordination and task structure, and mismatched coordination degrades the performance.

---

## 1. System Definition & Evaluated Architectures

The study defines and isolates five canonical agent architectures under identical tool access, prompts, and budget bounds:

1. **Single-Agent System (SAS)**:
   - A single LLM instance interacting in an observe-think-act loop.
   - Serves as the fundamental benchmark baseline against which all multi-agent setups are compared.

2. **Independent MAS**:
   - Multiple agents work in parallel without peer communication or interaction.
   - Their outputs are aggregated (e.g., voting or selection) at completion.
   - Low coordination overhead; effective for parallelizable search and ensemble consensus.

3. **Centralized MAS**:
   - A designated supervisor/coordinator agent assigns subtasks, oversees execution, and validates outputs before final submission.
   - Strong centralized verification mechanism; catches and filters out early intermediate errors.

4. **Decentralized MAS**:
   - Peer-to-peer communication among agents without a central orchestrator.
   - Agents negotiate, debate, or pass intermediate context directly.
   - Highly vulnerable to error propagation and ungrounded consensus when verification is absent.

5. **Hybrid MAS**:
   - Combines hierarchical supervision with localized peer-to-peer collaboration clusters.
   - Balances centralized verification with flexible domain-specific autonomy.

---

## 2. Experimental Setup & Benchmarks

The controlled evaluation covers **260 configurations** across **6 agentic benchmarks** and **3 leading LLM families** (GPT, Claude, Gemini/Open Frontier):

- **Evaluated Benchmarks**:
  - Financial reasoning (decomposable structured analysis)
  - Web navigation (interactive multi-step browsing)
  - Operating system interaction (shell commands, file operations, system debugging)
  - Tool-use benchmarks (multi-turn API calls, parameter selection)
  - Sequential planning (strict temporal and causal dependency chains)
  - Interactive coding / execution

---

## 3. Key Quantitative Findings & Scaling Principles

### ① Predictive Regression Scaling Model
- Formulated an empirical scaling law incorporating model capability ($I$), coordination efficiency, task complexity ($T$), tool overhead ($O$), and agent count ($n_a$).
- Cross-validated predictive accuracy:
  - $R^2 = 0.373$ (using general Intelligence Index).
  - $R^2 = 0.413$ (using Agent Capability Index, ACI).
- Successfully identifies the top-performing architecture for **87% of unseen configurations**.

### ② Capability-Saturation Effect
- Coordination benefits are not monotonically additive.
- As the underlying base model’s single-agent performance improves past a task-dependent saturation threshold, multi-agent coordination yields rapidly diminishing or negative returns.
- Weaker models gain significantly more from multi-agent structuring, whereas frontier models often suffer from excess coordination overhead on simpler subtasks.

### ③ Tool-Heavy Coordination Overhead
- Interaction between coordination efficiency and tool density is negative ($\hat{\beta} = -0.096, p = 0.002$).
- On tool-heavy tasks, multi-agent communication introduces latency, context fragmentation, and coordination friction that frequently underperform an optimized single agent with direct tool access.

### ④ Error Dynamics & Centralized Verification
- Turn count scales as a power law with agent count.
- Error taxonomy reveals that unconstrained peer-to-peer communication causes errors to cascade and compound.
- Centralized verification serves as an "error sink" that absorbs hallucinations and syntax/logic failures before they contaminate peer contexts.

### ⑤ Architecture-Task Alignment
- Multi-agent systems do not uniformly outperform single-agent baselines:
  - **+80.8%** relative performance gain on highly decomposable tasks (e.g., modular financial reasoning).
  - **-70.0%** relative performance drop on strict sequential planning tasks where coordination friction disrupts serialized execution.
- Task structure (decomposability vs. strict sequence) is the primary determinant of multi-agent efficacy.
