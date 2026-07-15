---
title: "How did Airbnb build their semantic layer?"
channel: vutr
author: "Vu Trinh"
published: 2025-03-13
url: https://vutr.substack.com/p/how-did-airbnb-build-their-semantic
paid: false
topics: ["Data Engineering", "Apache Airflow", "Apache Spark", "Data Warehouse", "Orchestration", "Data Quality"]
tags: [https, auto, minerva, image, airbnb, substackcdn]
---

# How did Airbnb build their semantic layer?

*Minerva, the Airbnb metric platform*

> Source: [Open post](https://vutr.substack.com/p/how-did-airbnb-build-their-semantic)

## Topics

[[data-engineering|Data Engineering]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[data-warehouse|Data Warehouse]] · [[orchestration|Orchestration]] · [[data-quality|Data Quality]]

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=158825951)

[![](https://substackcdn.com/image/fetch/$s_!AGhi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5a5d0850-6a8e-4267-bb9b-bfedf491721e_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!AGhi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5a5d0850-6a8e-4267-bb9b-bfedf491721e_2000x1429.png)

Image created by the author.

---

## Intro

Today, we will explore how Airbnb builds and serves its semantic layer internally and what we can learn from it. More correctly, Airbnb did not only build a layer that [“](https://www.ibm.com/think/topics/semantic-layer)*[simplifies interactions between complex data storage systems and business users.](https://www.ibm.com/think/topics/semantic-layer)*[“](https://www.ibm.com/think/topics/semantic-layer) They create a complete platform.

---

## Motivation

In 2010, Airbnb had only one data analyst. His laptop was Airbnb data warehouse. He often ran queries right on production databases, and Airbnb.com was down for some time because of the heavy queries.

[![](https://substackcdn.com/image/fetch/$s_!pXa7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa73cad80-f143-4b45-a033-aa7999a9ed97_532x320.png)](https://substackcdn.com/image/fetch/$s_!pXa7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa73cad80-f143-4b45-a033-aa7999a9ed97_532x320.png)

Image created by the author.

In the early 2010s, they hired more data scientists, and data kept growing. They upgraded their data infrastructure and built their own data orchestration tool, Airflow, with later open source.

[![](https://substackcdn.com/image/fetch/$s_!TrTB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2fb011b4-fb23-4c26-baa5-9a599c4f59d7_804x568.png)](https://substackcdn.com/image/fetch/$s_!TrTB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2fb011b4-fb23-4c26-baa5-9a599c4f59d7_804x568.png)

Their upgraded architecture. Image created by the author

Their top priority was to build a set of tables called **core\_data.** These tables set the foundation for many data demands at Airbnb:

* Airbnb’s experimentation platform for streamlining the A/B testing processes.
* [Dataportal](https://medium.com/airbnb-engineering/democratizing-data-at-airbnb-852d76c51770) — Airbnb's internal data catalog organizes and documents data assets.
* Interactively data exploration with Apache Superset
* [Data University](https://medium.com/airbnb-engineering/how-airbnb-democratizes-data-science-with-data-university-3eccc71e073a) — a program that teaches non-data scientists valuable skills to democratize data analysis at Airbnb.

However, the growth came with challenges:

* More users wanted to consume core\_data, so they created many tables on top of it. There was no way to tell if a table with the exact requirement existed.

  [![](https://substackcdn.com/image/fetch/$s_!ro2Z!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5ade169a-b90f-4c35-8564-a3eff150a2ae_532x390.png)](https://substackcdn.com/image/fetch/$s_!ro2Z!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5ade169a-b90f-4c35-8564-a3eff150a2ae_532x390.png)

  Image created by the author.
* Because of the complexity of the growing warehouse, Airbnb found it challenging to track data. Data users could spend many hours debugging the data discrepancies.

  [![](https://substackcdn.com/image/fetch/$s_!hIKQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8a827e55-201d-488d-b23c-f0dfde28c9bc_1002x322.png)](https://substackcdn.com/image/fetch/$s_!hIKQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8a827e55-201d-488d-b23c-f0dfde28c9bc_1002x322.png)

  Image created by the author.
* For data consumption, decision-makers complained that different teams reported different numbers for simple business questions. As a result, business users and even data scientists lost trust in the data.

  [![](https://substackcdn.com/image/fetch/$s_!QFR7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F831d263a-e59d-4643-bea5-a8795d0d19a2_470x338.png)](https://substackcdn.com/image/fetch/$s_!QFR7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F831d263a-e59d-4643-bea5-a8795d0d19a2_470x338.png)

  Image created by the author.

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=158825951)

---

## Airbnb Minerva

They revamped the data warehouse to improve data quality.

First, their data engineering team rebuilt key business data models, resulting in lean tables that eliminate redundant joins. These tables served as the new foundation for the analytics.

[![](https://substackcdn.com/image/fetch/$s_!UjzG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F93b2e7c6-973e-4165-82eb-55c933c1a7ed_370x486.png)](https://substackcdn.com/image/fetch/$s_!UjzG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F93b2e7c6-973e-4165-82eb-55c933c1a7ed_370x486.png)

Image created by the author.

That still was not enough.

They needed to join these tables to extract insight, backfill data whenever logic changes, or present the data consistently and correctly in many different consumption tools.

Airbnb built Minerva for these purposes.

Minerva took fact and dimension tables as inputs, performed data denormalization, and served the aggregated data to downstream applications. Airbnb hoped the Minerva API would close the gap between upstream data and downstream consumption.

[![](https://substackcdn.com/image/fetch/$s_!zod-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5297e02f-6bb2-49f2-8542-a402866085b6_1296x398.png)](https://substackcdn.com/image/fetch/$s_!zod-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5297e02f-6bb2-49f2-8542-a402866085b6_1296x398.png)

Image created by the author.

At the time of Airbnb’s sharing, Minerva contained more than 12,000 metrics and 4,000 dimensions, with 200+ data producers across different functions and teams.

---

## Architecture

Airbnb built Minerva on top of open-source projects:

[![](https://substackcdn.com/image/fetch/$s_!TfL3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcf146ebe-8c5d-4cfe-9258-7d017fc099e0_392x338.png)](https://substackcdn.com/image/fetch/$s_!TfL3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcf146ebe-8c5d-4cfe-9258-7d017fc099e0_392x338.png)

Image created by the author.

* Airflow for workflow orchestration.
* Apache Hive and Apache Spark for the compute engine.
* Presto and Apache Druid for serving.

For a metric, Minerva has components to cover its whole life cycle:

* Minerva defines metrics, dimensions, and metadata in a centralized Github repository. Anyone at Airbnb with proper permissions can update these definitions.
* It has a development flow for code review, static validation, and test runs.
* It executes data aggregation/denormalization by resue data assets and intermediate joined results.
* Minerva has a robust computation flow that canautomatically retry after job failures, plus the built-in data-quality checks.
* It exposes a unified data API to serve metrics and metadata.
* Because the Minervaversion controls data definitions (via Git), it can detect and track changes and then execute data backfilling.
* Its data management features include cost attribution, GDPR-based deletion, or data access control.
* For data retention, Minerva supports clean-up of data based on usage; infrequently used datasets can be deleted to save cost.

---

## Design principle

Airbnb built Minerva to be:

* **Standardized**: Data is defined in a single place. It must serve as a single entry point for anyone searching for definitions.
* **Declarative:** Users define the output they want (like SQL). Minerva will handle everything from calculating metrics to storing and serving.
* **Scalable**: Minerva must be scalable to support Airbnb’s internal data demands.
* **Consistent**: The data is always consistent. If the user changes the definitions, Minerva must perform data backfill and keep the data up-to-date.
* **Highly available**: Dataset replacement must be handled with minimal impact on data consumption.
* **Well-tested**: Users can prototype and validate their changes before they are merged into production.

### **Standardized**

Minerva is focused on metrics and dimensions instead of tables and columns like databases.

When a metric is defined in Minerva, users must provide necessary metadata, such as ownership, lineage, or metric description. Before Minerva, Airbnb managed metadata inefficiently as definitions scattered across various business intelligence tools.

Regarding version control in Minerva, they treat all definitions as code that must go through a review process before merging to production, just like code review.

[![](https://substackcdn.com/image/fetch/$s_!3ahR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee832728-d4fe-4615-bef3-93183053891a_500x194.png)](https://substackcdn.com/image/fetch/$s_!3ahR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee832728-d4fe-4615-bef3-93183053891a_500x194.png)

Image created by the author.

Minerva’s configuration system cores are event and dimension sources, corresponding to fact tables and dimension tables in the data warehouse:

[![](https://substackcdn.com/image/fetch/$s_!xLNP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe35058b-e2a0-437a-bc76-a62cf8bf7a6a_364x270.png)](https://substackcdn.com/image/fetch/$s_!xLNP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe35058b-e2a0-437a-bc76-a62cf8bf7a6a_364x270.png)

Image created by the author.

* Event sources define the atomic events which are used to calculate metrics.
* Dimension sources contain attributes that can be used with the metrics.

### **Declarative**

[![](https://substackcdn.com/image/fetch/$s_!9W9C!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ac7d462-4571-4b25-aa26-f700dc19c597_1400x606.png)](https://substackcdn.com/image/fetch/$s_!9W9C!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ac7d462-4571-4b25-aa26-f700dc19c597_1400x606.png)

The workflow of extracting insight before Minerva has a lot of steps (Left). Minerva saves users a lot of time (Right). [How Airbnb Standardized Metric Computation at Scale](https://medium.com/airbnb-engineering/airbnb-metric-computation-with-minerva-part-2-9afe6695b486) (2021)

One of Minerva’s promises is to simplify the time-consuming workflow so that users can quickly turn data into insights. Users can define a dimension set, an analysis-friendly dataset created from Minerva metrics and dimensions. Unlike ad-hoc datasets, dimension sets have several advantages:

* Users define what they want. Minerva abstracts all the technical implementation details and complexity of creating it from the users.
* Dimension sets can benefit from Minerva’s existing features.
* Minerva can store and optimize these dimension sets to reduce query times.
* Minerva can reuse dimension sets, which help reduce dataset duplication.

### **Scalable**

Minerva was serving 5,000+ datasets across hundreds of users and 80+ teams.

To ensure it can scale, Airbnb built Minerva’s computation with the DRY (Do not Repeat Yourself) principle. They tried to reuse materialized data as much as possible to reduce wasted computing resources.

The computational flow has several stages:

[![](https://substackcdn.com/image/fetch/$s_!Hvc2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb1ad2314-3603-4207-813c-d1477a2fe59d_1228x306.png)](https://substackcdn.com/image/fetch/$s_!Hvc2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb1ad2314-3603-4207-813c-d1477a2fe59d_1228x306.png)

Image created by the author.

* **Ingestion Stage**: Minerva sensors are triggered when new data is added to the table’s partitions. The latest data is then ingested into Minerva.
* **Data Check Stage**: This stage ensures that upstream data is “right. “ For example, a field should not be empty, or primary keys should be unique.
* **Join Stage**: Minerva executes the joins based on join keys to generate dimension sets. Minerva computes the same calculations (e.g., same city dimension) that happen on different dimension sets using the same logic on the same source tables. This ensures consistent dataset computation at scale.
* **Post-processing and serving stage**: Minerva further aggregates outputs for downstream consumption. It can optionally optimize data end-user query performance.

In addition, Airbnb included features to make Minerva operate efficiently. Some features are self-healing and automated backfilling.

Minerva tries to be data-aware. It checks for missing data for every job. If missing data is identified, it is included in the current run. This means a single run can have a data range changed dynamically (e.g., 3 days → 4 days of data). Users don’t need to reset tasks manually.

For the backfilling, if the backfill window is long (e.g., several months), it may generate an expensive query. If they split the backfill window into smaller ones, it will be too slow for a large initial window. To solve this, Airbnb introduced the batch backfill for Minerva.

[![](https://substackcdn.com/image/fetch/$s_!VfqX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc26fab7e-42c9-4607-bd17-0632f293b540_466x390.png)](https://substackcdn.com/image/fetch/$s_!VfqX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc26fab7e-42c9-4607-bd17-0632f293b540_466x390.png)

Image created by the author.

They still split the backfill window into smaller ones based on the scalability of that dataset. For example, a one-year window would be divided into 12 1-month windows. Then, they run these 12 jobs in parallel.

### Consistent

Internal users frequently change Minerva's definitions. Airbnb introduced a data version to ensure that Minerva datasets are consistent and up-to-date.

The data version is a hash of all the essential fields specified in the definitions (e.g., data source). When users change any field used for the hashing, the data version is automatically updated.

[![](https://substackcdn.com/image/fetch/$s_!Migc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F320eeca1-73fe-46d9-8390-3e89f2704146_528x332.png)](https://substackcdn.com/image/fetch/$s_!Migc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F320eeca1-73fe-46d9-8390-3e89f2704146_528x332.png)

Image created by the author.

Each dataset has a data version, which makes Minerva automatically create and backfill a new dataset. This approach ensures that upstream changes are propagated to all downstream datasets, and no Minerva dataset will diverge from the source of truth.

### **Highly Available**

Airbnb observed that backfills often could not catch up with user changes when updates affect many datasets. Given that Minerva promises to provide consistent and up-to-date data, a frequently changing dataset could result in backfill forever and cause data downtime.

Airbnb deployed a parallel computation environment called the Staging environment. The Staging environment replicates the Production environment. They will perform data backfilling in the staging before publishing it on the Production. The flow for the Staging environment is as follows:

[![](https://substackcdn.com/image/fetch/$s_!L24r!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5db21156-a49d-4b73-acac-b58c84f6c5ba_708x396.png)](https://substackcdn.com/image/fetch/$s_!L24r!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5db21156-a49d-4b73-acac-b58c84f6c5ba_708x396.png)

Image created by the author.

1. Users developed and tested changes in the local environment.
2. They merge changes to the Staging environment.
3. The Staging environment loads the Staging configurations, retrieves any necessary Production configurations if needed, and starts backfilling modified datasets.
4. The Staging changes are merged into Production when the backfill is done.

### **Well-Tested**

To help users validate data correctness, Minerva has a tool that reads from production but writes to a sandbox environment. The tool generates sample data on top of the user’s local modifications, allowing users to validate their changes.

The tool shows the step-by-step computation that Minerva follows to generate the output. This feature helps users debug issues just like they are running the logic. Finally, it also allows users to configure date ranges to limit the test data size, which helps them save a lot of time waiting for the test to finish.

---

## Consumption

The Minerva teams partnered with other internal teams to create an ecosystem around Minerva:

* Data catalog: They index all Minerva metrics and dimensions in Airbnb’s Dataportal. When a user searches for a metric, the Dataportal shows the result from Minerva.

* Dataportal also offers a data exploration feature called Metric Explorer. Users can see metric trends with additional slicing and drill-down options, such as Group By and Filter. Users who want to dig deeper can switch to Superset to perform more advanced analytics.
* They migrate the A/B test platform’s proprietary metric repo to Minerva, which helps achieve consistency across experimentation and analytics.
* To enable executive reporting, they built a reporting framework that turns a set of user-specified Minerva metrics and dimensions into aggregated metric time series.
* Minerva exposes API for Airbnb’s R and Python clients. This lets data scientists query Minerva data in a notebook environment. Data scientists can now have metric calculation results exactly like those of other tools such as Metric Explorer, saving them lots of time when investigating data discrepancies.

---

## Outro

Thank you for reading this far.

In this article, we explore the motivation behind the need for the semantic platform from Airbnb, the platform architecture and design principle, and finally, how Minerva can serve downstream consumption.

Now it’s time to say goodbye. See you in my following articles.

---

## Reference

*[1] The Airbnb Tech Blog, [How Airbnb Achieved Metric Consistency at Scale](https://medium.com/airbnb-engineering/how-airbnb-achieved-metric-consistency-at-scale-f23cc53dea70) (2021)*

*[2] The Airbnb Tech Blog, [How Airbnb Standardized Metric Computation at Scale](https://medium.com/airbnb-engineering/airbnb-metric-computation-with-minerva-part-2-9afe6695b486) (2021)*
