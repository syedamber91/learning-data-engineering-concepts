---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 7
chapter_title: Transactions
topic: The Slippery Concept of a Transaction
type: subtopic
tags: [ddia, acid, transactions, durability]
sources:
  - raw/ch07.md
---
# The Meaning of ACID
> The four letters of [[ACID]] — Atomicity, Consistency, Isolation, Durability — sound precise but hide enormous ambiguity, and one of them (C) isn't even a database property.

## The Idea
Coined by Härder and Reuter in 1983 to give fault-tolerance guarantees a precise vocabulary, ACID has since degraded into a marketing label: two databases can both claim ACID compliance while offering very different guarantees, especially around isolation. Its foil, BASE (Basically Available, Soft state, Eventual consistency — see [[Eventual Consistency]]), is defined even more loosely; in practice it just means "not ACID."

## How It Works
- **Atomicity** — nothing to do with concurrency (that's the I). It means: if a fault interrupts a transaction partway through its writes, the database rolls back everything already done, so the outcome is all-or-nothing. The real payoff is *safe retry* — a better name might have been "abortability."
- **Consistency** — the odd one out. It refers to application-defined invariants (e.g., ledger debits equal credits) staying true. The database can enforce a few invariant kinds (foreign keys, uniqueness), but in general the *application* must write transactions that preserve its invariants. So C is a property of the app, not the database — it was arguably added just to complete the acronym.
- **Isolation** — concurrent transactions must not trample each other. Textbooks formalize this as serializability: the committed outcome equals *some* serial one-at-a-time execution. Real systems rarely deliver that; Oracle's "serializable" level is actually snapshot isolation, a weaker guarantee (see [[Isolation Levels]]).
- **Durability** — once committed, data survives crashes. On one node that means nonvolatile storage plus a [[Write-Ahead Log]] for recovery; in a replicated system it can mean copying to enough nodes before acknowledging (see [[Replication]]).

## Trade-offs & Pitfalls
- "ACID compliant" tells you almost nothing concrete — always check the actual isolation semantics.
- Perfect durability is a fiction: fsync can misbehave on power loss, SSD firmware has bugs, disks silently corrupt data over time, 30–80% of SSDs develop bad blocks within four years, and correlated faults can take out every replica at once. Disk writes, remote replication, and backups are complementary risk reducers, not guarantees.
- Asynchronously replicated systems may lose recent writes on leader failure ([[Handling Node Outages]]).

## Examples & Systems
The transactional style dates to IBM System R (1975) and survives nearly unchanged in MySQL, PostgreSQL, Oracle, and SQL Server. Oracle 11g's "serializable" is really snapshot isolation. The counter-increment race (two clients read 42, both write 43) is the canonical isolation failure.

## Related
- up: [[The Slippery Concept of a Transaction]] · chapter: [[Ch 07 - Transactions]]
- [[Single-Object and Multi-Object Operations]] — where atomicity and isolation actually apply
- [[Snapshot Isolation and Repeatable Read]] — what Oracle's "serializable" really is
- [[Reliability]] — why perfect durability can't exist
- [[CAP Theorem]] — yet another, different meaning of "consistency"
