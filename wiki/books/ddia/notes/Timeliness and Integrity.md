---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 12
chapter_title: The Future of Data Systems
topic: Aiming for Correctness
type: subtopic
tags: [ddia, consistency, integrity, coordination-avoidance]
sources:
  - raw/ch12.md
---
# Timeliness and Integrity

> "Consistency" conflates two separable demands — seeing fresh data (timeliness) and never corrupting data (integrity) — and dataflow systems win by keeping only the one that actually matters.

## The Idea
Transactions are typically linearizable: the writer waits for commit, then everyone sees the write. Unbundled multi-stage dataflow is asynchronous by design — a sender doesn't wait for consumers — though a client *may* wait on an output stream (as in the uniqueness check of [[Enforcing Constraints]]); notably, waiting affects only *notification*, not the correctness of the processing itself. From this Kleppmann splits consistency into:
- **Timeliness** — users observe up-to-date state. Violations (replication lag, stale reads) are temporary; retry later and they vanish. [[Linearizability]] is a strong timeliness property (the [[CAP Theorem]]'s sense of consistency); read-after-write is a weaker useful one.
- **Integrity** — absence of corruption: no lost data, no contradictions, derived views correctly reflecting their sources. Violations are permanent; waiting fixes nothing, only explicit repair does. ACID "C" is really application-level integrity, with atomicity and durability as its tools.
Slogan: timeliness violations are "eventual consistency"; integrity violations are "perpetual inconsistency." In most applications integrity dominates — a day's lag on a credit-card statement is normal; a statement that doesn't add up, or a charge that vanished between customer and merchant, is catastrophic.

## How It Works
ACID delivers both properties together, so the distinction hardly matters there. Event-based dataflow *decouples* them: no timeliness unless you build waiting in, but integrity is the core streaming guarantee. [[Exactly-Once Semantics]] is an integrity mechanism — fault-tolerant delivery plus duplicate suppression. The integrity recipe, without distributed transactions: (1) represent each write as a single, atomically appendable immutable message ([[Event Sourcing]]-friendly); (2) derive all downstream state with deterministic derivation functions; (3) thread a client-generated request ID through everything for end-to-end [[Idempotence]]; (4) keep messages immutable so derived data can be reprocessed after bugs.

## Trade-offs & Pitfalls
- **Loose constraints suffice surprisingly often**: duplicate usernames can be apologized for, oversold stock reordered or discounted, flights overbooked deliberately, overdrafts fined — the *compensating transaction* / apology workflow already exists in most businesses (forklifts crush inventory whether or not your database coordinates). If the apology cost is acceptable, optimistic write + after-the-fact check beats validate-before-write; these apps need integrity (no lost reservations, no mismatched credits/debits) but not timely enforcement.
- **Coordination-avoiding systems**: combining (1) integrity without atomic commit and (2) tolerable loose constraints yields systems that skip synchronous coordination almost everywhere — e.g. multi-leader, multi-datacenter async replication that stays available independently — while remaining strongly integral. Coordination can be reintroduced narrowly where recovery would be impossible.
- The balance is economic: coordination reduces inconsistency-apologies but increases outage-apologies; neither reaches zero, so tune for the sweet spot.

## Examples & Systems
Credit-card settlement lag vs. sum errors; airline/hotel overbooking; overdraft fees; cross-datacenter multi-leader deployments running without cross-region coordination.

## Related
- up: [[Aiming for Correctness]] · chapter: [[Ch 12 - The Future of Data Systems]]
- [[Problems with Replication Lag]] — timeliness violations in their Ch 5 form
- [[The Cost of Linearizability]] — what strict timeliness charges you
- [[Handling Write Conflicts]] — conflict resolution kin of compensating transactions
- [[Trust, but Verify]] — auditing as integrity's enforcement arm
