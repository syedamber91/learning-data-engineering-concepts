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
