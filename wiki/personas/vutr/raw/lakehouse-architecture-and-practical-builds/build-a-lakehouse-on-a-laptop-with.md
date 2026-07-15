---
title: "Build a lakehouse on a laptop with dbt, Airflow, Trino, Iceberg, and MinIO"
channel: vutr
author: "Vu Trinh"
published: 2025-09-11
url: https://vutr.substack.com/p/build-a-lakehouse-on-a-laptop-with
paid: false
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Apache Iceberg", "Snowflake", "BigQuery", "Data Warehouse", "Data Lake", "Lakehouse", "Orchestration", "Data Governance"]
tags: [https, auto, image, substackcdn, fetch, good]
---

# Build a lakehouse on a laptop with dbt, Airflow, Trino, Iceberg, and MinIO

*A pet project for learning data engineering*

> Source: [Open post](https://vutr.substack.com/p/build-a-lakehouse-on-a-laptop-with)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[snowflake|Snowflake]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]] · [[data-lake|Data Lake]] · [[lakehouse|Lakehouse]] · [[orchestration|Orchestration]] · [[data-governance|Data Governance]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=172333626)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!y8QO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04941682-3bd8-4479-9b8d-52cbc092995a_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!y8QO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04941682-3bd8-4479-9b8d-52cbc092995a_2000x1428.png)

---

## Intro

I’m seeing the combination of using dbt, Airflow, and a cloud data warehouse frequently when companies want to build a comprehensive data system. This is easier to understand as these stacks provide simplicity, less management overhead, and are robust enough for most cases.

I’ve been thinking about building that system on my laptop for a long time, but I procrastinate for no reason. On the occasion of the long holiday at the beginning of September (Vietnam National Day, September 2nd), I finally sat down and did this project.

This article shares my experience in building a local data system using dbt, Airflow, Trino, Iceberg, and MinIO. All the code is available in this repo: <https://github.com/vutrinh274/local_lakehouse>

> ***Note 1:** This system is intended for learning purposes only and is not yet ready for production use.*
>
> ***Note 2:** The final setup will have a total of twelve running containers, as the Airflow environment setup will need seven containers. Make sure you won’t overwhelm your laptop here.*

## What are we gonna to build?

We will set up a lake house with [MinIO](https://www.min.io/) as the backend storage, [Iceberg](https://iceberg.apache.org/) as the table format, [Project Nessie](https://projectnessie.org/) as the catalog for Iceberg, [Trino](https://trino.io/) as the query engine, [dbt](https://www.getdbt.com/) as the abstraction for SQL transformation, and finally, [Airflow](https://airflow.apache.org/) to glue everything together.

For the sample data, we will use five input tables from the AdventureWorks sample dataset: product, product\_category, product\_subcategory, sale, and territories.

[![](https://substackcdn.com/image/fetch/$s_!B7vq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2b19f655-0c21-4e32-9134-e6b48fafa01c_986x624.png)](https://substackcdn.com/image/fetch/$s_!B7vq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2b19f655-0c21-4e32-9134-e6b48fafa01c_986x624.png)

> *[AdventureWorks](https://dataedo.com/samples/html/AdventureWorks/doc/AdventureWorks_2/home.html) database supports standard online transaction processing scenarios for a fictitious bicycle manufacturer - **Adventure Works Cycles**.*

My ultimate goal is to create a data system that mimics a production-ready system as closely as possible. That would take a lot of time and effort, so I decided to break it down into small projects. This one will set up the baseline as I will try to get the required tools up and running. Features like data governance or CI/CD will be introduced in future articles.

The entire stack will be set up using Docker Compose; you can run it along the way by [cloning this repository](https://github.com/vutrinh274/local_lakehouse) and starting it with the commands:

```
./manage-lakehouse.sh start
```

Make sure you make this script executable:

```
chmod +x manage-lakehouse.sh
```

To save this article from being too long, I won’t dive deep into each tool, but if you want to learn more about them, I wrote some articles here:

In each of the following sections, I will examine the system's sub-components in detail. Let’s start with the data lake.

## The data lake

> *This component is managed in the file `docker-compose-lake.yaml`. You can choose to run only the lake setup by running `docker compose -f docker-compose-lake.yaml up -d`*

### MinIO

In a typical lakehouse setup, data will be stored in cloud object storage. For this project, I will utilize MinIO, an open-source, distributed object storage system that uses local disks with an S3-compatible API. It is worth noting that, despite its compatibility, MinIO is not equivalent to cloud object storage. For production usage or benchmarking the self-built lakehouse performance for PoC, I will always recommend an object storage service from a cloud vendor.

To start the MinIO server, I will use its official image `minio/minio`:

[![](https://substackcdn.com/image/fetch/$s_!YUg9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F991a983a-71a9-4b24-b9af-2b555f92040e_940x778.png)](https://substackcdn.com/image/fetch/$s_!YUg9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F991a983a-71a9-4b24-b9af-2b555f92040e_940x778.png)

* The MinIO container is exposed with two ports: 9000 and 9001. The first will be used to serve the S3 API, and the latter will be used for the web console.
* The container has some environment variables. Other services will use this information to talk to the MinIO server.

  > ***Note:** Storing credentials like passwords directly in the Docker Compose file, as shown here, is a (very) bad practice in production.*
* At the time the container started, shell script commands are run to initiate the MinIO client and create the bucket `local-lakehouse`. This bucket is used to store all the lakehouse data in this project.

After starting the MinIO server, visit localhost:9001 and log in using the username and password specified in the Docker Compose file, which are `admin` and `password`, respectively. After logging in, you will see the `local-lakehouse` bucket created there:

[![](https://substackcdn.com/image/fetch/$s_!o0kD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F142b6ce7-c407-4d6d-baab-63a3d940037c_572x110.png)](https://substackcdn.com/image/fetch/$s_!o0kD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F142b6ce7-c407-4d6d-baab-63a3d940037c_572x110.png)

### Project Nessie

[![](https://substackcdn.com/image/fetch/$s_!oPlF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a165ee3-8d07-4b80-880c-ab73692e3472_552x194.png)](https://substackcdn.com/image/fetch/$s_!oPlF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a165ee3-8d07-4b80-880c-ab73692e3472_552x194.png)

For the Iceberg catalog, I chose Nessie. The reason is simple: I found that Nessie is the most mature catalog available on the market. The git-like feature from Nessie also excites me. To start Nessie, I will use its official image and expose the port 19120:

---

[![](https://substackcdn.com/image/fetch/$s_!qxOG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8e454003-6e06-4aa7-86a5-1bc510cc8184_600x200.png)](https://substackcdn.com/image/fetch/$s_!qxOG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8e454003-6e06-4aa7-86a5-1bc510cc8184_600x200.png)

**This article is sponsored by Astronomer.** If you run dbt and Airflow, read this before your next deployment. Cosmos is the OSS bridge between them. With 20M+ monthly downloads, data teams everywhere are turning dbt projects into Airflow DAGs for controllability, observability, and scale. **[Join Astronomer’s webinar on September 25 to learn:](https://www.astronomer.io/events/webinars/the-best-way-to-orchestrate-your-dbt-workflows-with-airflow-video/?utm_source=vu-trinh&utm_medium=paidmedia&utm_campaign=webinar-dbt-with-airflow-9-25)**

* How Airflow orchestration unlocks control and visibility for your dbt models
* How Cosmos runs dbt Core or dbt Cloud/Fusion as DAGs and Task Groups with just a few lines of code
* Best practices and performance tuning for Cosmos at scale

[Register Now](https://www.astronomer.io/events/webinars/the-best-way-to-orchestrate-your-dbt-workflows-with-airflow-video/?utm_source=vu-trinh&utm_medium=paidmedia&utm_campaign=webinar-dbt-with-airflow-9-25)

---

## The Trino

> *This component is managed in the file `docker-compose-trino.yaml`. You can choose to run only the Trino setup by running `docker compose -f docker-compose-trino.yaml up -d`*

### Trino cluster

For the query engine, I will choose Trino thanks to its support for a wide range of data sources via the connectors. The connectors contain the necessary information for Trino to work with the data source.

A Trino cluster has a coordinator node and a set of worker nodes:

[![](https://substackcdn.com/image/fetch/$s_!9648!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1874f015-4b6a-4933-986f-c15775411af9_978x608.png)](https://substackcdn.com/image/fetch/$s_!9648!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1874f015-4b6a-4933-986f-c15775411af9_978x608.png)

* The coordinator parses, plans, and orchestrates queries. A node can act as both coordinator and worker; however, it is recommended to dedicate a single node solely for the coordinator to ensure optimal performance.
* The workers execute the query.

In this project, I will set up a cluster consisting of one coordinator and two workers. To configure the role for each Trino node, I prepared two files:

* Coordinator configuration: `./trino\_config/coordinator/config.properties`

  [![](https://substackcdn.com/image/fetch/$s_!sTsX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4320b8ca-2403-4d27-8bfc-ea2ea9e80020_654x160.png)](https://substackcdn.com/image/fetch/$s_!sTsX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4320b8ca-2403-4d27-8bfc-ea2ea9e80020_654x160.png)
* Worker configuration: `./trino\_config/worker/config.properties`

[![](https://substackcdn.com/image/fetch/$s_!TtH2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1d87092e-93fd-4d66-9702-224f673d6244_662x122.png)](https://substackcdn.com/image/fetch/$s_!TtH2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1d87092e-93fd-4d66-9702-224f673d6244_662x122.png)

Both the Coordinator and Worker require the `discovery.uri`. The Coordinator informs its accept endpoint, and the Worker knows which Coordinator it will communicate with.

### Catalog and connector

To work with a data source, Trino introduces the concept of the catalog (this is different from the Iceberg catalog), which represents a single data source that the Trino engine can access. Each catalog must be associated with a connector.

In the scope of this project, I will configure a Trino catalog with the file `./trino\_config/catalog/iceberg.properties`:

[![](https://substackcdn.com/image/fetch/$s_!7zIL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffa7f521b-a9c9-4cce-a240-1bccd782f7d2_976x404.png)](https://substackcdn.com/image/fetch/$s_!7zIL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffa7f521b-a9c9-4cce-a240-1bccd782f7d2_976x404.png)

* The catalog will have the name “iceberg“ (based on the name of the config file, not the connector name)
* We specify Nessie as the catalog type, the URI with the Nessie-catalog container endpoint, and the 19120 port.
* For the git-like feature, Nessie requires the `ref` option. In the scope of this project, we will specify the default Nessie branch here: `main`.
* For the warehouse-dir, we specify the bucket created at the time of MinIO server creation: the `local-lakehouse`.
* For the s3.endpoint, we used the value in the MINIO\_DOMAIN (in our project, it is `minio`) env variable in the MinIO container, plus the port 9000.
* We also need to input the MinIO region (MINIO\_REGION), the access key (MINIO\_ROOT\_USER), and the secret key (MINIO\_ROOT\_PASSWORD) here.

### SQL init script

There is an SQL script to initialize some required schemas in Trino. It will be run when you run the command:

```
./manage-lakehouse.sh start
```

The script's content creates three schemas: landing, staging, and curated.

[![](https://substackcdn.com/image/fetch/$s_!ShID!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd1f388b2-250c-4b02-aaee-ffcfbfdf801e_340x114.png)](https://substackcdn.com/image/fetch/$s_!ShID!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd1f388b2-250c-4b02-aaee-ffcfbfdf801e_340x114.png)

A schema in Trino will be associated with a namespace in Nessie. Nessie’s namespace enables the logical grouping of tables, similar to a schema in Snowflake or a dataset in BigQuery. Each namespace will be stored in separate “folders“:

[![](https://substackcdn.com/image/fetch/$s_!_Lmi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff97d582b-a1c8-43a6-a7c0-f8a32adad03a_284x272.png)](https://substackcdn.com/image/fetch/$s_!_Lmi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff97d582b-a1c8-43a6-a7c0-f8a32adad03a_284x272.png)

> **Note**: Cloud object storage does not have folders. However, users can organize the data using a prefix to **make it look like folders**. A prefix is a string of characters at the beginning of the object key. Two objects, `2025/sales.csv` and `2025/inventory.csv`, will appear to be in a `2025` folder. However, they are just two objects in the bucket that share the `reports/2025/` prefix. No actual folders here.

### Glue things together

Here is the content of the `docker-compose-trino.yaml` file:

[![](https://substackcdn.com/image/fetch/$s_!h6Yq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8187e13e-4add-4cee-9661-56368ff9de80_994x826.png)](https://substackcdn.com/image/fetch/$s_!h6Yq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8187e13e-4add-4cee-9661-56368ff9de80_994x826.png)

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=172333626)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

---

## The dbt project

I set up a simple dbt project in `./dags/dbt\_trino`:

* The `profiles.yml` contains the information to let dbt work with the Trino cluster

  [![](https://substackcdn.com/image/fetch/$s_!juMe!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0fe1f3e5-f9ac-4884-be92-18489356a7f6_418x366.png)](https://substackcdn.com/image/fetch/$s_!juMe!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0fe1f3e5-f9ac-4884-be92-18489356a7f6_418x366.png)
* In the `dbt\_project.yml`, I specify the dataset for the models and seeds:

  [![](https://substackcdn.com/image/fetch/$s_!mjmc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F42d6da9d-c9d6-4673-8b26-500520cca6eb_252x336.png)](https://substackcdn.com/image/fetch/$s_!mjmc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F42d6da9d-c9d6-4673-8b26-500520cca6eb_252x336.png)
* In the seeds folder, 5 CSV files contain the [AdventureWorks sample dataset](https://github.com/vutrinh274/bauplan_example/tree/master/adventure_works_data): product, product\_category, product\_subcategory, sale, and territories. As configured in the `dbt\_project`, when running `[dbt seed](https://docs.getdbt.com/reference/commands/seed)`, all these CSV files will be loaded into the `landing` schema in Trino.

  > The `dbt seed` command will load CSV files in the seed paths (default: `seeds` folder) into the configured warehouse.

  [![](https://substackcdn.com/image/fetch/$s_!tgDk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5e33a4f8-39d3-4f91-aacd-1a1742e45414_374x298.png)](https://substackcdn.com/image/fetch/$s_!tgDk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5e33a4f8-39d3-4f91-aacd-1a1742e45414_374x298.png)
* In the `models` folder, there are dbt models to transform the data in the `landing` schema. The data undergoes two stages: staging and curated, where curated data is ready for downstream usage.

  [![](https://substackcdn.com/image/fetch/$s_!MFje!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa22d5502-cdee-467c-adcf-893c51b83600_284x328.png)](https://substackcdn.com/image/fetch/$s_!MFje!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa22d5502-cdee-467c-adcf-893c51b83600_284x328.png)
* In production, data in the staging area must be cleaned, standardized, and transformed before being processed according to business logic in the curated area. In the scope of the project, I have to admit that I was pretty lazy as I only `select \*` from landing tables in the staging area.

## The Airflow DAG

> *This component is managed in the file `docker-compose-airflow.yaml`. You can choose to run only the lake setup by running `docker compose -f docker-compose-airflow.yaml up -d`*

### Getting the Airflow 3.0.6 environment running

For Airflow, I used the officially supported Docker Compose file from Airflow, so there's not much to discuss here, except that we need to install the dbt package for the Airflow environment.

> ***Note**: The Docker Compose file from Airflow uses CeleryExecutor by default; you can adjust the executor based on your needs.*

After [downloading the Docker Compose file](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#fetching-docker-compose-yaml), I need to adjust the `image` configuration in the file to use a custom one, which is defined by the Dockerfile located in the same directory:

[![](https://substackcdn.com/image/fetch/$s_!HnVn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F11c7652d-d0c5-4cab-afde-92f428556901_552x76.png)](https://substackcdn.com/image/fetch/$s_!HnVn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F11c7652d-d0c5-4cab-afde-92f428556901_552x76.png)

When specifying `build: .`, Docker will look for the Dockerfile in the same directory, build it, and use that image for the container. In the scope of our project, the Dockerfile is simply based on the existing official Airflow image, adds the `requirements-dbt.txt` file, and installs it.

[![](https://substackcdn.com/image/fetch/$s_!QIUE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a9a1ce9-6810-42a2-a49e-30f6d1cf12ad_890x116.png)](https://substackcdn.com/image/fetch/$s_!QIUE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a9a1ce9-6810-42a2-a49e-30f6d1cf12ad_890x116.png)

The `requirements-dbt.txt` file contains two dbt packages:

[![](https://substackcdn.com/image/fetch/$s_!YfMp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Febfa33dc-e1ea-428f-91bc-f7aa896fcd50_266x82.png)](https://substackcdn.com/image/fetch/$s_!YfMp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Febfa33dc-e1ea-428f-91bc-f7aa896fcd50_266x82.png)

After the Airflow environment is started, you can visit it via `localhost:8081`. By default, the Airflow webserver port will be mapped to the host’s 8080 port. However, this port is already in use by the Trino coordinator, so I had to adjust the Airflow UI to port 8081:

[![](https://substackcdn.com/image/fetch/$s_!F6dp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F548b2114-bd3e-4a7e-bb05-7db7cabc80a3_276x170.png)](https://substackcdn.com/image/fetch/$s_!F6dp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F548b2114-bd3e-4a7e-bb05-7db7cabc80a3_276x170.png)

When visiting the Airflow UI for the first time, you need to log in. Use the ones set in \_AIRFLOW\_WWW\_USER\_USERNAME (default is `airflow`) and \_AIRFLOW\_WWW\_USER\_PASSWORD (default is `airflow`):

[![](https://substackcdn.com/image/fetch/$s_!mQ9E!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F765226f6-8e7f-4331-9879-045cdf50a1da_986x80.png)](https://substackcdn.com/image/fetch/$s_!mQ9E!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F765226f6-8e7f-4331-9879-045cdf50a1da_986x80.png)

### The custom Airflow operator to work with dbt

Upon checking, I found that there is only a supported Operator for dbt Cloud, so we need to create our own operator for the Airflow worker to run the dbt command.

In the `docker-compose-airflow.yaml`, the folder ./dags, ./logs, ./config, ./plugins will be mounted to Airflow environment. We will define our DAGs and the custom operator in the ./dags folder. A quick note: to allow the worker to view our dbt project, I need to move the `dbt\_trino` folders into the ./dags folder.

[![](https://substackcdn.com/image/fetch/$s_!fjnK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe8896fac-6cb9-46f7-9831-ac8f45321beb_202x96.png)](https://substackcdn.com/image/fetch/$s_!fjnK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe8896fac-6cb9-46f7-9831-ac8f45321beb_202x96.png)

Back to the custom operator, I defined the logic in the ./dags/custom\_operator/

[![](https://substackcdn.com/image/fetch/$s_!0Kde!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc9c7836a-a065-46c6-a10f-1580af6a8950_252x130.png)](https://substackcdn.com/image/fetch/$s_!0Kde!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc9c7836a-a065-46c6-a10f-1580af6a8950_252x130.png)

To define the custom operator, one must extend the `BaseOperator` and explain the logic for the `execute method`. The DbtCoreOperator accepts arguments that are later used to build the dbt command.

[![](https://substackcdn.com/image/fetch/$s_!rXEy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc85a3a12-b781-4dab-9b67-eafb84c64efc_474x530.png)](https://substackcdn.com/image/fetch/$s_!rXEy!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc85a3a12-b781-4dab-9b67-eafb84c64efc_474x530.png)

In the `execute` method, we construct the dbt command and utilize the `[dbtRunner](https://docs.getdbt.com/reference/programmatic-invocations)`, the entry point for executing commands. It is a part of the dbt CLI package, [an official support for dbt programmatic invocations since version 1.5](https://docs.getdbt.com/reference/programmatic-invocations).

[![](https://substackcdn.com/image/fetch/$s_!EkoK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb30dc973-b496-48a5-a8ed-bd66d86a2242_618x524.png)](https://substackcdn.com/image/fetch/$s_!EkoK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb30dc973-b496-48a5-a8ed-bd66d86a2242_618x524.png)

### The DAG

After having the custom operator, I define a simple DAG in ./dags/dbt\_dag.py:

[![](https://substackcdn.com/image/fetch/$s_!Hq0z!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe0c5bccb-a5ae-4d57-806d-9b7ff861ea82_244x152.png)](https://substackcdn.com/image/fetch/$s_!Hq0z!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe0c5bccb-a5ae-4d57-806d-9b7ff861ea82_244x152.png)

We import the DbtCoreOperator and other required packages, specify the dbt project path (which is now located inside the ./dags folder), and define a DAG with two tasks, the first will run `dbt seed`to load CSV files to the `landing`, and the second will run `dbt run` to execute the model defined in the `./dags/dbt\_trino/models` directory.

[![](https://substackcdn.com/image/fetch/$s_!SlL6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa202f9f5-9d71-4932-ace2-6a9ae328698f_450x858.png)](https://substackcdn.com/image/fetch/$s_!SlL6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa202f9f5-9d71-4932-ace2-6a9ae328698f_450x858.png)

### Run the pipeline

Now you can run the pipeline, open `localhost:8081`, navigate to `Dags` from the left menu, and choose `dbt\_pipeline` (the DAG name is defined by the `dag\_id` in the `dbt\_dag.py`)

[![](https://substackcdn.com/image/fetch/$s_!2q0T!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F521faa98-3617-4da7-beb0-5c72298e6ec5_400x344.png)](https://substackcdn.com/image/fetch/$s_!2q0T!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F521faa98-3617-4da7-beb0-5c72298e6ec5_400x344.png)

After that, you can trigger the pipeline to run manually:

[![](https://substackcdn.com/image/fetch/$s_!7Xx1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fca63f457-5d12-4726-8873-2dbf5552cdfd_1410x326.png)](https://substackcdn.com/image/fetch/$s_!7Xx1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fca63f457-5d12-4726-8873-2dbf5552cdfd_1410x326.png)

Here is the result of one of my attempts:

* Seed task:

[![](https://substackcdn.com/image/fetch/$s_!3Kvd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff84639f4-188e-4caf-844b-8766a4cfee00_2442x1022.png)](https://substackcdn.com/image/fetch/$s_!3Kvd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff84639f4-188e-4caf-844b-8766a4cfee00_2442x1022.png)

* Run task

[![](https://substackcdn.com/image/fetch/$s_!bwBC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe3efdd7f-254b-4a05-8a74-ef69506d7505_2440x1054.png)](https://substackcdn.com/image/fetch/$s_!bwBC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe3efdd7f-254b-4a05-8a74-ef69506d7505_2440x1054.png)

Yeah, I know, that was a lot of retries because I reused the SQL logic last used with Snowflake, which led to incompatibilities when switching to Trino. But don’t worry, I'll fix all of them, and you can run the pipeline super smoothly. (At least that's what I hope).

You can visit the MinIO bucket to see if the Iceberg data is actually there:

[![](https://substackcdn.com/image/fetch/$s_!xE_7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F17846b3d-a946-4814-939e-d92ce2875cb2_522x476.png)](https://substackcdn.com/image/fetch/$s_!xE_7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F17846b3d-a946-4814-939e-d92ce2875cb2_522x476.png)

Here is my content inside the `curated` namespace, there are tables `fact\_sale`, `dim\_country`, and `dim\_product`. There is also a folder with the \_\_dbt\_tmp suffix, which stores the temp data during the time dbt executes the commands.

## Clean up

To clean up everything, you can run the following command to wipe out all the Docker containers:

```
./manage-lakehouse.sh stop
```

## Outro

In this article, I first share my intention for this pet project, provide a high-level overview of how things work, and outline the solutions/tools involved. Then, I delve into each component to share in detail how they get it up and running.

I hope my work here could help you with some of the first steps in building your own pet project. You can use the data source you want, define more complex SQL logic, adjust the settings of Trino to handle extensive data, or execute dbt commands at a higher isolation level with the Kubernetes executor.

Thank you for reading this far. See you in the next articles. If you follow this project and encounter any issues, please don't hesitate to contact me.

## Reference

*[1] Gilles Philippart, [Build a Data Lakehouse with Apache Iceberg, Polaris, Trino & MinIO](https://medium.com/@gilles.philippart/build-a-data-lakehouse-with-apache-iceberg-polaris-trino-minio-349c534ecd98), 2025*

*[2] Alex Merced, [Hands-on with Apache Iceberg on Your Laptop: Deep Dive with Apache Spark, Nessie, Minio, Dremio, Polars, and Seaborn](https://dev.to/alexmercedcoder/hands-on-with-apache-iceberg-on-your-laptop-deep-dive-with-apache-spark-nessie-minio-dremio-polars-and-seaborn-2hgk), 2024*

*[3] [Iceberg official documentation](https://iceberg.apache.org/docs/1.5.2/)*

*[4] [Airflow official documentation](https://airflow.apache.org/docs/apache-airflow/stable/index.html)*

*[5] [MinIO official documentation](https://docs.min.io/community/minio-object-store/index.html)*

*[6] [Project Nessie official documentation](https://projectnessie.org/guides/)*

*[7] [dbt official documentation](https://docs.getdbt.com/docs/introduction)*

*[8] [Trino official documentation](https://trino.io/docs/current/index.html)*
