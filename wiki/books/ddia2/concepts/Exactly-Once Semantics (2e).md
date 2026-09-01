---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, fault-tolerance, streaming]
sources:
  - raw/ch12.md
---
# Exactly-Once Semantics

Making a stream processor's *effects* appear to happen once, even though the message may be delivered many times. Not exactly-once delivery — which is impossible — but atomic commit of output plus offset, or idempotent writes.

See [[Fault Tolerance (Stream Processing) (2e)]]; the book prefers the more honest name "effectively-once."

## Appears In
- [[Batch and Stream Processing (2e)]]
- [[Composing Data Storage Technologies (2e)]]
- [[Distributed Transactions (2e)]]
- [[Distributed Transactions Across Different Systems (2e)]]
- [[Durable Execution and Workflows (2e)]]
- [[Enforcing Constraints (2e)]]
- [[Exactly-Once Message Processing Revisited (2e)]]
- [[Fault Tolerance (2e)]]
- [[Fault Tolerance (Stream Processing) (2e)]]
- [[Messaging Systems (2e)]]
- [[Modes of Dataflow (2e)]]
- [[Processing Streams (2e)]]
- [[Serving Derived Data (2e)]]
- [[Systems of Record and Derived Data (2e)]]

## In the vutr data-engineering wiki
- [[exactly-once-needs-idempotent-sink]] — the same rule stated flatly: exactly-once ultimately depends on an idempotent sink.
- [[exactly-once-and-missing-data-detection]] — the source side of the same gap — at-least-once produces duplicates, offsets committed too early produce silent loss, and both need detection before an idempotent sink can help.
