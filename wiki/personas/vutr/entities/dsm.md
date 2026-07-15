---
persona: vutr
kind: entity
sources:
- raw/storage-models-nsm-dsm-pax-column-store-additional/we-might-not-completely-understand.md
- raw/storage-models-nsm-dsm-pax-column-store-additional/oltp-vs-olap-data-format-and-indexing.md
- raw/storage-models-nsm-dsm-pax-column-store-additional/partitioning-and-clustering.md
last_updated: '2026-07-15'
qc: passed
slug: dsm
topics:
- storage-models-nsm-dsm-pax-and-column-store
---

DSM (Decomposition Storage Model) is the true column store: a single column's values are stored continuously on their own page, with a dedicated header for that column's metadata, rather than being interleaved with the rest of the row the way [[nsm]] does it.

The mechanism solves a problem [[nsm]] doesn't have to think about: once a row's values live in separate places, how does the DBMS know which value in the `user_name` page belongs to which value in the `revenue` page? DSM's answer is to enforce a fixed length for every value in a column, which turns column access into array arithmetic — the address of the value at offset *i* is `first_element_address + i * element_size`, the same trick that gives arrays O(1) random access. Values sitting at the same offset across different column pages correspond to the same logical row, so a query first finds the matching offsets in the filtered column, then reuses those same offsets to pull the corresponding values out of the other needed columns.

That layout is precisely why DSM is good for analytics and bad for transactions. An OLAP query that filters on `user_name` and aggregates `created_date`/`revenue` only touches the pages for those three columns — no redundant I/O from the other columns in the table — and because a column's values often share patterns (e.g. a platform column with only two distinct values, Android and iOS), DSM compresses much better than [[nsm]]. The same design is expensive in the opposite direction: reading one row with 20 columns means consolidating data scattered across 20 different pages, and writing a row into a 100-column table means splitting that write across 100 separate locations — overhead NSM simply doesn't pay. Vu also flags a second-order cost: OLAP queries rarely touch just one column at a time, so the DBMS regularly has to reassemble data from physically scattered column pages, meaning genuine "jumping around on disk" even in the column-optimized case — precisely the problem [[pax-hybrid-layout]] was introduced to address.

Vu's own survey found this pure form of columnar storage rarer than the marketing suggests: of the products that describe themselves as column stores, only [[clickhouse]] and [[redshift]] actually split data vertically and keep column values completely separate; everything else claiming "columnar" — BigQuery, Snowflake, DuckDB, Parquet — is really running [[pax-hybrid-layout]] underneath. He also notes Redshift specifically does not support user-defined table partitioning at all, unlike BigQuery, ClickHouse, or Iceberg-family formats — a further way its true-DSM design departs from the PAX-based majority.

*See also: [[nsm]] · [[pax-hybrid-layout]] · [[oltp-vs-olap-access]] · [[clustering-sort-order-and-z-ordering]]*

## Related in the other wiki
- [[Column-Oriented Storage]] — DDIA's general treatment of storing each column's values contiguously for analytic scans, the same idea this entity grounds in vutr's fixed-length-offset mechanism.
- [[Sort Order in Column Storage]] — DDIA discusses how column stores benefit from a chosen sort order across columns; see [[clustering-sort-order-and-z-ordering]] for vutr's concrete sort/Z-order mechanics on top of this same DSM/PAX physical layer.
