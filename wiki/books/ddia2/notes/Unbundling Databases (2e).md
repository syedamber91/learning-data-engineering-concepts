---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 13
chapter_title: A Philosophy of Streaming Systems
type: topic
tags: [ddia2, unbundling, unix-philosophy, relational-philosophy, information-management]
sources:
  - raw/ch13.md
---
# Unbundling Databases
**At an abstract level, databases, batch/stream processors, and operating systems all perform the same functions: they store some data, and they allow you to process and query it.** **A database stores data in records of a data model; an operating system's filesystem stores data in files — but at their core both are "information management" systems.** **Batch processors are like a distributed version of Unix.**

**There are many practical differences, of course** — **many filesystems cope poorly with a directory containing 10 million small files, whereas a database with 10 million small records is completely normal and unremarkable.** **Nevertheless the similarities and differences are worth exploring.**

**Unix and relational databases approached information management with very different philosophies.** **Unix viewed its purpose as presenting programmers with a logical but fairly low-level hardware abstraction; relational databases wanted to give application programmers a high-level abstraction hiding the complexities of on-disk data structures, concurrency, and crash recovery.** **Unix developed pipes and files that are just sequences of bytes; databases developed SQL and transactions.**

**Which is better? It depends what you want.** **Unix is "simpler" in the sense of being a fairly thin wrapper around hardware resources; relational databases are "simpler" in the sense that a short declarative query can draw on a lot of powerful infrastructure — query optimization, indexes, join methods, concurrency control, replication — without the query author needing to understand the implementation.**

**The tension has lasted for decades** — both emerged in the early 1970s — **and still isn't resolved.** **The NoSQL movement could be interpreted as wanting to apply a Unix-esque approach of low-level abstractions to distributed OLTP data storage.** **This topic attempts to reconcile the two, in the hope of combining the best of both worlds.**

## Subtopics
- [[Composing Data Storage Technologies (2e)]] — federated databases unify reads; unbundled databases unify writes.
- [[Designing Applications Around Dataflow (2e)]] — application code as a derivation function, in a spreadsheet-like model.
- [[Observing Derived State (2e)]] — the write path, the read path, and where the boundary between them sits.

## Key Takeaways
- **The unbundling metaphor is precise, not loose.** A database already contains secondary index maintenance, materialized view maintenance, replication logs, and full-text indexing — **unbundling means providing those same facilities as separate composable pieces of software.**
- **Federation and unbundling are two sides of one coin**: federation unifies *reads* across systems, unbundling unifies *writes*. **Reads are the easier problem.**
- **The goal is breadth, not depth.** Unbundling doesn't aim to beat a single database on its own workload; it aims to cover a wider range of workloads than any one product can.

## Since the 1st Edition
Essentially unchanged from the 1st edition's [[Unbundling Databases]] — the same Unix-versus-relational framing, the same three subtopics, and the same reconciliation goal. The individual subtopics have gained new systems and examples but the argument is the same.

## Related
- chapter: [[Ch 13 - A Philosophy of Streaming Systems (2e)]]
- [[Batch Processing with Unix Tools (2e)]] — the Unix philosophy in action
- [[Data Integration (2e)]] — the problem unbundling addresses
- 1st edition: [[Unbundling Databases]] — the same topic
