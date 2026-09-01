---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 8
chapter_title: Transactions
topic: Serializability
type: subtopic
tags: [ddia2, 2pl, locking, deadlock, predicate-lock, index-range-lock]
sources:
  - raw/ch08.md
---
# Two-Phase Locking
> For around 30 years, the only widely used algorithm for serializability. Writers block readers, readers block writers, and one slow transaction can stop the database.

> **2PL is not 2PC.** 2PL provides **serializable isolation**; 2PC provides **atomic commit in a distributed database**. Best to think of them as entirely separate concepts and ignore the unfortunate similarity in names.

## The Idea
Locks are often used to prevent dirty writes: if two transactions concurrently write the same object, the lock makes the second wait. **2PL makes the lock requirements much stronger.** Several transactions may **concurrently read** the same object as long as nobody is writing — **but as soon as anyone wants to write, exclusive access is required**:
- **If A has read an object and B wants to write it, B must wait until A commits or aborts** — so B can't change the object unexpectedly behind A's back.
- **If A has written an object and B wants to read it, B must wait until A commits or aborts.** Reading an old version, as read committed allows, **is not acceptable under 2PL.**

**In 2PL, writers don't just block other writers; they also block readers, and vice versa.** Snapshot isolation's mantra — *readers never block writers, and writers never block readers* — **captures the key difference.** In exchange, **because 2PL provides serializability it protects against all the race conditions discussed earlier, including lost updates and write skew.**

## How It Works
2PL is **used by the serializable isolation level in MySQL/InnoDB and SQL Server, and by repeatable read in Db2.**

Blocking is implemented with a lock on each object that can be in **shared** or **exclusive** mode (a multi-reader single-writer lock):
- **To read, acquire the lock in shared mode.** Several transactions may hold it in shared mode simultaneously, **but if another holds it exclusively they must wait.**
- **To write, acquire the lock in exclusive mode.** No other transaction may hold it at all, so any existing lock forces a wait.
- **A transaction that first reads then writes may upgrade its shared lock to exclusive**, working the same way as acquiring exclusive directly.
- **After acquiring a lock, a transaction must hold it until the end** (commit or abort). **This is where "two-phase" comes from**: the **growing phase** while the transaction executes is when locks are acquired; the **shrinking phase** at the end is when they are released. **The two phases must not overlap — once a lock is released, no new locks may be acquired.**

**With so many locks, deadlock happens quite easily** — A stuck waiting for B while B waits for A. **The database automatically detects deadlocks and aborts one of them** so the others progress; **the aborted transaction must be retried by the application.**

**Predicate locks.** A serializable database **must prevent phantoms**. In the meeting room case, if one transaction has searched for existing bookings for a room in a time window, **another must not concurrently insert or update a booking for the same room and overlapping time** (concurrent bookings for other rooms, or non-overlapping times, are fine).

Conceptually this needs a **predicate lock**: like a shared/exclusive lock, **but belonging to all objects matching a search condition rather than to a particular object**. **The key idea is that a predicate lock applies even to objects that do not yet exist but might be added in the future — phantoms. If 2PL includes predicate locks, the database prevents all forms of write skew and other race conditions, and its isolation becomes serializable.**

**Index-range locks.** **Predicate locks do not perform well**: with many locks held by active transactions, **checking for matching locks becomes time-consuming.** So most 2PL databases implement **index-range locking** (also **next-key locking**), **a simplified approximation.**

**It is safe to simplify a predicate by making it match a greater set of objects.** A lock on bookings of room 123 between noon and 1 p.m. can be approximated by **locking bookings for room 123 at any time**, or by **locking all rooms between noon and 1 p.m.** — **safe because any write matching the original predicate also matches the approximation.**

In practice you would have an index on `room_id` and/or on `start_time`/`end_time`. If the database uses the `room_id` index, it **attaches a shared lock to that index entry**, recording that a transaction searched for bookings of room 123. If it uses a time-based index, it **attaches a shared lock to a range of values** in that index. **Either way an approximation of the search condition is attached to one of the indexes.** **If there is no suitable index to attach a range lock to, the database can fall back to a shared lock on the entire table** — bad for performance, since it stops all other transactions writing to the table, **but a safe fallback.**

## Trade-offs & Pitfalls
**The big downside — and the reason 2PL hasn't been the default since the 1970s — is performance.** Transaction throughput and query response times are **significantly worse under 2PL than under weak isolation**, partly from the overhead of acquiring and releasing locks, **but more importantly from reduced concurrency**: by design, **if two concurrent transactions do anything that might in any way result in a race condition, one must wait.**

**The worst case is a full-table read.** A backup, analytical query, or integrity check **must take a shared lock on the entire table**: it first waits for all in-progress writers to finish, and then **while the whole table is being read — potentially a long time — all transactions wanting to write are blocked. In effect the database becomes unavailable for writes for an extended time.**

**So databases running 2PL can have quite unstable latencies and can be very slow at high percentiles** if there is contention. **Just one slow transaction, or one that accesses a lot of data and acquires many locks, could cause the rest of the system to grind to a halt.** Transaction timeouts and slow query monitoring are used to detect and limit misbehaving queries.

**Deadlocks are also much more frequent under 2PL** than under lock-based read committed, depending on access patterns — an additional performance problem, since **an aborted-and-retried transaction has to do all its work over again. If deadlocks are frequent, this means significant wasted effort.**

## Examples & Systems
MySQL/InnoDB and SQL Server (serializable via 2PL); Db2 (repeatable read via 2PL); index-range/next-key locking as the practical approximation of predicate locks.

## Since the 1st Edition
Essentially unchanged from the 1st edition's [[Two-Phase Locking (2PL)]] — the same lock modes, the same growing/shrinking phase explanation, the same 2PL-is-not-2PC warning, the same performance critique, and the same predicate-lock and index-range-lock treatment. Another very stable section, which fits: 2PL is a 1970s algorithm and nothing about it has changed.

## Related
- up: [[Serializability (2e)]] · chapter: [[Ch 08 - Transactions (2e)]]
- [[Serializable Snapshot Isolation (2e)]] — the optimistic alternative that fixes the performance problem
- [[Write Skew and Phantoms (2e)]] — what predicate locks exist to prevent
- [[Two-Phase Commit (2e)]] — the differently named, unrelated protocol
- 1st edition: [[Two-Phase Locking (2PL)]] — the same subtopic
