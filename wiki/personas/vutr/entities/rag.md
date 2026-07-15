---
persona: vutr
kind: entity
sources:
- raw/llms-ai-agents-and-vector-databases-additional/everything-you-need-to-know-about-bee.md
- raw/llms-ai-agents-and-vector-databases-additional/my-ds-colleague-spent-one-year-learning.md
last_updated: '2026-07-15'
qc: passed
slug: rag
topics:
- llms-ai-agents-and-vector-databases
---

Retrieval-Augmented Generation exists because [[llm|an LLM's]] "memory" is whatever it absorbed during training, frozen at a knowledge-cutoff date. The exam analogy makes the failure mode concrete: relying on training alone is like studying chapters 1–8 and getting asked about chapter 9 — the model, like the student, gets it wrong. RAG is the "open-book" version of that exam: instead of memorizing every fact, the model is allowed to consult a library — a document, a blog, a database — and retrieve the relevant passage before answering. The model's job shifts from memorization to consumption and synthesis of retrieved text.

Framed as an agent tool (see [[ai-agent]]), RAG is described as the agent's "library card": it lets the system query external knowledge — company docs, a vector database, or a knowledge graph — to fact-check itself before generating an answer, which is what grounds responses in reality and cuts down hallucination. This retrieval role sits alongside NL2SQL as one of the two foundational "Retrieving Information" tools an agent needs, the other being "Executing Actions" (API wrappers, code execution, human-in-the-loop approval).

RAG and fine-tuning are not competing techniques to choose between once and for all. Fine-tuning reshapes a model's behavior for a specific task but is a poor fit for teaching new, rapidly changing facts, because it depends on a training process that is slow and only as good as its input data. RAG solves exactly that gap by keeping facts external and fresh. In practice the two are complementary rather than binary: many systems fine-tune to shape how a model behaves and use RAG to supply fresh, domain-specific knowledge on top of that behavior. Deciding which mix an organization needs is explicitly framed as a call for AI/ML engineers and data scientists to make, not something data engineers should default into on their own — the data engineer's job is to prepare and serve the data (including under low-latency, continuously-updating pipelines) that RAG needs to consult.

*See also: [[llm]] · [[ai-agent]] · [[vector-embedding]] · [[semantic-layer-and-data-modeling]] · [[text-to-sql-challenges]]*
