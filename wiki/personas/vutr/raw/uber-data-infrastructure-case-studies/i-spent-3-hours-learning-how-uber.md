---
title: "I spent 3 hours learning how Uber manages data quality."
channel: vutr
author: "Vu Trinh"
published: 2024-10-26
url: https://vutr.substack.com/p/i-spent-3-hours-learning-how-uber
paid: false
topics: ["Apache Spark", "Data Modeling", "Data Quality", "ETL"]
tags: [https, auto, quality, uber, image, test]
---

# I spent 3 hours learning how Uber manages data quality.

*From the standard to the data quality platform*

> Source: [Open post](https://vutr.substack.com/p/i-spent-3-hours-learning-how-uber)

## Topics

[[apache-spark|Apache Spark]] · [[data-modeling|Data Modeling]] · [[data-quality|Data Quality]] · [[etl|ETL]]

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=150666259)

[![](https://substackcdn.com/image/fetch/$s_!n7qe!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F92606d6b-4276-497a-a756-97c681b42820_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!n7qe!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F92606d6b-4276-497a-a756-97c681b42820_2000x1429.png)

Image created by the author.

---

## Intro

If you've been following my writing for a while, you might have noticed that I’ve spent a lot of time covering the technical aspects of OLAP systems, table formats, and how big companies manage their data infrastructure.

I’ve mainly focused on the "engineering" side and seemed to have overlooked the "data"—the most crucial part for anyone who works with it daily!

Thus, I’ve decided to dedicate more time to learning and writing about the "data" itself: data modeling, data management, data quality, and more.

This article will be the first you’ll read about "data" on my site.

(Hopefully, it won’t be the last!)

Today, you and I will dive into how Uber manages their data quality.

---

## Overview

Uber extensively leverages data to provide efficient and reliable transportation worldwide, supported by hundreds of services, machine learning models, and thousands of datasets.

Being a data-driven company means that poor data can significantly impact operations—something Uber understands better than most.

[![](https://substackcdn.com/image/fetch/$s_!GmMb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcb635b76-5990-4819-9cfe-2722bfb1e51e_1688x472.png)](https://substackcdn.com/image/fetch/$s_!GmMb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcb635b76-5990-4819-9cfe-2722bfb1e51e_1688x472.png)

Image created by the author.

To address this, they built a consolidated data quality platform that monitors, automatically detects, and manages data quality issues. This platform supports over 2,000 datasets, detecting around 90% of data quality incidents.

The following sections explore how Uber established data quality standards and built an integrated workflow to achieve operational excellence.

---

## **Challenges**

To address data quality issues at Uber's data scale, they had to overcome the following limitations:

[![](https://substackcdn.com/image/fetch/$s_!wTov!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc96b1958-4a97-4748-a6fb-9201fbaa8267_542x500.png)](https://substackcdn.com/image/fetch/$s_!wTov!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc96b1958-4a97-4748-a6fb-9201fbaa8267_542x500.png)

Image created by the author.

* Lack of standardized data quality measurements across teams.
* Creating tests for datasets involved significant manual effort.
* The incident management process required improvement.
* Integration with other data platforms was necessary to provide a centralized experience for all of Uber's internal data users.
* A standardized, automated method for creating alerts was needed.

---

## **Data Quality Standardization**

Here are some common data issues when Uber tried to collect feedback from internal data users and analyze significant data incidents in the past:

* Data arriving late after
* Data are missing or duplicated entries
* Data discrepancies between different data centers
* Data values are incorrect.

Following these insights, they define the below test categories, which expect to cover all data quality aspects:

[![](https://substackcdn.com/image/fetch/$s_!i9h9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fea39d935-fe8a-43f2-99c2-371e89d13b64_486x436.png)](https://substackcdn.com/image/fetch/$s_!i9h9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fea39d935-fe8a-43f2-99c2-371e89d13b64_486x436.png)

Image created by the author.

* **Freshness:** the delay after which data is 99.9% complete

  + *Assertion pass if current\_timestamp – **latest\_timestamp where data is 99.9%** **complete** < freshness SLA*
* **Completeness:** the row completeness percentage.

  + *Assertion pass if downstream\_row\_count / upstream\_row\_count > completeness SLA*
* **Duplicates:** the percentage of rows that have duplicate primary keys

  + *Assertion pass if (1 – primary\_key\_count ) / total\_row\_count < duplicates SLA*
* **Cross-datacenter Consistency:** the percentage of data loss by comparing a dataset copy in the current data center with the copy in the other data center.

  + *Assertion pass if min(row\_count, row\_count\_other\_copy) / row\_count > consistency SLA*
* **Others:** any test with complicated checks based on business logic

  + *Based on User-defined tests*

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=150666259)

---

## **Data Quality Platform Architecture**

From a 10,000-foot view, Uber's data quality architecture consists of the following components:

[![](https://substackcdn.com/image/fetch/$s_!S2UN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9a2e8c2b-96ab-470a-bbc3-0d76c6f392e9_804x518.png)](https://substackcdn.com/image/fetch/$s_!S2UN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9a2e8c2b-96ab-470a-bbc3-0d76c6f392e9_804x518.png)

Image created by the author.

* Test Execution Engine
* Test Generator
* Alert Generator
* Incident Manager
* Platform’s success metrics
* Consumption Tools

The Test Execution Engine runs onboarded tests on schedules or on-demand using various query engines, with the results stored in databases. The other components leverage this engine to cover the entire data quality lifecycle.

### **Test Generator**

[![](https://substackcdn.com/image/fetch/$s_!fpnc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9e6e02a0-247b-4e71-ae43-64ca5c5cfb98_1728x824.png)](https://substackcdn.com/image/fetch/$s_!fpnc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9e6e02a0-247b-4e71-ae43-64ca5c5cfb98_1728x824.png)

Image created by the author.

This component is designed to automatically generate the standard tests defined in the "Data Quality Standardization" section. The tests are generated using the dataset’s metadata, fetched from Uber’s centralized metadata service. Key fields required during the test auto-generation process include the dataset’s SLAs, partition keys (for large tables that test only the latest data partition), and primary keys.

Uber also supports auto-generating tests for all upstream and downstream tables, leveraging internal lineage service. Uber created a daily Spark job to fetch the latest lineage to support this use case. The job also refreshes all auto-generated test definitions to reflect any metadata change and accordingly updates the logic of the test generation process.

### **Test Execution Engine**

The engine is the Celery-based web service supporting approximately 100,000 daily executions of about 18,000 tests. Tests can be auto-generated (like mentioned above) or defined by users. Each test is characterized by an assertion that must be true for it to pass.

The tests can be reduced to a few logical assertions. The most basic is comparing a computed value with a constant number. Another common pattern is comparing one computed value with another computed value. Uber observed that most data quality tests are defined by one of these two simple assertion patterns.

Uber uses assertion patterns to construct the test expression, which is a string of symbols representing instructions that the execution engine can interpret.

The string is a flattened [Abstract Syntax Tree (AST)](https://en.wikipedia.org/wiki/Abstract_syntax_tree) that contains expressions and parameters to control the execution. At execution time, the expression is parsed into a tree and evaluated in a [post-order traversal](https://www.geeksforgeeks.org/postorder-traversal-of-binary-tree/). In this approach, every test can be represented as an AST and processed by the execution engine.

### **Alert Generator**

Alerts can also be auto-generated following templates and business rules. The process needs extra parameters which can be retrieved from the metadata service, such as table owners, or alert email. Uber will create alerts per dataset (table A or table B) per test category (freshness or completeness) based on results generated by the test execution engine. Moreover, Uber’s engineers also need to prevent false alerts and provides good user experience.

Uber introduced a sustained period indicating the table SLA allowing test failures. If the test has a sustained period of 3 hours, the platform will set its status as WARN until the test failures violate the sustained period.

Even for real alerts, the unnecessary number of alerts can overwhelm users. For example, when data arrive late, the freshness alert will trigger, and the Completeness and Cross-datacenter Consistency alerts are very likely to be triggered at the same time—three alerts for one issue.

Uber tries to limit the alert count in this case by default setting the Freshness alert as a dependency of other categories, so other alerts will be ignored to avoid duplicate notifications about the same root cause.

### **Incident Manager**

[![Image](https://substackcdn.com/image/fetch/$s_!-dJd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd8e39394-ec7e-4f7f-9b0e-70793669f368_1224x903.png "Image")](https://substackcdn.com/image/fetch/$s_!-dJd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd8e39394-ec7e-4f7f-9b0e-70793669f368_1224x903.png)

Incident Manager workflow. Figure 5, [How Uber Achieves Operational Excellence in the Data Quality Experience](https://www.uber.com/en-VN/blog/operational-excellence-data-quality/) (2021)

After users had received an alert, investigated the root cause, and mitigated the quality issue, Uber added an internal scheduler to rerun failed tests with exponential backoff automatically. Thanks to this, users can validate whether the incident has been resolved successfully if the same test passes again and resolve the alert automatically without any user manual intervention.

Uber also developed a tool that allows users to annotate an incident and trigger a rerun manually. Users can report any incidents they discover while consuming data, and the data quality platform will check for overlap with any auto-detected incidents. Data producers are notified to acknowledge reported incidents. Uber aggregates both auto-detected and user-reported incidents to ensure that the final data quality status reflects all quality-related factors.

### **Consumption Tools**

Uber also provides a variety of different tools to let users understand their datasets’ quality:

[![](https://substackcdn.com/image/fetch/$s_!OZHZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F29f3116f-30d0-4ef9-a2cb-4d66b1f6be60_1318x784.png)](https://substackcdn.com/image/fetch/$s_!OZHZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F29f3116f-30d0-4ef9-a2cb-4d66b1f6be60_1318x784.png)

Image created by the author.

* [Databook](https://www.uber.com/blog/databook/) is the centralized dashboard that manages metadata for all Uber datasets. Uber integrated the quality platform with Databook to show data quality results in the UI.
* Uber has a Query Runner tool that can access any data storage, such as MySQL, Postgres, or Hive. The data quality platform integrates with this tool to help users query quality status. The query API takes the dataset name and time range and verifies whether the query time range overlaps with any ongoing data incidents.
* The ETL Manager serves as the controller for all Uber data pipelines. It can call the data quality platform to trigger new test executions immediately after a pipeline finishes, ensuring a quality check is performed. Additionally, before scheduling a data pipeline, the ETL Manager can consume data quality results for its input datasets. If the quality of any dataset fails to meet the SLA, the ETL Manager will not run the pipeline.
* Uber has a metric platform that consolidates business metrics definitions and calculates and serves metrics using raw datasets. The data quality platform is closely integrated with the metric platform by defining specific standard tests for metrics and providing metric-level quality through the metric platform's query layer.

---

## Outro

Thank you for reading this far.

In this article, we've explored how Uber established data quality standards across internal teams and built a platform capable of efficiently testing data quality across Uber's vast number of datasets.

See you in my next blog.

---

## **References**

*[1] Uber Engineering Blog, [How Uber Achieves Operational Excellence in the Data Quality Experience](https://www.uber.com/en-VN/blog/operational-excellence-data-quality/) (2021)*

---

## Before you leave

If you want to discuss this further, please leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/), [Email](http://vutrinh2704@gmail.com), or [Twitter](https://x.com/_vutrinh).

[Leave a comment](https://vutr.substack.com/p/i-spent-3-hours-learning-how-uber/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
