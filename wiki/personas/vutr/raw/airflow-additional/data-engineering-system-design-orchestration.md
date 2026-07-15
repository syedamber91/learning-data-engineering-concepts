---
title: "Data Engineering System Design: Orchestration + Apache Airflow"
channel: vutr
author: "Vu Trinh"
published: 2026-04-14
url: https://vutr.substack.com/p/data-engineering-system-design-orchestration
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Kafka", "Apache Spark", "Data Warehouse", "Orchestration", "Data Quality", "ETL"]
tags: [https, task, auto, airflow, image, fetch]
---

# Data Engineering System Design: Orchestration + Apache Airflow

*Orchestration system design problems and how to solve them with Airflow. Insights and lessons you can apply to your jobs and interviews.*

> Source: [Open post](https://vutr.substack.com/p/data-engineering-system-design-orchestration)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[data-warehouse|Data Warehouse]] · [[orchestration|Orchestration]] · [[data-quality|Data Quality]] · [[etl|ETL]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=193360073)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!BLLQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5dbfb6e6-04e0-42fd-89a9-590f9f01036f_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!BLLQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5dbfb6e6-04e0-42fd-89a9-590f9f01036f_2000x1429.png)

---

# Intro

You might have heard of system design.

It is the process of selecting software components (by evaluating the trade-offs) and gluing them together (in a suitable way) to achieve the desired functionality.

That’s the broad definition for software engineering.

Zoom into the data engineering field.

System design is also about selecting and gluing, but the focus is more on the reliability, trustworthiness, and scalability of the data. You have to choose the right techniques, frameworks, file formats, or storage optimizations for ingesting, storing, and serving data.

An important difference between data engineering and software engineering is that, unlike software, data must be moved through multiple stages, from object storage to different layers of the data warehouse. The journey requires an orchestration layer that … orchestrates the whole movement. It’s not only a cron scheduler or a task execution engine, but also the actor that enables integration between stations, ensures fault tolerance, and provides backfilling capability.

In this article, we take a closer look at one of the most important aspects in data engineering system design: the orchestration. I will discuss a set of orchestration problems. Those are:

* Scheduling
* (Task) Dependency Management
* Branching
* Deal with failures
* Backfilling
* Concurrency & Resource Control
* Resource isolation
* Observability

Then we bring in Airflow, the most used orchestration platform at the moment, to see how Airflow could help us solve those problems. We revisit Airflow first, then discuss each problem and see how Airflow could fit into the picture. The goal of the article is to make you and me aware of orchestration problems and how we can solve them with Airflow, so we can be confident in our daily tasks or system design interviews (for data engineers).

> ***Note 1**: You won’t see any concrete use cases or scenarios, as I try to discuss these problems as “patterns” so you can apply them based on your needs.*
>
> ***Note 2**: Insights I delivered in this article are based on my personal experiences. If you see I miss anything, feel free to provide feedback.*
>
> ***Note 3**: I reference the latest Airflow documentation to demonstrate Airflow’s capability. If you’re using an older version of Airflow, you might find some concepts/features not available.*
>
> ***Note 4**: I assume you have some getting-started experience with Airflow: if you can write a simple DAG with a few tasks, you’re good to go.*

---

# Airflow revisit

Apache Airflow was created in 2014 at **Airbnb**, when the company was dealing with massive, increasingly complex data workflows. At the time, existing orchestration tools were either too rigid or lacked scalability. To address this challenge, **Maxime Beauchemin**, a data engineer at Airbnb, spearheaded the creation of Airflow.

At its core, Airflow operates on the concept of **Directed Acyclic Graphs (DAGs)** to model workflows. It is essentially a roadmap for the workflow and contains two main components:

[![](https://substackcdn.com/image/fetch/$s_!b8-B!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe73baaa6-8c3d-46f0-ae1e-6c60fb3ba21d_708x324.png)](https://substackcdn.com/image/fetch/$s_!b8-B!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe73baaa6-8c3d-46f0-ae1e-6c60fb3ba21d_708x324.png)

* **Tasks (Nodes)** are individual work units, such as running a query, copying data, executing a script, or calling an API.
* **Dependencies (Edges)**: The relationships between tasks that define their execution order (e.g., preprocessing is executed only after retrieving data from a third-party API).

Airflow ensures tasks are executed according to their dependencies, automatically manages retries on failure (based on their retry configuration), and thoroughly logs task execution for monitoring and debugging.

The orchestration platform comprises several components:

[![](https://substackcdn.com/image/fetch/$s_!-xgl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde4b0932-6c5e-4c08-b028-9232cb66c5bb_666x448.png)](https://substackcdn.com/image/fetch/$s_!-xgl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde4b0932-6c5e-4c08-b028-9232cb66c5bb_666x448.png)

* **Scheduler**: The component responsible for parsing DAG files, scheduling tasks, and queuing them for execution based on their dependencies and schedules. The **executor** logic runs inside the scheduler.
* **Web Server** provides the Airflow UI, allowing users to visualize workflows, monitor task execution, inspect logs, and trigger DAG runs.
* **Metadata Database**: A central database that stores all metadata, including DAG definitions, task states, execution logs, and schedules. It’s essential for tracking workflow history.
* **DAG folder**: It contains DAG files defined by users.
* **Workers**: Components that execute the tasks assigned by the executor.

The workflow between Airflow’s components can be broken down into the following steps:

[![](https://substackcdn.com/image/fetch/$s_!8mzK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbbb2afcb-8cfc-4b33-9ac5-80c3bb144a16_1410x976.png)](https://substackcdn.com/image/fetch/$s_!8mzK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbbb2afcb-8cfc-4b33-9ac5-80c3bb144a16_1410x976.png)

1. **DAG definition**: The users define the Python DAG file in the DAG directory.
2. **DAG Parsing**: The Scheduler scans the DAG directory, parses the DAG file, and loads it into the Metadata Database.
3. **Scheduling**: Based on the DAG definitions and schedule intervals, the Scheduler determines which tasks are ready for execution and queues them.
4. **Task Execution**: The Executor fetches the queued tasks and assigns them to available Workers. The Workers execute the tasks, and task states are updated in the Metadata Database.
5. **Monitoring**: The Web Server queries the Metadata Database and visualizes DAG runs, task statuses, and logs in real-time. Users can monitor task progress, inspect logs, or trigger manual DAG runs from the UI.
6. **Retries and State Updates**: If a task fails, the Scheduler ensures retries are handled according to the task’s retry configuration. The Executor updates task states in the database until all tasks are either completed successfully or fail after retry limits are reached.

---

# Orchestration problems

Your orchestration toolkit could be simply a Python script, a cron expression, and a VM at first.

Then someone asked if we could:

* Run a second script after the first one finishes.
* Have another that depended on both.
* Re-execute the runs from last week to apply the bug fixes.
* Retry if tasks failed, but still respect the dependencies between them.
* Have a notification, a log, or a kind of UI to observe the flow.
* Onboard more scripts to deal with more data sources
* Run the flow based on an external event instead of a fixed scheduler.

That’s when you have orchestration problems. I’ve been there more than once. Every time, the same concerns show up: scheduling, retries, dependencies, backfills, resource management, and observability.

In the rest of the article, I will discuss common orchestration problems (based on my personal observations) and explore how Airflow could solve them.

We start with the most obvious one: scheduling.

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=193360073)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

---

> ***Note**: There will be example Airflow code; however, it is only pseudo code.*

---

# Scheduling

[![](https://substackcdn.com/image/fetch/$s_!5Eio!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F56e7af72-0179-44dc-93d7-cee65ed9aa9d_1204x246.png)](https://substackcdn.com/image/fetch/$s_!5Eio!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F56e7af72-0179-44dc-93d7-cee65ed9aa9d_1204x246.png)

## Problems

Scheduling means telling the pipeline when it should run. There are multiple approaches to inform the pipeline:

* Cron scheduling (e.g., daily, every 6 hours): The simple case is time-based. Run the daily revenue report at 6 am. Refresh the user activity table every hour. Cron handles this well enough, and for many pipelines, it’s all you need.

  [![](https://substackcdn.com/image/fetch/$s_!TMSR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ff40644-c6e4-4391-83fe-efe9207defcc_368x338.png)](https://substackcdn.com/image/fetch/$s_!TMSR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ff40644-c6e4-4391-83fe-efe9207defcc_368x338.png)
* Event-driven triggering: However, cron-based scheduling has a problem: it doesn’t actually have any information about the current status of the data. For example, a data source might have data available between 3:00 and 8:00. In such a case, you need the pipeline to run “when something happened “.

  [![](https://substackcdn.com/image/fetch/$s_!9OEH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F23ede535-43b7-4210-ad72-733b0cc0e70c_564x252.png)](https://substackcdn.com/image/fetch/$s_!9OEH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F23ede535-43b7-4210-ad72-733b0cc0e70c_564x252.png)

  That’s when event-driven scheduling comes to the rescue. Based on my observation, there are two types:

  + Actively wait for an event to happen: it could be a file landed in object storage or a dependent table updated.
  + Passively triggered by an event: a table insertion will trigger the pipeline.

## How does Airflow handle it?

### Cron

Airflow allows us to define the cron expression for the DAG; it could be explicitly defined (e.g., "0 6 \* \* \*") or used with preset ones (e.g., “@daily“):

```
@dag(schedule="0 6 * * *")
def dag_1():
   ...

@dag(schedule="@daily")
def dag_2():
    ...
```

That’s straightforward. But that’s not enough for us to work efficiently with Airflow cron-based scheduling. Airflow separates “when a task executes” from “what data interval it owns”. Every task has access to **data\_interval\_start** and **data\_interval\_end**, the window the run is responsible for. You can use these parameters to scope the data window processing. For example:

```
@dag(schedule="0 6 * * *")
def dag_1():
    @task
    def task_1(data_interval_start=None, data_interval_end=None):
        # For a daily DAG running on April 5 at 6:00 am:
        #   data_interval_start = 2026-04-04 06:00:00
        #   data_interval_end   = 2026-04-05 06:00:00
        # The task owns exactly one day of data — re-running gives the same result
        query = f"""
            SELECT * FROM orders
            WHERE created_at >= '{data_interval_start}'
              AND created_at <  '{data_interval_end}'
        """
        return run_query(query)
```

As you can see, the run on April 5 at 6:00 AM will have a data interval from 2026-04-04 06:00:00 to 2026-04-05 06:00:00. Because Airflow was originally designed for ETL, which usually processes batches of historical data, a common assumption is that if you schedule your processing to run every day at 6:00, the 2026-04-04 batch of data will be fully available at 2026-04-05 06:00:00.

[![](https://substackcdn.com/image/fetch/$s_!1HWy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0737f3fe-02ed-4bac-ad02-349f8fabc3a5_1132x486.png)](https://substackcdn.com/image/fetch/$s_!1HWy!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0737f3fe-02ed-4bac-ad02-349f8fabc3a5_1132x486.png)

Historically, Airflow used the “execution\_date” parameter for this purpose. However, it has been deprecated since version 2.2 because it does not provide a clear definition of an “interval”. That’s why **data\_interval\_start** and **data\_interval\_end** are introduced and recommended by Airflow.

### Event-driven

For active waiting, Airflow provides Sensors.

[![](https://substackcdn.com/image/fetch/$s_!SY1F!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa590af0b-8525-4b00-8e3b-0c9f0264387c_1492x504.png)](https://substackcdn.com/image/fetch/$s_!SY1F!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa590af0b-8525-4b00-8e3b-0c9f0264387c_1492x504.png)

A Sensor is a special kind of operator whose only job is to wait for a condition (with a configurable timeout) to be true. For example:

```
# Example A: S3KeySensor — wait for a file to land in S3
@dag(schedule="@daily")
def dag_1():
    wait_for_object = S3KeySensor(
        task_id="...",
        bucket_name="...",
        bucket_key="...",  # {{ ds }} = logical date
        poke_interval=60,        # check every 60 seconds
        timeout=60 * 60 * 6,     # give up after 6 hours
    )

    @task
    def process():
        ...

    wait_for_file >> process()
```

* S3KeySensor waits for a file to appear in S3.
* ExternalTaskSensor waits for a task in another DAG to finish.

Once the condition is met, the sensor is considered a successful task, and downstream tasks run. Under the hood, sensors poll (e.g., periodically list a file in S3 to see if it exists).

A small note: the sensor is simply a task; it still needs to be scheduled using a cron expression.

—

For passive triggering, Airflow has an asset. An asset is a named logical object, a URI like s3://bucket/…, that represents a piece of data.

A task declares that it produces updates to an asset (via the `outlets` parameter), and another DAG declares (via the `schedule` parameter) that it runs when that asset updates.

[![](https://substackcdn.com/image/fetch/$s_!WLcc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e941b8e-ba36-4068-86d3-a72d4a0f32f2_900x700.png)](https://substackcdn.com/image/fetch/$s_!WLcc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e941b8e-ba36-4068-86d3-a72d4a0f32f2_900x700.png)

When the producer task finishes successfully, Airflow marks the asset as updated, and any DAGs that depend on it are automatically triggered.

```
test_asset = Asset("s3://bucket/...")

@dag(schedule="@daily")
def dag_1():
    @task(outlets=[test_asset])  # declares this task updates the Asset
    def task_1():
        write_parquet("s3://bucket/...")

# This DAG runs automatically whenever task_1 updates test_asset.
@dag(schedule=[test_asset])
def dag_2():
    @task
    def task_2():
        ...
```

> ***Note**: only DAGs can be fired based on the asset updated event; you can’t define a task in a DAG that will be triggered based on the updated asset. Although a task can have the* `inlets` *parameter, it only indicates that this task can access information of assets defined in the parameter.*
>
> [![](https://substackcdn.com/image/fetch/$s_!pp1D!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3cf02066-46f0-4dc3-a829-cbaac8ea9236_1572x170.png)](https://substackcdn.com/image/fetch/$s_!pp1D!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3cf02066-46f0-4dc3-a829-cbaac8ea9236_1572x170.png)
>
> [Source: Astronomer’s documentation](https://www.astronomer.io/docs/learn/airflow-datasets)

The `@asset` decorator is a shortcut for **defining a DAG with a single task** that updates an asset.

[![](https://substackcdn.com/image/fetch/$s_!zAUG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc5e0c465-e61f-4bba-bb21-4136f173d138_1196x622.png)](https://substackcdn.com/image/fetch/$s_!zAUG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc5e0c465-e61f-4bba-bb21-4136f173d138_1196x622.png)

You can chain multiple asset-orienter DAGs like this to form a complete pipeline. **Remember, each function that is decorated with** `@asset` **is a DAG, not a task:**

```
from airflow.sdk import asset


@asset(schedule="@daily") # the first dag is scheduled daily
def asset_1():
    ...


@asset(schedule=asset_1) #
def asset_2(context):
    ...


@asset(schedule=asset_2)
def asset_3(context):
    ...
```

Besides defining assets like this, you can define a DAG to be triggered via an external event from message systems such as Kafka:

```
import json

from airflow.providers.common.messaging.triggers.msg_queue import MessageQueueTrigger
from airflow.sdk import dag, Asset, AssetWatcher, task

KAFKA_TOPIC = "kafka://<your_kafka_host>:<port>/<your_topic>"

trigger = MessageQueueTrigger(
    queue=KAFKA_TOPIC,
    ...
)
kafka_topic_asset = Asset(
    "kafka_topic_asset", watchers=[AssetWatcher(name="kafka_watcher", trigger=trigger)]
)

@dag(schedule=[kafka_topic_asset])
def dag_1():
    @task
    def task_1(**context):
        ...
```

Or, you can have more control by triggering the DAG via the API. For example, an AWS Lambda function can run logic that, when invoked, triggers a specific DAG.

[![](https://substackcdn.com/image/fetch/$s_!54DQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa0757cf5-d225-4967-8a24-e815d08cd05c_968x1220.png)](https://substackcdn.com/image/fetch/$s_!54DQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa0757cf5-d225-4967-8a24-e815d08cd05c_968x1220.png)

[Source: Airflow REST API.](https://airflow.apache.org/docs/apache-airflow/3.1.6/stable-rest-api-ref.html#operation/trigger_dag_run)

---

# (Task) Dependency Management

[![](https://substackcdn.com/image/fetch/$s_!-Xfp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ec55182-298b-45b8-bf3d-963cd4b7d8a8_918x318.png)](https://substackcdn.com/image/fetch/$s_!-Xfp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ec55182-298b-45b8-bf3d-963cd4b7d8a8_918x318.png)

## Problems

The production pipeline isn’t linear. It’s a graph. And a graph needs nodes and edges with different patterns, depending on the use case:

* One-to-one: Task X has only task Y as downstream, and task Y has only task X as upstream.
* Fan-out: Task A extracts data. Tasks B and C transform different subsets in parallel
* Fan-in: Task D waits for both B and C to finish before it loads the final result
* Cross-pipeline dependencies: a pipeline waits for a task from a different pipeline to finish.

In real production use cases, additional requirements arise, such as task B consuming the result of task A, task D executing when task B succeeds, and not caring about task C.

---

> *I invite you to join my paid membership to read this article and over 180 other high-quality data engineering articles, with a limited-time **50% discount** on the annual plan:*
>
> [50% ⬇️ annual plan, END ON APRIL 16](https://vutr.substack.com/subscribe?coupon=72ab786c&utm_content=193360073)
>
> *The discount will end **on April 16th—only 2 days left** since the release of this article. Come and grab it!*

---

## How does Airflow handle it?

### Task dependencies

Airflow lets you define the task dependencies inside a DAG using the bit shift operators like “>>” or “<<“.

> ***Note**: There are other methods for declaring dependencies. You can [read here](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html#relationships). In this article, I discuss only bit-shift operators to avoid confusion and inconsistency.*

For example:

[![](https://substackcdn.com/image/fetch/$s_!ug66!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F70bcf0b4-cb62-4781-ac9e-27fe2faa2ccf_944x476.png)](https://substackcdn.com/image/fetch/$s_!ug66!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F70bcf0b4-cb62-4781-ac9e-27fe2faa2ccf_944x476.png)

```
# one-to-one
task_X >> task_Y

# Fan out
task_A >> [task_B, task_C]

# Fan in
[task_B, task_C] >> task_D

# Cross-pipeline dependencies
@task()
def task_Z():
  ...

@task()
def trigger_dag():
    # Trigger DAG 2 (Data Processing)
    trigger = TriggerDagRunOperator(
            task_id='...',
            trigger_dag_id='...',
            conf={...},
            dag=...
        )
    return trigger

task_Z >> trigger_dag
```

### Data exchange between tasks

To exchange data between tasks, you can use Airflow XCom, a mechanism that allows tasks to exchange data within the same DAG run instance.

[![](https://substackcdn.com/image/fetch/$s_!Acri!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F15223b55-ced1-486f-8772-8e0731cde775_860x584.png)](https://substackcdn.com/image/fetch/$s_!Acri!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F15223b55-ced1-486f-8772-8e0731cde775_860x584.png)

To persist data, XCom requires a backend; the default is the Airflow database. For larger datasets, users can set up object storage as the backend.

Here is an example:

```
# Source: https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html

@task(do_xcom_push=True, multiple_outputs=True)
def task_1(**context):
    return {"key1": "value1", "key2": "value2"}


@task
def task_2(**context):
    key1 = context["ti"].xcom_pull(task_ids="task_1", key="key1")  # retrive key 1
    key2 = context["ti"].xcom_pull(task_ids="task_1", key="key2")  # retrive key 2
    data = context["ti"].xcom_pull(task_ids="task_1", key="return_value") # retrive all
```

### Trigger rules

[![](https://substackcdn.com/image/fetch/$s_!NtfV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc7e398ea-82de-4b81-b8bd-22f11f8de43c_1614x324.png)](https://substackcdn.com/image/fetch/$s_!NtfV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc7e398ea-82de-4b81-b8bd-22f11f8de43c_1614x324.png)

To have finer control over how a task would be triggered, Airflow lets you define a trigger rule for a task. For example, a task runs only when all its parents succeed, or it runs when all its parents fail. Here are the full options:

[![](https://substackcdn.com/image/fetch/$s_!e_DS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f3da283-dc7e-434f-8252-dc67796cc90a_1558x972.png)](https://substackcdn.com/image/fetch/$s_!e_DS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f3da283-dc7e-434f-8252-dc67796cc90a_1558x972.png)

[Source](https://www.astronomer.io/docs/learn/airflow-trigger-rules)

The code will look like this:

```
from airflow.sdk import task

@task 
def task_A():
    ...

@task 
def task_B():
    ...

@task(trigger_rule="all_done") # task C is run when both A and B are done, both can be failed or succeed
def task_C():
    ...

[task_A, task_B] >> task_C
```

---

# Branching

[![](https://substackcdn.com/image/fetch/$s_!RM7U!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc0ccd26a-e2c6-42c5-bb3d-73d72e000fc4_692x372.png)](https://substackcdn.com/image/fetch/$s_!RM7U!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc0ccd26a-e2c6-42c5-bb3d-73d72e000fc4_692x372.png)

## Problems

There are cases where you need a pipeline run to take a different path when something happens.

For example, you run a data quality check after extraction, and if it fails, you skip the load and fire an alert instead. The weekday runs are incremental, and weekend runs are full refreshes. Or the applied transformation depends on the trigger configuration.

## How does Airflow handle it?

Airflow has the `BranchPythonOperator` (@task.branch), which lets a task return the `task_id` (based on conditions) of the immediately downstream task that should run. Everything else gets skipped.

[![](https://substackcdn.com/image/fetch/$s_!xXIQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F10d8458f-c519-4148-acae-912a6f7248f1_1276x734.png)](https://substackcdn.com/image/fetch/$s_!xXIQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F10d8458f-c519-4148-acae-912a6f7248f1_1276x734.png)

```
@dag(schedule="@daily")
def etl():
    @task
    def extract():
        ...

    @task.branch
    def check_data_quality():
        null_ratio = get_null_ratio("raw_table")
        if null_ratio > 0.05:
            # the "alert_and_skip" is the task id
            return ["alert_and_skip"]   # skip load, fire alert
        # the "load_to_warehouse" is the task id
        return ["load_to_warehouse"]    # proceed normally

    @task
    def load_to_warehouse():
        ...

    @task
    def alert_and_skip():
        send_slack_alert("Data quality check failed: too many nulls")

    extract >> check_data_quality >> [load_to_warehouse, alert_and_skip]
```

For the simpler yes/no case, `ShortCircuitOperator` (@task.short\_circuit) either continues the pipeline or skips all downstream tasks based on a Boolean.

[![](https://substackcdn.com/image/fetch/$s_!bArj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F63f0b7e9-407b-4113-9a43-e25b84c85f68_1590x412.png)](https://substackcdn.com/image/fetch/$s_!bArj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F63f0b7e9-407b-4113-9a43-e25b84c85f68_1590x412.png)

```
@dag(schedule="@daily")
def etl():
    @task
    def extract():
        ...

    @task.short_circuit
    def has_new_data():
        row_count = run_query("SELECT count(*) FROM ...")
        return row_count > 0   # False → skip all downstreams: transform + load

    @task
    def transform():
        ...

    @task
    def load():
        ...

    extract >> has_new_data >> transform >> load
```

---

# Deal with failures

[![](https://substackcdn.com/image/fetch/$s_!-q5_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F84e78c54-a0e0-40c9-ab9b-ad73956e6724_616x326.png)](https://substackcdn.com/image/fetch/$s_!-q5_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F84e78c54-a0e0-40c9-ab9b-ad73956e6724_616x326.png)

## Problems

Failures are inevitable. The API server is down, or the source database is overloaded. When a task in a pipeline fails, it needs to be (automatically):

* Retried with the right setup (e.g., not to put more pressure on the already overloaded source)
* Terminated to prevent it from running forever.
* Informed the pipeline owner.

## How does Airflow handle it?

You can set **retries (**number of retries**)**, **retry\_delay (**delay between retries**)**, and **retry\_exponential\_backoff** (use backoff retry or not). In addition, you can set an **execution\_timeout** to kill anything that takes longer than expected.

These can be configured at two levels: at the DAG level or as per-task overrides (e.g., when a task needs its own settings). When a task fails, after exhausting retries, Airflow marks all downstream tasks as upstream\_failed and skips them. We can use callbacks, such as **on\_failure\_callback**, to trigger alerts or run cleanup logic.

```
def alert_on_failure(context):
    task_id = context["task_instance"].task_id
    error = context["exception"]
    send_alert(f"Task {task_id} failed: {error}")

# DAG-level defaults: every task in this DAG inherits these unless overridden
default_args = {
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
    "retry_exponential_backoff": True,
    "on_failure_callback": alert_on_failure,
}

@dag(
    schedule="@daily",
    default_args=default_args,
)
def dag_1():
    @task
    def task_1():
        return run_query("SELECT * FROM source")

    @task(  # task-level override
        retries=5,
        retry_delay=timedelta(minutes=2),
        execution_timeout=timedelta(hours=1),
    )
    def task_2():
        ...

    @task  # back to DAG-level defaults
    def load(db_data, api_data):
        ...
```

---

# Backfilling

[![](https://substackcdn.com/image/fetch/$s_!K4t9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F43ba369e-8b76-42f2-a77a-dc367416c50e_896x300.png)](https://substackcdn.com/image/fetch/$s_!K4t9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F43ba369e-8b76-42f2-a77a-dc367416c50e_896x300.png)

## Problems

Your pipeline has been running daily for six months. Then you find out that the transformation logic has had a bug since March, and it’s been quietly producing incorrect aggregates the whole time. You fix the code. But you need to apply the fix logic to the historical batch. You need to reprocess every affected day. That could be 100+ runs, respecting the same dependency graph as a normal run.

## How does Airflow handle it?

Airflow has a built-in `backfill` command that re-runs a DAG over a date range. In case you need to fill up historical data when creating the DAG, the `catchup` parameter controls whether Airflow auto-runs missed intervals when you create a DAG.

```
# catchup=True will fill up the runs from 2026-01-01 (start_date)
@dag(schedule="@daily", start_date=datetime(2026, 1, 1), catchup=True)
def dag_1():
    @task
    def task_1(data_interval_start=None):
        partition = data_interval_start.date()
        query = f"""
            SELEC ... FROM transactions ...
            WHERE dt = '{partition}'
        """
        run_query(query)
```

```
airflow backfill create --dag-id dag_1 \
    --start-date 2026-03-01 \
    --end-date 2026-03-20 \
```

Also, the backfill action can be configured in the UI:

[![](https://substackcdn.com/image/fetch/$s_!dGxE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3492f622-5d79-4436-99d2-0c821e9da329_1442x774.png)](https://substackcdn.com/image/fetch/$s_!dGxE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3492f622-5d79-4436-99d2-0c821e9da329_1442x774.png)

[Source](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/backfill.html)

---

# Concurrency & Resource Control

[![](https://substackcdn.com/image/fetch/$s_!s_Oq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F82c17d37-4e4f-49ee-8627-3b5d08797b6b_854x566.png)](https://substackcdn.com/image/fetch/$s_!s_Oq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F82c17d37-4e4f-49ee-8627-3b5d08797b6b_854x566.png)

## Problems

If a set of ready-to-run tasks (without upstream dependencies or with all upstreams finished) is available, it should be run at the same time (in most cases) to reduce the overall DAG duration.

But how many tasks run at once is fine?

A normal daily run with 10 concurrent tasks is fine. Then you kick off a 90-day backfill. Suddenly, that’s 900 tasks all trying to run at once. The scheduler gets overwhelmed. Workers run out of resources. Your production database, which was configured for 10 concurrent queries, starts throwing connection errors.

Things will slow down or crash.

And concurrency is only half the story. Even with the right number of tasks running, they often share resources. One task hits the prod database (with a limit on concurrent queries). Other tasks call the same API endpoint, which has strict rate limits.

Priority and guardrail are needed.

## How does Airflow handle it?

The knobs exist at several layers. Globally, there are parameters with the format of AIRFLOW\_\_CORE\_\_PARAMETER\_NAME.

* **max\_active\_runs\_per\_dag**: The maximum number of active runs of a DAG at a time. A **[DAG run](https://airflow.apache.org/docs/apache-airflow/stable/dag-run.html)** is an instance of a DAG over time. For example, a run at 2026-04-01 and a run at 2026-04-02 of a given DAG are the two DAG runs. You need to consider this parameter when running backfill operations.

  [![](https://substackcdn.com/image/fetch/$s_!dGMD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe70b8722-98c7-409c-bae2-d35d04398ac2_1318x522.png)](https://substackcdn.com/image/fetch/$s_!dGMD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe70b8722-98c7-409c-bae2-d35d04398ac2_1318x522.png)

* **max\_active\_tasks\_per\_dag:** The maximum number of task instances that can be run in **a DAG run.** This prevents a single DAG from occupying all scheduled slots.

  [![](https://substackcdn.com/image/fetch/$s_!_2JE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee0d8c82-9ea7-4e26-9d01-b4d2b9266aab_1394x552.png)](https://substackcdn.com/image/fetch/$s_!_2JE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee0d8c82-9ea7-4e26-9d01-b4d2b9266aab_1394x552.png)
* **parallelism**: The maximum number of task instances that can run concurrently on a scheduler **across all DAGs** in a single Airflow environment (which could have more than one scheduler). If this parameter is 20 and there are 3 schedulers, the maximum number of task instances that can run concurrently across all DAGs is 60. This is the global cap applied to all DAGs.

  [![](https://substackcdn.com/image/fetch/$s_!KGiq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0d5bec79-9521-4c4a-bed0-f2836bee1487_1610x620.png)](https://substackcdn.com/image/fetch/$s_!KGiq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0d5bec79-9521-4c4a-bed0-f2836bee1487_1610x620.png)

For the DAG level, you can set:

* **max\_active\_runs**: If set, this will overwrite the global setting **max\_active\_runs\_per\_dag**.
* **max\_active\_tasks**: If set, this will overwrite the global setting **max\_active\_tasks\_per\_dag**.

For the task level, you can set:

* **max\_active\_tis\_per\_dag**: controls the number of concurrent running task instances across DAG runs per task.
* **pool**: named ***logical buckets*** with a fixed number of slots. You assign a task to a pool, and Airflow guarantees that the total number of running tasks in that pool never exceeds the limit. For example, if you have a `production_db` pool with 5 slots and 10 tasks configured for it, there will never be more than 5 active tasks at a time.

  [![](https://substackcdn.com/image/fetch/$s_!WHKi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd0418f24-28bc-489d-8b21-78f156b6f9a7_940x674.png)](https://substackcdn.com/image/fetch/$s_!WHKi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd0418f24-28bc-489d-8b21-78f156b6f9a7_940x674.png)
* **priority\_weight**: Pools tell Airflow how many tasks can run. They don’t tell Airflow which tasks should run first when there’s a queue. That’s what priority\_weight is for. When the pool fills up, and tasks are waiting, Airflow looks at each waiting task’s effective priority and picks the highest. The higher number wins. The default is 1.

  [![](https://substackcdn.com/image/fetch/$s_!3x4_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F000bc1b7-9bc6-4e09-afac-6b2dbd39133b_1226x632.png)](https://substackcdn.com/image/fetch/$s_!3x4_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F000bc1b7-9bc6-4e09-afac-6b2dbd39133b_1226x632.png)

More on pool and priority\_weight.

There’s a small but useful detail: a task can take more than one schedule slot. The pool\_slots parameter (default 1) allows you to say “this task is heavy, it consumes 2 slots.”

[![](https://substackcdn.com/image/fetch/$s_!jndm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5c5e1de5-c06f-448c-b517-9e80734fd1e8_858x442.png)](https://substackcdn.com/image/fetch/$s_!jndm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5c5e1de5-c06f-448c-b517-9e80734fd1e8_858x442.png)

So if you have a 5-slot pool and a heavy task takes 2 slots, only 3 light tasks (with pool\_slots is 1 by default) can run. This is useful when tasks in the same pool aren’t equally resource-intensive.

Regarding **priority\_weight**, the priority\_weight you set on a task isn't always the value Airflow uses for the decision. There's a **weight\_rule** that decides how the weight is calculated:

* **downstream (default)**: A task’s effective weight is its own weight plus the weights of every task downstream of it. The result: tasks early in the DAG get scheduled aggressively, because they unblock everything that comes after. Use this when you want runs to make forward progress as fast as possible.

  [![](https://substackcdn.com/image/fetch/$s_!dOM2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F99afc834-5793-4ba9-8c60-8c68389b3f90_1320x342.png)](https://substackcdn.com/image/fetch/$s_!dOM2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F99afc834-5793-4ba9-8c60-8c68389b3f90_1320x342.png)
* **upstream**: The opposite. A task’s effective weight is its own weight plus the weights of every task upstream of it. Tasks late in the DAG get prioritized. Use this when you have many DAG runs queued up, and you’d rather finish the runs you’ve already started than start new ones.

  [![](https://substackcdn.com/image/fetch/$s_!xbnk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F47784e89-044f-4194-bda7-7b96e411cc4c_1890x486.png)](https://substackcdn.com/image/fetch/$s_!xbnk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F47784e89-044f-4194-bda7-7b96e411cc4c_1890x486.png)
* **absolute**: The number (**priority\_weight**) you set is the number used. No graph traversal, no aggregation like the two previous rules. Use this when you know exactly which tasks matter and want full control.

  [![](https://substackcdn.com/image/fetch/$s_!U7G7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fca02ebf3-b43f-4274-a982-1d385032ebbe_352x324.png)](https://substackcdn.com/image/fetch/$s_!U7G7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fca02ebf3-b43f-4274-a982-1d385032ebbe_352x324.png)

Here is an example of setting these configurations:

```
# Global settings via environment variables
# AIRFLOW__CORE__PARALLELISM=30                    # max 30 tasks running across entire Airflow
# AIRFLOW__CORE__MAX_ACTIVE_RUNS_PER_DAG=4         # max 4 concurrent runs of the same DAG


# Create pools via CLI or UI

# airflow pools set production_db 5 "Limit concurrent queries to prod DB."
# airflow pools set vendor_api   3 "Respect API rate limit of 3 req/s."

@dag(
    schedule="@daily",
    max_active_runs=2,         # only 2 DAG runs at a time
    max_active_tasks=8,        # max 8 tasks running within this DAG
)
def dag_1():

    @task(
        pool="production_db",
        priority_weight=10, 
    )
    def extract_critical():
        ...

    @task(pool="production_db")
    def extract_normal():
        ...

    # Heavy task — takes 2 slots in the vendor_api pool instead of 1
    @task(
        pool="vendor_api",
        pool_slots=2,          # counts as 2 of the 3 available slots
        priority_weight=5,
    )
    def fetch_large():
        ...

    # Light task — takes the remaining slot
    @task(pool="vendor_api")
    def fetch_small():
        ...


    # What this gives you:
    # - prod DB never gets more than 5 concurrent queries
    # - vendor API never gets more than 3 concurrent calls
    # - when prod DB is full, extract_critical_table jumps the queue (weight=10)
    # - fetch_large blocks 2 slots, so only 1 small task can join it
```

---

# Resource isolation

[![](https://substackcdn.com/image/fetch/$s_!OuMN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fef90e2cf-343f-4cc5-9ed9-6b7b250cb42f_1054x436.png)](https://substackcdn.com/image/fetch/$s_!OuMN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fef90e2cf-343f-4cc5-9ed9-6b7b250cb42f_1054x436.png)

## Problems

Airflow tasks are not the same.

One task runs a quick SQL query that finishes in 10 seconds.

Another loads a 50GB Parquet file into memory and trains a model.

A third needs Python 3.11 and the latest version of Pydantic, while a fourth was written two years ago and is locked to an older Pydantic version.

If all of these tasks run in the same Python process on the same worker, you get two kinds of pain:

* **Resource contention.** The 50GB load will take all the RAM. One greedy task drags affect all other tasks.
* **Dependency hell.** You can’t have two versions of the same library installed in one Python environment. When you upgrade P`ydantic` for the new task, the old one breaks.

Both of these are isolation problems. We need a way to say “this task runs *here*, with *these* libraries, on *that* *hardware profile.*”

## How does Airflow handle it?

To understand how Airflow helps us solve the isolation problem, first, let’s understand what an executor is.

Executors are responsible for determining where and how tasks are executed. Different executors offer varying levels of scalability, isolation, and complexity:

* **LocalExecutor**: runs tasks as subprocesses on the scheduler machine. No isolation. It works well for small deployments and local development, but it doesn't support separation.

  [![](https://substackcdn.com/image/fetch/$s_!EW0O!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F10e3bc81-d35d-4b98-a98c-ee488dc6ea21_712x542.png)](https://substackcdn.com/image/fetch/$s_!EW0O!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F10e3bc81-d35d-4b98-a98c-ee488dc6ea21_712x542.png)
* **CeleryExecutor**: This executor allows us to enter distributed systems and horizontal scaling. It relies on [Celery, a robust distributed task queue](https://docs.celeryq.dev/en/latest/getting-started/introduction.html). Compared to the LocalExecutor, the workers who run the task are separate from the scheduler machines. The CeleryExecutor setup involves a message broker (most commonly RabbitMQ or Redis) and Celery workers.

  [![](https://substackcdn.com/image/fetch/$s_!xId_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F27d1617d-0e8d-4ff1-9452-71a8a9ade295_1140x890.png)](https://substackcdn.com/image/fetch/$s_!xId_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F27d1617d-0e8d-4ff1-9452-71a8a9ade295_1140x890.png)

  + Celery workers are typically long-running processes that continuously run to pick up tasks, allowing more than one task to run concurrently on a worker. **This means all tasks on a given worker share the same Python environment.** To scale the task-running capability, we add more machines that run Celery worker processes.
  + You can set up multiple worker groups (called "queues") and route tasks to specific groups using a task parameter called **queue**. For example, heavy tasks go to high-memory workers, light tasks go to regular workers.
* **KubernetesExecutor:** This executor is designed for cloud-native and containerized environments. It dynamically creates Kubernetes pods for each task. This one provides the best resource isolation, scalability, and fault tolerance.

  [![](https://substackcdn.com/image/fetch/$s_!cvm-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2a84dc0b-25e6-4897-89b6-d4b2eccc0974_1260x656.png)](https://substackcdn.com/image/fetch/$s_!cvm-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2a84dc0b-25e6-4897-89b6-d4b2eccc0974_1260x656.png)

  + When the Airflow scheduler senses that a task is ready for execution, it requests a new pod from the Kubernetes API. This newly created pod then executes the task, reports its result to the Airflow metadata database, and terminates upon task completion (users can choose to persist the pod for later debugging).
  + The pod could have its own dependencies (each will have its own Docker image) and resource profile (each could freely ask for resources from k8s, as long as the k8s cluster still has resources available)
  + The trade-off is the cold start: The k8s pod needs to be initiated (e.g., pull the Docker image, health check) to run the task; it could take a while compared to the above executors before executing your tasks. It also requires strong knowledge of containerization and Kubernetes.

Even on a Celery worker with one shared Python environment, Airflow gives you ways to isolate individual tasks:

* **PythonVirtualenvOperator**: Airflow creates a fresh virtualenv just for this task, installs the requirements you specify, runs the task code, then cleans up the virtualenv.
* **DockerOperator**: Airflow will run the task inside a Docker container with whatever image you provide. You manage the dependencies via the image.
* **KubernetesPodOperator**: Even if you’re not using **KubernetesExecutor**, this operator lets individual tasks spin up their own pod for execution (in the pre-configurated k8s cluster). Useful when most of your DAGs are fine on Celery, but a few specific tasks need full isolation.

Here is an example:

```
# Example 1: Routing to different worker groups via Celery queues

@dag(schedule="@daily")
def mixed_workload():
    @task(queue="default")           # regular workers
    def quick_sql_check():
        ...

    @task(queue="high_memory")       # routed to a high-RAM workers
    def load_large_parquet():
        ...

    @task(queue="gpu")               # routed to a GPU workers
    def train_model(data):
        ...

    quick_sql_check()
    train_model(load_large_parquet())


# Example 2: Per-task Python dependency isolation with @task.virtualenv

@dag(schedule="@daily")
def legacy_report():
    @task.virtualenv(
        requirements=[...],
        ...
    )
    def run_legacy_report():
        ...


# Example 3: KubernetesPodOperator — full container isolation per task

@dag(schedule="@daily")
def ml_pipeline():
    train = KubernetesPodOperator(
        task_id="...",
        name="...",
        image="...",
        cmds=["python", "/app/train.py"],
        container_resources={ # resource request to the k8s cluster
            "request_memory": "16Gi",
            "request_cpu": "4",
            "limit_memory": "32Gi",
            "limit_gpu": "1",
        },
    )
```

---

# Observability

[![](https://substackcdn.com/image/fetch/$s_!FjM7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6d882df1-6256-48f4-818f-adf7bd277761_1702x746.png)](https://substackcdn.com/image/fetch/$s_!FjM7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6d882df1-6256-48f4-818f-adf7bd277761_1702x746.png)

## Problems

Once you have hundreds of DAGs and thousands of tasks, the questions show up.

Which tasks are running right now? Which ones failed last night? Why did they fail? Is this DAG getting slower compared to last week? Did we miss the SLA? Who triggered this manual run, and with what parameters? How does the relationship of the 50 tasks in this DAG look?

## How does Airflow handle it?

Airflow ships with a web UI.

[![Graph View showing Dag structure with no Dag run selected (Light Mode)](https://substackcdn.com/image/fetch/$s_!04ed!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F00056a8d-ae03-4b03-a3f3-b8b22b29ac81_2562x1284.png "Graph View showing Dag structure with no Dag run selected (Light Mode)")](https://substackcdn.com/image/fetch/$s_!04ed!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F00056a8d-ae03-4b03-a3f3-b8b22b29ac81_2562x1284.png)

DAG’s lineage. [Source](https://airflow.apache.org/docs/apache-airflow/stable/ui.html)

[![Dag Runs Tab (Light Mode)](https://substackcdn.com/image/fetch/$s_!d0IW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9a2c48c1-96eb-4258-952a-6dbd1ff85d36_2700x1312.png "Dag Runs Tab (Light Mode)")](https://substackcdn.com/image/fetch/$s_!d0IW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9a2c48c1-96eb-4258-952a-6dbd1ff85d36_2700x1312.png)

DAG’s status. [Source](https://airflow.apache.org/docs/apache-airflow/stable/ui.html)

[![Dag Code Tab (Light Mode)](https://substackcdn.com/image/fetch/$s_!Novq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19ed9748-65d7-4c16-bd4b-ad5d808468cf_2586x1308.png "Dag Code Tab (Light Mode)")](https://substackcdn.com/image/fetch/$s_!Novq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19ed9748-65d7-4c16-bd4b-ad5d808468cf_2586x1308.png)

Task’s Code. [Source](https://airflow.apache.org/docs/apache-airflow/stable/ui.html)

[![Task Logs (light mode)](https://substackcdn.com/image/fetch/$s_!WTPN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6d28a389-fd01-498c-ad63-385c7ff6329d_2700x1312.png "Task Logs (light mode)")](https://substackcdn.com/image/fetch/$s_!WTPN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6d28a389-fd01-498c-ad63-385c7ff6329d_2700x1312.png)

Task’s Log. [Source](https://airflow.apache.org/docs/apache-airflow/stable/ui.html)

You get real-time DAG status, lineage, task durations, logs, and run history in one place. Task logs are accessible straight from the UI; there's no need to SSH into worker machines. Deadline misses or task failure callbacks.

Here is an example of how you set the deadline misses notification:

```
from datetime import timedelta
from airflow import DAG
from airflow.sdk.definitions.deadline import AsyncCallback, DeadlineAlert, DeadlineReference
from airflow.providers.slack.notifications.slack_webhook import SlackWebhookNotifier

with DAG(
    dag_id="monitored_pipeline",
    schedule="@daily",
    # Fire a Slack alert if the DAG hasn't finished within 2 hours of being queued
    deadline=DeadlineAlert(
        reference=DeadlineReference.DAGRUN_QUEUED_AT,
        interval=timedelta(hours=2),
        callback=AsyncCallback(
            SlackWebhookNotifier,
            kwargs={
                "text": "DAG {{ dag_run.dag_id }} missed deadline at {{ deadline.deadline_time }}"
            },
        ),
    ),
):
    @task
    def task_1():
        ...

    @task
    def task_2(data):
        ...
```

---

# Outro

In this article, we first revisit the Apache Airflow architecture and concepts. Then we move on to discuss the 8 orchestration problems, including:

* Scheduling
* (Task) Dependency Management
* Branching
* Deal with failures
* Backfilling
* Concurrency & Resource Control
* Resource isolation
* Observability

In each section, in addition to the problems, we explore how Apache Airflow could solve them.

Thank you for reading this far.

See you in my next articles.

---

# References

*[1] [Apache Airflow Official Documentation](https://airflow.apache.org/docs/apache-airflow/stable/index.html)*

*[2] [Astronomer Official Documentation](https://www.astronomer.io/docs/learn/overview)*
