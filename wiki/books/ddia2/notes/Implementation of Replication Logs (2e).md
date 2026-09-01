---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 6
chapter_title: Replication
topic: Single-Leader Replication
type: subtopic
tags: [ddia2, statement-based, wal-shipping, logical-log, binlog, cdc]
sources:
  - raw/ch06.md
---
# Implementation of Replication Logs
> Ship the statements, ship the disk bytes, or ship the row changes. The third one is why you can upgrade your database without downtime.

## The Idea
Several replication methods are used in practice, and the choice has consequences that reach far beyond the storage engine.

## How It Works
**Statement-based replication.** The leader logs every write request (statement) it executes and sends that statement log to followers. For a relational database, every `INSERT`, `UPDATE`, or `DELETE` is forwarded, and each follower parses and executes it as if received from a client. This breaks down in several ways:
- Any statement calling a **nondeterministic function** — `NOW()` for the current time, `RAND()` for a random number — is likely to generate a different value on each replica.
- Statements using an **autoincrementing column**, or depending on existing data (`UPDATE … WHERE <condition>`), **must be executed in exactly the same order on each replica** or they may have different effects — limiting when there are multiple concurrent transactions.
- Statements with **side effects** (triggers, stored procedures, user-defined functions) may produce different side effects on each replica unless those effects are absolutely deterministic.

Workarounds exist — the leader can replace nondeterministic function calls with a fixed return value when logging so all followers get the same value. **The idea of executing deterministic statements in a fixed order is the event sourcing model**, also known as **state machine replication**. Statement-based replication was used in MySQL before 5.1 and is still sometimes used because it is quite compact, but **MySQL now switches to row-based replication by default if there is any nondeterminism in a statement**. VoltDB uses it and makes it safe by **requiring transactions to be deterministic** — but determinism is hard to guarantee in practice, so many databases prefer other methods.

**Write-ahead log shipping.** A WAL is needed anyway to make B-tree storage engines robust, and since it contains all the information needed to restore indexes and heap to a consistent state, **the same log can build a replica on another node**: besides writing it to disk, the leader sends it across the network, and the follower builds a copy of exactly the same files. Used in **PostgreSQL and Oracle**.

The main disadvantage: **the log describes the data at a very low level** — which bytes changed in which disk blocks — making replication **tightly coupled to the storage engine**. If the database changes its storage format between versions, **it is typically not possible to run different versions on leader and followers.** That sounds like a minor implementation detail but has a big operational impact: **if the protocol allows a follower to run a newer version than the leader, you can do a zero-downtime database software upgrade** by upgrading followers first and then failing over to an upgraded node. **If it doesn't — as is often the case with WAL shipping — such upgrades require downtime.**

**Logical (row-based) log replication.** Use a **different log format for replication than for the storage engine**, decoupling the replication log from storage internals. Such a log is called **logical**, to distinguish it from the storage engine's physical representation. For a relational database it is a sequence of records describing writes at **row granularity**:
- For an **inserted** row, the new values of all columns.
- For a **deleted** row, enough information to uniquely identify it — typically the primary key, or the old values of all columns if there is no primary key.
- For an **updated** row, enough to identify it plus the new values of all columns (or at least all changed ones).

A transaction modifying several rows generates several such records followed by a **commit record**. When configured for row-based replication, **MySQL keeps a separate logical log — the binlog — in addition to the WAL**; **PostgreSQL implements logical replication by decoding the physical WAL into row insert/update/delete events**.

## Trade-offs & Pitfalls
- **Because a logical log is decoupled from storage internals, it can more easily be kept backward compatible**, allowing leader and follower to run different database versions — which enables **upgrading with minimal downtime**. That is the practical reason to prefer it.
- **A logical log format is also easier for external applications to parse**, which is useful for sending database contents to an external system such as a data warehouse or a specialised system for building custom indexes and caches. **This technique is called change data capture.**
- Statement-based replication's compactness is real but its determinism requirements are hard to meet; WAL shipping is simple but couples you to one software version across the cluster.

## Examples & Systems
MySQL (statement-based before 5.1, binlog for row-based today); PostgreSQL and Oracle (WAL shipping); PostgreSQL logical decoding; VoltDB (deterministic statement-based).

## Since the 1st Edition
Very close to the 1st edition's [[Implementation of Replication Logs]] — the same three formats with the same failure modes and the same zero-downtime-upgrade argument. **Added:** the explicit link from deterministic-statement execution to **event sourcing and state machine replication**, which the 1st edition did not connect here, and the note that MySQL auto-switches to row-based on detecting nondeterminism. The 1st edition also covered **trigger-based replication** as a fourth method; the 2nd edition drops it.

## Related
- up: [[Single-Leader Replication (2e)]] · chapter: [[Ch 06 - Replication (2e)]]
- [[Change Data Capture (2e)]] — the logical log put to external use
- [[Event Sourcing and CQRS (2e)]] — deterministic replay as a data model
- [[B-Trees (2e)]] — where the WAL comes from
- 1st edition: [[Implementation of Replication Logs]] — the same subtopic, plus triggers

## In the vutr data-engineering wiki
- [[northguard-segment-level-replication]] — LinkedIn's Northguard replicates at segment granularity rather than whole partitions — a granularity twist on this section's question of what unit of the log you actually ship and store.
