---
title: "Bauplan: Operate your lakehouse with zero infrastructure"
channel: vutr
author: "Vu Trinh"
published: 2025-03-20
url: https://vutr.substack.com/p/bauplan-operate-your-lakehouse-with
paid: false
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Apache Iceberg", "Data Warehouse", "Data Lake", "Lakehouse", "Orchestration"]
tags: [https, auto, bauplan, image, substackcdn, fetch]
---

# Bauplan: Operate your lakehouse with zero infrastructure

*FaaS data pipelines on S3*

> Source: [Open post](https://vutr.substack.com/p/bauplan-operate-your-lakehouse-with)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[data-warehouse|Data Warehouse]] · [[data-lake|Data Lake]] · [[lakehouse|Lakehouse]] · [[orchestration|Orchestration]]

---

> *I’m making my life less dull by spending time learning and researching “how it works“ in the data engineering field.*
>
> *Here is a place where I share everything I’ve learned. Not subscribe yet? Here you go:*
>
> [Subscribe now](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!B8NP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F630ecef6-7c95-46f0-a849-bc57654fa14b_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!B8NP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F630ecef6-7c95-46f0-a849-bc57654fa14b_2000x1428.png)

Image created by the author.

---

## Intro

AWS Lambda is a fascinating service.

I first used it in 2021, and the experience was seamless. I wrote some code and configured how it should be triggered, and that was it.

Whenever a new file arrived in S3, my Lambda function would wake up, execute some logic, and then go back to sleep. I didn’t have to worry anything about the infrastructure.

That made me wonder: could I achieve the same simplicity with my data pipelines?

What if there was no need to set up an Airflow environment or provision a Spark cluster? What if I could define the pipeline logic—similar to an AWS Lambda function—and somehow, the input data would transform into the desired output?

This week, we’re diving into Bauplan, a solution that makes that wish come true.

---

## Overview

Function-as-a-Service (FaaS) is a cloud computing model that allows developers to run code in response to events without managing the infrastructure. It enables a serverless approach, where the cloud provider handles provisioning, scaling for bursty workloads, and execution, allowing engineers to focus on writing logic. A well-known example is AWS Lambda.

[![](https://substackcdn.com/image/fetch/$s_!mVa3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F59eacd31-cb8b-4088-a62b-278a62a4a2e2_922x446.png)](https://substackcdn.com/image/fetch/$s_!mVa3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F59eacd31-cb8b-4088-a62b-278a62a4a2e2_922x446.png)

Image created by the author.

FaaS makes it simple for the developer.

[Bauplan](https://www.bauplanlabs.com/), a team from New York and San Francisco, believes that the FaaS model can also simplify work for data engineers, analysts, data scientists, or anyone who wants to work with data.

[![](https://substackcdn.com/image/fetch/$s_!Ol9W!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2f0b7487-df79-412f-bcfa-471eb1448ab9_592x326.png)](https://substackcdn.com/image/fetch/$s_!Ol9W!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2f0b7487-df79-412f-bcfa-471eb1448ab9_592x326.png)

Image created by the author.

Still, the solutions available on the market cannot adapt to the data workload. We usually define a data pipeline as a Directed Acyclic Graph (DAG), in which each node is a function that receives data from previous nodes, applies logic, and outputs results for the following nodes.

[![](https://substackcdn.com/image/fetch/$s_!QQqp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0a801450-9a24-4fda-abee-9fd67ca4bfb9_898x354.png)](https://substackcdn.com/image/fetch/$s_!QQqp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0a801450-9a24-4fda-abee-9fd67ca4bfb9_898x354.png)

Image created by the author.

Modularizing the business logic into nodes makes developing, collaborating, and testing more convenient. But when implementing the DAG data pipeline using available FaaS solutions, some challenges emerge:

* **Scaling:** Existing FaaS runtimes are designed for simple, independent functions that produce small outputs (e.g., a webhook). They have limitations when applied to data pipelines. Additionally, these FaaS platforms usually reuse instances for subsequent triggers. It can use the same function instance for 10 GB and 1TB of input with the same data function. “Out of memory” errors are common.

  [![](https://substackcdn.com/image/fetch/$s_!1R5W!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa80f11e1-700d-4cd7-b038-10cae424b629_472x268.png)](https://substackcdn.com/image/fetch/$s_!1R5W!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa80f11e1-700d-4cd7-b038-10cae424b629_472x268.png)

  Image created by the author.
* **Large intermediate I/O**: To implement the DAG concept, users must chain functions. A function acts as a “node“ that receives input from previous functions and produces output for the following functions. Data functions typically have large inputs and outputs, which increases the cost of serializing and moving the data payload between functions. Popular FaaS platforms' chaining best practices are limiting because intermediate data frames can only be transferred through object storage.

  [![](https://substackcdn.com/image/fetch/$s_!yLbq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc5cd9f4d-13b9-47e4-8760-0a49b403df70_552x330.png)](https://substackcdn.com/image/fetch/$s_!yLbq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc5cd9f4d-13b9-47e4-8760-0a49b403df70_552x330.png)

  Image created by the author.
* **Slow feedback loop**: Data science projects are exploratory and require rapid iteration to validate hypotheses. Current FaaS platforms lack the interactivity needed for these projects due to their slow build times and lack of interactive logging. AWS Lambda provides only observability through Cloudwatch.

  [![](https://substackcdn.com/image/fetch/$s_!x87c!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7faaab81-6f83-427f-9e99-0e97902ba7af_384x282.png)](https://substackcdn.com/image/fetch/$s_!x87c!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7faaab81-6f83-427f-9e99-0e97902ba7af_384x282.png)

  Image created by the author.

So, how does Bauplan promise to solve these problems?

---

## The Bauplan FaaS

Bauplan is a FaaS service designed for data pipelines. Unlike other services, Bauplan initiates and scales independent instances for every run. It also promises to boost the intermediate data exchange process and allow users to modify and run DAGs interactively.

For the design principles:

[![](https://substackcdn.com/image/fetch/$s_!gNGs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F65db2a00-ba35-4896-96ac-6211159d7be2_568x242.png)](https://substackcdn.com/image/fetch/$s_!gNGs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F65db2a00-ba35-4896-96ac-6211159d7be2_568x242.png)

Image created by the author.

* Bauplan aims to make an execution stateless, and its instances only live during that run. Starting with new instances each time enables Bauplan to adapt to different resource requirements; the same pipeline can run with a 10GB dataset and later scale up to a 100 GB dataset.
* For the infrastructure, the Bauplan pipeline will run on the cloud Virtual Machines (VMs), which offer the highest level of customization. Using cloud VMs also allows Bauplan to offer multiple deployment models, such as BYOC, where customers can control where data is stored and processed.
* Bauplan is different from other tools because Bauplan has both data and runtime awareness (i.e., serverless runtimes like AWS Lambda don’t know about the data, and orchestration tools don’t know about the runtime). We’ll explore this design more deeply when we run some code later.
* Bauplan brings an interactive experience to the developer; although the pipeline runs on the cloud, users can develop as it runs on their laptops. Bauplan provides a CLI tool and Python SDK for users to interact with the system.
* Users define a function in Bauplan by specifying tables as input and output.

### Architecture

Bauplan has a Control Plane (CP) and a Data Plane (DP):

[![](https://substackcdn.com/image/fetch/$s_!-ftB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F62a36f2c-7bfc-428d-9bc3-35495a10dd8f_896x430.png)](https://substackcdn.com/image/fetch/$s_!-ftB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F62a36f2c-7bfc-428d-9bc3-35495a10dd8f_896x430.png)

Image created by the author.

* The CP exposes multi-tenant APIs. It only deals with metadata. The CP lives in Bauplan’s VPC.
* Each customer has a DP, a fleet of one or more cloud VMs that can be deployed in the customer VPCs. A Golang binary is installed in each VM to spawn the worker. These workers are the only Bauplan components that can access customer data.

To enable the developer to have an interactive experience, there is a bidirectional gRPC connection between customers and workers. Users write some `print` or `logging` statements to understand what happens during the pipeline run; although the code is run inside cloud VMs, the results are immediately visible to users thanks to the bidirectional connection.

### Planning

So, the CP needs to deal with metadata, but what is its responsibility?

Bauplan acts like a database; it translates Python and SQL code into an execution plan when it begins running the pipeline. When the user requests a run, the code is routed to the control plane (CP). The CP will parse the code and reconstruct the DAG topology from the functions, resulting in a logical plan.

This plan only represents the dependencies between steps and the required packages as specified by the user. Importantly, Bauplan will refuse to run DAGs that refer to non-existing tables (unlike dbt, for example), point to wrong snapshots, or ship Python code with invalid formatting.

[![](https://substackcdn.com/image/fetch/$s_!sOEK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F76939d02-3465-44f3-8483-85bae5a751da_1448x544.png)](https://substackcdn.com/image/fetch/$s_!sOEK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F76939d02-3465-44f3-8483-85bae5a751da_1448x544.png)

Image created by the author.

To give running instructions to the worker, the CP forms the physical plan from the logical one. This physical plan contains instructions for the containerized runtime of the transformation functions and mapping dataframes to a physical table in object storage. When having the physical plan, the CP sends it to workers to start the execution.

> *Data in Bauplan are store in Iceberg table in object storage, we will explore the storage layer soon.*

### The cache

As mentioned, function instances only exist during execution time. The two runs of the data pipeline will have different sets of instances. To reduce the latency when re-running the pipeline, Bauplan developed a robust package caching mechanism that avoids re-installing packages across runs, thus avoiding the overhead calls to PyPI.

For data caching, Bauplan’s data awareness makes database-like optimizations possible:

* **Re-using intermediate data**: Functions produce intermediate dataframes, and Bauplan tracks the change in code and data to cache and reuse intermediate data.

  [![](https://substackcdn.com/image/fetch/$s_!5Ly-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4069726b-749e-4a41-8b9b-eab2e9bd5de0_564x272.png)](https://substackcdn.com/image/fetch/$s_!5Ly-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4069726b-749e-4a41-8b9b-eab2e9bd5de0_564x272.png)

  Image created by the author.
* **Retrieving only missing columns**: The first run reads four columns from the table, and the second run requires exactly these four columns plus column X. Bauplan will reuse the four columns from the cache and only download one additional column X from the data source.

  [![](https://substackcdn.com/image/fetch/$s_!ltQ4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fff42229c-c448-45de-a1ff-75ab84417447_616x300.png)](https://substackcdn.com/image/fetch/$s_!ltQ4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fff42229c-c448-45de-a1ff-75ab84417447_616x300.png)

  Image created by the author.
* **Cache invalidation:** Because the physical data are stored in immutable files (via the Iceberg metadata), dataframe changes are identified with data commits such that the cache knows when data needs an update.

  [![](https://substackcdn.com/image/fetch/$s_!9v_w!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3b69f655-fc9f-46b7-9589-ba10d5850208_620x280.png)](https://substackcdn.com/image/fetch/$s_!9v_w!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3b69f655-fc9f-46b7-9589-ba10d5850208_620x280.png)

  Image created by the author.

### The data exchange

To enhance the data exchange process between functions, Bauplan represents intermediate dataframes as Arrow tables. From the official document:

> The Arrow columnar format includes a language-agnostic in-memory data structure specification, metadata serialization, and a protocol for serialization and generic data transport.

Unlike file formats like Parquet or CSV, which specify how data is organized on disk, Arrow focuses on how data is organized in memory.

[![](https://substackcdn.com/image/fetch/$s_!dR-h!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F75b893c6-34ec-4b48-86a2-087ac813d9d4_536x262.png)](https://substackcdn.com/image/fetch/$s_!dR-h!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F75b893c6-34ec-4b48-86a2-087ac813d9d4_536x262.png)

Image created by the author.

Arrow store values for each column contiguously in memory. This design is highly advantageous for data analytics workloads, which focus on a subset of columns when dealing with large datasets.

[![](https://substackcdn.com/image/fetch/$s_!Px5H!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F773dea41-6a3e-4000-811e-bcfe8fceeb24_460x216.png)](https://substackcdn.com/image/fetch/$s_!Px5H!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F773dea41-6a3e-4000-811e-bcfe8fceeb24_460x216.png)

Image created by the author.

Before Arrow, each system used its internal memory format. When two systems communicate, each converts its data into a standard format before transferring it, incurring serialization and deserialization costs. Apache Arrow aims to provide a highly efficient format for processing within a single system. As more systems adopt it, they can share data at a very low cost, potentially even through shared memory at zero cost.

[![](https://substackcdn.com/image/fetch/$s_!Mv-A!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0eceb864-8e2c-427f-8b8e-f13df4380060_1240x528.png)](https://substackcdn.com/image/fetch/$s_!Mv-A!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0eceb864-8e2c-427f-8b8e-f13df4380060_1240x528.png)

Image created by the author.

When Bauplan executes the pipeline, it will pick the sharing mechanism: memory or local disk (functions in the same worker) or Arrow Flight (across workers). Because other solutions only support S3-backed data exchange, moving data between functions in Bauplan can be hundreds of times faster, thanks to Arrow.

With Arrow, functions can read tables from shared memory, memory-map, or stream them from gRPC (with Flight), which gives the function greater flexibility when dealing with multiple data sources with different data transfer mechanisms.

> *A [memory-mapped file](https://en.wikipedia.org/wiki/Memory-mapped_file) is a segment of virtual memory that has been assigned a direct byte-for-byte correlation with some portion of a file or file-like resource. The benefit of memory mapping a file is increasing I/O performance, especially when used on large files.*

Moreover, if a downstream function runs on the same worker as the upstream function, it can read the Arrow intermediate data on the worker without copying the data. Given intermediate data with 10GBs and four functions needed to read it, it only takes 10Gbs physical RAM instead of 10x4=40Gbs.

---

## The storage

Bauplan does not stop there; beyond the FaaS data pipeline, they also aim to provide a complete lakehouse solution by offering a storage layer with Iceberg and Project Nessie.

If you have some Parquet files in the object storage, Bauplan can help you transform them into an Iceberg table in a single line of code. The data stays in your VPC; it doesn’t need to move anywhere.

Netflix created Apache Iceberg to achieve better table correctness and faster query planning (than Hives). An Apache Iceberg table has three layers organized hierarchically:

[![](https://substackcdn.com/image/fetch/$s_!qXMo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0da0451b-2a2b-4f26-8aad-63ba94220266_474x620.png)](https://substackcdn.com/image/fetch/$s_!qXMo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0da0451b-2a2b-4f26-8aad-63ba94220266_474x620.png)

Image created by the author.

* The data layer stores the table’s actual data, including the data and deleted files.
* Manifest files track the data files in the data layer.
* A manifest list captures the snapshot of an Iceberg table at a specific moment.
* Metadata files contain information about an Iceberg table at a specific time, such as the schema or the latest snapshot.
* The catalog is where every Iceberg data operation begins. It provides the engine with the location of the current metadata pointer and tells you where to go first.

Like other table formats, Iceberg's ultimate goal is to bring data warehouse capabilities to the data lake; one important one is the ACID constraints.

The Iceberg only ensures atomic transactions at the table level. To bring the software development experience to the lakehouse, Bauplan uses Project Nessie for the Iceberg table catalog. It is an open-source versioned metadata catalog that enables cross-table transactions for Iceberg. Users can update multiple tables together and guarantee all changes occur atomically – an all-or-nothing commit across tables.

[![](https://substackcdn.com/image/fetch/$s_!Swfv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F40b50529-0184-419f-b5f4-1fc167498e2e_884x328.png)](https://substackcdn.com/image/fetch/$s_!Swfv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F40b50529-0184-419f-b5f4-1fc167498e2e_884x328.png)

Image created by the author.

Bauplan makes it easier for users to seamlessly work with Nessie and Iceberg tables by providing CLI commands and Python SDKs. Users will feel just like they are working with a Git repository.

In the next section, we'll explore all the cool Bauplan features mentioned above, where we'll run some code.

This post was written in collaboration with the [Bauplan team](https://www.bauplanlabs.com/). The final wording and opinions are mine.

## Run some code

We will run some Python code and CLI commands; I prepared a [Git repo](https://github.com/vutrinh274/bauplan_example) so you can follow along. Make sure you pull the repo locally and enter the [bauplan\_example](https://github.com/vutrinh274/bauplan_example) folder.

First, we need to set up a Python virtual environment with the [requirements.txt](https://github.com/vutrinh274/bauplan_example/blob/master/requirements.txt) file from the repo. We will install `bauplan`, `streamlit` and `duckdb` packages.

Next, we need the Bauplan API key, which gives you access to the Bauplan sandbox environment. You can contact Bauplan [here](https://www.bauplanlabs.com/#join) for the key.

```
bauplan config set api_key "your_bauplan_key"
```

Then, we will run some bash scripts to set up; let’s make those scripts executable:

```
chmod -R +x scripts/
```

Bauplan is designed to operate exclusively in the cloud to ensure a fully auditable and secure data development cycle. They require us to store data in object storage so it can support importing to the Iceberg table.

Currently, Bauplan only supports S3 as the data source and Parquet and CSV as file formats. We will run a script that creates an S3 bucket, uploads some CSV files, checks out to a branch, creates a namespace, and then imports these files to the Iceberg table in Bauplan Sandbox. But first, make sure you configure your AWS CLI:

```
aws configure # Entering AWS access key, secret and default region
```

Then, run the [setup.sh](https://github.com/vutrinh274/bauplan_example/blob/master/scripts/setup.sh) with the S3 bucket name you want to create and the Bauplan branch. The branch must be in a pattern `<your-user-name>.<something>`

```
./scripts/setup.sh <bucket name> <bauplan branch>
```

[![](https://substackcdn.com/image/fetch/$s_!q6l7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F882583fa-5ec7-44f3-8e24-ecf4ce66b5f5_1008x692.png)](https://substackcdn.com/image/fetch/$s_!q6l7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F882583fa-5ec7-44f3-8e24-ecf4ce66b5f5_1008x692.png)

Image created by the author.

Wait for a while, and then you will have five tables in your catalog. The script will create a namespace called `adventure`. A namespace in Bauplan is a logical container that helps organize tables within a data catalog. We will work on your input branch and the `adventure` namespace from this time. Let’s list out the input tables:

```
bauplan table --namespace adventure
```

Before we move on, let’s understand the input data. We will have five input tables from the [AdventureWorks sample dataset](https://github.com/vutrinh274/bauplan_example/tree/master/adventure_works_data): product, product\_category, product\_subcategory, sale, and territories.

> *[AdventureWorks](https://dataedo.com/samples/html/AdventureWorks/doc/AdventureWorks_2/home.html) database supports standard online transaction processing scenarios for a fictitious bicycle manufacturer - **Adventure Works Cycles**.*

The relationship of the tables is:

[![](https://substackcdn.com/image/fetch/$s_!f1Er!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa3563684-51d2-4652-b59f-bf2c48013a86_1822x830.png)](https://substackcdn.com/image/fetch/$s_!f1Er!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa3563684-51d2-4652-b59f-bf2c48013a86_1822x830.png)

Image created by the author.

In this project, we will write a Bauplan pipeline to transform these input tables into a dimensional data model with a `fact_sale`, `dim_product`, and `dim_country`:

[![](https://substackcdn.com/image/fetch/$s_!q0I0!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F21590eee-d4c7-4d17-a949-bf418182603c_1706x786.png)](https://substackcdn.com/image/fetch/$s_!q0I0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F21590eee-d4c7-4d17-a949-bf418182603c_1706x786.png)

Image created by the author.

We implement the transformation pipeline using Bauplan models. A model function takes tabular data as input and produces tabular data. We will write a DAG to transform the data using the duckdb engine:

[![](https://substackcdn.com/image/fetch/$s_!N1w_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe6b713fd-4d67-4f21-b2f6-280c4268b53a_672x506.png)](https://substackcdn.com/image/fetch/$s_!N1w_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe6b713fd-4d67-4f21-b2f6-280c4268b53a_672x506.png)

Image created by the author.

We define these models in the [models.py](https://github.com/vutrinh274/bauplan_example/blob/master/pipeline/models.py) file. A very important point is that the Bauplan model is aware of both data and runtime.

For runtime awareness, you can use Bauplan’s decorator to specify the runtime for each model, such as the Python version and packages, how to materialize the output, and allow for explicit column selection and filter pushdown.

For data awareness, each model must have inputs, which can be tables in the catalog or other models. We specify and use them like Python function parameters.

Here is the code of the `dim_product` model. As you can see, for this model, Bauplan knows that it must run the model with `Python 3.11`, `duckdb 1.0.0` and the model has `product`, `product_category`, `product_subcategory` as input data.

You can check the codes for all the models [here](https://github.com/vutrinh274/bauplan_example/blob/master/pipeline/models.py).

[![](https://substackcdn.com/image/fetch/$s_!oABQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F906352e5-0569-4cb1-836a-3cfd58b11396_1362x994.png)](https://substackcdn.com/image/fetch/$s_!oABQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F906352e5-0569-4cb1-836a-3cfd58b11396_1362x994.png)

Screenshot from my [code](https://github.com/vutrinh274/bauplan_example).

After having the models, we run the pipeline:

```
bauplan run --project-dir pipeline --namespace adventure
```

We submit the code to Bauplan. It will plan and execute it. If there are any errors, it will display in real-time in the terminal for us thanks to the bidirectional gRPC connection between us and the Bauplan workers.

To run the pipeline, we need a [bauplan\_project.yml](https://github.com/vutrinh274/bauplan_example/blob/master/pipeline/bauplan_project.yml) file containing the project’s unique ID and name. I located both the bauplan\_project.yml and models.py files in the pipeline folder.

After the pipeline finishes, you can check the output tables by listing the namespace adventure again:

```
bauplan table --namespace adventure
```

Finally, to have more fun with the project, I created a small Streamlit app with a world-class SQL editor (:D) to query the output table:

```
streamlit run streamlit/app.py
```

Here is a quick demo video to showcase my world-class SQL editor:

To clean up, you can run the [clean\_up.sh](https://github.com/vutrinh274/bauplan_example/blob/master/scripts/clean_up.sh) to clean up the S3 bucket and Bauplan table automatically:

```
./scripts/clean_up.sh <bucket name> <bauplan branch>
```

---

## My thoughts

In a world where data is the new gold, every company wants the ability to capture, store, process, and serve data to drive business decisions. However, not every company has a dedicated data team. In many cases, you might be the team's first and only data person.

At the beginning of this article, I had a wish—and it came true. Bauplan handles tasks that would typically require an entire infrastructure team. Its goal is to provide a seamless, developer-friendly way to work with large-scale data directly in Python, eliminating infrastructure bottlenecks.

When running some code with Bauplan, I was truly impressed by how seamlessly it imports data files from object storage into Iceberg tables. Setting up an Iceberg catalog, configuring the Iceberg writer, and managing the physical layout is usually a painful process, but Bauplan simplifies it significantly.

Defining data transformations is also a pleasant experience, thanks to Bauplan’s concept of a “model.” I can run transformations with Python 3.9 or 3.10 simply by changing a few lines in a decorator. The model’s data-awareness makes it incredibly intuitive to write transformation logic—I can specify it as easily as defining function inputs in Python.

Bauplan is truly innovative. It’s well worth your time trying, especially if you’re a data engineer, data analyst, or data scientist—or if you simply love working with data.

Personally, I hope Bauplan will expand to support data processing runtimes like Spark or Trino. A serverless Spark or Trino cluster would be a game-changer. Additionally, a robust SQL editor for querying data in the catalog would be a valuable addition.

---

## Outro

Thank you for reading this far.

In this article, we explore the challenges of implementing the data pipeline with available FaaS solutions, how Bauplan promises to solve them, Bauplan’s design goals and architecture, how Bauplan offers a complete zero-infrastructure lakehouse with the Iceberg + Project Nessie storage layer, and finally we write some code to build a Bauplan pipeline.

Now, it’s time to say goodbye. See you in my following articles.

---

## Reference

*[1] [Bauplan Documents](https://docs.bauplanlabs.com/en/latest/)*

*[2] Jacopo Tagliabue, Tyler Caraza-Harter, Ciro Greco, [Bauplan: zero-copy, scale-up FaaS for data pipelines](https://arxiv.org/pdf/2410.17465) (2024)*
