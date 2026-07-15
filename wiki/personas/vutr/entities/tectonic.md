---
persona: vutr
kind: entity
sources:
- raw/meta-data-stack-and-infrastructure/how-did-meta-move-terabytes-of-data.md
- raw/meta-data-stack-and-infrastructure/how-did-meta-modernize-their-lakehouse.md
last_updated: '2026-07-15'
qc: passed
slug: tectonic
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Tectonic is the distributed filesystem Meta built to replace HDFS, adopted for "operational efficiency." It is the storage backbone for two different workloads: Meta's Hive-based data warehouse, and Scribe's Durable Data Store, where it holds message payloads. Rather than the fixed-replica-count model, Tectonic relies on erasure coding for data reliability — a lower storage footprint than naive replication, paid for with more resources needed to reconstruct data after a failure.

*See also: [[scribe]] · [[scribe-write-path-and-batching]] · [[shared-foundations-consolidation]]*
