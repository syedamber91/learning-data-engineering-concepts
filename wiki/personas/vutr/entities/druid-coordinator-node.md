---
persona: vutr
kind: entity
sources:
- raw/druid-pinot-real-time-olap/the-architecture-of-apache-druid.md
last_updated: '2026-07-15'
qc: passed
slug: druid-coordinator-node
topics:
- apache-pinot-druid-and-real-time-olap
---

Coordinator nodes manage data distribution across historical nodes: they tell historical nodes to load new data, drop outdated data, replicate data, and move data to load-balance the cluster. A coordinator runs a leader-election process to determine which single node actually executes coordinator tasks at any time, with the rest acting as redundant backups.

A coordinator runs periodically, determines the cluster's current state, and makes decisions by comparing that current state against the expected state — the source draws an explicit parallel to how Kubernetes reconciles state. Like every other Druid node type, coordinators communicate with Zookeeper for current cluster information. They're also connected to a MySQL database that stores additional operational parameters and configuration — including a rule table that controls how segments are created, destroyed, and replicated across the cluster.

**The rule table.** Rules tell the coordinator: how segments should be assigned to different historical-node tiers, how many replicas of a segment should exist in each tier, and when to drop segments. Beyond enforcing these rules, coordinator nodes keep the cluster balanced by controlling how segments are distributed, and can direct historical nodes to load additional copies of a segment to improve fault tolerance and availability — the replica count itself is configurable.

*See also: [[apache-druid]] · [[druid-historical-node]] · [[druid-realtime-node]] · [[druid-broker]]*
