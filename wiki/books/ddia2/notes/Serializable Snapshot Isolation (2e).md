---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 8
chapter_title: Transactions
topic: Serializability
type: subtopic
tags: [ddia2, ssi, optimistic-concurrency-control, mvcc, premise, foundationdb]
sources:
  - raw/ch08.md
---
# Serializable Snapshot Isolation
> Full serializability with only a small performance penalty over snapshot isolation. First described in 2008 — which is why the 1970s answer of "just use serializable" finally became practical.

## The Idea
The chapter has painted a bleak picture: **implementations of serializability that don't perform well (2PL) or don't scale well (serial execution)**, versus **weak isolation levels with good performance but prone to race conditions**. **Are serializable isolation and good performance fundamentally at odds?**

**It seems not.** **Serializable snapshot isolation (SSI) provides full serializability with only a small performance penalty compared to snapshot isolation.** It is comparatively new — **first described in 2008** — and today SSI and similar algorithms are used in **single-node databases** (PostgreSQL's serializable level, SQL Server's In-Memory OLTP/Hekaton, HyPer), **distributed databases** (CockroachDB, FoundationDB), and **embedded storage engines** such as BadgerDB.

## How It Works
**Pessimistic versus optimistic concurrency control.** **2PL is pessimistic**: if anything might possibly go wrong, it's better to wait until the situation is safe — like mutual exclusion in multithreaded programming. **Serial execution is pessimistic to the extreme**, essentially giving each transaction an exclusive lock on the whole database (or shard) for its duration, **compensated by making each transaction very fast so the "lock" is held briefly.**

**SSI is optimistic**: instead of blocking when something potentially dangerous happens, **transactions continue anyway, in the hope that everything will turn out all right.** At commit time **the database checks whether isolation was violated; if so the transaction aborts and must retry. Only transactions that executed serializably are allowed to commit.**

**Optimistic concurrency control is an old idea** whose merits have been debated a long time. **It performs badly under high contention** — many transactions accessing the same objects means a high proportion of aborts, and **if the system is already near maximum throughput, the load from retries makes performance worse.** **But with enough spare capacity and not-too-high contention, optimistic techniques tend to outperform pessimistic ones.** **Contention can be reduced with commutative atomic operations**: several transactions incrementing a counter don't care about order (as long as the counter isn't read in the same transaction), so **the increments can all apply without conflicting.**

**As the name suggests, SSI is based on snapshot isolation** — all reads come from a consistent snapshot — **plus an algorithm for detecting serialization conflicts among reads and writes and deciding which transactions to abort.**

**Decisions based on an outdated premise.** Write skew has a recurring pattern: **a transaction reads data, examines the result, and decides to write based on what it saw.** Under snapshot isolation **the original query result may no longer be up to date by commit time.** Put another way, **the transaction acts on a premise** — "there are currently two doctors on call" — **and by commit time the premise may no longer be true.**

**The database doesn't know how the application uses a query result**, so to be safe it must assume **any change in the query result means the transaction's writes may be invalid** — there may be a causal dependency between the queries and the writes. **To provide serializability, the database must detect when a transaction may have acted on an outdated premise and abort it.** Two cases:

**1. Detecting reads of a stale MVCC object version** (an uncommitted write occurred before the read). Transaction 43 sees Aaliyah as `on_call = true` because transaction 42, which modified it, is uncommitted. **By the time 43 wants to commit, 42 has committed — so the write that was ignored has now taken effect and 43's premise is no longer true.** So **the database tracks when a transaction ignores another's writes due to MVCC visibility rules, and at commit checks whether any ignored writes have now been committed. If so, abort.**

**Why wait until commit rather than aborting immediately?** Because **if transaction 43 turns out to be read-only it needn't abort at all** (no risk of write skew), and at read time the database doesn't yet know whether a write is coming. Moreover **transaction 42 may yet abort, or still be uncommitted when 43 commits, so the read may turn out not to have been stale.** **By avoiding unnecessary aborts, SSI preserves snapshot isolation's support for long-running reads.**

**2. Detecting writes that affect prior reads** (the write occurs after the read). This uses a technique similar to index-range locks — **except SSI locks don't block other transactions.** If transactions 42 and 43 both search for on-call doctors in shift 1234 and there is an index on `shift_id`, **the database uses index entry 1234 to record that both transactions read this data** (without an index, tracking happens at table level). **This information is kept only for a while**: after a transaction finishes and all concurrent transactions finish, the database can forget it.

**When a transaction writes, it looks in the indexes for other transactions that recently read the affected data.** This is like acquiring a write lock on the key range, **but rather than blocking until readers commit, the lock acts as a tripwire — it simply notifies those transactions that the data they read may no longer be up to date.** So 43 notifies 42 and vice versa; **42 commits first and succeeds** (43's conflicting write hasn't taken effect yet), **but when 43 wants to commit, 42's conflicting write has already committed, so 43 must abort.**

## Trade-offs & Pitfalls
**Granularity of tracking is the key engineering trade-off.** Keeping detailed track of each transaction's activity lets the database **be precise about which transactions must abort, but the bookkeeping overhead can become significant.** **Less detailed tracking is faster but aborts more transactions than strictly necessary.** In some cases **it's actually fine for a transaction to read information later overwritten** — depending on what else happened, the execution can sometimes be proven serializable anyway, **and PostgreSQL uses this theory to reduce unnecessary aborts.**

**Versus 2PL:** the big advantage is that **one transaction never blocks waiting for another's locks.** As with snapshot isolation, writers don't block readers and vice versa, which **makes query latency much more predictable and less variable** — and **read-only queries can run on a consistent snapshot with no locks at all**, very appealing for read-heavy workloads.

**Versus serial execution:** SSI **is not limited to a single CPU core.** **FoundationDB distributes serialization-conflict detection across multiple machines**, scaling to very high throughput; **even with data sharded across machines, transactions can read and write across shards while remaining serializable.**

**Versus nonserializable snapshot isolation:** the serializability check adds overhead, **and how significant it is remains debated** — **some believe serializability checking isn't worth it; others believe its performance is now so good that there's no need for weaker snapshot isolation any more.**

**Abort rate dominates SSI's overall performance.** **A transaction that reads and writes over a long period is likely to hit conflicts and abort, so SSI requires read/write transactions to be fairly short** (long-running **read-only** transactions are fine). **However, SSI is less sensitive to slow transactions than 2PL or serial execution.**

## Examples & Systems
PostgreSQL serializable, SQL Server Hekaton, HyPer (single-node); CockroachDB, FoundationDB (distributed); BadgerDB (embedded).

## Since the 1st Edition
The mechanism is unchanged from the 1st edition's [[Serializable Snapshot Isolation]] — the same optimistic/pessimistic framing, the same two detection cases with the same doctors example, and the same performance discussion. **Updated:** the systems roster now includes **CockroachDB, FoundationDB, and BadgerDB**, and the comparison to serial execution adds **FoundationDB's distributed conflict detection** as concrete evidence that SSI scales beyond one core — a claim the 1st edition could state only in principle.

## Related
- up: [[Serializability (2e)]] · chapter: [[Ch 08 - Transactions (2e)]]
- [[Snapshot Isolation and Repeatable Read (2e)]] — the foundation SSI builds on
- [[Two-Phase Locking (2e)]] — the pessimistic alternative
- [[Write Skew and Phantoms (2e)]] — the anomaly SSI detects
- 1st edition: [[Serializable Snapshot Isolation]] — the same subtopic
