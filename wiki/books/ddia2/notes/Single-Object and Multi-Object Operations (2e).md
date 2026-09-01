---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 8
chapter_title: Transactions
topic: What Exactly Is a Transaction
type: subtopic
tags: [ddia2, multi-object, single-object, abort, retry, compare-and-set]
sources:
  - raw/ch08.md
---
# Single-Object and Multi-Object Operations
> Storage engines give you atomicity and isolation for one object almost universally. The interesting question is what happens when your invariant spans several.

## The Idea
In ACID, **atomicity** means that if an error occurs partway through a sequence of writes, the transaction is aborted and the writes so far discarded — **an all-or-nothing guarantee** that saves you from worrying about partial failure. **Isolation** means concurrently running transactions don't interfere: if one makes several writes, another should see **either all or none of them, but not a subset**.

Both definitions assume you want to modify **several objects** at once, and such **multi-object transactions** are often needed when pieces of data must be kept in sync. The book's example is an email application: displaying the unread count with `SELECT COUNT(*) FROM emails WHERE recipient_id = 2 AND unread_flag = true` may be too slow, so you denormalize it into a separate counter field — **and now every new message must increment it and every read must decrement it.** Without isolation, a user can see the mailbox listing showing an unread message while the counter shows zero, because the increment hasn't happened yet. (**If an incorrect unread counter seems insignificant, think of a customer account balance instead of an unread counter and a payment instead of an email.**) Without atomicity, an error partway leaves the mailbox and counter permanently out of sync.

**Multi-object transactions need a way to determine which reads and writes belong together.** In relational databases that is typically **based on the client's TCP connection**: everything between `BEGIN TRANSACTION` and `COMMIT` on a connection is one transaction, and **if the TCP connection is interrupted, the transaction must be aborted.** **Many nonrelational databases have no such grouping** — even a multi-put API **doesn't necessarily mean transaction semantics**: the command may succeed for some keys and fail for others, leaving a partially updated state.

## How It Works
**Single-object writes.** Atomicity and isolation also apply when changing a single object. Writing a 20 kB JSON document: **if the connection is interrupted after 10 kB, does the database store an unparseable fragment? If power fails mid-overwrite, do you get old and new values spliced together? If another client reads during the write, does it see a partial value?** Each outcome would be incredibly confusing, so **storage engines almost universally provide atomicity and isolation at the level of a single object on one node** — atomicity via a crash-recovery log, isolation via a lock on each object.

Some databases provide **more complex atomic operations**: an **increment**, removing the need for a read-modify-write cycle, and a **conditional write**, allowing a write only if the value hasn't been concurrently changed — **the database equivalent of compare-and-set (CAS)**. (*Strictly, "atomic increment" uses* atomic *in the multithreaded sense; in ACID terms it should be called an isolated or serializable increment, but that isn't the usual term.*)

**These single-object operations are useful and can prevent lost updates, but they are not transactions in the usual sense.** Aerospike's "strong consistency" mode and the "lightweight transactions" feature of Cassandra and ScyllaDB offer **linearizable reads and conditional writes on a single object, but no guarantees across multiple objects.**

**The need for multi-object transactions.** Could you implement any application with only a key-value model and single-object operations? Sometimes — but often writes to several objects must be coordinated:
- **Foreign keys and graph edges.** A row in one table references a row in another; a vertex has edges to other vertices. **Multi-object transactions ensure these references remain valid** when inserting several records that refer to one another.
- **Denormalized documents.** In a document model the fields updated together are usually within one document, so no multi-object transaction is needed — **but document databases lacking joins encourage denormalization**, and updating denormalized information means updating several documents at once.
- **Secondary indexes.** In anything but a pure key-value store, indexes must be updated on every value change. **These are different database objects from a transaction point of view** — without isolation, **a record can appear in one index but not another** because the second index update hasn't happened yet.

Such applications can still be implemented without transactions, **but error handling becomes much more complicated without atomicity, and the lack of isolation causes concurrency problems.**

## Trade-offs & Pitfalls
**Handling errors and aborts.** A key feature of a transaction is that it can be **aborted and safely retried**. ACID databases embrace this: if in danger of violating atomicity, isolation, or durability, they would **rather abandon the transaction entirely than leave it half-finished**. **Not all systems follow that philosophy** — leaderless datastores work on a **best-effort** basis: "the database will do as much as it can, and if it runs into an error it won't undo something it has already done," leaving recovery to the application.

**Many developers prefer to think only about the happy path.** Popular ORM frameworks such as **Rails ActiveRecord and Django don't retry aborted transactions** — the error becomes an exception bubbling up the stack, user input is thrown away, and the user gets an error message. **This is a shame, because the whole point of rolling back is to enable safe retries.**

But **retrying isn't perfect either**:
- **If the transaction actually succeeded** but the network was interrupted while acknowledging the commit, **retrying performs it twice** unless you have application-level deduplication.
- **If the error is due to overload or high contention, retrying makes it worse.** Limit the number of retries, use exponential backoff, and handle overload-related errors differently from other errors.
- **Retry only after transient errors** — deadlock, isolation violation, temporary network interruption, failover. **After a permanent error such as a constraint violation, a retry is pointless.**
- **Side effects outside the database may happen even if the transaction aborts.** You don't want to send an email again on every retry. **If you need several systems to commit or abort together, two-phase commit can help.**
- **If the client process crashes while retrying, any data it was writing is lost.**

## Examples & Systems
The email unread-counter example; Aerospike strong consistency and Cassandra/ScyllaDB lightweight transactions as single-object-only guarantees; Rails ActiveRecord and Django as ORMs that don't retry.

## Since the 1st Edition
Close to the 1st edition's [[Single-Object and Multi-Object Operations]], including the email counter example, the three single-object write hazards, the three reasons for multi-object transactions, and the retry caveat list. **Added:** **conditional writes / compare-and-set** named here as a single-object primitive with a forward link to lost-update prevention, and the Aerospike/Cassandra/ScyllaDB examples of linearizable single-object operations that are explicitly *not* transactions.

## Related
- up: [[What Exactly Is a Transaction (2e)]] · chapter: [[Ch 08 - Transactions (2e)]]
- [[Preventing Lost Updates (2e)]] — where compare-and-set is used properly
- [[Weak Isolation Levels (2e)]] — what happens without full isolation
- [[Two-Phase Commit (2e)]] — committing across systems with side effects
- 1st edition: [[Single-Object and Multi-Object Operations]] — the same subtopic
