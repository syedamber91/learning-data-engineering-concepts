---
book: Designing Data-Intensive Applications
type: concept
tags: [ddia, concept, data-structures, storage-engines]
sources:
  - raw/glossary.md
---
# Bloom Filters

A tiny probabilistic set summary that answers "definitely not present" or "maybe
present" — never a false negative, occasionally a false positive. LSM engines keep
one per SSTable so a lookup for a missing key can skip reading segments from disk
at all, fixing the "miss is expensive" weakness of layered storage.

In the book: the read-optimization noted in [[SSTables and LSM-Trees]] (Ch 3).
Same trick reappears in join optimization and query engines throughout the big-data
ecosystem.

## Referenced In
- [[Data Structures That Power Your Database]]
- [[SSTables and LSM-Trees]]
- [[Uses of Stream Processing]]

## Related in the other wiki
- [[bloom-filter]] — Vu's entity note on the same probabilistic "definitely not present" guarantee, framed around skipping an SSTable read entirely in an LSM-tree.
