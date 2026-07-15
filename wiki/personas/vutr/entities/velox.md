---
persona: vutr
kind: entity
sources:
- raw/meta-data-stack-and-infrastructure/how-did-meta-modernize-their-lakehouse.md
last_updated: '2026-07-15'
qc: passed
slug: velox
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Velox is the C++ database acceleration library Meta built to unify the more-than-twelve fragmented execution engines it had accumulated across Presto, Spark, and its streaming systems — the source explicitly likens it to Databricks's Photon for Spark. Velox receives a fully optimized query plan and executes it using the resources of the local machine; refactoring the DWIO storage-format library into Velox let Meta open-source it. By centralizing execution, Velox "democratizes" optimizations that used to live inside a single engine at a time, and it's also where Meta rebuilt its CoreSQL function library for performance.

*See also: [[shared-foundations-consolidation]] · [[coresql]] · [[presto-on-spark-architecture]]*
