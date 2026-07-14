---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, streams, fault-tolerance]
sources:
  - raw/ch11.md
  - raw/ch12.md
---
# Exactly-Once Semantics

The goal that each input event affects final state as if processed exactly once,
even though failures force retries (so *processing* may happen more than once).
Achieved by making the retry invisible: atomically commit outputs + offsets
(microbatching, transactions spanning processor and sinks) or make effects
[[Idempotence|idempotent]] with end-to-end operation IDs.

In the book: [[Fault Tolerance]] (Ch 11) for the stream-processor techniques, and
[[The End-to-End Argument for Databases]] (Ch 12) for why infrastructure alone can't
finish the job — the application-level identifier has to flow end to end.

## Referenced In
- [[Batch and Stream Processing]]
- [[Home]]
- [[Data Integration]]
- [[Distributed Transactions in Practice]]
- [[Fault Tolerance]]
- [[Processing Streams]]
- [[The End-to-End Argument for Databases]]
- [[Timeliness and Integrity]]

## Related in the other wiki
- [[exactly-once-needs-idempotent-sink]] — this page's "make effects idempotent with end-to-end operation IDs" is precisely the rule vutr's note states directly: exactly-once ultimately depends on an idempotent sink.
