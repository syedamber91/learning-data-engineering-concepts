---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 1
chapter_title: Reliable, Scalable, and Maintainable Applications
type: topic
tags: [ddia, reliability, fault-tolerance, resilience]
sources:
  - raw/ch01.md
---
# Reliability
> Reliability means a system keeps doing the right thing even when things go wrong — and "things going wrong" splits into hardware faults, software errors, and human mistakes.

A system is informally reliable when it does what users expect, tolerates mistakes and unusual usage, performs adequately under its expected load, and blocks unauthorized access. Kleppmann compresses this to: *continuing to work correctly when adversity strikes*. The pivotal distinction is **fault vs. failure**: a fault is one component drifting from its spec; a failure is the whole system no longer delivering its service. Faults can never be driven to zero probability, so the engineering goal is fault-*tolerance* — designing so faults don't escalate into failures. Total tolerance is impossible (no design survives the planet being swallowed by a black hole), so you always choose *which* fault classes to tolerate. Counterintuitively, deliberately injecting faults — Netflix's Chaos Monkey randomly kills processes — keeps the tolerance machinery exercised, because poor error handling is where many critical bugs hide. Prevention beats cure only where no cure exists, notably security breaches: leaked data cannot be un-leaked.

## Subtopics
- [[Hardware Faults]] — random, largely uncorrelated component deaths; countered with redundancy and, increasingly, software fault-tolerance.
- [[Software Errors]] — systematic, correlated bugs that lie dormant until an unusual circumstance triggers them everywhere at once.
- [[Human Errors]] — the leading cause of outages; mitigated by design, sandboxes, testing, fast recovery, and telemetry.
- [[How Important Is Reliability]] — why even "noncritical" apps owe users reliability, and when cutting corners is a conscious choice.

## Key Takeaways
- Fault ≠ failure: build systems where component faults are absorbed before users notice.
- You can only tolerate *chosen* classes of faults — be explicit about which.
- Hardware faults are random and independent; software faults are systematic and correlated, making them far more dangerous.
- Humans cause most outages; the fix is systemic (design, sandboxes, rollback, monitoring), not blame.
- Triggering faults on purpose (chaos engineering) is a legitimate reliability tool.
- Sacrificing reliability for development or operational cost can be rational — but only when done knowingly.

## Related
- chapter: [[Ch 01 - Reliable, Scalable, and Maintainable Applications]]
- [[Scalability]] — today's reliability erodes under tomorrow's load
- [[Maintainability]] — operations quality feeds directly into reliability
- [[Faults and Partial Failures]] — Ch 8 extends fault thinking to distributed systems
- [[Handling Node Outages]] — Ch 5's replication answer to machine loss
