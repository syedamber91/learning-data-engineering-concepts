---
persona: vutr
kind: entity
sources:
- raw/druid-pinot-real-time-olap/a-glimpse-of-apache-pinot-the-real.md
last_updated: '2026-07-15'
qc: passed
slug: pinot-cluster-components
topics:
- apache-pinot-druid-and-real-time-olap
---

Pinot's architecture has four main components — controllers, brokers, servers, and minions — plus two external services it leans on: Apache Zookeeper for state management and a persistent object store. Cluster management itself runs on Apache Helix, a framework for managing partitions, replicas, and resources in a distributed system. (Brokers get their own note: [[pinot-broker]].)

**Servers** host segments and execute queries. A segment is stored as a directory in the Unix filesystem holding a metadata file (the segment's column types, cardinality, encoding scheme, column statistics, and which indexes are available per column) and an append-only index file (indexes for every column). Segments are stored with multiple replicas for high availability, and all replicas participate in query processing, which also improves throughput. Servers have a pluggable architecture for loading columnar indexes from different storage formats, letting them read from distributed filesystems like HDFS or object storage like S3 — and notably, Pinot stores segments in object storage and loads them into servers for processing; a server doesn't hold the authoritative copy itself.

**Controllers** maintain the mapping of segments to servers using a configurable strategy, and trigger changes to that mapping in response to requests or to changes in server availability (a server going down, a server being added). Controllers support administrative tasks like listing, adding, or deleting tables and segments, and let users define a table's retention interval for the garbage collector. LinkedIn runs three controller instances per data center for fault tolerance, with a single master among them.

**Minions** handle maintenance tasks assigned by the controllers' job scheduler — the source's example is data purging, which LinkedIn must do to comply with legal requirements. Because Pinot's data is immutable, a minion can't just delete rows in place: it downloads the relevant segments, removes the unwanted records, rewrites and reindexes the segments, and uploads them back into the system.

**Zookeeper** acts as the centralized metadata store and the communication mechanism between cluster nodes, holding cluster state, segment assignments, and metadata.

**Segment load, as a Helix state machine.** Helix manages cluster state via state machines: each resource has a current state and a desired state, and when the state changes Helix sends that change to the relevant nodes, which act on it to reach the desired state. A segment starts life `OFFLINE`. To bring it `ONLINE`, Helix instructs server nodes to fetch the segment from object storage based on the mapping, and the servers unpack and load it, becoming ready for query execution — Helix then marks it `ONLINE`. For real-time ingestion from Kafka, segments instead transition from `OFFLINE` to `CONSUMING` (see [[segment-completion-protocol]] for how that consumption gets finalized). Brokers listen for these cluster-state changes via Helix and update their own routing table and server-to-segment mapping accordingly.

**Data upload.** When new data needs to be uploaded, the controller loads the segment via an HTTP POST, unpacks it to verify data integrity, and checks whether the segment's size exceeds the table's quota. It then writes the segment's metadata to Zookeeper and updates cluster state, marking the segment `ONLINE` with the desired number of replicas.

*See also: [[apache-pinot]] · [[pinot-broker]] · [[segment-completion-protocol]] · [[immutable-segment]]*
