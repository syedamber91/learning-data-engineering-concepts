---
persona: vutr
kind: concept
sources:
- raw/big-tech-case-studies-batch-1-spotify-twitter-facebook-discord-notion/lets-build-a-data-platform-like-spotify.md
last_updated: '2026-07-15'
qc: passed
slug: spotify-event-delivery-architecture-evolution
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Spotify's notes treat "event delivery" — getting an event from a client on someone's phone into the central system — as the single most foundational piece of its data infrastructure, and the architecture went through two very different eras to keep that promise as volume grew from nothing to over a trillion events a day.

The on-prem era ran on Kafka 0.7, and the notes are specific about why that version shaped everything downstream: Kafka Broker in 0.7 lacked the ability to act as reliable persistent storage. Because the broker itself couldn't be trusted to hold data durably, Spotify refused to consider an event "persisted" until it landed in HDFS — making Hadoop the single point of failure for the whole pipeline. Kafka Producers ran on every host that needed to send events, and a layer of Kafka Groupers sat between producers and consumers: each Grouper consumed all events from one local data center and republished them as compressed, batched messages to a single topic for the consumers to pull. Consumers wrote to HDFS and only sent an ACK back to the producer via a dedicated broker once the write succeeded, so the producer on the US West Coast literally waited on confirmation that its data had landed in HDFS in London. ETL jobs then ran per hourly partition, checking a combination of "which servers should have sent data" against end-of-file markers, and delaying processing for that hour if the check found the data incomplete.

The 2015 move to Google Cloud Platform replaced nearly every physical component of that design while keeping its logical shape — the notes give this direct mapping: Kafka becomes PubSub, HDFS becomes Cloud Storage, and Hive/MapReduce become BigQuery. The new pipeline has four components: a File Tailer watches log files for new events, an Event Delivery Service reformats and forwards them, a Reliable Persistent Queue provides the durable intermediate storage the old design lacked, and ETL jobs deduplicate and export from the queue into hourly HDFS-equivalent partitions. The choice of queue was not automatic — Spotify evaluated both Kafka 0.8 and Cloud Pub/Sub. Kafka 0.8 improved on 0.7 and added Mirror Maker for cross-datacenter mirroring, but it failed Spotify's stress test: if an admin removed brokers from a cluster, the producer entered a state it couldn't self-recover from, and Mirror Maker only mirrored data on a best-effort basis. Pub/Sub, by contrast, passed a 2-million-events-per-second producer test with almost no server errors, and a consumer test pulling batches of 1,000 messages held median end-to-end latency around 20 seconds with no observed message loss. Spotify chose Pub/Sub, and processing itself moved from MapReduce batch jobs to Google Dataflow's hourly-windowed streaming jobs — the same shift that produced Scio, Spotify's Scala API for Apache Beam, which it later open-sourced.

The payoff scaled with the architecture: by the end of Q1 2019 Spotify was producing over 8 million events per second at peak and more than 350 TB of raw daily data, on a system that, unlike the on-prem design, no longer treats a single Hadoop cluster as the one thing that must never go down. Around this event-delivery core, Spotify frames its broader data platform as three components — event delivery (collecting data), data processing (running the 38,000+ scheduled pipelines on BigQuery, Flink, or Dataflow via Scio), and data management (attribution, privacy, retention, access control, lineage, and quality checks on each data endpoint) — with the platform team deliberately balancing centralized infrastructure ownership against distributed control, allowing event consumers to control the data update without requiring the infrastructure team.

*See also: [[spotify-pubsub-scio]] · [[twitter-lambda-to-kappa-pipeline]] · [[notion-postgres-to-datalake-migration]]*
