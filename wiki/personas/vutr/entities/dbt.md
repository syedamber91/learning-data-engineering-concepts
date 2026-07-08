---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: dbt
topics:
- dbt
---

dbt is a CLI tool that compiles SQL + Jinja models and runs them on your data warehouse — that's it. It's not an engine like Spark and not a database like Postgres or Snowflake; source() references raw tables and ref() references other dbt models, but dbt itself never loads data or knows its content.

*See also: [[star-schema]] · [[grain-declaration]] · [[surrogate-keys]] · [[scd-type-2]] · [[scd-type-1-and-3]] · [[dbt-origin-and-adoption]]*
