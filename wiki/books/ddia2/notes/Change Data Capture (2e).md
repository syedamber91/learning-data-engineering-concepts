---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 12
chapter_title: Stream Processing
topic: Databases and Streams
type: subtopic
tags: [ddia2, cdc, debezium, log-compaction, outbox-pattern, snapshot, data-contract]
sources:
  - raw/ch12.md
---
# Change Data Capture
> Make the database the leader and everything else a follower. The mechanism was always there — the replication log — it just wasn't a public API.

## The Idea
**The problem with most databases' replication logs is that they have long been considered an internal implementation detail, not a public API.** **Clients are supposed to query through the data model and query language, not parse replication logs.** **For decades many databases simply had no documented way of getting the log of changes**, making it difficult to replicate all changes to a different storage technology.

**More recently there has been growing interest in change data capture (CDC): observing all data changes written to a database and extracting them in a form that can be replicated to other systems.** **CDC is especially interesting if changes are made available as a stream, immediately as they are written.**

**Capture the changes and continually apply them to a search index; if applied in the same order, the index data matches the database.** **The index and any other derived systems are just consumers of the change stream.** **The dual-writes race condition is solved: even though the two requests arrive concurrently, the database decides the order, writes them to its replication log in that order, and the index applies them in the same order.** **Need the data somewhere else too? Simply add another consumer.**

## How It Works
**CDC essentially makes one database the leader — the one from which changes are captured — and turns the others into followers.** **A log-based message broker is well suited for transporting the change events, since it preserves message ordering.**

**Logical (row-based) replication logs can implement CDC**, though with challenges such as **handling schema changes and properly modeling updates.** **The Debezium open source project addresses these**, containing **source connectors for MySQL, PostgreSQL, Oracle, SQL Server, Db2, Cassandra, and many others** that **attach to replication logs and surface changes in a standard event schema.** **The Kafka Connect framework offers CDC connectors too; Maxwell parses the MySQL binlog, GoldenGate does Oracle, and pgcapture does PostgreSQL.**

**Like message brokers, CDC is usually asynchronous**: **the source database does not wait for a change to reach consumers before committing.** **This means adding a slow consumer doesn't affect the system of record much — but all the issues of replication lag apply.**

**Initial snapshot.** **With the log of all changes ever made you could reconstruct the entire database by replaying it. But keeping all changes forever would require too much disk space and replaying would take too long, so the log is truncated.** **Building a new full-text index requires a full copy — applying only recent changes would miss items not recently updated.** **So without the entire history you need to start from a consistent snapshot**, and **the snapshot must correspond to a known position or offset in the change log** so you know where to start applying changes. **Some CDC tools integrate this; others leave it manual.** **Debezium uses Netflix's DBLog watermarking algorithm to provide incremental snapshots.**

**Log compaction.** **If you can keep only limited history you must snapshot every time you add a derived system — but log compaction provides a good alternative.** **The principle: the storage engine periodically looks for log records with the same key, throws away duplicates, and keeps only the most recent update for each key**, making segments much smaller and allowing them to be merged, all in the background. **An update with a special null value — a tombstone — indicates deletion and causes removal during compaction. As long as a key is not overwritten or deleted, it stays in the log forever.** **So the disk space for a compacted log depends only on the current contents of the database, not the number of writes ever made.**

**The same idea works for log-based brokers and CDC.** **If every change has a primary key and every update replaces the previous value for that key, it's sufficient to keep just the most recent write per key.** **Then to rebuild a derived system you start a new consumer from offset 0 of the log-compacted topic and scan all messages: the log is guaranteed to contain the most recent value for every key** (and maybe some older values), **so you can obtain a full copy of the database contents without taking another snapshot.** **Kafka supports this, letting the broker be used for durable storage, not just transient messaging.**

**API support for change streams.** **Most popular databases now expose change streams as a first-class interface, rather than the retrofitted and reverse-engineered CDC of the past.** **MySQL and PostgreSQL send changes through the same replication log they use for their own replicas**, and **most cloud vendors offer CDC solutions** — **Datastream for Google Cloud's databases and warehouses.**

**Even eventually consistent, quorum-based databases such as Cassandra now support CDC.** **This is challenging because there's no single source of truth to subscribe to** — **whether data is visible depends on each reader's consistency preferences.** **Cassandra sidesteps this by exposing raw log segments for each node rather than a single stream of mutations**, so **consumers must read each node's segments and decide how to merge them, much as a quorum reader does.**

## Trade-offs & Pitfalls
**CDC versus event sourcing.** Both store all changes as a log of change events; **the biggest difference is the level of abstraction:**
- **In CDC the application uses the database in a mutable way**, updating and deleting at will, and **the change log is extracted at a low level** — ensuring the extracted order matches the actual write order and avoiding the dual-writes race.
- **In event sourcing the application logic is explicitly built on immutable events written to an event log.** **The store is append-only, updates and deletes are discouraged or prohibited, and events reflect things that happened at the application level rather than low-level state changes.**

**Which is better depends on your situation.** **Adopting event sourcing is a big change for an application not already doing it.** **In contrast, CDC can be added to an existing database with minimal changes — the application writing to the database might not even know CDC is occurring.**

**Log compaction differs between the two.** **A CDC update event typically contains the entire new version of the record, so the current value for a key is entirely determined by the most recent event and compaction can discard earlier ones.** **With event sourcing, events are modeled at a higher level, typically expressing the intent of a user action rather than the mechanics of the state update — so later events don't override prior ones and you need the full history to reconstruct the final state. Log compaction is not possible in the same way.** **Event-sourced applications typically store snapshots of derived state so they needn't reprocess the full log** — **but this is only a performance optimization; the intention is that the system can store all raw events forever and reprocess them whenever required.**

> **CDC and database schemas.** **Though CDC appears easier to adopt than event sourcing, it has its own challenges.** **In a microservices architecture a database is typically accessed by only one service, with others going through its public API — making the database an internal implementation detail whose schema developers can change freely.** **But CDC systems typically use the upstream database's schema when replicating, which turns those schemas into public APIs that must be managed like the service's public API.** **Removing a column will break downstream consumers depending on that field.** **Such challenges always existed with data pipelines, but typically impacted only warehouse ETL — since CDC is often a data stream, other production services might be consumers, and breaking them can cause a customer-facing outage.** **Data contracts are often used to prevent these breakages.**
>
> **A common way to decouple internal from external schemas is the outbox pattern**: **outboxes are tables with their own schemas, exposed to the CDC system rather than the internal domain model.** **Developers can then modify internal schemas freely while leaving outbox tables untouched.** **This might look like a dual write — it is** — **but outboxes avoid the dual-writes problems by keeping both writes in the same system, so both appear in a single transaction.** **The trade-offs: developers must maintain the transformation between internal and outbox schemas, which can be challenging, and an outbox increases the data the database writes to storage, which might trigger performance problems.**

## Examples & Systems
Debezium (with DBLog watermarking), Kafka Connect, Maxwell, GoldenGate, pgcapture; Datastream for Google Cloud; Cassandra's per-node raw log segments; Kafka log compaction.

## Since the 1st Edition
The 1st edition's [[Change Data Capture]] covered the same concept, the same leader/follower reframing, initial snapshots, log compaction, and the CDC-versus-event-sourcing comparison. **New:** **Debezium's DBLog watermarking** for incremental snapshots; **first-class change-stream APIs** now shipping in mainstream databases and clouds; **CDC for quorum databases** like Cassandra, with its per-node-segments workaround; and — most practically — **the entire CDC-and-database-schemas box**, covering the accidental-public-API problem, **data contracts**, and **the outbox pattern with its honest admission that it is a dual write made safe by staying in one transaction.**

## Related
- up: [[Databases and Streams (2e)]] · chapter: [[Ch 12 - Stream Processing (2e)]]
- [[Keeping Systems in Sync (2e)]] — the problem this solves
- [[Implementation of Replication Logs (2e)]] — the logical log CDC reads
- [[Event Sourcing and CQRS (2e)]] — the higher-abstraction alternative
- 1st edition: [[Change Data Capture]] — the same subtopic

## In the vutr data-engineering wiki
- [[change-data-capture-cdc-and-data-sourcing]] — vutr sorts the trigger-based and log-based extraction mechanisms onto a clean complexity/impact spectrum, and adds the DELETE-blindness failure mode of query-based CDC that the book doesn't cover.
- [[log-based-cdc]] — the log-based approach specifically — lowest source impact, highest coupling to internal formats — with the WAL/redo-log/binlog naming and the Debezium-to-Kafka pipeline shape.
