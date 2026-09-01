---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, cdc, integration, derived-data]
sources:
  - raw/ch12.md
  - raw/ch13.md
---
# Change Data Capture

Turning a database's own replication log into a stream other systems can consume, so indexes, caches, and warehouses stay in sync with the system of record without dual writes.

See [[Change Data Capture (2e)]] and [[Keeping Systems in Sync (2e)]].

## Appears In
- [[Change Data Capture (2e)]]
- [[Combining Specialized Tools by Deriving Data (2e)]]
- [[Composing Data Storage Technologies (2e)]]
- [[Databases and Streams (2e)]]
- [[Designing Applications Around Dataflow (2e)]]
- [[Fault Tolerance (Stream Processing) (2e)]]
- [[Implementation of Replication Logs (2e)]]
- [[Keeping Systems in Sync (2e)]]
- [[Log-Based Message Brokers (2e)]]
- [[State, Streams, and Immutability (2e)]]
- [[Stream Joins (2e)]]
- [[The End-to-End Argument for Databases (2e)]]

## In the vutr data-engineering wiki
- [[log-based-cdc]] — reading the replication log directly, named across Oracle, Postgres, and MySQL.
