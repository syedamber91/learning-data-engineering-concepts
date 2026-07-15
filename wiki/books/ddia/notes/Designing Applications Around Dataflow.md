---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 12
chapter_title: The Future of Data Systems
topic: Unbundling Databases
type: subtopic
tags: [ddia, dataflow, database-inside-out, stream-operators]
sources:
  - raw/ch12.md
---
# Designing Applications Around Dataflow

> Treat application code as derivation functions wired between streams of state changes — the "database inside-out" pattern — instead of code polling a passive mutable store.

## The Idea
Kleppmann frames unbundling-plus-application-code as the *database inside-out* design pattern (his 2014 talk; "unbundling" is Jay Kreps's term), an amalgam of dataflow languages (Oz, Juttle), functional reactive programming (Elm), and logic programming (Bloom). The touchstone is the spreadsheet: VisiCalc in 1979 already recomputed any formula whose inputs changed. Data systems should offer the same reactivity — change a record and every index, cache, and aggregation depending on it updates itself — but with durability, fault tolerance, scale, and integration across heterogeneous tools that spreadsheets never needed.

## How It Works
- **Application code as a derivation function.** Some derivations are cookie-cutter (a [[Secondary Indexes]] entry is just extracted, sorted field values); others need custom logic — full-text pipelines (stemming, synonyms, inverted indexes), ML models derived from training data, UI-shaped caches. Databases technically host custom code via triggers and stored procedures, but as an afterthought.
- **Separate code from state.** Databases are poor application-deployment environments (no good story for dependency management, versioning, rolling upgrades, monitoring), while tools like Mesos, YARN, Docker, and Kubernetes specialize in exactly that. Keep stateless services for logic, databases for durable state — "separation of Church and state."
- **Subscribe, don't poll.** The typical web architecture treats the database as a mutable shared variable read synchronously over the network; almost no language lets you *subscribe* to a variable, and databases inherited that passivity (the observer pattern bolted on, change-stream APIs only just emerging). Dataflow thinking makes code respond to state changes by producing further state changes — echoing tuple spaces from the 1980s and actor-style [[Message-Passing Dataflow]].
- **Stricter than messaging.** Maintaining [[Derived Data]] demands stable event ordering (all views must apply the same order or they diverge — ruling out dual writes and brokers that reorder on redelivery) and no message loss (one dropped event desynchronizes a view permanently; in-memory actor state fails this). Modern stream processors deliver both, far cheaper than distributed transactions, and let arbitrary application code run as composable operators, Unix-pipe style.

## Trade-offs & Pitfalls
Compared to microservices' synchronous REST calls, dataflow replaces request/response with one-directional asynchronous streams. The currency-exchange example: a purchase service can query a rate service per purchase (network dependency, latency, failure coupling), or subscribe to a rate stream and keep a local copy — turning an RPC into a local lookup via a stream–table join. Faster and more fault-tolerant, but the join becomes time-dependent: reprocessing later sees different rates, so historical joins need the rate *as of* purchase time, an open problem either way.

## Examples & Systems
Oz, Juttle, Elm, Bloom, VisiCalc; Mesos/YARN/Docker/Kubernetes; tuple spaces; Kafka-style processors running operator code; the currency-conversion stream join.

## Related
- up: [[Unbundling Databases]] · chapter: [[Ch 12 - The Future of Data Systems]]
- [[Databases and Streams]] — Ch 11 origin of subscribing to change logs
- [[Stream Joins]] — mechanics and time-dependence of the enrichment join
- [[Dataflow Through Services - REST and RPC]] — the synchronous style being replaced
- [[Event Sourcing]] — the log-of-events substrate this pattern assumes
