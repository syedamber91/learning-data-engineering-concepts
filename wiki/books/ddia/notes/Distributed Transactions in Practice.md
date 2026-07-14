---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 9
chapter_title: Consistency and Consensus
topic: Distributed Transactions and Consensus
type: subtopic
tags: [ddia, xa-transactions, exactly-once, in-doubt-locks]
sources:
  - raw/ch09.md
---
# Distributed Transactions in Practice
> XA-style heterogeneous transactions deliver real value (exactly-once message processing) but earn their bad reputation: ~10x slowdowns, in-doubt transactions clutching locks through outages, and a coordinator that quietly becomes a single point of failure.

## The Idea
Distributed transactions — especially [[Two-Phase Commit]]-based ones — are simultaneously praised as a safety guarantee that's hard to get any other way and blamed for killing performance and causing outages; many cloud services refuse to offer them. MySQL's distributed transactions have been measured at over 10x slower than single-node ones, mostly from the extra `fsync` disk forcing needed for crash recovery plus additional network round-trips. Before judging, separate two conflated kinds: **database-internal** distributed transactions (all nodes run the same software — e.g., VoltDB, MySQL Cluster NDB — free to use optimized private protocols, often fine) and **heterogeneous** ones spanning different technologies (two vendors' databases, or a database plus a message broker), which are far harder.

## How It Works
**Exactly-once message processing.** The killer app for heterogeneous transactions: atomically commit a message acknowledgment on the broker together with the database writes that processed it. If either side fails, both abort and the broker safely redelivers — the message takes effect exactly once ([[Exactly-Once Semantics]]) even across retries. This only works if *every* system with side effects speaks the same atomic commit protocol (an email server that can't participate may resend on retry).

**XA transactions.** X/Open XA (1991) is the standard for 2PC across heterogeneous systems — not a network protocol but a C API for talking to a transaction coordinator, supported by PostgreSQL, MySQL, DB2, SQL Server, Oracle, and brokers like ActiveMQ, HornetQ, MSMQ, IBM MQ (in Java via JTA over JDBC/JMS drivers). The coordinator is typically a library inside the application process, logging commit/abort decisions to the *application server's local disk*. If that process or machine dies, prepared-but-uncommitted participants are stuck in doubt until the same server restarts and replays the log — participants cannot contact the coordinator, since all communication flows through its client library.

**Locks held in doubt.** Why in-doubt transactions hurt: participants hold row-level exclusive locks on modified rows (and, under [[Two-Phase Locking (2PL)]], shared locks on rows read) until commit or abort. A coordinator down for 20 minutes means those locks are held 20 minutes; a lost coordinator log means *forever*, blocking every other transaction touching those rows — potentially freezing large parts of the application ([[Read Committed]]'s dirty-write protection is exactly what's holding the lock).

## Trade-offs & Pitfalls
- **Orphaned in-doubt transactions** happen in practice (corrupted/lost coordinator logs) and survive server reboots — a correct 2PC must preserve their locks across restarts. Resolution is manual, by an administrator, usually mid-outage.
- **Heuristic decisions** — a participant unilaterally committing/aborting an in-doubt transaction — are a euphemism for *probably breaking atomicity*; emergency use only.
- The coordinator is itself a database of transaction outcomes: often not replicated (single point of failure), and it makes "stateless" application servers stateful, since its logs become critical durable state.
- XA is a lowest common denominator: no cross-system deadlock detection, incompatible with [[Serializable Snapshot Isolation (SSI)]].
- Even database-internal 2PC *amplifies failures* — all participants must respond, so any broken part fails the whole transaction — the opposite of fault tolerance.

## Examples & Systems
MySQL's 10x XA penalty; VoltDB and MySQL Cluster NDB internal transactions; JTA/JDBC/JMS; MSDTC orphaned transactions; message-broker + database exactly-once pipelines (revisited with [[Log-Based Message Broker]]s in Chapter 11).

## Related
- up: [[Distributed Transactions and Consensus]] · chapter: [[Ch 09 - Consistency and Consensus]]
- [[Atomic Commit and Two-Phase Commit (2PC)]] — the protocol underneath XA
- [[Keeping Systems in Sync]] — Chapter 11's alternative to heterogeneous 2PC
- [[Messaging Systems]] — the brokers participating in these transactions
- [[Fault-Tolerant Consensus]] — what a properly replicated coordinator would look like
