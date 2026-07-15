---
persona: vutr
kind: entity
sources:
- raw/dbt-and-dimensional-modeling/why-is-dbt-so-popular.md
- raw/dbt-and-dimensional-modeling/how-to-learn-dbt-cheap-and-fast.md
- raw/dbt-and-dimensional-modeling/deep-dive-into-the-kimball-dimensional.md
last_updated: '2026-07-15'
qc: passed
slug: dbt
topics:
- dbt
---

dbt is a CLI tool that lets you transform data efficiently using SQL — Vu is emphatic that this is *all* it is: not an engine like Spark, not a database like Postgres or Snowflake, just a tool for managing SQL data transformation. It has two components, a compiler and a runner. You write dbt models, run a command in the terminal, and dbt compiles the model code into SQL statements and executes them against your data warehouse — Snowflake, BigQuery, Databricks, or an engine like Spark or Trino. dbt never loads your data and doesn't know its content beyond schema and metadata; everything happens inside the warehouse itself.

At dbt's core is the **model**: a SQL query saved in a `.sql` file, each one defining a transformation into a desired output. When dbt runs, it executes these queries and materializes the result as a table or view — giving the transformation logic a tangible, versioned form. A model's code is not pure SQL, though; it combines SQL with Jinja templating, and two special Jinja functions carry the tool's whole dependency model: `source()` lets a model reference a raw physical table in the warehouse, and `ref()` lets a model reference another dbt model. Chained together, these let dbt build a complete transformation lineage — the leftmost model points at a physical table via `source`, and every model downstream points at its predecessor via `ref` — which is also what lets dbt auto-generate documentation and a lineage graph, and what lets teams write modular, reusable model structures rather than one monolithic query.

Because a dbt model is fundamentally code, it inherits software-engineering workflow for free: it can be tracked in git, tested before a production run, rolled back to a previous version, and wired into CI/CD pipelines — the same discipline software engineers apply to application code, applied here to SQL transformation. In Vu's own multi-day Kimball-modeling project, dbt is the thing that turns hand-drafted SQL logic (staging views over wildcard BigQuery tables, incremental merge logic for SCD Type 2 dimensions, an `insert_overwrite` fact table) into something runnable, testable, and re-runnable per snapshot date via a `--vars` flag rather than hard-coded SQL edits — see [[dbt-incremental-strategies-for-scd]] for the mechanics.

*See also: [[dbt-origin-and-adoption]] · [[dimensional-modeling]] · [[elt-vs-etl]] · [[democratization-of-transformation]] · [[data-modeling-is-not-dbt-modeling]] · [[dbt-incremental-strategies-for-scd]] · [[star-schema]] · [[grain-declaration]] · [[surrogate-keys]] · [[scd-type-2]] · [[scd-type-1-and-3]]*
