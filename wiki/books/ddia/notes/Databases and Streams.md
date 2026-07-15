---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 11
chapter_title: Stream Processing
type: topic
tags: [ddia, change-data-capture, event-sourcing, immutability]
sources:
  - raw/ch11.md
---
# Databases and Streams

Log-based brokers borrowed database ideas (durability, logs) for messaging; this topic runs the influence the other way and argues the connection is fundamental: a write to a database *is* an event. A [[Replication]] log is already a stream of write events that followers consume, and the state machine replication principle — same events, same order, same final state — is stream processing in disguise. That insight solves a real problem: applications combine an OLTP store, cache, search index, and warehouse, and keeping those copies in sync via dual writes leads to silent, permanent divergence. The fix is to make one system the leader and let every other system follow its ordered change stream — via [[Change Data Capture]] pulled from the storage layer, or [[Event Sourcing]] designed into the application. Both rest on the same philosophical move: treat the append-only log of immutable events as the system of record, and all mutable state as a cache derived from it.

## Subtopics
- [[Keeping Systems in Sync]] — why heterogeneous data systems drift apart, and how dual writes race and half-fail without any error being raised.
- [[Change Data Capture]] — extracting a database's change stream (triggers or log parsing), initial snapshots, [[Log Compaction]], and first-class change-stream APIs.
- [[Event Sourcing]] — modeling application changes as intent-level immutable events; commands vs events; deriving current state by replay.
- [[State, Streams, and Immutability]] — state as the integral of an event stream; ledger-style auditability, multiple read views (CQRS), concurrency benefits, and where immutability breaks down.

## Key Takeaways
- Every database write is an event; the replication log makes this literal, and [[Total Order Broadcast]] makes it a correctness principle.
- Dual writes fail two ways: concurrent writers interleave differently in different systems (a race no one detects without [[Version Vectors]]), and partial failure leaves systems inconsistent unless you pay for atomic commit.
- CDC and event sourcing both funnel writes through one ordered log — CDC at the storage level, transparently to the application; event sourcing at the domain level, deliberately.
- Log compaction lets a change stream double as a full database copy, so new [[Derived Data]] systems can bootstrap from offset 0 without fresh snapshots.
- Immutability enables replay, auditability, and multiple read-optimized views, but churn-heavy datasets and legally required deletion (excision) are genuine limits.

## Related
- chapter: [[Ch 11 - Stream Processing]] · part: [[Part III - Derived Data]]
- [[Transmitting Event Streams]] — the log-based transport these change streams ride on
- [[Implementation of Replication Logs]] — the replication machinery CDC piggybacks on
- [[Data Integration]] — Ch 12 generalizes this log-centric integration story
