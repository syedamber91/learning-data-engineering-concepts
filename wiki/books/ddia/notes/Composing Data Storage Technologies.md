---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 12
chapter_title: The Future of Data Systems
topic: Unbundling Databases
type: subtopic
tags: [ddia, unbundled-database, federation, event-log]
sources:
  - raw/ch12.md
---
# Composing Data Storage Technologies

> The features inside a database — indexes, views, replication logs — can be rebuilt *between* databases, with an event log as the synchronization spine.

## The Idea
Databases bundle several derivation facilities: [[Secondary Indexes]], [[Materialized Views]], replication logs, full-text search. Chapters 10–11 showed people rebuilding exactly these facilities *outside* the database with batch and stream processors. Kleppmann's reasoning: running `CREATE INDEX` makes a database snapshot a table, backfill the index, then apply the ongoing write stream — which is structurally the same operation as [[Setting Up New Followers]] or bootstrapping [[Change Data Capture]]. So organization-wide dataflow already behaves like one huge database, with every ETL/stream pipeline acting as an index-maintenance subroutine. Batch and stream processors are elaborate, distributed implementations of triggers and view-refresh routines, run by different teams on different machines.

## How It Works
Starting from the premise that no single data model fits all access patterns, two composition strategies emerge:
- **Federation (unifying reads)**: one query interface over many storage engines — the *polystore* idea, e.g. PostgreSQL foreign data wrappers. Relational in spirit: elegant high-level semantics, complicated implementation.
- **Unbundling (unifying writes)**: make it easy to reliably propagate every change to every system that needs it, via CDC and event logs — the database's index-maintenance machinery, extracted and generalized. Unix in spirit: small tools composed over a uniform low-level interface.
Kleppmann judges write synchronization the harder and more valuable problem. His preferred mechanism is an asynchronous ordered log with idempotent consumers ([[Idempotence]]) rather than distributed transactions across heterogeneous stores: without a standard transaction protocol spanning technologies from different teams, [[Two-Phase Commit]] integration is impractical, whereas a log is a simple abstraction anything can consume.

## Trade-offs & Pitfalls
- Log-based integration buys **loose coupling** twice over: a slow or crashed consumer only builds up buffered log entries (fault containment; catch-up later), where synchronous transactions escalate local faults into system-wide failures; and teams can own components independently behind the log interface.
- Unbundling is *not* a database replacement — you still need stores to hold stream-processor state and serve query results, and specialized engines (MPP warehouses) still win on their home workloads.
- More moving parts means more learning curves and operational quirks; a single integrated product is often faster and more predictable. If one product covers your needs, use it — unbundling targets breadth of workloads, not depth, and premature composition is premature optimization.
- **What's missing**: an unbundled equivalent of the Unix shell — a declarative way to say, in effect, "pipe this database into that search index" and have precomputed, continuously maintained views (even over graphs and application logic) appear automatically. Differential dataflow research points in this direction.

## Examples & Systems
PostgreSQL foreign data wrappers (federation); CDC/event-log pipelines maintaining search indexes; MPP data warehouses as still-integrated specialists; differential dataflow as early research; the hypothetical MySQL-to-Elasticsearch "pipe" as the aspirational interface.

## Related
- up: [[Unbundling Databases]] · chapter: [[Ch 12 - The Future of Data Systems]]
- [[The Unix Philosophy]] — composable small tools tradition unbundling inherits
- [[Change Data Capture]] — the extraction mechanism for write synchronization
- [[Keeping Systems in Sync]] — the Ch 11 problem this composition solves
- [[Comparing Hadoop to Distributed Databases]] — breadth-over-depth argument's origin
