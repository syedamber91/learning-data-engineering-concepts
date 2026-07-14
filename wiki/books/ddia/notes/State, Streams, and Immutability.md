---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 11
chapter_title: Stream Processing
topic: Databases and Streams
type: subtopic
tags: [ddia, immutability, cqrs, changelog]
sources:
  - raw/ch11.md
---
# State, Streams, and Immutability
> Mutable state and an append-only event log are two views of the same thing: state is the integral of events, the change stream is its derivative.

## The Idea
Databases store current state because that's what reads want; but every state is just the accumulated result of the events that produced it — a seat map is the sum of reservations, a balance the sum of credits and debits. The changelog records the evolution of state over time. If the log is the system of record, the database becomes a cache of the latest values — Pat Helland's framing. [[Log Compaction]] bridges the two by retaining only each key's newest version.

## How It Works
- **Immutability's payoffs**: accountants have used append-only ledgers for centuries — errors get compensating entries, never erasures, preserving auditability. Buggy code that appends bad events is far easier to diagnose and recover from than code that overwrites destructively. Events also capture information state loses: an add-then-remove cart sequence is invisible in current state but gold for analytics.
- **Many views, one log**: separating the write path (immutable log) from read paths lets you derive multiple read-optimized representations from the same events, just like multiple stream consumers. New features get new views built by replaying the log, run alongside the old system, then swapped — easier than schema migration. This split is called **command query responsibility segregation (CQRS)**. [[Denormalization]] in read views becomes safe because the log-to-view translation keeps them consistent (compare Twitter's fan-out timelines in [[Describing Load]]); classic normalization debates (see [[Many-to-One and Many-to-Many Relationships]]) fade.
- **Concurrency**: async view updates cause read-your-write anomalies ([[Reading Your Own Writes]]); fixes include transactionally updating view with log append, or [[Total Order Broadcast]] techniques. But event sourcing also *simplifies* concurrency: a self-contained event needs one atomic append instead of a multi-object transaction, and a single-threaded partition consumer needs no write locks at all (compare [[Actual Serial Execution]]).

## Trade-offs & Pitfalls
High-churn datasets make immutable history prohibitively large; compaction and GC performance become critical. Privacy law may demand *true* deletion (Datomic "excision", Fossil "shunning") — appending a deletion marker isn't enough, and genuinely erasing data is hard because copies linger in storage engines, filesystems, SSDs, and backups.

## Examples & Systems
Druid ingesting from [[Apache Kafka]], Pistachio using Kafka as a commit log, Kafka Connect sinks exporting to databases and indexes; Git/Mercurial/Fossil as immutable-history systems; MVCC snapshots in databases (see [[Snapshot Isolation and Repeatable Read]]).

## Related
- up: [[Databases and Streams]] · chapter: [[Ch 11 - Stream Processing]]
- [[Event Sourcing]] — application-level immutable event logs
- [[Change Data Capture]] — extracting the changelog from databases
- [[Materialized Views]] — read views derived from the log
