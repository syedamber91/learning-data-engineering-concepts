---
persona: vutr
kind: entity
sources:
- raw/lakehouse-architecture-and-practical-builds/build-a-lakehouse-on-a-laptop-with.md
last_updated: '2026-07-15'
qc: passed
slug: trino
topics:
- data-architecture-warehouse-lake-lakehouse-mesh-lambda-kappa
---

Trino is the query engine Vu chose for his laptop-scale [[lakehouse]] build ("Build a lakehouse on a laptop with dbt, Airflow, Trino, Iceberg, and MinIO"), specifically because of its support for a wide range of data sources through connectors — modules that carry the information Trino needs to talk to a given data source. A Trino cluster splits into a coordinator node, which parses, plans, and orchestrates queries, and worker nodes, which actually execute them; a node can technically act as both, but Vu follows the recommendation to dedicate one node solely to the coordinator role for optimal performance. His own setup runs one coordinator and two workers, each configured via its own `config.properties` file, with both roles requiring a `discovery.uri` so the worker knows which coordinator to report to and the coordinator knows its own accept endpoint.

Trino introduces its own notion of a *catalog* to represent a single data source — a name Vu is careful to flag as different from the Iceberg catalog (in his build, that's [[project-nessie]]). Each Trino catalog is tied to a connector; his `iceberg.properties` catalog file names Nessie as the catalog type, points at the Nessie container's endpoint and port, specifies the Nessie `ref` (branch, `main` in his setup) for its git-like versioning, and supplies the object-storage warehouse directory, endpoint, region, and credentials for MinIO. On top of Trino he ran an SQL init script that creates three schemas — landing, staging, curated — each schema mapping to a namespace in Nessie, which groups tables logically the way a schema does in Snowflake or a dataset does in BigQuery; each namespace's data physically lives under its own object-storage prefix (Vu notes explicitly that cloud object storage has no real folders — two objects sharing a `2025/` prefix only *look* like they're in a folder).

*See also: [[project-nessie]] · [[bauplan]] · [[lakehouse]] · [[lakehouse-build-decision-framework]]*

## Open questions
- **source gap**: the post shows the coordinator/worker config files and the Iceberg-catalog properties but doesn't explain how Trino's query planner decides work distribution across workers, or what happens operationally when a worker fails mid-query.
