---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: data-modeling-is-not-dbt-modeling
topics:
- dbt
---

Many people think writing dbt models is doing data modeling — that's wrong. A data model defines how data is structured and related, ensuring consistency, and is tool-agnostic; a dbt model is just a SQL-based transformation script that shapes raw data inside the warehouse. In an era where people belittle data modeling to move fast, I've learned that throwing more resources at a slow, messy query won't fix it.

*See also: [[star-schema]] · [[grain-declaration]] · [[surrogate-keys]] · [[dbt]] · [[scd-type-2]] · [[scd-type-1-and-3]]*
