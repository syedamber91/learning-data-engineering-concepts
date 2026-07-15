---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 5
chapter_title: Replication
topic: Leaders and Followers
type: subtopic
tags: [ddia, replication-log, wal, change-data-capture]
sources:
  - raw/ch05.md
---
# Implementation of Replication Logs

> Leaders ship changes to followers as SQL statements, raw WAL bytes, logical row records, or trigger-captured events — each format trades compactness against decoupling.

## The Idea

Leader-based replication needs a concrete wire format for the change stream. Four approaches exist in practice, differing in how tightly they couple to the storage engine and how deterministic they are.

## How It Works

**1. Statement-based.** The leader forwards every executed write statement (INSERT/UPDATE/DELETE) and followers re-execute it. Breaks down when statements are nondeterministic — `NOW()` or `RAND()` yield different values per replica; autoincrement columns and condition-dependent updates require identical execution order; triggers and stored procedures may produce divergent side effects. Workarounds (leader substitutes fixed values) exist but edge cases abound. MySQL used this before 5.1 and now falls back to row-based when nondeterminism is detected; VoltDB keeps it safe by *requiring* deterministic transactions.

**2. [[Write-Ahead Log]] (WAL) shipping.** Storage engines already append every write to a log — the main data files for LSM engines ([[SSTables and LSM-Trees]]), a recovery log for [[B-Trees]]. The leader streams these exact bytes to followers, which rebuild identical on-disk structures. Used by PostgreSQL and Oracle. Downside: the log describes byte-level changes to disk blocks, welding replication to the storage engine version — leader and followers usually cannot run different releases, so zero-downtime rolling upgrades (upgrade followers, then fail over) are impossible.

**3. Logical (row-based) log.** A format decoupled from engine internals: inserted rows carry all new column values; deletes carry enough to identify the row (primary key, or all old values without one); updates carry the row identity plus changed columns; a commit record closes each transaction. MySQL's row-based binlog works this way. Being backward compatible, it permits mixed versions and even mixed storage engines, and it's easy for external consumers to parse — the basis of [[Change Data Capture]] feeding warehouses, caches, and indexes.

**4. Trigger-based.** Replication lifted into application code: a trigger logs each change into a side table that an external process reads and forwards. Offers flexibility — replicate a subset, cross database products, apply custom conflict logic — at the cost of higher overhead and more bugs than built-in replication. Oracle Databus and Postgres Bucardo work this way; Oracle GoldenGate reads the database log for similar ends.

## Trade-offs & Pitfalls

- Statement logs are compact but nondeterminism silently diverges replicas.
- WAL shipping is exact but version-locks the cluster and blocks rolling upgrades.
- Logical logs cost a little more space but buy upgrade freedom and external integration.
- Trigger-based is the most flexible and the most fragile.

## Examples & Systems

MySQL (statement → row-based binlog), VoltDB, PostgreSQL and Oracle (WAL shipping), Oracle GoldenGate, Databus, Bucardo.

## Related

- up: [[Leaders and Followers]] · chapter: [[Ch 05 - Replication]]
- [[Change Data Capture]] — logical logs consumed by external systems
- [[SSTables and LSM-Trees]] — log-structured engines whose log *is* the data
- [[B-Trees]] — why a WAL exists for page-overwriting engines
- [[Setting Up New Followers]] — new replicas replay this same log
- [[northguard-segment-level-replication]] — Northguard's choice to replicate at segment granularity rather than whole partitions is a granularity twist on the same replication-log implementation question: what unit of the log do you actually ship and store.
