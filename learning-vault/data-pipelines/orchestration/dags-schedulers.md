---
title: "DAGs & Schedulers"
area: "Data Pipelines"
topic: "Orchestration"
tags: [dags, schedulers, airflow, orchestration, data-pipelines, dependencies]
---

# DAGs & Schedulers

*Part of [[orchestration-moc|Orchestration]] · [[data-pipelines-moc|Data Pipelines]]*

← Prev: [[idempotency|Idempotency]] · Next: [[data-quality-validation|Data Quality & Validation]] →

## Recap — where we just were

In [[idempotency|Idempotency]] you built the safety net for pipeline failures: design every step so that running it twice produces exactly the same result as running it once — upserts instead of plain inserts, deterministic keys instead of randomly generated IDs. Now you have steps that are safe to retry. The next question is: *who decides which steps run, in what order, and what to do when one of them fails?* That is the job of a **DAG** and a **scheduler**.

---

## Level 1 — The big idea

A **DAG** (directed acyclic graph — pronounced "dag") is a diagram, a map, that shows every task in a pipeline and which tasks must finish before others can start.

A **scheduler** is the engine that reads that map and actually runs the tasks at the right time, in the right order, retrying them automatically when they fail.

**Everyday analogy — a recipe and a chef:**
A recipe (DAG) lists every step — chop vegetables, boil water, fry onions, add sauce, plate — and shows the order: you cannot add sauce before frying onions; you cannot plate before adding sauce. The chef (scheduler) reads the recipe, keeps track of what is done, and starts the next step the moment its prerequisites are finished, running independent steps at the same time when possible.

<!-- mermaid-source:
graph LR
    A[Chop Vegetables] --> C[Fry Onions]
    B[Boil Water] --> D[Cook Pasta]
    C --> E[Add Sauce]
    D --> E
    E --> F[Plate Dish]
-->
![[dags-schedulers-d1.svg]]

Notice: arrows point one way only, and there are no loops — you never cycle back to a step you already completed. These two properties are what make it a *directed acyclic* graph, and together they guarantee the scheduler can always find a task that is ready to run next.

---

## Level 2 — How it actually works

Now that you have the intuition, let's unpack each word in *directed acyclic graph* and then trace exactly what the scheduler does with it.

### The graph: nodes and edges

A **graph** is a set of *nodes* (things) connected by *edges* (relationships). In a pipeline DAG, every **node** is a task — "download file", "run SQL query", "send report" — and every **edge** (arrow) means "this task must finish before that task can start."

### Directed: one-way arrows

**Directed** means every arrow has a direction. Task A → Task B means A must finish before B starts. The reverse is not implied. This is how you encode *prerequisite* logic.

### Acyclic: no loops, ever

**Acyclic** means there are zero cycles — no path that ever circles back to a task already in the run. Why does this matter? If Task A depended on Task B and Task B depended on Task A, neither could ever start — a logical deadlock. Schedulers reject DAGs that contain cycles before running a single line of code.

**A valid DAG — arrows go forward only:**

<!-- mermaid-source:
graph LR
    A[Extract] --> B[Transform]
    B --> C[Load]
-->
![[dags-schedulers-d2.svg]]

**An invalid DAG — a cycle the scheduler immediately rejects:**

<!-- mermaid-source:
graph LR
    X[Step X] --> Y[Step Y]
    Y --> Z[Step Z]
    Z --> X
-->
![[dags-schedulers-d3.svg]]

Step Z depends on Step Y, Step Y on Step X, and Step X on Step Z — none can start. The cycle is the bug; the acyclic constraint is the fix.

### What the scheduler does, step by step

<!-- mermaid-source:
graph TD
    S[Scheduler reads DAG definition] --> I[Find tasks with no unfinished upstream tasks]
    I --> Q[Mark those tasks READY and queue them]
    Q --> W[Send each READY task to a worker process]
    W --> R{Task result}
    R -->|Success| UN[Mark SUCCESS and unblock downstream tasks]
    R -->|Failure| RT[Mark FAILED and retry up to N times]
    RT --> W
    UN --> I
-->
![[dags-schedulers-d4.svg]]

**New term — worker:** the process that actually runs your code. The scheduler is a traffic controller; it never touches your data. Workers are the labourers that execute the SQL query or Python function.

The scheduler loops this constantly. The moment any task succeeds, it re-evaluates which downstream tasks are now unblocked. Tasks with no dependency between them run *in parallel* automatically — no extra effort from you.

---

## Level 3 — See it with real numbers

**Scenario:** a daily revenue pipeline at an e-commerce company processes 1,000,000 order rows every night at 2 AM.

The pipeline has five tasks:

| Task | Depends on | What it does |
|---|---|---|
| extract_orders | — | Pull 1,000,000 rows from the orders database |
| extract_products | — | Pull 50,000 rows from the products database |
| join_data | extract_orders, extract_products | Join orders to products on product_id |
| compute_revenue | join_data | Multiply quantity × price, group by date |
| load_to_warehouse | compute_revenue | Upsert results into daily_revenue table |

<!-- mermaid-source:
graph LR
    EO[Extract Orders] --> JD[Join Data]
    EP[Extract Products] --> JD
    JD --> CR[Compute Revenue]
    CR --> LW[Load to Warehouse]
-->
![[dags-schedulers-d5.svg]]

`extract_orders` and `extract_products` share no dependency with each other, so they start simultaneously — cutting the wall-clock time roughly in half.

**In Apache Airflow (the most common open-source scheduler), this DAG is defined in Python:**

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extract_orders(): ...      # your actual logic here
def extract_products(): ...
def join_data(): ...
def compute_revenue(): ...
def load_to_warehouse(): ...

with DAG(
    dag_id="daily_revenue",
    schedule_interval="0 2 * * *",  # cron: every day at 02:00
    start_date=datetime(2026, 1, 1),
) as dag:

    t_orders   = PythonOperator(task_id="extract_orders",    python_callable=extract_orders)
    t_products = PythonOperator(task_id="extract_products",  python_callable=extract_products)
    t_join     = PythonOperator(task_id="join_data",         python_callable=join_data)
    t_revenue  = PythonOperator(task_id="compute_revenue",   python_callable=compute_revenue)
    t_load     = PythonOperator(task_id="load_to_warehouse", python_callable=load_to_warehouse)

    [t_orders, t_products] >> t_join >> t_revenue >> t_load
```

**Input → execution → result:**

1. Airflow triggers at 02:00. Both `extract_orders` and `extract_products` start simultaneously.
2. At 02:11, both finish. `join_data` is now unblocked and starts.
3. At 02:18, `join_data` finishes. `compute_revenue` starts.
4. At 02:23, `compute_revenue` finishes. `load_to_warehouse` runs the idempotent upsert from the previous lesson.
5. At 02:25, the pipeline is marked SUCCESS. Total: 25 minutes instead of ~40 if every task ran one after another.

If `join_data` fails on step 3, Airflow retries it up to (say) 3 times before marking it FAILED and alerting the on-call engineer — without disturbing the tasks that already succeeded or those downstream.

---

## Level 4 — In the real world & common traps

### Real-world use case: Spotify's daily listening reports

Spotify runs hundreds of DAGs every night to compute listener statistics. A single "daily plays" DAG fans out to dozens of parallel extract tasks — one per country — then funnels into a join, then into a rollup, then into a load into their analytics warehouse. Without a DAG scheduler, engineers would have to manually trigger each script in the right order and babysit every failure. Instead, Airflow handles the sequencing, parallelism, retries, and alerting automatically. Engineers intervene only when a task truly cannot recover on its own.

### Common misconceptions

**People think: a DAG scheduler is just a fancy cron job.**
Actually: cron fires one script at a fixed time with no knowledge of dependencies. A DAG scheduler understands *relationships* between tasks, parallelises independent branches, retries only the failed task rather than the whole pipeline, and keeps a full history of every past run. A scheduler is to cron what a GPS is to a paper map.

**People think: the scheduler runs the actual data processing.**
Actually: the scheduler is only the traffic controller. It decides *when* and *in what order* to hand tasks to workers. The workers are what touch your data. Airflow itself does not move a single byte — your Python functions or SQL queries do that.

**People think: acyclic means the pipeline must be a single straight line.**
Actually: acyclic means no *loops*, not no *branches*. A DAG can fan out to many parallel tasks and then merge back together. A branching tree is perfectly valid. The only illegal shape is a circle that brings you back to a task already visited.

---

## Level 5 — Expert view

### How DAGs & Schedulers relate to neighbouring concepts

| Concept | What it solves | How it relates to DAGs & Schedulers |
|---|---|---|
| **Batch vs Streaming** | *When* to process: chunks on a schedule vs. events the instant they arrive | DAG schedulers are built for *batch*. Streaming pipelines (Kafka, Flink) operate continuously and have no concept of a "run" with a start and end — a DAG scheduler is the wrong tool there |
| **Idempotency** | Making individual steps safe to retry | The scheduler's automatic retry is only useful *because* tasks are idempotent. Without idempotency, a retry after a partial write corrupts data; with it, a retry is just free error recovery |
| **Data Quality & Validation** | Catching bad data before it poisons the warehouse | Data quality checks are themselves DAG tasks: they run after a load step and fail loudly if the data looks wrong, blocking every downstream task until a human investigates |

### Trade-offs: when a DAG scheduler is (and is not) the right tool

**Use it when** you have multiple interdependent steps that benefit from parallelism, you need retries and a history of past runs, and the pipeline runs on a predictable schedule (daily, hourly).

**Skip it when** you have a single short script with no dependencies — cron is simpler and sufficient. Also skip it when you need to react to events in milliseconds: the scheduler's overhead (seconds to minutes per task launch) is far too slow for real-time work.

**Operational edge cases worth knowing:**
- *Backfilling:* if you deploy a new DAG today but need it to run for every past date it missed, schedulers support re-running the DAG for historical dates in order. Because tasks are idempotent, backfills are safe.
- *Fan-out limits:* a DAG that spawns thousands of parallel tasks can overwhelm the worker pool. Production DAGs cap concurrency explicitly.
- *Scheduler availability:* early Airflow had one scheduler process; if it died, no DAGs ran. Modern Airflow 2+ supports multiple scheduler replicas so a single crash does not halt the whole system.

---

## Check yourself

**Memory hook:** *"The DAG is the recipe; the scheduler is the chef. No loops, no deadlocks, no burnt dinner."*

**Q1: What does "acyclic" mean, and why does a DAG require it?**
A1: Acyclic means no cycles — no path that loops back to a task already in the graph. Without this, tasks could form a circular dependency where each waits on the other and nothing can ever start. The scheduler detects and rejects cycles before running anything.

**Q2: In the Level 3 pipeline, why do `extract_orders` and `extract_products` run at the same time?**
A2: They have no dependency on each other — neither lists the other as an upstream task. The scheduler sees both as immediately READY at trigger time and sends them to workers simultaneously, cutting total runtime.

**Q3: Why does the scheduler's automatic retry depend on the tasks being idempotent?**
A3: If a task is not idempotent, retrying it after a partial write could duplicate rows or produce wrong totals. Idempotency guarantees that re-running a task produces the same end state as running it once — so the scheduler can retry freely without corrupting data.

---

## Connects to

[[batch-vs-streaming|Batch vs Streaming]] · [[idempotency|Idempotency]] · [[transactions-acid|Transactions & ACID]] · [[data-quality-validation|Data Quality & Validation]]

---

## Coming up next

[[data-quality-validation|Data Quality & Validation]] — now that a scheduler is running your pipeline on time and retrying failures automatically, the next challenge is: *how do you know the data that arrived is actually correct?* Data quality checks are the last line of defence before silent bad data reaches your warehouse and poisons every report built on top of it.