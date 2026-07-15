---
persona: vutr
kind: concept
sources:
- raw/storage-models-nsm-dsm-pax-column-store-additional/we-might-not-completely-understand.md
- raw/storage-models-nsm-dsm-pax-column-store-additional/oltp-vs-olap-data-format-and-indexing.md
last_updated: '2026-07-15'
qc: passed
slug: pax-hybrid-layout
topics:
- storage-models-nsm-dsm-pax-and-column-store
---

PAX is the hybrid storage model sitting between [[nsm]] and [[dsm]]: table data is first split horizontally into row groups, and *within* each row group, the columns' values are stored next to each other. The goal, in Vu's words, is to get the fast, efficient scans of the column store while keeping the locality of the row store — column values from the same row stay physically close, at least within the scope of that row group. A PAX file carries global metadata pointing to where each row group lives, and each row group in turn carries its own metadata about its contents. Mechanically, building one is two steps repeated per row group: split the incoming data horizontally into a portion, then within that portion write out all values for one column before moving on to the next column.

The finding Vu treats as the article's whole point: most systems that market themselves as "column stores" are actually PAX under the hood, not true [[dsm]]. He names BigQuery, Snowflake, DuckDB, Parquet, and ORC as PAX systems — with Parquet as the example he expects to surprise people most, since its row-group/column-chunk structure is exactly this pattern. Of everything he surveyed, only [[clickhouse|ClickHouse]] and [[redshift|Redshift]] actually implement pure DSM (each column stored in a completely separate place). His closing prompt for readers is deliberately blunt: next time someone says a product "stores data in a columnar fashion," ask them whether that's PAX or DSM — because most documentation blurs the distinction, and the two have materially different point-query and compression behavior (see [[oltp-vs-olap-access]]).

A related pattern shows up when an OLAP system needs to absorb heavy real-time writes without giving up columnar reads. BigQuery is Vu's example: rather than writing incoming data straight into columnar/PAX storage (expensive per-write), its engineers rebuilt the storage engine to treat streaming ingestion as a first-class citizen — data lands first in row-store format, then gets converted to column/hybrid format in the background for consumption. He observes the same write-then-convert pattern in Apache Hudi. The benefit is a clean separation of concerns between the write path and the read path; the cost is operational complexity in keeping the background conversion running and consistent. Vu is explicit that, due to limited public information, BigQuery and Hudi were the only two systems he could confirm use this approach, though he expects it to spread as more OLAP systems chase real-time ingestion and querying.

*See also: [[nsm]] · [[dsm]] · [[oltp-vs-olap-access]] · [[partitioning-schemes-across-systems]] · [[snowflake-micro-partitions]]*

## Related in the other wiki
- [[Column-Oriented Storage]] — DDIA's general column-store treatment; this concept adds the specific detail that most real "column stores" (BigQuery, Snowflake, DuckDB, Parquet) are actually the PAX hybrid, not the pure columnar layout DDIA describes in the abstract.
- [[Writing to Column-Oriented Storage]] — DDIA's discussion of the write-path cost of column-oriented layouts is the same tension behind BigQuery/Hudi's row-store-then-convert-to-columnar pattern this concept describes.
