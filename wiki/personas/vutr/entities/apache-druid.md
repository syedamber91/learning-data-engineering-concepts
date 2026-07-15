---
persona: vutr
kind: entity
sources:
- raw/druid-pinot-real-time-olap/the-architecture-of-apache-druid.md
last_updated: '2026-07-15'
qc: passed
slug: apache-druid
topics:
- apache-pinot-druid-and-real-time-olap
---

Apache Druid began at Metamarkets (now Rill), a company helping marketers access, interact with, and visualize marketing insights. Metamarkets needed guaranteed query performance and data availability under high concurrency for the dashboards underneath its product — users needed an interactive experience exploring event streams, which meant fast query response, high availability (downtime hurts the business), and concurrency (many simultaneous users). After finding Hadoop, and the available open-source options more broadly, couldn't meet those needs, Metamarkets built Druid: "a data store for real-time analytics on large data sets."

**Architecture.** Druid has a share-nothing architecture. A cluster is made of distinct node types, each responsible for a set of duties: real-time nodes ingest and query event streams as they arrive ([[druid-realtime-node]]); historical nodes load and serve the durable, deep-storage-backed segments ([[druid-historical-node]]); broker nodes route queries to whichever node types hold the needed data and merge the results ([[druid-broker]]); and coordinator nodes manage how segments are distributed and replicated across historical nodes ([[druid-coordinator-node]]). The source notes it is based on Druid's 2014 technical paper, so it describes the original design and does not cover components added later, such as Overlord nodes.

**Storage format.** Druid tables are collections of timestamped events, partitioned into segments — typically 5 to 10 million rows each — which are the fundamental unit both replication and distribution operate on. Every table carries a timestamp column, which Druid requires because it drives both data distribution and retention policy. Segments are identified by a data-source identifier, the time interval they cover, and a version; later versions hold fresher data, and reads for a given time range always go to the latest-version segments. Segments are stored in remote storage in columnar format, so only the columns a query actually needs get loaded, and different data types get different compression schemes to shrink their footprint on disk and in memory further. See [[immutable-segment]] for how this compares to Pinot's segment model.

*See also: [[apache-pinot]] · [[real-time-olap]] · [[druid-broker]] · [[druid-realtime-node]] · [[druid-historical-node]] · [[druid-coordinator-node]] · [[immutable-segment]]*
