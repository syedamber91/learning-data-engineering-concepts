---
persona: vutr
kind: concept
sources:
- raw/bigquery-internals/everything-you-need-to-know-about.md
last_updated: '2026-07-15'
qc: passed
slug: storage-compute-disaggregation-bigquery
topics:
- bigquery-internals
---

Dremel's storage layer went through the same shared-nothing-to-disaggregated arc as its shuffle layer (see [[disaggregated-shuffle-service]]), just earlier and for different reasons. In its original form, Dremel ran on a few hundred shared-nothing servers, each holding a subset of the data on local disks — the conventional wisdom of the time being that dedicated hardware and direct-attached disks squeeze the most performance out of an analytical system. In 2009 Dremel moved onto Borg (Google's Kubernetes predecessor) to handle growing workload, which meant storing each table's data across three different local disks managed by independent servers so data could be shared across jobs — but storage and compute were still coupled: data had to be physically shifted whenever the cluster was resized, and the two couldn't scale independently.

Given improvements in Google's storage and network, Google revisited that shared-nothing choice and moved to a shared-disk architecture built on the Google File System (GFS). The first attempt was rough: Google reports an "order-of-magnitude performance degradation," because now every read has to cross the network to reach storage instead of hitting a local disk. Google spent real effort tuning the storage format, metadata representation, query affinity, and prefetching before shared-disk Dremel actually outperformed the local-disk approach. The payoff went beyond raw latency: GFS being a fully managed internal service improved Dremel's SLOs and robustness, eliminated the step of first loading shared tables onto a Dremel server's local disk, and made onboarding new teams easier since their data no longer required resizing the cluster to load.

The same GFS migration is also where Vu locates BigQuery's lakehouse-like roots. Dremel's original 2006 design was DBMS-shaped: data had to be explicitly loaded into Dremel before it was queryable, meaning only Dremel could see it. When Google introduced a shared storage format on GFS, that format had two properties that changed the picture: it was columnar, and it was **self-describing** — carrying its own metadata. Because the format described itself, custom transformation tools and SQL-based analytics could use data sitting in that format without any prior loading step; any file in the storage system could become part of the queryable repository, and many different tools could share the same underlying data. Vu draws the direct line from this to the modern Lakehouse idea: users stop loading data into the warehouse and instead bring the warehouse's compute to where the data already sits.

*See also: [[disaggregated-shuffle-service]] · [[dremel-query-engine]] · [[capacitor-file-format]]*
