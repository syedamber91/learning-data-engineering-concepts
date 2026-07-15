---
persona: vutr
kind: entity
sources:
- raw/big-tech-case-studies-batch-1-spotify-twitter-facebook-discord-notion/how-did-discord-evolve-to-handle.md
last_updated: '2026-07-15'
qc: passed
slug: discord-derived-dag-system
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Derived is Discord's in-house data transformation system, introduced in a 2021 article, built to turn petabytes of raw data into BigQuery tables while maintaining a complex DAG of precomputed data. A "derived table" at Discord is a SQL SELECT statement referencing raw data or other derived tables as its predecessors in the DAG; users define these in YAML configuration files that also carry refresh frequency, schema, description, update strategy, update schedule, date range, and BigQuery-specific optimizations like cluster columns or partition schemes. Derived's design requirements, per the notes, included: users only need to know SQL; the system infers the DAG automatically from the SQL rather than requiring users to declare dependencies; production configuration lives in Git; the system integrates with Discord's existing privatization and data-governance systems; metadata is exposed for monitoring, lineage, and performance tooling; and backfilling must not be complex.

Operationally, Derived used a CLI to load table configurations and validate DAG-wide dependencies during development, and to spin up test tables against shadow production data; a pull request triggered CI to deploy new tables into a shadow production environment (a mimic of production) so changes could be validated against real data before merging. Job scheduling, visualization, and monitoring ran on Airflow, and each transformation run deployed as its own Kubernetes pod. Table metadata was stored in a dedicated log store, queryable via BigQuery and joinable with BigQuery's own information schema for details like bytes processed and slot usage. Derived served Discord well early on, but the notes describe it as eventually limited in usability and flexibility for more complex use cases — the gap that led to the Dagster + dbt rebuild (see [[discord-declarative-vs-imperative-orchestration]]).

*See also: [[discord-declarative-vs-imperative-orchestration]] · [[dbt-incremental-race-condition]]*
