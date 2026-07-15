---
title: "How did Discord evolve to handle trillions of data points"
channel: vutr
author: "Vu Trinh"
published: 2024-08-20
url: https://vutr.substack.com/p/how-did-discord-evolve-to-handle
paid: false
topics: ["dbt", "Apache Airflow", "Apache Kafka", "Apache Spark", "Apache Flink", "BigQuery", "Data Warehouse", "Orchestration", "Data Governance"]
tags: [https, auto, discord, image, dagster, substackcdn]
---

# How did Discord evolve to handle trillions of data points

*From in-house solutions to the modern data stack*

> Source: [Open post](https://vutr.substack.com/p/how-did-discord-evolve-to-handle)

## Topics

[[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-flink|Apache Flink]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]] · [[orchestration|Orchestration]] · [[data-governance|Data Governance]]

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=147548381)

[![](https://substackcdn.com/image/fetch/$s_!mnAO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd38223c-dc23-4968-9aaa-3589c5629583_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!mnAO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd38223c-dc23-4968-9aaa-3589c5629583_2000x1429.png)

Image created by the author.

---

## Intro

The series on how big companies handle data analytics will continue with Discord, a chat app used by tens of millions.

Unlike companies like Uber, LinkedIn, or Twitter, which rely on open-source projects like Kafka, Flink, and Spark alongside cloud services, Discord initially deployed in-house orchestration solutions to manage their analytics workload.

However, as their needs grew more complex, the limitations of their initial setup led them to rebuild their data orchestration infrastructure using modern, open-source tools.

---

## Derived - The in-house solution.

In a 2021 article, Discord introduced its internal solution, Derived, which helped it transform petabytes of raw data into the BigQuery data warehouse.

Their main requirement for this system is to maintain a complex Directed Acyclic Graph (DAG) of precomputed data.

[![](https://substackcdn.com/image/fetch/$s_!QySj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F69426f88-6bf9-4af4-962a-4acdff9c7db2_573x472.png)](https://substackcdn.com/image/fetch/$s_!QySj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F69426f88-6bf9-4af4-962a-4acdff9c7db2_573x472.png)

Discord’s DAG. Image created by the author.

Data flows from raw to cleaned tables, undergoing multiple transformation steps that may reference several tables.

At Discord, a derived table represents a data transformation using predecessor tables in the DAG as input. Essentially, it is an SQL SELECT statement referencing raw data or other derived tables.

They want to build a solution that satisfies the following criteria:

* Users only need to know SQL to define derived table (transformation logic)
* The system will infer the DAG from the SQL; thus, users do not need to consider the DAG structure.
* Using Git for production configuration.
* Seamless integration with their existing privatization systems and data governance policies.
* The system must expose accessible metadata to build monitoring, lineage, and performance tooling.
* Data backfilling must not be complex.

Taking into account those requirements, they build the ***Derived*** system with the following technical highlights:

[![](https://substackcdn.com/image/fetch/$s_!iqtE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F85b9655c-2add-4dc6-be40-1ffa35a0051b_800x597.png)](https://substackcdn.com/image/fetch/$s_!iqtE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F85b9655c-2add-4dc6-be40-1ffa35a0051b_800x597.png)

Discord’s Derived. Image created by the author.

* Users use the YAML file to define the derived table's configuration. Within the YAML file, users can specify the SQL logic and settings like refresh frequency, schema, description, data update strategy, update schedule, date range, and BigQuery optimizations, including cluster columns or partition schemes.

[![](https://substackcdn.com/image/fetch/$s_!ABir!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0d2e8788-a00e-4fe6-bd5d-cc38a1c29911_1024x1402.png)](https://substackcdn.com/image/fetch/$s_!ABir!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0d2e8788-a00e-4fe6-bd5d-cc38a1c29911_1024x1402.png)

Example Derived Configuration in YAML. [Reference](https://discord.com/blog/how-discord-creates-insights-from-trillions-of-data-points)

* Users can use the CLI to load table configurations and validate dependencies across the entire DAG for development.
* Discord leveraged Ariflow for job scheduling, visualization, and monitoring.
* The CLI also lets users create test versions of tables using shadow production data.
* Once a pull request is made, CI deploys all new tables to a shadow production environment (a mimic of the production environment), allowing users to validate their changes with real data before merging to the production branch.
* Each transformation run will be deployed separately as a Kubernetes Pod.

[![](https://substackcdn.com/image/fetch/$s_!CxgW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa27536ec-e7be-4925-9fc2-b50c4a801531_899x498.png)](https://substackcdn.com/image/fetch/$s_!CxgW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa27536ec-e7be-4925-9fc2-b50c4a801531_899x498.png)

Image created by the author.

* They store table metadata in a dedicated log store, accessible via BigQuery, which enables data observability. Discord can integrate this metadata with BigQuery's information schema for detailed insights like byte processing and slot usage.

The Derived system served Discord well in the early days. Still, over time, they realized that this in-house solution was limited in offering usability and flexibility in more complex use cases. The next iteration is needed.

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=147548381)

---

## **New solution with Dagster and dbt**

For the transformation layer, between solutions like Coalesce or SQLMesh, Discord chooses to go with dbt, thanks to its rich features and functionality.

The orchestration is more of a headache than that when there are plenty of available solutions from the open-source community: Airflow, Argo, Prefect, Kestra, and Mage.

After thorough research and consideration, they chose Dagster. Here are the key reasons behind Discord's decision:

* Declarative automation: Orchestration like Ariflow requires specifying the imperative workflow, which contains a sequence of tasks that run on a pre-defined schedule (at 3:00 PM or every 6 hours). Dagster offers a different approach, allowing users to specify how up-to-date they expect each data asset to be. Dagster will take care of the scheduling to ensure data arrives on time.

  [![](https://substackcdn.com/image/fetch/$s_!fIEK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F92f3c986-34a9-4318-b127-64e3c519abdd_771x382.png)](https://substackcdn.com/image/fetch/$s_!fIEK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F92f3c986-34a9-4318-b127-64e3c519abdd_771x382.png)

  Image created by the author.
* Dagster has a modern UI that provides self-service observability for data engineers and data scientists.

[![](https://substackcdn.com/image/fetch/$s_!pbNd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd4b17227-e3fa-4a6f-9a39-31d123043e91_1348x680.png)](https://substackcdn.com/image/fetch/$s_!pbNd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd4b17227-e3fa-4a6f-9a39-31d123043e91_1348x680.png)

Dagster Asset Observeration UI. [Source](https://docs.dagster.io/concepts/assets/asset-observations)

* It is easy to run Dagster locally.
* Dagster supports out-of-the-box deployment and execution on [Kubernetes](https://docs.dagster.io/_apidocs/libraries/dagster-k8s).
* Dagster supports the seamless migration of Airflow jobs.

Next, we’ll take a glimpse of how Discord data engineer operates their new data infrastructure with Dagster and dbt:

[![](https://substackcdn.com/image/fetch/$s_!UCpe!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe165ab78-43e2-40e9-b665-743b071466e1_799x601.png)](https://substackcdn.com/image/fetch/$s_!UCpe!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe165ab78-43e2-40e9-b665-743b071466e1_799x601.png)

Discord's next data infrastructure iteration. Image created by the author.

* As mentioned, every Derived data transformation runs as an independent Kubernetes pod. Thanks to the support of operating efficiently in Kubernetes of Dagster, their engineer can get things up and running quickly.
* They integrated dbt with Dagster using [software-defined assets](https://docs.dagster.io/concepts/assets/software-defined-assets). A few words from Dagster about this feature:

> *An **asset** is an object in persistent storage, such as a table, file, or persisted machine learning model. Asset definitions enable a declarative approach to data management, in which code is the source of truth on what data assets should exist and how those assets are computed.* — [Source](https://docs.dagster.io/concepts/assets/software-defined-assets) —

* Instead of defining the transformation logic using YAML, they switch to dbt.
* They schedule their entire DAG using Dagster's declarative automation method, triggered by scheduled runs monitoring our raw data layer.
* To address a race condition in dbt incremental updates, where multiple runs would conflict by trying to delete the same temporary table, they modified dbt's logic for storing temporary data. This allowed for parallel execution of various partitions of the same asset.

> *Based on my experience with dbt, when using the dbt incremental model, it creates a temporary table named in the format* `destination_table__dbt_tmp`*. This temp table is used to update the destination table incrementally, and dbt deletes it after the update is complete. However, if multiple incremental models are executed for the same table, temp tables with different data ranges are created with the same* `__dbt_tmp` *name. This can lead to conflicts when dbt tries to use or delete a temp table from a different run. I guess Discord will adjust dbt to include the specific data range in the temp table name, distinguishing each run from the others.*

* Discord also creates customized dbt CLI commands to boost developer productivity.
* They also implemented a robust CI/CD process to prevent disruptive changes across table logic, dbt macros, and dbt tests.
* Discord engineers leverage various dbt packages to onboard new features and functionality faster than YAML.

## **Outro**

In this article, we learned some valuable lessons from Discord's data orchestration evolution journey. The initial Derived solution served them well in the first place, but Derived showed some limitations when there were requirements for more flexibility and usability. They decided to rebuild their data infrastructure with dagster and dbt to continue providing seamless data analytics.

---

## **References**

*[1] Daniel Meas, [How Discord Creates Insights From Trillions Of Data Points](https://discord.com/blog/how-discord-creates-insights-from-trillions-of-data-points) (2021)*

*[2] Zach Bluhm, [How Discord Uses Open-Source Tools for Scalable Data Orchestration & Transformation](https://discord.com/blog/how-discord-uses-open-source-tools-for-scalable-data-orchestration-transformation) (2024)*

---

## Before you leave

If you want to discuss this further, please leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/), [Email](http://vutrinh2704@gmail.com), or [Twitter](https://x.com/_vutrinh).

[Leave a comment](https://vutr.substack.com/p/how-did-discord-evolve-to-handle/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
