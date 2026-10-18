---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 9
chapter_title: The Trouble with Distributed Systems
topic: Unreliable Clocks
type: subtopic
tags: [ddia2, process-pause, lease, garbage-collection, steal-time, real-time]
sources:
  - raw/ch09.md
---
# Process Pauses
> A thread can stop for 15 seconds in the middle of a function and never know it. Everything a node believes about its own liveness is provisional.

## The Idea
A database with a single leader per shard: **only the leader may accept writes. How does a node know it is still leader and may safely accept writes?**

**One option is a lease** — a lock with a timeout. **Only one node can hold the lease at a time**, so on obtaining it a node knows it is leader **for a certain amount of time, until the lease expires.** **To remain leader it must periodically renew before expiry**; if it fails, it stops renewing and another node takes over.

The obvious request-handling loop:

```java
while (true) {
  request = getIncomingRequest();
  // Ensure that the lease always has at least 10 seconds remaining
  if (lease.expiryTimeMillis - System.currentTimeMillis() < 10000) {
    lease = lease.renew();
  }
  if (lease.isValid()) {
    process(request);
  }
}
```

**Two things are wrong with this code.** **First, it relies on synchronized clocks**: the lease's expiry time is set by a different machine but compared against the local system clock — **if the clocks are out of sync by more than a few seconds, the code starts doing strange things.**

**Second — and this survives even if you switch to the local monotonic clock — it assumes very little time passes between checking the time and processing the request.** Normally the code runs quickly and the 10-second buffer is ample. **But what if an unexpected pause occurs?** If the thread stops for 15 seconds around `lease.isValid`, **the lease will likely have expired by the time the request is processed and another node will already have taken over.** **Nothing tells this thread it was paused, so it won't notice until the next loop iteration — by which time it may already have done something unsafe.**

## How It Works
**Is it reasonable to assume a thread might pause that long? Unfortunately, yes.** Eight reasons:
- **Contention among threads accessing a shared resource** such as a lock or queue can make threads spend a lot of time waiting. **Often worse on machines with more CPU cores, and difficult to diagnose.**
- **Garbage collection.** Many runtimes occasionally **stop all running threads**; in the past such stop-the-world pauses **sometimes lasted several minutes.** With modern algorithms this is less of a problem, **but GC pauses can still be noticeable.**
- **VM suspension.** A VM can be **suspended and resumed at any point in a process's execution, for an arbitrary length of time** — used for **live migration** between hosts without a reboot, where the pause length depends on how fast processes write to memory.
- **End-user devices.** Laptops and phones may be **suspended and resumed arbitrarily** — when the user closes the lid.
- **Context switching.** When the OS switches to another thread, or the hypervisor to another VM, **the running thread can be paused at any arbitrary point.** For a VM, **CPU time spent in other VMs is steal time.** Under heavy load, **a long queue of waiting threads means it may take some time before the paused thread runs again.**
- **Synchronous disk access.** A thread may be **paused waiting for a slow disk I/O operation.** **In many languages disk access can happen surprisingly** — **the Java classloader lazily loads class files when first used, which could happen at any time.** **I/O pauses and GC pauses may even conspire to combine their delays**, and if the disk is a network filesystem or network block device such as Amazon EBS, **I/O latency is further subject to network delay variability.**
- **Paging.** If the OS allows swapping, **a simple memory access may cause a page fault requiring a disk load**, pausing the thread; under memory pressure this may require swapping another page out. **In extreme circumstances the OS spends most of its time swapping and gets little actual work done — thrashing.** **Paging is often disabled on server machines** if you'd rather kill a process than risk it.
- **`SIGSTOP`.** A Unix process can be paused by this signal — **pressing Ctrl-Z in a shell** — stopping it from getting CPU cycles until resumed with `SIGCONT`. **Even if your environment doesn't normally use `SIGSTOP`, it might be sent accidentally by an operations engineer.**

**All of these can preempt the running thread at any point and resume it later without the thread noticing.** The problem resembles making multithreaded code thread-safe: **you can't assume anything about timing, because arbitrary context switches and parallelism may occur.** **But the single-machine tools — mutexes, semaphores, atomic counters, lock-free structures, blocking queues — don't translate to distributed systems, because there is no shared memory, only messages over an unreliable network.**

**A node must assume its execution can be paused for a significant time at any point, even mid-function. During the pause the rest of the world keeps moving and may declare it dead. Eventually it continues, without even noticing it was asleep until it checks its clock later.**

## Trade-offs & Pitfalls
**Providing response time guarantees.** These pause reasons **can be eliminated if you try hard enough.** Software controlling **aircraft, rockets, robots, and cars** must respond quickly and predictably to sensor inputs; in these **hard real-time systems the software must respond by a specified deadline, and missing it may fail the entire system.** (*In embedded systems, **real-time** means carefully designed and tested to meet timing guarantees in all circumstances — in contrast to the vaguer web usage describing servers pushing data to clients.*) **You wouldn't want your airbag's release delayed by an inopportune GC pause.**

**Real-time guarantees require support at all levels**: a **real-time operating system (RTOS)** guaranteeing CPU allocation in specified intervals; **library functions documenting worst-case execution times**; **dynamic memory allocation restricted or disallowed** (real-time garbage collectors exist, but the application must not give the collector too much work); and **an enormous amount of testing and measurement.** **All this severely restricts the languages, libraries, and tools available, so developing real-time systems is very expensive** and mostly confined to safety-critical embedded devices. **And "real-time" is not "high-performance" — real-time systems may have *lower* throughput, since they prioritise timely responses above all else.** **For most server-side data processing systems, real-time guarantees are simply not economical or appropriate** — so these systems **must suffer the pauses and clock instability of a non-real-time environment.**

**Limiting the impact of garbage collection.** **GC used to be one of the biggest reasons for pauses, but GC algorithms have improved a lot** — **a properly tuned collector now usually pauses for no more than a few milliseconds.** Java offers **CMS, G1, ZGC, Epsilon, and Shenandoah**, each optimized for different memory profiles; **Go offers a simpler concurrent mark-and-sweep collector that attempts to optimize itself.**

**To avoid GC pauses entirely, use a language without a garbage collector**: **Swift uses automatic reference counting**, while **Rust and Mojo track object lifetimes via the type system** so the compiler determines how long memory must be allocated.

**Or mitigate within a GC language**: **pool and reuse objects rather than discarding them**, or **allocate data off-heap**. **A more extreme approach is to treat GC pauses like brief planned outages** — let other nodes handle requests while one collects. **If the runtime can warn the application that a pause is coming, the application can stop accepting new requests, drain outstanding ones, and then collect with nothing in flight** — **hiding GC pauses from clients and reducing high response-time percentiles.** **A variant: use the collector only for short-lived objects and restart processes periodically**, one node at a time with traffic shifted away, before enough long-lived objects accumulate to need a full collection.

## Examples & Systems
CMS, G1, ZGC, Epsilon, Shenandoah (Java); Go's concurrent mark-and-sweep; Swift ARC, Rust and Mojo lifetimes; `SIGSTOP`/`SIGCONT`; Amazon EBS as a network block device.

## Since the 1st Edition
The lease-renewal bug, the eight pause causes, and the real-time discussion carry over from the 1st edition's [[Process Pauses]]. **Substantially updated:** the garbage-collection material — **ZGC, Epsilon, and Shenandoah** are named alongside CMS and G1, **Go's collector** is contrasted, and **Swift, Rust, and Mojo** appear as non-GC alternatives. The 1st edition's GC discussion predated most of these.

## Related
- up: [[Unreliable Clocks (2e)]] · chapter: [[Ch 09 - The Trouble with Distributed Systems (2e)]]
- [[Distributed Locks and Leases (2e)]] — the fencing-token fix for exactly this bug
- [[Timeouts and Unbounded Delays (2e)]] — the same problem outside the process
- [[Latency and Response Time (2e)]] — GC pauses as a source of response-time variability
- 1st edition: [[Process Pauses]] — the same subtopic
