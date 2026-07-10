---
persona: alex
kind: concept
sources:
- vutr/partition-reassignment-and-cluster-balancing
last_updated: '2026-07-10'
qc: passed
slug: 010-partition-reassignment-and-cluster-balancing
topics:
- kafka
learner: alex
source_note: partition-reassignment-and-cluster-balancing
mastery: mastered
---

*What Alex understood:* Wait, so I always pictured it like a supermarket adding a new checkout lane — the line just spreads out on its own. But Kafka isn't like that at all. The new lane stands there empty, because the partitions are physically glued to their old brokers' disks. Since compute and storage are stuck together, rebalancing means literally hauling data across the network, like moving apartments — not just updating an address in a directory.

The built-in way is: you write the moving plan yourself with a script (generate a plan, execute it, then verify it), and the human drives every step. And the scary default is it moves EVERYBODY — even partitions that were perfectly fine where they were. At PayPal's size, with peaks over a trillion messages a day, that default could knock a cluster out for days, so they changed it to only move the partitions that were actually in trouble (the under-replicated ones), and used the same trick to patch many clusters in parallel, one broker per cluster at a time.

Then there are three escapes. Cruise Control is like hiring a smart moving planner — it measures how loaded every broker is, builds a model, and picks proposals against goals. But the trucks are still slow, and it planned from a photo of the city; while the trucks are driving, the city changes, so the plan can be stale by the time it lands. That's why it only really works when traffic is calm.

AutoMQ cheats by making moving free: everyone's stuff already sits in one shared warehouse (object storage), so "moving" a partition is just editing the registry of who handles what. No trucks, so its AutoBalancer can rebalance continuously — every minute or so it snapshots the cluster, checks goals like "CPU at 50%, give or take 20%," where hard goals can never break and soft ones get dropped on conflict, and runs the highest-scoring fix.

Northguard doesn't move boxes at all — all NEW boxes (segments) just get assigned to the new broker, and since segments are created way more often than whole logs, the new guy fills up naturally.

## Follow-up questions

**Alex:** Cruise Control's big weakness was that it plans from a snapshot that goes stale while the slow data copy happens. But AutoMQ's Decision Scheduler ALSO acts on a snapshot of the ClusterModel taken on an interval — why doesn't AutoMQ's decision go stale in exactly the same way?

**vutr:** Great catch — the seam you found is exactly the right one. The staleness problem isn't caused by snapshotting itself; it's caused by how long execution takes after the snapshot. In Cruise Control's world, replicating partition data is slow, so by the time a decision executes, the cluster state it was based on may have changed significantly — that's what makes the decision less accurate. In AutoMQ's world, executing a reassignment moves no data: the controller just rewrites the broker↔partition mapping in KRaft-style metadata, so decisions execute quickly and accurately because nothing waits on replication. The window between the Decision Scheduler snapshotting the ClusterModel and the plan finishing is tiny, so the snapshot barely has time to go stale — and since the scheduler wakes again on its interval (e.g. every 60 seconds) and looks for goal-violating brokers, any imbalance that appears after one cycle is caught in the next.

**Alex:** Northguard adds a broker with zero movement by pointing the next active segment at it — but all the old segments still live on the old brokers. Doesn't the cluster stay unbalanced for reads of old data? Does old data ever get moved off a hot broker, or does it just age out?

**vutr:** (the wiki does not cover this — see open questions)
