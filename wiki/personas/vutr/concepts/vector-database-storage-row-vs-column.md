---
persona: vutr
kind: concept
sources:
- raw/llms-ai-agents-and-vector-databases-additional/i-spent-8-hours-learning-about-vector.md
last_updated: '2026-07-15'
qc: passed
slug: vector-database-storage-row-vs-column
topics:
- llms-ai-agents-and-vector-databases
---

Every database engine picks one of row, column, or hybrid physical layout, and the standard rule of thumb is that row favors OLTP (point lookups, random access, reading a whole row) while column and hybrid favor OLAP (scanning many rows but only a few columns, where skipping unneeded columns saves I/O). The question the source sets out to answer is which side [[vector-embedding|vector embedding]] workloads land on — and the honest answer given is "it depends, and it's still being worked out," because vector databases are a new enough category that the field hasn't converged.

**The case for row.** The typical vector workload is: find related vectors given an input vector, then return the whole matching record — the complete document or image plus its metadata — not just a couple of columns. That access pattern favors storing the vector and its associated data close together and loading the entire record on a match, which is why row store is a legitimate fit here, and why several vector databases adopt it. Weaviate is named as one example: it stores data as a key-value store on an LSM tree, where writes first land in an in-memory Memtable, and once that fills up it flushes to disk as an immutable, sorted SSTable, with SSTables later compacted into larger ones to improve read performance. ChromaDB is the second named example, and its story is a concrete admission rather than a clean design choice: it uses SQLite (row-oriented) under the hood, but the source notes ChromaDB's own maintainers originally built on DuckDB — a columnar OLAP engine — before conceding that an OLTP-style engine actually suited their retrieval workload better.

**The case for column/hybrid.** The counter-pressure is that a vector database's end users — typically data scientists — also run ordinary analytical workloads, and nothing beats a genuine OLAP engine at that job; running both a dedicated vector store and a separate analytics warehouse means maintaining two systems. LanceDB is named as the vendor answering this by building a multi-purpose system on a purpose-built new columnar format (Lance) rather than reusing Parquet. That substitution matters because standard columnar formats like Parquet are described as a poor fit for vector data specifically: Parquet is weak at random access, and the wide columns that vector embeddings produce make Parquet's row-group sizing difficult to tune. The lakehouse paradigm's promise of one shared storage layer queryable by any engine breaks down here — loading data into a dedicated vector database for performance means giving up that shared-storage property — which is presented as the reason multiple new columnar formats are emerging at once to compete with Parquet on this specific workload: Lance (from LanceDB), Nimble (from Meta), and F3 (from an unnamed group of researchers), all trying to outperform Parquet for vector or AI workloads generally.

The unresolved tension — row's fit for whole-record retrieval versus column's fit for shared analytical access, and Parquet's incumbency versus a wave of new formats trying to unseat it for this one workload — is exactly why the source declines to give a single verdict and instead frames this as an open architectural question the vector-database market is still answering.

*See also: [[vector-embedding]] · [[approximate-nearest-neighbor-search]] · [[vector-quantization-and-compression]]*
