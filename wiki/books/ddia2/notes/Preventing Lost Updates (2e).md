---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 8
chapter_title: Transactions
topic: Weak Isolation Levels
type: subtopic
tags: [ddia2, lost-update, compare-and-set, optimistic-locking, select-for-update, crdt]
sources:
  - raw/ch08.md
---
# Preventing Lost Updates
> Read, modify, write. Do it twice concurrently and one modification disappears. Five remedies, and the right one depends on whether you have a single up-to-date copy of the data.

## The Idea
The read-committed and snapshot discussions focused on what a **read-only** transaction sees. **The best known conflict between concurrently *writing* transactions is the lost update problem.**

It occurs if an application **reads a value, modifies it, and writes back the modified value** — the read-modify-write cycle. **If two transactions do this concurrently, one of the modifications can be lost**, because the second write doesn't include the first modification. (**The later write *clobbers* the earlier one.**) The pattern appears in:
- **Incrementing a counter or updating an account balance.**
- **Making a local change to a complex value** — adding an element to a list within a JSON document requires parsing, changing, and writing back the whole document.
- **Two users editing a wiki page at the same time**, each saving by sending the entire page contents, overwriting whatever is currently there.

## How It Works
**1. Atomic write operations.** Many databases provide atomic updates that **remove the need for read-modify-write in application code**, and they are **usually the best solution if your code can be expressed in terms of them**:

```sql
UPDATE counters SET value = value + 1 WHERE key = 'foo';
```

**MongoDB** provides atomic operations for local modifications to part of a JSON document; **Redis** for modifying structures such as priority queues. **Not all writes can be expressed this way** — wiki page edits involve arbitrary text editing, handled instead by CRDT/OT algorithms — **but where they apply they are usually the best choice.** They are **usually implemented by exclusively locking the object when it is read** so no other transaction can read it until the update is applied, **or by forcing all atomic operations onto a single thread.**

**Watch out for ORMs:** they **make it easy to accidentally write unsafe read-modify-write cycles instead of using the database's atomic operations** — a source of subtle bugs difficult to find by testing.

**2. Explicit locking.** If built-in atomic operations don't suffice, **the application can explicitly lock the objects it will update**, then perform read-modify-write; any other transaction trying to update or lock the same object **is forced to wait**. The book's example is a multiplayer game where several players can move the same figure: **an atomic operation isn't sufficient because the application must also check the move against the rules of the game**, logic you can't sensibly express as a database query.

```sql
BEGIN TRANSACTION;
SELECT * FROM figures WHERE name = 'robot' AND game_id = 222 FOR UPDATE;
-- Check whether move is valid, then update the position
UPDATE figures SET position = 'c4' WHERE id = 1234;
COMMIT;
```

`FOR UPDATE` tells the database to lock all rows returned by the query. **This works, but you need to think carefully about your application logic — it's easy to forget a necessary lock somewhere and introduce a race condition.** And **locking multiple objects risks deadlock**, where transactions wait on each other; **many databases detect deadlocks automatically and abort one**, which the application handles by retrying.

**3. Automatically detecting lost updates.** Atomic operations and locks **force read-modify-write cycles to happen sequentially**. The alternative: **let them run in parallel and, if the transaction manager detects a lost update, abort and retry.** Databases can perform this check efficiently **in conjunction with snapshot isolation**: **PostgreSQL's repeatable read, Oracle's serializable, and SQL Server's snapshot isolation levels all detect lost updates and abort the offending transaction.** **MySQL/InnoDB's repeatable read does not.** Some authors argue **a database must prevent lost updates to qualify as providing snapshot isolation — so by that definition MySQL does not provide snapshot isolation.**

**The big advantage is that it requires no special database features in application code.** You may forget a lock or an atomic operation and introduce a bug; **lost update detection happens automatically and is thus less error-prone** — though **you still have to retry aborted transactions at the application level.**

**4. Conditional writes (compare-and-set).** In databases without transactions you often find a **conditional write** that allows an update **only if the value hasn't changed since you last read it** — the database equivalent of the CPU's atomic CAS instruction:

```sql
UPDATE wiki_pages SET content = 'new content'
  WHERE id = 1234 AND content = 'old content';
```

If the content changed, the update has no effect, **so you must check whether it took effect and retry if necessary.** Instead of comparing full content you can **use a version number column incremented on every update**, applying the update only if the version hasn't changed — **sometimes called optimistic locking**.

**A subtlety worth knowing:** if another transaction concurrently modified `content`, **the new content may not be visible under MVCC visibility rules**. **Many MVCC implementations have an exception to the visibility rules for exactly this scenario**, where values written by other transactions **are visible to the evaluation of the `WHERE` clause of `UPDATE` and `DELETE` queries**, even though they aren't otherwise visible in the snapshot.

## Trade-offs & Pitfalls
**5. Conflict resolution and replication.** In replicated databases, preventing lost updates takes on another dimension. **Locks and conditional writes assume there is a single up-to-date copy of the data** — but **multi-leader and leaderless databases usually allow concurrent writes and replicate asynchronously, so they cannot guarantee a single up-to-date copy.** **Techniques based on locks or conditional writes therefore do not apply.**

Instead, the common approach is to **allow concurrent writes to create several conflicting versions (siblings)** and use application code or special data structures to resolve and merge them afterward. **Merging can prevent lost updates if the updates are commutative** — applying them in different orders on different replicas still gives the same result. **Incrementing a counter and adding an element to a set are commutative; that is the idea behind CRDTs.** **However, some operations, such as conditional writes, cannot be made commutative.**

**And the default in many replicated databases makes things worse:** **LWW conflict resolution is prone to lost updates** by construction.

## Examples & Systems
`UPDATE ... SET value = value + 1`; MongoDB and Redis atomic operations; `SELECT ... FOR UPDATE`; PostgreSQL/Oracle/SQL Server automatic detection versus MySQL/InnoDB's lack of it; CRDTs for commutative merges.

## Since the 1st Edition
The 1st edition's [[Preventing Lost Updates]] covered atomic operations, explicit locking, automatic detection, compare-and-set, and the replication dimension — the same five. **Added:** the note that **atomic operations may be implemented by forcing them onto a single thread**; the explicit link from wiki-page editing to **CRDT/OT algorithms** in the replication chapter; and the **MVCC visibility exception for `WHERE` clauses in `UPDATE`/`DELETE`**, which the 1st edition raised as an open concern about whether CAS is safe under snapshot isolation without saying how implementations resolve it.

## Related
- up: [[Weak Isolation Levels (2e)]] · chapter: [[Ch 08 - Transactions (2e)]]
- [[Write Skew and Phantoms (2e)]] — the generalisation of this problem
- [[Dealing with Conflicting Writes (2e)]] — the replication-side answer
- [[Single-Object and Multi-Object Operations (2e)]] — where conditional writes are introduced
- 1st edition: [[Preventing Lost Updates]] — the same subtopic
