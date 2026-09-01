---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, architecture, scale, simplicity]
sources:
  - raw/ch01.md
---
# Single-Node Systems

One machine, no distribution. The 2nd edition argues far more forcefully than the 1st that this is the right default: modern servers have enormous RAM and NVMe throughput, and distribution buys scale at the cost of an entire category of failure modes.

See [[Distributed Versus Single-Node Systems (2e)]] — and [[Faults and Partial Failures (2e)]] for exactly what you take on when you cross that line.

## Appears In
- [[Cloud Computing Versus Supercomputing (2e)]]
- [[Cloud Versus Self-Hosting (2e)]]
- [[Column-Oriented Storage (2e)]]
- [[Combining Specialized Tools by Deriving Data (2e)]]
- [[Consensus (2e)]]
- [[Distributed Transactions (2e)]]
- [[Distributed Transactions Across Different Systems (2e)]]
- [[Distributed Versus Single-Node Systems (2e)]]
- [[Enforcing Constraints (2e)]]
- [[Faults and Partial Failures (2e)]]
- [[ID Generators and Logical Clocks (2e)]]
- [[Keeping Everything in Memory (2e)]]
- [[Linearizability (2e)]]
- [[Linearizable ID Generators (2e)]]
