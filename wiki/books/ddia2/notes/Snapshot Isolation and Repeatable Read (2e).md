---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 8
chapter_title: Transactions
topic: Weak Isolation Levels
type: subtopic
tags: [ddia2, snapshot-isolation, mvcc, repeatable-read, read-skew, visibility-rules]
sources:
  - raw/ch08.md
---
# Snapshot Isolation and Repeatable Read
> Every transaction reads from a consistent snapshot frozen at its start. Readers never block writers, writers never block readers — and nobody agrees what to call it.

## The Idea
Read committed looks like it does everything a transaction needs: it allows aborts, prevents reading incomplete results, and prevents concurrent writes intermingling. **But plenty of concurrency bugs remain.**

The book's example: Aaliyah has $1,000 split across two accounts of $500. A transaction transfers $100 between them. **If she looks at her balances at exactly the wrong moment**, she may see one account before the incoming payment arrived (still $500) and the other after the outgoing transfer (now $400) — **so it appears she has only $900, and $100 has vanished into thin air.**

This is **read skew**, an example of a **nonrepeatable read**: reading account 1 again at the end of the transaction would show a different value ($600). **Read skew is considered acceptable under read committed** — the balances she saw were indeed committed when she read them.

> **The term *skew* is unfortunately overloaded.** Earlier it meant an unbalanced workload with hot spots; **here it means a timing anomaly.**

For Aaliyah this is temporary — reload in a few seconds and it resolves. **But such temporary inconsistency is not tolerable for:**
- **Backups.** Copying an entire database may take hours while writes continue, so **parts of the backup contain older data and parts newer.** Restore from such a backup and **the inconsistencies, such as disappearing money, become permanent.**
- **Analytical queries and integrity checks.** Queries scanning large parts of the database — analytics, or a periodic integrity check monitoring for corruption — **are likely to return nonsensical results if they observe different parts of the database at different points in time.**

**Snapshot isolation is the most common solution.** Each transaction **reads from a consistent snapshot** — it sees all the data committed at the start of the transaction, and even if the data changes subsequently, it sees only the old data from that point in time. **It is a boon for long-running read-only queries**: it is very hard to reason about a query whose data is changing as it executes, and much easier when the data is frozen.

**Variants are supported by PostgreSQL, MySQL/InnoDB, Oracle, SQL Server, and others**, though detailed behaviour varies. **Some databases — Oracle, TiDB, Aurora DSQL — choose snapshot isolation as their highest isolation level.** Cloud warehouses such as **BigQuery** frequently use it too, since it provides a point-in-time view for analytical queries.

## How It Works
**Multiversion concurrency control (MVCC).** Implementations typically **use write locks to prevent dirty writes, but reads require no locks**. The key performance principle: **readers never block writers, and writers never block readers** — so a database can serve long-running read queries on a consistent snapshot while processing writes normally, with no lock contention between the two.

Instead of two versions of each row, the database must potentially keep **several committed versions**, since in-progress transactions may need different points in time — hence *multiversion*. In PostgreSQL's implementation, **a transaction gets a unique, always-increasing transaction ID (txid)**, and everything it writes is tagged with that ID. (*PostgreSQL txids are 32-bit and overflow after ~4 billion transactions; the vacuum process cleans up to ensure overflow doesn't affect data.*)

Each row has an **`inserted_by`** field with the ID of the inserting transaction, and a **`deleted_by`** field, initially empty. **Deleting a row doesn't remove it** — it sets `deleted_by`. **Later, when no transaction can any longer access the deleted or overwritten data, a garbage collection process removes marked rows and frees their space.** **An update is internally translated into a delete and an insert**: transaction 13 deducting $100 from account 2 leaves a $500 row marked deleted by 13 and a $400 row inserted by 13.

**All versions of a row are stored within the same database heap**, regardless of whether their transactions committed, and **the versions of a row form a linked list** (newest-to-oldest or the reverse) so queries can iterate over them.

**Visibility rules for a consistent snapshot.** Transaction IDs decide which versions are visible:
1. **At the start of each transaction, the database lists all other transactions in progress** at that moment. **Any writes they made are ignored, even if they subsequently commit** — ensuring the snapshot isn't affected by another transaction committing.
2. **Writes by transactions with a later transaction ID are ignored**, regardless of whether they committed.
3. **Writes by aborted transactions are ignored**, regardless of when the abort happened. This is convenient: **on abort we needn't immediately remove the rows, since the visibility rule filters them out** and GC can remove them later.
4. **All other writes are visible.**

Put another way, **a row is visible if (a) the transaction that inserted it had already committed when the reader's transaction started, and (b) the row is not marked for deletion, or if it is, the deleting transaction had not yet committed when the reader started.**

**A long-running transaction may keep using its snapshot for a long time**, reading values that others long since overwrote. **By never updating values in place but inserting a new version every change, the database provides a consistent snapshot with only a small overhead.**

**Indexes.** The most common approach is that **each index entry points at one version of a row** (oldest or newest), with each version referencing the next; **a query using the index iterates over the rows to find one that is visible and matches.** When GC removes invisible versions, the corresponding index entries can also go. **Implementation details matter a lot for performance** — PostgreSQL has optimisations to avoid index updates if different versions of a row fit on the same page, and **some databases store only differences between versions rather than full copies.**

**Another approach — immutable B-trees** — is used in **CouchDB, Datomic, and LMDB**: a **copy-on-write** variant that doesn't overwrite pages but **creates a new copy of each modified page**, with parent pages up to the root copied and updated to point at the new children; **unaffected pages are shared with the new tree.** **Every write transaction creates a new B-tree root, and a root is a consistent snapshot at its creation time** — **no need to filter by transaction ID**, since subsequent writes cannot modify an existing tree, only create new roots. This still requires background compaction and GC.

## Trade-offs & Pitfalls
**The naming is a genuine mess, and the book is blunt about it.** MVCC is often used to implement snapshot isolation, but **different databases use different terms for the same thing** — snapshot isolation is called **"repeatable read" in PostgreSQL and "serializable" in Oracle**. And **different systems use the same term with different meanings**: in PostgreSQL "repeatable read" means snapshot isolation, **in MySQL it means an implementation of MVCC with weaker consistency than snapshot isolation**, and **IBM Db2 uses "repeatable read" to mean serializability.**

**The reason is historical.** The SQL standard **has no concept of snapshot isolation**, because it is based on System R's 1975 definition of isolation levels and **snapshot isolation hadn't been invented yet**. It defines *repeatable read*, which looks superficially similar, so **PostgreSQL calls its snapshot isolation level "repeatable read" in order to claim standards compliance.**

**Worse, the standard's definition is flawed** — "ambiguous, imprecise, and not as implementation-independent as a standard should be." Even though several databases implement repeatable read, **there are big differences in the guarantees they provide despite being ostensibly standardized.** The level has been formally defined in the research literature, **but most implementations don't satisfy that definition. As a result, nobody really knows what repeatable read isolation means.**

## Examples & Systems
PostgreSQL, MySQL/InnoDB, Oracle, SQL Server, TiDB, Aurora DSQL, BigQuery (snapshot isolation variants); CouchDB, Datomic, LMDB (immutable copy-on-write B-trees).

## Since the 1st Edition
Very close to the 1st edition's [[Snapshot Isolation and Repeatable Read]] — the same disappearing-$100 example, the same backup and integrity-check motivations, the same MVCC mechanics and visibility rules, and the same "nobody really knows what repeatable read means" conclusion. **Updated:** the systems list adds **TiDB, Aurora DSQL, and BigQuery** as snapshot-isolation-as-highest-level or analytics uses; PostgreSQL's `created_by`/`deleted_by` fields are renamed to `inserted_by`/`deleted_by`; and the note on storing version deltas rather than full copies is new.

## Related
- up: [[Weak Isolation Levels (2e)]] · chapter: [[Ch 08 - Transactions (2e)]]
- [[Serializable Snapshot Isolation (2e)]] — snapshot isolation plus conflict detection
- [[B-Trees (2e)]] — the copy-on-write variant reused here
- [[Read Committed (2e)]] — the weaker level this generalises
- 1st edition: [[Snapshot Isolation and Repeatable Read]] — the same subtopic
