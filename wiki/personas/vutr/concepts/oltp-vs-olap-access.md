---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: oltp-vs-olap-access
topics:
- storage-models-nsm-dsm-pax-and-column-store
- sql-fundamentals-and-execution-model
---

OLTP systems are asked to 'find this one specific thing' and need a precise, map-like lookup; OLAP systems are asked to 'summarize these few attributes across everything' and demand efficient data elimination. A look-up index won't help much in OLAP, because when you scan billions of rows the bottleneck is minimizing the volume of data read from storage, not locating a single record.

*See also: [[parquet]] · [[dsm]] · [[clickhouse]] · [[redshift]] · [[nsm]] · [[pax-hybrid-layout]]*
