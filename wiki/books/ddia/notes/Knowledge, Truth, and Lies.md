---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 8
chapter_title: The Trouble with Distributed Systems
type: topic
tags: [ddia, system-models, quorum, epistemology, correctness]
sources:
  - raw/ch08.md
---
# Knowledge, Truth, and Lies

After networks that lie by silence, clocks that lie by drift, and processes that vanish mid-thought, a philosophical question becomes an engineering one: what can a node actually *know*? Nothing for certain — a node's entire view of the world is inferred from messages received or not received, and a missing reply cannot distinguish a dead peer from a dead link. Rather than despair, the chapter's answer is discipline: state your assumptions explicitly as a *system model*, then design algorithms provably correct within that model. Reliable behavior is achievable atop unreliable foundations, but it must be constructed, not assumed. This topic covers three pillars. First, truth by vote: since no single node's self-assessment can be trusted (a paused node believes it is a healthy leader), decisions like "is that node dead?" go to a [[Quorum]], and mechanisms like [[Fencing Tokens]] stop deposed leaders from corrupting shared resources. Second, the honesty boundary: this book assumes nodes are unreliable but truthful; [[Byzantine Faults]] — nodes that actively lie — belong to aerospace and blockchains, though cheap defenses against *accidental* lies (checksums, input sanitization, multi-server NTP) are worthwhile. Third, formalization: timing models (synchronous, partially synchronous, asynchronous) crossed with failure models (crash-stop, crash-recovery, Byzantine), and correctness split into safety properties (never violated, ever) and liveness properties (eventually satisfied, given caveats).

## Subtopics
- [[The Truth Is Defined by the Majority]] — why a node must accept the quorum's verdict over its own senses, and how fencing tokens protect resources from self-appointed leaders.
- [[Byzantine Faults]] — lying nodes, the Byzantine Generals Problem, where BFT matters (flight control, Bitcoin) and why datacenter systems skip it.
- [[System Model and Reality]] — the standard timing and node-failure models, safety vs liveness, and the gap between proofs and production.

## Key Takeaways
- A node cannot trust its own judgment — leadership, lock ownership, even "how long was I asleep" must be validated against the majority.
- Only one majority can exist at a time, which is what makes quorum decisions safe.
- Protecting a resource requires the *resource itself* to check fencing tokens; trusting clients to check their own lock status is insufficient.
- Assume honest-but-unreliable nodes unless you have multiple mutually distrustful organizations or radiation-hardened requirements.
- Prove safety properties unconditionally; grant liveness properties caveats ("if a majority survives and the network heals").
- The partially synchronous, crash-recovery model best matches real systems — and even proofs within it can be betrayed by realities like disks that forget.

## Related
- up: [[Ch 08 - The Trouble with Distributed Systems]]
- [[Fault-Tolerant Consensus]] — Ch 9 algorithms built on these models
- [[Limitations of Quorum Consistency]] — quorum mechanics from Ch 5
- [[Membership and Coordination Services]] — ZooKeeper's role in leader/lock truth
- [[Eventual Consistency]] — a liveness property, as this topic clarifies
