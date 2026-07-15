---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 7
chapter_title: Transactions
type: topic
tags: [ddia, transactions, acid, safety-guarantees]
sources:
  - raw/ch07.md
---
# The Slippery Concept of a Transaction

A transaction lets an application bundle several reads and writes into one logical unit that either commits in full or aborts and leaves no trace — collapsing a whole zoo of failure modes (crashes mid-write, network drops, concurrent clients clobbering each other, half-updated reads) into a single, retryable outcome. The model dates to IBM System R in 1975, and MySQL, PostgreSQL, Oracle, and SQL Server still follow it closely four decades later. The NoSQL wave of the late 2000s made transactions its main casualty — dropping them or quietly redefining the word — which spawned two opposing myths: that transactions are the enemy of scalability, and that no "serious" application can live without them. Both are hyperbole; transactions are a design trade-off like any other, and this topic pins down what the guarantees actually mean. Even the [[ACID]] acronym turns out to be slippery: implementations differ enough that "ACID compliant" has drifted into marketing (its foil, BASE — basically available, soft state, eventually consistent — is vaguer still, meaning little more than "not ACID").

## Subtopics

- [[The Meaning of ACID]] — atomicity is really abortability, consistency belongs to the application not the database, isolation is formally serializability but rarely delivered as such, and durability is a spectrum of risk-reduction rather than an absolute.
- [[Single-Object and Multi-Object Operations]] — where transaction guarantees are genuinely needed: single-object atomicity as a storage-engine baseline, why [[Denormalization]], foreign keys, and [[Secondary Indexes]] demand multi-object transactions, and why safe retry on abort is subtler than it looks.

## Key Takeaways

- The defining feature of a transaction is abortability: a failed transaction is guaranteed to have changed nothing, so the application can retry without fearing partial effects.
- ACID's C is the odd one out — invariants like "credits equal debits" are the application's responsibility; the database supplies atomicity, isolation, and durability as raw material.
- The word *consistency* alone carries at least four meanings in this book (replica consistency, consistent hashing, [[CAP Theorem]] linearizability, ACID invariants) — always ask which one is in play.
- Durability is never absolute: disks corrupt silently, fsync can lie on power loss, asynchronous replicas lag, and 30–80% of SSDs develop bad blocks within four years — so disk writes, [[Replication]], and backups must be layered, not chosen between.
- Single-object atomic operations (increment, compare-and-set) marketed as "lightweight transactions" are not transactions in the usual sense — the term properly means grouping operations across multiple objects.
- Retrying aborted transactions is the whole point, yet popular ORMs (ActiveRecord, Django) don't do it; and retries need care around lost commit acknowledgments, overload feedback loops, permanent errors, and non-database side effects like sending email.

## Related

- chapter: [[Ch 07 - Transactions]]
- [[Weak Isolation Levels]] — what databases actually provide instead of the textbook isolation guarantee
- [[Serializability]] — the formal ideal that ACID isolation gestures at
- [[Leaderless Replication]] — the best-effort philosophy that abandons abort-and-retry entirely
- [[Atomic Commit and Two-Phase Commit (2PC)]] — extending atomicity across multiple systems
- [[Reliability]] — the fault-tolerance framing that motivates transactions in the first place
