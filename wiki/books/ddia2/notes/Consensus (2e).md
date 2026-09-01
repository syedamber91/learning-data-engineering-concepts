---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 10
chapter_title: Consistency and Consensus
type: topic
tags: [ddia2, consensus, paxos, raft, zab, flp, byzantine]
sources:
  - raw/ch10.md
---
# Consensus
The chapter has accumulated several things that are **easy on a single node but a lot harder with fault tolerance:**
- **A database can be linearizable with a single leader and all reads and writes on it** — **but how do you fail over if that leader fails, while avoiding split brain? How do you ensure a node believing itself leader hasn't been voted out while temporarily paused?**
- **A linearizable ID generator on a single node is just a counter with an atomic fetch-and-add — what if it crashes?**
- **An atomic CAS decides who gets a lock or lease, or ensures uniqueness of a name. On a single node CAS may be one CPU instruction — how do you make it fault-tolerant?**

**All of these are instances of the same fundamental problem: consensus.** **The standard formulation involves getting multiple nodes to agree on a single value.** It is **one of the most important and fundamental problems in distributed computing**, and **infamously difficult to get right — many systems have gotten it wrong in the past.**

**The best-known consensus algorithms are Viewstamped Replication, Paxos, Raft, and Zab.** They have quite a few similarities but are not the same. **They all work in a non-Byzantine system model**: network communication may be arbitrarily delayed or dropped, and nodes may crash, restart, and become disconnected, **but the algorithms assume nodes otherwise follow the protocol correctly and do not behave maliciously.**

**There are also consensus algorithms tolerating some Byzantine nodes** — **a common assumption is that fewer than one-third of nodes are Byzantine-faulty** — **used in blockchains, for example.** But Byzantine fault-tolerant algorithms are beyond this book's scope.

> **The impossibility of consensus.** You may have heard of the **FLP result** — Fischer, Lynch, Paterson — **proving no algorithm is always able to reach consensus if there is a risk that a node may crash.** In a distributed system we must assume nodes may crash, **so reliable consensus is impossible. Yet here we are, discussing algorithms for achieving consensus. What's going on?**
>
> **First, FLP doesn't say we can never reach consensus; it says we can't guarantee a consensus algorithm will always terminate.** **Moreover, FLP is proved assuming a deterministic algorithm in the asynchronous system model** — the algorithm **cannot use any clocks or timeouts.** **If it can use timeouts to suspect a node may have crashed (even if the suspicion is sometimes wrong), consensus becomes solvable.** **Even allowing random numbers is sufficient.** **So although FLP is of great theoretical importance, distributed systems can usually achieve consensus in practice.**

## Subtopics
- [[The Many Faces of Consensus (2e)]] — five formulations, all equivalent.
- [[Consensus in Practice (2e)]] — epochs, two rounds of voting, and the costs.
- [[Coordination Services (2e)]] — the systems built specifically to sell you consensus.

## Key Takeaways
- **Consensus unifies the whole chapter.** Leader election, linearizable ID generation, fault-tolerant CAS, and atomic commitment are not four problems but one.
- **The four properties of consensus** — uniform agreement, integrity, validity, termination — separate cleanly into **three safety properties and one liveness property (termination)**, which is why a large-scale outage can stop a consensus system from processing requests **but cannot corrupt it into making inconsistent decisions.**
- **Any consensus algorithm requires at least a majority of nodes functioning correctly to assure termination**, and that majority forms a quorum.

## Since the 1st Edition
The 1st edition's [[Fault-Tolerant Consensus]] material covered the same four algorithms, the same four properties, and the same FLP box. **The structural change is scope**: the 1st edition's consensus topic also contained **atomic commit and two-phase commit**, which have moved to [[Ch 08 - Transactions (2e)]] — leaving this topic free to concentrate on the equivalence result and the practical algorithms. **Added:** the note that **Byzantine-tolerant consensus assumes fewer than one-third faulty nodes** and is used in blockchains.

## Related
- chapter: [[Ch 10 - Consistency and Consensus (2e)]]
- [[Linearizable ID Generators (2e)]] — the argument that demands consensus
- [[Two-Phase Commit (2e)]] — atomic commitment, now in the transactions chapter
- 1st edition: [[Fault-Tolerant Consensus]] — the closest predecessor
