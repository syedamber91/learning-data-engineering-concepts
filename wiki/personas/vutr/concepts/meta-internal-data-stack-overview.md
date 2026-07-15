---
persona: vutr
kind: concept
sources:
- raw/meta-data-stack-and-infrastructure/groupby-44-meta-the-data-stack.md
last_updated: '2026-07-15'
qc: passed
slug: meta-internal-data-stack-overview
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Meta's internal data stack is best understood as one company's answer to the same question every planet-scale operation (the source names Twitter and LinkedIn too) has to answer eventually: how engineers safely query, monitor, and productionize data once off-the-shelf tooling stops being an option. The warehouse itself holds millions of Hive tables, physically stored using an internal fork of ORC, and is divided into namespaces — either geographic or logical partitions of the warehouse — so tables queried together sit in the same namespace without data having to move; when two namespaces both need a table, Meta pays for it with replication instead. Retention is deliberately finite: tables carry a set period (the source's example is 90 days), after which data is archived or deleted, and every table is tied to an on-call group responsible for it. Data lands in the warehouse from three paths: snapshots of operational (graph) databases, logs from clients and servers, and the Dataswarm pipeline layer pulling from other warehouse tables.

Querying that warehouse means picking between Presto and Spark, and the choice is a workload call, not a preference: Presto handles most day-to-day ad hoc queries, scanning billions of rows in seconds to minutes, while Spark takes the heavier workloads needing more memory or complex joins, with Spark's Java/Scala/Python APIs used directly for the most complex transformations rather than SQL. Around that querying layer sit a set of purpose-built tools: [[scuba]] for real-time analytics on live logging data, used by both data and software engineers analyzing trends and by production engineers debugging live issues; Daiquery as the single web-based notebook entry point across the warehouse (via Presto or Spark), Scuba, and other sources, with Bento — Meta's managed Jupyter implementation supporting Python or R — as the upgrade path for more complex analysis; and Unidash as the dashboarding layer, integrated directly with Daiquery so a query and its chart can be exported straight into a dashboard.

Pipeline development follows a specific pattern: business logic in SQL, wrapped in Python for orchestration and scheduling via Dataswarm, Meta's internal library and the direct predecessor to Apache Airflow. Monitoring that orchestration runs through CDM (Central Data Manager), a web tool the source describes as "the Dataswarm UI" — the single entry point for finding failing tasks and their logs, defining and running backfills, navigating upstream dependencies and blockers, and setting up data-quality checks. Even the software-engineering environment is bespoke: most engineers use a customized VS Code fork, source control runs on an internal fork of Mercurial rather than Git, and the entire data-pipeline codebase lives in one monorepo. None of this is presented as necessarily better than the equivalent open-source stack — it's what an organization ends up building when its scale outpaces off-the-shelf tooling, the same organizational pressure that the [[shared-foundations-consolidation|Shared Foundations program]] was later a more deliberate response to.

*See also: [[scuba]] · [[shared-foundations-consolidation]]*
