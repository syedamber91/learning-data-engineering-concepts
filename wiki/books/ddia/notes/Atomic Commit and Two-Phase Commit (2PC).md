---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 9
chapter_title: Consistency and Consensus
topic: Distributed Transactions and Consensus
type: subtopic
tags: [ddia, two-phase-commit, atomic-commit, coordinator]
sources:
  - raw/ch09.md
---
# Atomic Commit and Two-Phase Commit (2PC)
> 2PC achieves all-or-nothing commit across nodes through two irrevocable promises — a participant's "yes" surrenders its right to abort, and the coordinator's logged decision is final — but a crashed coordinator leaves participants blocked "in doubt".

## The Idea
On a single node, atomicity ([[ACID]]) hinges on one device: the storage engine writes the transaction's data durably (via the [[Write-Ahead Log]]), then appends a commit record; the instant the disk finishes that record is the commit point. With multiple nodes — a multi-object transaction in a partitioned database, or a term-partitioned secondary index ([[Partitioning and Secondary Indexes]]) — just sending "commit" to everyone is unsafe: one node may hit a constraint violation, another's request may be lost, a third may crash mid-commit. Since a commit, once visible, is irrevocable (other transactions build on it — the foundation of [[Read Committed]]), a node may only commit when it's *certain* everyone else will too. That is the **atomic commit problem**. [[Two-Phase Commit]] is its classic solution — and, importantly, it is *not* the same thing as [[Two-Phase Locking (2PL)]]: 2PC provides atomic commit, 2PL provides serializable isolation; the name similarity is pure misfortune.

## How It Works
2PC introduces a **coordinator** (transaction manager), often a library inside the application process. The flow as a system of promises:
1. The application gets a globally unique transaction ID from the coordinator and runs ordinary single-node transactions on each **participant**, tagged with that ID. Anything failing here → abort freely.
2. **Phase 1 (prepare):** the coordinator asks every participant whether it can commit. A participant answering "yes" must first make the transaction durable on disk and check all constraints — it thereby *promises to commit under all circumstances* (crash, power failure, full disk are no longer excuses) while not yet committing. It has surrendered its right to abort.
3. **Commit point:** with all votes in, the coordinator decides (commit only on unanimous "yes") and writes the decision to *its own* transaction log — 2PC's commit point reduces to a single-node atomic commit on the coordinator.
4. **Phase 2:** the decision goes out to all participants. If a request fails, the coordinator retries *forever* — the decision is irrevocable. A participant that crashed after voting "yes" must commit on recovery.

"Irrevocable" describes phase 2, not eternity: a committed transaction can still be undone afterward, but only by a brand-new, separate transaction that reverses its effects — a **compensating transaction**. 2PC guarantees the commit itself can't be unwound from inside the protocol; whether a later compensating transaction is a correct undo of the original (e.g. it doesn't clash with something else that happened in between) is the application's problem, not the database's.

## Trade-offs & Pitfalls
- **Coordinator failure creates in-doubt participants.** Before prepare, a participant can abort unilaterally; after voting "yes", it can neither commit nor abort alone — a timeout doesn't help (aborting could disagree with a participant that already committed). It must simply wait for the coordinator to recover and read its log; transactions with no commit record there are aborted. 2PC is therefore a **blocking** atomic commit protocol.
- **Three-phase commit** (3PC) is nonblocking in theory but assumes bounded network delay and response times; with unbounded delays and [[Process Pauses]], a nonblocking protocol would need a perfect failure detector, which timeouts are not — so 2PC persists despite its flaw.
- Atomic commit is formalized differently from [[Consensus]] (commit requires *every* vote; consensus any proposed value, from a majority), yet the two are reducible to each other; nonblocking atomic commit is strictly harder than consensus.

## Examples & Systems
XA transactions and Java Transaction API expose 2PC to applications; WS-AtomicTransaction for SOAP; coordinator implementations include Narayana, JOTM, BTM, MSDTC. The book's memorable analogy: a wedding — the officiant collects both "I do"s (prepare), and once pronounced, the marriage stands even if you faint before hearing it; you query the officiant afterward.

## Related
- up: [[Distributed Transactions and Consensus]] · chapter: [[Ch 09 - Consistency and Consensus]]
- [[Distributed Transactions in Practice]] — XA, held locks, and operational fallout
- [[Fault-Tolerant Consensus]] — elected coordinators and majority votes fix the blocking
- [[Single-Object and Multi-Object Operations]] — why multi-object atomicity matters
- [[The Meaning of ACID]] — the atomicity contract being upheld
