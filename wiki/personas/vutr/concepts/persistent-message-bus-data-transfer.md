---
persona: vutr
kind: concept
sources:
- raw/big-tech-case-studies-batch-1-spotify-twitter-facebook-discord-notion/how-did-facebook-design-their-real.md
last_updated: '2026-07-15'
qc: passed
slug: persistent-message-bus-data-transfer
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Facebook's 2018 real-time processing paper (as summarized in the notes) treats "how do processing nodes hand data to each other" as one of five foundational design decisions for a real-time system, alongside language paradigm, processing semantics, state-saving, and backfill — and it lays out three mechanisms with genuinely different trade-offs rather than treating this as a solved problem.

Direct message transfer uses RPC or in-memory queues to pass data straight between nodes, buying end-to-end latency in the tens of milliseconds. Broker-based message transfer puts a broker between nodes to forward messages; it adds overhead but improves scalability by letting one broker multiplex several input streams to multiple output processors and apply backpressure when needed. Persistent storage-based transfer is the most reliable of the three: one processor writes its output to a persistent store and the next reads from it, which lets the two sides operate at different speeds and lets any reader replay the same data multiple times — the property that makes recovery straightforward. Layered on top of this choice is a second axis borrowed from the same vocabulary Spark uses for RDD dependencies: narrow dependencies connect a fixed number of sender partitions to receiver partitions one-to-one, while wide dependencies connect every sender partition to every receiver partition.

Facebook's actual choice is persistent storage, implemented as Scribe (see [[scribe]]) — a persistent message bus playing the same connective role Kafka plays in Twitter's and Spotify's architectures. The notes are explicit that this was a latency trade Facebook was willing to make deliberately: since the target was second-level latency rather than millisecond latency, the minor cost of writing to and reading from Scribe was acceptable, and a persistent store's extra hardware and bandwidth cost bought four concrete advantages. Fault tolerance: a stream node can fail and be replaced without affecting the rest of the system, because the data persists on Scribe regardless — and the bus supports running duplicate downstream nodes for redundant output. Performance isolation: a slow node doesn't back up into the node before it, and if a machine is overloaded, its jobs can move to a new machine that resumes from where the input stream left off. Ease of use: because any point in the DAG can be replayed from Scribe, debugging is a matter of reprocessing the same input from a new node, and applications can be composed flexibly — Puma's output can feed Stylus, and Stylus's output can feed Scuba or Hive. Scalability: partition count is just the bucket count per Scribe category, adjustable up or down.

The persistent-bus choice is also what makes Facebook's whole system decoupled by design: transport (Scribe) and processing (Puma, Stylus, Swift — see [[facebook-stream-processors-puma-swift-stylus]]) are separate concerns connected only by the bus, which is precisely the shape LinkedIn's Kafka and Spotify's Pub/Sub/Kafka lineage also converged on independently.

*See also: [[facebook-stream-processors-puma-swift-stylus]] · [[state-and-output-processing-semantics]] · [[stream-state-saving-mechanisms]]*

## Related in the other wiki
- [[Messaging Systems]] — DDIA's chapter on message brokers is the general vocabulary (direct/broker/log-based transfer) that this note's three-way Facebook-specific split instantiates.
