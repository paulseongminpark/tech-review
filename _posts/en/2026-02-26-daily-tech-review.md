---
layout: post
title: "Diffusion-based inference LLMs achieve 1,000+ tokens/sec, transforming AI generation paradigms, while open-weight coding models significantly reduce cloud API dependency, rapidly expanding the local AI development ecosystem."
date: 2026-02-26
lang: en
permalink: /en/2026/02/26/daily-tech-review/
pair: 2026-02-26-daily-tech-review
tags: ["developer-tools", "opensource"]
---


## Today in One Line

Diffusion-based inference LLMs achieve 1,000+ tokens/sec, transforming AI generation paradigms, while open-weight coding models significantly reduce cloud API dependency, rapidly expanding the local AI development ecosystem.

---

## 1. Inception Labs Achieves 1,000 Tokens/Sec with Mercury 2 — Official Launch of Diffusion-Based Inference LLM

Inception Labs announced Mercury 2 on February 25, completely abandoning traditional autoregressive token generation in favor of Diffusion-based parallel refinement generation, achieving 1,009 tokens/sec on NVIDIA Blackwell GPUs. This is approximately 11x faster than Claude Haiku and 14x faster than GPT-5 Mini, while maintaining equivalent quality to speed-optimized models on inference LLM benchmarks (AIME 2025: 91.1%, GPQA, LiveCodeBench).[1][2][3]

**Why it matters:** It fundamentally breaks the "speed vs. quality" tradeoff in production AI systems for fields like agent loops where latency accumulates, voice interfaces, and real-time coding autocomplete. Especially in workflows with frequent tool calls, it solves the problem of compounded latency per step, dramatically improving the practicality of AI agents.

- **Architecture:** Diffusion method starting from noise and refining multiple tokens in parallel, applying inference optimization on the proven technical foundation built by developers of Sora·Stable Diffusion·Flux
- **Pricing:** $0.25/1M input tokens, $0.75/1M output tokens — about 60% cheaper than OpenAI API, native 128K context support for massive reductions in RAG·tool usage costs
- **Compatibility:** Fully compatible with OpenAI API, immediate support from Vercel AI SDK, open-source demo to be released on GitHub, enabling reuse of existing LLM integration assets

**What's next:** Diffusion-based inference is expected to lead to standardization efforts by other model providers, with accelerated adoption anticipated especially in voice AI and real-time editing tools.

**Source:** [Introducing Mercury 2](https://www.inceptionlabs.ai/blog/introducing-mercury-2), [Mercury 2 Overview — YouTube](https://www.youtube.com/watch?v=quOe8V2n9rU), Hacker News #6 — Feb 25

---

## 2. Alibaba Qwen Releases Qwen3-Coder-Next Open Source for Coding Agents — Sonnet-Level Performance with 3B Active Parameters

Alibaba's Qwen team released Qwen3-Coder-Next in early February, a Mixture-of-Experts structure activating only 3B out of 80B total parameters, surpassing existing DeepSeek V3.2 (37B active)·Kimi K2.5·GLM-4.7 (each 32B active) on coding benchmarks. It supports 256K native context length and can operate at 20~40 tokens/sec on local hardware (64GB MacBook, RTX 5090, AMD Radeon 7900 XTX), setting a new standard for open-weight models.

**Why it matters:** It eliminates API dependency and ensures data privacy while enabling complex coding agents without Claude or OpenAI API cost constraints. Amid Anthropic's Claude Code limitations and OpenAI's price increases, developers now have a reliable open-source alternative, making enterprise-grade local AI development environments a reality.

- **Architecture:** Gated DeltaNet + Gated Attention hybrid, 3x smaller than existing Qwen3 (235B) but with 4x more experts, additional coding-specialized experts for maximized performance
- **Performance:** Sonnet 4.5 level on coding benchmarks, top scores among small models on AIME 2025·GPQA, reliable function calling and JSON schema generation even in local execution
- **Deployment:** Immediately downloadable via Ollama·Hugging Face·Kaggle, quantization options (Q4, Q5, FP8) for various hardware environments, no restrictions with MIT/Apache 2.0 commercial license

**What's next:** As Qwen3-Coder-Next adoption spreads, it is likely to become the default model standard for local development agent platforms (Emdash, OpenClaw, etc.), paving the way for enterprises to build closed-loop coding systems on their own servers.

**Source:** Qwen3-Coder-Next Blog, [The Complete 2026 Guide to Running Qwen3](https://dev.to/sienna/qwen3-coder-next-the-complete-2026-guide-to-running-powerful-ai-coding-agents-locally-1k95), [A Dream of Spring for Open-Weight LLMs](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)

---

## 3. GitHub Agentic Workflows, Technical Preview Begins — Activates Low-Level Repository Automation Beyond CI/CD

GitHub's Agentic Workflows, announced on February 13, enables direct execution of AI agents (GitHub Copilot CLI, Claude Code, OpenAI Codex) within GitHub Actions. By describing automation intent in Markdown files, a compiler converts them to YAML for agents to automatically handle issue triage·PR review·CI failure analysis·documentation updates·test coverage monitoring. It minimizes security gaps with read-only default execution permissions and Safe Outputs sandboxing, while providing raw access to repository·issue·action·security info via GitHub MCP server.

**Why it matters:** While existing CI/CD was suited only for deterministic builds·deployments, Agentic Workflows allows agents to autonomously handle heuristic decisions difficult for humans (e.g., which label to apply to which issue, what to fix based on PR comment context), dramatically reducing developers' repetitive triage·review burdens. It is expected to be a game-changer for open-source maintainers, shortening thousands of PR processing times from days to hours.

- **Security Design:** Container isolation execution, read-only default permissions, firewall-based internet access restrictions, user input sanitization, Safe Outputs for write operation permission control — over 3x stronger sandboxing than general CLI agents
- **Developer Experience:** Define automation by simply adding Markdown files to `.github/workflows/` directory, compile and commit with `gh aw` CLI, compatible with all coding agents (GitHub Copilot·Claude Code·OpenAI Codex interchangeable)
- **Triggers:** Flexible automation triggers via issue·PR·comment events, scheduled execution, manual dispatch, comment commands; MIT open-source release via collaboration with GitHub Next·Microsoft Research·Azure Core Upstream

**What's next:** With over 50 official agent workflow templates (Peli's Agent Factory) rapidly spreading in the ecosystem, enterprise repository agent automation adoption costs are expected to plummet, potentially improving development team maintenance productivity by 30~50%.

**Source:** [GitHub Agentic Workflows Technical Preview](https://github.blog/changelog/2026-02-13-github-agentic-workflows-are-now-in-technical-preview/), GitHub previews Agentic Workflows, [GitHub Blog — Agentic Workflows](https://github.blog)

---

## Comments

