---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 7
chapter_title: Transactions
topic: Weak Isolation Levels
type: subtopic
tags: [ddia, lost-updates, concurrency, compare-and-set]
sources:
  - raw/ch07.md
---
# Preventing Lost Updates
> When two transactions each read-modify-write the same object concurrently, one write can silently clobber the other — five distinct defenses exist.

## The Idea
**Anomaly: lost update.** A read-modify-write cycle (read value → compute → write back) run by two clients at once loses one modification: the second write is based on the pre-update value and doesn't include the first change. Classic instances: two counter increments yielding +1 instead of +2; editing a field inside a JSON document; two wiki editors saving full-page contents over each other; account-balance updates. Note this is *not* a dirty write — both writes touch committed data — so [[Read Committed]] doesn't stop it.

## How It Works
1. **Atomic write operations.** Push the modify step into the database: `UPDATE counters SET value = value + 1 …` is safe in most relational systems. MongoDB offers atomic partial-document updates; Redis has atomic data-structure ops. Usually implemented by an exclusive lock held over the read-and-update ("cursor stability"), or by funneling all atomic ops through one thread. Best choice whenever the change is expressible this way — arbitrary edits (wiki text) are not.
2. **Explicit locking.** `SELECT … FOR UPDATE` locks the rows read, forcing other read-modify-write cycles to queue. Needed when application logic must run between read and write (e.g., validating a game move before repositioning a figure). Fragile: forget one lock and you've reintroduced the race.
3. **Automatic detection.** Let cycles run in parallel under snapshot isolation and abort a transaction if the transaction manager spots a lost update. PostgreSQL repeatable read, Oracle serializable, and SQL Server snapshot level all do this; MySQL/InnoDB repeatable read does **not** — leading some to argue it doesn't truly provide snapshot isolation. Least error-prone: no special app code required.
4. **Compare-and-set.** In transaction-less stores: update only if the value still equals what you last read (`… WHERE id = 1234 AND content = 'old content'`), retrying otherwise. Unsafe if the WHERE clause reads from an old snapshot — verify your database's semantics first.
5. **Conflict resolution in replicated systems.** Locks and compare-and-set presuppose a single up-to-date copy. Multi-leader and leaderless [[Replication]] don't have one, so those techniques fail there. Instead, keep conflicting versions (siblings) and merge them later ([[Detecting Concurrent Writes]]), or use commutative atomic operations — increments and set-adds apply in any order, the idea behind Riak 2.0 datatypes.

## Trade-offs & Pitfalls
- ORMs make it easy to write unsafe read-modify-write code by accident instead of using atomic ops.
- Last-write-wins conflict resolution, the default in many replicated stores, is inherently lossy.

## Examples & Systems
MongoDB, Redis, PostgreSQL, Oracle, SQL Server, MySQL/InnoDB, Riak 2.0; counter, wiki-page, and multiplayer-game scenarios.

## Related
- up: [[Weak Isolation Levels]] · chapter: [[Ch 07 - Transactions]]
- [[Write Skew and Phantoms]] — the generalization when transactions update *different* objects
- [[Multi-Leader Replication]] — why single-copy assumptions break
- [[Linearizability]] — the formal "single up-to-date copy" guarantee
