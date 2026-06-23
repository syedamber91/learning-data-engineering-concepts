---
title: "Batch vs Streaming"
area: "Data Pipelines"
topic: "Processing Paradigms"
tags: [batch-processing, streaming, data-pipelines, lambda-architecture, latency, throughput]
---

# Batch vs Streaming

*Part of [[processing-paradigms-moc|Processing Paradigms]] · [[data-pipelines-moc|Data Pipelines]]*

← Prev: [[normalization-vs-denormalization|Normalization vs Denormalization]] · Next: [[idempotency|Idempotency]] →

## Recap — where we just were

In [[normalization-vs-denormalization|Normalization vs Denormalization]] you made a deliberate choice about *how* to store data: keep every fact in one place (normalized) for safe writes, or duplicate facts across a wide table (denormalized) for fast reads. That tension — accuracy vs speed — resurfaces at the pipeline level. Now that you know how to shape your tables, the next question is: *when* should you process the data flowing into them? Should you wait and handle a large pile all at once, or should you handle each piece the instant it arrives? That is exactly what batch vs streaming answers.

---

## Level 1 — The Big Idea

**Batch processing** collects a large, bounded chunk of data over time and processes the whole chunk in one go, triggered on a schedule.

**Streaming processing** handles each piece of data the moment it arrives — continuously, with no waiting.

The core trade-off: **batch wins on throughput** (how much total work gets done efficiently), **streaming wins on latency** (how quickly a single result comes back).

**Everyday analogy — the laundromat:**

- **Batch** = collect all your dirty clothes in a hamper for a week, then run one big load on Sunday morning. Efficient use of water and time, but if you need a clean shirt on Thursday, you are out of luck.
- **Streaming** = wash each item the moment it gets dirty. You always have clean clothes available, but the machine runs constantly.

Neither is universally better. You choose based on whether you need the shirt *right now* or whether saving effort matters more.

<!-- mermaid-source:
graph LR
    A[Data arrives] -->|wait and collect| B[Batch Job runs on schedule]
    B --> C[Result available hours later]

    D[Data arrives] -->|process immediately| E[Stream Processor]
    E --> F[Result available in milliseconds]
-->
![[batch-vs-streaming-d1.svg]]

---

## Level 2 — How it actually works

Now that you have the intuition, let's open each approach and look at the actual machinery.

### Batch processing — collect, trigger, process, output

A batch pipeline follows a fixed rhythm: data accumulates in storage, a scheduler fires the job, the processor reads the whole dataset, and output lands in a warehouse or report.

<!-- mermaid-source:
graph TD
    A[Data Source - orders, logs, sensor readings] -->|data lands in storage| B[Data Store - S3 or a database]
    B -->|scheduler fires at midnight| C[Batch Processor - Spark or SQL job]
    C -->|reads all of yesterdays rows| D[Transform and aggregate]
    D --> E[Output - data warehouse or report]
-->
![[batch-vs-streaming-d2.svg]]

A **scheduler** (the subject of [[dags-schedulers|DAGs & Schedulers]]) wakes the job at a fixed time — say, 2 AM every night. The job reads every row from the previous day, crunches the numbers, and writes the results. By morning the dashboard shows yesterday's totals. The data is complete and accurate, but always slightly stale.

**Why batch still dominates many pipelines:** the input is fixed, so you can re-run the same job on the same file as many times as you need. It is easier to test, easier to debug, and one large pass through data is often cheaper than thousands of tiny operations.

### Streaming processing — event arrives, process immediately, write result

A streaming pipeline is event-driven: each new piece of data triggers processing the instant it lands.

<!-- mermaid-source:
graph LR
    A[Event Source - click, payment, sensor] -->|publish| B[Message Queue - Kafka]
    B -->|consume continuously| C[Stream Processor - Flink or Spark Streaming]
    C -->|within milliseconds| D[Sink - live dashboard, alert, or database]
-->
![[batch-vs-streaming-d3.svg]]

A **message queue** (like **Apache Kafka**) acts as a shock absorber: producers drop events in, the processor pulls them out one by one. The processor applies logic — filter, count, join — and writes the result immediately. If a fraudulent payment arrives, the fraud-detection pipeline can flag it within 50 milliseconds, before the charge clears.

The critical structural difference: batch works on a *bounded* set (yesterday's file, which has a clear start and end). Streaming works on an *unbounded* stream — data keeps arriving forever, so the system must be designed never to stop.

### When systems use both — Lambda and Kappa

Because each paradigm has blind spots, large-scale systems often combine them.

**Lambda architecture** runs a batch pipeline and a streaming pipeline in parallel, then merges their answers:

<!-- mermaid-source:
graph TD
    S[Data Source] --> BL[Batch Layer - accurate but slow]
    S --> SL[Speed Layer - fast but approximate]
    BL --> SV[Serving Layer - merge results]
    SL --> SV
    SV --> Q[User Query]
-->
![[batch-vs-streaming-d4.svg]]

The speed layer gives you a near-real-time estimate; the batch layer corrects it with accurate numbers a few hours later.

**Kappa architecture** removes the batch layer entirely: use streaming only, but keep all raw events in a replayable log. If a bug forces you to reprocess history, you replay the log through the stream processor. One codebase, not two.

---

## Level 3 — See it with real numbers

**Scenario:** an e-commerce site generates 500,000 order events per day. You need total revenue by product category.

### Option A — nightly batch job

Orders land in an S3 bucket as JSON files throughout the day. At 2 AM, a **PySpark** job reads all 500,000 rows:

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as spark_sum

spark = SparkSession.builder.appName("daily-revenue").getOrCreate()

orders = spark.read.json("s3://orders/2026-06-22/*.json")

revenue = (
    orders
    .groupBy("category")
    .agg(spark_sum("price").alias("total_revenue"))
    .orderBy("total_revenue", ascending=False)
)

revenue.write.parquet("s3://reports/revenue/2026-06-22/")
```

- **Input:** 500,000 rows of JSON, roughly 400 MB
- **Run time:** ~4 minutes on a modest cluster
- **Latency:** up to 26 hours — data from 00:01 waits until 2 AM the next night
- **Output:** a clean Parquet file, accurate and complete, ready for the BI dashboard

### Option B — continuous streaming job

A **Spark Structured Streaming** job reads from **Kafka** as orders arrive and keeps a running total:

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as spark_sum

spark = SparkSession.builder.appName("live-revenue").getOrCreate()

stream = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "orders")
    .load()
)

live = (
    stream
    .groupBy("category")
    .agg(spark_sum("price").alias("running_revenue"))
)

live.writeStream.outputMode("complete").format("console").start().awaitTermination()
```

- **Latency:** 50–200 ms end-to-end per event
- **Output:** a live counter updating on the dashboard in near real time
- **Trade-off:** the running total is an approximation until the pipeline has seen all events for the day; late-arriving events (network delays, retries) can cause slight undercounts mid-day

---

## Level 4 — In the real world & common traps

### Named use case: Netflix overnight encoding vs live recommendations

Netflix runs **both** paradigms, each where it fits best:

- **Batch:** every night, a **Spark** job scans billions of viewing records and re-trains the global recommendation model. The job takes hours and processes terabytes, but it does not need to be instant — the model just needs to be fresh by morning.
- **Streaming:** the instant you finish an episode, a **Kafka**-**Flink** pipeline processes that event and refreshes "what to watch next" within one second. If Netflix waited for the overnight batch run, your recommendation would be 24 hours stale.

Same company, same raw data, two paradigms chosen deliberately for different latency requirements.

### Common misconceptions

**People think: "Streaming is always better — why would anyone use batch?"**
Actually, batch is simpler to write, far easier to debug (the input is a fixed file you can inspect and replay), often cheaper to run, and produces more accurate results because it sees the *complete* dataset. For monthly invoices, payroll, or training machine-learning models, batch is the right tool. Streaming adds real engineering complexity you should only accept when low latency genuinely matters to the business.

**People think: "Real-time streaming means zero latency."**
Actually, "real-time" in data engineering typically means *milliseconds to seconds*, not zero. Every streaming pipeline still has network hops, serialization, processing windows, and write delays. Fifty milliseconds is excellent engineering. Zero milliseconds violates physics.

**People think: "Lambda architecture is the safe, modern best practice."**
Actually, Lambda means maintaining two separate codebases — one batch, one streaming — that must produce identical results. Any logic change must be made in both places, doubling the risk of bugs and silent divergence between layers. Many teams now prefer **Kappa architecture** specifically to avoid this maintenance burden.

---

## Level 5 — Expert view

### How batch and streaming relate to neighbouring concepts

| Concept | Relationship |
|---|---|
| [[dags-schedulers\|DAGs & Schedulers]] | Batch jobs are *triggered* by schedulers; a DAG defines the ordered steps inside a batch pipeline |
| [[idempotency\|Idempotency]] | Essential in both paradigms: when a batch job retries or a stream processor replays an event, idempotency ensures you never double-count |
| [[transactions-acid\|Transactions & ACID]] | Full ACID guarantees are expensive; streaming systems often weaken isolation for speed, making exactly-once delivery a hard engineering problem |
| [[data-quality-validation\|Data Quality & Validation]] | Batch pipelines can validate the whole dataset in one pass; streaming pipelines must validate each row in flight, with incomplete context |

### Trade-offs at a glance

| Dimension | Batch | Streaming |
|---|---|---|
| Latency | Minutes to hours | Milliseconds to seconds |
| Throughput efficiency | Very high — one optimized pass | High, but bounded by event rate and always-on overhead |
| Operational complexity | Low — fixed input, easy replay | High — unbounded input, state management, fault recovery, watermarks |
| Infrastructure cost | Efficient — spin up, run, shut down | Higher — always-on cluster |
| Accuracy | High — sees the complete dataset | Lower initially — partial state until all events arrive |
| Reprocessing on bug fix | Easy — re-run the job on the same file | Harder — must replay the full event log |

### Edge cases and scale nuances

**Micro-batching:** **Spark Structured Streaming** does not actually process one event at a time. It collects events into tiny time windows (every 100 ms, for example) and runs a mini-batch over each window. This is fast enough for most "streaming" use cases while reusing the mature batch execution engine. True event-at-a-time processing — as in **Apache Flink** — achieves genuinely lower latency but is more complex to operate.

**Watermarks:** a streaming processor computing a total over a five-minute window needs to know when it has seen *all* events for that window. But events arrive late — a mobile app might buffer clicks while offline and flush them minutes after the fact. A **watermark** is a configurable threshold: "treat any event arriving more than X seconds late as lost." Set it too tight and you silently drop valid data; set it too loose and results are delayed. There is no universally correct answer — it is a business decision about how much late data you can tolerate.

**Backpressure:** if events arrive faster than the processor can handle, the backlog in the message queue grows. Batch jobs have no equivalent problem — the file simply waits. Well-designed streaming systems detect backpressure and slow down producers or scale up consumers automatically; poorly designed ones fall over under load spikes.

---

## Check yourself

**Memory hook:** *Batch = Sunday laundry (efficient, scheduled, one big pile). Streaming = wash each item the moment it is dirty (instant, continuous, never stops).*

**Q1: A bank needs to block a fraudulent credit-card charge within one second of it being made. Should it use batch or streaming, and why?**
A: Streaming. A batch job introduces minutes to hours of latency, so the fraudulent charge would already be approved before the job ever runs. A streaming pipeline processes the payment event as it arrives and can block it in under a second.

**Q2: What is the main operational downside of a Lambda architecture?**
A: You must maintain two separate codebases — a batch job and a streaming job — that must produce identical results. Any logic change must be applied in both places, which doubles the risk of divergence and bugs.

**Q3: Why is exactly-once delivery in a streaming system difficult to achieve?**
A: A processor can crash mid-event, forcing a replay of the last message. Without careful design, the same event is processed twice, corrupting counts or totals. Making replay safe requires [[idempotency|Idempotency]] — ensuring that processing the same event twice produces the same result as processing it once — which adds significant engineering complexity.

---

## Connects to

[[dags-schedulers|DAGs & Schedulers]] · [[idempotency|Idempotency]] · [[transactions-acid|Transactions & ACID]] · [[data-quality-validation|Data Quality & Validation]] · [[normalization-vs-denormalization|Normalization vs Denormalization]]

---

## Coming up next

[[idempotency|Idempotency]] — now that you know pipelines can re-run (batch jobs retry on failure, streaming processors replay events), you immediately need to know how to make those re-runs safe; idempotency is the guarantee that running the same operation twice produces exactly the same result as running it once, and it is the property that makes both batch and streaming pipelines trustworthy at scale.