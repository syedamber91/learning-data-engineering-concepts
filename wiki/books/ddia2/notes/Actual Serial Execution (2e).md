---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 8
chapter_title: Transactions
topic: Serializability
type: subtopic
tags: [ddia2, serial-execution, stored-procedures, voltdb, redis, state-machine-replication]
sources:
  - raw/ch08.md
---
# Actual Serial Execution
> Remove concurrency entirely and serializability is free by definition. Two things changed in the 2000s that made this viable: cheap RAM, and the realization that OLTP transactions are short.

## The Idea
**The simplest way of avoiding concurrency problems is to remove the concurrency**: execute one transaction at a time, in serial order, on a single thread. This **completely sidesteps detecting and preventing conflicts, and the resulting isolation is by definition serializable.**

Obvious as it sounds, **it was only in the 2000s that database designers decided a single-threaded transaction loop was feasible.** Two developments caused the rethink:
- **RAM became cheap enough** that for many use cases the entire active dataset fits in memory, so transactions execute much faster than when waiting for disk.
- **OLTP transactions are usually short and make only a small number of reads and writes.** Long-running analytical queries are typically read-only, so **they can run on a consistent snapshot outside the serial execution loop.**

Implemented in **VoltDB/H-Store, Redis, and Datomic**. A single-threaded system **can sometimes outperform a concurrent one, because it avoids the coordination overhead of locking — but its throughput is limited to a single CPU core.** To make the most of that thread, **transactions must be structured differently.**

## How It Works
**Encapsulating transactions in stored procedures.** Early database designers imagined a transaction could encompass an entire flow of user activity — booking an airline ticket end to end, committed atomically. **Unfortunately humans are very slow to make up their minds.** A transaction waiting for user input means supporting a huge number of concurrent, mostly idle transactions, which most databases cannot do efficiently — **so almost all OLTP applications keep transactions short by never waiting for a user inside one.** On the web this means **a transaction is committed within the same HTTP request; a new request starts a new transaction.**

But even with humans out of the critical path, **transactions are still executed interactively, one statement at a time**: query, read result, maybe another query, with queries and results travelling back and forth between application and database machines. **In this interactive style a lot of time is spent in network communication** — so **disallowing concurrency would give dreadful throughput**, with the database mostly waiting for the application's next query.

**For this reason, single-threaded systems don't allow interactive multi-statement transactions.** The application must either **limit itself to single-statement transactions or submit the entire transaction code to the database ahead of time, as a stored procedure.** Provided all required data is in memory, **a stored procedure executes very quickly, without waiting for network or disk I/O.**

**Sharding.** Serial execution limits throughput to one CPU core. **To scale across cores and nodes, shard your data** (supported in VoltDB). **If each transaction reads and writes only within a single shard, each shard can have its own transaction processing thread**, so you can give each CPU core its own shard and **transaction throughput scales linearly with core count.**

**But any transaction touching multiple shards must be coordinated across all of them**, with the stored procedure performed in lockstep to ensure serializability system-wide. **Cross-shard transactions are vastly slower**: **VoltDB reports about 1,000 cross-shard writes per second** — orders of magnitude below its single-shard throughput, **and it cannot be increased by adding machines.** More recent research explores making multishard transactions more scalable. **Whether transactions can be single-shard depends very much on the data**: simple key-value data often shards easily, **but data with multiple secondary indexes is likely to require a lot of cross-shard coordination.**

## Trade-offs & Pitfalls
**Stored procedures have a somewhat bad reputation**, for four reasons:
- **Vendor-specific languages** — Oracle's PL/SQL, SQL Server's T-SQL, PostgreSQL's PL/pgSQL — that **haven't kept up with general-purpose languages**, look ugly and archaic today, and **lack a library ecosystem.**
- **Code running in a database is difficult to manage**: harder to debug, more awkward to version-control and deploy, trickier to test, and difficult to integrate with metrics collection.
- **A database is often much more performance-sensitive than an application server**, since one database instance is shared by many application servers — **so a badly written stored procedure causes much more trouble than equivalent bad code in an application server.**
- **In a multitenant system allowing tenants to write stored procedures, executing untrusted code in the same process as the database kernel is a security risk.**

**Those issues can be overcome.** Modern implementations **use existing general-purpose languages instead of PL/SQL**: **VoltDB uses Java or Groovy, Datomic uses Java or Clojure, Redis uses Lua, MongoDB uses JavaScript.** They are also useful when application logic can't easily live elsewhere — **an application exposing its database through a GraphQL proxy that lacks complex validation logic can embed that logic in a stored procedure**, avoiding a separate validation service.

**VoltDB also uses stored procedures for replication**: rather than copying a transaction's writes between nodes, **it executes the same stored procedure on each replica** — which **requires stored procedures to be deterministic**, so a transaction needing the current time must obtain it through special deterministic APIs. **This is state machine replication.**

**Summary of the constraints** under which serial execution is viable:
- **Every transaction must be small and fast** — one slow transaction stalls all transaction processing.
- **The active dataset should fit in memory.** Rarely accessed data could move to disk, **but if it were needed in a single-threaded transaction the system would get very slow.**
- **Write throughput must be low enough for one CPU core**, or transactions must shard without cross-shard coordination.
- **Cross-shard transactions are possible, but their throughput is hard to scale.**

## Examples & Systems
VoltDB/H-Store, Redis, Datomic; PL/SQL, T-SQL, PL/pgSQL versus Java, Groovy, Clojure, Lua, JavaScript.

## Since the 1st Edition
Close to the 1st edition's [[Actual Serial Execution]] — the same two enabling developments, the same stored-procedure argument, the same VoltDB cross-shard throughput figure, and the same summary constraints. **Added:** the **multitenant security risk** of executing untrusted stored procedures in the database process; the **GraphQL proxy** example as a modern reason to put logic in the database; and an explicit forward link from stored-procedure determinism to the durable-execution material in Chapter 5.

## Related
- up: [[Serializability (2e)]] · chapter: [[Ch 08 - Transactions (2e)]]
- [[Keeping Everything in Memory (2e)]] — the enabling storage change
- [[Durable Execution and Workflows (2e)]] — determinism as a general problem
- [[Implementation of Replication Logs (2e)]] — state machine replication
- 1st edition: [[Actual Serial Execution]] — the same subtopic
