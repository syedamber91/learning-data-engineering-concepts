---
book: Designing Data-Intensive Applications
type: home
tags: [ddia, moc]
---
# Designing Data-Intensive Applications — Vault Home

Study-notes vault for Martin Kleppmann's *Designing Data-Intensive Applications*
(O'Reilly, 2017). Every chapter → topic → subtopic from the book's table of contents
has its own synthesized note; cross-cutting ideas live in `concepts/`. Notes are
original-wording syntheses for personal study — not excerpts of the book.

The book's arc: single-node foundations (data models, storage engines, encoding) →
distributed data (replication, partitioning, transactions, faults, consensus) →
derived data (batch, streams, and the future of dataflow-centric systems).

## Parts
1. [[Part I - Foundations of Data Systems]] — Ch 1–4
2. [[Part II - Distributed Data]] — Ch 5–9
3. [[Part III - Derived Data]] — Ch 10–12

## Chapters
| # | Chapter |
|---|---------|
| 1 | [[Ch 01 - Reliable, Scalable, and Maintainable Applications]] |
| 2 | [[Ch 02 - Data Models and Query Languages]] |
| 3 | [[Ch 03 - Storage and Retrieval]] |
| 4 | [[Ch 04 - Encoding and Evolution]] |
| 5 | [[Ch 05 - Replication]] |
| 6 | [[Ch 06 - Partitioning]] |
| 7 | [[Ch 07 - Transactions]] |
| 8 | [[Ch 08 - The Trouble with Distributed Systems]] |
| 9 | [[Ch 09 - Consistency and Consensus]] |
| 10 | [[Ch 10 - Batch Processing]] |
| 11 | [[Ch 11 - Stream Processing]] |
| 12 | [[Ch 12 - The Future of Data Systems]] |

## Concept hubs
Cross-chapter ideas: [[Replication]], [[Partitioning]], [[Consensus]],
[[Causality]], [[Quorum]], [[ACID]], [[Isolation Levels]], [[CAP Theorem]],
[[Two-Phase Commit]], [[Write-Ahead Log]], [[MapReduce]], [[Derived Data]],
[[Exactly-Once Semantics]], [[Apache Kafka]], [[ZooKeeper]] — full set in the
`concepts/` folder.

## Log
- [[log|Ingestion Log]]
