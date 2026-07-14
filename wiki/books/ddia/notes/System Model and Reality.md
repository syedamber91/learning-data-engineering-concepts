---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 8
chapter_title: The Trouble with Distributed Systems
topic: Knowledge, Truth, and Lies
type: subtopic
tags: [ddia, system-models, safety-liveness, correctness, formal-methods]
sources:
  - raw/ch08.md
---
# System Model and Reality
> Algorithms are proved correct against explicit system models — timing assumptions crossed with failure modes — with safety properties holding unconditionally and liveness properties allowed caveats; but reality can still exceed the model.

## The Idea
Distributed algorithms must not depend on the quirks of particular hardware and software. The tool for this is a *system model*: a formal abstraction stating exactly which faults an algorithm may assume can and cannot occur. Proofs of correctness are proofs *within a model* — which makes choosing a realistic model the crucial judgment call.

## How It Works
**Timing models**, three standard choices: the *synchronous model* assumes bounded network delay, bounded process pauses, and bounded clock error — not zero or perfectly synced, just never exceeding a known cap; unrealistic for most practical systems, as this chapter has shown. The *partially synchronous model* behaves synchronously most of the time but occasionally blows past all bounds arbitrarily — the realistic middle ground, since networks and processes are usually well behaved but timing assumptions do shatter. The *asynchronous model* permits no timing assumptions at all, not even a clock (so no timeouts) — very restrictive, but some algorithms manage. **Node-failure models**, three more: *crash-stop* (a failed node never returns), *crash-recovery* (nodes may crash and later return, with stable storage surviving but in-memory state lost), and *Byzantine* (nodes may do anything, including deceive — see [[Byzantine Faults]]). For real systems, partially synchronous + crash-recovery is generally the most useful pairing.

**Correctness** is defined by properties, e.g., for a fencing-token generator: *uniqueness* (no token issued twice), *monotonic sequence* (if request x completed before y began, x's token is smaller), *availability* (a non-crashed requester eventually gets a response). The critical split is **safety vs liveness**: safety ≈ nothing bad happens, liveness ≈ something good eventually happens — the word "eventually" is the tell, and yes, [[Eventual Consistency]] is a liveness property. Precisely: a safety violation points to a specific moment where it broke and cannot be undone; a liveness property may be unsatisfied now yet always retain hope. The methodological payoff: demand safety *always*, in every model-permitted situation — even total node failure must not produce a wrong result — while liveness may carry caveats like "provided a majority survives and the network eventually heals" (partial synchrony itself requires outages to be finite).

## Trade-offs & Pitfalls
Models are maps, not territory. Crash-recovery assumes stable storage survives crashes — but disks get corrupted, wiped by misconfiguration, or vanish behind firmware bugs after reboot; a quorum node with amnesia breaks the quorum condition and the algorithm's correctness with it. Modeling "storage that mostly survives" is more honest and much harder to reason about. Real implementations sometimes need code for "impossible" cases, even if it just logs and exits for a human to clean up — Kleppmann quips this is the line between computer science and software engineering. Still, models are invaluable: theoretical analysis exposes bugs that hide in real systems for years until timing assumptions break; proof and empirical testing are complements, not rivals.

## Examples & Systems
Fencing-token property specification; quorum amnesia via lost stable storage; firmware that forgets its disks on reboot; partially-synchronous crash-recovery as the workhorse model for Ch 9's consensus algorithms.

## Related
- up: [[Knowledge, Truth, and Lies]] · chapter: [[Ch 08 - The Trouble with Distributed Systems]]
- [[Byzantine Faults]] — sibling: the harshest failure model
- [[Fault-Tolerant Consensus]] — algorithms proved within these models
- [[Eventual Consistency]] — the liveness property named here
- [[Limitations of Quorum Consistency]] — quorum conditions that storage amnesia breaks
