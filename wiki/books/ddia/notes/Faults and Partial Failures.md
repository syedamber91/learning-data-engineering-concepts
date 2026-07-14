---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 8
chapter_title: The Trouble with Distributed Systems
type: topic
tags: [ddia, partial-failure, fault-tolerance, distributed-systems]
sources:
  - raw/ch08.md
---
# Faults and Partial Failures

A single computer is designed to be all-or-nothing: when hardware is healthy, the same operation deterministically yields the same result, and when something inside breaks, the machine prefers to crash outright (kernel panic, blue screen) rather than hand back a wrong answer. This deliberate design hides messy physics behind an idealized model. Distributed systems destroy that comfort. Once software spans several machines joined by a network, some pieces can be broken in unpredictable ways while others hum along fine — a *partial failure* — and these failures are nondeterministic: the same multi-node operation may succeed, fail, or leave you unable to tell which happened, because even message travel time is unpredictable. Kleppmann quotes Coda Hale's litany of real incidents — long-lived partitions, PDU and switch failures, accidental rack power-cycles, and a truck driven into a datacenter's HVAC — to show how wide the failure surface really is. The engineering response is to accept partial failure as normal and build [[Fault Tolerance]] into software, constructing a reliable whole from unreliable parts, the way TCP builds ordered, retransmitted delivery on top of IP's drop/duplicate/reorder chaos, or error-correcting codes carry clean data over noisy radio links. There is a ceiling — TCP cannot erase delay — but the higher layer absorbs enough low-level mess to make the residual faults tractable.

## Subtopics
- [[Cloud Computing and Supercomputing]] — two philosophies of large-scale computing: HPC escalates any fault to total failure and restarts from checkpoints, while cloud services must tolerate node death mid-flight and keep serving.

## Key Takeaways
- Partial failure — some nodes broken, others fine, nondeterministically — is *the* defining property that separates distributed systems from single machines.
- A single computer chooses total crash over wrong answers; a distributed system has no such global crash switch.
- You often cannot know whether an operation succeeded, because network transit time is itself nondeterministic.
- Reliable systems can be built from unreliable components (ECC over noisy channels, TCP over IP), but only up to a limit — abstraction reduces, never eliminates, the fault surface.
- Even small clusters must plan for faults; test them deliberately (Chaos-Monkey style) rather than hoping they are rare. Pessimism pays.

## Related
- up: [[Ch 08 - The Trouble with Distributed Systems]]
- [[Reliability]] — Ch 1 groundwork: fault vs failure, building dependable systems
- [[Hardware Faults]] — single-machine fault modes this chapter generalizes
- [[Unreliable Networks]] — the first concrete source of partial failure
- [[Unreliable Clocks]] — the second: timing you cannot trust
- [[Knowledge, Truth, and Lies]] — how to reason once certainty is gone
