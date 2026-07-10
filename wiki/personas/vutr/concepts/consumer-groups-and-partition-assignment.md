---
persona: vutr
kind: concept
sources:
- raw/kafka/apache-kafka-consumer.md
- raw/kafka/if-youre-learning-kafka-this-article.md
- raw/kafka/apache-kafka-part-1-overview.md
last_updated: '2026-07-10'
qc: passed
slug: consumer-groups-and-partition-assignment
topics:
- kafka
---

A common assumption is that scaling Kafka consumption means making one consumer faster. It doesn't. When producers write faster than your single consumer can read, the answer is not a bigger consumer — it needs "friends" to share the workload. That is what a consumer group is: one or more consumers with the same group ID consuming a set of subscribed topics together. Assign a group ID once, and any new consumer instance added to the group automatically receives that same ID.

The unit the group divides up is the partition, not the message. LinkedIn made a partition in a topic the smallest unit of parallelism, so at any given time all messages from one partition are consumed by only a single consumer within a group. Two hard consequences follow. First, if the group has more consumers than the topic has partitions, the extra consumers get no messages at all — adding consumers past the partition count buys you nothing. Second, different consumer groups consume the topic independently; the single-consumer-per-partition rule only applies inside a group. A concrete mapping: a topic with four partitions (p0, p1, p2, p3) and a group of three consumers (c0, c1, c2) might resolve to c0→p0, c1→p1 and p2, c2→p3.

Who decides that mapping? Two roles, often confused. The **Group Coordinator** is one of the brokers chosen for this responsibility (different groups get different brokers, determined by the group ID); it balances load within the group and reacts to membership changes. The **group leader** is a consumer: when a consumer wants to join, it sends a join request to the coordinator, and the first one to join becomes the leader. The leader gets the list of all active consumers from the coordinator and assigns a subset of partitions to each. Membership itself is maintained by heartbeats — each consumer uses a background thread to send heartbeats to the coordinator, and as long as they arrive at regular intervals the consumer is assumed alive. If heartbeats stop, the coordinator takes a few seconds to decide the consumer is dead — during which that consumer's partitions process nothing — then triggers a rebalance (see [[consumer-group-rebalancing]]). A consumer that leaves cleanly notifies the coordinator, which triggers rebalancing immediately. Kafka lets you control the heartbeat frequency via consumer configuration.

The leader assigns partitions using one of Kafka's assignment strategies:

**Range** (the default) works on each topic *independently*, giving each consumer a consecutive subset of that topic's partitions: divide partitions by consumers, and if it doesn't divide evenly, the first few consumers take the extras. With topics T1 and T2 at three partitions each and consumers C1, C2: 3/2 = 1 with a remainder, so C1 gets T1[P1, P2] and T2[P1, P2] while C2 gets only T1[P3] and T2[P3]. The per-topic remainder lands on the same first consumers every time — more burden on those instances.

**Round Robin** works *across all subscribed topics*, dealing partitions out sequentially: C1 gets T1-P1, T1-P3, T2-P2; C2 gets T1-P2, T2-P1, T2-P3. This maximizes the number of consumers used — add a third consumer to that example and each ends up with two partitions. The trade-off: it moves a lot of partitions around when rebalancing happens.

**Sticky** assigns like round robin initially but differs on *reassignment*: it preserves as many existing assignments as possible. In the same example, if C2 dies and C3 replaces it, only C2's partitions move to C3 — C1's are left alone. Its two goals are a balanced assignment and minimal rebalancing overhead by keeping assignments in place.

**Cooperative Sticky** is the same assignor but supports cooperative rebalancing, letting consumers keep consuming from partitions that aren't being reassigned instead of everyone stopping — the distinction that matters most in large groups, covered in [[consumer-group-rebalancing]].

Note what the group does *not* solve: how consumers fetch and track position. Consumers still pull sequentially per partition and commit offsets through the broker's internal \_\_consumer\_offsets topic ([[pull-based-consumption-and-offset-commit]]), and which partition a message lands on in the first place is the producer's decision, not the group's ([[message-key-partitioning-strategies]]).
