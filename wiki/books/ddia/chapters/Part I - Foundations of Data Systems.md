---
book: Designing Data-Intensive Applications
type: part-moc
tags: [ddia, foundations]
sources:
  - raw/partI.md
---
# Part I – Foundations of Data Systems

Part I covers ideas that hold for any data system, single-node or distributed. The
through-line: before you can reason about clusters, you need a vocabulary for what
"good" means (reliability, scalability, maintainability), a grasp of how data is modeled
and queried, how storage engines physically organize data, and how data is encoded
so systems can evolve without breaking.

## Chapters
- [[Ch 01 - Reliable, Scalable, and Maintainable Applications]] — defines the three
  quality axes the whole book optimizes for.
- [[Ch 02 - Data Models and Query Languages]] — relational vs document vs graph
  models, and declarative querying.
- [[Ch 03 - Storage and Retrieval]] — storage engine internals: hash indexes,
  [[SSTables and LSM-Trees]], [[B-Trees]], column stores.
- [[Ch 04 - Encoding and Evolution]] — serialization formats and
  [[Schema Evolution]] for rolling upgrades.

## Related
- [[Home]] · next: [[Part II - Distributed Data]]
