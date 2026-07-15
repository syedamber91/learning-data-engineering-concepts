---
persona: vutr
kind: entity
sources:
- raw/iceberg-hudi-delta-open-table-formats/i-spent-5-hours-exploring-the-story.md
- raw/iceberg-hudi-delta-open-table-formats/why-walmart-chose-apache-hudi-for.md
- raw/iceberg-hudi-delta-open-table-formats/how-do-iceberg-delta-lake-and-hudi.md
- raw/iceberg-hudi-delta-open-table-formats/how-do-delta-lake-iceberg-and-hudi.md
- raw/iceberg-hudi-delta-open-table-formats/why-do-we-need-open-table-formats.md
last_updated: '2026-07-15'
qc: passed
slug: apache-hudi
topics:
- iceberg
---

Hudi — Hadoop Upsert, Delete, and Incremental — was started at Uber by Vinoth Chandar (who later founded Onehouse) to solve a problem neither Iceberg nor Delta Lake was built to answer first: how do you mutate a small slice of a huge Hadoop table efficiently? Uber's second-generation platform moved raw data into a Hadoop lake instead of loading it straight into Vertica, which solved the ingestion side but exposed a new pain: HDFS and Parquet don't support in-place updates, so any change forced a full snapshot rebuild. In 2015, with roughly 100GB of genuinely new data landing per table per day, Uber's ingestion job still had to reprocess 100+ terabytes to fold that change in — a full-dataset Parquet rewrite taking over 20 hours on 1,000+ Spark executors, for updates as small as a single fare adjustment. The same problem hit ETL and modeling jobs, which rebuilt derived tables from scratch on every run instead of pulling only what changed.

The second motivation was serving latency. Lambda architecture (parallel batch-accuracy and streaming-freshness layers) and Kappa architecture (one streaming pipeline replaying history for reprocessing) both still leave you needing two serving layers when historical batch analytics and real-time serving have fundamentally different access patterns — analytical scans want columnar layout, real-time record lookups want row-oriented speed. Uber's own data showed workloads spread across a wide range of latency and completeness needs; for anything tolerating roughly 10-minute freshness, a dedicated "speed" serving layer became unnecessary if the lake itself could ingest and serve fast enough. Both pressures — incremental processing and near-real-time serving from one lake — are what Hudi was designed to answer.

**Architecture.** Hudi's own metadata lives in a `.hoodie` directory: `hoodie.properties` holds static table config (name, version, partitioning, file format, table type), while the rest of `.hoodie` builds the table's **Timeline** — see [[hudi-timeline]] for the full instant/action/state model. Data itself splits into two file kinds: columnar **Base Files** (Parquet) for read-efficient scanning, and row-oriented **Log Files** (Avro) that capture changes cheaply for write-efficient ingestion. A table is sharded into **File Groups** (each identified by a `fileId`), and each File Group holds a sequence of **File Slices** — one Base File plus its associated Log Files, each slice a full version of that group's data as of a particular Timeline instant. This is Hudi's version of Multiversion Concurrency Control: `COMPACTION` merges a slice's logs into a new Base File to produce the next slice, and `CLEAN` removes old slices no longer needed, giving Hudi both read/write efficiency (columnar base + row-oriented log) and built-in data versioning (each slice tied to a specific Timeline instant).

**Records and the index.** Every record's identity is a "hoodie key" — a record key plus the partition path it belongs to — which Hudi uses to guarantee no duplicate keys within (or, for non-partitioned tables, across) the whole table and to route updates/deletes to the right file group without a full scan. That routing mechanism is Hudi's **index**, detailed in [[hudi-index]] — the feature the notes repeatedly flag as what actually sets Hudi apart from Iceberg or Delta Lake, neither of which maintains an equivalent record-to-file lookup structure.

**Concurrency.** Hudi's atomic commit — creating the `<instant>.<action>.completed` file — is a specific case of [[occ-on-object-storage]], but with one twist neither Iceberg nor Delta Lake needs: Hudi requires an explicit lock (via a configured provider such as Zookeeper or DynamoDB), held only for the duration of the final commit check, not the whole transaction. While holding it, the writer checks the Timeline for any commits that completed during its own execution and aborts on a real conflict. Hudi v1.0 (2024) added **Non-Blocking Concurrency Control (NBCC)**, letting multiple writers commit without contending over that lock at write time at all — conflicts, if any, are resolved later, during the read or compaction pass instead.

**Adoption in production.** Walmart's own benchmarking — detailed in [[walmart-hudi-benchmark]] — is the concrete large-scale validation of Hudi's incremental-processing bet: Hudi + Spark 3.x beat legacy batch ingestion by more than 5x and, despite losing to Delta Lake's Z-ordering on raw query speed, won on real-time deduplication and compaction throughput at 600K+ compute cores across a multi-cloud (GCP + Azure) Hadoop/Spark deployment.

*See also: [[hudi-index]] · [[hudi-timeline]] · [[iceberg-metadata-layer]] · [[apache-iceberg]] · [[conditional-writes]] · [[open-table-formats]] · [[occ-on-object-storage]] · [[copy-on-write-vs-merge-on-read]] · [[walmart-hudi-benchmark]]*
