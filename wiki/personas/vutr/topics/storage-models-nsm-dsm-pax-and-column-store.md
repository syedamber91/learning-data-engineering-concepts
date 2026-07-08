---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: storage-models-nsm-dsm-pax-and-column-store
---

Related: [[nsm]] · [[dsm]] · [[pax-hybrid-layout]] · [[clickhouse]] · [[redshift]] · [[parquet]] · [[oltp-vs-olap-access]]

## Comparisons
Three storage models sit on a spectrum from row-oriented to fully column-oriented:

- [[nsm]] (row store) keeps a full record together — great for OLTP insertion and mutation, but poor at compression because columns don't share patterns.
- [[pax-hybrid-layout]] is the hybrid middle ground: horizontal row groups first, columns stored together within each group. [[parquet]] (and ORC), BigQuery, Snowflake, and DuckDB all live here — the systems that *say* [[pax-hybrid-layout]] but are really PAX.
- [[dsm]] is the true column store: each column stored completely separately, offsets computed arithmetically. Only [[clickhouse]] and [[redshift]] were found to do this.

The cleanest contrast is [[clickhouse]] vs [[parquet]]: ClickHouse *only* splits vertically (pure [[dsm]]), while Parquet-style formats horizontally partition into row groups before storing columns together ([[pax-hybrid-layout]]).

## Open questions
- If [[pax-hybrid-layout]] dominates real-world 'column stores', what concrete workloads make true [[dsm]] in [[clickhouse]] and [[redshift]] worth the trade-off?
- Why do so few products commit to true [[dsm]] — is horizontal row-grouping in [[pax-hybrid-layout]] a compression, pruning, or I/O advantage?
- How do the OLAP pruning techniques (Zone Maps, partitioning, Z-ordering) interact differently with [[pax-hybrid-layout]] row groups versus [[dsm]]'s fully separate columns?
- Does [[nsm]]'s weak compression fully disqualify it from analytical use, or are there hybrid setups worth exploring?

## Synthesis
The headline is that [[pax-hybrid-layout]] is a leaky label: most systems calling themselves columnar actually run [[pax-hybrid-layout]] (horizontal row groups, then columns stored together), not the true [[dsm]] where each column lives completely separately. [[parquet]], BigQuery, Snowflake, and DuckDB are all PAX; only [[clickhouse]] and [[redshift]] were found to implement genuine DSM. This all traces back to [[oltp-vs-olap-access]] — [[nsm]] wins for fast record lookup, while the analytical camp optimizes for pruning — so the practical takeaway ([[pax-hybrid-layout]]) is to always ask which model a product truly uses before trusting the 'columnar' claim.

## Related topics
- [[apache-pinot-druid-and-real-time-olap]] — Pinot and Druid store data as immutable columnar segments, an application of the DSM/column-store storage model for fast analytical scans.
- [[data-engineering-career-roadmap-and-learning-philosophy]] — The roadmap cites 'columnar always performs better for analytical reads' as a fundamental that never becomes obsolete — the core claim of the storage-models note.
- [[lsm-tree-storage-engines]] — LSM-trees and the NSM/DSM/PAX models are the two axes of physical storage design — write path versus column layout — that OLAP engines combine.
- [[olap-engine-internals-bigquery-snowflake-clickhouse-redshift-duckdb-databricks]] — The engines split on storage layout — ClickHouse and Redshift are true DSM while BigQuery, Snowflake, and DuckDB use PAX — the exact taxonomy of the storage-models note.
- [[parquet]] — Parquet is a PAX-hybrid layout — row-groups first, then columnar — the leaky 'columnar' label the storage-models note dissects.
- [[sql-fundamentals-and-execution-model]] — OLTP-vs-OLAP access is the shared hinge — a map-like lookup serves OLTP while scan-and-summarize OLAP drives the columnar storage choice.
