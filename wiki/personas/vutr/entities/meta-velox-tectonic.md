---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: meta-velox-tectonic
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Meta holds multiple exabytes of warehouse data and fought sprawl by narrowing from twelve different engines and six SQL dialects down to two dialects — MySQL for OLTP and PrestoSQL for OLAP. It built Velox, a C++ database-acceleration library, replaced HDFS with Tectonic, and runs Scribe, an internal message queue built over 18 years that ingests over 15TB/s and serves over 110TB/s.
