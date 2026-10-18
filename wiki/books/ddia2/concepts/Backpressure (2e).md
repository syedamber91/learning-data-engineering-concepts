---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, streams, flow-control]
sources:
  - raw/ch12.md
  - raw/ch02.md
---
# Backpressure

Slowing the producer down when the consumer can't keep up, rather than buffering without bound or dropping data. TCP does it with its sliding window; Unix pipes with a fixed-size buffer that blocks the writer; message brokers choose between backpressure, buffering, and dropping.

Log-based brokers sidestep it by buffering on disk and letting slow consumers lag — see [[Log-Based Message Brokers (2e)]].

## Appears In
- [[Comparing B-Trees and LSM-Trees (2e)]]
- [[Describing Performance (2e)]]
- [[Distributed Job Orchestration (2e)]]
- [[Log-Based Message Brokers (2e)]]
- [[Messaging Systems (2e)]]
- [[The Limitations of TCP (2e)]]
