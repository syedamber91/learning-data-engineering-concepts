---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Related: [[uber-lambda-kafka]] · [[netflix-iceberg-maestro]] · [[linkedin-kafka-beam]] · [[meta-velox-tectonic]] · [[twitter-kappa-migration]] · [[spotify-pubsub-scio]] · [[doordash-flink-iceberg]] · [[lambda-vs-kappa]] · [[batch-reprocessing-blindness]]

## Comparisons
Two architectural camps emerge. [[linkedin-kafka-beam]] and [[uber-lambda-kafka]] keep **Lambda** — parallel batch and stream paths — while [[twitter-kappa-migration]] abandoned Lambda (Scalding+Heron) for **Kappa** (PubSub+Dataflow+BigTable), trading complexity for ~10s stabilized latency and ~1GB/s throughput.

On the messaging backbone, **Kafka** is not universal. [[linkedin-kafka-beam]] invented it and [[uber-lambda-kafka]] runs one of its largest deployments, but [[spotify-pubsub-scio]] fled Kafka 0.8 to Google Cloud Pub/Sub after it failed a stress test, and [[meta-velox-tectonic]] rolled its own Scribe queue (15TB/s in, 110TB/s out) instead. [[doordash-flink-iceberg]] went the other way — moving *toward* open-source Kafka+Flink.

On table formats, [[netflix-iceberg-maestro]] migrated ~1.5M Hive tables to **Iceberg** and [[doordash-flink-iceberg]] chose Iceberg over Delta Lake for Flink-integration maturity, while [[uber-lambda-kafka]] leans on Hudi.

Google Cloud is a recurring destination: [[twitter-kappa-migration]] (Dataflow/BigTable), [[spotify-pubsub-scio]] (Pub/Sub), and [[uber-lambda-kafka]] (2024 migration).

## Open questions
- Why did [[linkedin-kafka-beam]] and [[uber-lambda-kafka]] keep Lambda while [[twitter-kappa-migration]] found Kappa worth the migration — what workload differences drove opposite calls?
- [[twitter-kappa-migration]] reports only 95%+ result match with the old batch pipeline — where does the remaining <5% discrepancy come from, and is it acceptable?
- Was [[spotify-pubsub-scio]]'s Kafka producer instability specific to the 0.8 version, and would a modern Kafka have avoided the Pub/Sub migration?
- [[doordash-flink-iceberg]] deploys each Flink app as a separate Kubernetes pod — how does that isolation choice trade off against resource efficiency at 30M messages/sec?
- How does [[meta-velox-tectonic]]'s Velox acceleration library interact with its consolidation down to just PrestoSQL and MySQL dialects?

## Synthesis
Across these seven case studies, scale forces the same recurring choices: how to reconcile batch and stream ([[lambda-vs-kappa]]), and how to escape [[batch-reprocessing-blindness]] where a system reprocesses whole partitions because it can't tell what changed. The messaging layer is contested — [[linkedin-kafka-beam]] birthed Kafka and [[uber-lambda-kafka]] runs it at trillions of messages/day, yet [[spotify-pubsub-scio]] and [[meta-velox-tectonic]] routed around Kafka entirely. The durable lesson is consolidation and maturity over novelty: [[meta-velox-tectonic]] collapsed twelve engines into two SQL dialects, and [[netflix-iceberg-maestro]] and [[doordash-flink-iceberg]] both bet on Iceberg for the table format that finally makes incremental processing tractable.

## Related topics
- [[airflow]] — Netflix's Maestro and the other case studies are production orchestration systems solving the same DAG-scheduling problem space Airflow was built for.
- [[data-architecture-warehouse-lake-lakehouse-mesh-lambda-kappa]] — The case studies are a live proving ground for the Lambda-vs-Kappa debate — LinkedIn/Uber kept Lambda while Twitter migrated to Kappa.
- [[kafka]] — LinkedIn invented Kafka and Uber runs it at trillions of messages/day, while Spotify and Meta deliberately routed around it — the case studies map Kafka's real adoption boundary.
- [[iceberg]] — Netflix migrated ~1.5M Hive tables to Iceberg and DoorDash chose Iceberg over Delta for Flink maturity, making Iceberg the table-format winner in these studies.
- [[flink]] — DoorDash's move toward open-source Kafka+Flink (one pod per Flink app, 30M msgs/sec) is a headline case for Flink at production scale.
