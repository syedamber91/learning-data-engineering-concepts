---
title: "Batch vs Streaming"
area: "Data Pipelines"
topic: "Processing Paradigms"
tags: [batch-processing, streaming, data-pipelines, latency, throughput, lambda-architecture]
---

# Batch vs Streaming

*Part of [[processing-paradigms-moc|Processing Paradigms]] · [[data-pipelines-moc|Data Pipelines]]*

## In one line
**Batch processing** collects data into a fixed pile and crunches it all at once on a schedule; **streaming** processes each piece of data the instant it arrives, one event at a time, without ever waiting.

## Picture this
Imagine a restaurant at closing time. The manager gathers *all* the receipts from the whole day, then adds them up at midnight to get the daily total — that is **batch processing**: you wait, collect everything, then compute in one go.

Now picture a cashier with a running till that updates the total the moment each customer pays — that is **streaming**: every new event immediately changes the result, with no waiting for closing time.

## How it actually works

**Batch processing** treats data as *bounded* — meaning the dataset has a defined beginning and end, like "all orders placed yesterday." A job is scheduled (say, at 2:00 AM), reads every record in that fixed chunk, performs the computation (totals, joins, transformations), writes the results somewhere, and then **stops**. Nothing runs again until the next scheduled window.

The key insight is why batch is so efficient at scale: reading a huge file sequentially from disk is one of the fastest things a computer can do. The system never has to pause and wait; it just ploughs through the data from start to finish. This gives batch excellent **throughput** — the amount of data processed per second.

The cost is **latency** — the delay between an event happening in the real world and you seeing its result. If your batch job runs at 2 AM and processes yesterday's data, your results are already up to 24 hours old before anyone looks at them.

**Streaming** treats data as *unbounded* — a never-ending flow of events, like a river that never stops. The system stays alive permanently, listening for new events via a message queue (tools like **Apache Kafka** act like a post box: producers drop messages in, consumers pick them up). Each event is processed the moment it arrives, often within milliseconds.

Streaming is harder to build for three reasons:

1. **Out-of-order events** — a network packet from 3 seconds ago can arrive after one from 5 seconds ago. Your logic must handle this.
2. **State management** — if you want a running total, you need to remember the previous total somewhere while processing the next event.
3. **Fault tolerance** — if the process crashes mid-stream, you must resume without double-counting any event.

Many real systems use **both** paradigms together in a pattern called **Lambda Architecture**: a streaming layer gives fast (but possibly approximate) results right now, while a batch layer runs nightly to produce accurate, corrected final numbers.

## Worked example

Suppose your e-commerce site takes 1,000,000 orders per day.

**Batch approach — nightly revenue report:**

```python
# Triggered once at 2:00 AM by a scheduler (e.g. Airflow)
import datetime

yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()

result = db.query(
    "SELECT SUM(amount) AS revenue FROM orders WHERE order_date = %s",
    [yesterday]
)
# Result after scanning all 1,000,000 rows:
# {"revenue": 482391.50}

# Latency: data is up to 24 hours old when the report lands.
# Throughput: 1,000,000 rows in one efficient sequential pass — fast and cheap.
db.write("daily_revenue_summary", {"date": yesterday, "revenue": 482391.50})
```

**Streaming approach — live revenue dashboard:**

```python
# Runs continuously, 24/7, listening to Kafka
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer("orders-topic", bootstrap_servers="kafka:9092")
running_total = 0.0

for message in consumer:          # this loop never ends — orders keep arriving
    order = json.loads(message.value)
    running_total += order["amount"]
    dashboard.update("live_revenue", running_total)
# Latency: each order updates the dashboard within ~50–200 milliseconds.
# Cost: always-on infrastructure, plus careful handling of crashes and replays.
```

The batch job is simpler and cheaper to operate. The streaming job keeps the dashboard current to the second, but demands more engineering to handle failures safely.

## In the real world

**Spotify** uses both paradigms. Batch jobs run each night — and once a year — to compute your "Wrapped" statistics: total minutes listened, top artists, etc. A 24-hour delay is perfectly acceptable for a year-in-review card. Streaming jobs, by contrast, update the play-count leaderboard and "Now Playing" feed within seconds, because listeners expect those numbers to reflect what is happening right now. Neither paradigm replaces the other; they solve different problems.

## Common misconceptions

**People think** streaming is always better because faster is always better — **actually** streaming is significantly more complex and expensive to build and maintain. For a report that runs once a day, streaming adds engineering cost for zero benefit.

**People think** batch means "slow" — **actually** batch can process billions of rows faster than an equivalent streaming system because it uses optimised bulk-read patterns (reading entire files sequentially) that streaming cannot leverage.

**People think** you must choose one or the other — **actually** most mature data platforms run both. Streaming handles "need it now" cases; batch handles "need it exactly right" cases. Lambda Architecture exists precisely because neither alone is enough.

## How it relates & differs

| Concept | How it RELATES | How it DIFFERS |
|---|---|---|
| [[dags-schedulers\|DAGs & Schedulers]] | Batch jobs are almost always triggered by a scheduler (e.g., an Airflow DAG fires at 2 AM). Streaming jobs also use orchestration to start and monitor the long-running process. | A DAG/scheduler is the *trigger mechanism*; batch vs streaming is about *how data is read and processed* — not just when the job starts. |
| [[idempotency\|Idempotency]] | Both paradigms need idempotent (safe-to-replay) jobs. If a batch re-runs or a streaming consumer replays a message after a crash, the result must not be double-counted. | Idempotency is *more urgently critical* in streaming because mid-stream failures are frequent and the system must resume safely without corrupting running totals on the fly. |
| [[data-quality-validation\|Data Quality & Validation]] | Both paradigms must validate incoming data (e.g., is `amount` a positive number? Is the `user_id` present?). | In batch, you can validate after collecting the whole window and quarantine bad rows in bulk. In streaming, you must validate each event *individually the moment it arrives* and decide immediately — drop it, flag it, or halt. |

## Why you'd use it (and when not to)

Use **batch** when a stale answer is acceptable (end-of-day reports, monthly invoices, nightly ML model training) and when you want simplicity and low infrastructure cost. Use **streaming** when latency genuinely matters — fraud detection must fire within seconds of a suspicious transaction, not the following morning. The trap is over-engineering: if a one-hour-old answer is good enough for your use case, building a streaming pipeline is one of the most common and costly mistakes in data work. Ask "how old can this answer be?" before choosing.

## Check yourself

**Memory hook:** Batch = bucket (fill it up completely, then pour it all out). Stream = tap (water flows the instant you open it).

**Q1: What does "bounded" mean in the context of batch processing, and why does it matter?**
A: Bounded means the dataset has a defined start and end — for example, "all orders from yesterday." This matters because the batch job can read a fixed, known chunk of data all at once, which is what makes it efficient. Streaming data is unbounded — it has no end — so the job must run forever.

**Q2: Name two things that make streaming harder to build than batch.**
A: (Any two of:) events can arrive out of order; the system must maintain state (e.g., a running total) across many individual events; the system must recover from crashes without double-counting records.

**Q3: What is Lambda Architecture and why would you use it?**
A: Lambda Architecture runs a streaming layer (fast, approximate answers in milliseconds) and a batch layer (slower, accurate answers) in parallel. You use it when you need both speed *and* correctness — the stream gives you a live dashboard, and the nightly batch job corrects any errors the stream introduced.

## Connects to

[[dags-schedulers|DAGs & Schedulers]] · [[idempotency|Idempotency]] · [[data-quality-validation|Data Quality & Validation]] · [[tables-keys-sql-basics|Tables, Keys & SQL Basics]]