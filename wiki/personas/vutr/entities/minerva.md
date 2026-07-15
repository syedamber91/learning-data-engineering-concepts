---
persona: vutr
kind: entity
sources:
- raw/airbnb-data-infrastructure/how-did-airbnb-build-their-semantic.md
last_updated: '2026-07-15'
qc: passed
slug: minerva
topics:
- airbnb-data-infrastructure
---

Minerva is Airbnb's internal semantic layer platform — not a tool, but a complete platform covering a metric's whole life cycle. By the time Airbnb shared it publicly, Minerva contained more than 12,000 metrics and 4,000 dimensions, with 200+ data producers across different functions and teams, and was serving 5,000+ datasets across hundreds of users and 80+ teams.

Minerva was born from a trust problem, not a technology gap. Airbnb's core_data tables — the foundation for its experimentation platform, Dataportal catalog, Superset exploration, and Data University program — grew a sprawl of downstream tables with no way to tell whether an existing table already met a new requirement. Debugging data discrepancies ate hours, and different teams reported different numbers for the same business question, so decision-makers and even data scientists lost trust in the data. Airbnb's data engineering team first rebuilt core business data models into lean tables that eliminated redundant joins — but that alone wasn't enough, because users still needed to join those tables, backfill them when logic changed, and present them consistently across many consumption tools. Minerva is the platform built to close that gap: it takes fact and dimension tables as input, performs data denormalization, and serves the aggregated data through a unified API to downstream applications.

Architecturally, Minerva sits on open-source components: Airflow for orchestration, Hive and Spark for compute, and Presto and Druid for serving. For any given metric it covers definition (metrics, dimensions, and metadata live in a centralized GitHub repository anyone with permission can edit), review (a development flow with code review, static validation, and test runs before merge), computation (data aggregation and denormalization that reuses existing data assets and intermediate joined results), operations (automatic retry after job failures, plus built-in data-quality checks), a unified serving API, version-controlled change tracking that drives backfilling ([[minerva-data-versioning]]), data management (cost attribution, GDPR-based deletion, access control), and usage-based retention (infrequently used datasets can be deleted to save cost).

Airbnb designed Minerva against six named principles: standardized (metrics and dimensions, not tables and columns, are the unit of definition, with mandatory ownership/lineage/description metadata and Git-style code review for changes), declarative (users define the output they want — a "dimension set" — and Minerva handles the technical implementation, storage optimization, and reuse), scalable and highly available (detailed in [[minerva-backfill-and-staging-environment]]), consistent (detailed in [[minerva-data-versioning]]), and well-tested (a tool reads from production but writes to a sandbox, generating sample data on top of a user's local modifications and showing the step-by-step computation so users can validate and debug changes before merging, with configurable date ranges to keep test runs fast).

Minerva also anchors an ecosystem rather than standing alone. Dataportal indexes Minerva's metrics and dimensions so a metric search surfaces Minerva's results directly, and its Metric Explorer feature lets users see metric trends with Group By and Filter slicing before switching to Superset for deeper analysis. Airbnb migrated its A/B testing platform's proprietary metric repository into Minerva to achieve consistency between experimentation and analytics, built a reporting framework that turns user-specified Minerva metrics and dimensions into aggregated time series for executive reporting, and exposed Minerva through R and Python clients so data scientists get identical metric calculations in a notebook as in Metric Explorer — collapsing a common source of discrepancy-hunting.

*See also: [[minerva-data-versioning]] · [[minerva-backfill-and-staging-environment]] · [[airbnb-infrastructure-philosophy]] · [[airbnb-gold-silver-hadoop-clusters]]*
