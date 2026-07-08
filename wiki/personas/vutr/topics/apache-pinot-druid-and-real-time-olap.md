---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: apache-pinot-druid-and-real-time-olap
---

Related: [[apache-pinot]] · [[apache-druid]] · [[star-tree-index]] · [[pinot-broker]] · [[druid-broker]] · [[pinot-pql]] · [[real-time-olap]] · [[immutable-segment]]

## Comparisons
Against Elasticsearch, [[apache-pinot]] claims 4x less memory, 8x less disk, and 2x-4x lower latency. Against [[apache-druid]], Pinot's edge is structural: bit-compressed forward indices plus the [[star-tree-index]] give it an order-of-magnitude latency advantage. The two engines share a lot of DNA — both are [[real-time-olap]] systems built on [[immutable-segment]] storage — but they diverge on architecture and query routing. Druid's [[druid-broker]] never caches real-time-node results to protect freshness, whereas Pinot's [[pinot-broker]] leans on scatter-gather-merge and token-bucket multi-tenancy. Note the query-surface trade-off too: [[pinot-pql]] drops joins, nested queries, DDL, and record-level operations to stay fast.

## Open questions
- The source gives Pinot's advantage over Druid as "order-of-magnitude latency," but under what query shapes does that hold, and where does Druid's share-nothing design win instead?
- How exactly does Druid's real-time-node-to-historical-node handoff of segments behave, and what is the freshness/consistency boundary during that conversion?
- What are the practical limits imposed by [[pinot-pql]] lacking joins and nested queries — how do teams model around them?
- The note says memory for high-QPS simple queries and NVMe for complex queries on larger data; where is the crossover, and who decides the placement?
- Druid brokers use last known state during Zookeeper failure — what staleness window does that introduce?

## Synthesis
[[apache-pinot]] and [[apache-druid]] are two takes on [[real-time-olap]] that agree on the fundamentals — [[immutable-segment]] columnar storage, memory for high-QPS simple queries, NVMe for heavier ones — but split on architecture. Druid's [[druid-broker]] protects freshness by refusing to cache real-time-node results, while Pinot bets on structural speed via the [[star-tree-index]] and bit-compressed forward indices, accepting a deliberately narrow [[pinot-pql]] as the cost. The recurring theme is that immutability buys consistency and parallelism, and that these engines earn their QPS by trading query-surface generality for latency.

## Related topics
- [[olap-engine-internals-bigquery-snowflake-clickhouse-redshift-duckdb-databricks]] — Pinot and Druid are real-time OLAP engines built on the same columnar, immutable-segment internals as the warehouse-scale OLAP engines.
- [[storage-models-nsm-dsm-pax-and-column-store]] — Pinot and Druid store data as immutable columnar segments, an application of the DSM/column-store storage model for fast analytical scans.
- [[kafka]] — Real-time OLAP engines ingest streaming events from Kafka to serve low-latency queries over fresh data.
- [[lsm-tree-storage-engines]] — Their immutable-segment storage with background merges mirrors the LSM-tree pattern of turning writes into immutable sorted files resolved by compaction.
