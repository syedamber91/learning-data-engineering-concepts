---
persona: vutr
kind: entity
sources:
- raw/clickhouse-internals/i-spent-3-hours-learning-the-overview.md
- raw/clickhouse-internals/i-spent-8-hours-learning-the-clickhouse.md
- raw/clickhouse-internals/clickhouse-real-time-insight-in-15.md
last_updated: '2026-07-15'
qc: passed
slug: clickhouse-keeper
topics:
- clickhouse-internals
---

ClickHouse Keeper is described as ClickHouse's own C++ replacement for Apache ZooKeeper. When a table uses a `Replicated*` MergeTree engine, ClickHouse Keeper is what backs the multi-master coordination scheme: it implements the Raft consensus algorithm so that each shard can consistently maintain a configurable number of replicas. Concretely, Keeper maintains the **global replication log** — the ordered record of table-state transitions (inserts, merges, mutations/DDL) that every node in a replicated cluster replays asynchronously to converge on the same state (see [[clickhouse-replication-and-keeper-consensus]]). The source notes that a replication log is typically maintained by a set of **three** ClickHouse Keepers.

Self-managing a ClickHouse cluster requires deciding how to coordinate the cluster's nodes at all — the source names "ClickHouse Keeper or Zookeeper" as one of the concrete operational decisions a team must make when running ClickHouse themselves, alongside sharding strategy and handling node membership changes. This is one of the specific burdens that managed platforms like [[tinybird]] take off a team's hands.

*See also: [[clickhouse-replication-and-keeper-consensus]] · [[mergetree-storage-engine]] · [[clickhouse]]*
