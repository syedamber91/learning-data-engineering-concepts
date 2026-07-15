---
persona: vutr
kind: concept
sources:
- raw/amazon-s3-gfs-hdfs-distributed-file-systems-additional/amazon-s3-for-data-engineers.md
last_updated: '2026-07-15'
qc: passed
slug: prefix-as-folders
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

Object storage has no real folders. A bucket is a flat namespace of objects, each identified by a unique key; a **prefix** is just a leading substring of that key, and two objects like `reports/2025/sales.csv` and `reports/2025/inventory.csv` merely *appear* to sit in a `2025` folder inside a `reports` folder because their keys happen to share the `reports/2025/` prefix. There is no folder object behind that appearance — it's a display convention layered onto a flat keyspace.

That flatness is not incidental — it's the mechanism S3 uses to distribute load. S3 maps objects to storage servers by partitioning object keys, specifically their prefixes, across servers in lexicographic order: objects whose prefix's first character falls in a given range (e.g., A-F, G-M, N-S, T-Z) land in the same partition, and S3 can detect a partition taking disproportionate traffic and split it into smaller partitions automatically. AWS explicitly recommends maximizing character diversity at the *start* of a prefix to help this auto-splitting behave well (Google Cloud recommends the same for its own auto-scaling). The payoff is throughput scaling by prefix count: AWS documents at least 3,500 PUT/COPY/POST/DELETE or 5,500 GET/HEAD requests per second per partitioned prefix, with no limit on the number of prefixes a bucket can have — ten well-distributed prefixes buys roughly 35,000 PUT/s or 55,000 GET/s in aggregate.

The practical upshot for a data engineer: prefix design is a genuine performance lever, not cosmetic naming. A bucket layout that clusters everything under one narrow prefix range concentrates load onto one partition regardless of how "organized" it looks; diversifying the prefix's leading characters is what actually lets S3 spread — and auto-split — the workload.

*See also: [[amazon-s3]] · [[object-storage-operational-practices]]*
