---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 12
chapter_title: Stream Processing
type: topic
tags: [ddia2, cdc, event-sourcing, replication-log, state-machine-replication]
sources:
  - raw/ch12.md
---
# Databases and Streams
**Log-based message brokers succeeded by taking ideas from databases and applying them to messaging. We can also do the opposite: take ideas from messaging and streams and apply them to databases.**

**One approach is to use an event stream as the system of record** — **event sourcing.** **Instead of storing data in a model mutated by updating and deleting, model every state change as an immutable event written to an append-only log, with read-optimized materialized views derived from those events.** **Log-based brokers configured never to delete old events are well suited for this**, since they use append-only storage and can notify consumers with low latency.

**But you don't have to go as far as event sourcing.** **Even with mutable data models, event streams are useful for databases** — **in fact, every write to a database is an event that can be captured, stored, and processed.** **The connection between databases and streams runs deeper than the physical storage of logs on disk; it is quite fundamental.**

**A replication log is a stream of database write events produced by the leader as it processes transactions.** **Followers apply that stream to their own copy and end up with an accurate copy of the same data** — **the events describe the data changes that occurred.** And **state machine replication** says: **if every event represents a write, and every replica processes the same events in the same order, the replicas all end up in the same final state.**

## Subtopics
- [[Keeping Systems in Sync (2e)]] — the dual-writes problem, and why it can't be fixed by care.
- [[Change Data Capture (2e)]] — extracting the change log and treating derived systems as followers.
- [[State, Streams, and Immutability (2e)]] — why an append-only log and mutable state are two sides of one coin.

## Key Takeaways
- **The organising insight is that a database's replication log was always a stream** — it was simply treated as an internal implementation detail rather than something you could subscribe to.
- Once you can subscribe to it, **the multi-system consistency problem becomes a single-leader replication problem**, which the book already knows how to solve.
- **Immutability is the connective tissue** between this chapter and batch processing: the same property that lets you rerun a batch job lets you rebuild a derived view from scratch.

## Since the 1st Edition
The 1st edition's [[Databases and Streams]] topic had the same framing and the same three subtopics, plus a fourth on the "Advantages of immutable events" which the 2nd edition folds into [[State, Streams, and Immutability (2e)]]. Substantively stable; the changes are in the subtopics.

## Related
- chapter: [[Ch 12 - Stream Processing (2e)]]
- [[Implementation of Replication Logs (2e)]] — the log being captured
- [[Event Sourcing and CQRS (2e)]] — the data-model version of this idea
- 1st edition: [[Databases and Streams]] — the same topic
