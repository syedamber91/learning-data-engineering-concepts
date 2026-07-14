---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 12
chapter_title: The Future of Data Systems
type: topic
tags: [ddia, data-integration, derived-data, dataflow]
sources:
  - raw/ch12.md
---
# Data Integration

Kleppmann opens his forward-looking chapter with a claim the whole book has been building toward: no single tool fits every access pattern, so real applications inevitably stitch together several specialized systems — an OLTP store, a search index, caches, analytics, ML pipelines. The hard problem is not choosing tools but keeping all the copies of data consistent as it flows between them. His proposed answer is to treat one system as the authoritative source and derive everything else from an ordered log of changes, using batch and stream processors as the plumbing. This reframes [[Derived Data]] maintenance as an application of [[Total Order Broadcast]] rather than of distributed transactions, and it makes asynchrony, [[Idempotence]], and reprocessability the core design levers.

## Subtopics
- [[Combining Specialized Tools by Deriving Data]] — why funneling writes through a single ordered log beats dual writes and [[Two-Phase Commit]], and where total ordering breaks down at scale.
- [[Batch and Stream Processing]] — batch and stream engines as the machinery of integration: functional-style derivation, reprocessing for schema evolution, the lambda architecture and its unification.

## Key Takeaways
- Every tool is optimized for a usage pattern; "general-purpose" software still embodies assumptions, so complex apps must compose several systems.
- Deciding a single order of writes (via [[Change Data Capture]] or [[Event Sourcing]]) and deriving all other views from that log avoids the permanent divergence caused by dual writes.
- Log-based derivation trades the [[Strong Consistency]] timing guarantees of distributed transactions for fault containment and practicality; Kleppmann judges XA too fragile to be the integration backbone.
- Total ordering is itself a [[Consensus]] problem and stops scaling across partitions, datacenters, and microservices — capturing [[Causality]] without a global order remains open research.
- Reprocessing historical data is what makes systems evolvable: old and new views can coexist during a gradual, reversible migration (the railway dual-gauge analogy).
- Unified batch/stream engines (replayable logs, [[Exactly-Once Semantics]], event-time windowing) deliver the lambda architecture's benefits without running two parallel codebases.

## Related
- chapter: [[Ch 12 - The Future of Data Systems]] · part: [[Part III - Derived Data]]
- [[Keeping Systems in Sync]] — the Ch 11 problem this topic generalizes
- [[Unbundling Databases]] — the architectural vision built on these integration ideas
- [[Batch Processing with Unix Tools]] — batch-side foundations of the derivation machinery
