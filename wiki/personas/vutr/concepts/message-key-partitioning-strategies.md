---
persona: vutr
kind: concept
sources:
- raw/kafka/apache-kafka-producer.md
- raw/kafka/if-youre-learning-kafka-this-article.md
- raw/kafka/doordashs-real-time-processing-system.md
last_updated: '2026-07-10'
qc: passed
slug: message-key-partitioning-strategies
topics:
- kafka
---

A common assumption is that a Kafka message has some explicit ID and the key is just metadata. Neither is true. A message stored in Kafka has no explicit message ID at all — it is addressed by its logical offset within a partition — and the key, while optional and null by default, is not decoration: it is the input to the routing decision that determines which partition a message lands on. Since partitions are how Kafka achieves scalability and redundancy (each partition can live on a different server, so a topic scales horizontally), the key is effectively how you control where your data physically goes.

Where the decision happens in the send path: when you call the producer API, the process creates a ProducerRecord that must include the value and destination topic, and may include a key, partition, timestamp, and headers. The producer serializes the key and value objects to byte arrays. Only if no partition was explicitly specified does the record get routed to the partitioner — the component that chooses the partition based on the key. Once topic and partition are known, the record joins the batch of messages headed to that same topic and partition, and a separate thread ships those batches to the appropriate brokers (see [[producer-send-path-and-acks]] for the rest of the flow, and [[message-batching-and-compression]] for why batches matter).

The partitioner then splits on one question: is the key null?

**Null key, no custom partitioner.** Here a second misconception needs correcting: "keyless messages are spread round-robin" is only true on old versions. With Kafka ≤ v2.3, the Round-Robin partitioner assigns messages to partitions cyclically — one after another, then back to the first. From Kafka ≥ 2.4, the default is the Sticky Partitioner: it sticks to one particular partition for a batch of records, sending as many records as possible to that same partition until a condition is met — such as the batch reaching its limit — and only then switches to another partition. The why is batching mechanics: the producer accumulates records per topic-partition (controlled by the batch size limit and the linger wait time before sending), and Kafka batches to achieve larger sequential disk operations and avoid many small requests. Round-robin fragments records across many partitions and therefore many small batches; sticky fills one batch at a time.

**Non-null key.** Kafka hashes the key and uses the result to map the message to a partition — the learning-baseline article describes this as consistent hashing on the key. The guarantee that follows is the whole point: messages with the same key are always routed to the same partition. Combined with per-partition sequential consumption, this is how you get ordering and locality for a given entity. If neither default fits, Kafka lets you define a custom partitioner.

DoorDash's real-time platform shows these knobs pulled deliberately at billions-of-events scale. Building on Kafka and Flink (fronted by the Confluent Kafka REST Proxy so services and mobile/web clients don't each manage producer connections), DoorDash prioritized throughput and availability over data consistency and tuned three things: they cut the replication factor from 3 (one leader, two followers) to 2, saving disk space and the CPU spent on replication; they set acks=1, so the producer is acknowledged as soon as the leader has the message rather than waiting for follower replication; and they leaned on the sticky partitioner to pin produced messages to one partition per batch until the batch limit is hit. Together, this tuning contributed to a 30–40% decrease in Kafka broker CPU utilization. Note the trade-off is explicit, not hidden: fewer replicas and leader-only acks buy throughput by accepting more data-loss risk.

Downstream, the partitioning choice is also a parallelism choice: a topic's partition is the smallest unit of parallelism, and within a consumer group each partition is consumed by exactly one consumer ([[consumer-groups-and-partition-assignment]]). A key that hashes hot traffic onto one partition concentrates that load on one consumer — the routing decision made at produce time is the load distribution you live with at consume time.
