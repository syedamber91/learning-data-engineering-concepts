---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 8
chapter_title: Transactions
type: topic
tags: [ddia2, isolation, race-conditions, concurrency-bugs, security]
sources:
  - raw/ch08.md
---
# Weak Isolation Levels
**If two transactions don't access the same data, or both are read-only, they can safely run in parallel.** Concurrency issues arise only when one transaction reads data another is concurrently modifying, or when two try to modify the same data.

**Concurrency bugs are hard to find by testing**, because they trigger only when you get unlucky with timing — rare occurrences that are usually difficult to reproduce. **Concurrency is also difficult to reason about**, especially in a large application where you don't necessarily know what other code is touching the database. Application development is hard enough with one user at a time; **many concurrent users make it much harder, because any piece of data could unexpectedly change at any time.**

So databases have long tried to hide concurrency from application developers through **transaction isolation**. In theory, **serializable** isolation means the database guarantees transactions have the same effect as if they ran one at a time. **In practice, serializable isolation has a performance cost, and many databases don't want to pay it** — so systems commonly use **weaker levels** that protect against some concurrency issues but not all. **Those levels are much harder to understand and can lead to subtle bugs, but they are nevertheless used in practice.**

## Subtopics
- [[Read Committed (2e)]] — the most basic level: no dirty reads, no dirty writes.
- [[Snapshot Isolation and Repeatable Read (2e)]] — reading from a consistent point in time, via MVCC.
- [[Preventing Lost Updates (2e)]] — the read-modify-write race, and five ways to stop it.
- [[Write Skew and Phantoms (2e)]] — the subtler anomaly that only serializability prevents.

## Key Takeaways
- **This is not a theoretical problem.** Concurrency bugs from weak isolation and race conditions have **caused substantial loss of money — including bankrupting a Bitcoin exchange — led to investigation by financial auditors, and caused customer data to be corrupted.**
- **"Use an ACID database if you're handling financial data!" misses the point.** Even many popular relational systems, usually considered ACID, **use weak isolation by default**, so they wouldn't necessarily have prevented these bugs.
- **This is also a security problem.** Even if concurrency issues are rare in normal operation, **an attacker might deliberately send a burst of highly concurrent requests to your API to exploit concurrency bugs.** To build reliable *and secure* applications, such bugs must be **systematically prevented**, not left to luck.
- The book notes drily that **much of the banking system relies on text files exchanged via secure FTP**, where **an audit trail and human-level fraud prevention matter more than ACID properties.**
- The chapter's approach is deliberately **informal, using examples**; rigorous definitions live in the academic literature.

## Since the 1st Edition
The 1st edition's [[Weak Isolation Levels]] made the same argument with the same Bitcoin exchange and financial-audit examples. **Added:** the explicit **security framing** — that an attacker can deliberately generate concurrency to exploit these bugs, so systematic prevention is a security requirement rather than a robustness nicety. The subtopic structure is unchanged.

## Related
- chapter: [[Ch 08 - Transactions (2e)]]
- [[Serializability (2e)]] — the level that prevents everything here
- [[The Meaning of ACID (2e)]] — where isolation is defined
- 1st edition: [[Weak Isolation Levels]] — the same topic
