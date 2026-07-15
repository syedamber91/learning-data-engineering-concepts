---
persona: vutr
kind: entity
sources:
- raw/llms-ai-agents-and-vector-databases-additional/my-ds-colleague-spent-one-year-learning.md
last_updated: '2026-07-15'
qc: passed
slug: ai-agent
topics:
- llms-ai-agents-and-vector-databases
---

An AI agent is defined plainly as a Language Model in a loop with the tools it needs to get a job done — a goal-oriented system, not just a chat window. The anatomy is presented as three cooperating parts, matched to a body metaphor: the Model is the Brain (the reasoning engine that decides what to do next), Tools are the Hands (without them the agent can only "talk," not act — see [[agent-orchestration-layer]] for how retrieval and action tools are organized), and the Orchestration Layer is the Nervous System (the governing logic that decides when the model reasons, when it calls a tool, and how it folds the result back in — see [[agent-orchestration-layer]] and [[agentic-problem-solving-loop]] for the mechanics).

On the Brain: choosing which [[llm|LLM]] to use is framed as a trade-off among cognitive capacity, operating cost, and speed, and the guidance is explicit that model choice should be evaluated against task-specific, business-mapped metrics rather than public benchmarks — see [[model-selection-and-routing]] for the worked example (Gemini Flash matching frontier-model performance on a Text2SQL component at a fraction of the cost) and the model-routing strategy that follows from it.

This entity note is grounded in the article's explicit framing: the technical content on agents comes from the author's data-science colleague, Son Tran, with the Substack author (Vu Trinh) crediting himself only with editing the draft and producing the illustrations — a provenance detail worth keeping attached to any claim sourced from this post.

*See also: [[agent-orchestration-layer]] · [[multi-agent-design-patterns]] · [[agentic-problem-solving-loop]] · [[agent-intelligence-ladder]] · [[model-selection-and-routing]] · [[rag]]*
