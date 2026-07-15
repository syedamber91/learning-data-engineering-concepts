---
persona: vutr
kind: entity
sources:
- raw/big-tech-case-studies-batch-2-apple-github-pinterest-canva/groupby-19-how-apple-built-icloud.md
last_updated: '2026-07-15'
qc: passed
slug: cloudkit
topics:
- big-tech-case-studies-batch-2-apple-github-pinterest-canva
---

CloudKit is Apple's cloud backend service — the infrastructure layer behind iCloud. Vu Trinh's GroupBy #19 curates a piece titled "How Apple built iCloud to store billions of databases," framing iCloud's scale challenge at the level of the database itself rather than the row or table: the claim is billions of separate databases, not billions of rows in one. The curated teaser names the two storage systems CloudKit is built on — Cassandra and FoundationDB — used together rather than either one alone.

What vutr's captured post actually establishes is narrow: CloudKit is a dual-database backend, and the scale target is in the billions of databases. The teaser itself says the linked piece "takes a look into how exactly each is used within their cloud and the problems they've solved," but that explanation — which workloads go to Cassandra versus FoundationDB, and why a single engine wasn't enough — lives in the external article, not in vutr's own words. Nothing in the captured post says which of the two systems handles which responsibility, or what "billions of databases" means structurally (one per user, one per app, one per record type).

*See also: [[github-merge-queue]] · [[rockstorewidecolumn]] · [[creator-content-usage-accounting-at-scale]]*
