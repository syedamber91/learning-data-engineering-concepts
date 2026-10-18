---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, storage, durability, recovery]
sources:
  - raw/ch04.md
  - raw/ch08.md
---
# Write-Ahead Log

Append every change to a sequential log before applying it to the main data structure, so a crash mid-update can be repaired by replaying the log. The mechanism behind B-tree crash safety and the raw material for change data capture.

See [[B-Trees (2e)]] and [[Change Data Capture (2e)]].

## Appears In
- [[B-Trees (2e)]]
- [[Byzantine Faults (2e)]]
- [[Clock Synchronization and Accuracy (2e)]]
- [[Comparing B-Trees and LSM-Trees (2e)]]
- [[Distributed Locks and Leases (2e)]]
- [[Distributed Transactions (2e)]]
- [[Durable Execution and Workflows (2e)]]
- [[Fault Tolerance (2e)]]
- [[Formal Methods and Randomized Testing (2e)]]
- [[ID Generators and Logical Clocks (2e)]]
- [[Implementation of Replication Logs (2e)]]
- [[JSON, XML, and Binary Variants (2e)]]
- [[Log-Structured Storage (2e)]]
- [[Monotonic Versus Time-of-Day Clocks (2e)]]

## In the vutr data-engineering wiki
- [[write-ahead-log]] — Vu grounds the same log-before-apply principle in the LSM memtable's durability story rather than the book's B-tree crash-recovery framing.
- [[log-based-cdc]] — the same rule across three real DBMSs — Oracle's redo log, Postgres's WAL, MySQL's binlog — and why that crash-recovery guarantee makes the log the ideal complete source for CDC.
