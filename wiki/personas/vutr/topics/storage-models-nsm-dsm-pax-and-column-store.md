---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: storage-models-nsm-dsm-pax-and-column-store
---

Related: [[nsm]] · [[dsm]] · [[pax]] · [[column-store]] · [[clickhouse]] · [[redshift]] · [[parquet]] · [[oltp-vs-olap-access]] · [[pax-vs-dsm-distinction]]

## Comparisons
Three storage models sit on a spectrum from row-oriented to fully column-oriented:

- [[nsm]] (row store) keeps a full record together — great for OLTP insertion and mutation, but poor at compression because columns don't share patterns.
- [[pax]] is the hybrid middle ground: horizontal row groups first, columns stored together within each group. [[parquet]] (and ORC), BigQuery, Snowflake, and DuckDB all live here — the systems that *say* [[column-store]] but are really PAX.
- [[dsm]] is the true column store: each column stored completely separately, offsets computed arithmetically. Only [[clickhouse]] and [[redshift]] were found to do this.

The cleanest contrast is [[clickhouse]] vs [[parquet]]: ClickHouse *only* splits vertically (pure [[dsm]]), while Parquet-style formats horizontally partition into row groups before storing columns together ([[pax]]).

## Open questions
- If [[pax]] dominates real-world 'column stores', what concrete workloads make true [[dsm]] in [[clickhouse]] and [[redshift]] worth the trade-off?
- Why do so few products commit to true [[dsm]] — is horizontal row-grouping in [[pax]] a compression, pruning, or I/O advantage?
- How do the OLAP pruning techniques (Zone Maps, partitioning, Z-ordering) interact differently with [[pax]] row groups versus [[dsm]]'s fully separate columns?
- Does [[nsm]]'s weak compression fully disqualify it from analytical use, or are there hybrid setups worth exploring?

## Synthesis
The headline is that [[column-store]] is a leaky label: most systems calling themselves columnar actually run [[pax]] (horizontal row groups, then columns stored together), not the true [[dsm]] where each column lives completely separately. [[parquet]], BigQuery, Snowflake, and DuckDB are all PAX; only [[clickhouse]] and [[redshift]] were found to implement genuine DSM. This all traces back to [[oltp-vs-olap-access]] — [[nsm]] wins for fast record lookup, while the analytical camp optimizes for pruning — so the practical takeaway ([[pax-vs-dsm-distinction]]) is to always ask which model a product truly uses before trusting the 'columnar' claim.
