---
persona: vutr
kind: concept
sources:
- raw/uber-data-infrastructure-case-studies/how-did-uber-build-their-data-infrastructure.md
- raw/uber-data-infrastructure-case-studies/i-spent-7-hours-understanding-ubers.md
last_updated: '2026-07-15'
qc: passed
slug: uber-presto-deployment-and-query-routing
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Presto is Uber's primary interactive query interface: 500K queries daily, over 50 PB of data, 9,000 daily active users, spread across 20 clusters totaling 7,000 nodes. Presto's own architecture is a coordinator that parses, analyzes, plans, and optimizes a query before dispatching it, and worker nodes that execute the resulting tasks against chunks of data in external storage — an MPP design that performs computation in memory rather than spilling intermediate results to disk, which is what makes it fast for interactive, large-scale analytical queries.

Around that, Uber added two of its own layers. The **client layer** covers internal dashboards, tools, and backend services that talk to Presto over JDBC. The **routing layer** sits in front of the Presto clusters as a load balancer, routing each query to a cluster based on live statistics like resource utilization and queue depth. To cut latency further, Uber implemented an **SSD-based cache** per worker node: when a worker needs data from an external system like HDFS, it first checks its local SSD cache — a hit reads locally, a miss makes the remote call and then caches the result for the next read.

The other major extension is the **Pinot connector**, built so Uber's real-time exploration needs could run standard PrestoSQL over Pinot data. The connector's job is deciding how much of the physical query plan can be pushed down into Pinot rather than executed in Presto itself. The first version was limited by the connector API to predicate pushdown alone; Uber then improved Presto's query planner and extended the Connector API so more operators — projection, aggregation, limit — could also be pushed down to Pinot. Each additional pushed-down operator lowers query latency and lets the query actually benefit from Pinot's own indexing, rather than pulling more raw data into Presto than necessary.

Uber also tried to collapse SQL fragmentation across the stack with **CommonSQL**: a unified syntax plus an internal SQL editor that talks to Presto (via the client layer) so users can iteratively refine a query before pushing it to production. The payoff is that one CommonSQL query can run directly on Pinot or Presto, or be converted into a Flink or Spark job — one query surface, several execution targets.

*See also: [[uber-data-platform]] · [[uber-pinot-upsert-mechanism]] · [[uber-flink-unified-platform]]*
