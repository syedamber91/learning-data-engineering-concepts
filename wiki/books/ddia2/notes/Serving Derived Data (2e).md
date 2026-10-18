---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 11
chapter_title: Batch Processing
topic: Batch Use Cases
type: subtopic
tags: [ddia2, derived-data, kafka, bulk-load, side-effects, dmz]
sources:
  - raw/ch11.md
---
# Serving Derived Data
> Do not write to your production database from inside a batch job. Push to a stream, or build the database files and bulk-load them.

## The Idea
**Batch jobs are often used to build precomputed or derived datasets** — product recommendations, user-facing reports, features for ML models — **typically served from a production database, key-value store, or search engine.** **Whatever the system, the precomputed data needs to get from the batch processor's DFS or object store back into the database serving live traffic.**

**You might be tempted to use your database's client library directly within the batch job and write to the server one record at a time. This will work, but it is a bad idea for several reasons:**
- **Making a network request for every record is orders of magnitude slower than a batch task's normal throughput.** **Even with client-side batching, performance is likely to be poor.**
- **Batch frameworks run many tasks in parallel.** **If all tasks write concurrently to the same output database at batch-processing rates, that database can easily be overwhelmed, and its query performance will suffer** — **which can in turn cause operational problems in other parts of the system.**
- **Batch jobs normally provide a clean all-or-nothing guarantee**: **if the job succeeds, the result is every task run exactly once even if some failed and retried; if the job fails, no output is produced.** **But writing to an external system produces externally visible side effects that cannot be hidden this way** — **you have to worry about results from partially completed jobs being visible to other systems, and a failed-and-restarted task may duplicate output.**

## How It Works
**A better solution is to have batch jobs push precomputed datasets to streams such as Kafka topics.** **Search engines like Elasticsearch, real-time OLAP systems like Pinot and Druid, derived datastores like Venice, and cloud warehouses like ClickHouse all have built-in ability to ingest from Kafka.** This fixes several problems:
- **Streaming systems are optimized for sequential writes**, better suited to a batch job's bulk write workload.
- **They act as a buffer between the batch job and production databases** — **downstream systems can throttle their read rate to keep serving production traffic comfortably.**
- **The output of a single batch job can be consumed by multiple downstream systems.**
- **They can serve as a security boundary**, deployed in a **demilitarized zone (DMZ) network** between the batch processing network and the production network.

**One issue streaming doesn't inherently solve is the all-or-nothing guarantee.** **On completion, batch jobs must send a notification to downstream systems that the job is done and the data can be served**, and **consumers must keep received data invisible to queries — like an uncommitted transaction under read-committed isolation — until notified.**

**Another pattern, more common when bootstrapping databases, is to build a brand-new database inside the batch job and bulk-load those files directly** from a DFS, object store, or local filesystem. **Many systems offer bulk import tools** — **TiDB's Lightning, Apache Pinot's Hadoop import jobs**, and **RocksDB's API to bulk-import SST files from batch jobs.**

## Trade-offs & Pitfalls
- **Building databases in batch and bulk-importing is very fast and makes it easier for systems to atomically switch between dataset versions.** **But it can be challenging to incrementally update datasets from jobs that build brand-new databases.**
- **It's common to take a hybrid approach when both bootstrapping and incremental loads are needed** — **Venice supports hybrid stores allowing batch row-based updates and full dataset swaps.**

## Examples & Systems
Kafka as the intermediary; Elasticsearch, Pinot, Druid, Venice, ClickHouse as ingesting systems; TiDB Lightning, Pinot Hadoop import, RocksDB SST bulk import.

## Since the 1st Edition
This is the 1st edition's [[The Output of Batch Workflows]], **renamed and rebuilt around streams.** The 1st edition made the same three arguments against writing directly to a production database, and described **building search indexes and key-value stores as batch output files then loading them** — that bulk-load pattern survives. **New:** **pushing to Kafka as the recommended primary approach**, with its four benefits including the **DMZ security boundary**; the **completion-notification requirement** for preserving all-or-nothing semantics; and the **hybrid batch-plus-incremental** pattern with Venice as the example.

## Related
- up: [[Batch Use Cases (2e)]] · chapter: [[Ch 11 - Batch Processing (2e)]]
- [[Systems of Record and Derived Data (2e)]] — the framing this depends on
- [[Transmitting Event Streams (2e)]] — the streaming systems used as the intermediary
- [[Read Committed (2e)]] — the isolation analogy for hiding incomplete output
- 1st edition: [[The Output of Batch Workflows]] — the same subtopic under its old name
