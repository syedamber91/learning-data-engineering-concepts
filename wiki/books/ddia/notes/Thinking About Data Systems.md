---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 1
chapter_title: Reliable, Scalable, and Maintainable Applications
type: topic
tags: [ddia, data-systems, composite-systems, nonfunctional-requirements]
sources:
  - raw/ch01.md
---
# Thinking About Data Systems
> Databases, caches, queues, and search indexes are best understood as one family — "data systems" — because modern applications compose them into a single, application-defined whole.

## The Idea
Most applications today are constrained by data — its volume, its complexity, and how fast it changes — rather than by raw CPU. Engineers rarely build storage engines from scratch; instead they assemble standard building blocks: databases for durable storage, caches to avoid repeating expensive work, search indexes for keyword lookup, stream processors for asynchronous messaging, and batch processors for periodic bulk computation. The interesting question is which of these tools fits a given job, and how to combine them when no single tool suffices.

Treating these categories as one umbrella — *data systems* — is justified for two reasons. First, the traditional boundaries have blurred: Redis is a datastore that also behaves like a message queue, while [[Apache Kafka]] is a queue that offers database-grade durability. Second, demanding applications routinely stitch several specialized tools together with application code, so the "database" the outside world sees is really a composite.

## How It Works
A typical composite pairs a primary database with, say, a Memcached-style cache and a full-text search server such as Elasticsearch or Solr. Application code carries the burden of keeping the cache and index consistent with the source of truth (a problem developed much further in [[Keeping Systems in Sync]]). The composite hides its internals behind an API, and at that point the developer has effectively designed a new special-purpose data system — one that may promise guarantees like correct cache invalidation on writes. You become a data system designer, whether you intended to or not.

Design then raises hard questions: how to keep data correct when components fail internally, how to keep performance steady while parts of the system are degraded, how to grow with load, and what a clean API looks like. Context matters too — team experience, legacy constraints, delivery deadlines, risk tolerance, and regulation all shape the answer.

## The Three Concerns
The book distills the concerns that matter in most systems to three:
- **[[Reliability]]** — keep working *correctly* even when hardware, software, or humans go wrong.
- **[[Scalability]]** — have sensible strategies for growth in data, traffic, or complexity.
- **[[Maintainability]]** — let many people, over years, work on the system productively.

These words are used loosely in industry; the rest of the chapter pins down what each actually means so they can be engineered deliberately rather than invoked as slogans.

## Related
- chapter: [[Ch 01 - Reliable, Scalable, and Maintainable Applications]]
- [[Reliability]] — first of the three core concerns
- [[Scalability]] — coping with growth in load
- [[Maintainability]] — long-term human cost of a system
- [[Keeping Systems in Sync]] — the cache/index consistency problem in depth
- [[Apache Kafka]] — example of blurred tool categories
