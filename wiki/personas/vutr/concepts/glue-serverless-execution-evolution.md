---
persona: vutr
kind: concept
sources:
- raw/cloud-kubernetes-docker-infrastructure-tooling/i-spent-6-hours-learning-aws-glue.md
last_updated: '2026-07-15'
qc: passed
slug: glue-serverless-execution-evolution
topics:
- cloud-kubernetes-docker-infrastructure-tooling
---

[[aws-glue|Glue]]'s promise of "just submit the job" hides three real architectural generations behind it, and the source's account of each is really a story about start-time variance. **Glue 1.0** was cluster-based and batch-oriented, offering three ways to start a job: reuse a pre-allocated cluster, allocate from a service-wide warm pool, or provision a brand-new cluster from EC2. A job could only begin once its entire cluster was ready, and idle clusters were retired after a fixed period to control cost. The result was high variability: warm starts (reusing or warm-pool clusters) landed under a minute, but cold starts — provisioning a new cluster from scratch — took 8 to 10 minutes.

**Glue 2.0**, introduced in 2020, attacked that variance directly with a new resource manager and a lightweight Spark application stack. Jobs could now begin execution as soon as the *first* instance was ready, rather than waiting on the whole cluster; Spark's own scheduler was modified to pull executors from Glue's resource manager instead of a cluster-based system like YARN; and the resource manager kept a warm pool of pre-initialized Spark instances, paired with ML models predicting EC2 instance demand across regions, to push cold-start time down to under 10 seconds. **Glue 3.0** then added true auto-scaling — dynamically resizing the cluster *during* a running job — by extending Spark's shuffle-tracking algorithm so workers could be safely scaled down without losing intermediate shuffle state, plus deliberate dampening of frequent resize events to avoid resource churn.

Two more specific engineering efforts round out the performance story. In 2021, AWS introduced a **cloud shuffle storage plugin** that writes Spark shuffle data to S3 instead of local disk, decoupling shuffle storage from compute — the classic problem the source names is that skewed partitions or under-provisioned local storage can exhaust an individual worker during a shuffle, traditionally solved only by repartitioning the dataset or adding more cluster resources. Making this work required extending Spark internals directly: the block manager and the shuffle reader/writer. Support for other cloud storage providers followed in 2022. Separately, also in 2021, Glue introduced **native SIMD vectorized readers** to remove a CPU bottleneck in ETL jobs converting raw CSV/JSON into Parquet: traditional deserialization was constrained by CPU and memory bandwidth that had fallen behind S3's improving network speeds, so the readers were reimplemented in C++ using SIMD instructions for micro-parallel parsing/tokenization/indexing, storing the result in an in-memory Arrow-based columnar format that both optimizes memory-bandwidth use and reduces the cost of converting into Parquet on write.

*See also: [[aws-glue]] · [[glue-dynamicframe-and-schema-inference]] · [[glue-data-catalog-and-crawlers]]*
