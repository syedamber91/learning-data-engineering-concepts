---
persona: vutr
kind: concept
sources:
- raw/clickhouse-internals/i-spent-3-hours-learning-the-overview.md
- raw/clickhouse-internals/i-spent-8-hours-learning-the-clickhouse.md
last_updated: '2026-07-15'
qc: passed
slug: clickhouse-replication-and-keeper-consensus
topics:
- clickhouse-internals
---

Replication in ClickHouse serves two purposes at once: high availability and higher read throughput, since reads can be load-balanced across replicas. Every MergeTree engine has a matching replicated variant (`MergeTree` → `ReplicatedMergeTree`, `ReplacingMergeTree` → `ReplicatedReplacingMergeTree`, `AggregatingMergeTree` → `ReplicatedAggregatingMergeTree`), and ClickHouse's sharding model lets a table's data be divided into shards (a shard is effectively a separate table users can query directly, or view consolidated via a distributed table engine) while each shard can also be replicated across nodes for fault tolerance.

The mechanism rests on the idea of **table state** — a set of table parts plus metadata like column names and types. Three kinds of operations change that state: inserts (add a part), merges (add a part, remove the merged-from parts), and mutations/DDL (add parts, remove parts, or alter metadata). Each operation is first performed locally on one node, then recorded as a state transition in a **global replication log**. This log is maintained by a set of ClickHouse Keepers (typically three) using the Raft consensus algorithm (see [[clickhouse-keeper]]) — the source calls this a "multi-master coordination scheme." All cluster nodes start pointed at the same log position; as any node executes operations, the other nodes asynchronously replay the log to catch up. The direct consequence is that replicated tables in ClickHouse are only **eventually consistent** — a node may briefly read an outdated table state, though all nodes eventually converge.

A worked example makes the asynchronous replay concrete: with a table replicated across three nodes, Node 1 receives two `INSERT`s and records them in the log. Node 2 replays only the first log entry (fetching it and downloading the corresponding part from Node 1). Meanwhile Node 3 replays both entries — downloading both parts from Node 1 — then locally merges the two downloaded parts into a new part, deletes the inputs, and records its own merge entry in the log. All nodes continue replaying the log asynchronously from there. Nothing in the source requires nodes to replay the log at the same pace or in lockstep — each node's local table state is a function of how far through the log it has gotten.

This eventual-consistency default is exactly what the `insert_quorum` setting (see [[clickhouse-insert-process-and-idempotency]]) is designed to override for batch workloads that can't tolerate reading a partial replica state.

*See also: [[clickhouse-keeper]] · [[mergetree-storage-engine]] · [[clickhouse-insert-process-and-idempotency]]*
