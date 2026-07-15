---
persona: vutr
kind: entity
sources:
- raw/big-tech-case-studies-batch-2-apple-github-pinterest-canva/groupby-17-pinterests-new-wide-column.md
last_updated: '2026-07-15'
qc: passed
slug: rockstorewidecolumn
topics:
- big-tech-case-studies-batch-2-apple-github-pinterest-canva
---

Rockstorewidecolumn is the storage service Pinterest Engineering built to sit underneath KVStore, Pinterest's client-facing key-value abstraction. Vu Trinh's GroupBy #17 curates the distinction directly from the source: KVStore is "the client facing abstraction," while Rockstorewidecolumn is the separate storage service underneath it — described as "a wide column, schemaless NoSQL database built using RocksDB."

The curated post also carries Pinterest Engineering's own illustration, captioned "Logical view of a wide column database with versioned values" — establishing that values in this store carry versions, consistent with a wide-column model where a single row key can hold multiple named columns, each potentially holding more than one version of its value. The teaser calls the result "massively scalable" and "highly available." Beyond naming these pieces — the KVStore/Rockstorewidecolumn split, the RocksDB foundation, and the versioned-value data model — vutr's captured post does not walk through how RocksDB's on-disk structures are adapted into the wide-column model, or what made KVStore alone insufficient before Rockstorewidecolumn was built.

*See also: [[cloudkit]] · [[github-merge-queue]] · [[creator-content-usage-accounting-at-scale]]*
