---
layout: post
title: "Weave solves Git merge issues in the multi-agent coding era, Claude solves a 52-year-old math problem, DeepSeek V4 launch imminent."
date: 2026-03-05
lang: en
permalink: /en/2026/03/05/daily-tech-review/
pair: 2026-03-05-daily-tech-review
tags: ["opensource", "developer-tools", "github", "frameworks"]
---

## Today in One Line
Weave solves Git merge issues in the multi-agent coding era, Claude solves a 52-year-old math problem, DeepSeek V4 launch imminent.

---

## 1. Weave: Agent-Friendly Git Merge Algorithm Released

Weave, developed by Ataraxy Labs, is an entity-level semantic merge driver that overcomes the limitations of Git's line-based merging. When Claude Code, Cursor, and Codex write code simultaneously, even if multiple agents add different functions to the same file, it parses the code structure with a tree-sitter parser and merges at the function level instead of marking it as a conflict.

**Why it matters:** As multi-agent parallel work becomes the industry standard, Git's line-based merging is becoming a serious bottleneck. Weave achieved perfect 31/31 merges on benchmarks compared to Git's 15/31, and is provided as an MCP server so agents can claim entities before editing.

- Weave operates at the merge driver level without changing Git workflows, making it immediately compatible with existing toolchains.
- It provides a foundation for agents to detect and coordinate conflicts in advance, in the form of an MCP server equipped with 14 tools.
- It handles language-specific special cases like Python class merges to prevent scope errors due to indentation mistakes.

**What's next:** Expansion to unsupported base languages like Bash is expected with the addition of tree-sitter grammars.

**Source:** [Weave – A language aware merge algorithm based on entities](https://github.com/Ataraxy-Labs/weave)

---

## 2. Claude Opus 4.6 Solves 52-Year-Old Knuth Math Problem

Stanford Computer Science professor Donald Knuth announced that an open problem he had been pondering for the past few weeks was solved in a short time after the release of Anthropic's Claude Opus 4.6 three weeks ago. This is the Hamiltonian cycle decomposition problem, where after 31 exploration attempts, Knuth guided Claude to find a purely mathematical framing and ultimately derived a generalized construction.

**Why it matters:** This is a concrete demonstration that large language models can qualitatively assist human experts in reasoning-based problem solving. It suggests that even legendary computer scientists like Knuth can benefit from Claude's systematic exploration and reframing capabilities.

- Claude converged by following human leader's plan validation instructions through 31 iterative cycles of DFS exploration, result logging, and problem redefinition.
- Knuth proved that Claude's generalized decomposition is valid for odd m > 1, and that 760 unique "Claude-style decompositions" exist.
- The Stanford paper ([Claude's Cycles](https://www-cs-faculty.stanford.edu/~knuth/papers/claude-cycles.pdf)) shows how important the way developers present tasks (clear progress documentation, periodic validation requests) is for improving model performance.

**What's next:** This collaboration approach is expected to spread as a best practice for problem solving in specialized fields like mathematics and theoretical physics.

**Source:** [Claude's Cycles [pdf]](https://www-cs-faculty.stanford.edu/~knuth/papers/claude-cycles.pdf)

---

## 3. DeepSeek V4 Scheduled for Release on March 3, Native Multimodal and Coding Optimized

According to a Financial Times report on February 28, DeepSeek V4 is a 1 trillion parameter model scheduled for release in early March, supporting photo, video, and text generation natively as a multimodal model. This model, presumed to be 'Model1' discovered in the updated FlashMLA library code, is optimized for coding and long-context software engineering tasks.

**Why it matters:** After DeepSeek V3 (January 2025) with 67.9 billion parameters outperformed models 10 times more expensive, the Chinese open-source camp is rapidly catching up with Western closed-model companies. V4's coding benchmarks (83.7% on BenchVerified) and math (99.4% on Frontier Math, 11x better than GPT-5.2) could reset industry standards.

- Collaboration with Chinese chip makers like Huawei and Cambricon reduces NVIDIA dependency, with multimodal support greatly expanding image and video processing capabilities.
- 512-dimensional structure transformation, NVIDIA Blackwell (H200) GPU optimization, and token-level sparse MLA implementation for long-context (1M+ tokens) scenarios.
- Expected to launch as an open-weight model, immediately impacting the open-source community and local deployment ecosystem.

**What's next:** After official release in early March, integration with inference frameworks like Ollama and vLLM, and spread of local deployment guides expected.

**Source:** [DeepSeek's Next Move: What V4 Will Look Like](https://recodechinaai.substack.com/p/deepseeks-next-move-what-v4-will)

## Comments

