---
persona: vutr
kind: entity
sources:
- raw/dbt-and-dimensional-modeling/dimensional-modeling-overview.md
- raw/dbt-and-dimensional-modeling/deep-dive-into-the-kimball-dimensional.md
- raw/dbt-and-dimensional-modeling/i-spent-6-hours-learning-about-slowly.md
last_updated: '2026-07-15'
qc: passed
slug: grain-declaration
topics:
- dbt
---

The grain is the level of detail a single fact-table row represents — are you tracking individual transactions, daily summaries, or monthly aggregates? — and every row in a fact table must sit at that same grain. Vu treats declaring it as the second of Kimball's four design steps (after selecting the business process, before identifying dimensions or facts), and as foundational precisely because it has to be settled before either of the following steps can be done sensibly: you cannot choose which dimensions matter, or which measures to capture, until you know what a single row of the fact table actually represents.

In his own hands-on project, the grain decision is concrete: `fact_sale` is declared at the order level, so each row records one order's date, order number, revenue, cost, and profit, plus foreign keys to `dim_product` and `dim_territories`. That single, explicit grain is what lets every measure on the row — and every join out to a dimension — mean the same thing consistently across the whole table.

*See also: [[star-schema]] · [[surrogate-keys]] · [[dbt]] · [[scd-type-2]] · [[scd-type-1-and-3]] · [[dbt-origin-and-adoption]] · [[dimensional-modeling]]*
