---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 8
chapter_title: The Trouble with Distributed Systems
topic: Unreliable Clocks
type: subtopic
tags: [ddia, gc-pauses, leases, real-time, preemption]
sources:
  - raw/ch08.md
---
# Process Pauses
> A thread can be frozen for seconds or minutes at any line of code — GC, VM suspension, page faults — and resume convinced no time has passed, still acting on leases and leadership it lost while asleep.

## The Idea
Even with a perfect local clock, code that assumes "little time passes between these two lines" is broken in a distributed system. The canonical example: a partition leader holds a *lease* (a lock with a timeout) proving its leadership, checks that at least 10 seconds remain, then processes a request. If the thread is paused for 15 seconds right after the check, the lease expires mid-pause, another node takes over, and the woken thread — with no idea it slept — does something unsafe. (The check has a second bug: it compares an expiry set by a *different machine's* clock against the local clock, so it also depends on synchronization.)

## How It Works
Pauses of that magnitude are not exotic. Causes:
- **Garbage collection.** Stop-the-world GC pauses have been known to last minutes; even "concurrent" collectors like HotSpot's CMS must occasionally stop everything.
- **Virtualization.** A VM can be suspended (memory saved to disk) and resumed at any point, e.g., for live migration; pause length tracks how fast processes dirty memory. Time stolen by co-resident VMs is *steal time*.
- **End-user devices.** A laptop lid closes; execution stops indefinitely.
- **Scheduling.** OS context switches and hypervisor switches preempt threads arbitrarily; under heavy load the wait to run again can be long.
- **Slow I/O.** Synchronous disk waits — sometimes triggered invisibly, like Java's classloader lazily loading a class mid-execution; network filesystems (EBS-style) add network jitter to disk latency; GC and I/O delays can compound.
- **Paging.** A memory access can page-fault to disk; under memory pressure the OS may *thrash*, doing little but swapping — servers often disable paging entirely, preferring to kill a process.
- **Signals.** SIGSTOP (Ctrl-Z) halts a process until SIGCONT — possibly sent by accident.

The situation mirrors single-machine thread-safety: assume nothing about timing. But the single-machine toolkit (mutexes, semaphores, atomic counters) does not carry over — there is no shared memory, only messages over an unreliable network. A paused node's peers may declare it dead; it wakes without noticing it slept.

## Trade-offs & Pitfalls
**Response-time guarantees** are possible: hard real-time systems (aircraft, airbags, robots) use RTOS scheduling with guaranteed CPU slices, libraries documenting worst-case execution, restricted or forbidden dynamic allocation, and exhaustive testing. This is enormously expensive, restricts tooling, and lowers throughput — real-time is not high-performance — so server-side systems rightly skip it and must live with pauses. **Mitigations short of real-time:** treat imminent GC like a planned brief outage — warn the app, drain requests off the node, collect, resume (some trading systems do this); or use GC only for short-lived objects and restart processes periodically before long-lived garbage accumulates, rolling-upgrade style. These reduce, never eliminate, pauses.

## Examples & Systems
Minutes-long JVM stop-the-world pauses; HotSpot CMS; live VM migration; Amazon EBS latency; airbag controllers as hard real-time; financial-trading GC choreography.

## Related
- up: [[Unreliable Clocks]] · chapter: [[Ch 08 - The Trouble with Distributed Systems]]
- [[The Truth Is Defined by the Majority]] — the zombie-leader consequence of pauses
- [[Fencing Tokens]] — the defense against stale lease holders
- [[Leader Election]] — leases as the leadership mechanism at risk
- [[Synchronous Versus Asynchronous Networks]] — same static-allocation trade-off for CPU time
