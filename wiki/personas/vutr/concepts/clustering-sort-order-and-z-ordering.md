---
persona: vutr
kind: concept
sources:
- raw/storage-models-nsm-dsm-pax-column-store-additional/oltp-vs-olap-data-format-and-indexing.md
- raw/storage-models-nsm-dsm-pax-column-store-additional/partitioning-and-clustering.md
last_updated: '2026-07-15'
qc: passed
slug: clustering-sort-order-and-z-ordering
topics:
- storage-models-nsm-dsm-pax-and-column-store
---

Clustering shares partitioning's goal — help the engine skip data it doesn't need — but works at a finer grain. Where [[partitioning-schemes-across-systems|partitioning]] is limited by the cardinality of the partition key, clustering reorganizes data *within* partitions (or across the whole table, if unpartitioned) so that similar values end up physically co-located. Vu names BigQuery, Snowflake, Iceberg, and ClickHouse as systems supporting sort-based clustering — and calls out ClickHouse specifically as *always* clustered, since every MergeTree table requires a primary key that the engine uses to sort the data.

**Sort clustering.** The simplest mechanism is sorting the data by one or more columns before writing it, so rows with similar values in those columns are more likely to land in the same file. A query with a filter on the sorted column (e.g. `WHERE device_id = 1`) triggers a metadata scan first: for each file, the engine reads that column's min/max statistics, and if the target value falls outside a file's range, the whole file is skipped without ever being read.

The catch is that sorting on more than one column only pays off if your filter respects the sort order. If a table is sorted first by `device_id`, then by `customer_id`, filtering on `device_id` alone (or on both, in that order) benefits fully; filtering on `customer_id` alone does not, because that column's values are scattered across the range dictated by `device_id`, not sorted independently. Vu's worked example: a table with `device_id` and `customer_id` each ranging over `[0,1,2,3]`, sorted by `device_id` then `customer_id`, produces four files — one per `device_id` value, each spanning the full `customer_id` range. Filtering `device_id = 1` (or `device_id = 1 AND customer_id = ...`) only has to scan one file; filtering on `customer_id` alone forces a scan of all four files, because every file contains the full range of `customer_id` values.

**Z-ordering.** Multi-dimensional clustering techniques exist to fix that asymmetry, and Z-ordering (Morton coding) is the one Vu works through in detail, built on the mathematical idea of a **space-filling curve** — a continuous curve that visits every point in an N-dimensional space exactly once while preserving spatial locality, so points close together in N-D space stay close together once mapped onto the resulting 1-D line. Sorting the data by each row's position on that 1-D curve, rather than by the raw column values, is what lets clustering treat multiple dimensions more fairly.

The Z-value itself is computed by **bit interleaving**: convert each clustered column's value to binary, then build a new binary number by taking the first bit from the first dimension, the first bit from the second dimension, and so on across all dimensions, repeating for each remaining bit position. (Vu's toy example: interleaving `010` and `001` gives `000110`.) Sorting the dataset by these Z-values produces the characteristic recursive Z-shaped traversal the technique is named for.

Working through the same `device_id`/`customer_id` example under Z-ordering (four possible values each) yields four files, but along different boundaries than plain sorting: each file now covers a 2×2 block of the `device_id`×`customer_id` grid rather than one full `device_id` value against the entire `customer_id` range. Filtering `device_id = 1` now touches 2 files instead of 1 (slightly worse than sort-clustering's best case), but filtering `customer_id = 3` also touches only 2 files instead of all 4 — Z-ordering "treats clustered keys more fairly" by giving up a little of sort-clustering's best-case performance on the leading column to avoid its worst-case performance on the trailing one. Delta Lake, Iceberg, and Hudi are the systems Vu names as supporting Z-ordering.

**Cost and maintenance.** Clustering is not free: it slows writes, since data must be placed in a specific order rather than simply appended, and new incoming data degrades an existing sort order over time (rows for a previously-clustered value can land in newer files that overlap already-sorted ranges), which means the data has to be periodically reorganized to restore locality. In BigQuery this reclustering is automatic and free; in Snowflake it's automatic but carries an extra cost. Either way, Vu frames the real decision as knowing two things about your system: what kind of clustering it offers (plain sort vs. multi-dimensional like Z-ordering), and how — or whether — it maintains the clustered state for you.

**Open gap, in Vu's own words:** he explicitly skips the Hilbert curve, the other well-known space-filling curve used for multi-dimensional clustering, admitting "I suck at Math... forgive me for skipping the Hilbert curve" — so this pack has no grounded mechanism for it, only Z-ordering.

*See also: [[partitioning-schemes-across-systems]] · [[snowflake-micro-partitions]] · [[dsm]] · [[iceberg-hidden-partitioning-and-sort-order]] · [[olap-data-skipping-zone-maps-partitioning-clustering]]*

## Related in the other wiki
- [[Sort Order in Column Storage]] — DDIA's discussion of choosing a sort order in a column store is the general case of vutr's sort-clustering mechanism and its column-order dependency.
- [[Partitioning and Secondary Indexes]] — DDIA's chapter on the tension between physical layout and query patterns is the broader frame for why a single sort order can't serve every filter column equally, which is exactly the gap Z-ordering is built to narrow.
