---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 13
chapter_title: A Philosophy of Streaming Systems
topic: Unbundling Databases
type: subtopic
tags: [ddia2, federated-database, polystore, trino, create-index, meta-database]
sources:
  - raw/ch13.md
---
# Composing Data Storage Technologies
> `CREATE INDEX` is a batch job. Once you see that, the dataflow across an entire organization starts looking like one huge database.

## The Idea
The book has discussed several features provided by databases: **secondary indexes**, letting you efficiently search records by field value; **materialized views**, a kind of precomputed cache of query results; **replication logs**, keeping copies on other nodes up to date; and **full-text search indexes**. **In Chapters 11 and 12 similar themes emerged — building full-text search indexes, maintaining materialized views, replicating changes to derived systems via CDC.** **There are parallels between the features built into databases and the derived data systems people build with batch and stream processors.**

## How It Works
**Creating an index.** **Think about what happens when you run `CREATE INDEX`.** **The database scans a consistent snapshot of the table, picks out all the field values being indexed, sorts them, and writes out the index.** **Then it processes the backlog of writes made since the snapshot was taken** (assuming the table wasn't locked, so writes could continue). **Then it keeps the index up to date whenever a transaction writes to the table.**

**This is remarkably similar to setting up a new follower replica, and also very similar to bootstrapping CDC in a streaming system.** **Whenever you run `CREATE INDEX`, the database essentially reprocesses the existing dataset and derives the index as a new view onto the existing data.** **The existing data may be a snapshot of state rather than a log of all changes, but the two are closely related.**

**The meta-database of everything.** **In this light, the dataflow across an entire organization starts looking like one huge database.** **Whenever a batch, stream, or ETL process transports data from one place and form to another, it is acting like the database subsystem that keeps indexes or materialized views up to date.**

**Viewed like this, batch and stream processors are like elaborate implementations of triggers, stored procedures, and materialized view maintenance algorithms, and the derived data systems they maintain are like different index types.** **A relational database may support B-tree, hash, spatial, and other index types; in the emerging architecture of derived data systems, instead of implementing those as features of one integrated product, they are provided by various pieces of software running on different machines, administered by different teams.**

**Starting from the premise that no single data model or storage format suits all access patterns, there are two avenues for composing different tools into a cohesive system:**

**Federated databases (unifying reads).** **Provide a unified query interface to a wide variety of underlying storage engines and processing methods — a federated database or polystore.** **PostgreSQL's foreign data wrapper feature fits this pattern, as do federated query engines such as Trino, Hoptimator, and Xorq.** **Applications needing a specialized data model or query interface can still access the underlying engines directly, while users wanting to combine data from disparate places can do so through the federated interface.** **This follows the relational tradition of a single integrated system with a high-level query language and elegant semantics, but a complicated implementation.**

**Unbundled databases (unifying writes).** **Federation addresses read-only querying but has no good answer to synchronizing writes.** **Within a single database, creating a consistent index is a built-in feature; when composing several storage systems we similarly need to ensure all data changes end up in all the right places, even in the face of faults.** **Making it easier to reliably plug together storage systems — through CDC and event logs — is like unbundling a database's index maintenance features in a way that can synchronize writes across disparate technologies.** **This follows the Unix tradition of small tools that do one thing well, communicate through a uniform low-level API (pipes), and can be composed using a higher-level language (the shell).**

## Trade-offs & Pitfalls
**Making unbundling work.** **Federation and unbundling are two sides of the same coin.** **Federated read-only querying requires mapping one data model into another, which takes thought but is ultimately quite manageable.** **Keeping writes to several systems in sync is the harder engineering problem.**

**The traditional approach requires distributed transactions across heterogeneous systems, which are problematic.** **Transactions within a single storage or stream processing system are feasible, but when data crosses the boundary between technologies, an asynchronous event log with idempotent writes is a much more robust and practicable approach.** **Distributed transactions are used within some stream processors to achieve exactly-once semantics and work quite well — but when a transaction must involve systems written by different groups of people, the lack of a standardized transaction protocol makes integration much harder.** **An ordered log of events with idempotent consumers is a much simpler abstraction and much more feasible across heterogeneous systems.**

**The big advantage of log-based integration is loose coupling, in two ways:**
- **At a system level, asynchronous event streams make the system more robust to outages or performance degradation of individual components.** **If a consumer runs slow or fails, the log buffers messages, letting the producer and other consumers continue unaffected; the faulty consumer catches up when fixed, so it doesn't miss data, and the fault is contained.** **By contrast, the synchronous interaction of distributed transactions tends to escalate local faults into large-scale failures.**
- **At a human level, unbundling allows components and services to be developed, improved, and maintained independently by different teams.** **Specialization lets each team focus on doing one thing well with well-defined interfaces.** **Event logs provide an interface powerful enough to capture fairly strong consistency properties — because of durability and ordering — but general enough to apply to almost any kind of data.**

**Unbundled versus integrated systems.** **If unbundling becomes the way of the future, it will not replace databases in their current form.** **They will still be needed for maintaining state in stream processors and serving queries for batch and stream output**, and **specialized query engines will continue to matter — warehouse engines are optimized for exploratory analytical queries and handle that workload very well.**

**The complexity of running several pieces of infrastructure can be a problem.** **Each piece has a learning curve, configuration issues, and operational quirks, so it is worth deploying as few moving parts as possible.** **A single integrated product may also achieve better and more predictable performance on the workloads it is designed for.** **Building for scale you don't need is wasted effort and may lock you into an inflexible design — in effect, a form of premature optimization.**

**The goal of unbundling is not to compete with individual databases on performance for particular workloads; the goal is to let you combine several databases to achieve good performance for a much wider range of workloads than one piece of software allows. It's about breadth, not depth.** **So if a single technology does everything you need, you're most likely best off simply using it rather than reimplementing it from lower-level components.** **The advantages of unbundling come into the picture only when no single piece of software satisfies all your requirements.**

## Examples & Systems
PostgreSQL foreign data wrappers; Trino, Hoptimator, Xorq as federated query engines; CDC and event logs as the unbundling mechanism.

## Since the 1st Edition
The 1st edition's [[Composing Data Storage Technologies]] made the same `CREATE INDEX`-as-batch-job argument, the same meta-database framing, the same federation-versus-unbundling split, and the same breadth-not-depth conclusion. **Updated:** the federated query engine examples now name **Trino, Hoptimator, and Xorq** — the 1st edition cited PostgreSQL foreign data wrappers and the academic polystore literature, since production federated engines were barely established.

## Related
- up: [[Unbundling Databases (2e)]] · chapter: [[Ch 13 - A Philosophy of Streaming Systems (2e)]]
- [[Change Data Capture (2e)]] — the mechanism that unifies writes
- [[Cloud Data Warehouses (2e)]] — unbundling that actually happened, in the warehouse stack
- [[Setting Up New Followers (2e)]] — the process `CREATE INDEX` resembles
- 1st edition: [[Composing Data Storage Technologies]] — the same subtopic
