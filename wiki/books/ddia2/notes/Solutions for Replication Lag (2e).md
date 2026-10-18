---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 6
chapter_title: Replication
topic: Single-Leader Replication
type: subtopic
tags: [ddia2, newsql, strong-consistency, linearizability, transactions]
sources:
  - raw/ch06.md
---
# Solutions for Replication Lag
> The honest answer changed since 2017: for most applications, the best solution to replication lag is to pick a database that doesn't have it.

## The Idea
When working with an eventually consistent system, **think about how the application behaves if replication lag increases to several minutes or even hours**. If the answer is "no problem," great. If the result is a bad experience for users, **design the system to provide a stronger guarantee, such as read-after-write**. The book's warning: **pretending that replication is synchronous when in fact it is asynchronous is a recipe for problems down the line.**

## How It Works
An application *can* provide a stronger guarantee than the underlying database — by performing certain reads on the leader or a synchronously updated follower, as the previous subtopic described. **However, dealing with these issues in application code is complex and easy to get wrong.**

**The simplest programming model for application developers is to choose a database that provides a strong consistency guarantee for replicas, such as linearizability, and supports ACID transactions.** That lets you mostly ignore the challenges arising from replication and **treat the database as if it had just a single node**.

## Trade-offs & Pitfalls
- **The historical argument has been settled by events.** In the early 2010s the NoSQL movement promoted the view that strong consistency and transactions **limited scalability**, and that large-scale systems would have to embrace eventual consistency. **Since then, a number of databases have started providing strong consistency and transaction support while also offering the fault tolerance, high availability, and scalability advantages of a distributed database** — the trend called **NewSQL**, which is "less about SQL specifically and more about new approaches to scalable transaction management."
- **But weaker consistency still has legitimate uses.** Even with scalable, strongly consistent distributed databases available, some applications choose other forms of replication because they **offer stronger resilience in the face of network interruptions and have lower overheads compared to transactional systems** — which is exactly what the rest of the chapter explores.

## Examples & Systems
NewSQL-style distributed databases combining transactions with horizontal scalability.

## Since the 1st Edition
The 1st edition's [[Solutions for Replication Lag]] made the "handling this in application code is complex" point and gestured at transactions as the answer, but framed it as an open question — its closing line invited the reader toward Chapters 7 and 9 without asserting that scalable strongly consistent databases existed. **The 2nd edition takes a position**: NewSQL delivered, the NoSQL-era trade-off is no longer forced, and the default recommendation is to buy strong consistency rather than build it in application code — while still crediting weaker models for resilience and lower overhead.

## Related
- up: [[Single-Leader Replication (2e)]] · chapter: [[Ch 06 - Replication (2e)]]
- [[Problems with Replication Lag (2e)]] — the problems being solved
- [[Linearizability (2e)]] — the guarantee being recommended
- [[Relational Versus Document Models (2e)]] — where NoSQL and NewSQL are introduced
- 1st edition: [[Solutions for Replication Lag]] — the same subtopic, more tentative
