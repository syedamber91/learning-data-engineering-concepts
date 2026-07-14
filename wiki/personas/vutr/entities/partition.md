---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: partition
topics:
- kafka
---

LinkedIn made a partition the smallest unit of parallelism, so at any moment all messages from one partition are consumed by only a single consumer within a consumer group. A direct consequence: if a group has more consumers than partitions, the surplus consumers get no messages.

*See also: [[kafka-origin]] · [[paypal-kafka-scale]] · [[tiered-storage-kip-405]] · [[linkedin-kafka-scale]] · [[logical-offset]] · [[acks-setting]]*

## Related in the other wiki
- [[Partitioning]] — DDIA's general concept of splitting a dataset into disjoint subsets across nodes for scalability is exactly what a Kafka partition operationalizes, down to the "more consumers than partitions leaves some idle" failure mode echoing DDIA's skew/hot-spot concern.
