---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, replication, consistency]
sources:
  - raw/ch06.md
  - raw/ch10.md
---
# Eventual Consistency

The weak guarantee that if you stop writing and wait long enough, all replicas will converge on the same value. It says nothing about how long, and nothing about what you may read in the meantime.

The book's complaint is that the name is a promise about the end state with no promise about the journey — hence the more useful, more specific models in [[Problems with Replication Lag (2e)]] and the strong alternative in [[Linearizability (2e)]].

## Appears In
- [[Change Data Capture (2e)]]
- [[Combining Specialized Tools by Deriving Data (2e)]]
- [[Dealing with Conflicting Writes (2e)]]
- [[Detecting Concurrent Writes (2e)]]
- [[Problems with Replication Lag (2e)]]
- [[Solutions for Replication Lag (2e)]]
- [[Synchronous Versus Asynchronous Replication (2e)]]
- [[System Model and Reality (2e)]]
- [[The Meaning of ACID (2e)]]
- [[Timeliness and Integrity (2e)]]
- [[Writing to the Database When a Node Is Down (2e)]]
