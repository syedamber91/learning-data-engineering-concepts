---
title: "DAGs & Schedulers"
area: "Data Pipelines"
topic: "Orchestration"
tags: [airflow, orchestration, dag, pipeline, scheduling, data-engineering]
---

# DAGs & Schedulers

*Part of [[orchestration-moc|Orchestration]] · [[data-pipelines-moc|Data Pipelines]]*

## In one line
A DAG is a blueprint of tasks and their "must-run-before" rules; a scheduler is the engine that reads that blueprint and runs each task at the right time, in the right order, automatically.

## Picture this
Imagine making breakfast: you have to **boil water** before you can **brew coffee**, and you have to **toast bread** before you can **butter toast** — but boiling water and toasting bread can happen at the same time. Your recipe card listing these steps and their order is the **DAG**. You following the recipe — actually firing up the kettle and toaster — is the **scheduler**.

The one iron rule: you can never go backwards. You cannot butter toast before toasting it. There are no loops. That "no loops" rule is the "acyclic" part of the name.

## How it actually works

**What is a DAG?**

DAG stands for **Directed Acyclic Graph** — three words worth unpacking one at a time.

- **Graph** — a collection of *nodes* (things) connected by *edges* (relationships). Think of a map where cities are nodes and roads between them are edges.
- **Directed** — each edge has an arrow. "Task A must finish *before* Task B can start." The arrow always points forward, never sideways or backward.
- **Acyclic** — no cycles, no loops. Task A cannot eventually depend on itself. If A → B → C, then C cannot point back to A. This rule matters because a loop would create a deadlock: every task would be waiting for another task that is also waiting.

In a data pipeline, the **nodes are tasks** — things like "download yesterday's sales file", "clean the data", "load it into the warehouse" — and the **edges encode which task must finish before the next one begins**.

**What does a scheduler do?**

A scheduler (Apache Airflow is the most common; Prefect and Dagster are popular alternatives) does three things:

1. **Reads the DAG** — it parses your blueprint to understand what tasks exist and in what order.
2. **Triggers tasks on a schedule** — you tell it "run this pipeline every night at 2 AM" using a **cron expression**, a compact time formula. For example, `0 2 * * *` means "at minute 0 of hour 2, every day."
3. **Handles retries and failures** — if a task fails because the database was temporarily down, the scheduler waits and retries automatically, instead of silently skipping or crashing the whole pipeline.

Critically, the scheduler enforces dependencies for you: it will not start Task B until Task A has reported success. You do not have to write that logic yourself in every script.

## Worked example

Say you work at an e-commerce company and every night you need to:

1. Pull 500,000 rows of order data from the production database.
2. Clean and validate them (remove nulls, fix broken date formats).
3. Load the clean rows into the data warehouse.
4. Send a Slack alert to your team confirming the pipeline finished.

Here is what that looks like as an Airflow DAG in Python:

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extract():   ...  # fetch 500,000 rows from production DB
def transform(): ...  # clean nulls, fix date formats
def load():      ...  # write to warehouse
def notify():    ...  # post Slack message

with DAG(
    dag_id="nightly_orders_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule_interval="0 2 * * *",  # fires at 2:00 AM every night
    max_active_runs=1,              # never run two copies simultaneously
) as dag:

    t_extract   = PythonOperator(task_id="extract",   python_callable=extract)
    t_transform = PythonOperator(task_id="transform", python_callable=transform)
    t_load      = PythonOperator(task_id="load",      python_callable=load)
    t_notify    = PythonOperator(task_id="notify",    python_callable=notify)

    t_extract >> t_transform >> t_load >> t_notify
```

The `>>` operator sets the dependency chain. If `transform` fails at 2:17 AM, Airflow retries it (say, three times, five minutes apart) and only proceeds to `load` once it succeeds — or marks the entire DAG run as failed and alerts you. Nothing downstream runs on bad data.

## In the real world

Airbnb built Apache Airflow internally in 2014 because their data team was managing hundreds of interdependent jobs with hand-written cron scripts. When one script failed, nothing downstream knew about it, so dashboards silently showed stale numbers. Airflow gave them a single graph where every dependency was explicit, failures lit up in a UI, and retries were automatic. Today companies like Stripe, Robinhood, and LinkedIn run thousands of DAGs daily — orchestrating everything from fraud-detection model retraining to nightly billing summaries to the reports that executives read every morning.

## Common misconceptions

**People think DAGs are an Airflow-specific idea — actually** DAGs are a concept from mathematics and computer science that predates Airflow by decades. Apache Airflow, Prefect, Dagster, dbt (for SQL transformations), and Apache Spark all use DAGs internally. The scheduler tool varies; the underlying graph idea is universal.

**People think "acyclic" means tasks can never repeat across different pipeline runs — actually** it means within a *single execution*, no task can be its own ancestor. You can absolutely run the same DAG every night — each night is a fresh *run instance*, not a loop in the graph. The graph structure has no cycles; the scheduler's clock triggers new instances of it on a schedule.

**People think the scheduler fires tasks as fast as possible, ignoring timing — actually** the scheduler fires the DAG on the schedule you define, and it also respects *concurrency limits*. With `max_active_runs=1`, it will not start Tuesday's run until Monday's has fully finished, even if Monday ran late. You control the throttle.

## How it relates & differs

| Concept | How it relates | Key difference |
|---|---|---|
| [[batch-vs-streaming\|Batch vs Streaming]] | Most scheduled DAGs process data in batches — once a night, once an hour. The scheduler decides *when* the batch fires. | Batch vs Streaming is about *how data flows*; DAGs are about *how tasks are ordered and triggered*. One answers "how much at once?", the other answers "in what sequence?" |
| [[idempotency\|Idempotency]] | Schedulers retry failed tasks automatically. If a task is not idempotent — meaning running it twice produces different or duplicate results — a retry can insert 500,000 rows twice into your warehouse. | Idempotency is a property of individual tasks; the DAG is the structure that *triggers* those retries. They are partners: the DAG provides the retry mechanism; idempotency makes retries safe. |
| [[data-quality-validation\|Data Quality & Validation]] | A validation check — "confirm today's extract contains more than 400,000 rows before we load it" — is often one node in the DAG, placed between extract and transform. | Data quality is about *correctness of the data itself*; the DAG is about *sequencing and timing tasks*. The DAG is the frame; a quality check is one specific type of task you slot into it. |

## Why you'd use it (and when not to)

Use a DAG-based scheduler when you have multiple interdependent tasks that must run reliably, on a schedule, with visibility into failures — a nightly pipeline with ten or more steps is the sweet spot. The overhead pays off fast when things break (and they always do). Do *not* reach for Airflow when you have a single, simple script that runs once a day with no dependencies: a plain cron job or a GitHub Actions scheduled workflow is far lighter. Orchestrators add real operational cost — they need their own server, a metadata database to track run state, and ongoing maintenance. Spend that cost only when your pipeline is genuinely complex.

## Check yourself

**Memory hook:** A DAG is a one-way recipe — tasks flow forward, never in circles; the scheduler is the chef who follows it on a timer.

**Q1: Why must a DAG be acyclic?**
A: A cycle means Task A waits for Task B, which waits for Task A — a permanent deadlock. Neither task can ever start, so the rule "no cycles" is what makes scheduling possible in the first place.

**Q2: Task C depends on both Task A and Task B. Task A finishes successfully, but Task B fails. What does the scheduler do with Task C?**
A: It blocks Task C entirely. The scheduler will not start C until all of its upstream dependencies have succeeded. It will retry Task B according to the retry policy, and only proceed to C if B eventually succeeds.

**Q3: What does the cron expression `0 6 * * 1` most likely mean?**
A: Run at 6:00 AM every Monday. In cron notation, the fields are minute, hour, day-of-month, month, day-of-week — and `1` in the last position means Monday.

## Connects to

[[batch-vs-streaming|Batch vs Streaming]] · [[idempotency|Idempotency]] · [[data-quality-validation|Data Quality & Validation]]