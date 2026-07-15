---
persona: vutr
kind: entity
sources:
- raw/druid-pinot-real-time-olap/a-glimpse-of-apache-pinot-the-real.md
last_updated: '2026-07-15'
qc: passed
slug: apache-pinot
topics:
- apache-pinot-druid-and-real-time-olap
---

Apache Pinot is LinkedIn's real-time OLAP system, introduced in 2013 to serve tens of thousands of analytical queries per second in production while still offering near-real-time data ingestion from streaming sources — a combination classic OLAP tooling (bulk-load oriented, high latency) can't provide. The motivating example the source gives is LinkedIn's "Who viewed my profile" feature: a large user base, low-latency response, very high QPS, all on top of what is fundamentally an analytical query.

LinkedIn's stated requirements for a system like Pinot: fast, interactive-level performance (batch tools like MapReduce and Spark have high throughput but their latency and lack of online processing "limit fluent interaction"); near-linear scalability under high concurrent query load; cost-effectiveness with an upper bound as data and query volume grow; low data-ingestion latency (querying recently-added rows without waiting on a batch job, unlike systems that only support bulk loads); flexibility (not boxing users into predefined dimensions when they drill down); fault tolerance; uninterrupted operation (no downtime for upgrades or schema changes); and a cloud-friendly architecture. See [[real-time-olap]] for how these requirements frame the broader real-time-OLAP problem space.

**Architecture in brief.** Pinot follows the lambda architecture: it consumes online data directly from Kafka and offline data from Hadoop, with the offline data serving as the global view and the online data providing the more current view. Data is organized into tables with a fixed schema of dimension and metric columns, plus a special time column used specifically to merge the offline and online halves during a query (see [[offline-realtime-query-merge]]). Tables are partitioned into segments — a typical segment holds a few dozen million records, and a table can have tens of thousands of segments; segments are immutable, columnar, redundantly replicated, and encoded with dictionary encoding and bit packing to cut size (see [[immutable-segment]]). The cluster itself is built from four component types — controllers, brokers, servers, and minions — coordinated via Apache Helix and Zookeeper (see [[pinot-cluster-components]] and [[pinot-broker]]).

Users query Pinot through PQL, a deliberately narrow SQL subset (see [[pinot-pql]]), and Pinot can return pre-aggregated answers straight from its star-tree index when a query's shape allows it (see [[star-tree-index]]).

**Cloud-friendly by design.** Pinot has a share-nothing architecture of stateless instances: all persistent data lives in object storage and all metadata in Zookeeper, with local disk used only as a cache that can always be refilled from object storage or Kafka — the same pattern the source likens to Amazon Redshift and Snowflake. This means Pinot can add or remove server nodes at any time without risking data loss or a performance hit, and it deploys cleanly on container orchestrators like Kubernetes since only the code communicating with cloud object storage needs to change.

**Operating Pinot as a service.** LinkedIn runs Pinot as a self-service model with a dedicated operating team that grows with demand. New columns can be added to an existing schema without downtime — Pinot auto-fills the column with default values across existing segments and makes it queryable within minutes. Pinot also parses query logs and execution statistics to automatically add inverted indexes to columns when doing so would improve performance. Table configurations are stored in source control and synced to Pinot via a REST API, so every configuration change can be audited, searched, and reviewed like code.

**Two use-case shapes.** LinkedIn observed its users splitting into two categories: high-throughput, low-complexity queries over a small number of query patterns, which need data resident in memory to serve high QPS; and complex or larger-volume queries that don't need high query rates, which are placed on hardware with NVMe storage — LinkedIn co-locates this hardware with other tenants for efficient utilization.

*See also: [[apache-druid]] · [[real-time-olap]] · [[pinot-broker]] · [[pinot-cluster-components]] · [[star-tree-index]] · [[pinot-pql]] · [[immutable-segment]]*
