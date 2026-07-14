---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 7
chapter_title: Transactions
topic: Weak Isolation Levels
type: subtopic
tags: [ddia, isolation-levels, dirty-reads, locking]
sources:
  - raw/ch07.md
---
# Read Committed
> The baseline isolation level: you never see uncommitted data (no dirty reads) and never overwrite uncommitted data (no dirty writes).

## The Idea
Read committed is the most widely used of the weak [[Isolation Levels]]. It draws a clean line at commit time: a transaction's writes become visible to others only at the moment it commits, all at once, and a transaction can only clobber values that were already committed. (An even weaker level, read uncommitted, blocks dirty writes but permits dirty reads.)

## How It Works
**Anomaly: dirty read** — transaction B observes data that transaction A has written but not yet committed. Why it's bad: B may see one of A's multi-object updates but not the others (new email visible, counter not yet bumped), and B may act on data that is later rolled back — data that never officially existed.

**Anomaly: dirty write** — B overwrites a value A wrote but hasn't committed. Example: Alice and Bob race to buy the same used car. The purchase touches two tables (listing owner, invoice recipient). With dirty writes the updates interleave so Bob wins the listing while Alice receives the invoice. Read committed prevents this by making conflicting writers queue.

**Implementation.**
- Dirty writes: row-level exclusive locks. A writer takes the lock on each object it modifies and holds it until commit or abort; a second writer blocks until then.
- Dirty reads: *not* usually via read locks (one long writer would stall every reader — terrible for response times and operability). Instead the database keeps two values per locked object — the last committed value and the in-flight new value — and serves readers the old committed value until the writer commits. This is a two-version precursor of MVCC.

## Trade-offs & Pitfalls
- Read committed does **not** stop the lost-update race: two counter increments where the second write lands after the first *committed* is legal here, yet an increment is still lost ([[Preventing Lost Updates]]).
- It also permits read skew across a transaction's multiple queries ([[Snapshot Isolation and Repeatable Read]]) and all write-skew/phantom anomalies ([[Write Skew and Phantoms]]).
- Concurrency bugs under weak isolation are real-world costly: lost money, auditor investigations, corrupted customer data — even in databases marketed as ACID.

## Examples & Systems
Default isolation level in Oracle 11g, PostgreSQL, SQL Server 2012, and MemSQL. IBM DB2 and SQL Server (with read_committed_snapshot off) are the rare systems still using read locks for it.

## Related
- up: [[Weak Isolation Levels]] · chapter: [[Ch 07 - Transactions]]
- [[Single-Object and Multi-Object Operations]] — the email/counter dirty-read scenario
- [[Snapshot Isolation and Repeatable Read]] — the next-stronger level, generalizing the two-version trick
- [[Two-Phase Locking (2PL)]] — how locks extend when you want full serializability
