---
persona: vutr
kind: concept
sources:
- raw/lakehouse-architecture-and-practical-builds/the-6-questions-you-must-answer-when.md
last_updated: '2026-07-15'
qc: passed
slug: lakehouse-build-decision-framework
topics:
- data-architecture-warehouse-lake-lakehouse-mesh-lambda-kappa
---

Vu's framework for building a [[lakehouse]] from scratch, with no vendor doing the work behind the scenes, is organized around six questions he says every builder must answer, deliberately staying tool-agnostic in his own writing so the framework transfers across stacks.

**1. Which table format(s)?** He calls this the single most important decision, because BigQuery and Snowflake already prove the alternative is viable: both decouple compute from storage (S3 for Snowflake, Colossus for BigQuery) behind a vendor-controlled metadata/translation layer that handles ACID, versioning, time travel, and access control invisibly. Choosing to self-manage that translation layer means picking among Delta Lake, Iceberg, or Hudi (or newer entrants like DuckLake or Apache Paimon) — see [[lakehouse-metadata-layer-as-translator]] — evaluated against concrete business requirements (schema evolution needs, fine-grained access control, real-time ingestion, concurrency, daily data volume), never by reputation alone.

**2. Which query engine(s)?** Because a lakehouse separates the query engine from storage in principle, it's tempting to treat this as an independent choice — but Vu insists the two decisions must be evaluated together, since a table format's *maturity* of support differs sharply by engine (his example: a format can work great with Spark and be "another story" with Flink).

**3. How do you manage the storage layout?** Self-managing a lakehouse means also managing the physical file layout, which Vu frames through Spider-Man's "with great power comes great responsibility." Two levers: colocation (partitioning splits the table into physical portions so an engine touches only what it needs; clustering — sorting or z-ordering — groups related records more finely but needs continuous re-arrangement as new data lands only locally sorted, not globally) and file-size control (smaller files write faster and use less write-side memory, but read operations suffer from opening/closing many small files, which is why formats and engines expose a compaction process to rebalance file size without breaking read/write integrity).

**4. How do you manage table-format metadata?** The translator layer itself — see [[lakehouse-metadata-layer-as-translator]] — accumulates metadata files over the life of the lakehouse, and Vu warns that an unmanaged metadata layer becomes its own performance bottleneck; there must be a deliberate strategy (frequency, target size) for keeping the metadata file count under control, the same way data-file compaction needs one.

**5. How do you manage access control?** Vendors like BigQuery and Snowflake let you set security policy through a UI; self-managing means deciding for yourself whether users can bypass the table format entirely and query object storage directly, choosing between access rules and credential vending (temporary credentials), choosing RBAC and/or ABAC, building activity/access logging for incident detection, and protecting PII — all without a vendor's out-of-the-box tooling.

**6. What about user/developer experience?** Vu's blunt framing: "You build a fancy data lakehouse, but only you and your team understand how to interact with it... your lakehouse adds no value." This covers three sub-problems: discoverability (search, business glossaries, lineage — typically requiring integration with a tool like DataHub or OpenMetadata), local development (letting users iterate on pipelines on their own laptop, e.g. via local-friendly engines like Polars or DuckDB, though syntax can mismatch across environments), and UI/UX (an SQL editor, table browser, job monitor, permission granting — the kind of polish vendors like BigQuery, Snowflake, and Databricks have invested heavily in, and that self-builders must replicate with a dedicated web-app effort).

Vu's own closing synthesis is that answering all six well, from zero, is highly resource-intensive — see [[every-decision-has-a-tradeoff]] for how he resolves that into a recommendation to hand parts of the stack to vendors unless the organization has the scale and diverse requirements to justify full self-management.

*See also: [[lakehouse]] · [[lakehouse-metadata-layer-as-translator]] · [[lakehouse-query-performance-techniques]] · [[trino]] · [[project-nessie]] · [[every-decision-has-a-tradeoff]]*
