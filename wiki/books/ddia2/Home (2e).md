---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: home
tags: [ddia2, moc]
---
# Designing Data-Intensive Applications, 2nd Edition — Vault Home

Study-notes vault for Martin Kleppmann and Chris Riccomini's *Designing
Data-Intensive Applications*, 2nd edition (O'Reilly). Every chapter → topic →
subtopic from the book's own table of contents has its own synthesized note;
cross-cutting ideas live in `concepts/`. Notes are original-wording syntheses
for personal study — not excerpts of the book.

Every file in this tree carries a **` (2e)`** filename suffix so its wikilinks stay
unambiguous alongside the 1st edition vault at [[Home|DDIA 1st edition]]. Headings
inside the notes are unsuffixed.

**The book's arc.** The 2nd edition drops the 1st edition's three Parts and runs as
fourteen chapters: architectural trade-offs and nonfunctional requirements → data
models, storage engines, and encoding → replication, sharding, and transactions →
the distributed-systems troubles and the consensus that answers them → batch and
stream processing, a philosophy for integrating them, and finally the ethics of
building any of it.

## Chapters
| # | Chapter | 1st edition counterpart |
|---|---------|-------------------------|
| 1 | [[Ch 01 - Trade-Offs in Data Systems Architecture (2e)]] | [[Ch 01 - Reliable, Scalable, and Maintainable Applications]] (split) |
| 2 | [[Ch 02 - Defining Nonfunctional Requirements (2e)]] | [[Ch 01 - Reliable, Scalable, and Maintainable Applications]] (split) |
| 3 | [[Ch 03 - Data Models and Query Languages (2e)]] | [[Ch 02 - Data Models and Query Languages]] |
| 4 | [[Ch 04 - Storage and Retrieval (2e)]] | [[Ch 03 - Storage and Retrieval]] |
| 5 | [[Ch 05 - Encoding and Evolution (2e)]] | [[Ch 04 - Encoding and Evolution]] |
| 6 | [[Ch 06 - Replication (2e)]] | [[Ch 05 - Replication]] |
| 7 | [[Ch 07 - Sharding (2e)]] | [[Ch 06 - Partitioning]] (renamed) |
| 8 | [[Ch 08 - Transactions (2e)]] | [[Ch 07 - Transactions]] + 2PC from [[Ch 09 - Consistency and Consensus]] |
| 9 | [[Ch 09 - The Trouble with Distributed Systems (2e)]] | [[Ch 08 - The Trouble with Distributed Systems]] |
| 10 | [[Ch 10 - Consistency and Consensus (2e)]] | [[Ch 09 - Consistency and Consensus]] |
| 11 | [[Ch 11 - Batch Processing (2e)]] | [[Ch 10 - Batch Processing]] |
| 12 | [[Ch 12 - Stream Processing (2e)]] | [[Ch 11 - Stream Processing]] |
| 13 | [[Ch 13 - A Philosophy of Streaming Systems (2e)]] | [[Ch 12 - The Future of Data Systems]] (renamed) |
| 14 | [[Ch 14 - Doing the Right Thing (2e)]] | [[Doing the Right Thing]] (promoted from a section) |

There are **no Part divisions** in the 2nd edition. The 1st edition's
[[Part I - Foundations of Data Systems]], [[Part II - Distributed Data]], and
[[Part III - Derived Data]] were dropped.

## What changed between editions
Every note in this vault ends with a **"Since the 1st Edition"** section, and links
to its 1st-edition counterpart. The headline structural changes:

- **Chapter 1 became two chapters.** Architectural trade-offs (cloud vs. self-hosting,
  distributed vs. single-node, operational vs. analytical) split from the nonfunctional
  requirements themselves (reliability, scalability, maintainability).
- **"Partitioning" is now "Sharding"** throughout, freeing "partition" for the network kind.
- **Distributed transactions and 2PC moved** out of the consistency chapter and into
  [[Ch 08 - Transactions (2e)]], where they belong.
- **"The Future of Data Systems" became [[Ch 13 - A Philosophy of Streaming Systems (2e)]]**,
  and the ethics material it carried was promoted into a chapter of its own.
- **MapReduce is declared largely obsolete**, kept for its concepts rather than its practice.
- **Genuinely new material**: vector search and embeddings, sync engines and local-first
  software, cloud data warehouses and the lakehouse, object storage displacing HDFS,
  the separation of storage and compute, and a far stronger case for single-node systems.

## Concept hubs
Cross-chapter ideas: [[Replication (2e)]], [[Sharding (2e)]], [[Consensus (2e)]],
[[Linearizability (2e)]], [[Causality (2e)]], [[Quorum (2e)]], [[ACID (2e)]],
[[Serializability (2e)]], [[Snapshot Isolation (2e)]], [[Two-Phase Commit (2e)]],
[[Write-Ahead Log (2e)]], [[LSM-Trees (2e)]], [[B-Trees (2e)]],
[[Column-Oriented Storage (2e)]], [[Change Data Capture (2e)]],
[[Event Sourcing (2e)]], [[Exactly-Once Semantics (2e)]], [[Idempotence (2e)]],
[[Backpressure (2e)]], [[Apache Kafka (2e)]], [[MapReduce (2e)]],
[[Derived Data (2e)]], [[Object Storage (2e)]],
[[Separation of Storage and Compute (2e)]], [[Vector Search (2e)]],
[[Sync Engines (2e)]] — full set in the `concepts/` folder.

## Provenance
- `raw/` — the book's own text, converted from the local PDF with Microsoft
  `markitdown` and split by chapter. This is the receipt layer: every note's
  frontmatter names the `raw/chNN.md` it was synthesized from.
- `index.yaml` — machine-readable map of every note to its sources.

## Log
- [[log (2e)|Ingestion Log]]
