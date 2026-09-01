---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, fault-tolerance, exactly-once, retries]
sources:
  - raw/ch12.md
  - raw/ch13.md
---
# Idempotence

An operation you can safely apply more than once without changing the result beyond the first application. The workhorse of at-least-once delivery: if retrying is harmless, you no longer need exactly-once machinery.

Usually achieved with a client-generated request ID carried end to end — see [[The End-to-End Argument for Databases (2e)]] and [[Fault Tolerance (Stream Processing) (2e)]].

## Appears In
- [[Aiming for Correctness (2e)]]
- [[Combining Specialized Tools by Deriving Data (2e)]]
- [[Composing Data Storage Technologies (2e)]]
- [[Database-Internal Distributed Transactions (2e)]]
- [[Dataflow Through Services - REST and RPC (2e)]]
- [[Durable Execution and Workflows (2e)]]
- [[Exactly-Once Message Processing Revisited (2e)]]
- [[Fault Tolerance (Stream Processing) (2e)]]
- [[Messaging Systems (2e)]]
- [[Problems with Distributed Systems (2e)]]
- [[The End-to-End Argument for Databases (2e)]]
- [[The Limitations of TCP (2e)]]
- [[Timeliness and Integrity (2e)]]
- [[Unreliable Networks (2e)]]
