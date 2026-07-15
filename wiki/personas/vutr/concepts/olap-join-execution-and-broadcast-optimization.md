---
persona: vutr
kind: concept
sources:
- raw/olap-cost-and-multi-engine-comparison/7-insights-to-help-you-learn-any.md
last_updated: '2026-07-15'
qc: passed
slug: olap-join-execution-and-broadcast-optimization
topics:
- olap-cost-and-multi-engine-comparison
---

Databases generally reach for one of three join strategies, and OLAP workloads systematically favor two of the three. Nested Loop Join (NLJ) iterates every record of the left table in an outer loop and scans the right table for matches in an inner loop; it performs well in OLTP when the left table is small or the right table has an index on the join column, turning the inner scan into a quick lookup — but OLAP workloads typically put large tables on both sides of a join with no point-lookup index available, which is exactly what makes NLJ, per vutr's notes, "generally considered unsuitable" there. Sort Merge Join (SMJ) sorts both tables on their join columns first, then walks the two sorted sequences with pointers, advancing and matching until either side runs out; the up-front sort is the expensive part, so SMJ is a strong choice specifically when the tables are already sorted or the query itself needs sorted output. Hash Join targets equi-joins directly: a build phase hashes the smaller table's join column into an in-memory hash table, then a probe phase hashes the larger table's rows against it to find matches; when the build side is too large for memory, Grace Hash Join partitions both tables into on-disk buckets and processes matching bucket pairs to avoid overflowing memory.

OLAP engines lean on Hash Join and Sort-Merge Join, and execute them in parallel across many machines: both tables are hashed on their join columns and distributed into worker-owned buckets, each worker performs a local join against its own bucket, and if one join key value is disproportionately common, the worker holding it gets overloaded — a data-skew problem the system resolves by re-partitioning or re-hashing to rebalance load. Of the two, Hash Join is described as the more widely adopted: Snowflake and BigQuery rely on it "heavily or exclusively," while Spark supports both hash and sort-merge, and the preference for hash joins traces to their efficiency in memory-rich environments and their avoidance of Sort-Merge's expensive up-front sort, provided the hash table fits in memory.

The standard optimization layered on top of Hash Join in these engines is the Broadcast Hash Join: when one of the two tables is small enough to fit entirely in memory, the system skips shuffling *both* tables across the network and instead sends the whole small table to every worker node, which builds its own local hash table from the broadcast copy and probes it against its own slice of the larger table — cutting network traffic sharply since only the small table ever moves. BigQuery and Snowflake both automatically detect when this optimization applies at runtime, without requiring an explicit hint from the query author.

*See also: [[redshift-code-generation-and-self-tuning-operations]] · [[broadcast-join-and-bucket-join]] · [[sort-merge-join-vs-shuffle-hash-join]]*
