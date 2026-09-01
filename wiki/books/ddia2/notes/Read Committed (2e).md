---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 8
chapter_title: Transactions
topic: Weak Isolation Levels
type: subtopic
tags: [ddia2, read-committed, dirty-read, dirty-write, row-locks, read-uncommitted]
sources:
  - raw/ch08.md
---
# Read Committed
> Two guarantees, and they're the default in Oracle, PostgreSQL, and SQL Server: you only read committed data, and you only overwrite committed data.

## The Idea
**The most basic level of transaction isolation** makes two guarantees:
- **When reading, you will see only data that has been committed** — no **dirty reads**.
- **When writing, you will overwrite only data that has been committed** — no **dirty writes**.

## How It Works
**No dirty reads.** If a transaction has written data but not yet committed or aborted, **can another transaction see that uncommitted data? If so, that's a dirty read.** Read committed must prevent this: **a transaction's writes become visible to others only when it commits, and then all at once.** So if user 1 sets `x = 3` but hasn't committed, user 2's `get x` still returns the old value 2.

Preventing dirty reads matters for two reasons. **If a transaction updates several rows, a dirty read means another transaction may see some updates but not others** — the email example, where the user sees the new unread email but not the updated counter. **Seeing the database in a partially updated state is confusing to users and may cause other transactions to make incorrect decisions.** And **if a transaction aborts, its writes must be rolled back** — if dirty reads were allowed, a transaction may have read data that is later rolled back, so **any transaction that read uncommitted data would also need to abort, leading to cascading aborts.**

**No dirty writes.** If two transactions concurrently update the same row, we normally assume the later write overwrites the earlier. **But what if the earlier write is part of an uncommitted transaction, so the later write overwrites an uncommitted value? That's a dirty write.** Read committed prevents it, **usually by delaying the second write until the first transaction commits or aborts.**

The book's worked example: on a used-car site, Aaliyah and Bryce simultaneously try to buy the same car. Buying requires two writes — updating the listing to reflect the buyer, and creating the sales invoice. With dirty writes, **the sale is awarded to Bryce (winning update to `listings`) but the invoice is sent to Aaliyah (winning update to `invoices`).** Read-committed isolation prevents such mishaps.

**But read committed does not prevent the counter-increment race.** There the second write happens *after* the first transaction committed, so it isn't a dirty write. **It's still incorrect, but for a different reason** — that is the lost update problem.

**Implementing read committed.** It is **very popular — the default in Oracle Database, PostgreSQL, SQL Server, and many others.**

**Dirty writes are prevented with row-level locks**: a transaction wanting to modify a row must first acquire the lock and hold it until commit or abort; only one transaction can hold it, so another writer must wait. Databases do this automatically in read-committed mode and stronger.

**Dirty reads could be prevented with the same lock** — requiring readers to briefly acquire and release it — **but this does not work well in practice**, because **one long-running write transaction can force many read-only transactions to wait.** That harms read-only response time and **is bad for operability: a slowdown in one part of an application has a knock-on effect in a completely different part.** Nevertheless some databases do this — **IBM Db2, and SQL Server with `read_committed_snapshot=off`.**

**The more common approach** is for the database to remember, for every written row, **both the old committed value and the new value set by the transaction holding the write lock.** While the transaction is ongoing, **other transactions reading the row are simply given the old value**; only on commit do they switch to the new one.

## Trade-offs & Pitfalls
- **Some databases support an even weaker level, read uncommitted**, which **prevents dirty writes but not dirty reads** — immediately returning the latest written value even if uncommitted. **This performs better, since the database need not store two versions of the row**, and it **reduces the probability of (but does not prevent) lost updates.**
- The knock-on-effect argument against read locks is the important operability insight here: **a concurrency-control choice can turn a slow writer into an application-wide outage.**

## Examples & Systems
Oracle, PostgreSQL, SQL Server (read committed by default); IBM Db2 and SQL Server with `read_committed_snapshot=off` (read locks); the used-car purchase as the dirty-write example.

## Since the 1st Edition
Essentially unchanged from the 1st edition's [[Read Committed]] — the same two guarantees, the same used-car dirty-write example, the same argument against read locks, and the same old-value/new-value implementation. One of the most stable sections in the book.

## Related
- up: [[Weak Isolation Levels (2e)]] · chapter: [[Ch 08 - Transactions (2e)]]
- [[Snapshot Isolation and Repeatable Read (2e)]] — the generalisation of the two-version trick
- [[Preventing Lost Updates (2e)]] — the race read committed does *not* stop
- 1st edition: [[Read Committed]] — the same subtopic
