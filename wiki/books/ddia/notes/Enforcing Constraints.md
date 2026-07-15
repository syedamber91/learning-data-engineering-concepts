---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 12
chapter_title: The Future of Data Systems
topic: Aiming for Correctness
type: subtopic
tags: [ddia, uniqueness-constraints, total-order, partitioned-logs]
sources:
  - raw/ch12.md
---
# Enforcing Constraints

> Uniqueness requires consensus — and a partitioned, totally ordered log with a single-threaded consumer supplies it scalably, even across partitions, without atomic commit.

## The Idea
Beyond duplicate suppression, applications need constraints: unique usernames, one passenger per seat, non-negative balances, no overselling stock, no double-booked rooms. Ch 9 established that enforcing uniqueness in a distributed setting requires [[Consensus]]: concurrent conflicting requests need one accepted, others rejected. The usual answer is a single leader deciding everything — which works until you need leader failover, putting you back at consensus. The unbundled-database question: can log-based dataflow enforce the same constraints? Yes — because a log's ordering guarantee *is* [[Total Order Broadcast]], which is equivalent to consensus.

## How It Works
- **Scaling by partition**: uniqueness checking shards cleanly — [[Partitioning]] by the value that must be unique (hash of username, request ID) routes all potential conflicts to one place, with no cross-partition coordination. Asynchronous multi-master setups are ruled out, since independent masters can both accept conflicting writes; immediate rejection demands synchronous coordination somewhere.
- **Uniqueness via a log**: (1) each username claim is a message appended to the partition chosen by hash of the username; (2) a single-threaded stream processor reads the partition sequentially, tracks taken names in local state, and emits success/rejection messages; (3) the client watches the output stream for its verdict. This mirrors linearizable storage built on total order broadcast, scales by adding partitions, and generalizes: route all writes that *might* conflict to the same partition and validate them sequentially with arbitrary logic (an idea going back to Bayou in the 1990s).
- **Multi-partition operations without atomic commit**: a transfer touches three partitions (request ID, payer, payee). Instead of [[Two-Phase Commit]] across them — which drags every partition into one total order and kills independent throughput — decompose: (1) client assigns a request ID and appends the transfer as a *single* message (single-object appends are atomic almost everywhere); (2) a stream processor reads it and emits a debit instruction partitioned by payer and a credit instruction partitioned by payee, carrying the request ID; (3) downstream processors deduplicate by request ID and apply balances. A crash mid-stage just replays deterministically; duplicates are absorbed by the end-to-end ID. Overdraft protection slots in as a validating processor, partitioned by payer, gating what enters the request log.

## Trade-offs & Pitfalls
- The client experiences the check asynchronously unless it explicitly waits on the output stream — timeliness is traded away, integrity kept (see [[Timeliness and Integrity]]).
- Correctness of the fan-out stage depends on **determinism**: reprocessing must regenerate identical instructions, or deduplication breaks.
- The strict form of a constraint still funnels each conflict domain through one thread; throughput within a partition is bounded by that.

## Examples & Systems
Twitter/Manhattan-style username claiming; Bayou's validate-on-replay heritage; the two-stage debit/credit pipeline replacing a three-partition atomic commit.

## Related
- up: [[Aiming for Correctness]] · chapter: [[Ch 12 - The Future of Data Systems]]
- [[The End-to-End Argument for Databases]] — supplies the request ID this design leans on
- [[Implementing Linearizable Systems]] — the same algorithm in Ch 9 dress
- [[Partitioned Logs]] — the substrate providing per-partition total order
- [[Handling Write Conflicts]] — conflict definitions the validating processor applies
