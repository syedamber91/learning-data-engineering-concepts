---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 12
chapter_title: Stream Processing
topic: Processing Streams
type: subtopic
tags: [ddia2, cep, stream-analytics, materialized-views, ivm, percolator]
sources:
  - raw/ch12.md
---
# Uses of Stream Processing
> Four uses, and in three of them the relationship between queries and data is inverted: the query is stored long-term and the data flows past it.

## The Idea
**Stream processing has long been used for monitoring**, where an organization wants to be alerted if certain things happen — **fraud detection systems determining whether a credit card's usage patterns have unexpectedly changed, and trading systems examining price changes and executing trades according to rules.**

## How It Works
**Complex event processing (CEP)** is **an approach developed in the 1990s for analyzing event streams, especially for applications that require searching for certain event patterns.** **Similarly to the way a regular expression lets you search for patterns of characters in a string, CEP lets you specify rules to search for patterns of events in a stream.**

**CEP systems often use a high-level declarative query language like SQL, or a GUI, to describe the patterns to detect.** **Queries are submitted to an engine that consumes the input streams and internally maintains a state machine performing the matching**; **when a match is found the engine emits a complex event with the details of the pattern detected.**

**In these systems the relationship between queries and data is reversed compared to normal databases.** **Usually a database stores data persistently and treats queries as transient**: a query comes in, the database searches for matching data, and forgets the query. **CEP engines reverse these roles: queries are stored long-term, and as each event arrives the engine checks whether it has now seen a pattern matching any standing query.** **Implementations include Esper, Apama, and TIBCO StreamBase; Flink and Spark Streaming also have SQL support for declarative queries on streams.**

**Stream analytics.** **The boundary with CEP is blurry, but as a general rule stream analytics is less focused on detecting specific event sequences and more oriented toward aggregations and statistical metrics over large volumes of events** — **measuring the rate of a type of event, calculating a rolling average, or comparing current statistics to previous intervals** to detect trends or alert on metrics unusually high or low compared to the same time last week.

**Such statistics are usually computed over fixed time intervals** — the average queries per second over the last five minutes and their 99th percentile response time. **Averaging over a few minutes smooths out irrelevant second-to-second fluctuations while still giving a timely picture.** **The interval over which you aggregate is a window.**

**Stream analytics sometimes uses probabilistic algorithms**: **Bloom filters for set membership, HyperLogLog for cardinality estimation, and various percentile estimation algorithms.** **These produce approximate results but require significantly less memory than exact algorithms.** **This sometimes leads people to believe stream processing systems are always lossy and inexact — that is wrong. There is nothing inherently approximate about stream processing; using probabilistic algorithms is merely an optimization.**

**Frameworks designed with analytics in mind include Apache Storm, Spark Streaming, Flink, Samza, Apache Beam, and Kafka Streams; hosted services include Google Cloud Dataflow and Azure Stream Analytics.**

**Maintaining materialized views.** **A stream of database changes can keep derived systems — caches, search indexes, warehouses — up to date with a source database.** **These are examples of maintaining materialized views: deriving an alternative view onto a dataset so you can query it efficiently, and updating it whenever the underlying data changes.** **In event sourcing, application state maintained by applying a log of events is also a kind of materialized view.**

**Unlike stream analytics, considering only events within a time window is usually not sufficient** — **building the view potentially requires all events over an arbitrary period, apart from obsolete events discarded by log compaction. In effect you need a window stretching all the way back to the beginning of time.** **In principle any stream processor could do this, although maintaining events forever runs counter to the assumptions of analytics-oriented frameworks that operate on limited windows.** **Kafka Streams and Confluent's ksqlDB support this usage, building on Kafka's log compaction.**

**Search on streams.** **Besides CEP's multi-event patterns, there is sometimes a need to search for individual events by complex criteria such as full-text queries.** **Media monitoring services subscribe to feeds of news articles and broadcasts and search for mentions of companies, products, or topics of interest** — **formulating a search query in advance, then continually matching the stream against it.** **Similar features exist on websites — real estate site users asking to be notified when a matching property appears.** **Elasticsearch's percolator feature is one option.**

**Conventional search engines index documents then run queries over the index. Searching a stream turns this on its head: queries are stored, and documents are evaluated against them, as in CEP.** **In the simplest case you test every document against every query, which can be slow with many queries — to optimize, you can index the queries as well as the documents and narrow the set that may match.**

## Trade-offs & Pitfalls
> **Incremental view maintenance (IVM).** **Databases might seem well suited for materialized view maintenance — they keep full copies of datasets, and many support materialized views.** **Unfortunately, databases often refresh view tables using periodic batch jobs or on-demand requests such as PostgreSQL's `REFRESH MATERIALIZED VIEW`, not on every update to source data.** **Two significant drawbacks make this inappropriate for stream processing:** **poor efficiency** — **all data is reprocessed every time the view is updated, though most of it likely remains unchanged** — and **data freshness** — **changes aren't reflected until the query is run again at its next scheduled update.**
>
> **It is possible to write triggers that update views efficiently when the data is easily partitioned and the computation is naturally incremental** — a view of total sales revenue per day can update just the appropriate day's row on each sale. **Bespoke solutions work in a few cases, but many SQL queries can't be easily or efficiently converted to incremental computation.**
>
> **IVM is a more general solution: techniques that convert queries written in SQL or other languages into operators capable of incremental computation.** **Rather than processing entire datasets, IVM algorithms recompute and update only data that has changed**, making view computation far more efficient, **which means updates can run much more frequently, dramatically increasing data freshness.**
>
> **Materialize, RisingWave, ClickHouse, and Feldera all use IVM techniques to provide efficient incremental materialized views.** **They ingest streams of events to expose materialized views in real time: recent events are buffered in memory and periodically used to update on-disk views, and reads combine the recent events and the materialized data into a single real-time view.** **Since reads are often SQL and views are often stored in OLAP-style formats, these systems also support large-scale warehouse-style queries.**

**Event-driven architectures and RPC.** **Message-passing systems are an alternative to RPC, used for example in the actor model** — **but we normally don't think of them as stream processors, for three reasons:** **actor frameworks are primarily a mechanism for managing concurrency and distributed execution of communicating modules, whereas stream processing is primarily a data management technique**; **communication between actors is often ephemeral and one-to-one, whereas event logs are durable and multi-subscriber**; and **actors can communicate in arbitrary ways including cyclic request/response, but stream processors are usually acyclic pipelines where every stream is the output of one job derived from well-defined inputs.**

**There is some crossover, though.** **Apache Storm has distributed RPC, allowing user queries to be farmed out to nodes that also process event streams, interleaved with events from the input streams and aggregated back to the user.** **It is also possible to process streams using actor frameworks — but many don't guarantee message delivery on crashes, so the processing is not fault-tolerant unless you implement additional retry logic.**

## Examples & Systems
Esper, Apama, TIBCO StreamBase (CEP); Storm, Spark Streaming, Flink, Samza, Beam, Kafka Streams, Cloud Dataflow, Azure Stream Analytics (analytics); Kafka Streams and ksqlDB (materialized views); Elasticsearch percolator (stream search); Materialize, RisingWave, ClickHouse, Feldera (IVM).

## Since the 1st Edition
The 1st edition's [[Uses of Stream Processing]] covered CEP, stream analytics, materialized views, search on streams, and message passing/RPC — the same five. **The major addition is the incremental view maintenance box**, naming **Materialize, RisingWave, ClickHouse, and Feldera** and explaining precisely why a database's `REFRESH MATERIALIZED VIEW` is not a substitute. That whole category of system emerged after 2017.

## Related
- up: [[Processing Streams (2e)]] · chapter: [[Ch 12 - Stream Processing (2e)]]
- [[Materialized Views and Data Cubes (2e)]] — the batch-side view maintenance
- [[Reasoning About Time (2e)]] — what a window actually means
- [[Full-Text Search (2e)]] — the conventional index-then-query direction
- 1st edition: [[Uses of Stream Processing]] — the same subtopic
