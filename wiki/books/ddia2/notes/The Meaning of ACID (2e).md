---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 8
chapter_title: Transactions
topic: What Exactly Is a Transaction
type: subtopic
tags: [ddia2, acid, atomicity, consistency, isolation, durability, base]
sources:
  - raw/ch08.md
---
# The Meaning of ACID
> Coined in 1983 to establish precise terminology. Today, "ACID compliant" tells you almost nothing — the book calls it "mostly a marketing term."

## The Idea
**ACID** — atomicity, consistency, isolation, durability — was coined in **1983 by Theo Härder and Andreas Reuter** to establish precise terminology for fault-tolerance mechanisms in databases. **In practice one database's implementation of ACID does not equal another's**; there is a lot of ambiguity around isolation in particular. **The high-level idea is sound, but the devil is in the details, and "ACID" has unfortunately become mostly a marketing term.**

> Systems not meeting the ACID criteria are sometimes called **BASE** — basically available, soft state, eventual consistency. **This is even more vague**; the only sensible definition of BASE seems to be "not ACID."

## How It Works
**Atomicity.** *Atomic* means different things in different branches of computing: in multithreaded programming an atomic operation is one no other thread can observe half-finished. **In ACID, atomicity is not about concurrency at all** — that is covered by the I. **ACID atomicity describes what happens if a client wants to make several writes but a fault occurs after some have been processed**: a process crashes, a network connection is interrupted, a disk becomes full, an integrity constraint is violated. If the writes are grouped into an atomic transaction that cannot be committed, **the transaction is aborted and the database must discard or undo any writes made so far.** Without it, after a partway error it is difficult to know which changes took effect; retrying risks making some changes twice. **The ability to abort on error and discard all that transaction's writes is the defining feature — "abortability" would perhaps have been a better term than atomicity.**

**Consistency.** **The word is terribly overloaded — the book counts at least five meanings:** replica consistency and eventual consistency in replication; a *consistent snapshot* (consistent with the happens-before relation); *consistent hashing* as a sharding approach; consistency in the *CAP theorem*, where it means linearizability; and **in ACID, an application-specific notion of the database being in a "good state."**

ACID consistency means you have **invariants** that must always be true — in an accounting system, credits and debits across all accounts must balance. If a transaction starts from a valid database and its writes preserve validity, the invariants always hold (though **an invariant may be temporarily violated during execution, it should be satisfied again at commit**). To have the database enforce invariants you must **declare them as constraints in the schema** — foreign-key, uniqueness, and check constraints; more complex requirements can sometimes be modelled with triggers or materialized views. **But complex invariants can be difficult or impossible to express**, and then it is the application's responsibility to define its transactions correctly. **If you write bad data violating invariants you never declared, the database can't stop you** — so **the C in ACID often depends on how the application uses the database and is not a property of the database alone.**

**Isolation.** Most databases are accessed by several clients at once, which is fine until they touch the same records. The book's example: two clients concurrently incrementing a counter with read-modify-write; **it should go from 42 to 44 but goes to 43.** Isolation means concurrently executing transactions are isolated from each other and cannot step on each other's toes. **The classic textbooks formalize isolation as serializability**: each transaction can pretend it is the only one running, and the database ensures the committed result is the same as if they had run serially. **But serializability has a performance cost**, so in practice many databases use weaker forms, allowing limited interference. **Some popular databases don't even implement it** — Oracle has an isolation level called "serializable" that actually implements snapshot isolation, a weaker guarantee.

**Durability.** The promise that **after a transaction commits successfully, any data it wrote will not be forgotten, even given a hardware fault or database crash.** On a single node that typically means writing to nonvolatile storage; since regular file writes are buffered in memory, databases use **`fsync`** to ensure data really reached disk, plus a **write-ahead log** to recover from a crash partway through a write, plus **checksums** (MySQL, MongoDB, PostgreSQL) to detect corrupted or incomplete log entries. **In a replicated database, durability may mean the data was successfully copied to a certain number of nodes**, and the database must wait for those writes or replications before reporting commit. **But perfect durability does not exist**: if all your disks and all your backups are destroyed simultaneously, nothing can save you.

## Trade-offs & Pitfalls
**Replication and durability — nothing is perfect.** Historically durability meant writing to archive tape, then disk or SSD, more recently replication. The book's catalogue of why no single technique suffices:
- **Write to disk and the machine dies** — the data isn't lost but is inaccessible until you fix the machine or move the disk. Replicated systems stay available.
- **A correlated fault** — a power outage, or a bug crashing every node on a particular input — **can knock out all replicas at once**, losing anything only in memory. **So writing to disk is still relevant for replicated databases.**
- **In an asynchronously replicated system, recent writes may be lost** when the leader becomes unavailable.
- **SSDs have been shown to sometimes violate their guarantees on sudden power loss; even `fsync` isn't guaranteed to work correctly.** Disk firmware has bugs like any other software — **causing drives to fail after exactly 32,768 hours of operation**. And **`fsync` is hard to use: even PostgreSQL used it incorrectly for over 20 years.**
- **Subtle interactions between the storage engine and the filesystem** can corrupt files after a crash, and **filesystem errors on one replica can sometimes spread to other replicas.**
- **Data on disk can gradually become corrupted without detection.** If it has been corrupted for some time, replicas and recent backups may be corrupted too, and you must restore from a historical backup.
- **One study found 30–80% of SSDs develop at least one bad block in the first four years**, only some correctable by firmware. Magnetic drives have fewer bad sectors but a higher rate of complete failure.
- **A worn-out SSD disconnected from power can start losing data within weeks to months**, depending on temperature.

**No one technique provides absolute guarantees. There are only risk-reduction techniques — writing to disk, replicating to remote machines, backups — and they can and should be used together.** As always, **take any theoretical "guarantees" with a healthy grain of salt.**

## Examples & Systems
Oracle's misnamed "serializable"; `fsync`, WALs, and checksums in MySQL/MongoDB/PostgreSQL.

## Since the 1st Edition
The four definitions and the "ACID is a marketing term" verdict carry over from the 1st edition's [[The Meaning of ACID]], as does the BASE aside. **The durability discussion is substantially expanded**: the 1st edition's replication-versus-durability box was shorter, and the 2nd adds the 32,768-hour firmware bug, PostgreSQL's 20-year `fsync` misuse, filesystem errors propagating between replicas, the 30–80% bad-block study, and worn-SSD data retention. The list of five meanings of "consistency" is also new — the 1st edition listed fewer.

## Related
- up: [[What Exactly Is a Transaction (2e)]] · chapter: [[Ch 08 - Transactions (2e)]]
- [[Weak Isolation Levels (2e)]] — the I, examined at length
- [[Hardware and Software Faults (2e)]] — the failure rates behind the durability caveats
- [[Enforcing Constraints (2e)]] — the C as a distributed-systems problem
- 1st edition: [[The Meaning of ACID]] — the same subtopic
