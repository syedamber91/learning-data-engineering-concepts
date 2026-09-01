---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 13
chapter_title: A Philosophy of Streaming Systems
topic: Data Integration
type: subtopic
tags: [ddia2, reprocessing, lambda-architecture, kappa-architecture, schema-migration]
sources:
  - raw/ch13.md
---
# Batch and Stream Processing
> Stream processing keeps derived views fresh; batch processing lets you rebuild them in a completely different shape. You need both, and the reason is application evolution.

## The Idea
**The goal of data integration is to make sure data ends up in the right form in all the right places** — **consuming inputs, transforming, joining, filtering, aggregating, training models, evaluating, and writing to the appropriate outputs.** **Batch and stream processors are the tools.** **Their outputs are derived datasets: search indexes, materialized views, recommendations, aggregate metrics.**

**They have a lot of principles in common. The main fundamental difference is that stream processors operate on unbounded datasets, whereas batch inputs are of known, finite size.**

## How It Works
**Maintaining derived state.** **Batch processing has a quite strong functional flavor**, even when not written in a functional language: **it encourages deterministic, pure functions whose output depends only on the input and that have no side effects other than the explicit outputs, treating inputs as immutable and outputs as append-only.** **Stream processing is similar but extends operators to allow managed, fault-tolerant state.**

**The principle of deterministic functions with well-defined inputs and outputs is not only good for fault tolerance but also simplifies reasoning about the dataflows in an organization.** **Whether the derived data is a search index, a statistical model, or a cache, it helps to think in terms of pipelines that derive one thing from another, pushing state changes through functional application code and applying the effects to derived systems.**

**In principle derived systems could be maintained synchronously**, just as a relational database updates secondary indexes within the same transaction. **However, asynchrony is what makes event-log-based systems robust: it allows a fault in one part of the system to be contained locally, whereas distributed transactions abort if any participant fails, so they tend to amplify failures by spreading them.** **Secondary indexes often cross shard boundaries — a sharded system must either send writes to multiple shards or reads to all shards — and such cross-shard communication is also most reliable and scalable if the index is maintained asynchronously.**

**Reprocessing data for application evolution.** **Stream processing reflects input changes in derived views with low delay; batch processing lets large amounts of accumulated historical data be reprocessed to derive new views onto an existing dataset.**

**Reprocessing provides a good mechanism for maintaining a system and evolving it to support new features and changed requirements.** **Without it, schema evolution is limited to simple changes like adding a new optional field or a new record type. With it, you can restructure a dataset into a completely different model.**

> **Schema migrations on railways.** **In the early days of railway building in 19th-century England there were various competing standards for the gauge — the distance between the rails.** **Trains built for one gauge couldn't run on tracks of another, restricting interconnections.** **After a single standard was decided in 1846, other tracks had to be converted — but how, without shutting the line for months or years?** **The solution: first convert to dual gauge or mixed gauge by adding a third rail.** **This can be done gradually, and once done, trains of both gauges run on the line using two of the three rails.** **Eventually, once all trains use the standard gauge, the nonstandard rail is removed.** **"Reprocessing" the existing tracks this way, allowing old and new versions to exist side by side, makes it possible to change the gauge gradually over years.** **Nevertheless the undertaking is expensive, which is why nonstandard gauges still exist — the BART system in the San Francisco Bay Area uses a different gauge from the majority of the US.**

**Derived views allow gradual evolution.** **To restructure a dataset you don't need a sudden switch: maintain the old and new schemas side by side as two independently derived views onto the same underlying data, shift a small number of users to the new view to test performance and find bugs while most continue on the old, gradually increase the proportion, and eventually drop the old view.**

**The beauty of gradual migration is that every stage is easily reversible if something goes wrong — you always have a working system to go back to.** **Reducing the risk of irreversible damage allows you to be more confident about going ahead and thus to move faster.**

## Trade-offs & Pitfalls
**Unifying batch and stream processing.** **An early proposal was the lambda architecture, which had a number of problems and has fallen out of use.** **More recent systems allow batch computations (reprocessing historical data) and stream computations (processing events as they arrive) in the same system — sometimes known as the kappa architecture.**

**Unifying them requires three features:**
- **The ability to replay historical events through the same processing engine that handles recent events.** **Log-based brokers can replay messages, and some stream processors can read input from a distributed filesystem or object storage.**
- **Exactly-once semantics for stream processors** — **ensuring the output is the same as if no faults had occurred**, which as with batch requires discarding partial outputs of failed tasks.
- **Tools for windowing by event time, not processing time**, since **processing time is meaningless when reprocessing historical events.** **Apache Beam provides an API for expressing such computations, runnable on Flink or Google Cloud Dataflow.**

## Examples & Systems
The 19th-century railway gauge conversion as the migration analogy; lambda and kappa architectures; Apache Beam over Flink or Cloud Dataflow.

## Since the 1st Edition
The 1st edition's [[Batch and Stream Processing]] covered the same material including the railway gauge box and the three unification requirements. **The change is the verdict on lambda architecture**: the 1st edition presented it as a proposal with known problems and described the emerging unified approach; **the 2nd states plainly that it "has fallen out of use"** and names **the kappa architecture** as what replaced it.

## Related
- up: [[Data Integration (2e)]] · chapter: [[Ch 13 - A Philosophy of Streaming Systems (2e)]]
- [[Batch Processing Models (2e)]] and [[Processing Streams (2e)]] — the two families
- [[Reasoning About Time (2e)]] — why event-time windowing is required
- [[Evolvability - Making Change Easy (2e)]] — the irreversibility argument
- 1st edition: [[Batch and Stream Processing]] — the same subtopic
