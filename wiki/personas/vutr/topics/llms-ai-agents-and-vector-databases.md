---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: llms-ai-agents-and-vector-databases
---

Related: [[llm]] · [[rag]] · [[ai-agent]] · [[vector-embedding]] · [[hnsw]] · [[product-quantization]] · [[parquet]] · [[semantic-layer]] · [[model-selection]] · [[text-to-sql]]

## Comparisons
- [[rag]] vs fine-tuning: fine-tuning is inefficient for teaching new, rapidly-changing facts, while [[rag]] lets the model consult external knowledge. But the choice isn't binary — many systems combine both.
- [[hnsw]] vs [[product-quantization]]: both make [[vector-embedding]] search tractable, but from different angles — [[hnsw]] is a graph-layered index that speeds up the approximate nearest neighbor traversal, while [[product-quantization]] compresses the vectors themselves via sub-vector centroids.
- [[parquet]] vs vector storage: Parquet serves columnar analytics well, but its poor random access and wide-column row-group sizing make it a bad fit for the random-access, high-dimensional workload of [[vector-embedding]].
- [[semantic-layer]] vs data modeling: not competitors — data modeling handles physical complexity while the [[semantic-layer]] provides logical simplicity as a serving abstraction on top.

## Open questions
- When exactly should a system combine [[rag]] and fine-tuning rather than pick one, since the choice is explicitly not binary?
- Which storage substrate replaces [[parquet]] for embeddings, given random-access and wide-column limitations?
- How far up the five levels does an [[ai-agent]] realistically go in production — is Level 4 (self-evolving) practical yet?
- Can [[text-to-sql]] ever handle the data-modeling decision-making, which I doubt AI does well?
- With model leadership lasting only ~six months, how should [[model-selection]] be operationalized so a system re-evaluates on task-specific performance rather than settling?

## Synthesis
The through-line: an [[llm]] is a language probability distribution, not a fact store, so real AI systems bolt facts on from outside — via [[rag]] and via an [[ai-agent]] that loops the model with tools. Underneath all of it, [[vector-embedding]] is the backbone, which is why index and compression structures like [[hnsw]] and [[product-quantization]] matter and why [[parquet]] doesn't fit. And on the consumption side I stay skeptical — [[model-selection]] must track a six-month-shifting frontier, and [[text-to-sql]] plus the [[semantic-layer]] remind us that data-modeling judgment is the part I doubt AI does well.

## Related topics
- [[parquet]] — Vu argues Parquet is a bad fit for vector embeddings because its poor random access and wide-column row-groups mismatch the high-dimensional random-access workload.
- [[sql-fundamentals-and-execution-model]] — Text-to-SQL lets an LLM generate queries, though Vu doubts AI can handle the data-modeling judgment behind good SQL.
- [[data-engineering-career-roadmap-and-learning-philosophy]] — The roadmap defers AI to last yet insists 'using AI is not optional,' and both notes stress that data-modeling decision-making stays human.
