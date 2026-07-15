---
persona: vutr
kind: concept
sources:
- raw/cloud-kubernetes-docker-infrastructure-tooling/i-spent-6-hours-learning-aws-glue.md
last_updated: '2026-07-15'
qc: passed
slug: glue-dynamicframe-and-schema-inference
topics:
- cloud-kubernetes-docker-infrastructure-tooling
---

When [[aws-glue|Glue]] was first built, most query engines — including Spark — needed a schema known before they could work with a dataset. That's easy for self-describing formats like Avro or Parquet, which can expose their schema without a full read, and hard for JSON, which requires scanning the entire dataset just to know its shape. Glue's answer was a new data structure, the **DynamicFrame**: rather than requiring a schema upfront, it embeds schema metadata directly in each record and only infers a global schema when one is actually needed. Structurally, a DynamicFrame is still stored as a Spark RDD, but of `DynamicRecord`s — each one a tree-based structure carrying both column metadata and values, and constructible from Avro, CSV, JSON, Parquet, or JDBC-sourced relational data.

DynamicFrames support the standard transformations (selection, projection, Python/Scala UDFs) plus ones purpose-built for deeply nested data, but the source is explicit about their ceiling: they lack the advanced analytics capability of Spark DataFrames, such as joins or complex aggregations. The typical Glue pattern reflects that split — read and filter with a DynamicFrame, then convert to a DataFrame for anything heavier.

The schema-inference process itself goes further than plain Spark's approach. Glue inspects every record and unifies the structures it finds — field names and types alike — across the whole dataset, and it introduces a special **union type** that records every possible type a field might take, including null, absence of a value, or an outright type conflict between records. That flexibility is what lets Glue build one coherent schema out of genuinely messy, schema-less JSON without simply failing on the first inconsistency it meets.

Schema flexibility on the read side created a real problem on the write side: the Parquet format itself needs its schema known before writing, which is exactly what DynamicFrames were built to avoid needing upfront. The **Glue Parquet Writer**, introduced in 2019, resolves this by building the first row group incrementally in memory — dynamically creating columns and setting Parquet's definition/repetition levels as new fields are actually encountered in the data — and only flushing that first row group (thereby fixing the file's schema) once the in-memory buffer passes a default 128MB threshold. Any new field discovered in the data *after* that point triggers a new output file with its own, updated schema, rather than retroactively rewriting the first — which is also why downstream engines like Spark sometimes need configuration adjustments to correctly read a collection of Glue-written Parquet files whose schemas differ file to file.

*See also: [[aws-glue]] · [[glue-serverless-execution-evolution]] · [[glue-data-catalog-and-crawlers]]*
