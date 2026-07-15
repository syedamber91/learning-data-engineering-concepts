---
persona: vutr
kind: entity
sources:
- raw/uber-data-infrastructure-case-studies/groupby-30-uber-how-ledgerstore-supports.md
- raw/uber-data-infrastructure-case-studies/groupby-31-migrating-a-trillion-entries.md
last_updated: '2026-07-15'
qc: passed
slug: uber-ledgerstore
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

LedgerStore (LSG) is Uber's append-only, ledger-style database, built to power a petabyte-scale index storage footprint of trillions of indexes for Uber's business-critical ledger data. Uber migrated this ledger data onto LedgerStore from DynamoDB, moving more than a trillion entries — a few petabytes of data — transparently and without disruption to production traffic.

**source gap**: both captured posts are newsletter-digest teasers linking to Uber's original engineering blog posts; neither explains LedgerStore's actual indexing architecture, its consistency/replication model, or the mechanics of the DynamoDB migration itself (how writes were dual-directed, how correctness was verified, or what made "trillions of indexes" specifically hard) — only that the migration happened at that scale and didn't cause disruption.

*See also: [[uber-data-platform]] · [[uber-hudi-etl-pipeline-and-impact]]*
