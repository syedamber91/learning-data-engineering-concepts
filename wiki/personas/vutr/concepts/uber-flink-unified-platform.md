---
persona: vutr
kind: concept
sources:
- raw/uber-data-infrastructure-case-studies/how-did-uber-build-their-data-infrastructure.md
- raw/uber-data-infrastructure-case-studies/i-spent-7-hours-understanding-ubers.md
last_updated: '2026-07-15'
qc: passed
slug: uber-flink-unified-platform
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Uber picked Apache Flink for stream processing because it supports many workloads via native state management and checkpointing (for failure recovery), scales easily while handling backpressure well, and has a large, active open-source community. On top of stock Flink, Uber built two platform layers.

**FlinkSQL** lets users write Apache Calcite SQL instead of Flink's native API. The system converts SQL input into a logical plan, runs it through an optimizer to produce a physical plan, then translates that physical plan into an actual Flink job via the Flink API — the same compile-plan-optimize-execute shape SQL engines generally use, applied here to unbounded streaming input rather than bounded batch input. Hiding this complexity from users pushed operational overhead onto Uber's infrastructure team, who had to solve two problems that FlinkSQL's abstraction created: **resource estimation and auto-scaling** (Uber studied the correlation between common job types and their resource needs, and continuously monitors workload shifts between peak and off-peak hours to drive auto-scaling) and **job monitoring with automatic failure recovery** (since users can't see behind FlinkSQL's abstraction, Uber built a rule-based engine that compares a job's live metrics against expectations and takes actions like restarting the job automatically).

**The unified deployment/management/operation architecture** is a three-layer stack. The platform layer organizes business logic and integrations with other platforms (ML, workflow management, SQL compilation) and turns that logic into a standard Flink job definition. The job management layer owns the Flink job's whole lifecycle — validation, deployment, monitoring, failure recovery — stores job state (checkpoints, metadata), acts as a proxy routing jobs to physical clusters based on job metadata, and continuously monitors all jobs' health to auto-recover failed ones; it exposes API abstractions upward to the platform layer. The bottom layer is the compute clusters and storage backend (HDFS, S3, or GCS for job checkpoints), abstracted so the layers above don't care whether they're running on-prem or in the cloud.

The result, per Uber, is that Flink became the company's central real-time processing platform, responsible for thousands of jobs — feeding Pinot for OLAP serving ([[uber-pinot-upsert-mechanism]]) and underpinning both [[uber-multi-region-failover-and-backfilling|Uber's all-active multi-region failover]] and its [[uber-realtime-use-case-tradeoffs|real-time use cases]].

*See also: [[uber-data-platform]] · [[uber-kafka-scale-customizations]] · [[uber-pinot-upsert-mechanism]]*
