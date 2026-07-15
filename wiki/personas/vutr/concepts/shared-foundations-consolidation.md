---
persona: vutr
kind: concept
sources:
- raw/meta-data-stack-and-infrastructure/how-did-meta-modernize-their-lakehouse.md
last_updated: '2026-07-15'
qc: passed
slug: shared-foundations-consolidation
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

By 2023 Meta's Hive-based lakehouse — started in 2010, eleven years before Databricks even coined the term "lakehouse" — had grown from tens of petabytes to multiple exabytes, and its architecture of independently scaled data, metadata, and compute had quietly produced a fragmentation problem: at least six SQL dialects, three separate implementations each of the Metastore client and the ORC codec, roughly twelve engines targeting overlapping workloads, and many redundant copies of the same data in different formats. None of this was one bad decision — it was the accumulated cost of a decade of every team bringing its own compute engine to the same Hive-managed data, compounded by Hive being too slow for interactive queries (which forced new, tightly-coupled compute-and-storage engines) and having no story at all for stream processing (which forced separate, poorly-integrated streaming systems built over time).

Meta's fix, the Shared Foundations program, was explicitly organizational as much as technical: hundreds of engineers working to "use fewer systems" (one query engine per workload class — batch, streaming, interactive, machine learning), build "reusable components" where full consolidation wasn't possible (shared storage encodings even across different compute engines), and enforce "consistent APIs" so moving between systems didn't mean relearning syntax and semantics. The named payoffs were engineering efficiency, faster innovation, and better user experience, and the program touched every layer: storage (unifying three fragmented ORC/DWRF codec implementations onto the fastest of the three — Presto's — and refactoring the DWIO library into the new [[velox]] execution engine), the SQL dialect (collapsing six variants down to two — MySQL for OLTP, PrestoSQL for OLAP — via the shared [[coresql]] parser-and-function-library pair), the execution engine itself ([[velox]] absorbing what had been twelve engines' worth of duplicated optimization logic), and the compute engines, where interactive query systems converged onto Presto and batch pipelines onto a new hybrid described in [[presto-on-spark-architecture]].

The consolidation wasn't cost-free migration theater. Deprecating two of the four interactive engines, Raptor and Cubrick, alone saved "several hundred thousand lines of code and several thousand machines," and the two-year interactive-query migration had to solve real syntactic incompatibilities between old dialects and PrestoSQL along the way — building a function-mapping layer flexible enough to translate every old query into a supported Presto query. The throughline is that Meta names reusability and consistency, not new features, as the direct source of both its cost savings and its later ability to focus on innovation rather than maintaining twelve engines in parallel.

*See also: [[coresql]] · [[velox]] · [[presto-on-spark-architecture]] · [[scuba]]*
