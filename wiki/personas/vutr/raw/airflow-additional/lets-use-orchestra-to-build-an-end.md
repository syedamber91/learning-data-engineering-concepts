---
title: "Let's use Orchestra to build an end-to-end data pipeline in 10 minutes"
channel: vutr
author: "Vu Trinh"
published: 2025-04-24
url: https://vutr.substack.com/p/lets-use-orchestra-to-build-an-end
paid: false
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Snowflake", "Databricks", "BigQuery", "Data Warehouse", "Orchestration", "ETL"]
tags: [https, auto, orchestra, pipeline, good, substackcdn]
---

# Let's use Orchestra to build an end-to-end data pipeline in 10 minutes

*Spoiler: You don't have to manage the infrastructure.*

> Source: [Open post](https://vutr.substack.com/p/lets-use-orchestra-to-build-an-end)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]] · [[orchestration|Orchestration]] · [[etl|ETL]]

---

> *I’m making my life less dull by spending time learning and researching “how it works“ in the data engineering field.*
>
> *Here is a place where I share everything I’ve learned. Not subscribe yet? Here you go:*
>
> [Subscribe now](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!kcj-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F403b657a-3166-4829-9e9f-c3caf179f3ee_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!kcj-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F403b657a-3166-4829-9e9f-c3caf179f3ee_2000x1428.png)

---

## Intro

We’re living in a time when it’s getting easier for data practitioners to build data pipelines. Cloud data warehouses are getting more and more powerful. The introduction of dbt streamlines data transformation using SQL.

However, that does not mean the above pattern has no challenges. We must set up the traditional orchestrator environments and determine how to schedule dbt tasks. If you use the free version of dbt, you must write a custom operator by yourself, as there is only support for the dbt cloud operator.

These tasks are not easy.

Realizing these hassles, [Orchestra](https://getorchestra.io/), a complete Data and AI workflow solution, offers us a more efficient way to operate the end-to-end data pipeline.

---

## Motivation

The idea of Orchestra is simple:

Giving everyone the power to build and manage Data and AI workflows, even if they have little engineering experience.

Orchestra aims to democratize the ability to build, deploy, and monitor pipelines, which was the main responsibility of highly skilled data engineers in the past.

With Orchestra, we only need to log in to the platform and set up how to connect with external systems like dbt or the cloud data warehouse, and then we can start building the first data pipeline.

It’s an efficient, declarative framework for defining DAGs, with the option to use Python/dbt. Orchestra abstracts away all the complexity for users and exposes only modern UI/UX for all operations.

---

## Let’s build a data pipeline

This section will walk you through the step-by-step process of building a data pipeline on Orchestra. We will also explore Orchestra concepts and features.

### A brief on the data pipeline

> *You can find all the related code in this [repo](https://github.com/vutrinh274/dbt_example).*

[![](https://substackcdn.com/image/fetch/$s_!PIGf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F89b694f7-2fcb-450a-bb34-716ae8c9cbe5_676x374.png)](https://substackcdn.com/image/fetch/$s_!PIGf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F89b694f7-2fcb-450a-bb34-716ae8c9cbe5_676x374.png)

In this project, we will need an [Orchestra account](https://app.getorchestra.io/signup), a [Snowflake (trial) account](https://signup.snowflake.com/), and an S3 bucket to follow along.

We will use a Python script to load CSV files to S3.

> *We use five AdventureWorks sample datasets: product, product\_category, product\_subcategory, sale, and territories. You can find these files in the repo.*

Then, we load these tables into Snowflake and set up a [dbt-snowflake](https://docs.getdbt.com/docs/core/connect-data-platform/snowflake-setup) project for the transformation.

All the tasks will be scheduled using Orchestra. You can check the Python script [here](https://github.com/vutrinh274/dbt_example/blob/main/python/upload_to_s3.py) and the dbt-snowflake project [here](https://github.com/vutrinh274/dbt_example/tree/main/dbt_example).

In the scope of this article, I won’t dive deep into how you could set up your Snowflake warehouse or the dbt project. If you want to learn, here are some good resources to get started:

* [Snowflake quick start](https://docs.snowflake.com/en/user-guide-getting-started)
* [dbt core quick start](https://docs.getdbt.com/guides/manual-install?step=4)
* [dbt-snowflake set up](https://docs.getdbt.com/docs/core/connect-data-platform/snowflake-setup)

### Set up the integrations

Like a traditional orchestrator, such as Airflow, one of the first things you want to do before building a data pipeline is to set up how you connect with the external systems. You would add some connections and maybe write some custom [hooks](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/connections.html), which can be time-consuming.

Orchestra provides managed integrations that take care of auth, error handling, triggering, polling, and metadata gathering out of the box. We set up “[integrations](https://docs.getorchestra.io/docs/core-concepts/integrations),” which are connections to external systems. They support [a wide range](https://www.getorchestra.io/integrations) of integrations:

[![](https://substackcdn.com/image/fetch/$s_!nqCr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F356ca6a7-e3cf-46b9-bd48-0427567d8215_460x300.png)](https://substackcdn.com/image/fetch/$s_!nqCr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F356ca6a7-e3cf-46b9-bd48-0427567d8215_460x300.png)

* ETL tools: Airbyte, Fivetran
* Data Warehouse: Databricks, Snowflake, or BigQuery
* Cloud Services: common tools in AWS, Azure, and GCP
* BI tools: Power BI, Tableau, Sigma, Lightdash, etc.
* Transformation: dbt core, dbt cloud, or Coalesce
* Utility functions: Python, http, etc.

To create a new integration, we click **“Integrations“** from the sidebar and then choose the needed integration from the UI.

[![](https://substackcdn.com/image/fetch/$s_!DIhB!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8061791b-9b00-416a-ad70-7fc18adcad3b_1454x404.png)](https://substackcdn.com/image/fetch/$s_!DIhB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8061791b-9b00-416a-ad70-7fc18adcad3b_1454x404.png)

For this project, we need to define three integrations: Snowflake, dbt, and Python.

[![](https://substackcdn.com/image/fetch/$s_!Tud2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbfd66b31-21ec-476b-9a5b-c90ab68c3fab_746x626.png)](https://substackcdn.com/image/fetch/$s_!Tud2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbfd66b31-21ec-476b-9a5b-c90ab68c3fab_746x626.png)

* The Python integration requires the connection name, the repo containing the Python scripts, and the token to help Orchestra have read access to the repo. You can check this [guide](https://docs.getorchestra.io/docs/integrations/utility/python/#github) to get the GitHub token.
* The dbt-core integration requires the connection name, the repo containing the dbt project, the GitHub token, and the dbt profile.
* The Snowflake integration requires the connection name and the Snowflake warehouse information.

### Set up the pipeline

Like Airflow, there is a concept called **“task,“** the most basic execution unit in Orchestra. Tasks leverage integrations to interact with the external system and execute the user-defined logic.

Users arrange tasks into [Pipelines](https://docs.getorchestra.io/docs/core-concepts/pipelines/), specifying the upstream and downstream dependencies. In other words, Pipeline lets Orchestra know in which order it should run your tasks.

To build the pipeline, we choose **Pipelines** in the sidebar → **New pipeline → + Create new Pipeline:**

* After this, you will see two options: **Orchestra** and **GitHub**. At this time, we will go with the **Orchestra**. This option lets you build the data pipeline directly on Orchestra’s UI.

  [![](https://substackcdn.com/image/fetch/$s_!xOrh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F017bdb74-6130-4a8e-808a-c6b3c027e883_500x148.png)](https://substackcdn.com/image/fetch/$s_!xOrh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F017bdb74-6130-4a8e-808a-c6b3c027e883_500x148.png)
* In the next step, Orchestra prompts you to choose the type of trigger you want. [Available options](https://docs.getorchestra.io/docs/core-concepts/triggers/) are manual, triggering by webhook, triggering by other pipelines, triggering by sensor, or cron jobs. For the sake of simplicity, we will go with the manual option. We can change or add trigger types later.
* Next, we will add the first task by clicking “**Add task”** in the **Task Group**. Tasks in the same Task group will be run in parallel.

  [![](https://substackcdn.com/image/fetch/$s_!MoF9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F080c46c9-44d2-416e-996e-d3a08737a676_474x196.png)](https://substackcdn.com/image/fetch/$s_!MoF9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F080c46c9-44d2-416e-996e-d3a08737a676_474x196.png)
* The first task is the Python task, which uses the defined Python integration. Orchestra will ask us to **“Choose an integration job.”** For this task, we will go with the “**Python-execute script.”**

  [![](https://substackcdn.com/image/fetch/$s_!xaSj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe1b4622f-9268-4672-ae72-49484b908010_486x130.png)](https://substackcdn.com/image/fetch/$s_!xaSj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe1b4622f-9268-4672-ae72-49484b908010_486x130.png)
* The task will run this [Python script](https://github.com/vutrinh274/dbt_example/blob/main/python/upload_to_s3.py) to upload data from the local to the S3 bucket. This task also needs some environment variables to work with the S3 client (e.g., AWS\_ACCESS\_KEY\_ID, etc**).** We enter some information for this task, and the values of the environment variables will be included in the section **“Environment Variables JSON.“** Orchestra will encode these variables when we save them.

[![](https://substackcdn.com/image/fetch/$s_!REEd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff88704f9-8f5a-4f6a-93a6-c5d8bd5dc46f_1144x686.png)](https://substackcdn.com/image/fetch/$s_!REEd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff88704f9-8f5a-4f6a-93a6-c5d8bd5dc46f_1144x686.png)

* Next, we set up a Snowflake task that runs queries to load the CSV from the S3 bucket. We click **“Add task“** in the next task group to set the dependencies between this task and the Python task. Before this task, [we had to set up a few things from Snowflake](https://docs.snowflake.com/en/user-guide/data-load-s3-config-storage-integration) so it could read the data in S3.
* We choose **Run Query (Snowflake)**

  [![](https://substackcdn.com/image/fetch/$s_!RLQi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd0600dbf-9c13-4da0-9f2f-3069557c89c6_534x162.png)](https://substackcdn.com/image/fetch/$s_!RLQi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd0600dbf-9c13-4da0-9f2f-3069557c89c6_534x162.png)
* Enter the task’s name, the SQL needed to be run, and the defined Snowflake connection. You can check the SQL script [here](https://github.com/vutrinh274/dbt_example/blob/main/snowflake/load_data_from_S3.sql).

  [![](https://substackcdn.com/image/fetch/$s_!ola5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F65bb92a0-e282-4bd5-bbd6-b2cec5ccd6e0_602x530.png)](https://substackcdn.com/image/fetch/$s_!ola5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F65bb92a0-e282-4bd5-bbd6-b2cec5ccd6e0_602x530.png)
* The two final tasks will be dbt tasks. The first one will run all staging models to clean the data loaded from the S3 bucket. The latter will run all curated models to transform data from staging into fact and dimension tables. For the dbt staging task, we choose the dbt Core command task.

  [![](https://substackcdn.com/image/fetch/$s_!4yrk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F580dad14-f460-4f4c-a05d-a36430867e04_594x158.png)](https://substackcdn.com/image/fetch/$s_!4yrk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F580dad14-f460-4f4c-a05d-a36430867e04_594x158.png)
* Then, we enter some required information for this task:

[![](https://substackcdn.com/image/fetch/$s_!f0zQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd41ec739-62dc-4aef-859a-e5279fde1304_1454x656.png)](https://substackcdn.com/image/fetch/$s_!f0zQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd41ec739-62dc-4aef-859a-e5279fde1304_1454x656.png)

* For the dbt curated task, we will configure it the same as the dbt staging task, except for the dbt commands, which need to be changed to `dbt build -s tag:curated`

And that’s it; we built a pipeline with Orchestra. To recap what we’ve done, you can check the video here:

### Run the pipeline

After having the pipeline’s tasks can be run in one of the following ways:

* Run based on the trigger configuration.
* Run the whole pipeline manually.

  [![](https://substackcdn.com/image/fetch/$s_!ovcL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbd6d08c8-e6d8-4c66-9033-8fe17db291ab_792x406.png)](https://substackcdn.com/image/fetch/$s_!ovcL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbd6d08c8-e6d8-4c66-9033-8fe17db291ab_792x406.png)
* Run a specific task.

  [![](https://substackcdn.com/image/fetch/$s_!b30R!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c40d0bd-619e-4cc7-9273-e076a96e26ba_792x272.png)](https://substackcdn.com/image/fetch/$s_!b30R!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c40d0bd-619e-4cc7-9273-e076a96e26ba_792x272.png)

### Observability

A very cool feature of Orchestra is that the platform will aggregate all the metadata for us.

After running the pipeline, Orchestra will display the status of that run for us; in the screenshot below, we can check the status of each task. If a task has any issues, we can detect them from here, fix them, and re-run the pipeline.

[![](https://substackcdn.com/image/fetch/$s_!nj98!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa8350531-4cee-4bff-a012-91dafa39c9e3_794x276.png)](https://substackcdn.com/image/fetch/$s_!nj98!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa8350531-4cee-4bff-a012-91dafa39c9e3_794x276.png)

Upon the pipeline finishes, we can click the **“Explore lineage“** button to explore its lineage.

[![](https://substackcdn.com/image/fetch/$s_!q11_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe3b91ae6-da31-4670-9ba5-24fd60b95872_812x266.png)](https://substackcdn.com/image/fetch/$s_!q11_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe3b91ae6-da31-4670-9ba5-24fd60b95872_812x266.png)

Orchestra also keeps the history of every pipeline’s run.

[![](https://substackcdn.com/image/fetch/$s_!6s5v!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3cbba241-282b-4b8d-bee9-795642bb031b_894x274.png)](https://substackcdn.com/image/fetch/$s_!6s5v!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3cbba241-282b-4b8d-bee9-795642bb031b_894x274.png)

In addition, Orchestra also collects metadata about our data assets. In our project, we made five Snowflake tables and eight dbt models.

For the native Snowflake tables, Orchestra can automatically collect the metadata; for the dbt models, we must explicitly allow Orchestra to do that. We can go back to the pipeline and edit the dbt tasks to let them collect the metadata:

We can check all the assets from the sidebar in the Data Assets section. For my pipeline, the data assets include metadata like Snowflake’s table structure (from the left), the number of assets, the asset coverage, the asset health, or the asset listing.

### Environment

When we build the pipeline, we want different development environments (e.g., dev, staging, and prod). Airflow requires us to set up multiple instances and multiple compute instances (e.g., two Spark clusters for the dev and prod environments).

Orchestra provides a simpler way; an environment is just a configuration. When defining a pipeline, users can add this configuration in each task to specify the different environments it can run.

For our project, imagine we need to separate the environment: “develop” and “production” for the Snowflake and dbt tasks. We want the same pipeline to run on two different Snowflake warehouses. To achieve this in Orchestra, we need:

* Two Snowflake and two dbt integrations are associated with the “develop” and “production” environments.
* Defining “develop” and “production” configuration environments in Orchestra UI, including associated integrations for each environment
* Use these configurations in desired tasks.

After this, whenever you run the pipeline or a single task, it will run in a specific environment—the default one or the one you choose. Orchestra will spin up separate resources and align these across environments behind the scene for us.

With this approach, we can control which tasks should be run in different environments and which are acceptable to run in one environment.

Orchestra also allows us to trigger the pipeline manually via GitHub workflow, which helps us integrate deeply with the CI/CD pipeline; let's say the current pipeline has two environments: “develop” and “production”:

* I want whenever I push dbt’s changes to the “develop” branch, it will run the Orchestra pipeline in the “develop” environment to validate the change.
* If there are no issues, I will merge changes to the “main“ branch and run the Orchestra pipeline in the “production” environment.

Orchestra provides the [orchestra-hq/run-pipeline](https://github.com/marketplace/actions/orchestra-run-pipeline) GitHub Action to let users integrate into the GitHub workflow. All we need is the [Orchestra API key and the pipeline’s ID](https://github.com/marketplace/actions/orchestra-run-pipeline) (from the URL).

For this project, I prepared [a GitHub workflow](https://github.com/vutrinh274/dbt_example/blob/main/.github/workflows/main.yml) as follows:

[![](https://substackcdn.com/image/fetch/$s_!DRHz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F040b49e8-8ed4-41b2-aafe-08d5bd597d5a_762x1056.png)](https://substackcdn.com/image/fetch/$s_!DRHz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F040b49e8-8ed4-41b2-aafe-08d5bd597d5a_762x1056.png)

The workflow has two jobs. The first will check if there is a pull request from the develop branch; if so, it will run my pipeline in the “develop“ environment. The latter will check if there is a push into the “main“ branch; if so, it will execute the pipeline in the “production“ environment.

[![](https://substackcdn.com/image/fetch/$s_!VbE5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F164aed37-a5b9-4bce-a98c-84f004473a50_888x458.png)](https://substackcdn.com/image/fetch/$s_!VbE5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F164aed37-a5b9-4bce-a98c-84f004473a50_888x458.png)

A very cool thing is that the output, when running from the pipeline, will be streamed to the UI when we observe the running workflow from GitHub.

### Version Control

The level of how Orchestrate can integrate with Git does not stop there. When we create the pipeline, Orchestra will record the pipeline definition in a YAML file. Whenever we make changes to the pipeline in the UI, it will show changes just like Git:

[![](https://substackcdn.com/image/fetch/$s_!hA6x!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F43714c6d-7b83-4acf-b88e-d009a9053129_1204x368.png)](https://substackcdn.com/image/fetch/$s_!hA6x!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F43714c6d-7b83-4acf-b88e-d009a9053129_1204x368.png)

Orchestra gives us the ability to version control this YAML file with Git. To do this for our project, we need to:

* Allow Orchestra to have access to your Repo. We go to Settings → User Git-control settings → Connect. It will ask if you allow Orchestra to have some specific permissions.
* Edit the pipeline, click the **Cogwheel** symbol, and choose **GitHub** for pipeline storage. We then fill in some Git’s information, click **update,** and click **save.**
* There will be a pull request to add the Orchestra pipeline’s YAML file to your repo.
* From now on, we can change the YAML file in the repo, and those changes will be reflected in the Orchestra pipeline UI.

In the video below, I configured the version control for the Pipeline YAML file in my repo and adjusted the file from my IDE to add another DBT task. Let's see how it works:

### Access Control

To implement access control, we created a Group with associated permissions. Orchestra lets us define permissions on high-level resources like account settings to low-level ones like pipelines or environments.

After that, we will add users to suitable groups. When in a group, users will be granted all the permissions associated with that group

---

## My thoughts

Orchestra is built for scale and makes building modern data workflows super easy. It provides a much more seamless way to build data pipelines, especially the “modern“ ones with dbt + cloud data warehouse; everything can be done on its intuitive UI/UX. The ability to collect, aggregate, and display metadata is also really valuable.

Regarding operating in different environments, Orchestra also does a very good job of abstracting the complexity of infrastructure management behind the scenes and only letting users operate on some configurations. The GitHub integration also impresses me a lot.

These are only some of my first impressions of Orchestra. There is a lot of flexibility and features I did not explore fully, like how to support multiple domains and effectively govern access to different resources in large enterprise organizations - these are very difficult using traditional workflow orchestration platforms.

Of course, all the tools will have pros and cons, and I believe that if I spend more time with Orchestra, I can spot some points that need to improve.

With this platform, it is sure that you can’t have the flexibility you got with Airflow, where you can write custom operators and construct the DAG in Python; in return, Orchestra will abstract all the complexity away, while you can build a robust pipeline from the UI or in code.

I think Orchestra is really worth your time [trying](https://www.getorchestra.io/pricing), especially if you have limited resources on your team or just want to spend time on business logic instead of maintaining an workflow orchestration system.

---

## Outro

Thank you for reading this far.

In the last 10 minutes, we have explored Orchestra and its motivation. We have also built a pipeline and tried out some very cool features from the platform. Finally, these are my naive thoughts on Orchestra.

Now, it’s time to say goodbye. See you in my next article.

---

## Reference

*[1] [Orchestra Documentation](https://docs.getorchestra.io/docs/quick-start/)*

*[2] [Orchestra website](https://getorchestra.io)*

*[3] [Product-Demos](https://www.youtube.com/channel/UC562ybrRtpDC9gNQTx6nYKg)*
