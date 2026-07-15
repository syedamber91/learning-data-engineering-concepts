---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 3
chapter_title: Storage and Retrieval
topic: Column-Oriented Storage
type: subtopic
tags: [ddia, column-store, lsm-tree, write-path]
sources:
  - raw/ch03.md
---
# Writing to Column-Oriented Storage
> Compressed, sorted column files can't be edited in place — so column stores buffer writes in memory LSM-style and merge them into the column files in bulk.

## The Idea
Everything that makes a column store fast to read — columnar layout, [[Column Compression]], and a chosen [[Sort Order in Column Storage]] — makes it hostile to writes. A B-tree-style update-in-place is off the table: you cannot poke a new value into the middle of a compressed run. Worse, because a row is identified purely by its *position* within each column file, inserting one row into the middle of the sorted order would force a consistent rewrite of **every** column file. The warehouse workload (mostly large read-only analyst queries, with bulk loads rather than random user writes) tolerates a heavier write path, but there still has to be one.

## How It Works
The chapter's earlier ideas come to the rescue: the solution is exactly the [[SSTables and LSM-Trees]] pattern.
- **Buffer in memory:** incoming writes land in an in-memory store that keeps them in a sorted structure ready for flushing. Notably, it makes no difference whether that in-memory stage is itself row-oriented or column-oriented — only the on-disk format matters.
- **Merge in bulk:** once enough writes accumulate, they are merged with the existing on-disk column files and written out as *new* files in one sequential pass, preserving sort order and compression.
- **Read both sides:** a query must combine the (large, old) column data on disk with the (small, recent) writes in memory. The query optimizer does this merging invisibly, so from the analyst's perspective inserts, updates, and deletes are reflected in the very next query — no "visible only after the nightly load" lag.

## Trade-offs & Pitfalls
- Writes cost background merge work and temporary duplication, the same tax LSM engines pay via [[Compaction]] — acceptable here because analytics is read-dominated.
- Every read silently spans two structures; the simplicity is in the optimizer, not the storage.
- The positional-identity invariant is unforgiving: any scheme that updated columns independently would corrupt row reassembly, which is why bulk rewrite-and-swap is the only safe route.

## Examples & Systems
This is essentially how Vertica (the commercialization of C-Store) handles writes: memory-staged writes merged into compressed, sorted column files on disk.

## Related
- up: [[Column-Oriented Storage]] · chapter: [[Ch 03 - Storage and Retrieval]]
- [[SSTables and LSM-Trees]] — the write pattern being reused wholesale
- [[Sort Order in Column Storage]] — the sorted files these merges must preserve
- [[B-Trees]] — the update-in-place approach that is impossible here
