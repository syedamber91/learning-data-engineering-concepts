---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 8
chapter_title: Transactions
type: topic
tags: [ddia2, transactions, system-r, nosql, newsql]
sources:
  - raw/ch08.md
---
# What Exactly Is a Transaction?
**Almost all relational databases today, and some nonrelational ones, support transactions**, and most follow the style introduced in **1975 by IBM System R, the first SQL database**. Some implementation details have changed, but **the general idea has remained virtually the same for 50 years**: transaction support in MySQL, PostgreSQL, Oracle, and SQL Server is **uncannily similar to System R's**.

In the late 2000s nonrelational (NoSQL) databases gained popularity, aiming to improve on the relational status quo with new data models and with replication and sharding by default. **Transactions were the main casualty**: many of that generation abandoned them entirely, **or redefined the word to describe a much weaker set of guarantees than had previously been understood.**

The hype led to a popular belief that **transactions were fundamentally unscalable** and any large-scale system would have to abandon them for performance and availability. **More recently, that belief has turned out to be wrong.** So-called **NewSQL** databases — **CockroachDB, TiDB, Spanner, FoundationDB, YugabyteDB** — have shown that transactional systems can scale to large data volumes and high throughput, **combining sharding with consensus protocols to provide strong ACID guarantees at scale.**

That doesn't mean every system must be transactional either; **as with every other design choice, transactions have advantages and limitations.**

## Subtopics
- [[The Meaning of ACID (2e)]] — what the four letters actually promise, and where each is vague.
- [[Single-Object and Multi-Object Operations (2e)]] — which guarantees apply to one object versus many, and how to handle aborts.

## Key Takeaways
- **The design is 50 years old and essentially unchanged.** That stability is worth noticing: unlike storage engines or replication, transaction semantics have not been rewritten by the distributed era.
- **NoSQL didn't just weaken transactions — it redefined the word**, which is why "supports transactions" on a feature list tells you almost nothing.
- **The scalability objection has been answered.** NewSQL is the counterexample, and the mechanism is named: sharding plus consensus.
- The question the chapter sets up is not *should you use transactions* but **what exact guarantees do you get, and what do they cost** — which is why the whole chapter is organised around anomalies rather than around features.

## Since the 1st Edition
The 1st edition's Chapter 7 opened similarly, tracing transactions to System R and describing the NoSQL retreat. **The change is the verdict.** The 1st edition presented the "transactions don't scale" claim as a live debate it would examine; **the 2nd edition states flatly that the belief turned out to be wrong** and names the five NewSQL systems that disproved it, plus the mechanism (sharding + consensus). It also adds the Post Office Horizon scandal as evidence that missing ACID transactions cause real harm.

## Related
- chapter: [[Ch 08 - Transactions (2e)]]
- [[Solutions for Replication Lag (2e)]] — the same NewSQL verdict, from the replication side
- [[Humans and Reliability (2e)]] — the Horizon scandal in full
- 1st edition: [[Ch 07 - Transactions]] — the chapter opening this revises
