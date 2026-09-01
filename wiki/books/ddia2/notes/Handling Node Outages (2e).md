---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 6
chapter_title: Replication
topic: Single-Leader Replication
type: subtopic
tags: [ddia2, failover, split-brain, fencing, catch-up-recovery, github-incident]
sources:
  - raw/ch06.md
---
# Handling Node Outages
> Follower failure is easy. Leader failure is failover, and failover is where committed writes get discarded, two nodes both think they're leader, and a timeout that's slightly wrong makes an overloaded system worse.

## The Idea
Any node can go down — unexpectedly through a fault, or deliberately for planned maintenance such as rebooting to install a kernel security patch. **Being able to reboot individual nodes without downtime is a big advantage for operations**, so the goal is to keep the system running despite individual node failures and to keep the impact as small as possible.

## How It Works
**Follower failure: catch-up recovery.** Each follower keeps a local log of the changes it has received from the leader. If it crashes and restarts, or the network between it and the leader is temporarily interrupted, recovery is easy: **from its log it knows the last transaction processed before the fault**, so it connects to the leader, requests all changes from that point, applies them, and resumes the stream.

Conceptually simple, but **challenging in terms of performance**: with high write throughput or a long offline period there may be a lot to catch up on, putting **high load on both the recovering follower and the leader** while it happens. The leader can delete its log of writes once all followers confirm processing, but a long-unavailable follower forces a choice: **retain the log until it recovers** (risking running out of disk space on the leader) or **delete the unacknowledged log** (in which case the follower cannot recover from the log and must be restored from a backup).

**Leader failure: failover.** Trickier. A follower must be promoted, clients reconfigured to write to the new leader, and other followers switched to consuming from it. This can be manual or automatic; automatic failover usually has three steps:
1. **Determining that the leader has failed.** Crashes, power outages, network issues — **there is no foolproof way of detecting what happened**, so most systems simply use a **timeout**: nodes bounce messages back and forth, and a node that doesn't respond for some period — say 30 seconds — is assumed dead. (Planned maintenance doesn't need this, since the leader can trigger a safe handoff before shutting down.)
2. **Choosing a new leader.** Either an **election** among the remaining replicas or an appointment by a previously established **controller node**. The best candidate is usually **the replica with the most up-to-date changes from the old leader**, to minimise data loss. Getting all nodes to agree is a **consensus problem**.
3. **Reconfiguring the system.** Clients must send writes to the new leader. **If the old leader comes back, it might still believe it is the leader**, not realising the others forced it to step down — so the system must ensure it becomes a follower and recognises the new leader.

## Trade-offs & Pitfalls
**Failover is fraught with things that can go wrong:**
- **Lost writes with asynchronous replication.** The new leader may not have received all the old leader's writes. If the former leader rejoins after a new one is chosen, what happens to those writes? The new leader may have taken conflicting writes meanwhile. **The most common solution is to simply discard the old leader's unreplicated writes — meaning writes you believed committed weren't durable after all.**
- **Discarding writes is especially dangerous when other storage systems must stay coordinated with the database.** The book's worked incident: **at GitHub, an out-of-date MySQL follower was promoted to leader.** The database used an autoincrementing counter for primary keys, but the new leader's counter lagged the old one's, so **it reused primary keys previously assigned by the old leader**. Those primary keys were also used in a Redis store, so the reuse produced inconsistency between MySQL and Redis — **which disclosed some private data to the wrong users.**
- **Split brain.** In certain fault scenarios two nodes can both believe they are leader. If both accept writes and there is no conflict-resolution process, **data is likely to be lost or corrupted**. Some systems shut down one node if two leaders are detected, but **if that mechanism is not carefully designed you can end up with both nodes shut down** — and there is a risk that by the time split brain is detected and the old node stopped, **data has already been corrupted**. Guarding against split brain by limiting or shutting down old leaders is called **fencing**.
- **Choosing the timeout is genuinely hard.** A longer timeout means slower recovery when the leader really fails. Too short, and **unnecessary failovers occur**: a temporary load spike can push response times above the timeout, or a network glitch can delay packets. **If the system is already struggling with high load or network problems, an unnecessary failover is likely to make the situation worse, not better.**

**These problems have no easy solutions.** For this reason **some operations teams prefer to perform failovers manually, even when the software supports automatic failover.**

**The most important thing is to pick an up-to-date follower as the new leader.** With synchronous or semisynchronous replication, that is the follower the old leader waited for before acknowledging writes; with asynchronous replication, pick the follower with the **highest log sequence number**. **Losing a fraction of a second's worth of writes may be tolerable; picking a follower that is behind by several days could be catastrophic.**

## Examples & Systems
The GitHub MySQL/Redis primary-key-reuse incident; fencing as the split-brain countermeasure.

## Since the 1st Edition
Close to the 1st edition's [[Handling Node Outages]], including the GitHub incident, split brain, and the timeout dilemma. **Added:** the controller-node option alongside election for choosing a new leader; the note that planned maintenance allows a safe handoff and so bypasses failure detection; and the explicit closing guidance on **how** to pick the most up-to-date follower under each replication mode, which the 1st edition left implicit.

## Related
- up: [[Single-Leader Replication (2e)]] · chapter: [[Ch 06 - Replication (2e)]]
- [[Distributed Locks and Leases (2e)]] — where fencing is examined properly
- [[Consensus (2e)]] — the problem leader election actually is
- [[Synchronous Versus Asynchronous Replication (2e)]] — which writes survive a failover
- 1st edition: [[Handling Node Outages]] — the same subtopic
