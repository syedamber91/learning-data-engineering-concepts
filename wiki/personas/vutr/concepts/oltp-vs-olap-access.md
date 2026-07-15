---
persona: vutr
kind: concept
sources:
- raw/storage-models-nsm-dsm-pax-column-store-additional/oltp-vs-olap-data-format-and-indexing.md
- raw/storage-models-nsm-dsm-pax-column-store-additional/what-makes-oltp-databases-so-quick.md
- raw/storage-models-nsm-dsm-pax-column-store-additional/partitioning-and-clustering.md
last_updated: '2026-07-15'
qc: passed
slug: oltp-vs-olap-access
topics:
- storage-models-nsm-dsm-pax-and-column-store
- sql-fundamentals-and-execution-model
---

Once a workload has settled on a storage layout — [[nsm]] for OLTP, [[dsm]]/[[pax-hybrid-layout]] for OLAP — the next question Vu poses is separate but related: given that layout, how does the system actually *find* the data it needs? He frames the two workloads' access patterns as fundamentally different asks. OLTP systems are asked to "find this one specific thing" and need a precise, map-like lookup; OLAP systems are asked to "summarize these few attributes across everything" and demand a method of efficient data elimination instead.

For OLTP, the map-like lookup is a [[b-plus-tree-index|B+Tree index]]: given a filter on the indexed column — a point lookup or range filter (`=`, `<`, `>`, `between`) such as fetching a customer by ID — the tree descends from root to leaf, comparing the search value against each page's keys to pick a child pointer, until it reaches the leaf page holding the actual data. This is the ubiquitous OLTP query shape, and it's cheap precisely because the tree structure lets the engine skip most of the table without reading it.

For OLAP, that same lookup index "won't help much." Faced with queries scanning billions of rows, the bottleneck isn't locating a single record — it's minimizing the volume of data read and processed at all. [[dsm]]/[[pax-hybrid-layout]] already narrows this by column (the engine only opens the columns a query needs), but Vu's posts describe three further, complementary techniques for skipping data within those columns, which they present as a coarse-to-fine hierarchy: lightweight block-level metadata such as Zone Maps (skip a chunk without reading it, based on stored min/max/null-count/distinct-count/Bloom-filter statistics), partitioning (skip whole physical partitions based on a filter on the partition key — see [[partitioning-schemes-across-systems]]), and clustering (co-locate similar values physically so a partition's or table's own Zone Map statistics become tight enough to be useful — see [[clustering-sort-order-and-z-ordering]]). The throughline both posts return to: OLTP's B+Tree index answers "where is this row," while OLAP's whole toolbox of physical-layout tricks answers "which bytes can I avoid reading."

*See also: [[b-plus-tree-index]] · [[nsm]] · [[dsm]] · [[pax-hybrid-layout]] · [[partitioning-schemes-across-systems]] · [[clustering-sort-order-and-z-ordering]]*

## Related in the other wiki
- [[Transaction Processing or Analytics]] — DDIA's chapter draws the same OLTP-vs-OLAP line at the workload level; this concept adds vutr's own framing of *why* the access pattern differs (map-like lookup vs. data elimination) and the concrete mechanisms (B+Tree vs. Zone Maps/partitioning/clustering) each side uses.
- [[Other Indexing Structures]] — DDIA's survey of index structures beyond the primary key is the broader context for this concept's B+Tree-for-OLTP claim.
