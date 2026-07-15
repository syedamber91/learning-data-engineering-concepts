---
persona: vutr
kind: concept
sources:
- raw/clickhouse-internals/clickhouse-real-time-insight-in-15.md
last_updated: '2026-07-15'
qc: passed
slug: tinybird-ingestion-and-scaling
topics:
- clickhouse-internals
---

Tinybird departs from the classic shared-nothing deployment pattern (where each replica holds a subset of data) in how it manages compute. Instead, it stores data in object storage (S3 or GCS), and each replica has local SSDs used purely as a cache — which makes replicas **stateless**. That statelessness is what lets Tinybird scale horizontally (add or remove replicas to match write/read load, with no data-rebalance process needed when nodes come and go) and vertically (change a replica's resource spec), and combining both gives the platform a way to adapt to differing concurrency and latency needs. Vu frames this as conceptually similar to the storage/compute separation used by some cloud data platforms generally, without naming ClickHouse's own multi-master replication model as the specific point of contrast (see [[clickhouse-replication-and-keeper-consensus]] for that mechanism).

**Ingestion** happens through Kafka, object storage, or streamed HTTP payloads via the Events API. Each ingestion source is configured as a **datasource** (schema, ClickHouse storage engine, associated connection), and a **connection** holds the physical-source credentials (e.g., a Kafka connection's bootstrap servers, key, and secret). To protect cluster resources, Tinybird batches incoming insertions over a flush interval (length depends on the billing plan) before flushing — trading some latency for reduced ingestion pressure. Failure handling is split by error type: retriable errors go to a staging area for later re-ingestion, while non-retriable errors are routed to a quarantine table for manual investigation — Vu explicitly likens this to the dead-letter-queue pattern used in streaming systems like Kafka. Beyond retry handling, Tinybird applies **two-phase backpressure** to keep one noisy ingestion source from starving others: phase one delays ingestion from that source while continuously monitoring the number and age of delayed insertions; if those metrics cross a threshold, phase two applies a temporary rate limit to that source specifically.

The **Kafka Connector** gets its own design discussion. It's a Python service deployed as one Kubernetes cluster spanning multiple regions — a deliberately unusual choice given Python isn't typically associated with high-performance systems. Tinybird's stated reasoning: Python was already the language used for their other backend services, and the Global Interpreter Lock (GIL) isn't a bottleneck here because the actual bottlenecks are network I/O and ClickHouse's own ingestion capacity; for the components that do need to bypass the GIL, they use native libraries such as the `confluent_kafka` C++ bindings for Kafka communication. Architecturally, the connector uses a **controller/worker model**: a controller manages multiple workers, one or more workers are assigned to a given Kafka topic, and the connector's scale is a function of how many worker instances are assigned to that topic.

*See also: [[tinybird]] · [[tinybird-pipes-serving-and-dev-experience]] · [[clickhouse-replication-and-keeper-consensus]]*
