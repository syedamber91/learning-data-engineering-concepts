---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, data-model, immutability, audit]
sources:
  - raw/ch03.md
  - raw/ch12.md
---
# Event Sourcing

Store the immutable sequence of things that happened, and derive current state by folding over it. Gives you auditability, time travel, and the freedom to compute new views from old events.

See [[Event Sourcing and CQRS (2e)]] and [[State, Streams, and Immutability (2e)]].

## Appears In
- [[Change Data Capture (2e)]]
- [[Combining Specialized Tools by Deriving Data (2e)]]
- [[Consensus in Practice (2e)]]
- [[Databases and Streams (2e)]]
- [[Event Sourcing and CQRS (2e)]]
- [[Event-Driven Architectures (2e)]]
- [[Formal Methods and Randomized Testing (2e)]]
- [[Implementation of Replication Logs (2e)]]
- [[Materialized Views and Data Cubes (2e)]]
- [[Stars and Snowflakes - Schemas for Analytics (2e)]]
- [[State, Streams, and Immutability (2e)]]
- [[The End-to-End Argument for Databases (2e)]]
- [[The Many Faces of Consensus (2e)]]
- [[Timeliness and Integrity (2e)]]

## In the vutr data-engineering wiki
- [[log-based-cdc]] — the infrastructure-layer sibling — extracting row changes from a log rather than writing intent events to one.
