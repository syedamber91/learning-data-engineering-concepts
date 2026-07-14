---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 1
chapter_title: Reliable, Scalable, and Maintainable Applications
topic: Reliability
type: subtopic
tags: [ddia, software-bugs, systematic-faults, cascading-failure]
sources:
  - raw/ch01.md
---
# Software Errors
> Systematic software faults are correlated across nodes — one bad assumption can take down every instance at once — making them far more damaging than random hardware failures.

## The Idea
Where hardware faults strike machines independently, software faults are *systematic*: the same bug ships to every node, so when the trigger arrives, everything breaks together. This correlation is exactly why they cause many more whole-system failures than uncorrelated hardware problems, and why they are harder to anticipate.

## How It Works
The chapter catalogs the main shapes this class takes:
- A bug that crashes *every* application server given one particular bad input — the June 30, 2012 leap second, which hung many services simultaneously via a Linux kernel bug, is the canonical case (clock trouble returns in depth in [[Unreliable Clocks]]).
- A runaway process that exhausts a shared resource: CPU, memory, disk space, or network bandwidth.
- A depended-on service that slows down, stops responding, or starts returning corrupted answers.
- Cascading failures, where a small fault in one component trips a fault in the next, which trips more — the failure propagates through the system.

The underlying mechanism is usually a hidden assumption: the software presumes something about its environment that is true almost always, until circumstances make it false. Because the assumption held for so long, the bug lies dormant and untested until the unusual condition finally arrives — everywhere at once.

## Trade-offs & Pitfalls
There is no single fix for systematic faults; the defense is an accumulation of small practices: deliberately examining assumptions and component interactions, thorough testing, process isolation, letting processes crash and restart cleanly, and measuring and monitoring production behavior. A particularly powerful pattern: if the system claims a guarantee — e.g. a message queue promising that messages in equals messages out — have it continuously audit that invariant at runtime and alert on any discrepancy. The pitfall to avoid is treating software faults like hardware faults: redundancy is useless when every replica runs the same bug.

## Examples & Systems
- The 2012 leap-second Linux kernel bug that froze applications across the internet simultaneously.
- Message-queue self-checking (incoming count vs. outgoing count) as a live invariant audit.
- Cascading-failure incidents such as the 2011 Amazon EC2/RDS US-East disruption cited by the chapter's references.

## Related
- up: [[Reliability]] · chapter: [[Ch 01 - Reliable, Scalable, and Maintainable Applications]]
- [[Hardware Faults]] — the uncorrelated fault class this contrasts with
- [[Human Errors]] — the third fault class: the people running the system
- [[Unreliable Clocks]] — Ch 8: why time-related assumptions are especially treacherous
- [[Faults and Partial Failures]] — Ch 8: fault reasoning at distributed scale
