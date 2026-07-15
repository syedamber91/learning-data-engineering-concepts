---
persona: vutr
kind: entity
sources:
- raw/meta-data-stack-and-infrastructure/how-did-meta-modernize-their-lakehouse.md
last_updated: '2026-07-15'
qc: passed
slug: coresql
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

CoreSQL is Meta's answer to having accumulated more than six internal SQL dialects: a single standard dialect meant to work across engines, from Presto to the XStream streaming platform. Modeled on how Google achieved the same goal with ZetaSQL, CoreSQL needed two pieces — a SQL parser/analyzer (Meta rewrote its Python implementation in C++ for performance and integration with its C++ engines, and was working to bind its Java/Presto implementation to the same C++ library) and a library of query functions and operators (initially reused from Presto's Java implementation, then migrated onto Velox to maximize performance).

*See also: [[velox]] · [[shared-foundations-consolidation]] · [[presto-on-spark-architecture]]*
