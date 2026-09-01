---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, systems, streaming, broker]
sources:
  - raw/ch12.md
---
# Apache Kafka

The log-based message broker that anchors most of the book's stream-processing material: a partitioned, replicated, append-only log with consumer offsets and disk-backed retention.

See [[Log-Based Message Brokers (2e)]] and [[Log-Based Message Brokers (2e)]]. The 2nd edition adds its object-storage-backed successors — WarpStream, Confluent Freight, Bufstream.

## Appears In
- [[Avro (2e)]]
- [[Change Data Capture (2e)]]
- [[Consensus in Practice (2e)]]
- [[Database-Internal Distributed Transactions (2e)]]
- [[Distributed Locks and Leases (2e)]]
- [[Event-Driven Architectures (2e)]]
- [[Exactly-Once Message Processing Revisited (2e)]]
- [[Fault Tolerance (Stream Processing) (2e)]]
- [[Formal Methods and Randomized Testing (2e)]]
- [[Log-Based Message Brokers (2e)]]
- [[Messaging Systems (2e)]]
- [[Microservices and Serverless (2e)]]
- [[Request Routing (2e)]]
- [[Serving Derived Data (2e)]]

## In the vutr data-engineering wiki
- [[kafka]] — vutr's topic is the production history behind this one-paragraph sketch, and now runs *past* the book: LinkedIn's Northguard rewrite is the same company walking back its own original design.
