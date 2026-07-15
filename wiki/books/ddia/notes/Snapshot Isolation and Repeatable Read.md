---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 7
chapter_title: Transactions
topic: Weak Isolation Levels
type: subtopic
tags: [ddia, snapshot-isolation, mvcc, read-skew]
sources:
  - raw/ch07.md
---
# Snapshot Isolation and Repeatable Read
> Every transaction reads from a frozen, consistent snapshot of the database taken at its start — implemented by keeping multiple versions of each object (MVCC).

## The Idea
**Anomaly: read skew (nonrepeatable read).** Alice holds $1,000 across two accounts. A transfer of $100 runs while she checks her balances: she reads account 1 before the transfer ($500) and account 2 after it ($400) — $100 appears to have vanished. Each value she read *was* committed, so read committed allows this. Rereading later gives a different answer, hence "nonrepeatable." Transient for a web page, but fatal for **backups** (hours-long copies mixing old and new data, making the inconsistency permanent on restore) and for **long analytic scans or integrity checks** ([[Transaction Processing or Analytics]]), which return nonsense if the data shifts under them. Snapshot isolation fixes this by letting each transaction see exactly the data that was committed when it began.

## How It Works
Writers still take locks against dirty writes, but **readers never block writers and writers never block readers** — the defining performance mantra. The mechanism is *multi-version concurrency control (MVCC)*: the database retains several committed versions of each object because different in-flight transactions need to see different points in time.

PostgreSQL-style implementation: every transaction gets an increasing txid. Rows carry `created_by` and `deleted_by` txid fields; a delete only marks the row, and an update becomes delete-old + create-new. Garbage collection reclaims versions no transaction can still see. Visibility rules at read time: ignore writes from (1) transactions still in progress when yours started, (2) aborted transactions, (3) transactions with a later txid — everything else is visible. Equivalently: the creator committed before your snapshot, and any deleter had not.

Indexes either point at all versions and rely on visibility filtering (PostgreSQL, with same-page optimizations), or the engine uses append-only/copy-on-write [[B-Trees]] where each write batch produces a new root that *is* an immutable snapshot (CouchDB, Datomic, LMDB) — at the cost of background [[Compaction]].

## Trade-offs & Pitfalls
- Naming chaos: Oracle calls this level "serializable"; PostgreSQL and MySQL call it "repeatable read," because the SQL standard (written in 1975 terms, before snapshot isolation existed) has no name for it. The standard's level definitions are ambiguous, implementations differ widely, and DB2 uses "repeatable read" to mean serializability — the term has lost any precise meaning.
- Snapshot isolation still permits lost updates (in some implementations), write skew, and phantoms ([[Write Skew and Phantoms]]).
- Long-lived snapshots keep old versions alive, growing storage until GC can reclaim them.

## Examples & Systems
PostgreSQL, MySQL/InnoDB, Oracle, SQL Server; CouchDB, Datomic, LMDB (append-only B-tree variant).

## Related
- up: [[Weak Isolation Levels]] · chapter: [[Ch 07 - Transactions]]
- [[Read Committed]] — the weaker level this generalizes (per-query vs per-transaction snapshots)
- [[Serializable Snapshot Isolation (SSI)]] — bolting serializability checks onto MVCC
- [[Skewed Workloads and Relieving Hot Spots]] — the other, unrelated meaning of "skew"
