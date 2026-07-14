---
persona: vutr
kind: concept
sources:
- raw/kafka/apache-kafka-consumer.md
- raw/kafka/if-youre-learning-kafka-this-article.md
last_updated: '2026-07-10'
qc: passed
slug: consumer-group-rebalancing
topics:
- kafka
---

Rebalancing is not a background optimization Kafka quietly performs — it is the process of moving partition ownership between consumers, and depending on which of the two types you get, it can mean a window where your entire consumer group processes nothing. It is triggered whenever the number of consumers in a group changes: a member is added, or a member crashes, and the remaining consumers must start consuming messages from partitions previously owned by someone else.

**How the group detects the change.** The machinery sits with the Group Coordinator — one of the brokers chosen for this responsibility, determined by the group ID (different groups land on different brokers). Consumers prove they are alive by sending heartbeats to the coordinator from a background thread. As long as heartbeats arrive at regular intervals, the coordinator assumes the consumer is alive. If they stop, the coordinator declares the consumer unavailable and triggers a rebalance. Two failure paths matter here, and they have different costs:

- **Crash:** the coordinator takes a few seconds to decide a silent consumer is dead. During those seconds, that consumer's partitions are simply not processed by anyone.
- **Graceful leave:** the departing consumer notifies the coordinator it is leaving, and the coordinator triggers the rebalance immediately — no dead-time waiting on missed heartbeats.

Kafka lets you control the heartbeat frequency and related consumer configuration parameters, which is the knob between "detect failures fast" and "don't rebalance on every network hiccup."

**Who computes the new assignment.** Not the coordinator. The first consumer to join the group becomes the group leader; it fetches the list of active consumers from the coordinator and assigns a subset of partitions to each member, using the configured strategy (see [[consumer-groups-and-partition-assignment]]).

**The two rebalance types.** This is where the real trade-off lives:

1. **Eager rebalancing:** every consumer stops consuming, gives up *all* of its partition ownership, and rejoins the group to receive a brand-new assignment. The whole group is briefly unavailable — even consumers whose partitions would not have moved.
2. **Cooperative rebalancing:** only a subset of partitions changes hands, and consumers keep processing the partitions that are not being reassigned. Mechanically it runs in phases: the group leader notifies all consumers which partitions they will lose; those consumers stop processing *only those* partitions and give up ownership; then the leader assigns the orphaned partitions to their new owners. This proceeds incrementally, a few rounds, until the assignment is stable. The critical property is that it never requires the total group to stop — which matters most in large consumer groups, where a full stop-the-world pause is expensive.

**Why your assignment strategy decides how painful rebalancing is.** The strategies differ precisely in how much partition movement a rebalance causes. Round robin maximizes consumer utilization but requires a lot of partition movement on rebalance. The Sticky strategy assigns like round robin initially but preserves as many existing assignments as possible on reassignment: in Vu Trinh's example with topics T1 and T2 (three partitions each) and consumers C1 and C2, when C2 dies and C3 replaces it, only C2's old partitions move to C3 — C1's partitions are left alone. Its two goals are a balanced assignment and minimal rebalance overhead. Cooperative Sticky is the same assignor but with cooperative rebalancing enabled, so consumers keep consuming from untouched partitions during the reassignment.

One more consequence worth internalizing: because the broker tracks consumption via committed offsets rather than the consumer tracking itself (see [[pull-based-consumption-and-offset-commit]]), a consumer that inherits a partition after a rebalance picks up from the last committed position — the broker assumes everything before that point was processed. Rebalancing moves ownership; the offset commit protocol is what makes that ownership transfer resumable.

## Related in the other wiki
- [[Rebalancing Partitions]] — DDIA's requirement that rebalancing not interrupt availability is precisely what separates Kafka's eager rebalancing (whole group stops) from cooperative rebalancing (only the affected partitions pause) — the same fairness-vs-availability trade-off DDIA describes for storage nodes, here applied to consumer ownership instead of data location.
