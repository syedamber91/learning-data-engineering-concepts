---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: batch-reprocessing-blindness
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Batch processing can't tell which records actually changed, so it defends by conservatively reprocessing whole partitions. Uber captures this exactly: not knowing whether a driver's earning data changed, it must assume 'data was changed in the last X days' and reprocess all X partitions — the core motivation behind streaming and incremental table formats.

*See also: [[doordash-flink-iceberg]] · [[linkedin-kafka-beam]] · [[netflix-iceberg-maestro]] · [[uber-lambda-kafka]] · [[twitter-kappa-migration]] · [[meta-velox-tectonic]]*
