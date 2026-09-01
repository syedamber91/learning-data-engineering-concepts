---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 9
chapter_title: The Trouble with Distributed Systems
type: topic
tags: [ddia2, partial-failure, nondeterminism, fault-tolerance]
sources:
  - raw/ch09.md
---
# Faults and Partial Failures
**A program on a single computer normally behaves predictably: either it works or it doesn't.** Buggy software may give the appearance that the computer is "having a bad day" — often fixed by a reboot — **but that is mostly just a consequence of badly written software.**

**There is no fundamental reason software on a single computer should be flaky.** When hardware works correctly, the same operation always produces the same result — it is **deterministic**. When there is a hardware problem such as memory corruption or a loose connector, **the consequence is usually a total system failure**: kernel panic, blue screen of death, failure to start. **An individual computer with good software is usually either fully functional or entirely broken, but not something in between.**

**This is a deliberate design choice.** If an internal fault occurs, **we prefer a computer to crash completely rather than return a wrong result, because wrong results are difficult and confusing to deal with.** So computers **hide the fuzzy physical reality on which they are implemented and present an idealized system model that operates with mathematical perfection.** (**This is not actually true** — data does get silently corrupted and CPUs do sometimes return the wrong result — **but it happens rarely enough that we can get away with ignoring it.**)

**Software running on several computers connected by a network is fundamentally different.** Faults occur much more frequently, so **we can no longer ignore them — we have no choice but to confront the messy reality of the physical world.** The book quotes Coda Hale's anecdote of what that reality contains: long-lived network partitions in a single datacenter, PDU failures, switch failures, accidental power cycles of whole racks, whole-datacenter backbone and power failures, **and a hypoglycemic driver smashing his Ford pickup truck into a datacenter's HVAC system** — "and I'm not even an ops guy."

## Key Takeaways
- **A partial failure is when some parts of the system are broken in an unpredictable way while other parts work fine.** The difficulty is that **partial failures are nondeterministic**: anything involving multiple nodes and the network may sometimes work and sometimes unpredictably fail — **and you may not even know whether something succeeded.**
- **This nondeterminism and possibility of partial failure is what makes distributed systems hard to work with.**
- **But the payoff is real.** If a distributed system can tolerate partial failures, powerful possibilities open up — **rolling upgrades**, rebooting one node at a time to install updates while the system keeps working. **Fault tolerance therefore lets us make distributed systems more reliable than single-node systems: we can build a reliable system from unreliable components.**
- **Before implementing fault tolerance you need to know the faults you're supposed to tolerate.** Consider a wide range of possible faults, even fairly unlikely ones, **and artificially create such situations in your testing environment to see what happens.** **In distributed systems, suspicion, pessimism, and paranoia pay off.**

## Since the 1st Edition
Very close to the 1st edition's [[Faults and Partial Failures]] — the same single-computer determinism argument, the same Coda Hale anecdote, and the same "build a reliable system from unreliable components" conclusion. The 1st edition also included a "Cloud computing and supercomputing" comparison here, which the 2nd edition **moved forward to Chapter 1** as [[Cloud Computing Versus Supercomputing (2e)]].

## Related
- chapter: [[Ch 09 - The Trouble with Distributed Systems (2e)]]
- [[Problems with Distributed Systems (2e)]] — the same warning stated in Chapter 1
- [[Hardware and Software Faults (2e)]] — the fault rates behind "rarely enough to ignore"
- [[Fault Tolerance (2e)]] — fault injection as the recommended test approach
- 1st edition: [[Faults and Partial Failures]] — the same topic
