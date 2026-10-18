---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 10
chapter_title: Consistency and Consensus
topic: Consensus
type: subtopic
tags: [ddia2, total-order-broadcast, shared-log, cas, fetch-and-add, consensus-number]
sources:
  - raw/ch10.md
---
# The Many Faces of Consensus
> Single-value consensus, compare-and-set, shared logs, fetch-and-add, and atomic commitment look completely different. They are the same problem.

## The Idea
Consensus can be expressed in several ways:
- **Single-value consensus** is very similar to an **atomic CAS**, and can implement locks, leases, and uniqueness constraints.
- **Constructing an append-only log** also requires consensus, **usually formalized as total order broadcast.** With a log you can implement **state machine replication, leader-based replication, event sourcing**, and other patterns.
- **An atomic fetch-and-add** turns out to be equivalent to consensus.
- **Atomic commitment** of a multidatabase or multishard transaction requires all participants to agree whether to commit or abort.

**In fact these problems are all equivalent. If you have an algorithm solving one, you can convert it into a solution for any of the others.** **This is quite a profound and perhaps surprising insight — and it's why we can lump all these together under "consensus" even though they look quite different on the surface.**

## How It Works
**Single-value consensus.** One or more nodes propose values and the algorithm decides on one. Four properties:
- **Uniform agreement** — no two nodes decide differently.
- **Integrity** — after deciding, a node cannot change its mind.
- **Validity** — if a node decides value *v*, then *v* was proposed by a node.
- **Termination** — every node that does not crash eventually decides.

**Agreement and integrity define the core idea**: everyone decides the same outcome and cannot change their mind. **Validity rules out trivial solutions** — an algorithm always deciding null would satisfy agreement and integrity but not validity. **If you don't care about fault tolerance, the first three are easy: hardcode one node as "dictator."** **All the difficulty arises from the need for fault tolerance**, which **termination formalizes** — the algorithm must make progress, and **must decide even if a crashed node disappears and never comes back.** (The book's memorable framing: **imagine an earthquake buries your node under 30 feet of mud.**)

**Any consensus algorithm requires at least a majority of nodes functioning correctly to assure termination**, and that majority forms a quorum. **So termination assumes fewer than half the nodes are unreachable — but most algorithms ensure the safety properties always hold, even if a majority fail or a severe network problem occurs.** **A large-scale outage can stop the system processing requests, but cannot corrupt it into making inconsistent decisions.**

**Compare-and-set as consensus.** **With a fault-tolerant linearizable CAS, consensus is easy**: set the object to null, have each node CAS with expected value null and its own proposal as the new value; **the decided value is whatever the object ends up set to.** **Conversely, with consensus you can implement CAS**: propose the new values via consensus and set the object to whatever was decided. **So CAS and consensus are equivalent** — **both straightforward on a single node, challenging to make fault-tolerant.** (The object-store **conditional writes** from Chapter 6 are CAS in a distributed setting.)

**Shared logs as consensus.** **A shared log is one where multiple nodes can request that entries be appended** — single-leader replication is an example. Formally it supports adding a value and reading entries, satisfying:
- **Eventual append** — if a non-crashing node requests a value be added, it must eventually read that value in a log entry.
- **Reliable delivery** — no entries are lost; if one node reads an entry, eventually every non-crashing node reads it.
- **Append-only** — after a node reads an entry it is immutable, and new entries can be added only after it, not before; **rereading gives the same entries in the same order, even across crashes.**
- **Agreement** — if two nodes both read entry *e*, **prior to *e* they must have read exactly the same sequence of entries in the same order.**
- **Validity** — if a node reads an entry containing a value, a node previously requested that value's addition.

> **A shared log can be implemented using a total order broadcast protocol**, also known as **atomic broadcast** or **total order multicast**: to add a value you "broadcast" it, and when the protocol "delivers" it, it becomes a log entry.

**With a shared log, consensus is easy**: everyone requests their value be added, and **whichever value is read back in the first log entry is the decision** — all nodes read entries in the same order, so they agree. **Conversely, with consensus you can build a shared log**: run a separate consensus instance per log slot; a node proposes its value for an undecided slot; when a slot is decided and all previous slots are decided, the value is appended; **if a proposal wasn't chosen for a slot, the node retries with a later slot.**

**So consensus is equivalent to total order broadcast and shared logs.** **Single-leader replication without failover does not meet the liveness requirements**, since it stops delivering if the leader crashes — **as usual, the challenge is performing failover safely and automatically.**

**Fetch-and-add as consensus — almost.** **With CAS, fetch-and-add is easy**: read, then CAS with expected = the read value and new = value + 1, retrying on failure. **Less efficient under contention than a native fetch-and-add, but functionally equivalent.**

**Conversely?** Initialize the counter to 0 and have every proposer fetch-and-add. **One node reads 0 and is the winner; all others read an incremented value.** **That works for the winner — but the other nodes know they are not the winner and don't know who is.** **The winner could tell them — but what if it crashes before doing so? The others are left hanging, unable to decide, so consensus does not terminate. And they can't fall back to another node, because the node that read 0 may yet come back and rightly decide its own value.**

**The exception: if no more than two nodes will propose.** Then they exchange their proposals and each performs fetch-and-add: **the node reading 0 decides its own value, the node reading 1 decides the other's.** **So fetch-and-add has a consensus number of 2. CAS and shared logs solve consensus for any number of proposers — a consensus number of ∞.**

**Atomic commitment as consensus.** They seem similar, **but there is one important difference: with consensus it's OK to decide any value that was proposed, whereas with atomic commitment the algorithm must abort if any participant voted to abort.** Its properties add **validity** (if a node commits, all must have voted commit; if any voted abort, all must abort) and **nontriviality** (if all vote commit and no communication timeouts occur, all must commit — **which allows an abort if communication times out, while preventing an algorithm that always aborts**).

**With consensus you can solve atomic commitment**: every node sends its vote to every other; **nodes that received commit votes from everyone propose "commit" via consensus; nodes that received an abort vote or timed out propose "abort."** **"Commit" is proposed only if all voted commit** — and if some nodes propose abort while others propose commit because of a timeout, **it doesn't matter which is decided, as long as they all do the same thing.** **Conversely, with a fault-tolerant atomic commitment protocol you can solve consensus** by starting a transaction on a quorum performing single-node CAS. **So atomic commit and consensus are equivalent too.**

## Trade-offs & Pitfalls
- **The consensus number is the useful practical takeaway**: it tells you which primitives your infrastructure actually gives you. **A fetch-and-add counter is not a general-purpose coordination primitive; a CAS is.**
- **The equivalences are constructive but not efficient.** Converting between formulations proves theoretical equivalence — **the reason most systems provide shared logs is a practical choice, not a mathematical one.**

## Examples & Systems
Object-store conditional writes as distributed CAS; single-leader replication as an incomplete shared log.

## Since the 1st Edition
The 1st edition covered total order broadcast and its equivalence to consensus in [[Ordering Guarantees]], and covered single-value consensus properties in [[Fault-Tolerant Consensus]] — **but treated them as separate discussions in separate topics.** **The 2nd edition unifies them into one subtopic organised explicitly around equivalence**, adds **fetch-and-add** as a fourth formulation with the **consensus number** concept (2 versus ∞), and **relocates atomic commitment here as a fifth**, now that 2PC itself lives in the transactions chapter. The shared-log property list is also stated formally for the first time.

## Related
- up: [[Consensus (2e)]] · chapter: [[Ch 10 - Consistency and Consensus (2e)]]
- [[Consensus in Practice (2e)]] — which formulation systems actually implement
- [[Two-Phase Commit (2e)]] — the atomic commitment algorithm being compared
- [[Preventing Lost Updates (2e)]] — CAS in its single-node form
- 1st edition: [[Ordering Guarantees]] and [[Fault-Tolerant Consensus]] — the two topics this merges
