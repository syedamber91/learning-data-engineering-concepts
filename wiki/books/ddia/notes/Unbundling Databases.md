---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 12
chapter_title: The Future of Data Systems
type: topic
tags: [ddia, unbundled-database, dataflow, architecture]
sources:
  - raw/ch12.md
---
# Unbundling Databases

Databases, [[Hadoop]], and operating systems are all information-management systems, but Unix and the relational model embody opposite philosophies: thin low-level abstractions versus high-level declarative power. Kleppmann's synthesis is to "unbundle" the database — take the internal machinery that keeps indexes and [[Materialized Views]] consistent, and re-implement it across an organization using event logs, batch jobs, and stream processors, so that many specialized storage systems compose into one coherent whole. The chapter then pushes the idea outward: application code becomes derivation functions running as stream operators ([[Dataflow]] instead of request/response), and the write path can extend all the way to end-user devices, making UIs subscribing caches of server state.

## Subtopics
- [[Composing Data Storage Technologies]] — CREATE INDEX as reprocessing; federation (unifying reads) vs unbundling (unifying writes); why async logs beat distributed transactions for cross-system sync.
- [[Designing Applications Around Dataflow]] — the "database inside-out" pattern: application code as derivation functions, stream operators replacing RPC calls, spreadsheet-like reactivity for data systems.
- [[Observing Derived State]] — write path meets read path; caches and indexes as movable boundaries; offline-first stateful clients; reads as events.

## Key Takeaways
- Whole-organization dataflow already looks like one giant database: every ETL/batch/stream pipeline is a trigger or index-maintenance routine writ large.
- Federated databases unify querying (relational tradition); unbundled databases unify write synchronization (Unix tradition) — writes are the harder engineering problem.
- An ordered event log with idempotent consumers is a looser, more fault-containing coupling than [[Two-Phase Commit]] across heterogeneous systems, both technically and organizationally.
- Unbundling only pays when no single product covers your needs; it targets breadth of workloads, not beating one database at its specialty.
- The missing piece is a declarative "Unix shell" for composing storage systems (imagine piping a database into a search index as one command); differential dataflow research points that way.
- Stable ordering and fault-tolerant processing — not traditional messaging's redelivery semantics — are the prerequisites for maintaining [[Derived Data]].

## Related
- chapter: [[Ch 12 - The Future of Data Systems]] · part: [[Part III - Derived Data]]
- [[Data Integration]] — the problem unbundling is designed to solve
- [[Databases and Streams]] — Ch 11 groundwork: the change log as first-class citizen
- [[The Unix Philosophy]] — composable small tools, the unbundled tradition
- [[Aiming for Correctness]] — how to keep unbundled dataflow correct
