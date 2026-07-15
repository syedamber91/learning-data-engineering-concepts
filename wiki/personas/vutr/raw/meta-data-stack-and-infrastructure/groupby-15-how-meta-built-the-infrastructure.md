---
title: "GroupBy #15: How Meta built the infrastructure for Threads, Notion's data scale journey"
channel: vutr
author: "Vu Trinh"
published: 2023-12-26
url: https://vutr.substack.com/p/groupby-15-how-meta-built-the-infrastructure
paid: false
topics: ["Data Engineering", "Apache Airflow", "Apache Kafka", "Apache Spark", "Apache Flink", "Snowflake", "Databricks", "BigQuery", "Streaming", "Data Quality"]
tags: [https, engineering, blog, medium, auto, linkedin]
---

# GroupBy #15: How Meta built the infrastructure for Threads, Notion's data scale journey

*Plus: Grokking Concurrency Book, Prompt engineering Guide from Open AI*

> Source: [Open post](https://vutr.substack.com/p/groupby-15-how-meta-built-the-infrastructure)

## Topics

[[data-engineering|Data Engineering]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-flink|Apache Flink]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[bigquery|BigQuery]] · [[streaming|Streaming]] · [[data-quality|Data Quality]]

---

*This is **GroupBy**, the place where I share with you guys the resources I learn from people smarter than me in data engineer field.*

*Not subscribed yet? Here you go:*

[Subscribe now](https://vutr.substack.com/subscribe?)

![](https://substackcdn.com/image/fetch/$s_!D8N-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fvutr.substack.com%2Fimg%2Fsubstack.png)

Get more from Vu Trinh in the Substack app

Available for iOS and Android

[Get the app](https://substack.com/app/app-store-redirect?utm_campaign=app-marketing&utm_content=author-post-insert&utm_source=vutr)

[![](https://substackcdn.com/image/fetch/$s_!TBIn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F57677334-66e2-4f1b-95ed-dc3235460543_1300x900.png)](https://substackcdn.com/image/fetch/$s_!TBIn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F57677334-66e2-4f1b-95ed-dc3235460543_1300x900.png)

It might be too early, but Happy New Year, everyone!

---

> *👋 Hi, my name is Vu Trinh, a data engineer.*
>
> *I enjoy reading **good stuff** (related to data and engineering), and this newsletter is my effort on the journey to seek the "good stuff" across the entire Internet.*
>
> *Hope this issue find you well.*

---

> *Happy new year everyones.*
>
> *Fact: In Vietnam, we celebrate the New Year two times:*
>
> * *First date based on the solar calendar.*
> * *First date based on the lunar calendar.*

---

# 📚┆Book

## 📘┆[Grokking Concurrency](https://www.manning.com/books/grokking-concurrency?utm_source=social_media&utm_medium=nom_influencer&utm_campaign=book_bobrov_grokking_5_18_22)

✍┆[Kirill Bobrov](https://www.linkedin.com/in/luminousmen/)

> *In Grokking Concurrency you will:*
>
> * *Get up to speed with the core concepts of concurrency, asynchrony, and parallel programming*
> * *Learn the strengths and weaknesses of different hardware architectures*
> * *Improve the sequential performance characteristics of your software*
> * *Solve common problems for concurrent programming*
> * *Compose patterns into a series of practices for writing scalable systems*
> * *Write and implement concurrency systems that scale to any size*

> *I attempted to self-learn concurrency (programming) and gave up many times because I found it too hard to swallow. But this time, I feel quite confident. This book helped me a lot with simple words and interesting illustrations. Don’t skip this book.*

# 🎯 Side Project

> *40+ hours of debugging and you still want some more?*

## 📖┆[Data Engineering End-to-End Project - Spark, Kafka, Airflow, Docker, Cassandra, Python](https://medium.com/@dogukannulu/data-engineering-end-to-end-project-1-7a7be2a3671)

✍ [Dogukan Ulu](https://medium.com/@dogukannulu?source=post_page-----7a7be2a3671--------------------------------)

> *Gets random names from the API. Sends the name data to Kafka topics every 10 seconds using Airflow. Every message is read by Kafka consumer using Spark Structured Streaming and written to Cassandra table on a regular interval.*
>
> — From [author’s Github repo](https://github.com/dogukannulu/kafka_spark_structured_streaming?source=post_page-----7a7be2a3671--------------------------------)

[![](https://substackcdn.com/image/fetch/$s_!89-d!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F225167fe-85b8-4273-a3cc-e4b50e70d0f2_1151x661.png)](https://substackcdn.com/image/fetch/$s_!89-d!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F225167fe-85b8-4273-a3cc-e4b50e70d0f2_1151x661.png)

from author’s [article](https://medium.com/@dogukannulu/data-engineering-end-to-end-project-1-7a7be2a3671)

> *ooh Cassandra, interesting!*

---

# 🐙 Learning resource

> *I love to learn, and I assume you do too.*

## 🎓┆[Prompt engineering Guide from Open AI](https://platform.openai.com/docs/guides/prompt-engineering)

✍ OpenAI

> *This guide shares strategies and tactics for getting better results from large language models (sometimes referred to as GPT models) like GPT-4. The methods described here can sometimes be deployed in combination for greater effect. We encourage experimentation to find the methods that work best for you.*

## 📖┆[Five Python Decorators That Can Reduce Your Code By Half](https://python.plainenglish.io/five-python-wrappers-that-can-reduce-your-code-by-half-af775feb1d5)

✍ [Serop Baghdadlian](https://medium.com/@seropbaghdadlian)

> *Upgrade your Python game by using these wrappers for maximum efficiency and readability.*

---

# 🚀 Engineering

> *I have to believe in a world outside my own mind. — Memento (2000)*

## 📖┆[Colocated and Interleaved Tables in Distributed SQL Databases: Tradeoffs](https://medium.com/@magda7817/colocated-and-interleaved-tables-in-distributed-sql-databases-tradeoffs-f2e7b1b9d68e)

✍ [Denis Magda](https://medium.com/@magda7817?source=post_page-----f2e7b1b9d68e--------------------------------)

> *To mitigate network latency's impact on overall application performance, some databases support colocated and interleaved tables. This optimization technique allows storing child table records alongside their parent rows.*

## 📖┆[How Meta built the infrastructure for Threads](https://engineering.fb.com/2023/12/19/core-infra/how-meta-built-the-infrastructure-for-threads/)

✍ [Laine Campbell](https://engineering.fb.com/author/laine-campbell/)

> *On July 5, 2023, Meta launched Threads, the newest product in our family of apps, to an unprecedented success that saw it garner over 100 million sign ups in its first five days.*

## 📖┆**[Uber’s Highly Scalable and Distributed Shuffle as a Service](https://www.uber.com/en-SG/blog/ubers-highly-scalable-and-distributed-shuffle-as-a-service/)**

✍ [Uber Engineering Blog](https://www.uber.com/en-SG/blog/engineering/?uclick_id=15b6739c-0acd-406e-bdf6-884992beefa0)

> *We will focus on Spark shuffle scalability challenges in this blog post. We propose a new Remote Shuffle Service, codenamed RSS, which will move the shuffle from local to remote machines.*

## 📖┆[A Hudi Live Event: Notion's journey through different stages of data scale](https://www.linkedin.com/events/ahudiliveevent-notion-sjourneyt7138325735781400576/comments/)

✍ [Apache Hudi Community](https://www.linkedin.com/company/apache-hudi/)

> *Notion's Thomas Chow and Nathan Louie will talk about how their data infrastructure transformed to support their exponential growth and novel product use cases.*

## 📖┆**[Goldsky - A Gold Standard Architecture with ClickHouse and Redpanda](https://clickhouse.com/blog/clickhouse-redpanda-architecture-with-goldsky)**

✍ [The ClickHouse Team](https://clickhouse.com/blog)

> *Upon speaking with our customer Goldsky and hearing of such a pattern, we decided to share their deployment architecture for Redpanda, Apache Flink, and ClickHouse.*

---

# ✏ Data

> *The one thing that this job has taught me is that truth is stranger than fiction. — Predestination (2014)*

## 📖┆[How Airbnb Turned Itself Into A Data-Driven Company Through Business Intelligence](https://www.thdpth.com/p/how-airbnb-turned-itself-into-a-data)

✍ [Sven Balnojan](https://substack.com/profile/229923-sven-balnojan)

> *Why would you care about boring stuff like decision-making & business intelligence?.*

## 📖┆[Designing One Big Table (OBT)](https://leo-godin.medium.com/designing-one-big-table-obt-c1dd797d60ac)

✍ [Leo Godin](https://leo-godin.medium.com/?source=post_page-----c1dd797d60ac--------------------------------)

> *Arguing about OBT will get us nowhere. Instead, let’s focus ourselves on defining patterns and solutions to get the most out of them.*

## 📖┆[Data Usability: How to Build Better Data Products?](https://medium.com/@meskensjan/data-usability-how-to-build-better-data-products-78583d713bd1)

✍ [janmeskens](https://medium.com/@meskensjan?source=post_page-----78583d713bd1--------------------------------)

> *This article initiates by introducing a ‘data to impact framework,’ which illustrates how humans leverage data products — originating from AI and data pipelines — to transform raw data into tangible outcomes.*

## 📖┆[Nemo: Data discovery at Facebook](https://engineering.fb.com/2020/10/09/data-infrastructure/nemo/)

✍ [Haran Talmon](https://engineering.fb.com/author/haran-talmon/)

> *...we built Nemo, an internal data discovery engine. Nemo allows engineers to quickly discover the information they need, with high confidence in the accuracy of the results.*

## 📖┆[Meet Hodor — Gojek’s Upstream Data Quality Tool](https://www.gojek.io/blog/meet-hodor-gojeks-upstream-data-quality-tool)

✍ [Maulik Soneji](https://www.linkedin.com/in/maulik-soneji-48512781/)

> *Learn how Gojek’s Data Engineering team built a tool to capture metrics highlighting the quality of the data we collect.*

---

# 🤖 AI┆ML┆Data Science

> *You know, Burke, I don’t know which species is worse. — Ripley, Aliens (1986)*

## 📖┆[Should we even care about using LLMs to query enterprise data?](https://roundup.getdbt.com/p/should-we-even-care-about-using-llms)

✍ [Jason Ganz](https://substack.com/profile/73769889-jason-ganz)

> *And so now, we return to the original question that took us down this long and winding path - should we even care about connecting enterprise data to natural language queries by LLMs?*

## 📖┆[Why we use lenient p-value thresholds like 0.4 for A/B experiments at Agoda - Part 1](https://medium.com/agoda-engineering/why-we-use-lenient-p-value-thresholds-like-0-4-for-a-b-experiments-at-agoda-part-1-e93c7c56e666)

✍ [Agoda Engineering](https://medium.com/@agoda.eng?source=post_page-----e93c7c56e666--------------------------------)

> *Industry and academia usually use the p-value threshold of 0.05; however, at Agoda, we use a much more lenient threshold of 0.3 to 0.45. In this article, we will explain that this lenient threshold, despite its much higher false positive rate, is actually more beneficial to the company.*

## 📖┆[AI debugging at Meta with HawkEye](https://engineering.fb.com/2023/12/19/data-infrastructure/hawkeye-ai-debugging-meta/)

✍ [Partha Kanuparthy](https://engineering.fb.com/author/partha-kanuparthy/)

> *HawkEye is the powerful toolkit used internally at Meta for monitoring, observability, and debuggability of the end-to-end machine learning (ML) workflow that powers ML-based products.*

## 📖┆[Enhancing Content Review: Proactively addressing threats with AutoML](https://engineering.linkedin.com/blog/2023/enhancing-content-review--proactively-addressing-threats-with-au)

✍ [Shubham Agarwal](https://engineering.linkedin.com/blog/authors/s/shubham-agarwal)

> *This blog post delves into the AutoML framework for LinkedIn’s content abuse detection platform and its role in improving and fortifying content moderation systems at LinkedIn.*

## 📖┆[Building Trust and Combating Abuse On Our Platform](https://engineering.linkedin.com/blog/2023/casal--building-trust-and-combating-abuse---the-anti-abuse-core-)

✍ [Amit Mathapati](https://engineering.linkedin.com/blog/authors/a/amit-mathapati)

> *In this blog post, we discuss how we are harnessing AI to help us with abuse prevention and share an overview of our infrastructure and the role it plays in identifying and mitigating abusive behavior on our platform.*

---

# 🔥 Catch up

> *…Next Saturday night, we're sending you back to the future! — Dr. Emmett Brown, Back to the Future (1985)*

## 📖 [Airflow](https://airflow.apache.org/)┆[2.8.0 Release Note](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html#airflow-2-8-0-2023-12-14)

## 📖 [Snowflake](https://www.snowflake.com/en/)┆**[Snowpark Container Services Release Notes](https://docs.snowflake.com/en/release-notes/2023/other/2023-12-20)**

---

# 🥷 It will steal 27 seconds from you

> *Random thoughts, ideas.*

Updates: I will begin publishing a sub-newsletter in the next few weeks in the format of a mini-blog, where I'll share things I learn in the data engineering field. Here is some information about it:

Number of emails you will receive:

* Min: 1 (on Thursday)
* Max: 2 (another one on Saturday)

Length of the email:

* Maximum 3-minute read (but it might take me more than 3 days to prepare).

Focus on:

* "How it works internally" in modern analytics databases (like BigQuery, Snowflake, Databricks,…)
* Programming language tips: how to write better code or related content to Python, Rust.
* My experience during the journey to becoming a "senior" data engineer (hopefully).
* …

You can:

* Choose to receive these emails or not through a simple toggle configuration.

That's all for now. (I believe so).

Will continue updating...

Let me here your voice, for example:

'Your newsletter is so terrible, I can't handle it anymore.'

[Leave a comment](https://vutr.substack.com/p/groupby-15-how-meta-built-the-infrastructure/comments)

---

# “Hasta la vista, baby”

# -T800, Terminator 2: Judgment Day (1991)

Thanks for scrolling this far! There's a convenient subscribe box here if you want me to annoy you every week. 😄
