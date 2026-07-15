---
persona: vutr
kind: concept
sources:
- raw/druid-pinot-real-time-olap/a-glimpse-of-apache-pinot-the-real.md
- raw/druid-pinot-real-time-olap/the-architecture-of-apache-druid.md
last_updated: '2026-07-15'
qc: passed
slug: immutable-segment
topics:
- apache-pinot-druid-and-real-time-olap
---

Both Pinot and Druid organize their analytical data as immutable, columnar "segments" — but they arrive at immutability from different directions. Pinot's segments are fixed, read-optimized units from the start: partitioned subsets of a table (a typical segment holds a few dozen million records, and a table can carry tens of thousands of segments), stored redundantly across replicas, encoded with dictionary encoding and bit packing to shrink size, ranging from a few hundred megabytes to a few gigabytes. Any data update produces new segments rather than mutating existing ones. Druid's segments, by contrast, are the end product of a conversion: real-time nodes hold newly-ingested data as an in-memory row-store index, periodically persist it to disk in column-oriented form (triggered by time or by a maximum-row threshold), and a background task merges these persisted pieces into a single immutable data block covering a time range before it's uploaded to deep storage. Once a segment exists in either system, it doesn't change.

The payoff both sources land on is the same: immutability buys consistency and parallelism essentially for free. Druid's historical nodes can guarantee read consistency and parallelize execution more efficiently specifically because they never have to worry about a concurrent write modifying the data underneath them. Pinot gets an analogous guarantee by storing multiple segment replicas that all participate in query processing without read-time coordination overhead — replication here is as much about throughput as availability.

The two engines then diverge on what makes segments fast once they're immutable. Pinot layers structural indexing on top of its segments — the star-tree index (see [[star-tree-index]]), plus range and bitmap inverted indexes — in addition to the write-time dictionary encoding and bit packing. Druid's segments instead carry a timestamp dimension as a structural requirement, used for both data distribution and retention policy, get per-data-type compression schemes, and get tiered by access frequency (hot vs. cold) at the historical-node level (see [[druid-historical-node]]) rather than indexed more heavily.

*See also: [[apache-pinot]] · [[apache-druid]] · [[real-time-olap]] · [[star-tree-index]] · [[druid-historical-node]] · [[pinot-cluster-components]]*
