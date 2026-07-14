---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 12
chapter_title: The Future of Data Systems
type: topic
tags: [ddia, correctness, integrity, fault-tolerance]
sources:
  - raw/ch12.md
---
# Aiming for Correctness

Stateful systems remember mistakes forever, yet the tools we trust for correctness are shakier than they look: [[ACID]] semantics vary, weak [[Isolation Levels]] confuse even experts, "consistency" is poorly defined, and Jepsen testing keeps exposing products whose guarantees don't survive real network faults. [[Serializability]] and atomic commit help but confine you to single-datacenter scale. This topic builds Kleppmann's alternative: apply the end-to-end argument (correctness must be enforced at the application boundary, not assumed from infrastructure), enforce constraints through totally ordered logs rather than locks, split "consistency" into timeliness (freshness — negotiable) and integrity (no corruption — non-negotiable), and then distrust even your own stack enough to audit it continuously.

## Subtopics
- [[The End-to-End Argument for Databases]] — why TCP, transactions, and exactly-once stream semantics still can't stop a duplicated money transfer; only client-generated operation IDs flowing end-to-end can.
- [[Enforcing Constraints]] — uniqueness needs [[Consensus]], but a partitioned log with a single-threaded stream processor provides it scalably; multi-partition transactions decompose into deterministic, deduplicated stages.
- [[Timeliness and Integrity]] — the two requirements hiding inside "consistency"; dataflow systems sacrifice the first, preserve the second, and most businesses (which already run apology workflows) need exactly that.
- [[Trust, but Verify]] — hardware flips bits, mature databases ship isolation bugs; auditing, deterministic re-derivation, and Merkle-tree-style cryptographic checks make integrity observable instead of assumed.

## Key Takeaways
- Strong database guarantees do not make an application correct: bugs, retries across connection boundaries, and user resubmissions all bypass them; duplicate suppression must travel end-to-end as a request ID.
- Uniqueness and similar constraints require synchronous coordination somewhere — but routing conflicting writes to one log partition processed sequentially is coordination enough, and it scales by partition.
- Breaking a cross-partition operation into log-append → deterministic fan-out → idempotent apply achieves exactly-once effects without [[Two-Phase Commit]].
- Timeliness violations heal with waiting ("eventual consistency"); integrity violations are permanent ("perpetual inconsistency") — so integrity matters more, and streaming systems make precisely that trade.
- Loosely interpreted constraints plus compensating transactions (apologies) match real business practice; coordination-avoiding systems exploit this for multi-datacenter performance with strong integrity.
- Since hardware and software both betray their promises occasionally, don't blindly trust — design event-sourced, deterministic dataflows whose provenance can be re-checked end to end.

## Related
- chapter: [[Ch 12 - The Future of Data Systems]] · part: [[Part III - Derived Data]]
- [[Unbundling Databases]] — the dataflow architecture whose correctness this topic secures
- [[The Slippery Concept of a Transaction]] — Ch 7's foundations being reassessed
- [[Fault Tolerance]] — stream-processing exactly-once machinery this builds upon
- [[Consistency Guarantees]] — Ch 9's vocabulary that timeliness/integrity refines
