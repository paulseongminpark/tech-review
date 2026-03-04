---
layout: post
title: "The U.S. Department of Defense's AI policy upheaval is shaking the industry, the rift between OpenAI and Anthropic is deepening within the U.S. AI camp, and China's model extraction attacks are heightening tensions in the international AI competition."
date: 2026-03-02
lang: en
permalink: /en/2026/03/02/daily-tech-review/
pair: 2026-03-02-daily-tech-review
tags: ["ai-ml", "models", "research", "benchmarks"]
---


## Today in One Line
The U.S. Department of Defense's AI policy upheaval is shaking the industry, the rift between OpenAI and Anthropic is deepening within the U.S. AI camp, and China's model extraction attacks are heightening tensions in the international AI competition.

---

## 1. U.S. Department of Defense's Choice: Contract with OpenAI, Anthropic Designated as Supply Chain Risk

OpenAI has signed a contract with the U.S. Department of Defense to deploy AI models in classified environments (classified systems), and immediately after, the Trump administration designated Anthropic as a "supply chain risk" and ordered all federal agencies to cease use within 6 months.

**Why it matters:** This signifies a fundamental shift in the U.S. defense AI strategy. Until now, Anthropic's Claude was the only frontier LLM deployed in the Department of Defense's highest classified networks, but after Anthropic refused demands to remove safety guardrails, it faced sanctions, rapidly changing the landscape to a competition among OpenAI, xAI, and other companies for the defense AI market.

- On the night of February 28 (local time), Sam Altman announced the Pentagon contract via X; OpenAI agreed under the condition of retaining full control over its own safety stack, limiting deployment to cloud environments and establishing a multi-layered defense structure with OpenAI personnel on-site
- President Trump directed the "supply chain risk" designation for Anthropic on February 27; the Department of Defense must transition to Claude alternatives during a 6-month grace period, with the contract scale estimated at up to $200 million
- The Pentagon's requirements were to not restrict AI models from use for "any lawful purpose," but Anthropic insisted on two exceptions for large-scale domestic surveillance and fully autonomous weapons; in contrast, OpenAI accepted the same conditions

**What's next:** xAI's Grok has already received Pentagon classified system approval, and negotiations between Google and OpenAI are accelerating, with additional contracts expected within the next few months.

**Source:** [OpenAI announces deal with the Pentagon](https://techcrunch.com/2026/02/28/openais-sam-altman-announces-pentagon-deal-with-technical-safeguards/)

---

## 2. Chinese AI Companies Caught Illegally Extracting Over 16 Million Claude Conversations

Anthropic officially announced that three companies—DeepSeek, Moonshot AI, and MiniMax—collected over 16 million Claude conversations without authorization through approximately 24,000 fake accounts, marking this as evidence that China has replicated U.S. frontier AI technology on a large scale using "distillation" techniques.

**Why it matters:** This revelation shows that the AI hegemony competition between the U.S. and China has escalated from mere technology development to active industrial espionage levels. If Chinese AI companies bypassed legal channels to extract core capabilities of advanced models including U.S. safety guardrails on a massive scale, it directly impacts the effectiveness of U.S. export controls and national security strategies.

- DeepSeek targeted Claude's reasoning capabilities and "censorship-resistant alternative path generation" with over 150,000 synchronized traffic instances; Moonshot AI collected agent reasoning, tool use, and coding from over 3.4 million conversations; MiniMax focused on extracting agent coding and tool orchestration from over 13 million instances
- Anthropic reported that they used a "hydra cluster" architecture (distributing operations of large-scale fake account networks via proxy services), with one proxy network alone managing over 20,000 fake accounts simultaneously
- Distilled models lose essential safety guardrails, posing national security risks for misuse in biochemical weapons development, malicious cyber activities, etc.; Anthropic claims OpenAI faced similar attacks and argues this "reconfirms the legitimacy of chip export controls"

**What's next:** The U.S. government and AI industry are expected to build multi-layered defenses including large-scale proxy network detection, cross-industry information sharing, and strengthened access controls; in particular, China's agent model developments (GLM-5, MiniMax-M2.1, etc.) are rapidly advancing through these tactics.

**Source:** [Anthropic: Detecting and preventing distillation attacks](https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks)

---

## 3. Frontier LLM Performance Competition Heats Up: Anthropic's New Model Releases Redefine Industry Standards

Anthropic released Claude Opus 4.6 (1M token context, β release) on February 5 and followed with Claude Sonnet 4.6 at the end of February, dramatically closing the performance gap with OpenAI's GPT-5.2 and setting new industry standards for price-performance ratio.

**Why it matters:** Claude Opus 4.6 outperformed GPT-5.2 by about 144 Elo points (approximately 70% probability of higher score) on the GDPval-AA benchmark, while Sonnet 4.6 delivers performance far exceeding the previous Opus at a much lower cost, completely upending the "economics of model selection." This will immediately impact enterprise and government AI adoption decisions.

- Claude Opus 4.6 features 1M token context (about 3 million words), 128K output tokens, agent team functionality (parallel multi-agent coordination), and top scores on Terminal-Bench 2.0; industry-leading performance on Humanity's Last Exam surpassing GPT-5.2
- Claude Sonnet 4.6 maintains the same pricing ($3/$15 per 1M tokens) while achieving about 70% higher user preference than previous Opus 4.5 and OfficeQA scores equivalent to Opus 4.6; also adds context compaction (effective context expansion via automatic summarization) and adaptive thinking features
- Simultaneously, Meta's Llama 4 Scout (10M token context, 17B active parameters), GLM-5 (744B MoE, MIT license, trained exclusively on Huawei Ascend chips), MiniMax-M2.1 (230B total/10B active, excellent multilingual coding) are sparking competition in the open-source camp

**What's next:** This performance leap is restructuring each company's investment recovery strategies (frontier vs. open source), with institutions like Gartner expected to significantly revise LLM evaluation criteria by the first half of 2026; corporate AI vendor selection criteria are likely to shift from "peak performance" to a "performance-price-safety" triangle.

**Source:** [Anthropic: Introducing Claude Opus 4.6](https://www.anthropic.com/news/claude-opus-4-6) | OpenAI: Introducing GPT-5.2

## Comments

