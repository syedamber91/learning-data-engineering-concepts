---
persona: vutr
kind: concept
sources:
- raw/google-infrastructure/i-spent-5-hours-learning-how-google.md
last_updated: '2026-07-15'
qc: passed
slug: spark-bigquery-connector-vectorized-parquet-read
topics:
- google-infrastructure
---

Google's stated goal for Spark-on-BigLake was that customers running Spark against [[biglake-tables|BigLake tables]] should get price-performance comparable to running Spark directly against raw Parquet in GCS — despite the extra API layer in between. The open-source Spark BigQuery Connector gets there by integrating the [[bigquery-storage-api|Storage API]] with Spark DataFrames through Spark's DataSourceV2 interface: the Spark driver opens a Read API session during query planning to obtain the list of read streams, and Spark executors then read those streams in parallel during execution. The Read API returns rows already in Apache Arrow's columnar format, and because Spark has native Arrow support, ingesting that data means minimal memory copying rather than a deserialize-then-reformat step.

The Parquet path specifically needed a fix to hit that performance bar. Google's first implementation of Parquet scanning in the Read API reused Dremel's existing row-oriented Parquet reader and then translated the resulting rows into [[superluminal-execution-engine|Superluminal]]'s columnar in-memory format — which meant Parquet's on-disk columns were pivoted into rows by the reader and then pivoted back into Arrow columnar batches downstream, a round trip the source calls inefficient. The fix was a purpose-built vectorized Parquet reader that outputs Superluminal columnar batches directly from Parquet files, skipping the row-oriented intermediate step entirely; because Superluminal can operate directly on dictionary- and run-length-encoded data without first decoding it, reading straight from Parquet's encoded columns into Superluminal's format is substantially cheaper than going through a row-oriented reader built for a different engine's needs.

*See also: [[bigquery-storage-api]] · [[biglake-tables]] · [[superluminal-execution-engine]]*
