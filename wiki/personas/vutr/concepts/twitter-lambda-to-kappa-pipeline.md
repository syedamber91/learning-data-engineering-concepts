---
persona: vutr
kind: concept
sources:
- raw/big-tech-case-studies-batch-1-spotify-twitter-facebook-discord-notion/how-twitter-processes-4-billion-events.md
last_updated: '2026-07-15'
qc: passed
slug: twitter-lambda-to-kappa-pipeline
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Twitter's interaction and engagement pipeline — the source of truth for ads revenue and other data products — is the concrete case the notes use to show what actually breaks in a Lambda architecture at scale, and what changes when you cut over to Kappa.

The old Lambda design ran two separate pipelines that converged at the end of the day. Batch pulled from logs, client events, or tweet events sitting in HDFS, ran through many Scalding pipelines for preprocessing, fed into the Summingbird Platform (a layer that lets users define MapReduce-style logic once and execute it across engines like Scalding and Heron), and landed in the Manhattan distributed storage system — deployed in one data center and replicated to two others to save cost. Real-time ran the same Summingbird logic through Heron instead, sourced from Kafka topics, and stored results in the Nighthawk distributed cache — deployed across three data centers rather than one, since real-time had no batch fallback to lean on. A query service sat on top of both stores. The failure mode the notes call out is specific: when the event rate outran processing speed, backpressure built up inside the Heron topology (a DAG of bolts, which the notes liken to "workers"), and under sustained backpressure the Heron Stream Managers — the components that manage routing between topology stages — could fail outright. Twitter's fix was to restart the Heron containers to bring the Stream Managers back, but a restart itself causes event loss, directly hurting the accuracy the pipeline exists to guarantee.

The new architecture replaces both pipelines with a single Kappa-style stream, and the notes lay out its five steps precisely: (1) an on-prem stage consumes the source Kafka topics, does transformation and field re-mapping, and writes to intermediate Kafka topics; (2) Event Processors read those intermediate topics, convert events to Google Pub/Sub representation, and decorate each event with a UUID (used later for deduplication) plus processing-context metadata; (3) Event Processors publish to Pub/Sub with near-infinite retries, so delivery from the data centers to Google Cloud is at-least-once; (4) Google Dataflow jobs consume from Pub/Sub and perform deduplication and real-time aggregation, using the UUID from step 2; (5) Dataflow writes the aggregated result to BigTable. The combination of at-least-once publishing plus Dataflow-side deduplication is what the notes credit for "nearly exactly once" processing — Twitter engineered around exactly-once semantics without needing a transactional broker to provide them natively.

The evaluation numbers are concrete: latency stabilized at roughly 10 seconds, versus 10 seconds to 10 minutes under the old Lambda design, and throughput reached about 1 GB/s versus a ceiling of roughly 100 MB/s on the old pipeline — alongside eliminating event loss on restart and gaining the ability to handle late-arriving events. To validate correctness, Twitter ran two parallel Dataflow pipelines — one routing raw Pub/Sub data straight to BigQuery, another exporting the deduplicated, aggregated counts — so it could monitor the duplicate percentage directly, and it also loaded the old batch pipeline's results into BigQuery to run scheduled comparison queries against the new pipeline. The result: more than 95% of the new pipeline's output exactly matched the old batch pipeline, with the notes attributing the remaining discrepancy mainly to the old batch pipeline discarding late events that the new streaming pipeline captures.

*See also: [[persistent-message-bus-data-transfer]] · [[state-and-output-processing-semantics]] · [[twitter-kappa-migration]]*

## Related in the other wiki
- [[Exactly-Once Semantics]] — DDIA's concept of exactly-once delivery frames what Twitter's UUID-plus-Dataflow-deduplication trick is actually approximating without a transactional broker.
