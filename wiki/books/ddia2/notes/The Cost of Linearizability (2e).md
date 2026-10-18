---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 10
chapter_title: Consistency and Consensus
topic: Linearizability
type: subtopic
tags: [ddia2, cap-theorem, pacelc, latency, memory-barrier, attiya-welch]
sources:
  - raw/ch10.md
---
# The Cost of Linearizability
> CAP is of mostly historical interest. The real cost of linearizability isn't fault tolerance — it's latency, all the time, even when nothing is broken.

## The Idea
**Multi-leader replication is often a good choice for multi-region deployment.** Consider a **network partition** between two regions: **the network within each region works and clients can reach their local region, but the regions cannot connect to each other.**

**With a multi-leader database, each region continues operating normally** — writes are asynchronously replicated, so they **queue up and are exchanged when connectivity is restored.**

**With single-leader replication, the leader must be in one region, and all writes and linearizable reads must go to it.** **So clients connected to a follower region cannot make any writes or linearizable reads during the interruption.** They can still read from the follower, **but the results might be stale.** **If the application requires linearizable reads and writes, the interruption causes the application to become unavailable in the regions that cannot reach the leader.**

## How It Works
> **The unhelpful CAP theorem.** CAP is sometimes presented as **consistency, availability, partition tolerance: pick two out of three.** **Putting it this way is misleading.** **Network partitions are a kind of fault — they aren't something you choose but will happen whether you like it or not.** **The only way to guarantee no partitions is to have no network — that is, only one replica — but then you don't have high availability either.**
>
> **When the network is working correctly, a system can provide both consistency (linearizability) and availability. When a network fault occurs, you have to choose between them.** **So a better phrasing would be: either consistent or available when partitioned.** **A more reliable network makes this choice less often, but at some point the choice is inevitable.**
>
> **The CP/AP classification has other flaws.** **Consistency is formalized as linearizability** (the theorem says nothing about weaker models), and **the formalization of availability does not match the usual meaning of the term.** **Many highly available (fault-tolerant) systems do not meet CAP's idiosyncratic definition of availability.** All in all, **there is a lot of misunderstanding around CAP, and it has little practical value for designing systems.**

**Generalizations exist.** **PACELC** observes that designers **might also weaken consistency when the network is working fine, in order to reduce latency**: **during a partition (P) choose between availability (A) and consistency (C); else (E), when there is no partition, choose between low latency (L) and consistency (C).** **But this definition inherits several of CAP's problems**, including the counterintuitive definitions of consistency and availability.

**There are many more interesting impossibility results in distributed systems, and CAP has now been superseded by more precise results, so it is of mostly historical interest today.**

## Trade-offs & Pitfalls
**The deeper point: linearizability's real cost is latency, not fault tolerance.**

**Many distributed databases that choose not to provide linearizability do so primarily to increase performance, not so much for fault tolerance.** And the clinching example is not distributed at all: **even RAM on a modern multi-core CPU is not linearizable.** **If a thread on one core writes to a memory address and a thread on another core reads it shortly afterward, it is not guaranteed to read the value written** — unless a **memory barrier or fence** is used.

**Why?** **Every core has its own memory cache and store buffer.** **Reads are served from the cache by default and changes are asynchronously written to main memory.** Since cache access is much faster than main memory, **this is essential for good performance** — **but it means there are now multiple copies of the data, asynchronously updated, so linearizability is lost.**

**It makes no sense to use CAP to justify the multi-core memory consistency model.** **Within one computer we assume reliable communication, and we don't expect one core to keep operating if disconnected from the rest.** **The reason for dropping linearizability here is performance, not fault tolerance** — **and the same is true of many distributed databases.** **Linearizable systems tend to be higher latency, and this is true all the time, not only during a network fault.**

**Can't we find a more efficient implementation? It seems the answer is no.** **Attiya and Welch prove that if you want linearizability, the response time of read and write requests is at least proportional to the uncertainty of delays in the network.** **In a network with highly variable delays, like most computer networks, the response time of linearizable reads and writes is inevitably going to be high.** **A faster algorithm for linearizability does not exist** — **but weaker consistency models can be much faster, so this trade-off is important for latency-sensitive systems.**

## Examples & Systems
Multi-region multi-leader versus single-leader under partition; multi-core CPU caches and memory barriers as the non-distributed counterexample.

## Since the 1st Edition
The 1st edition's [[The Cost of Linearizability]] made the same argument, including the unhelpful-CAP box, the multi-core RAM example, and the Attiya-Welch result. **Sharpened:** the 1st edition said CAP is misleading and better stated as "consistent or available when partitioned"; **the 2nd edition goes further, saying CAP has been superseded by more precise results and is of mostly historical interest today**, and adds **PACELC** — with the same criticism applied to it.

## Related
- up: [[Linearizability (2e)]] · chapter: [[Ch 10 - Consistency and Consensus (2e)]]
- [[Geographically Distributed Operation (2e)]] — the multi-region choice this analyses
- [[Timeouts and Unbounded Delays (2e)]] — the network delay uncertainty that bounds performance
- [[Aiming for Correctness (2e)]] — approaches to avoiding linearizability without sacrificing correctness
- 1st edition: [[The Cost of Linearizability]] — the same subtopic
