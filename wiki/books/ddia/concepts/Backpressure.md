---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, streams, flow-control]
sources:
  - raw/ch11.md
---
# Backpressure

Slowing the producer down when the consumer can't keep up, rather than buffering
without bound or dropping data. TCP does it with its sliding window; Unix pipes with
a fixed-size buffer that blocks the writer; message brokers choose between
backpressure, buffering, and dropping.

In the book: one of the three answers to "producer faster than consumer" in
[[Messaging Systems]] (Ch 11), and part of why [[The Unix Philosophy]] pipelines
compose safely. Log-based brokers ([[Apache Kafka]]) sidestep it by buffering on
disk and letting slow consumers lag.

## Referenced In
- [[Messaging Systems]]
- [[Synchronous Versus Asynchronous Networks]]
- [[Timeouts and Unbounded Delays]]
- [[Transmitting Event Streams]]
- [[Unreliable Networks]]
