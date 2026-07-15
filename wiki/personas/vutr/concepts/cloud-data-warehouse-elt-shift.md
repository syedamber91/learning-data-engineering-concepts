---
persona: vutr
kind: concept
sources:
- raw/duckdb-polars-single-node-engines/why-single-node-engine-like-duckdb.md
last_updated: '2026-07-15'
qc: passed
slug: cloud-data-warehouse-elt-shift
topics:
- single-node-engines-duckdb-polars-vs-distributed-systems
---

Spark's rise happened alongside a second, related shift: the emergence of cloud data warehouses — BigQuery, Snowflake, Databricks (itself built from Spark), Redshift. Pay-as-you-go pricing models, cheaper storage, faster networks, and columnar storage/processing commoditized high-performance, cost-efficient warehouses in a way that hadn't existed before.

The claim worth being precise about: this emergence is credited as the main driver of the paradigm shift from ETL to ELT. Once transformation could happen cheaply and quickly inside the warehouse itself, people realized they didn't have to transform data *before* loading it — they could dump data straight from the source (with maybe some light processing), let the transformation happen later directly in the warehouse, and get a shiny warehouse running with just a few clicks, with most transformation logic now handled in SQL.

The user experience story is the same "vendors abstract infrastructure" pattern that shows up everywhere in this arc: vendors expose only minimal tuning knobs, and most of the time you don't need to manage a "cluster" the way you would with Spark or MapReduce — with the explicit exception of Redshift. Pay-as-you-go pricing also lets teams be more relaxed about provisioning up front compared to estimating cluster capacity ahead of time.

Still, the barrier to entry is lower here than for MapReduce or Spark, not zero. Three things don't go away: users must understand the specific pricing model (pay-as-you-go for *this* and pay-as-you-go for *that*) to keep billing reasonable; it's hard — close to impossible — to get a local development experience with these cloud data warehouses; and in some cases users still need to understand how the solution works behind the scenes to optimize cost and query performance.

*See also: [[spark-in-memory-model-and-overhead]] · [[single-node-engine-market-gap]]*
