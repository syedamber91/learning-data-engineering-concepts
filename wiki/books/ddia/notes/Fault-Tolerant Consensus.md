---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 9
chapter_title: Consistency and Consensus
topic: Distributed Transactions and Consensus
type: subtopic
tags: [ddia, consensus, raft, paxos, quorums]
sources:
  - raw/ch09.md
---
# Fault-Tolerant Consensus
> Real consensus algorithms (Paxos, Raft, Zab, VSR) guarantee agreement, integrity, and validity always — and termination whenever a majority survives — by electing leaders per epoch and requiring every decision to pass an overlapping quorum vote.

## The Idea
[[Consensus]]: one or more nodes propose values; the algorithm decides one. It settles races like the last airplane seat or duplicate username registrations. Formally, four properties must hold:
- **Uniform agreement** — no two nodes decide differently.
- **Integrity** — no node decides twice.
- **Validity** — the decided value was actually proposed by someone (rules out "always decide null").
- **Termination** — every non-crashed node eventually decides.

The first three are safety properties; termination is liveness — it forbids the algorithm from stalling forever, and is exactly what a dictatorial design (or 2PC with a dead coordinator) lacks. The model assumes crashed nodes never return (buried-in-mud semantics): any algorithm that must *wait* for a recovery cannot terminate, which is why [[Two-Phase Commit]] fails the bar.

## How It Works
**Majorities.** Termination provably requires a majority of nodes functioning — that majority forms a [[Quorum]]. Safety, though, is preserved by most implementations even if a majority fails: a big outage halts progress but never produces invalid decisions. Standard algorithms also assume no [[Byzantine Faults]] (tolerable only with fewer than one-third faulty nodes, via costlier protocols).

**Deciding sequences, not values.** Viewstamped Replication (VSR), Paxos, Raft, and Zab — similar but not identical — mostly skip the one-value formalism and decide a *sequence* of values, making them [[Total Order Broadcast]] algorithms: each message delivery is one consensus round, where agreement ⇒ same order everywhere, integrity ⇒ no duplicates, validity ⇒ no fabricated messages, termination ⇒ no losses. VSR, Raft, and Zab implement broadcast directly; Paxos's equivalent optimization is Multi-Paxos.

**Epochs break the circularity.** Consensus looks like single-leader replication — but electing a leader itself needs consensus. The escape: protocols guarantee a unique leader only *within an epoch* (ballot number in Paxos, view number in VSR, term number in Raft). Each suspected leader death triggers an election under an incremented, totally ordered epoch; between conflicting leaders, the higher epoch wins. Before deciding anything, a leader must confirm it hasn't been ousted — and per [[The Truth Is Defined by the Majority]], it can't trust its own judgment. So there are **two rounds of voting**: elect a leader, then vote on each of the leader's proposals. The key invariant is that the two quorums *overlap*: if a proposal vote succeeds, at least one voter also took part in the latest election, so an undisturbed proposal vote proves no higher epoch exists. Unlike 2PC, the leader is elected, only a *majority* (not all) must vote yes, and a defined recovery process restores consistency after elections — that trio is what buys fault tolerance. The FLP impossibility result (no deterministic consensus with crash risk) applies only in the fully asynchronous model without clocks or randomness; timeouts or random numbers make consensus solvable in practice.

## Trade-offs & Pitfalls
- Proposal voting is effectively synchronous replication — the durability/performance trade many databases decline ([[Synchronous Versus Asynchronous Replication]]).
- Strict majorities mean 3 nodes to survive 1 failure, 5 to survive 2; a partitioned minority blocks.
- Most algorithms assume static membership; dynamic reconfiguration is much less well understood.
- Timeout-based failure detection misfires on variable-latency networks, causing spurious elections; Raft can bounce leadership indefinitely across one flaky link. Robustness to bad networks remains open research.

## Examples & Systems
Raft (etcd), Zab ([[ZooKeeper]]), Multi-Paxos, Viewstamped Replication; Jepsen-style findings against homegrown election code.

## Related
- up: [[Distributed Transactions and Consensus]] · chapter: [[Ch 09 - Consistency and Consensus]]
- [[Total Order Broadcast]] — the form consensus takes in practice
- [[Atomic Commit and Two-Phase Commit (2PC)]] — the non-fault-tolerant cousin
- [[Handling Node Outages]] — the failover problem epochs solve safely
- [[System Model and Reality]] — where FLP's asynchronous model lives
- [[consensus]] (vutr wiki) — the systems-level "why Raft, why here" story (LinkedIn's Northguard, ZooKeeper's CP role) grounded in a data engineer's own posts; that topic explicitly points back here for the election-term/log-matching/quorum-commit mechanics its own sources don't cover
