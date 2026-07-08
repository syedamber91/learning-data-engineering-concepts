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
