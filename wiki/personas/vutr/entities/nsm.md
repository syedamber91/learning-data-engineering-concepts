---
persona: vutr
kind: entity
sources:
- raw/storage-models-nsm-dsm-pax-column-store-additional/we-might-not-completely-understand.md
- raw/storage-models-nsm-dsm-pax-column-store-additional/oltp-vs-olap-data-format-and-indexing.md
last_updated: '2026-07-15'
qc: passed
slug: nsm
topics:
- storage-models-nsm-dsm-pax-and-column-store
---

NSM (N-ary Storage Model) — the row store — is the physical layout most OLTP systems reach for: the DBMS continuously stores all the column values for a single row together, in a page. Vu's mental model for a page itself matters here: it's an atomic unit — a hardware page, OS page, or database page — where all of a page's data is read or written successfully, or none of it is; to align with the underlying hardware, the database page is typically a constant multiple of the 4KB hardware page (e.g. 32KB).

The mechanism is concrete, not just a label. Inside a page, a row's values sit next to each other; once one row is fully written, the next row goes right after it. A small structure called the **slot array** tracks where each row starts — one entry per row, each entry pointing to that row's byte offset. The header sits at the start of the page, then the slot array; the first row arrives at the *end* of the page. As more rows come in, the slot array grows toward the end of the page while row data grows toward the beginning — the page is full once the two meet in the middle. A row's identity is simply its page identifier plus its slot array entry.

That layout is what makes NSM fast for OLTP in both directions. Writing a new row means writing its column bytes sequentially to a single page — one contiguous append, not scattered writes. Reading a row is the mirror image: once the slot array points you to the row's start, the whole row is already contiguous, so the DBMS reads it in one pass with no jumping around to reassemble it from elsewhere.

The same property is exactly what hurts NSM on an analytical query. A query that filters on one column (e.g. `user_name` matching a pattern) still forces the DBMS to load the *entire* row just to test one field, because that field is stitched together with everything else in the row. A subsequent aggregation that only needs two of those columns (say `created_date` and `revenue`) can't be served by loading less data either — the physical layout doesn't let the engine pick out individual columns. And because values from different columns in the same row rarely share a pattern, NSM also compresses poorly compared to column-oriented layouts.

The summary vutr lands on: NSM is ideal for workloads needing fast insertion, fast mutation, and reads of the entire tuple — the OLTP profile — but is the wrong physical shape for workloads that scan a large amount of table data restricted to a subset of columns, which is exactly the OLAP profile that [[dsm]] and [[pax-hybrid-layout]] exist to serve instead.

*See also: [[dsm]] · [[pax-hybrid-layout]] · [[oltp-vs-olap-access]] · [[b-plus-tree-index]]*

## Related in the other wiki
- [[Data Structures That Power Your Database]] — DDIA's framing of how a database's on-disk data structure choice follows from its read/write workload, the same logic this entity applies specifically to row-vs-column physical layout.
