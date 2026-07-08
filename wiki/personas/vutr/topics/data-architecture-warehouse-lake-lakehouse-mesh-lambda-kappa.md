---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: data-architecture-warehouse-lake-lakehouse-mesh-lambda-kappa
---

Related: [[data-warehouse]] · [[data-lake]] · [[lakehouse]] · [[data-mesh]] · [[lambda-architecture]] · [[kappa-architecture]] · [[medallion]] · [[architecture-vs-pattern]] · [[cap-vs-acid-consistency]] · [[every-decision-has-a-tradeoff]]

## Comparisons
- [[data-warehouse]] locks schema-on-write for clean, query-ready data; [[data-lake]] defers structure to read time and, lacking ACID/DML/discovery/quality, tends to rot into a swamp.
- [[lakehouse]] is the reconciliation: lake-style low-cost object storage plus warehouse-style ACID, versioning, caching, and query optimization. But BigQuery and Snowflake, though technically lakehouses, break its spirit because you don't own the storage layer.
- [[lambda-architecture]] vs [[kappa-architecture]]: Lambda runs batch (correctness) and speed (freshness) layers in parallel — two codebases; Kappa runs one streaming pipeline and reprocesses history by replaying Kafka offsets, trading the dual-codebase burden for required stream expertise.
- [[data-mesh]] is orthogonal to the storage debate: it's an organizational decentralization per domain, where the blocker is mindset, not technology.
- Note the taxonomy split ([[architecture-vs-pattern]]): [[medallion]], [[lambda-architecture]], and [[kappa-architecture]] are patterns, not full architectures.

## Open questions
- If [[lakehouse]] managed-storage services like BigQuery and Snowflake violate the manifesto's spirit yet meet its technical definition, is 'controlling your storage layer' actually part of the definition or just an ideal?
- Given [[cap-vs-acid-consistency]], how much production confusion traces back to two different 'consistency' notions sharing one name?
- Does [[kappa-architecture]] fully retire [[lambda-architecture]] in practice, or does the required stream-system expertise keep Lambda alive?
- Since [[data-mesh]] is blocked mainly by mindset change, what makes the domain-driven decentralization succeed versus stall?
- If Medallion, Lambda, and Kappa are patterns and Modern Data Stack a philosophy ([[architecture-vs-pattern]]), which things in this space genuinely qualify as architectures?

## Synthesis
The through-line is a reconciliation story: [[data-warehouse]] (schema-on-write) and [[data-lake]] (schema-on-read, prone to swamp) converge into the [[lakehouse]], which bolts ACID and DBMS features onto cheap object storage — though managed engines meet its letter while betraying its spirit. Around that sit the streaming patterns [[lambda-architecture]] and [[kappa-architecture]], and the organizational move of [[data-mesh]], all clarified by [[architecture-vs-pattern]] (most of these are patterns, not blueprints). Underneath it all is [[cap-vs-acid-consistency]] — Lambda is a CAP workaround, not a victory — and the governing rule [[every-decision-has-a-tradeoff]]: pick based on the organization's needs, not the hype.
