---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 12
chapter_title: Stream Processing
topic: Databases and Streams
type: subtopic
tags: [ddia2, immutability, changelog, accounting, crypto-shredding, gdpr]
sources:
  - raw/ch12.md
---
# State, Streams, and Immutability
> Application state is what you get when you integrate an event stream over time. A change stream is what you get when you differentiate state by time.

## The Idea
**Batch processing benefits from the immutability of its input files**, and **this principle is also what makes event sourcing and CDC so powerful.**

**We normally think of databases as storing the current state**, a representation optimized for reads. **The nature of state is that it changes, so databases support updating and deleting as well as inserting. How does this fit with immutability?**

**Whenever you have state that changes, that state is the result of the events that mutated it over time.** **Your list of currently available seats is the result of the reservations you have processed; the current account balance is the result of the credits and debits; the response time graph is an aggregation of the individual response times of all requests.**

**No matter how the state changes, there was always a sequence of events that caused those changes. Even as things are done and undone, the fact remains true that those events occurred.** **The key idea is that mutable state and an append-only log of immutable events do not contradict each other; they are two sides of the same coin.** **The log of all changes — the changelog — represents the evolution of state over time.**

**If you are mathematically inclined: application state is what you get when you integrate an event stream over time, and a change stream is what you get when you differentiate the state by time.** (**The analogy has limits — the second derivative of state does not seem meaningful — but it's a useful starting point.**)

**Storing the changelog durably makes the state reproducible.** **If you consider the log of events your system of record and any mutable state as derived from it, it becomes easier to reason about the flow of data.** As Jim Gray and Andreas Reuter put it in 1992: **"There is no fundamental need to keep a database at all; the log contains all the information there is. The only reason for storing the database (i.e., the current end-of-the-log) is performance of retrieval operations."**

## How It Works
**Advantages of immutable events.** **Immutability in databases is an old idea** — **accountants have used it for centuries.** **When a transaction occurs it is recorded in an append-only ledger, essentially a log of events describing money, goods, or services changing hands, and the accounts are derived from the ledger by adding them up.** **If a mistake is made, accountants don't erase or change the incorrect transaction; they add another transaction that compensates** — refunding an incorrect charge. **The incorrect transaction remains forever, because it might be important for auditing.** **If incorrect derived figures were already published, the next period's figures include a correction. This is entirely normal in accounting.**

**Auditability is beneficial beyond finance.** **If you accidentally deploy buggy code that writes bad data, recovery is much harder if the code can destructively overwrite.** **With an append-only log, diagnosing what happened and recovering is much easier** — and **customer service can use an audit log to diagnose requests and complaints.**

**Immutable events also capture more information than just current state.** **On a shopping website a customer may add an item to their cart and then remove it. Although the second event cancels the first from the point of view of order fulfillment, it may be useful for analytics to know the customer considered that item and decided against it** — perhaps they'll buy it later, perhaps they found a substitute. **This is recorded in an event log but lost in a database that deletes cart items on removal.**

**Deriving several views from the same event log.** **By separating mutable state from the immutable log, you can derive several read-oriented representations from the same events** — just like having multiple stream consumers. **Druid ingests directly from Kafka this way, and Kafka Connect sinks export from Kafka to various databases and indexes.**

**An explicit translation step from log to database makes it easier to evolve your application.** **To introduce a feature presenting existing data in a new way, use the event log to build a separate read-optimized view and run it alongside the existing systems without modifying them.** **Running old and new side by side is often easier than a complicated schema migration** — **and once readers have switched, shut the old one down and reclaim its resources.**

**This makes normalization debates largely irrelevant.** **The traditional approach to schema design is based on the fallacy that data must be written in the same form it will be queried.** **If you can translate from a write-optimized event log to read-optimized application state, it is entirely reasonable to denormalize the read views, since the translation process keeps them consistent with the log.** **The social network home timeline is exactly this: highly denormalized, with your posts duplicated in all your followers' timelines, but the fan-out service keeps that duplicated state in sync, which keeps the duplication manageable.**

**Concurrency control.** **The biggest downside of CQRS is that log consumers are usually asynchronous, so a user could write to the log, read a derived view, and find their write not yet reflected.** **One solution is updating the read view synchronously with appending the event — but that requires either a distributed transaction across log and view, or waiting until the event is reflected, and both are usually impractical, so views are normally updated asynchronously.**

**On the other hand, deriving state from an event log simplifies some aspects of concurrency control.** **Much of the need for multi-object transactions stems from a single user action requiring changes in several places.** **With event sourcing you can design an event as a self-contained description of a user action — so the action requires only a single write in one place, appending to the log, which is easy to make atomic.** **And if the log and the application state are sharded the same way, a straightforward single-threaded log consumer needs no concurrency control for writes**: **by construction it processes only a single event at a time, and the log removes the nondeterminism of concurrency by defining a serial order of events in a shard.**

**Many systems that don't use event sourcing nevertheless rely on immutability for concurrency control** — **databases internally use immutable data structures or multiversion data for point-in-time snapshots, and version control systems such as Git, Mercurial, and Fossil rely on immutable data to preserve version history.**

## Trade-offs & Pitfalls
**Limitations of immutability.** **How feasible is keeping an immutable history forever? It depends on the amount of churn in the dataset.** **Some workloads mostly add data and rarely update or delete — easy to make immutable.** **Others have a high rate of updates and deletes on a comparatively small dataset; there the immutable history may grow prohibitively large, fragmentation may become an issue, and the performance of compaction and garbage collection becomes crucial for operational robustness.**

**Besides performance, you may need data deleted for administrative or legal reasons.** **Privacy regulations such as the GDPR require a user's personal information be deleted and erroneous information removed on demand, or an accidental leak of sensitive information may need to be contained.**

**In these circumstances it's not sufficient to append another event saying the prior data should be considered deleted — you actually want to rewrite history and pretend the data was never written.** **Datomic calls this excision; the Fossil version control system has a similar concept called shunning.**

**Truly deleting data is surprisingly hard, since copies live in many places.** **Storage engines, filesystems, and SSDs often write to a new location rather than overwriting in place, and backups are often deliberately immutable to prevent accidental deletion or corruption.**

**One way of enabling deletion is crypto-shredding**: **store data you may want to delete encrypted, and when you want to get rid of it, forget the encryption key.** **The encrypted data is still there, but nobody can use it.** **In a sense this only moves the problem: the actual data is still immutable, but your key storage is mutable.** **And you must decide up front which data is encrypted with the same key** — **you can later crypto-shred either all or none of the data under a particular key, but not some of it.** **Storing a separate key per data item would get too unwieldy, as key storage would grow as big as the primary storage.** **More sophisticated schemes such as puncturable encryption make it possible to selectively revoke a key's decryption abilities, but they are not yet widely used.**

**Overall, deletion is more a matter of "making it harder to retrieve the data" than actually "making it impossible."** **Nevertheless, you sometimes have to try.**

## Examples & Systems
Accounting ledgers as the centuries-old precedent; Druid ingesting from Kafka; Kafka Connect sinks; Git, Mercurial, Fossil; Datomic excision and Fossil shunning; crypto-shredding and puncturable encryption.

## Since the 1st Edition
The 1st edition covered this across [[State, Streams, and Immutability]] and a separate advantages-of-immutable-events discussion, including the accounting analogy, the derive-several-views argument, and the limitations-of-immutability caveat. **The 2nd edition merges them and adds:** **crypto-shredding**, with its honest accounting of what it does and doesn't solve, and **puncturable encryption** as the not-yet-practical improvement — reflecting that GDPR made deletion a real engineering requirement rather than a hypothetical.

## Related
- up: [[Databases and Streams (2e)]] · chapter: [[Ch 12 - Stream Processing (2e)]]
- [[Event Sourcing and CQRS (2e)]] — the same idea as a data model
- [[Change Data Capture (2e)]] — where log compaction bridges log and state
- [[Data Systems, Law, and Society (2e)]] — the deletion requirement
- 1st edition: [[State, Streams, and Immutability]] — the same subtopic
