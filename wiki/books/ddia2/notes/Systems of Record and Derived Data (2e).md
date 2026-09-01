---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 1
chapter_title: Trade-Offs in Data Systems Architecture
topic: Operational Versus Analytical Systems
type: subtopic
tags: [ddia2, system-of-record, derived-data, source-of-truth]
sources:
  - raw/ch01.md
---
# Systems of Record and Derived Data
> Which data is authoritative, and which data could you throw away and rebuild? Answering that for every store in your architecture is the cheapest clarity you can buy.

## The Idea
A **system of record** — also called a **source of truth** — holds the authoritative or canonical version of data. New data is written here first, and each fact is represented exactly once, typically in normalised form. If another system disagrees with it, the system of record is by definition correct. **Derived data** is the result of taking data from another system and transforming or processing it; if you lose it, you can re-create it from the source. The classic case is a cache: serve from it when present, fall back to the database when not. Denormalised values, indexes, materialized views, transformed representations, and models trained on a dataset all belong to this category.

## How It Works
- Derived data is technically **redundant** — it duplicates information that already exists — but it is usually what makes read queries fast, and you can derive several datasets from one source to view the same data several ways.
- Analytical systems are almost always derived data systems, since they consume data created elsewhere. Operational services usually mix the two: the primary databases data is first written to are systems of record, while the indexes and caches that accelerate reads — especially queries the system of record cannot answer efficiently — are derived.
- **The distinction is not a property of the tool.** Most databases, storage engines, and query languages are neither inherently a system of record nor inherently derived. A database is just a tool; which role it plays depends on how you use it in your application.

## Trade-offs & Pitfalls
- Once data in one system is derived from another, you need a process to update the derivative when the source changes — and this is where many designs quietly fail. Many databases are built on the assumption that your application will only ever use that one database, and offer little help integrating multiple systems to propagate such updates.
- The payoff for being explicit is architectural, not performance-related: being clear about which data is derived from which brings clarity to an otherwise confusing system. The failure mode is a graph of stores where nobody can say which one to believe.

## Examples & Systems
Caches, secondary indexes, materialized views, denormalised columns, and trained ML models as derived data; the primary application database as the usual system of record.

## Since the 1st Edition
The 1st edition introduced this framing very late — in Chapter 12's discussion of [[Derived Data]] and data integration — where it read as a synthesis of the whole book. The 2nd edition moves it into the opening chapter as basic vocabulary, which changes its function: it is now a lens you carry through every subsequent chapter rather than a conclusion you arrive at.

## Related
- up: [[Operational Versus Analytical Systems (2e)]] · chapter: [[Ch 01 - Trade-Offs in Data Systems Architecture (2e)]]
- [[Data Integration (2e)]] — the full treatment of keeping derived systems in sync
- [[Keeping Systems in Sync (2e)]] — dual writes and their failure modes
- [[Serving Derived Data (2e)]] — batch jobs whose whole output is derived data
- 1st edition: [[Derived Data]] — the same idea in its original, much later home
