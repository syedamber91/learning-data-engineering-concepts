---
persona: vutr
kind: entity
sources:
- raw/lakehouse-architecture-and-practical-builds/the-data-lake-warehouse-and-lakehouse.md
- raw/lakehouse-architecture-and-practical-builds/data-architecture-101.md
- raw/lakehouse-architecture-and-practical-builds/do-we-need-the-lakehouse-architecture.md
last_updated: '2026-07-15'
qc: passed
slug: data-warehouse
topics:
- data-architecture-warehouse-lake-lakehouse-mesh-lambda-kappa
- history-of-data-engineering
---

Vu frames the data warehouse through a growth story rather than a formal definition: a company starts with one transactional database, an analyst extracts from it directly, then a third-party service is added and joins/aggregates still work by hand. But once the product grows into many services and external tools, each generating its own data, pulling from every source separately and combining it manually stops being possible — that's the moment a centralized repository becomes necessary. Bill Inmon called this centralized place the data warehouse (this is data architecture's *centralized* branch, as opposed to the domain-owned [[data-mesh]]): a "place" that is the source of truth for ingestion, storage, processing, and serving, usually run by a centralized team.

Early implementations were relational data warehouses built on transactional-style databases never designed for analytical workloads; the 2000s–2010s OLAP-database boom, paired with cloud pay-as-you-go pricing, made warehousing more performant and cost-effective. Data is loaded schema-on-write — extracted from sources, transformed into a predefined structure, and loaded — which is exactly what makes the warehouse query-ready but also what earns it a bad reputation: it was designed to accept only structured data, and once video, audio, and text documents entered the picture, unstructured data caused it real trouble (Vu notes modern warehouses like Snowflake and BigQuery have since added support for storing and retrieving unstructured data directly, softening this critique). This structured-only limitation is the direct motivation for the [[data-lake]] that emerged alongside it, and the two were stitched together into the two-tier lake-plus-warehouse pattern that Vu says dominated from the mid-2000s to the 2020s, before the [[lakehouse]] tried to collapse them back into one system.

*See also: [[data-lake]] · [[kappa-architecture]] · [[lambda-architecture]] · [[data-mesh]] · [[medallion-architecture]] · [[lakehouse]]*

## Related in the other wiki
- [[Data Warehousing]] — DDIA's account of the warehouse as a read-only analytical copy of OLTP data loaded via ETL, with its own column-oriented storage internals distinct from OLTP's; Vu's growth-story framing (why a centralized repo becomes necessary once sources multiply) is the practitioner-level motivation behind the same abstraction.
