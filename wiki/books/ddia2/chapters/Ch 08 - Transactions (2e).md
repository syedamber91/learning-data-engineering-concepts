---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 8
chapter_title: Transactions
type: chapter-moc
tags: [ddia2, transactions, acid, isolation, serializability, 2pc, moc]
sources:
  - raw/ch08.md
---
# Ch 08 – Transactions
In the harsh reality of data systems many things can go wrong: **the database software or hardware may fail at any time**, including mid-write; **the application may crash at any time**, including halfway through a series of operations; **network interruptions** can cut the application off from the database or one node from another; **several clients may write at the same time**, overwriting each other's changes; **a client may read data that doesn't make sense** because it has only partially been updated; and **race conditions between clients can cause surprising bugs.**

**For decades, transactions have been the mechanism of choice for simplifying these issues.** A transaction groups several reads and writes into a logical unit; conceptually all of them execute as one operation, so **either the entire transaction succeeds (commit) or it fails (abort/rollback)** — and if it fails, the application can safely retry. **Error handling becomes much simpler, because the application need not worry about partial failures.**

**Transactions are not a law of nature.** They were created with a purpose: to simplify the programming model for applications accessing a database, letting the application ignore certain error scenarios and concurrency issues because the database handles them instead — its **safety guarantees**. Not every application needs them, and **sometimes there are advantages to weakening or abandoning them** for better performance or availability. But they prevent a lot of grief: **the technical cause behind the Post Office Horizon scandal was probably a lack of ACID transactions in the underlying accounting system.**

## Map
- [[What Exactly Is a Transaction (2e)]] — 50 years of System R's design, and what NoSQL did to it
  - [[The Meaning of ACID (2e)]] — atomicity, consistency, isolation, durability, and how vague each has become
  - [[Single-Object and Multi-Object Operations (2e)]] — why one-row atomicity isn't enough, and how to handle aborts
- [[Weak Isolation Levels (2e)]] — the levels people actually run in production
  - [[Read Committed (2e)]] — no dirty reads, no dirty writes
  - [[Snapshot Isolation and Repeatable Read (2e)]] — MVCC, visibility rules, and a naming disaster
  - [[Preventing Lost Updates (2e)]] — atomic operations, explicit locks, detection, and compare-and-set
  - [[Write Skew and Phantoms (2e)]] — the anomaly only serializability prevents
- [[Serializability (2e)]] — the strongest level, and the three ways to get it
  - [[Actual Serial Execution (2e)]] — one thread, stored procedures, and sharding
  - [[Two-Phase Locking (2e)]] — the 30-year standard, its performance, predicate and index-range locks
  - [[Serializable Snapshot Isolation (2e)]] — optimistic concurrency control that actually performs
- [[Distributed Transactions (2e)]] — atomicity when more than one node is involved
  - [[Two-Phase Commit (2e)]] — the system of promises, and what happens when the coordinator dies
  - [[Distributed Transactions Across Different Systems (2e)]] — XA, in-doubt locks, and heuristic decisions
  - [[Database-Internal Distributed Transactions (2e)]] — the same 2PC without the lowest-common-denominator trap
  - [[Exactly-Once Message Processing Revisited (2e)]] — you can get it with idempotence instead

## Chapter Summary
**Transactions are an abstraction layer that lets an application pretend certain concurrency problems and hardware/software faults don't exist.** A large class of errors is reduced to a simple abort, and the application just tries again. Not every application is susceptible — one reading and writing only single records can probably manage without — **but for complex access patterns transactions hugely reduce the number of error cases you must think about.**

The chapter's central table of anomalies by isolation level:

| Isolation level | Dirty reads | Read skew | Phantom reads | Lost updates |
|---|---|---|---|---|
| Read uncommitted | Possible | Possible | Possible | Possible |
| Read committed | Prevented | Possible | Possible | Possible |
| Snapshot isolation | Prevented | Prevented | Prevented | **Depends** |
| Serializable | Prevented | Prevented | Prevented | Prevented |

**Dirty reads** — one client reads another's uncommitted writes; prevented by read committed and above. **Dirty writes** — one client overwrites another's uncommitted write; almost all implementations prevent these, which is why they aren't in the table. **Read skew** — a client sees different parts of the database at different points in time (also called nonrepeatable reads); prevented by snapshot isolation, usually implemented with MVCC. **Phantom reads** — a transaction reads objects matching a search condition and another client writes something affecting that result; snapshot isolation prevents straightforward phantoms, **but phantoms in the context of write skew need special treatment such as index-range locks**. **Lost updates** — two clients do a read-modify-write cycle and one clobbers the other; **some snapshot isolation implementations prevent this automatically, others require a manual lock**. **Write skew** — a transaction reads, decides based on what it saw, and writes the decision, but by the time the write happens the premise is no longer true; **only serializable isolation prevents this.**

Three ways to implement serializability: **literally executing transactions in a serial order** (simple and effective if each transaction is fast — typically via stored procedures — and throughput fits on one CPU core or can be sharded); **two-phase locking** (the standard for decades, avoided by many applications because of poor performance); and **serializable snapshot isolation** (comparatively new, optimistic, letting transactions proceed without blocking and aborting at commit time if execution wasn't serializable).

Finally, **atomicity across multiple nodes via 2PC**. If all nodes run the same database software, distributed transactions can work quite well. **Across different storage technologies, using XA, 2PC is problematic**: very sensitive to faults in the coordinator and in the application code driving the transaction, and it interacts poorly with concurrency control. **Fortunately, idempotence can ensure exactly-once semantics without atomic commit across storage technologies.**

## Since the 1st Edition
This is the 1st edition's Chapter 7, restructured and extended. **Retained essentially intact:** the ACID definitions, single/multi-object operations, read committed, snapshot isolation and MVCC, lost updates, write skew and phantoms, serial execution, 2PL with predicate and index-range locks, SSI, and 2PC with the marriage analogy.

**Restructured:** the 1st edition's Chapter 7 ended at serializability; **distributed transactions and 2PC were in Chapter 9** ("Consistency and Consensus"). The 2nd edition **moves the whole atomic-commit discussion into the transactions chapter**, which is where it belongs — leaving Chapter 10 free to be about consistency and consensus proper.

**New or substantially expanded:** the opening argument that **NewSQL disproved the "transactions don't scale" belief**, naming CockroachDB, TiDB, Spanner, FoundationDB, and YugabyteDB; the **replication-versus-durability sidebar** with its catalogue of ways disks and `fsync` fail; **conditional writes (compare-and-set)** as a first-class lost-update remedy; [[Database-Internal Distributed Transactions (2e)]] as its own subtopic explaining exactly which XA problems internal transactions escape; and [[Exactly-Once Message Processing Revisited (2e)]], which shows the **message-ID-table idempotence pattern that removes the need for heterogeneous distributed transactions entirely** — the chapter's most practically useful addition.

## Related
- home: [[Home (2e)]] · previous: [[Ch 07 - Sharding (2e)]] · next: [[Ch 09 - The Trouble with Distributed Systems (2e)]]
- [[Ch 10 - Consistency and Consensus (2e)]] — where the fault-tolerant coordinator comes from
- [[Ch 06 - Replication (2e)]] — conflict resolution as the non-transactional alternative
- 1st edition: [[Ch 07 - Transactions]] — the chapter this one revises
