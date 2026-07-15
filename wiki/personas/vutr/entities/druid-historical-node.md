---
persona: vutr
kind: entity
sources:
- raw/druid-pinot-real-time-olap/the-architecture-of-apache-druid.md
last_updated: '2026-07-15'
qc: passed
slug: druid-historical-node
topics:
- apache-pinot-druid-and-real-time-olap
---

Historical nodes load and serve the segments that real-time nodes have finalized and shipped to deep storage (see [[druid-realtime-node]]). Segments live remotely on storage like S3 or HDFS, and a historical node's local disk is used only as a cache. Like real-time nodes, historical nodes announce their online state and the data they're serving to Zookeeper; Druid pushes instructions to Zookeeper telling historical nodes how to load and drop segments, including where a segment lives in deep storage and how to decompress and process it.

**Download path.** Before downloading a needed segment, a historical node first checks its local cache; only if the segment isn't cached does it fetch it from deep storage. After downloading, it announces its status to Zookeeper. Because historical nodes only ever deal with immutable data, they can guarantee consistency when reading segments, and immutability lets Druid parallelize more efficiently since there's never a concern that some other process is modifying the data mid-read (see [[immutable-segment]]).

**Tiering.** Historical nodes can be grouped into different tiers, each with its own configurable performance and fault-tolerance parameters. The purpose is to route segments to nodes by priority or access frequency: a "hot" tier of historical nodes might run high-CPU, high-memory hardware and hold the most frequently accessed data, while a "cold" tier holds only the less-frequently accessed segments.

*See also: [[apache-druid]] · [[druid-realtime-node]] · [[druid-coordinator-node]] · [[druid-broker]] · [[immutable-segment]]*
