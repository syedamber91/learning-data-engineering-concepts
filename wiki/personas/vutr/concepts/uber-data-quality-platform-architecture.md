---
persona: vutr
kind: concept
sources:
- raw/uber-data-infrastructure-case-studies/i-spent-3-hours-learning-how-uber.md
last_updated: '2026-07-15'
qc: passed
slug: uber-data-quality-platform-architecture
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Uber's consolidated data quality platform is organized around one shared engine and five components built on top of it: Test Generator, Test Execution Engine, Alert Generator, Incident Manager, and Consumption Tools. The **Test Execution Engine** is the shared foundation — a Celery-based web service that runs roughly 100,000 daily executions across about 18,000 tests, on schedule or on demand, storing results in databases. It works because every test — whichever of the standard [[uber-data-quality-standardization|test categories]] it is, or a user-defined one — reduces to one of a small number of logical assertions, most commonly "compare a computed value to a constant" or "compare one computed value to another computed value." Uber encodes each test as an **expression string** representing a flattened Abstract Syntax Tree (AST) with parameters controlling execution; at run time that string is parsed back into a tree and evaluated via post-order traversal, so any test — however it originated — is processed through the same execution path.

The **Test Generator** auto-generates the standard tests using a dataset's own metadata pulled from Uber's centralized metadata service — SLAs, partition keys (so large tables only test their latest partition), and primary keys. It also auto-generates tests across a dataset's upstream and downstream tables by consuming Uber's internal lineage service; a daily Spark job refreshes that lineage and, with it, regenerates the auto-generated test definitions whenever the underlying metadata changes.

The **Alert Generator** turns test results into alerts, filled out with extra metadata from the metadata service like table owners or alert emails, generated per dataset per test category. Two mechanisms exist specifically to prevent alert fatigue: a **sustained period** — e.g. if a table's SLA tolerates 3 hours of test failures, the platform marks status as WARN rather than alerting until failures exceed that window — and a **dependency rule**, since one root cause (e.g. late-arriving data) can otherwise trigger multiple category alerts simultaneously (Freshness, Completeness, and Cross-datacenter Consistency all firing for the same underlying delay); Uber defaults Freshness as a dependency of the other categories so the redundant alerts get suppressed.

The **Incident Manager** closes the loop after a user has investigated and mitigated an issue: an internal scheduler automatically reruns failed tests with exponential backoff, and if the same test passes again, the incident resolves itself with no manual intervention. Uber also lets users manually annotate an incident and trigger a rerun, and lets them report incidents they notice while consuming data — the platform checks reported incidents for overlap with auto-detected ones and notifies data producers to acknowledge them, aggregating both auto-detected and user-reported incidents into one final quality status.

Finally, **Consumption Tools** surface all of this to users: Databook is the centralized metadata dashboard, now showing data quality results directly in its UI; the Query Runner tool (which can query MySQL, Postgres, or Hive) integrates with the quality platform so a query's dataset name and time range can be checked against ongoing incidents; the ETL Manager — the controller for all of Uber's pipelines — can trigger a fresh test execution the moment a pipeline finishes, and can also refuse to run a pipeline at all if an input dataset's quality fails its SLA; and Uber's metric platform, which defines and serves business metrics from raw datasets, is integrated closely enough with the quality platform that metrics themselves get standard tests and metric-level quality surfaces through the metric platform's own query layer.

*See also: [[uber-data-quality-standardization]] · [[uber-hudi-etl-pipeline-and-impact]]*
