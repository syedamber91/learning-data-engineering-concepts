---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 2
chapter_title: Defining Nonfunctional Requirements
topic: Reliability and Fault Tolerance
type: subtopic
tags: [ddia2, fault-tolerance, spof, fault-injection, chaos-engineering]
sources:
  - raw/ch02.md
---
# Fault Tolerance
> Tolerance is always *of specific faults, up to a specific number*. A system that claims to tolerate "faults" without qualification is a system nobody has thought about carefully.

## The Idea
A system is **fault-tolerant** if it continues providing the required service to users in spite of certain faults occurring. If a system cannot tolerate a particular part becoming faulty, that part is a **single point of failure (SPOF)** — a fault there escalates into failure of the whole system.

## How It Works
The case study gives a concrete example. During fan-out, a machine updating materialized timelines might crash or become unavailable. Making the process fault-tolerant means ensuring another machine can take over **without missing any posts that should have been delivered and without duplicating any** — which is **exactly-once semantics**, examined in the stream processing chapter.

**Tolerance is bounded.** A system might tolerate a maximum of two hard drives failing simultaneously, or one of three nodes crashing. It makes no sense to aim for tolerance of *any* number of faults: if all nodes crash, nothing can be done. The book's illustration is deliberately absurd — surviving the Earth being swallowed by a black hole would require web hosting in space, and good luck getting that budget approved. The serious point is that the bound must be stated.

**Fault injection.** Counterintuitively, in a fault-tolerant system it can make sense to *increase* the rate of faults by triggering them deliberately — for example, randomly killing individual processes without warning. Many critical bugs are actually due to poor error handling, so deliberately inducing faults keeps the fault-tolerance machinery continually exercised and tested, increasing confidence that faults will be handled correctly when they occur naturally. **Chaos engineering** is the discipline built around improving confidence in fault-tolerance mechanisms through such experiments.

## Trade-offs & Pitfalls
- Untested fault-tolerance machinery is not fault tolerance; it is untested code on the least-exercised path in the system. That is the whole argument for fault injection.
- Tolerating faults is generally preferable to preventing them, but not universally: where no cure exists, prevention is better. Security is the given example — a compromise that exposed sensitive data cannot be undone. This book mostly deals with the kinds of faults that *can* be cured.

## Examples & Systems
Chaos engineering as the named discipline; exactly-once semantics as the correctness target for a fault-tolerant fan-out.

## Since the 1st Edition
The core idea is unchanged, but **fault injection and chaos engineering are new material** — chaos engineering had not yet consolidated into a named discipline in the 1st edition's treatment. The explicit "tolerance is bounded, state the bound" framing and the SPOF terminology are also sharper here.

## Related
- up: [[Reliability and Fault Tolerance (2e)]] · chapter: [[Ch 02 - Defining Nonfunctional Requirements (2e)]]
- [[Fault Tolerance (Stream Processing) (2e)]] — exactly-once semantics worked out properly
- [[Formal Methods and Randomized Testing (2e)]] — the rigorous end of the same instinct
- [[Hardware and Software Faults (2e)]] — what you are tolerating
