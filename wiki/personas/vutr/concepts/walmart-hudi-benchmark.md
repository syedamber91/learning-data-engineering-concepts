---
persona: vutr
kind: concept
sources:
- raw/iceberg-hudi-delta-open-table-formats/why-walmart-chose-apache-hudi-for.md
last_updated: '2026-07-15'
qc: passed
slug: walmart-hudi-benchmark
topics:
- iceberg
---

Walmart's lakehouse transformation is one of the few case studies in these notes with real, numbered benchmark results behind a table-format choice, run at genuine scale: 10,000+ stores, millions of transactions per hour, and 600K+ compute cores spread across Hadoop and Spark clusters on both Google Cloud and Azure. Walmart wanted to move from a batch-oriented lake to a near-real-time lakehouse while keeping full control across multiple clouds — ruling out a vendor-locked managed format from the start.

Walmart abstracted its production traffic into two representative workloads before testing anything. The **batch workload** was partition-oriented (year/month/day/hour), dominated by inserts (>99.9%) with a small but painful tail of late-arriving records (<0.1% updates) that forces the engine to reopen and rewrite old partitions. The **streaming workload** was the opposite: row-level upserts from CDC off a multi-terabyte Cassandra table, with updates making up more than 99.999% of the traffic and inserts almost none of it. Walmart then deployed Delta, Hudi, Iceberg, and its legacy pipeline into isolated environments, let each reach steady state, and only then measured.

**Results.** Hudi + Spark 3.x was the most performant on the batch workload — more than 5x faster than the legacy system. On the streaming workload, Delta Lake beat Hudi on raw ingestion speed by 27%, but Hudi's own compaction process was faster than Delta's at the time, because Delta's ingestion pipeline was paying for Z-ordering optimizations Hudi didn't yet have — an investment that paid off later on queries. On TPC-H query benchmarks (queries 1–7 for batch, 1–10 for streaming), Delta Lake outperformed in most queries by roughly a 40% margin, driven almost entirely by Z-ordering, while Hudi's real strength showed up in real-time deduplication, giving it faster access to the latest version of a record. Iceberg never made it into the ingestion or query benchmarks at all — Walmart hit cleanup problems getting an optimal file size during ingestion and simply skipped it rather than fight that issue through to a fair comparison.

Walmart chose Hudi. The deciding factors were breadth, not a single metric: batch and streaming support in one format, incremental processing that avoids full-table rewrites, efficient upserts/deletes via unique keys and Hudi's own index (see [[hudi-index]]), and operational extras (Bloom filters, commit notifications, monitoring) that fit its already-diverse 600K-core, multi-cloud stack.

Vu's own gloss on this result matters as much as the numbers: he explicitly flags that Hudi has since added Z-ordering and improved file-group metadata management, and expects the query-performance gap the 2023 benchmark found has likely narrowed significantly since — a caution that the specific numbers here are a 2023 snapshot of a moving target, not a permanent ranking. Walmart's own stated takeaways generalize past this one benchmark: the most popular tool isn't automatically the right one, fair and isolated benchmarking is what actually produces a trustworthy answer, and choosing open-source/self-managed over a vendor's managed offering is its own trade-off (full control, full operational burden) rather than a strictly better choice.

*See also: [[apache-hudi]] · [[copy-on-write-vs-merge-on-read]] · [[evaluate-before-adopting]] · [[hudi-index]] · [[delta-lake]]*
