---
title: "GroupBy #30: Uber- How LedgerStore Supports Trillions of Indexes, Composable Data Systems: Lessons from Apache Calcite Success"
channel: vutr
author: "Vu Trinh"
published: 2024-04-09
url: https://vutr.substack.com/p/groupby-30-uber-how-ledgerstore-supports
paid: false
topics: ["Data Engineering", "Apache Kafka", "Apache Spark", "Apache Iceberg", "Apache Flink", "Delta Lake", "BigQuery", "Lakehouse", "Streaming"]
tags: [https, blog, substack, engineering, platform, cloud]
---

# GroupBy #30: Uber- How LedgerStore Supports Trillions of Indexes, Composable Data Systems: Lessons from Apache Calcite Success

*Plus: Spotify - Data Platform Explained, Grab - Turning observations into actionable insights for enhanced decision-making.*

> Source: [Open post](https://vutr.substack.com/p/groupby-30-uber-how-ledgerstore-supports)

## Topics

[[data-engineering|Data Engineering]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[apache-flink|Apache Flink]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[lakehouse|Lakehouse]] · [[streaming|Streaming]]

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

[![](https://substackcdn.com/image/fetch/$s_!6DSX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F468d621e-2905-47d4-8a20-44f90854e82a_1400x1000.png)](https://substackcdn.com/image/fetch/$s_!6DSX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F468d621e-2905-47d4-8a20-44f90854e82a_1400x1000.png)

Image created by Canva Image Generator.

---

# 🚀 Engineering

> *I have to believe in a world outside my own mind. — Memento (2000)*

#### 📖┆[How LedgerStore Supports Trillions of Indexes at Uber](https://www.uber.com/en-SG/blog/how-ledgerstore-supports-trillions-of-indexes/)

✍ [Uber Engineering Blog](https://www.uber.com/blog/asia/)

> *This blog covers the significance of LedgerStore indexing and its architecture, which powers trillions of indexes, with a petabyte-scale index storage footprint.*

#### 📖┆[Composable Data Systems: Lessons from Apache Calcite Success](https://www.querifylabs.com/blog/composable-data-systems-lessons-from-apache-calcite-success)

✍ [Vladimir Ozerov](https://www.linkedin.com/in/devozerov/)

> *In this blog post, I would like to share our experience with Apache Calcite — a powerful composable toolset for building query optimizers. Apache Calcite achieved tremendous success, powering query optimization in many popular systems, such as Apache Hive and Apache Flink.*

#### 📖┆[Data Platform Explained](https://engineering.atspotify.com/2024/04/data-platform-explained/)

✍ [Anastasia Khlebnikova](https://www.linkedin.com/in/anastasia-khlebnikova-63827b4/) + [Carol Cunha](https://www.linkedin.com/in/zamithcunha/)

> *As engineers working at Spotify, we frequently find ourselves explaining our robust data platform to fellow professionals who are contemplating embarking on a similar venture within their organizations. Despite the number of articles, blog posts, and talks one can find online, it can be challenging to digest the information about the building blocks of a data platform, how to start building one, and the tradeoffs to consider for what is good for the business. In this blog post series, we’ll delve into what our data platform entails, its pivotal role at Spotify, and the key factors leading organizations to consider building one.*

#### 📖┆**[Netflix’s Media Landscape Evolution: From 3–2–1 to Cloud Storage Optimization](https://netflixtechblog.medium.com/netflixs-media-landscape-evolution-from-3-2-1-to-cloud-storage-optimization-77e9a19171ed)**

✍ [Netflix Technology Blog](https://netflixtechblog.medium.com/?source=post_page-----77e9a19171ed--------------------------------)

> *This blog will explore how harnessing user access patterns helped us optimize storage efficiency and cost-effectiveness smartly. Within this exploration, we delve into a cost analysis of lifecycle policies, explicitly examining the cost-effectiveness of various archival and purge strategies tailored to different AWS storage layers.*

#### 📖┆[The Design Philosophy of Great Tables](https://posit-dev.github.io/great-tables/blog/design-philosophy/)

✍ [Rich Iannone](https://github.com/rich-iannone) + [Michael Chow](https://github.com/machow)

> *Through the exploration of the qualities that make tables shine, the backstory of tables as a display of data, and the issues faced today, it’s clear how we can solve the great table dilemma with Great Tables.*

#### 📖┆[How we Built a 19 PiB Logging Platform with ClickHouse and Saved Millions](https://clickhouse.com/blog/building-a-logging-platform-with-clickhouse-and-saving-millions-over-datadog)

✍ [Clickhouse Blog](https://clickhouse.com/blog/)

> *In the interest of others benefiting from our journey, we provide the details of our own ClickHouse-powered logging solution that contains over 19 PiB uncompressed, or 37 trillion rows, for our AWS regions alone. As a general design philosophy, we aspired to minimize the number of moving parts and ensure the design was as simple and reproducible as possible.*

#### 📖┆[Small Files Issue: Where Streams and Tables Meet](https://hubertdulay.substack.com/p/small-files-issue-where-streams-and?r=46sqk&utm_campaign=post&utm_medium=web&triedRedirect=true)

✍ [Hubert Dulay](https://substack.com/profile/7035644-hubert-dulay)

> *The announcement that Confluent will now support seamless materialization of Apache Kafka topics as Iceberg Tables (aka Tableflow) has gotten the streaming world and lakehouse worlds rubbing their chins 🤔 and cleaning their monocles 🧐.*

#### 📖┆[Introducing Trio | Part II](https://medium.com/airbnb-engineering/introducing-trio-part-ii-fe836013a798)

✍ [Eli Hart](https://medium.com/@konakid?source=post_page-----fe836013a798--------------------------------)

> *Part two on how we built a Compose based architecture with Mavericks in the Airbnb Android app*

#### 📖┆**[Reverse Searching Netflix’s Federated Graph](https://netflixtechblog.com/reverse-searching-netflixs-federated-graph-222ac5d23576)**

✍ [Netflix Technology Blog](https://netflixtechblog.medium.com/)

> *As promised in the previous post, we’ll share how we partnered with one of our Studio Engineering teams to build reverse search. Reverse search inverts the standard querying pattern: rather than finding documents that match a query, it finds queries that match a document.*

#### 📖┆[Iris - Turning observations into actionable insights for enhanced decision making](https://engineering.grab.com/iris)

✍ [Huong Vuong](https://engineering.grab.com/authors#huong-vuong) + [Hai Nam Cao](https://engineering.grab.com/authors#hainam-cao)

> *Our Iris platform bridges the gap between raw data and meaningful insights, serving the needs of data-driven organisations. Specialising in meticulous monitoring and tracking of Spark and Presto jobs, Iris stands as a transformative tool for peak observability and effective decision-making.*

#### 📖┆[A Sniff Test for Some Query Optimizers](https://buttondown.email/jaffray/archive/a-sniff-test-for-some-query-optimizers/)

✍ [Justin Jaffray](https://buttondown.email/jaffray)

> *One important part of query planning is performing transformations over queries. Today I want to see how a couple common databases perform on a completely made-up and unrepresentative benchmark.*

#### 📖┆[Polars vs. pandas: What’s the Difference?](https://blog.jetbrains.com/dataspell/2023/08/polars-vs-pandas-what-s-the-difference/)

✍ [Jodie Burchell](https://blog.jetbrains.com/author/jodie-burchell-jetbrains-com)

> *If you’ve been keeping up with the advances in Python dataframes in the past year, you couldn’t help hearing about Polars, the powerful dataframe library designed for working with large datasets.*

---

# ✏ Data

> *The one thing that this job has taught me is that truth is stranger than fiction. — Predestination (2014)*

#### 📖┆[Synchronizing Organizational Decisions](https://sqlpatterns.com/p/synchronizing-organizational-decisions)

✍ [Ergest Xheblati](https://substack.com/@ergestx)

> *How metrics trees foster harmonized decisions and drive sustained impact.*

#### 📖┆[Dissecting What Makes a Data Strategy Fail: Fluff, Challenges, and Objectives](https://www.thdpth.com/p/dissecting-what-makes-a-data-strategy)

✍ [Sven Balnojan PhD](https://substack.com/profile/229923-sven-balnojan-phd)

> *Unfortunately, bad data strategies are everywhere. Sometimes, I find it hard to find examples of good ones! Most data startups start out with a bad strategy. Almost every single internal data initiative I read is bad.*

#### 📖┆[The Data Analyst Every CEO Wants](https://fromanengineersight.substack.com/p/the-data-analyst-every-ceo-wants)

✍ [Benoit Pimpaud](https://substack.com/profile/23621089-benoit-pimpaud)

> *The following lines list the top 5 things best to learn and focus on for being the analyst that every CEO should have by his side.*

---

# 🤖 AI┆ML┆Data Science

> *You know, Burke, I don’t know which species is worse. — Ripley, Aliens (1986)*

#### 📖┆[Sneak preview of GPT-5!](https://garymarcus.substack.com/p/sneak-preview-of-gpt-5)

✍ [Gary Marcus](https://substack.com/profile/14807526-gary-marcus)

> *Holy shit! OpenAI just gave me sneak preview early access to GPT-5 (to do some red-teaming) — and it’s incredible!*

#### 📖┆[When Will the GenAI Bubble Burst?](https://garymarcus.substack.com/p/when-will-the-genai-bubble-burst)

✍ [Gary Marcus](https://substack.com/profile/14807526-gary-marcus)

> *Why and how it could happen in the next 12 months.*

#### 📖┆[What is retrieval-augmented generation, and what does it do for generative AI?](https://github.blog/2024-04-04-what-is-retrieval-augmented-generation-and-what-does-it-do-for-generative-ai/)

✍ [Nicole Choi](https://github.blog/author/nicchoi29/)

> *Here’s how retrieval-augmented generation, or RAG, uses a variety of data sources to keep AI models fresh with up-to-date information and organizational knowledge.*

#### 📖┆[How we built Text-to-SQL at Pinterest](https://medium.com/pinterest-engineering/how-we-built-text-to-sql-at-pinterest-30bad30dabff)

✍ [Pinterest Engineering](https://medium.com/@Pinterest_Engineering?source=post_page-----30bad30dabff--------------------------------)

> *We took the rise in availability of Large Language Models (LLMs) as an opportunity to explore whether we could assist our data users with this task by developing a Text-to-SQL feature which transforms these analytical questions directly into code.*

#### 📖┆[Algorithm War Coming! (Part 2)](https://koopingshung.substack.com/p/algorithm-war-coming-part-2)

✍ [Koo Ping Shung](https://substack.com/profile/7906875-koo-ping-shung)

> *The algorithm war will be never-ending. GenAI models will keep on being trained, with each GenAI model successful in certain dimensions. Model that are currently doing better will only be replaced by a later model that is doing better on all coinciding dimensions.*

---

# 🔥 Catch up

> *…Next Saturday night, we're sending you back to the future! — Dr. Emmett Brown, Back to the Future (1985)*

📖┆BigQuery | [Differential privacy](https://cloud.google.com/bigquery/docs/differential-privacy) is now [generally available (GA)](https://cloud.google.com/products/#product-launch-stages).

📖┆BigQuery | User now use [BigLake to access Delta Lake tables](https://cloud.google.com/bigquery/docs/create-delta-lake-table). This feature is available in [preview](https://cloud.google.com/products/#product-launch-stages).

📖┆BigQuery | User can now perform [model monitoring](https://cloud.google.com/bigquery/docs/model-monitoring-overview) in BigQuery ML

📖┆[BigQuery data clean rooms](https://cloud.google.com/bigquery/docs/data-clean-rooms) with analysis rules and enhanced usage metrics are now [generally available (GA)](https://cloud.google.com/products/#product-launch-stages).

---

# 💠 Previously on Dimension

> *Dimension is my sub-newsletter where I note down things I learn from people smarter than me in the data engineering field.*

Here are the 3 latest articles:

### ***Published on 2024, March 23:***

### ***Published on 2024, March 30:***

### ***Published on 2024, April 6:***

Let me here your voice, for example:

'Your newsletter is so terrible, I can't handle it anymore.'

[Leave a comment](https://vutr.substack.com/p/groupby-30-uber-how-ledgerstore-supports/comments)

---

## “Hasta la vista, baby” -T800, Terminator 2: Judgment Day (1991)

Thanks for scrolling this far! There's a convenient subscribe box here if you want me to annoy you every week. 😄
