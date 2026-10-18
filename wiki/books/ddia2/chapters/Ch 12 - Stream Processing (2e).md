---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 12
chapter_title: Stream Processing
type: chapter-moc
tags: [ddia2, stream-processing, kafka, cdc, event-time, exactly-once, moc]
sources:
  - raw/ch12.md
---
# Ch 12 – Stream Processing
Chapter 11 assumed **the input is bounded — of a known and finite size — so the batch process knows when it has finished reading.** **The sort central to MapReduce must read its entire input before producing output, because the very last record could be the one with the lowest key.**

**In reality, a lot of data is unbounded because it arrives gradually over time.** **Users produced data yesterday and today and will produce more tomorrow; unless you go out of business, this never ends, so the dataset is never "complete" in any meaningful way.** **So batch processors must artificially divide the data into chunks of fixed duration** — a day's worth at the end of every day, an hour's at the end of every hour.

**The problem with daily batch processes is that changes in the input are reflected in the output a day later, which is too slow for many impatient users.** **To reduce the delay, run more frequently — a second's worth at the end of every second — or continuously, abandoning fixed time slices entirely and processing every event as it happens. That is the idea behind stream processing.**

**A stream refers to data that is incrementally made available over time.** The concept appears **in Unix stdin and stdout, in programming languages as lazy lists, in filesystem APIs, in TCP connections, and in audio and video delivered over the internet.**

## Map
- [[Transmitting Event Streams (2e)]] — events, producers, consumers, topics
  - [[Messaging Systems (2e)]] — the two defining questions, direct messaging, brokers, acknowledgments, dead letter queues
  - [[Log-Based Message Brokers (2e)]] — the durable hybrid: offsets, shards, retention, tiered storage
- [[Databases and Streams (2e)]] — every write to a database is an event
  - [[Keeping Systems in Sync (2e)]] — why dual writes are broken
  - [[Change Data Capture (2e)]] — making one database the leader and the rest followers
  - [[State, Streams, and Immutability (2e)]] — state as the integral of an event stream
- [[Processing Streams (2e)]] — what to do once you have the stream
  - [[Uses of Stream Processing (2e)]] — CEP, stream analytics, materialized views, stream search
  - [[Reasoning About Time (2e)]] — event time versus processing time, stragglers, window types
  - [[Stream Joins (2e)]] — stream–stream, stream–table, table–table, and time dependence
  - [[Fault Tolerance (Stream Processing) (2e)]] — microbatching, checkpointing, atomic commit, idempotence

## Chapter Summary
**In some ways stream processing is very much like batch processing, but done continuously on unbounded streams rather than a fixed-size input.** **From this perspective, message brokers and event logs serve as the streaming equivalent of a filesystem.**

**Two types of message broker.** The **AMQP/JMS style** assigns individual messages to consumers, who acknowledge them individually; **messages are deleted after acknowledgment.** **Appropriate as an asynchronous form of RPC** — a task queue where exact order doesn't matter and you never need to reread old messages. The **log-based** style **assigns all messages in a shard to the same consumer node and always delivers in the same order**; **parallelism comes from sharding, consumers track progress by checkpointing offsets, and the broker retains messages on disk so you can jump back and reread.** **The log-based approach resembles database replication logs, log-structured storage engines, and consensus, and is especially appropriate for systems that consume input streams and generate derived state or derived output streams.**

**Streams come from user activity events, sensors, and data feeds — and it is also useful to think of writes to a database as a stream.** **The changelog can be captured implicitly through CDC or explicitly through event sourcing, and log compaction allows the stream to retain a full copy of the database contents.** **Representing databases as streams opens powerful opportunities for integration**: keep search indexes, caches, and analytical systems continually up to date by consuming the change log, **and build fresh views onto existing data by consuming from the beginning.**

**Three purposes of stream processing:** searching for event patterns (**complex event processing**), computing windowed aggregations (**stream analytics**), and keeping derived data systems up to date (**materialized views**). **Reasoning about time is difficult** — the distinction between processing time and event timestamps, and stragglers arriving after you thought a window was complete. **Three types of join:** **stream–stream** (both inputs are activity events, matched within a time window), **stream–table** (one input is activity events, the other a database changelog keeping a local copy current, enriching each event), and **table–table** (both inputs are changelogs; every change on one side joins with the latest state of the other, producing a stream of changes to the materialized view).

**Fault tolerance needs finer-grained recovery than batch.** **You can't simply discard all output from a long-running process producing output continuously**, so recovery is based on **microbatching, checkpointing, transactions, or idempotent writes.**

## Since the 1st Edition
This is the 1st edition's Chapter 11, with a stable spine — the same three topics, the same message-broker comparison, the same CDC and event-sourcing material, the same event-time/processing-time discussion with the **Star Wars release-order analogy**, the same four window types, the same three join types, and the same fault-tolerance techniques.

**Genuinely new:** **dead letter queues**, with the poison-message loop that motivates them; **tiered storage for log brokers** — Kafka and Redpanda serving old messages from object storage, and **WarpStream, Confluent Freight, and Bufstream storing everything there, as Iceberg tables that batch and warehouse jobs can read directly**; **the outbox pattern and the CDC-turns-your-schema-into-a-public-API warning**, with data contracts; **Debezium's DBLog watermarking** for incremental snapshots; **CDC for quorum databases** like Cassandra; the **incremental view maintenance (IVM)** box naming Materialize, RisingWave, ClickHouse, and Feldera; and **crypto-shredding and puncturable encryption** in the limitations-of-immutability discussion.

**Compressed:** the 1st edition's separate topics on "Databases and Streams" subsections are consolidated, and its long treatment of "Processing Streams" use cases is tightened.

## Related
- home: [[Home (2e)]] · previous: [[Ch 11 - Batch Processing (2e)]] · next: [[Ch 13 - A Philosophy of Streaming Systems (2e)]]
- [[Event-Driven Architectures (2e)]] — message brokers from the encoding chapter
- [[Event Sourcing and CQRS (2e)]] — the data-model view of the same idea
- 1st edition: [[Ch 11 - Stream Processing]] — the chapter this one revises

## In the vutr data-engineering wiki
- [[kafka]] — vutr's Kafka topic is the single best companion to this chapter — where the book keeps the broker abstract, vutr traces one implementation's whole arc from LinkedIn's design bet to its cross-AZ cost problem.
