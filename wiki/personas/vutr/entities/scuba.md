---
persona: vutr
kind: entity
sources:
- raw/meta-data-stack-and-infrastructure/how-did-meta-modernize-their-lakehouse.md
- raw/meta-data-stack-and-infrastructure/groupby-44-meta-the-data-stack.md
last_updated: '2026-07-15'
qc: passed
slug: scuba
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Scuba is Meta's real-time analytics framework, used by data and software engineers to analyze trends in live logging data and by production engineers for debugging. It wasn't originally built for the warehouse: before Meta's Shared Foundations effort, Hive's architecture had no path for real-time ingestion, so Meta repurposed Scuba — a system "initially built for log analytics" — to fill that gap, alongside Presto, Raptor, and Cubrick as the four interactive-query engines the Shared Foundations program later tried to converge into one.

*See also: [[shared-foundations-consolidation]] · [[meta-internal-data-stack-overview]]*
