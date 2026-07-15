---
persona: vutr
kind: entity
sources:
- raw/google-infrastructure/procella-the-query-engine-at-youtube.md
- raw/google-infrastructure/i-spent-5-hours-learning-how-google.md
last_updated: '2026-07-15'
qc: passed
slug: superluminal-execution-engine
topics:
- google-infrastructure
---

Superluminal is [[procella|Procella]]'s query evaluation engine, and it makes a deliberate bet against the industry-standard approach of LLVM-compiling each execution plan to native code. LLVM compilation gets fast steady-state execution, but the compile step itself costs time, and Procella has to serve both analytical queries and high-QPS, millisecond-latency lookups (embedded view/like counters) from the same engine — a compile pause that's negligible for a slow analytical query is unacceptable for a request that must return in milliseconds. Superluminal instead uses C++ template metaprogramming for code generation, ahead of the query itself, then processes data in blocks with vectorized, CPU-cache-aware algorithms, operating directly on encoded data (no separate decode step) and processing everything in a fully columnar fashion. It also pushes filters down to the scan node, so each column is only read for the rows a query actually needs rather than scanning full rows and discarding columns later.

Superluminal is not confined to Procella: the source notes it also powers Google BigQuery BI Engine and BigLake processing, and the BigLake material describes the [[bigquery-storage-api|BigQuery Storage Read API]] integrating Superluminal directly — using it to execute GoogleSQL expressions and operators with vectorized processing, apply user predicates and security filters, and handle data masking, before transcoding results into Apache Arrow for cross-engine interoperability. The same engine's role in accelerating the Spark BigQuery connector's Parquet reads is covered in [[spark-bigquery-connector-vectorized-parquet-read]]. That a single execution engine, first built for one YouTube system, resurfaces as shared infrastructure inside BigQuery's read path is one of the clearest signals in these posts of just how much internal reuse sits underneath Google's separately-branded products.

*See also: [[procella]] · [[artus-columnar-format]] · [[bigquery-storage-api]] · [[spark-bigquery-connector-vectorized-parquet-read]] · [[colossus-and-borg-as-shared-substrate]]*
