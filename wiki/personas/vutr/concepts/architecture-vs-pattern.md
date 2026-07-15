---
persona: vutr
kind: concept
sources:
- raw/lakehouse-architecture-and-practical-builds/data-architecture-101.md
last_updated: '2026-07-15'
qc: passed
slug: architecture-vs-pattern
topics:
- data-architecture-warehouse-lake-lakehouse-mesh-lambda-kappa
---

Vu draws this line explicitly while sorting through the field's overloaded vocabulary: "the architecture is the high-level blueprint of how data is ingested, stored, processed, and served, while a pattern is a reusable solution to a specific problem in the architecture." He applies this test to every buzzword he covers rather than accepting vendor branding at face value: [[medallion-architecture]] is a pattern for organizing storage layers, not an architecture, and is not data modeling either; [[lambda-architecture]] and [[kappa-architecture]] are, in his words, "more like patterns than architectures, as they provide solutions for data processing and serving," not the full ingestion-to-serving blueprint. He extends the same skepticism sideways to two more terms that never quite earn "architecture" status in his account: Data Fabric ("more of a marketing term used by big players to sell their solution" — essentially the lake-plus-warehouse architecture with extra tooling for accessibility, discoverability, and security bolted on), and the Modern Data Stack ("more like a philosophy than an architecture" — a recommended set of modern cloud-native tools such as Fivetran, dbt, Dagster, and a cloud warehouse, rather than a blueprint in its own right).

The two genuine architectures in his taxonomy are the centralized [[data-warehouse]]/[[lakehouse]] line and the decentralized [[data-mesh]] — the two approaches he opens the whole piece with, before drilling into everything else as a pattern, philosophy, or marketing term layered on top of one of those two.

*See also: [[data-lake]] · [[data-warehouse]] · [[kappa-architecture]] · [[lambda-architecture]] · [[data-mesh]] · [[medallion-architecture]]*
