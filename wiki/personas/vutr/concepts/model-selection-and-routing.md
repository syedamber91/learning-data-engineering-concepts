---
persona: vutr
kind: concept
sources:
- raw/llms-ai-agents-and-vector-databases-additional/my-ds-colleague-spent-one-year-learning.md
last_updated: '2026-07-15'
qc: passed
slug: model-selection-and-routing
topics:
- llms-ai-agents-and-vector-databases
---

Choosing which [[llm]] powers an [[ai-agent|agent's]] brain is framed as a trade-off among cognitive capacity, operating cost, and speed — and the explicit recommendation is that model selection should not be driven by public online benchmarks, but by task-specific performance measured against metrics that map directly to business outcomes. The worked example: testing LLM capacity for a component of the Text2SQL feature found that Gemini Flash matched the performance of other frontier models while running at much lower cost and much faster — a result the source calls "surprising" precisely because it contradicts a naive "just pick the biggest/best-benchmarked model" heuristic.

That finding motivates Model Routing as a cost-and-performance optimization strategy: use frontier models for complex planning steps, and route simpler tasks to faster, cheaper models, rather than paying frontier-model cost for every single turn of a conversation.

The urgency behind both practices is time-bound: the source states that the "model of the year" usually keeps its title for only about six months, so a "set it and forget it" AI strategy is described as already falling behind. The recommended discipline is to constantly test new models against the system's actual business goals (with the help of Agent Ops) and upgrade when a better "brain" appears — which lets a system swap in improvements "without breaking your architecture," implying model choice is meant to be decoupled from the rest of the agent's orchestration and tooling rather than hard-wired to it.

*See also: [[ai-agent]] · [[agent-orchestration-layer]] · [[llm]]*
