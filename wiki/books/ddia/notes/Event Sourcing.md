---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 11
chapter_title: Stream Processing
topic: Databases and Streams
type: subtopic
tags: [ddia, event-sourcing, ddd, immutability]
sources:
  - raw/ch11.md
---
# Event Sourcing
> Store what the user *did* as immutable, intent-level events, and derive all mutable state from that log.

## The Idea
Event sourcing, from the domain-driven design community, applies the changelog idea at the application layer rather than the database layer. Where [[Change Data Capture]] extracts low-level row changes from a mutable database (the app unaware), event sourcing makes the application itself write only immutable events to an append-only store — updates and deletes are discouraged. Recording "student cancelled enrollment" preserves intent; recording "row deleted from enrollments, row added to feedback" bakes in assumptions about downstream use. New features (offer the seat to the waitlist) chain naturally off intent events. This aids evolution, debugging, and defense against buggy destructive writes.

## How It Works
- **Deriving state**: users want current state, not history, so the app deterministically folds the event log into read-optimized views — rerunnable at any time to reproduce the same state.
- **Compaction differs from CDC**: a CDC event holds the full new record, so [[Log Compaction]] can discard older versions per key. Intent events don't supersede each other — later events depend on earlier ones — so the *full* history must be kept; compaction doesn't apply. Snapshots of derived state are only a performance shortcut, not a substitute for the log.
- **Commands vs events**: a user request starts as a *command* that may fail validation (seat already taken — compare [[Fault-Tolerant Consensus]] on uniqueness). Once validated it becomes an immutable *event*, a fact consumers cannot reject. Validation must therefore happen synchronously before publishing — e.g. a serializable transaction that validates and appends atomically — or the request is split into a tentative event plus a later confirmation (a pattern from [[Total Order Broadcast]]).

## Trade-offs & Pitfalls
Downstream views are asynchronous, so read-your-write anomalies appear (see [[Reading Your Own Writes]]). The full-history requirement grows storage on high-churn data. Events must be designed carefully — they are permanent facts; corrections are new compensating events, never edits.

## Examples & Systems
Event Store is a dedicated database for this style, but a conventional database or a [[Log-Based Message Broker]] such as [[Apache Kafka]] works too. The event log parallels the chronicle data model and a star schema's fact table (see [[Stars and Snowflakes - Schemas for Analytics]]).

## Related
- up: [[Databases and Streams]] · chapter: [[Ch 11 - Stream Processing]]
- [[Change Data Capture]] — the database-level sibling of this idea
- [[State, Streams, and Immutability]] — the philosophy underlying both
- [[Uses of Stream Processing]] — event-sourced state as a materialized view
- [[log-based-cdc]] — vutr's concept on reading the database's write-ahead log directly; event sourcing is this note's application-layer sibling, writing immutable intent events straight to the log instead of extracting row changes from one.
