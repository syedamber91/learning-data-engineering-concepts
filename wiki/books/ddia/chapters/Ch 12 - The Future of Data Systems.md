---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 12
chapter_title: The Future of Data Systems
type: chapter-moc
tags: [ddia, chapter-moc, dataflow, correctness, ethics]
sources:
  - raw/ch12.md
---
# Ch 12 – The Future of Data Systems

The opinionated finale: Kleppmann switches from describing systems as they are to arguing how they *should* be built. The argument runs in four movements. First, since no single tool fits all access patterns, data integration should happen by designating systems of record and deriving everything else from ordered event logs — total order beats dual writes, and asynchronous derivation beats [[Two-Phase Commit]] across heterogeneous systems. Second, this amounts to *unbundling the database*: batch and stream processors are externalized index-maintenance routines, application code becomes derivation functions ([[Dataflow]] over request/response), and the write path can extend through derived views all the way to end-user devices. Third, correctness in such a world comes not from trusting transactions but from end-to-end operation IDs, constraints enforced by partitioned logs (uniqueness needs [[Consensus]], which a log provides), separating timeliness from integrity, and auditing everything. Fourth — because the same machinery scores, tracks, and surveils people — engineers bear ethical responsibility for what these systems do to humans.

## Map
- [[Data Integration]]
  - [[Combining Specialized Tools by Deriving Data]]
  - [[Batch and Stream Processing]]
- [[Unbundling Databases]]
  - [[Composing Data Storage Technologies]]
  - [[Designing Applications Around Dataflow]]
  - [[Observing Derived State]]
- [[Aiming for Correctness]]
  - [[The End-to-End Argument for Databases]]
  - [[Enforcing Constraints]]
  - [[Timeliness and Integrity]]
  - [[Trust, but Verify]]
- [[Doing the Right Thing]]
  - [[Predictive Analytics]]
  - [[Privacy and Tracking]]

## Chapter Summary
No one tool serves every use case, so applications must compose several specialized systems; the integration problem is solved by letting changes flow from systems of record through batch and stream transformations that maintain indexes, [[Materialized Views]], ML models, and caches as [[Derived Data]]. Keeping these derivations asynchronous and loosely coupled contains faults instead of escalating them, and expressing them as dataset-to-dataset transformations makes evolution easy: change the code and reprocess the input to rebuild any view, or to recover from bugs. Since databases do the same thing internally, this recasts application architecture as an unbundled database built from loosely coupled components. Derived state updates by observing upstream changes and can itself be observed downstream — potentially all the way to user devices, giving dynamically updating, offline-capable UIs. Correctness under faults is achievable without distributed transactions: end-to-end operation identifiers make operations idempotent ([[Idempotence]]), constraints are checked asynchronously (clients wait, or proceed and risk an apology), and most coordination can be avoided while preserving integrity — even geo-distributed. Audits verify integrity and catch corruption. Finally, data systems can harm people: opaque life-affecting decisions with no appeal, discrimination, normalized surveillance, breach exposure — and engineers have a responsibility to work toward a world that treats people with humanity and respect.

## Related
- [[Part III - Derived Data]] — the book part this chapter concludes
- [[Home]] — vault index
- previous: [[Ch 11 - Stream Processing]] — the event-log machinery this chapter generalizes
- [[Keeping Systems in Sync]] — Ch 11 statement of the integration problem
- [[Total Order Broadcast]] — the theoretical backbone of log-based constraint enforcement
