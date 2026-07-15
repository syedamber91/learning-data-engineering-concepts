---
persona: vutr
kind: entity
sources:
- raw/sql-fundamentals-and-execution-model-additional/fundamentals-that-help-you-understand.md
- raw/sql-fundamentals-and-execution-model-additional/sql-for-data-engineers.md
last_updated: '2026-07-15'
qc: passed
slug: hash-join
topics:
- sql-fundamentals-and-execution-model
---

Hash join rests on one simple fact: if two rows match on an equi-join, they have the same join-column values, so they hash to the same bucket. The classic in-memory algorithm has two phases. In the **build phase**, the system constructs an in-memory hash table from the smaller table (the "build table"), hashing each row's join column(s) to determine its bucket, with the goal of fitting the whole table in memory. In the **probe phase**, the system scans the second table (the "probe table"); each row's join column(s) are hashed with the same function, and that hash is used to look up matching rows in the build-side hash table. Hash join needs neither sorted input nor a pre-built index, which makes it effective for equi-joins whenever the build table fits in memory.

The failure mode is exactly that memory assumption breaking. If the hash table outgrows available memory, imagine it split into part A (fits in memory) and part B (spills to disk): for every probe row, after checking part A, the system must also check part B, which means loading B into memory and offloading A to disk — expensive back-and-forth I/O that degrades performance significantly.

**Grace Hash Join** (also called partitioned hash join, named after the Grace database machine from 1980s Tokyo) is the fix when the hash table won't fit in memory. It runs in two phases of its own. The **partitioning phase** scans both tables, applies the same hash function to their join columns, and distributes rows into buckets on disk, sized so each build-side bucket (ideally the matching probe-side bucket too) fits in memory for the next phase — any bucket still too large is recursively re-partitioned with a different hash function. The **probing phase** then processes each pair of corresponding buckets: the build bucket is loaded and turned into an in-memory hash table, and a classic hash join runs against the matching probe bucket. It costs two rounds of hashing, but each bucket is brought into memory exactly once, which bounds the disk I/O.

In OLAP systems, hash join is the workhorse: Snowflake uses hash join for most cases, and BigQuery *only* supports hash joins — neither offers sort-merge join as an alternative, while Spark supports both hash join and [[sort-merge-join]]. The key optimization at scale is the **broadcast hash join**: if the build table is small enough to fit entirely in memory, it is broadcast whole to every worker, and each worker builds its own local hash table from that copy and joins it against its assigned partition of the probe table — unlike a standard distributed hash join, where both sides get shuffled across the network, a broadcast join only ever moves the small table. Spark lets you configure the size threshold that triggers broadcast join detection and also lets you hint the strategy directly. BigQuery cannot be configured that way; Google's own Dremel paper (the query engine behind BigQuery) describes it starting with a hash join that shuffles data on both sides, then dynamically canceling the second shuffle and switching to broadcast if one side finishes fast and falls under a size threshold — users can only hint at this by ordering tables in the join statement. Snowflake similarly detects the broadcast opportunity automatically. The distributed variant of Grace Hash Join's partitioning idea also shows up directly in OLAP: when a join key has a disproportionate number of rows and threatens to overload a single worker, the system re-hashes and re-partitions that oversized partition, the same recursive-partitioning escape hatch the standalone Grace Hash Join uses.

*See also: [[sort-merge-join]] · [[nested-loop-join]] · [[query-lifecycle]]*
