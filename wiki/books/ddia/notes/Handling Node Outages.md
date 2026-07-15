---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 5
chapter_title: Replication
topic: Leaders and Followers
type: subtopic
tags: [ddia, failover, split-brain, fault-tolerance]
sources:
  - raw/ch05.md
---
# Handling Node Outages

> Follower crashes are healed by simple log replay, but leader failure triggers failover — a process riddled with data loss, split brain, and timeout dilemmas.

## The Idea

Nodes go down constantly — unplanned faults, but just as often planned maintenance like kernel patches. The goal is to keep the whole system serving traffic while individual machines reboot. Follower and leader failures demand very different treatment.

## How It Works

**Follower failure — catch-up recovery.** Each follower keeps its own local log of changes received from the leader. After a crash or a network blip, it knows the last transaction it processed, reconnects, requests everything since that point, applies it, and rejoins the stream. Cheap and safe.

**Leader failure — failover**, which requires three steps:
1. *Detect the failure.* There is no reliable way to distinguish crash from slowness, so systems use timeouts — no response for, say, 30 seconds means presumed dead.
2. *Choose a new leader*, via an election among replicas or appointment by a controller node. The best candidate is the replica with the freshest data. This is fundamentally a [[Consensus]] / [[Leader Election]] problem (Chapter 9).
3. *Reconfigure* clients to send writes to the new leader — see [[Request Routing]] — and force the old leader, if it returns, to recognize it has been demoted.

## Trade-offs & Pitfalls

Failover is a minefield:

- **Lost writes**: with async replication the new leader may lack the old leader's latest writes; when the old leader rejoins, the usual fix is to discard its unreplicated writes — violating clients' durability expectations.
- **External coordination hazards**: GitHub once promoted a lagging MySQL follower whose autoincrement counter was behind; it reissued primary keys already used, and because those keys also indexed a Redis store, private data leaked to the wrong users.
- **[[Split Brain]]**: two nodes simultaneously believe they are leader; if both accept writes with no conflict resolution, data is corrupted. Safety mechanisms that shoot one node down (fencing/STONITH — see [[Fencing Tokens]]) can misfire and kill both.
- **Timeout tuning**: too long delays recovery; too short triggers needless failovers under load spikes or network glitches — exactly when an extra failover hurts most.

These hazards are why some operations teams prefer manual failover even when automation exists.

## Examples & Systems

- GitHub's MySQL/Redis primary-key incident (2012).
- PostgreSQL, MySQL, MongoDB all implement variants of this failover choreography.

## Related

- up: [[Leaders and Followers]] · chapter: [[Ch 05 - Replication]]
- [[Synchronous Versus Asynchronous Replication]] — async lag is why failover loses writes
- [[Detecting Faults]] — the timeout problem in depth
- [[The Truth Is Defined by the Majority]] — why a quorum decides leadership
- [[Fault-Tolerant Consensus]] — the rigorous solution to electing a leader
