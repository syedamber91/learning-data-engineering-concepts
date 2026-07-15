---
persona: vutr
kind: entity
sources:
- raw/history-of-data-engineering-and-hadoop-ecosystem/8-minutes-to-understand-presto.md
- raw/history-of-data-engineering-and-hadoop-ecosystem/the-history-of-data-engineering.md
last_updated: '2026-07-15'
qc: passed
slug: presto
topics:
- history-of-data-engineering
---

Apache Spark, first developed in 2012, addressed the limitations of MapReduce for data processing; a robust query engine operating over vast amounts of unseen data has enough advantages that other players chased the same idea from different angles — BigQuery runs its Dremel engine over Colossus, Snowflake runs a set of workers over S3, and in 2012 Facebook developed its own interactive SQL query engine with the same vision: Presto, pitched as "SQL on everything." Facebook built it to address the growing need to extract insights from large amounts of data and to make SQL analytics accessible to more people across the organization. By late 2018, Facebook's data professionals used Presto for most SQL analytic workloads, spanning interactive/BI queries and long-running batch ETL jobs, processing hundreds of petabytes and quadrillions of rows daily. Documented Facebook use cases include interactive analytics (engineers and data scientists testing hypotheses and building dashboards), batch ETL (migrating users off legacy batch systems), A/B testing (joining large datasets for experiment and population data), and developer/advertiser analytics (powering tools like Facebook Analytics for external developers and advertisers).

**History and the Presto/Trino split.** Facebook started developing Presto in 2012 and open-sourced it in 2013. In 2014, Netflix reported using it on 10 petabytes of S3 data. In 2016, Amazon built its Athena service on top of Presto. In 2017, Starburst Data was founded to support Presto commercially. In 2018, the original Presto developers left Facebook over a policy change that gave Facebook committers more privilege to commit changes than the wider open-source community. In 2019, development forked into PrestoDB, maintained by Facebook, and PrestoSQL, maintained by the newly formed Presto Software Foundation; that same year Facebook donated PrestoDB to the Linux Foundation. In December 2020, PrestoSQL was rebranded as Trino, because Facebook had obtained a trademark on the name "Presto."

**Architecture.** A Presto cluster splits into a coordinator node, which parses, plans, and orchestrates queries, and worker nodes, which execute them. A typical query flow: the client sends an HTTP request with the SQL statement to the coordinator; the coordinator parses and analyzes the SQL, then creates and optimizes an execution plan and sends it to the workers; workers execute tasks operating on splits — chunks of data from an external storage system — taking as input either remote splits or intermediate results from upstream workers, and storing intermediate data in memory as much as possible (see [[presto-coordinator-worker-scheduling]] for the scheduling mechanics, [[presto-resource-management-and-fault-tolerance]] for how the cluster shares CPU/memory and survives failures, and [[presto-columnar-execution-optimizations]] for how it processes data efficiently once a task is running).

Facebook designed Presto for extensibility from the start via a plugin interface, letting users customize data types, functions, access control implementations, queuing policies, and connectors — a connector lets Presto talk to an external data store through four API surfaces: Metadata, Data Location, Data Source, and Data Sink. On the SQL side, Presto adheres to ANSI SQL for broad compatibility while adding extensions like lambda expressions and higher-order functions to make complex types (maps, arrays) more usable. Clients can reach Presto through a RESTful HTTP interface, a command-line interface, or a JDBC client compatible with BI tools like Tableau.

*See also: [[hadoop-mapreduce]] · [[apache-hive]] · [[presto-coordinator-worker-scheduling]] · [[presto-resource-management-and-fault-tolerance]] · [[presto-columnar-execution-optimizations]]*

## Related in the other wiki
- [[Parallel Query Execution]] — DDIA's account of MPP databases decomposing a join-filter-aggregate query into stages that run in parallel across partitions is the general pattern Presto's coordinator/worker split and stage-based execution instantiate concretely.
- [[Beyond MapReduce]] — DDIA's survey of declarative, cost-optimized alternatives to raw MapReduce is the same territory Presto (and its predecessor Hive) occupy from the SQL-engine side.
