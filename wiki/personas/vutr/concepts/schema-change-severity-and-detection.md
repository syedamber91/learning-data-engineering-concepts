---
persona: vutr
kind: concept
sources:
- raw/change-data-capture-cdc-and-data-sourcing-additional/data-engineering-system-design-11.md
last_updated: '2026-07-15'
qc: passed
slug: schema-change-severity-and-detection
topics:
- change-data-capture-cdc-and-data-sourcing
---

Knowing the source's schema today is, in Vu's words, only 50% of the story — schemas change without warning, and the default failure sequence is: the source team changes the schema, your pipeline fails, you violate the business SLA, and only then do you learn what happened. He ranks schema changes by severity. Additive changes (a new column) are usually safe, since existing queries that don't `SELECT *` simply ignore the new field. Rename or drop breaks any query that references the affected column directly. A type change breaks casts, comparisons, or ordering — his example is that ordering number-like strings produces a different result than ordering actual numbers. The hardest to catch is a semantic change: the column keeps its name and type, but its meaning shifts underneath you. This is the quiet failure — it usually surfaces only when a dashboard shows a weird trend, long after the change actually happened.

To prepare for these, Vu lists four concrete defenses: a schema registry (Confluent, AWS Glue) for streaming sources, where producers register their schema and compatibility rules reject incompatible changes at publish time; selective reads (`SELECT specific_columns` instead of `SELECT *`), which insulates you from columns the source adds or drops that you never needed anyway; validation at ingestion time, checking the incoming schema against what you expect (he notes dbt can do this); and an official channel for changes — third-party sources usually publish a changelog, and for internal sources, the fix is a standing arrangement with the source team to be notified before schema-affecting changes ship.

*See also: [[cdc-operational-considerations]] · [[data-quality-contract-with-source]] · [[source-access-trust-boundary]]*
