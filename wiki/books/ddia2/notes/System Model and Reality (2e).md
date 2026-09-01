---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 9
chapter_title: The Trouble with Distributed Systems
topic: Knowledge, Truth, and Lies
type: subtopic
tags: [ddia2, system-model, partially-synchronous, crash-recovery, safety, liveness, fail-slow]
sources:
  - raw/ch09.md
---
# System Model and Reality
> An algorithm is correct *in a system model*. State the model, prove the properties, and then remember that reality is a simplified abstraction's worst enemy.

## The Idea
**Algorithms must not depend too heavily on the details of the hardware and software they run on**, which requires **formalizing the kinds of faults we expect.** We do this by defining a **system model** — an abstraction describing an algorithm's assumptions.

## How It Works
**Three timing models are in common use:**
- **Synchronous model** — assumes **bounded network delay, bounded process pauses, and bounded clock error.** This doesn't imply exactly synchronized clocks or zero delay, just that **they never exceed a fixed upper bound.** **Not a realistic model of most practical systems**, because unbounded delays and pauses do occur.
- **Partially synchronous model** — the system **behaves synchronously most of the time but sometimes exceeds the bounds.** **A realistic model of many systems**: most of the time networks and processes are quite well behaved — otherwise we'd never get anything done — **but any timing assumptions may be shattered occasionally, and when that happens delay, pauses, and clock error may become arbitrarily large.**
- **Asynchronous model** — the algorithm **may make no timing assumptions at all; it doesn't even have a clock, so it cannot use timeouts.** Some algorithms can be designed for it, **but it is very restrictive.**

**Four node-failure models:**
- **Crash-stop (fail-stop) faults** — a node **can fail only by crashing**: it suddenly stops responding at any moment **and thereafter is gone forever; it never comes back.**
- **Crash-recovery faults** — nodes may crash at any moment **and perhaps start responding again after an unknown time.** Nodes are assumed to have **stable storage preserved across crashes, while in-memory state is lost.**
- **Degraded performance and partial functionality** — nodes may **slow down**, still responding to health checks while **too slow to get any real work done.** A Gigabit interface may **drop to 1 Kb/s because of a driver bug**; a process under memory pressure may **spend most of its time in garbage collection**; **worn-out SSDs can have erratic performance**; and hardware is affected by **high temperature, loose connectors, mechanical vibration, power supply problems, and firmware bugs.** **This is a limping node, gray failure, or fail-slow, and it can be even more difficult to deal with than a cleanly failed node.** A related problem: **a process stops doing some of the things it should while other aspects continue working** — a crashed or deadlocked background thread.
- **Byzantine (arbitrary) faults** — nodes may do absolutely anything, including trying to deceive others.

**For modeling real systems, the partially synchronous model with crash-recovery faults is generally the most useful.** It allows unbounded network delay, process pauses, and slow nodes.

**Defining correctness.** We define an algorithm's correctness by describing its **properties**. For **fencing tokens**, we might require:
- **Uniqueness** — no two requests return the same token value.
- **Monotonic sequence** — if request *x* returned token *t<sub>x</sub>*, request *y* returned *t<sub>y</sub>*, and *x* completed before *y* began, then *t<sub>x</sub>* < *t<sub>y</sub>*.
- **Availability** — a node that requests a token and does not crash eventually receives a response.

**An algorithm is correct in a system model if it always satisfies its properties in all situations that model assumes may occur.** **But if all nodes crash, or all network delays become infinite, no algorithm can get anything done. How do we still make useful guarantees?**

**Safety versus liveness.** Uniqueness and monotonic sequence are **safety** properties; availability is a **liveness** property. **A giveaway is that liveness properties often include the word "eventually"** — and yes, **eventual consistency is a liveness property.**

**Informally, safety is "nothing bad happens" and liveness "something good eventually happens" — but it's best not to read too much into those, because "good" and "bad" are value judgments that don't apply well to algorithms.** The precise definitions:
- **If a safety property is violated, we can point to the particular point in time it was broken** — the operation in which a duplicate token was returned. **After a safety property has been violated, the violation cannot be undone; the damage is already done.**
- **A liveness property works the other way**: it may not hold at a given moment — a node has sent a request but not yet received a response — **but there is always hope it may be satisfied in the future.**

**The advantage of the distinction is that it helps with difficult system models.** **For distributed algorithms it is common to require that safety properties always hold, in all possible situations** — **even if all nodes crash or the entire network fails, the algorithm must not return a wrong result.** **With liveness properties we are allowed caveats**: a request needs a response **only if a majority of nodes have not crashed and the network eventually recovers.** **The partially synchronous model's definition requires exactly that: any period of network interruption lasts only a finite duration and is then repaired.**

## Trade-offs & Pitfalls
**Mapping system models to the real world.** **When implementing an algorithm in practice, the messy facts of reality come back to bite you, and it becomes clear the system model is a simplified abstraction.**

**Crash-recovery algorithms generally assume data in stable storage survives crashes. But what if the data on disk is corrupted or wiped out by hardware error or misconfiguration? What if a server has a firmware bug and fails to recognize its hard drives on reboot even though they are correctly attached?** **Quorum algorithms rely on a node remembering the data it claims to have stored — if a node suffers amnesia, that breaks the quorum condition and the correctness of the algorithm.** **Perhaps a new model is needed in which stable storage mostly survives but may sometimes be lost — but that model becomes harder to reason about.**

**The theoretical description can declare that certain things are simply assumed not to happen**, and in non-Byzantine systems we do have to make such assumptions. **However, a real implementation may still have to include code to handle the case of something happening that was assumed impossible — even if that handling boils down to `printf("Sucks to be you"); exit(666);`**, letting a human operator clean up the mess. **(This is one difference between computer science and software engineering.)**

**That is not to say abstract system models are worthless — quite the opposite. They are incredibly helpful for distilling the complexity of real systems down to a manageable set of faults we can reason about**, so we can understand the problem and try to solve it systematically.

## Examples & Systems
The fencing-token properties as the worked correctness example; the 1 Kb/s Gigabit interface as the canonical fail-slow fault.

## Since the 1st Edition
Close to the 1st edition's [[System Model and Reality]] — the same three timing models, the same safety/liveness distinction with the same fencing-token properties, and the same `printf("Sucks to be you")` line. **Added:** **degraded performance and partial functionality as a fourth node-failure model**, named as **limping node / gray failure / fail-slow**, with concrete causes. The 1st edition listed only crash-stop, crash-recovery, and Byzantine.

## Related
- up: [[Knowledge, Truth, and Lies (2e)]] · chapter: [[Ch 09 - The Trouble with Distributed Systems (2e)]]
- [[Formal Methods and Randomized Testing (2e)]] — checking that properties actually hold
- [[Single-Leader Versus Leaderless Replication Performance (2e)]] — gray failures from the replication side
- [[Byzantine Faults (2e)]] — the fourth node-failure model
- 1st edition: [[System Model and Reality]] — the same subtopic
