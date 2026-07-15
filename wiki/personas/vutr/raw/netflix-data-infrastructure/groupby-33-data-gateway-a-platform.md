---
title: "GroupBy #33: Data Gateway - A Platform for Growing and Protecting the Data Tier at Netflix, The Cloud Storage Triad: Latency, Cost, Durability"
channel: vutr
author: "Vu Trinh"
published: 2024-04-30
url: https://vutr.substack.com/p/groupby-33-data-gateway-a-platform
paid: false
topics: ["Data Engineering", "Apache Kafka", "Apache Spark", "Apache Iceberg", "Snowflake", "BigQuery", "Data Modeling", "Data Warehouse"]
tags: [https, blog, engineering, substack, platform, cloud]
---

# GroupBy #33: Data Gateway - A Platform for Growing and Protecting the Data Tier at Netflix, The Cloud Storage Triad: Latency, Cost, Durability

*Plus: Solving RevenueCat's data ingestion challenges into Snowflake, From ZooKeeper to KRaft: How the Kafka migration works*

> Source: [Open post](https://vutr.substack.com/p/groupby-33-data-gateway-a-platform)

## Topics

[[data-engineering|Data Engineering]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[snowflake|Snowflake]] · [[bigquery|BigQuery]] · [[data-modeling|Data Modeling]] · [[data-warehouse|Data Warehouse]]

---

*This is **GroupBy**, the weekly compiled resources for data engineers.*

*Not subscribed yet? Here you go:*

[Subscribe now](https://vutr.substack.com/subscribe?)

![](https://substackcdn.com/image/fetch/$s_!D8N-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fvutr.substack.com%2Fimg%2Fsubstack.png)

Get more from Vu Trinh in the Substack app

Available for iOS and Android

[Get the app](https://substack.com/app/app-store-redirect?utm_campaign=app-marketing&utm_content=author-post-insert&utm_source=vutr)

> *👋 Hi, my name is Vu Trinh, a data engineer.*
>
> *I enjoy reading **good stuff** (related to data and engineering), and this newsletter is my effort on the journey to seek the "good stuff" across the entire Internet.*
>
> *Hope this issue find you well.*

---

[![](https://substackcdn.com/image/fetch/$s_!LnWo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffeed28de-4e1a-41c4-a79d-c381b5b13a68_1400x1000.png)](https://substackcdn.com/image/fetch/$s_!LnWo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffeed28de-4e1a-41c4-a79d-c381b5b13a68_1400x1000.png)

Image created by the Canva Image Generator.

---

# 🐙 Learning

> *I love to learn, and I assume you do too.*

#### 📖┆[Learn one thing at a time](https://blog.lawrencejones.dev/learn-one-thing/)

✍ [Lawrence Jones](https://twitter.com/lawrjones)

> *Of the mental models and rules I use in my life, by far the most useful is to learn only one thing at any given time.*

---

# 🚀 Engineering

> *I have to believe in a world outside my own mind. — Memento (2000)*

#### 📖┆[Data Gateway - A Platform for Growing and Protecting the Data Tier](https://netflixtechblog.medium.com/data-gateway-a-platform-for-growing-and-protecting-the-data-tier-f1ed8db8f5c6)

✍ [Netflix Technology Blog](https://netflixtechblog.medium.com/?source=post_page-----f1ed8db8f5c6--------------------------------)

> *The Netflix Online Datastore team has built a platform we call the Data Gateway to enable our datastore engineers to deliver powerful data abstractions which protect Netflix application developers from complex distributed databases and incompatible API changes. In this opening post, we cover the platform as the first part of a series which shows how we use this platform to raise the level of abstraction that application developers use every day to create, access, and maintain their online data.*

#### 📖┆[Solving RevenueCat's data ingestion challenges into Snowflake](https://www.revenuecat.com/blog/engineering/data-ingestion-snowflake/)

✍ [Jesús Sánchez](https://www.linkedin.com/in/jes%C3%BAs-antonio-s%C3%A1nchez-m%C3%A9ndez-64799a25/?originalSubdomain=es)

> *In this blog, I’ll take you through the intricacies of our data management practices, specifically focusing on the journey of our data from its origins to its final destination in Snowflake. We’ll explore the challenges we faced, the solutions we devised, and the insights we gained through the process of optimizing our data ingestion pipeline.*

#### 📖┆[The Deconstructed Database](https://sympathetic.ink/2024/04/29/The-Deconstructed-Database.html)

✍ [Julien Le Dem](https://julien.ledem.net/)

> *Recently there’s been more talk around the same idea of building composable data systems. Arrow and Iceberg have grown exponentially in popularity and some of the aspirational ideas in my talk in 2018 are now well established. We do live in the future I was hoping for then. In this post, I want to explain in more detail what those components are and, more importantly, the contracts that keep them decoupled and composable.*

#### 📖┆[The Cloud Storage Triad: Latency, Cost, Durability](https://materializedview.io/p/cloud-storage-triad-latency-cost-durability)

✍ [Chris Riccomini](https://substack.com/profile/69592459-chris-riccomini)

> *I believe that the future of database persistence is object storage—S3, Google Cloud Storage, and so on. New systems like Neon, WarpStream, and Turbopuffer persist data in object storage to offer infinite retention, durability, replication, data warehouse integration, and so on.*

#### 📖┆[No Memory? No Problem. External Aggregation in DuckDB](https://duckdb.org/2024/03/29/external-aggregation.html)

✍ [Laurens Kuiper](https://www.linkedin.com/in/lnkuiper/)

> *In a nutshell, that’s what this post is about. Since the 0.9.0 release, DuckDB’s hash aggregation can process more unique groups than fit in memory by offloading data to storage. In this post, we’ll explain how this works. If you want to know what hash aggregation is, how hash collisions are resolved, or how DuckDB’s hash table is structured, check out our first blog post on hash aggregation.*

#### 📖┆[From ZooKeeper to KRaft: How the Kafka migration works](https://strimzi.io/blog/2024/03/21/kraft-migration/)

✍ [Paolo Patierno](https://twitter.com/ppatierno)

> *Through this blog post we are going to describe the main differences between using ZooKeeper and KRaft for Kafka to store the cluster metadata and how the migration from the former to the latter works.*

#### 📖┆[Scaling Kafka by Parallel Processing](https://blogs.halodoc.io/maximizing-kafka-efficiency-exploring-parallel-consumers/)

✍ [Tanuj Kumar](https://www.linkedin.com/in/tanujkumar13334/)

> *In this blog post, we will delve into the world of parallel consumer strategies for Kafka, exploring various approaches and techniques for achieving parallelism in message processing. We will discuss the benefits and trade-offs of each approach, along with best practices for implementation.*

#### 📖┆[Designing Kafka Streams Applications](https://blogit.michelin.io/dkafka-streams/)

✍ [Valérie Servaire](https://blogit.michelin.io/author/servaire/) + [Paul Amar](https://blogit.michelin.io/author/paul-2/) + [Damien Fayet](https://blogit.michelin.io/author/damien/)+ [Sébastien Viale](https://blogit.michelin.io/author/sebastien/)

> *For the past 4 years, our journey into the heart of Kafka's capabilities has been shaped by two pivotal concepts: Master Topologies and Micro Topologies. These conceptual frameworks have become the backbone of our Kafka Streams application design, offering a comprehensive and granular understanding of our end-to-end communication.*

#### 📖┆[pg\_analytics: Transforming Postgres into a Fast OLAP Database](https://blog.paradedb.com/pages/introducing_analytics)

✍ [Ming Ying](https://www.linkedin.com/in/ming-ying/)

> *We’re excited to introduce pg\_analytics, an extension that accelerates the native analytical performance of any Postgres database by 94x. With pg\_analytics installed, Postgres is 8x faster than Elasticsearch and nearly ties ClickHouse on analytical benchmarks.*

#### 📖┆[Data Anywhere with Pipelines, Event Notifications, and Workflows](https://blog.cloudflare.com/data-anywhere-events-pipelines-durable-execution-workflows)

✍ [Matt Silverlock](https://blog.cloudflare.com/author/silverlock)

> *Data is fundamental to any real-world application: the database storing your user data and inventory, the analytics tracking sales events and/or error rates, the object storage with your web assets and/or the Parquet files driving your data science team, and the vector database enabling semantic search or AI-powered recommendations for your users.*

#### 📖┆[Investigation of a Cross-regional Network Performance Issue](https://netflixtechblog.medium.com/investigation-of-a-cross-regional-network-performance-issue-422d6218fdf1)

✍ [Netflix Technology Blog](https://netflixtechblog.medium.com/?source=post_page-----422d6218fdf1--------------------------------)

> *This was a very interesting debugging exercise that covered many layers of Netflix’s stack and infrastructure. While it technically wasn’t the “network” to blame, this time it turned out the culprit was the software components that make up the network (i.e. the TCP implementation in the kernel).*

#### 📖┆[How to test PySpark code with pytest](https://www.startdataengineering.com/post/test-pyspark/)

✍ [Start Data Engineering](https://www.startdataengineering.com/)

> *Have you worked, or are you working with a code base that “moved fast” but had zero to no tests? Every minor feature request makes you start sweating because looking at your codebase the wrong way makes things explode unpredictably.*

#### 📖┆[Docker Fundamentals for Data Engineers](https://www.startdataengineering.com/post/docker-for-de/)

✍ [Start Data Engineering](https://www.startdataengineering.com/)

> *Docker can be overwhelming to start with. Most data projects use Docker to set up the data infra locally (and often in production). Setting up data tools locally without Docker is (usually)a nightmare! The official docker documentation, while extremely instructive, does not provide a simple guide covering the basics for setting up data infrastructure.*

---

# ✏ Data

> *The one thing that this job has taught me is that truth is stranger than fiction. — Predestination (2014)*

#### 📖┆[Practical Data Modeling - Chapter 1](https://practicaldatamodeling.substack.com/p/practical-data-modeling-chapter-1?utm_source=post-email-title&publication_id=1473069&post_id=144076836&utm_campaign=email-post-title&isFreemail=true&r=2rj6sg&triedRedirect=true&utm_medium=email)

✍ [Joe Reis](https://substack.com/profile/3531217-joe-reis)

> *What is data modeling? If you ask a group of people this question, you’ll get as many answers as the number of people you asked. Let’s start by defining data and models and then clarifying what data modeling is and is not.*

---

# 🤖 AI┆ML┆Data Science

> *You know, Burke, I don’t know which species is worse. — Ripley, Aliens (1986)*

#### 📖┆[Linkedin - Musings on building a Generative AI product](https://www.linkedin.com/blog/engineering/generative-ai/musings-on-building-a-generative-ai-product)

✍ [Juan Pablo Bottaro](https://www.linkedin.com/in/juan-pablo-bottaro/)

> ***Was it easy to build? What went well and what didn’t?** Building on top of generative AI wasn’t all smooth sailing, and we hit a wall in many places. We want to pull back the “engineering” curtain and share what came easy, where we struggled, and what’s coming next.*

#### 📖┆[What can LLMs never do?](https://www.strangeloopcanon.com/p/what-can-llms-never-do)

✍ [Rohit Krishnan](https://substack.com/profile/12282408-rohit-krishnan)

> *On goal drift and lower reliability. Or, why can't LLMs play Conway's Game Of Life?*

#### 📖┆[When Do We Stop Finding New Music? A Statistical Analysis](https://www.statsignificant.com/p/when-do-we-stop-finding-new-music)

✍ [Daniel Parris](https://substack.com/profile/112812180-daniel-parris)

> *So today, we'll explore how our relationship to music changes with age and the developmental phenomena driving our forever-shifting cultural tastes.*

#### 📖┆[DragonCrawl: Generative AI for High-Quality Mobile Testing](https://www.uber.com/en-SG/blog/generative-ai-for-high-quality-mobile-testing/)

✍ [Uber Engineering Blog](https://www.uber.com/blog/asia/?uclick_id=15b6739c-0acd-406e-bdf6-884992beefa0)

> *This blog will cover a quick introduction to large language models, deep dive into our architecture, challenges, and results. We will close by touching a little on what is in store for DragonCrawl.*

#### 📖┆[Airbnb Brandometer: Powering Brand Perception Measurement on Social Media Data with AI](https://medium.com/airbnb-engineering/airbnb-brandometer-powering-brand-perception-measurement-on-social-media-data-with-ai-c83019408051)

✍ [Tiantian Zhang](https://medium.com/@watera427_75688?source=post_page-----c83019408051--------------------------------)

> *At Airbnb, we have developed Brandometer, a state-of-the-art natural language understanding (NLU) technique for understanding brand perception based on social media data.*

#### 📖┆[Shepherd: How Stripe adapted Chronon to scale ML feature development](https://stripe.com/blog/shepherd-how-stripe-adapted-chronon-to-scale-ml-feature-development)

✍ [Benjamin Mears](https://www.linkedin.com/in/benjamin-mears-81680714/)

> *In 2022 we began a partnership with Airbnb to adapt and implement its platform, Chronon, as the foundation for Shepherd—our next-generation ML feature engineering platform—with a view to open sourcing it. We’ve already used it to build a new production model for fraud detection with over 200 features, and so far the Shepherd-enabled model has outperformed our previous model, blocking tens of millions of dollars of additional fraud per year. While our work building Shepherd was specific to Stripe, we are generalizing the approach by contributing optimizations and new functionality to Chronon that anyone can use.*

---

# 🔥 Catch up

> *…Next Saturday night, we're sending you back to the future! — Dr. Emmett Brown, Back to the Future (1985)*

📖┆[SQL code generation](https://cloud.google.com/bigquery/docs/write-sql-gemini#generate_a_sql_query) is now available for all BigQuery projects. This feature is available in [preview](https://cloud.google.com/products#product-launch-stages).

📖┆[User-defined aggregate functions (UDAFs)](https://cloud.google.com/bigquery/docs/user-defined-aggregates) that support SQL expressions are in [preview](https://cloud.google.com/products#product-launch-stages). User can create a UDAF with the [CREATE AGGREGATE FUNCTION](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#sql-create-udaf-function) statement.

---

# 💠 Previously on Dimension

> *Dimension is my sub-newsletter where I note down things I learn from people smarter than me in the data engineering field.*

Here are the 3 latest articles:

### ***Published on 2024, April 13:***

### ***Published on 2024, April 20:***

### ***Published on 2024, April 27:***

Let me here your voice, for example:

'Your newsletter is so terrible, I can't handle it anymore.'

[Leave a comment](https://vutr.substack.com/p/groupby-33-data-gateway-a-platform/comments)

---

## “Hasta la vista, baby” -T800, Terminator 2: Judgment Day (1991)

Thanks for scrolling this far! There's a convenient subscribe box here if you want me to annoy you every week. 😄
