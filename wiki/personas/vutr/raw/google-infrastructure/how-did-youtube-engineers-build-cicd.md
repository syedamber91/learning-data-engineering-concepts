---
title: "How did YouTube engineers build CI/CD for data pipelines?"
channel: vutr
author: "Vu Trinh"
published: 2026-03-12
url: https://vutr.substack.com/p/how-did-youtube-engineers-build-cicd
paid: false
topics: ["Data Engineering", "Apache Spark", "Data Warehouse", "Data Quality"]
tags: [https, auto, image, good, substackcdn, fetch]
---

# How did YouTube engineers build CI/CD for data pipelines?

*CI/CD for data vs. code, and their frameworks to solve the problem at scale.*

> Source: [Open post](https://vutr.substack.com/p/how-did-youtube-engineers-build-cicd)

## Topics

[[data-engineering|Data Engineering]] · [[apache-spark|Apache Spark]] · [[data-warehouse|Data Warehouse]] · [[data-quality|Data Quality]]

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON**!*
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=189845738)

[![](https://substackcdn.com/image/fetch/$s_!U0f1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F61282fa0-3699-4729-8ad8-f42895c8b5dc_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!U0f1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F61282fa0-3699-4729-8ad8-f42895c8b5dc_2000x1429.png)

---

# Intro

Continuous Integration and Continuous Delivery (CI/CD) is a practice that automates the building, testing, and deployment of software changes, ensuring faster, less human intervention, and more reliable change deployment. If you don’t have it, you have to build the Docker, test, and deploy the changes manually. Just imagine how awful it is if your team has 5 members; you will have 5 different ways to handle that process.

CI/CD is a software engineering practice that has been around for a while.

[![](https://substackcdn.com/image/fetch/$s_!WV0_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3743a258-4d62-4da9-a78b-ae4c39dc479f_1112x454.png)](https://substackcdn.com/image/fetch/$s_!WV0_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3743a258-4d62-4da9-a78b-ae4c39dc479f_1112x454.png)

However, in data engineering, a branch of software engineering, CI/CD can be considered a new practice and still faces challenges without the “best-practice” solutions, given the fundamental differences between code and data.

At YouTube, where thousands of data pipelines run daily, their engineers face numerous challenges when building CI/CD to ship changes to those pipelines reliably. In a paper titled ["Unlocking the Power of CI/CD for Data Pipelines in Distributed Data Warehouses,"](https://www.vldb.org/pvldb/vol18/p4887-yang.pdf) they discussed these challenges and introduced their CI/CD framework to address them.

In this article, I will distill and simplify my understanding of the [paper](https://www.vldb.org/pvldb/vol18/p4887-yang.pdf). By the end, I hope you will have a better sense of the challenges of building CI/CD for data assets and might be able to apply some of Google’s insights to your own work.

---

# YouTube data warehouse

The YouTube data warehouse system must orchestrate thousands of data pipelines daily to ensure timely and reliable insights. These insights are used to build new features and improve user experience.

[![](https://substackcdn.com/image/fetch/$s_!NteQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc0935edd-1c4e-4a2d-9795-064280f8f259_888x536.png)](https://substackcdn.com/image/fetch/$s_!NteQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc0935edd-1c4e-4a2d-9795-064280f8f259_888x536.png)

The total data processed reaches multiple exabytes

> ***1 exabyte = 1,000,000 TB.***

Data in the system are time-partitioned (e.g., daily). YouTube version controls each partition independently, so they can update and roll back a partition without affecting other partitions.

To onboard a new data pipeline, the client can provide those inputs to the platform team:

* **Job Scheduling Configuration**: including when to run, the dependencies between upstream tables and the downstream materialized view, and the data-computing locality constraints (to minimize geographical data movement). The scheduling and resource allocation decisions are also guided by the data pipeline’s SLO constraints, such as the latency or throughput.

  [![](https://substackcdn.com/image/fetch/$s_!vp_c!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6dbeb738-80fa-43ce-ae75-503fc55afcf7_820x982.png)](https://substackcdn.com/image/fetch/$s_!vp_c!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6dbeb738-80fa-43ce-ae75-503fc55afcf7_820x982.png)
* **Data Management Configuration**: This controls how data is stored, accessed, and replicated.

  [![](https://substackcdn.com/image/fetch/$s_!4z_U!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F58160dcb-fdb9-423f-b4e4-9491a1ea7c9c_706x774.png)](https://substackcdn.com/image/fetch/$s_!4z_U!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F58160dcb-fdb9-423f-b4e4-9491a1ea7c9c_706x774.png)
* **Data Production Job Configurations**: detailed settings for each pipeline, as well as the computation resources and settings.

  [![](https://substackcdn.com/image/fetch/$s_!19ft!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb7d91fcd-86ac-46c9-a389-b5007c3d687e_432x476.png)](https://substackcdn.com/image/fetch/$s_!19ft!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb7d91fcd-86ac-46c9-a389-b5007c3d687e_432x476.png)
* **Business Logic Implementation**: The data transformation logic in SQL or other languages.

  [![](https://substackcdn.com/image/fetch/$s_!r5lN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa06c4ee8-44c4-4731-bd01-acd6e4f73522_656x778.png)](https://substackcdn.com/image/fetch/$s_!r5lN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa06c4ee8-44c4-4731-bd01-acd6e4f73522_656x778.png)

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=189845738)

---

# CI/CD Challenges

Given the complexity of thousands of data pipelines, they encounter some enormous challenges with the CI/CD:

* **The complexity of data**: many aspects of the data must be validated, including volume, variety, schema, semantics, quality, and dependencies between data assets, among many others. The expectation of how good the data will change as the business evolves. This makes it hard to define expected results for the test: it must be “big” enough in some cases, or its schema might need to be updated. In addition, when working with data, security must be the priority, given that YouTube handles information from billions of users worldwide.

  [![](https://substackcdn.com/image/fetch/$s_!k7Dc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3686e395-6e42-4579-b3d2-cb343a58c7cf_580x538.png)](https://substackcdn.com/image/fetch/$s_!k7Dc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3686e395-6e42-4579-b3d2-cb343a58c7cf_580x538.png)
* **Hard to replicate the infrastructure for testing**: a production data pipeline involves many components: the sources, the distributed systems, the cloud services, and on-demand hardware. Running the test pipeline under the same conditions as the production pipeline will ensure that their engineers can capture “weird“ things before shipping the changes into production. However, mirroring the production environment is not easy, given the scale of YouTube's data systems; simply duplicating everything would be super expensive.

  [![](https://substackcdn.com/image/fetch/$s_!L0tY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4ad7f42b-2db4-4371-bf40-89c1706a49e9_1386x714.png)](https://substackcdn.com/image/fetch/$s_!L0tY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4ad7f42b-2db4-4371-bf40-89c1706a49e9_1386x714.png)
* **Deployment Bottleneck**: Things need to be set up for a data CI/CD pipeline, which will be more than a Docker image, including the infrastructure for testing or the data sources.

  [![](https://substackcdn.com/image/fetch/$s_!he74!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9a22c88c-740b-4a39-a8aa-5a8693452659_852x958.png)](https://substackcdn.com/image/fetch/$s_!he74!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9a22c88c-740b-4a39-a8aa-5a8693452659_852x958.png)
* **Observability**: With the data scale at YouTube, things happen in a distributed manner. They need observability tools to observe and identify problems seamlessly in the distributed environment

  [![](https://substackcdn.com/image/fetch/$s_!0Bj0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6bdde51d-5326-48c5-94c0-d1a2abe53701_798x470.png)](https://substackcdn.com/image/fetch/$s_!0Bj0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6bdde51d-5326-48c5-94c0-d1a2abe53701_798x470.png)
* **Collaboration**: Pipelines can be built by different teams. A pipeline can consume data produced by other pipelines. The CI/CD must ensure changes don’t break the end-to-end data flow. This involves improving collaboration between teams to share knowledge of their own data pipeline.

  [![](https://substackcdn.com/image/fetch/$s_!Kglo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff0666ea6-a55e-4f93-a6f0-4eba6b5ba05e_1350x996.png)](https://substackcdn.com/image/fetch/$s_!Kglo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff0666ea6-a55e-4f93-a6f0-4eba6b5ba05e_1350x996.png)

YouTube notes that these challenges arise from fundamental differences between Traditional Software CI and Data Pipeline CI. Here is their comparison:

[![](https://substackcdn.com/image/fetch/$s_!zsde!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2d5da801-2a70-42ad-8832-a11b91241cb1_1174x1038.png)](https://substackcdn.com/image/fetch/$s_!zsde!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2d5da801-2a70-42ad-8832-a11b91241cb1_1174x1038.png)

Table 1: Traditional CI vs CI for data pipelines. [Source](https://www.vldb.org/pvldb/vol18/p4887-yang.pdf)

---

# YouTube CI/CD framework

So, YouTube built a robust CI/CD architecture with the following components:

* **Test Configurations**: This module lets clients configure their data pipeline testing. It enables testing a subgraph of a data pipeline in isolation.

  [![](https://substackcdn.com/image/fetch/$s_!Jb3X!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0d687712-f767-4e8a-946a-fe3e2481b802_652x508.png)](https://substackcdn.com/image/fetch/$s_!Jb3X!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0d687712-f767-4e8a-946a-fe3e2481b802_652x508.png)

  It also parameterizes the experimental conditions and leverages the production setup wherever possible. The module also supports integration of utilities such as data sampling, data diffs, or data quality checks.
* **Configuration Rewriter**: This component is responsible for reproducible testing by rewriting the production configurations. It uses the pipeline’s dependency graph to rewrite the subgraph configuration so that the subgraph can be tested in isolation.

  [![](https://substackcdn.com/image/fetch/$s_!JgRZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcd84b50e-fcbc-472b-99c2-6e496f499ac4_714x334.png)](https://substackcdn.com/image/fetch/$s_!JgRZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcd84b50e-fcbc-472b-99c2-6e496f499ac4_714x334.png)

  Thanks to an understanding of the dependency, the module can ensure correctness and minimize disruption to the production environment. By reusing the production configurations (after rewriting), the team reduces setup overhead.
* **Test Data Management**: This component is responsible for the test data. It masks sensitive data, generates synthetic data, and version controls the test data to enable test reproducibility and analysis.

  [![](https://substackcdn.com/image/fetch/$s_!RLug!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbfdb746e-449a-4c63-a800-1c4909afdbe3_1430x376.png)](https://substackcdn.com/image/fetch/$s_!RLug!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbfdb746e-449a-4c63-a800-1c4909afdbe3_1430x376.png)
* **Controller Module**: This manages the entire test process, from provisioning the test environments, ingesting test data, scheduling tests, analyzing the output, checking data quality, to monitoring and alerting.

  [![](https://substackcdn.com/image/fetch/$s_!MvVQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F64aaa272-726f-44e7-9b0a-7471d0f09c67_594x660.png)](https://substackcdn.com/image/fetch/$s_!MvVQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F64aaa272-726f-44e7-9b0a-7471d0f09c67_594x660.png)
* **Diagnostics and Reporting**: Tools for extracting insights, reporting, or root cause analysis.

  [![](https://substackcdn.com/image/fetch/$s_!A-qt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff01bd3d4-6b0c-4228-8fba-7cee8a934ce3_364x358.png)](https://substackcdn.com/image/fetch/$s_!A-qt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff01bd3d4-6b0c-4228-8fba-7cee8a934ce3_364x358.png)

This CI/CD framework helps YouTube deliver the following capabilities to the data warehouse system.

First is the automated data quality check. Those checks are generated by leveraging data properties, such as types and constraints. The goal is to increase test coverage and reduce the rule execution overhead.

[![](https://substackcdn.com/image/fetch/$s_!aXFV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F01793083-1e98-418d-9053-daf70e980866_1434x500.png)](https://substackcdn.com/image/fetch/$s_!aXFV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F01793083-1e98-418d-9053-daf70e980866_1434x500.png)

To retrieve the data properties, the system performs data profiling as part of the CI process. The framework also includes anomaly-detection algorithms to identify unexpected data patterns.

The second is the generation of production-aligned testing environments. As mentioned in the “Configuration Rewriter“, each test will have an isolated environment by cloning and rewriting production job configurations.

[![](https://substackcdn.com/image/fetch/$s_!3-iM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa19af84-4452-49c3-b7b6-f14a15e2287e_1164x506.png)](https://substackcdn.com/image/fetch/$s_!3-iM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa19af84-4452-49c3-b7b6-f14a15e2287e_1164x506.png)

By referencing the dependency graph of a data pipeline, the rewriting process promises to adjust only required configurations. For stateful components, such as the database, the controller module will provision test instances and ingest test data into them. The test data management component ensures the quality and relevance of the test data.

The third is efficient and cost-effective testing. Techniques such as data sampling help reduce the volume of test data. The CI/CD framework allows user-input sampling logic, as the teams that own those pipelines are best positioned to understand their data distribution.

[![](https://substackcdn.com/image/fetch/$s_!cbHa!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F698e32cf-3334-4320-b74b-4389cfc45663_912x718.png)](https://substackcdn.com/image/fetch/$s_!cbHa!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F698e32cf-3334-4320-b74b-4389cfc45663_912x718.png)

The fourth is collaboration and knowledge sharing. There is a component that was not mentioned earlier: the metadata hub, which centralizes knowledge about a data pipeline, including data dependencies, data quality metrics, and production configurations. The hub provides APIs that allow users to retrieve and edit metadata.

[![](https://substackcdn.com/image/fetch/$s_!18Mu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7b3e8dc0-3d64-42e6-87e4-f73c25e9a04b_940x726.png)](https://substackcdn.com/image/fetch/$s_!18Mu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7b3e8dc0-3d64-42e6-87e4-f73c25e9a04b_940x726.png)

Final is the production environment integration. The test process can access production capabilities (in isolation), such as the UI or monitoring alerts. This helps the test process be more effective and closer to the production environment.

[![](https://substackcdn.com/image/fetch/$s_!INe6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0dd6f4ab-bf25-4469-982d-618052ac1bff_644x400.png)](https://substackcdn.com/image/fetch/$s_!INe6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0dd6f4ab-bf25-4469-982d-618052ac1bff_644x400.png)

---

# The results

[![](https://substackcdn.com/image/fetch/$s_!U7IM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb8622f37-6490-4b84-a917-37628681eb6c_590x566.png)](https://substackcdn.com/image/fetch/$s_!U7IM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb8622f37-6490-4b84-a917-37628681eb6c_590x566.png)

* A team can reduce the data volume by 99.9% using the sampling framework, while preserving the data distributions. This reduces testing time from more than a day to nearly an hour.
* If teams leverage the framework to generate the testing environments, they can reduce the time to investigate the integrations (between components) by 50%.
* Schema changes were released in weeks instead of months, thanks to the dependency awareness and automated data quality checks. The framework will use the dependencies to pinpoint all downstream components affected.
* Reusing production configurations reduces inconsistency and infrastructure provision overhead and improves the reproducibility of the tests.
* The overall data quality of the whole data warehouse system improves.
* Collaboration enhancement significantly improves the data integrity and development velocity.

---

# Principles

Besides the framework, YouTube also shares their principles for designing its CI processes.

## Data

Data is more dynamic than code. Thus, data quality must be guaranteed by a set of validation techniques:

[![](https://substackcdn.com/image/fetch/$s_!eRAz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9532e2bb-4a89-41ca-be67-b5dd9cc4aa1f_906x662.png)](https://substackcdn.com/image/fetch/$s_!eRAz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9532e2bb-4a89-41ca-be67-b5dd9cc4aa1f_906x662.png)

* Schema validation is not only about the column names and types. The system must validate the constraints and relationships between data assets.
* SQL assertions (e.g., count null rows) in the pipeline.
* Anomaly detection methods, such as statistical or machine learning, to identify unexpected trends and patterns. They are extremely hard to detect with the naked eye or with binary validations.
* Data distributions and properties can change over time. Regular profiling to understand your data.
* Using statistical methods, such as hypothesis testing, to ensure data quality changes are statistically significant.

## Testing

Unit test is crucial, but it’s not enough:

[![](https://substackcdn.com/image/fetch/$s_!BrDO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5f51abc7-da7b-438d-82f2-8eb37b61b8d3_930x562.png)](https://substackcdn.com/image/fetch/$s_!BrDO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5f51abc7-da7b-438d-82f2-8eb37b61b8d3_930x562.png)

* Data diff test for discrepancies between two datasets.
* Test for integrations between components in a pipeline.
* End-to-end test to stimulate a real-world scenario, from data ingestion, data processing, to data consumption.

## Deployment process

[![](https://substackcdn.com/image/fetch/$s_!MPjf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F42e4c06a-f3e3-43ad-ba0c-c2755a52a42f_1014x680.png)](https://substackcdn.com/image/fetch/$s_!MPjf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F42e4c06a-f3e3-43ad-ba0c-c2755a52a42f_1014x680.png)

Automation as much as possible by leveraging Infrastructure as Code (IaC) for test infrastructure provision and by centralizing the data sources, settings, pipeline parameters, and environment variables. Using dependency management tools (e.g., uv or pip in Python) to ensure consistency between environments.

## Observability

CI/CD is also a product that requires careful observability through tracing, data lineage tracking, monitoring, logging, analysis, alerting, and anomaly detection.

## Collaboration

The more teams involved in building the data pipeline, the more complex the CI/CD is. YouTube encourages us to have a mechanism to share understanding and distributed ownership across teams.

## Test Data Management

[![](https://substackcdn.com/image/fetch/$s_!QUkn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc04c115b-48aa-422e-a29b-9b791c90f645_436x622.png)](https://substackcdn.com/image/fetch/$s_!QUkn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc04c115b-48aa-422e-a29b-9b791c90f645_436x622.png)

Test data is crucial in every scenario. It determines whether your test catches all possible errors, bugs, or other unexpected things before releasing to production. Test data for data pipeline testing even needs more effort to manage:

* Evolving the test data to align with the data’s schema changes and distributions.
* Masking sensitive information.
* Synthetic data generation to create realistic test data
* Considering data sampling to reduce the test volume while preserving the data distribution and characteristics.
* Version controlling test data for test reproducibility and traceability.

---

# Outro

In this article, I share my learning after reading the paper "Unlocking the Power of CI/CD for Data Pipelines in Distributed Data Warehouses" by YouTube engineers. We’ve learned about the scale of the YouTube data warehouse system, the challenges of their CI/CD process due to the dynamic nature of the data, and the organizational complexity. From there, we move on to their CI/CD framework to solve the problems and their principal guidelines, which we can apply to our data CI/CD framework.

Thank you for reading this far. See you in my next articles.

---

# Reference

*[1] Hongtao Yang, Zhichen Xu, Sergey Yudin, Andrew Davidson, [Unlocking the Power of CI/CD for Data Pipelines in Distributed Data Warehouses](https://www.vldb.org/pvldb/vol18/p4887-yang.pdf) (2025)*
