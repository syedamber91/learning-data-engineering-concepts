---
title: "GroupBy #44: Meta | The Data Stack"
channel: vutr
author: "Vu Trinh"
published: 2024-07-16
url: https://vutr.substack.com/p/groupby-44-meta-the-data-stack
paid: false
topics: ["Data Engineering", "Apache Airflow", "Apache Spark", "Data Warehouse", "Orchestration", "Data Quality"]
tags: [meta, https, stack, engineers, internal, warehouse]
---

# GroupBy #44: Meta | The Data Stack

*Plus: A Brief History of Modern Data Stack, How Canva collects 25 billion events per day*

> Source: [Open post](https://vutr.substack.com/p/groupby-44-meta-the-data-stack)

## Topics

[[data-engineering|Data Engineering]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[data-warehouse|Data Warehouse]] · [[orchestration|Orchestration]] · [[data-quality|Data Quality]]

---

*This is **GroupBy**, the weekly compiled resources for data engineers.*

*Not subscribed yet? Here you go:*

[Subscribe now](https://vutr.substack.com/subscribe?)

> *👋 Hi, my name is Vu Trinh, a data engineer.*
>
> *I share my lesson and excellent resources to read in this newsletter.*
>
> *Hope this issue finds you well.*

[![](https://substackcdn.com/image/fetch/$s_!sv65!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbc212358-5d3e-4daf-a791-344ac3ee08ad_1400x1000.png)](https://substackcdn.com/image/fetch/$s_!sv65!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbc212358-5d3e-4daf-a791-344ac3ee08ad_1400x1000.png)

Image created by the author.

---

# **Meta: Overview of the internal data stack**

## Intro

A planet-scale company like Meta, Twitter, or LinkedIn processes tons of data daily to support its operations. To support that need, those companies must build a robust data infrastructure. Today, we will have a glimpse of the Meta internal data stack.

> *You can find the original article from Meta [here](https://medium.com/@AnalyticsAtMeta/data-engineering-at-meta-high-level-overview-of-the-internal-tech-stack-a200460a44fe).*

## Data Warehouse

The Meta’s data warehouse is a repository for analytics requirements. It has millions of Hive tables, physically stored using an internal fork of ORC.

Data is spread across namespaces. Namespaces are either physical (geographical) or logical partitioning of the warehouse: tables are grouped into a namespace to efficiently be used in the same queries without moving data around. Thus, data replication is required when tables need to be accessed from two different namespaces.

Data in Meta's systems is kept only as long as needed. Tables in the warehouse usually have a set retention period, such as 90 days, after which older data is either archived or deleted.

Each table is linked to an on-call group, which designates the responsible team and the point of contact for any issues or questions about the data.

### Data warehouse ingestion

* Snapshot from operational databases (Meta’s graph database)
* Logs from clients or servers.
* From the Dataswarm pipeline, mainly retrieved by querying other warehouse’s tables.

## **Data discovery, data catalog**

Engineers at Meta developed a web-based tool called iData, which lets users search data assets (tables, dashboards,…) by keyword. The tool also includes lineage tools to help users trace upstream and downstream data assets.

## **The Query Engine**

Meta's data warehouse can be queried, mainly using Presto and Spark. Most of their pipelines and queries are written in either Spark SQL or Presto SQL.

They also use imperative approaches with Spark’s Java, Scala, and Python APIs for complex transformations.

The choice between Presto and Spark depends on the workload. Presto is more efficient for most queries, while Spark handles heavier workloads needing more memory or complex joins.

Presto clusters are sized to handle day-to-day ad-hoc queries, scanning billions of rows in seconds or minutes, depending on complexity.

## **Scuba: Real-time analytics**

Scuba is Meta's real-time data analytics framework. It is widely used by data and software engineers to analyze trends in real-time logging data and by software and production engineers to debug.

## **Daiquery & Bento: The notebooks**

At Meta, data engineers use Daiquery daily. This web-based notebook is a single entry point for querying various data sources, including the warehouse (via Presto or Spark), Scuba, and more. Users can upgrade their Daiquery notebooks to Bento notebooks for more complex query analysis. Bento is Meta’s managed Jupyter Notebook implementation, supporting Python or R code and a variety of visualization libraries in addition to queries.

## **Unidash: Dashboarding**

Unidash is the internal tool data engineers use to create dashboards (you can imagine [Apache Superset](https://superset.apache.org/) here). It integrates with Daiquery and many other tools; for example, engineers can write their query in Daiquery, create their graph there, and then export it to a new or existing Unidash dashboard.

## **Software development**

Most engineers at Meta use a customized version of [Visual Studio Code](https://code.visualstudio.com/) as an IDE. It has many custom plugins maintained by internal teams. They also use an fork of [Mercurial](https://www.mercurial-scm.org/) for source control and a monorepo structure—all data pipelines and most internal tools are in a single repository.

## **Pipeline Developing**

At Meta, engineers mainly develop data pipelines in SQL (for business logic) and wrapped in Python code (for orchestration and scheduling).

Their internal Python library for orchestrating and scheduling pipelines is called Dataswarm, a predecessor to [Airflow](https://airflow.apache.org/), and is developed and maintained internally.

## **Monitoring & operations**

Pipeline monitoring is done via a web-based tool called CDM (Central Data Manager), which can be seen as the *Dataswarm UI*.

This is the entry point to a broader tool:

* Identify failing tasks and find the corresponding logs
* Define and run backfills
* Navigate to upstream dependencies
* Identify upstream blockers
* Notifications
* Set up and monitor data quality checks

## **Outro**

Thank you for reading my note.

Now, let’s check some curated resources I found on the internet last week.

---

# 📋 The list

────────

[How Discord uses open-source tools for scalable data orchestration & transformation](https://discord.com/blog/how-discord-uses-open-source-tools-for-scalable-data-orchestration-transformation) — 11 mins, by Zach Bluhm

> *To continue delivering seamless service and insightful data analytics, we embraced an ambitious project: **to overhaul our data orchestration infrastructure using modern, open-source tools**.*

[Memory Management in DuckDB](https://duckdb.org/2024/07/09/memory-management) — 8 mins, by Mark Raasveldt

> *In this blog post, we will cover aspects of memory management within DuckDB – and provide examples of where they are utilized.*

[How Canva collects 25 billion events per day](https://www.canva.dev/blog/engineering/product-analytics-event-collection/) — 10 mins, by Long Nguyen

> *The architecture of our product analytics event delivery pipeline.*

[A Brief History of Modern Data Stack](https://www.dataengineeringweekly.com/p/a-brief-history-of-modern-data-stack) — 7 mins, by Ananth Packkildurai

> *A rise & fall of Modern Data Stack and what comes next?*

[Booking Deduplication: How Agoda Manages Duplicate Bookings Across Multiple Data Centers (Part 1)](https://medium.com/agoda-engineering/booking-deduplication-how-agoda-manages-duplicate-bookings-across-multiple-data-centers-08ddbe9e22f1) — 13 mins, Agoda Engineering Blog

> *Agoda introduced the booking deduplication feature many years ago to prevent the creation of duplicate bookings.*

[How data observability fits into the different stages in the data pipeline](https://medium.com/@mikldd/how-data-observability-fits-into-the-different-stages-in-the-data-pipeline-70d47aba8cbd) — 9 mins, by Mikkel Dengsøe

> *In this article, we’ll look into data observability tools’ role in different parts of the data pipeline and their limitations.*

---

## 😉 Previously on Dimension

> *Dimension is my sub-newsletter, where I note things I learn from people smarter than me in data engineering. Here is the latest article*

Let me hear your voice, for example:

'Your newsletter is so terrible, I can't handle it anymore.'

[Leave a comment](https://vutr.substack.com/p/groupby-44-meta-the-data-stack/comments)

Thanks for scrolling this far! There's a convenient subscribe box here if you want me to annoy you every week. 😄
