---
persona: vutr
kind: entity
sources:
- raw/google-infrastructure/procella-the-query-engine-at-youtube.md
last_updated: '2026-07-15'
qc: passed
slug: procella
topics:
- google-infrastructure
---

Procella is the SQL query engine YouTube built to unify four demands that used to each get their own dedicated system: reports and dashboards, embedded page statistics (view/like counters), time-series site-health monitoring, and ad-hoc analysis. Before Procella, YouTube ran Dremel for ad-hoc analytics, Bigtable for customer-facing dashboards, Monarch for site health, and Vitess for embedded statistics — a split that meant redundant ETL into multiple systems, a different query interface to learn per use case, and per-system performance ceilings. At the time the source paper was written, a single Procella deployment served hundreds of billions of daily queries.

The engine is built around four stated properties: a rich, nearly-complete standard-SQL surface; high scalability from separating compute and storage; high performance via state-of-the-art execution techniques (see [[superluminal-execution-engine]]); and data freshness across both batch and streaming ingestion. Architecturally, Procella is a set of specialized servers rather than one monolith. The Root Server (RS) accepts client SQL, rewrites/parses/plans it, consults the Metadata Server (MDS) to prune irrelevant data files, and builds the plan as a tree of query blocks connected by data streams; Data Servers (DS) execute pieces of that plan — reading source data from [[colossus-and-borg-as-shared-substrate|Colossus]] or from an in-memory buffer — and return results up the tree to the RS or a parent DS. Ingestion has its own split: a registration server handles offline/batch data (validating schema backward-compatibility, pruning and compacting schemas after a client's MapReduce job finishes), while a separate ingestion server handles real-time data arriving over RPC or PubSub, writing it to a Colossus write-ahead log and, in parallel, pushing it straight to the relevant data server's memory buffer — so a query can see data before it is durably compacted, trading a bit of consistency for near-real-time freshness (the buffer read path can be turned off if strict consistency is required instead). A compaction server periodically merges and repartitions those logs into larger columnar files, optionally applying user-defined SQL logic (filtering, aggregation, latest-value dedup) supplied at table-registration time.

Procella stores table data in its own columnar format, Artus (see [[artus-columnar-format]]), though it can also read Capacitor (the format Dremel uses). Because compute and storage are separated onto Colossus and Borg respectively, Procella inherits both the durability of Colossus (immutable files, RPC-only access, slower metadata operations) and the instability of Borg (machines torn down for maintenance, unpredictable per-task performance from incomplete isolation) — which is exactly why the engine invests so heavily in caching ([[procella-caching-and-affinity-scheduling]]), tail-latency defenses ([[procella-tail-latency-mitigation]]), and a dedicated high-QPS "stats serving" mode for the embedded-statistics use case ([[procella-stats-serving-mode]]). Distributed joins are chosen per-query from five strategies — broadcast, co-partitioned, shuffle, pipelined, and remote lookup — described in [[procella-distributed-join-strategies]].

*See also: [[artus-columnar-format]] · [[superluminal-execution-engine]] · [[colossus-and-borg-as-shared-substrate]] · [[procella-caching-and-affinity-scheduling]] · [[procella-distributed-join-strategies]] · [[procella-tail-latency-mitigation]] · [[procella-stats-serving-mode]]*
