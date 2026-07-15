---
persona: vutr
kind: entity
sources:
- raw/google-infrastructure/i-spent-5-hours-learning-how-google.md
last_updated: '2026-07-15'
qc: passed
slug: bigquery-storage-api
topics:
- google-infrastructure
---

Before the Storage API existed, getting data out of BigQuery-managed storage for an external engine meant exporting it to GCS first — a round trip through object storage before Spark or Trino could touch it. Google built the Storage API to let external engines read (and write) BigQuery-managed storage and [[biglake-tables|BigLake tables]] directly, as two gRPC-based services.

The Read API begins a session by letting the caller specify the number of parallel streams, a snapshot time, which columns to return, and a filter predicate; the response carries stream identifiers, a reference schema, and an expiration of at least six hours, after which no manual cleanup is needed since sessions expire automatically. Each stream sends serialized row blocks that can resume from a specific row offset after an error, and the API supports splitting a stream into child streams for dynamic work rebalancing mid-read. Received blocks are deserialized via Apache Avro or Apache Arrow, using the session's reference schema to keep long-lived decoders consistent across streams. The Read API embeds [[superluminal-execution-engine|Superluminal]] to run GoogleSQL expressions and operators with vectorized processing, apply user predicates and security filters, and handle data masking, before transcoding the results into Apache Arrow so different downstream engines can consume them uniformly and efficiently.

The Write API is the ingestion counterpart: scalable, high-speed, high-volume streaming ingestion into BigQuery-managed storage, with multiple concurrent streams, exactly-once delivery semantics, stream-level and cross-stream transactions, and a gRPC wire protocol. Its core abstraction is the stream itself, through which data is written to a table, and it exposes different write modes so callers can pick between real-time streaming and batch-commit processing semantics with different commit guarantees. The Read API in particular is what the Spark BigQuery connector rides on to get performant reads over BigLake tables — see [[spark-bigquery-connector-vectorized-parquet-read]].

*See also: [[biglake-tables]] · [[biglake-managed-tables]] · [[superluminal-execution-engine]] · [[spark-bigquery-connector-vectorized-parquet-read]]*
