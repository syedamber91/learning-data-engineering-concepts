---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: dbt
---

Related: [[star-schema]] · [[grain-declaration]] · [[surrogate-keys]] · [[scd-type-2]] · [[scd-type-1-and-3]] · [[dbt]] · [[medallion-architecture]] · [[one-big-table]] · [[dbt-origin-and-adoption]] · [[semantic-layer-over-a-mess]] · [[dimensional-modeling]] · [[elt-vs-etl]] · [[data-modeling-is-not-dbt-modeling]] · [[democratization-of-transformation]]

## Comparisons
**[[scd-type-2]] vs [[scd-type-1-and-3]]** — Type 2 is what I reach for by default: it preserves history by inserting a new row with start_date/end_date. Type 1 overwrites and keeps no history; Type 3 adds columns for a prior value but is rarely worth it since a LAG window function over a Type 2 table does the same in modern SQL. The higher types (5-7) are hybrids I don't see adopted in real life — in the end they're just labels.

**[[elt-vs-etl]]** — ETL made sense in the 1970s when storage and compute were expensive and coupled, so you curated a small subset before loading. Cheaper storage and more powerful SQL OLAP systems pushed transformation *inside* the warehouse (ELT), letting you keep raw data and evolve transformation logic. But ELT will not completely replace ETL — there are still cases where ETL is necessary.

**[[dbt]] vs [[data-modeling-is-not-dbt-modeling]]** — dbt is a great transformation tool (Jinja + SQL, trackable, roll-back-able, CI/CD-friendly), and its [[dbt-origin-and-adoption|explosive adoption since Tristan Handy built it in 2016]] drove a real [[democratization-of-transformation]] — but writing dbt models is *not* data modeling. dbt shapes data; a data model — tool-agnostic — defines how data is structured and related. Likewise, don't confuse [[medallion-architecture]] layers or a [[semantic-layer-over-a-mess|semantic layer]] with the modeling work itself.

**[[star-schema]] vs [[one-big-table]]** — a properly modeled star schema keeps understandability; OBT trades that away for query performance and only pays off when a careful modeling layer sits beneath it.

## Open questions
- Which specific cases still make ETL necessary rather than ELT, now that transformation has largely moved inside the warehouse?
- When is One Big Table actually the right choice, given it only proves its value with a careful data modeling layer beneath it?
- If a [[semantic-layer-over-a-mess|semantic layer]] over an existing mess just yields another mess, what has to be fixed in the modeling layer first before one is introduced?
- How far does the [[democratization-of-transformation]] via [[dbt]] go before the lack of a real data model starts to hurt — where's the line between enabling analysts and belittling modeling?

## Synthesis
Kimball's [[dimensional-modeling]] — grain first, then a denormalized [[star-schema]] with [[surrogate-keys]] and patterns like [[scd-type-2]] — exists to facilitate communication and guide how we serve data, not merely to make queries fast. The shift to [[elt-vs-etl]] and the rise of [[dbt]] — [[dbt-origin-and-adoption|created by Tristan Handy in 2016 and grown from 3 companies to 9,000+ by 2022]] — drove a [[democratization-of-transformation]], letting SQL-literate analysts write logic that once needed robust coding and enabling DEs and DAs to collaborate rather than replacing engineers. But cheap, democratized pipelines solve a different problem than modeling does: as I keep insisting in [[data-modeling-is-not-dbt-modeling]], a tool-agnostic data model is not a SQL script, and neither [[medallion-architecture]] layers, [[one-big-table]], nor a [[semantic-layer-over-a-mess|semantic layer]] can substitute for the modeling layer beneath them — a layer thrown over a mess just yields another mess.

## Related topics
- [[data-architecture-warehouse-lake-lakehouse-mesh-lambda-kappa]] — The medallion architecture and ELT-vs-ETL debate are shared ground — dbt drives the in-warehouse transformation that the lakehouse enables.
- [[data-engineering-career-roadmap-and-learning-philosophy]] — The roadmap front-loads data modeling as a fundamental, and Vu's insistence that dbt modeling is not data modeling is the same warning against confusing tools with the durable craft.
- [[sql-fundamentals-and-execution-model]] — dbt is Jinja + SQL that pushes transformation inside the warehouse, so its models are ultimately SQL execution that everybody in the data world speaks.
