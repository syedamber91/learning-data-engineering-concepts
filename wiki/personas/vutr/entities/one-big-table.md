---
persona: vutr
kind: entity
sources:
- raw/dbt-and-dimensional-modeling/dimensional-modeling-overview.md
last_updated: '2026-07-15'
qc: passed
slug: one-big-table
topics:
- dbt
---

Vu's own experience with One Big Table (OBT) is that it proves its value only when there's a careful data modeling layer already sitting beneath it. Putting all the data into a single table from the outset trades away data understandability for query performance — a trade he calls "terrible" when it's made in place of doing the modeling work.

He connects this to a broader observation about cloud data warehouses: platforms like BigQuery encourage denormalizing with nested or array fields specifically to avoid joins and improve performance. His concern is that this indirectly teaches people that joins are inherently bad — and since proper data modeling requires organizing information where it belongs (which, at query time, requires joins), people extend that belief into thinking data modeling itself is bad for query performance. His counter-evidence: BigQuery, Snowflake, and Databricks have all introduced Primary Key and Foreign Key constructs in recent years, along with techniques to optimize joins that use them — in his reading, these platforms are actively encouraging users to set these constraints and organize their data properly, not to abandon structure in favor of one flat table.

*See also: [[star-schema]] · [[grain-declaration]] · [[surrogate-keys]] · [[dbt]] · [[scd-type-2]] · [[scd-type-1-and-3]] · [[data-modeling-is-not-dbt-modeling]] · [[dimensional-modeling]]*
