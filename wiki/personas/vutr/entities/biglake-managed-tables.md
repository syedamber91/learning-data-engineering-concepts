---
persona: vutr
kind: entity
sources:
- raw/google-infrastructure/i-spent-5-hours-learning-how-google.md
last_updated: '2026-07-15'
qc: passed
slug: biglake-managed-tables
topics:
- google-infrastructure
---

BigLake Managed Tables (BLMTs) invert the deal that [[biglake-tables|BigLake tables]] make with open formats. A regular BigLake table leaves an open format like Iceberg or Delta Lake in charge of its own metadata; a BLMT has Google's BigMetadata manage 100% of the metadata instead, while the actual data still lands as Parquet files in object storage. The source frames two specific weaknesses of the open-table-format approach that motivate this: committing metadata atomically to an object store isn't the bottleneck by itself, but object stores can only update or replace a given object a handful of times per second, which caps mutation throughput; and because the transaction log sits alongside the data in object storage, a malicious writer with access to that storage can tamper with it and rewrite the table's history.

BLMT's answer is to move the metadata off object storage into BigMetadata, a stateful service that keeps the tail of the transaction log in memory and periodically converts it into a columnar layout for efficient reads. At query time, Dremel (BigQuery's engine) reads that columnar baseline and reconciles it with the in-memory tail, so combining a fast in-memory state with a periodically-flushed columnar baseline lets BLMT sustain mutation rates open table formats can't reach without giving up read performance. Because writers can no longer mutate the transaction log directly, the resulting metadata carries a reliable audit history — closing the tampering gap open formats leave open. BigMetadata's central role also unlocks a capability the source says open table formats don't currently support at all: multi-table transactions, since one metadata service can coordinate a commit across more than one table rather than each table owning an independent, isolated log. BLMTs also get DML support and high-throughput ingestion through the [[bigquery-storage-api|Write API]], plus behind-the-scenes storage optimization — adaptive file sizing, reclustering, garbage collection — that a self-managed open table format would otherwise need external tooling to perform.

*See also: [[biglake-tables]] · [[bigquery-storage-api]]*
