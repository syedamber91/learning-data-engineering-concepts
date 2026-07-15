---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 7
chapter_title: Transactions
topic: Serializability
type: subtopic
tags: [ddia, serial-execution, stored-procedures, in-memory]
sources:
  - raw/ch07.md
---
# Actual Serial Execution
> Eliminate concurrency instead of controlling it: run every transaction one at a time on a single thread — serializable by definition.

## The Idea
The bluntest route to serializability is to remove concurrency entirely. Dismissed for 30 years as hopeless for performance, it became viable around 2007 because of two shifts: RAM got cheap enough to hold the entire active dataset in memory (no disk waits), and designers noticed OLTP transactions are short with few reads/writes, while long analytic queries are read-only and can run on a snapshot outside the serial loop (see [[Transaction Processing or Analytics]]).

## How It Works
**Stored procedures, not interactive transactions.** Early designers imagined a whole user flow (an airline booking) as one transaction, but humans dawdle, so that would mean vast numbers of idle open transactions. Modern apps keep transactions inside one HTTP request — yet even then the usual client/server style sends statements one at a time over the network, and a serial executor would spend most of its time waiting for the app's next statement. So serial systems require the *entire* transaction to be submitted up front as a stored procedure that executes in-process against in-memory data, with no network or disk stalls.

Stored procedures' bad reputation (vendor-specific archaic languages like PL/SQL and T-SQL; hard to debug, version, test, monitor; a bad procedure hurts a shared database far more than bad app-server code) is addressed by using general-purpose languages: VoltDB runs Java/Groovy, Datomic Java/Clojure, Redis Lua. VoltDB even replicates by re-executing the same procedure on each replica — which forces procedures to be deterministic (e.g., current time only via special APIs).

**Scaling via [[Partitioning]].** One thread caps throughput at one CPU core. If each transaction touches only a single partition, every partition gets its own serial thread and throughput scales linearly with cores (supported in VoltDB). Cross-partition transactions must run in lock-step across all involved partitions: VoltDB measures ~1,000 cross-partition writes/second — orders of magnitude below single-partition rates, and not improvable by adding machines. Simple key-value data partitions easily; multiple [[Secondary Indexes]] force heavy cross-partition coordination.

## Trade-offs & Pitfalls
Constraints for viability: every transaction must be small and fast (one slow transaction stalls everything); the active dataset must fit in RAM (anti-caching — abort, fetch asynchronously, restart — can stretch this); write throughput must fit one core or partition cleanly; cross-partition use has a hard ceiling. No lock overhead is the upside.

## Examples & Systems
VoltDB/H-Store, Redis, Datomic; airline-booking flow as the cautionary interactive example.

## Related
- up: [[Serializability]] · chapter: [[Ch 07 - Transactions]]
- [[Two-Phase Locking (2PL)]] — the pessimistic locking alternative
- [[Serializable Snapshot Isolation (SSI)]] — the optimistic alternative that scales past one core
- [[Partitioning and Secondary Indexes]] — why secondary indexes resist partitioning
