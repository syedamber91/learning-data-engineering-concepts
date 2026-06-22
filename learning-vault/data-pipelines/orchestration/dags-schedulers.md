---
title: "DAGs & Schedulers"
area: "Data Pipelines"
topic: "Orchestration"
tags: [dag, airflow, scheduler, dependencies]
---

# DAGs & Schedulers

*Part of [[orchestration-moc|Orchestration]] · [[data-pipelines-moc|Data Pipelines]]*

**In one line:** A DAG is a map of tasks and the order they must run in; a scheduler is the robot that runs them on time and in that order.

**Picture this:** A recipe: you must boil pasta *before* you drain it, and drain it *before* you add sauce. You can't loop back and un-boil. That ordered, no-going-back flow is a DAG — a Directed Acyclic Graph.

**How it actually works:** "Directed" = each task points to the next; "Acyclic" = no loops, so it always ends. Each box is a task ("download data", "clean it", "load to warehouse") and arrows are dependencies. A *scheduler* like Apache Airflow reads the DAG, kicks off tasks when their inputs are ready, runs independent tasks in parallel, and retries the ones that fail — without you watching at 3 a.m.

**In the real world:** Airbnb built Airflow to run thousands of daily DAGs that turn raw bookings into the metrics and dashboards their teams rely on each morning. The scheduler guarantees "clean data" never runs before "raw data arrived".

**Why you'd use it (and when not to):** Use a DAG + scheduler when you have multi-step jobs with dependencies that must run reliably on a schedule. For a single script you run by hand once a month, a full orchestrator is overkill.

**Connects to:** [[data-quality-validation]] · [[batch-vs-streaming]] · [[idempotency]]
