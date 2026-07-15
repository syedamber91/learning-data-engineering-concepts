---
title: "GroupBy #22: Data Engineering Landscape in 2024, how I scaled my $1m/year revenue startup's data model"
channel: vutr
author: "Vu Trinh"
published: 2024-02-13
url: https://vutr.substack.com/p/groupby-22-navigating-the-data-engineering
paid: false
topics: ["Data Engineering", "dbt", "Apache Spark", "Snowflake", "BigQuery", "Data Warehouse", "Streaming"]
tags: [https, engineering, substack, platform, medium, cloud]
---

# GroupBy #22: Data Engineering Landscape in 2024, how I scaled my $1m/year revenue startup's data model

*Plus: SQL for the Weary, Why SQL is Unkillable, The Building Blocks of LLMs: Vectors, Tokens and Embeddings*

> Source: [Open post](https://vutr.substack.com/p/groupby-22-navigating-the-data-engineering)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-spark|Apache Spark]] · [[snowflake|Snowflake]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]] · [[streaming|Streaming]]

---

*This is **GroupBy**, where I share the resources I learn from people smarter than me in the data engineering field.*

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

[![](https://substackcdn.com/image/fetch/$s_!y9xj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6141f5bb-5651-4dd4-aa87-c9b48b03d2d1_1400x1000.png)](https://substackcdn.com/image/fetch/$s_!y9xj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6141f5bb-5651-4dd4-aa87-c9b48b03d2d1_1400x1000.png)

---

# 📈 Career

> *Don't let comfort hold you back.*

#### 📖┆[How to Build High-Performance Engineering Teams](https://luminousmen.com/post/how-to-build-highperformance-engineering-teams)

✍ [Kirill Bobrov](https://www.linkedin.com/in/luminousmen/)

> *Building a high-performance engineering team is like assembling a space shuttle; every component, no matter how small, plays a crucial role in ensuring a successful mission.*

#### 📖┆[How to hire low experience, high potential people](https://worktopia.substack.com/p/how-to-hire-low-experience-high-potential)

✍ [Tara Seshan](https://substack.com/profile/1590388-tara-seshan)

> *Finding diamonds in the rough*

---

# 🐙 Learning resource

> *I love to learn, and I assume you do too.*

#### 📖┆[SQL for the Weary](https://gvwilson.github.io/sql-tutorial/)

✍ [Greg Wilson](https://third-bit.com/)

> *Learning outcomes:*
>
> 1. *Explain the difference between a database and a database manager.*
> 2. *Write SQL to select, filter, sort, group, and aggregate data.*
> 3. *Define tables and insert, update, and delete records.*
> 4. *Describe different types of join and write queries that use them to combine data.*
> 5. *Use windowing functions to operate on adjacent rows.*
> 6. *Explain what transactions are and write queries that roll back when constraints are violated.*
> 7. *Explain what triggers are and write SQL to create them.*
> 8. *Manipulate JSON data using SQL.*
> 9. *Interact with a database using Python directly, from a Jupyter notebook, and via an ORM.*

---

# 🚀 Engineering

> *I have to believe in a world outside my own mind. — Memento (2000)*

#### 📖┆[Navigating the Data Engineering Landscape in 2024](https://airbyte.com/blog/data-engineering-landscape-2024)

✍ [Thalia Barrera](https://www.linkedin.com/in/thalia-barrera/) + [Jacob Prall](https://www.linkedin.com/in/jacob-prall-01abb867/)

> *Here's our take on the 5 big trends that everyone in data engineering needs to prepare for. And, more than just trends, we're offering practical tips on how you can use these insights to your advantage.Our goal is simple: to equip you with the information you need to navigate the data engineering trends of 2024 confidently. And yes, you guessed it – we're kicking things off with AI.*

#### 📖┆[A search engine in 80 lines of Python](https://www.alexmolas.com/2024/02/05/a-search-engine-in-80-lines.html)

✍ [Alex Molas](https://twitter.com/molasalex)

> *In this post I will walk you through the journey of building a search engine from scratch using Python.*

#### 📖┆[Dynamic Programming is not Black Magic](https://qsantos.fr/2024/01/04/dynamic-programming-is-not-black-magic/)

✍ [Quentin Santos](https://github.com/qsantos)

> *Dynamic programming itself is mostly natural when you understand what it does. And many common algorithms are actually just the application of dynamic programming to specific problems, including omnipresent path-finding algorithms such as Dijkstra’s algorithm.*

#### 📖┆[Our transformation journey toward an open data platform](https://medium.com/@bxh_io/our-transformation-journey-toward-an-open-data-platform-b6f869b6a173)

✍ [Ben Hall](https://medium.com/@bxh_io?source=post_page-----b6f869b6a173--------------------------------)

> *Our data scientists spent too much time spinning up clusters to get to the data, leaving little time for ML model experimentation that would help to drive new business. Scaling this complex environment became a major hurdle, especially with our decision to globalize operations across 3 major regions under one centralized enterprise data platform which we internally call Evergreen (“Always on” or like the largest container ships in the world).*

#### 📖┆[7 Lessons Learned migrating dbt code from Snowflake to Trino](https://medium.com/datamindedbe/7-lessons-learned-migrating-dbt-code-from-snowflake-to-trino-42fc907f0202)

✍ [Michiel De Muynck](https://medium.com/@michieldemuynck?source=post_page-----42fc907f0202--------------------------------)

> *Migrating from one data platform to another is never as simple as it seems. In the process of migrating several dbt projects from a Snowflake data warehouse to Starburst (i.e., enterprise Trino), we encountered a couple of differences between their SQL dialects that proved either tricky to find or difficult to deal with. In this post, I share 7 of these differences, and how we dealt with them.*

#### 📖┆[Performance Engineering and The Need for Speed](https://codeconfessions.substack.com/p/performance-engineering-1)

✍ [Abhinav Upadhyay](https://substack.com/profile/14520974-abhinav-upadhyay)

> *First of all let’s talk about why performance engineering is getting important in the current era of computing.*

#### 📖┆[Data Platform @ Rapido (Part -I) - efficient, scalable and cost friendly analytics](https://medium.com/rapido-labs/data-platform-rapido-part-i-cheap-efficient-and-scalable-analytics-52662111b2d2)

✍ [Sabyasachi Nandy](https://medium.com/@sabya.nandy14?source=post_page-----52662111b2d2--------------------------------)

> *In this series of articles, we will go through how the Data Platform team in Rapido stood up to this enormous challenge where we had to scale our systems within a very tight cost cap to meet our business needs.*

#### 📖┆[Migrating from Postgres to ScyllaDB, with 349X Faster Query Processing](https://scylladb.medium.com/migrating-from-postgres-to-scylladb-with-349x-faster-query-processing-c277fe18801b)

✍ [ScyllaDB](https://scylladb.medium.com/?source=post_page-----c277fe18801b--------------------------------)

> *How Coralogix cut processing times from 30 seconds to 86 milliseconds with a PostgreSQL to ScyllaDB migration*

#### 📖┆[Databases Are Falling Apart: Database Disassembly and Its Implications](https://materializedview.io/p/databases-are-falling-apart)

✍ [Chris Riccomini](https://substack.com/profile/69592459-chris-riccomini)

> *A recent trend in the database world is to break databases into their constituent components. Each component is provided on its own so infrastructure engineers can integrate them into databases. In this post, I discuss the history of database disassembly, the industry’s current state, where we’re heading, and the implications of this trend.*

#### 📖┆[Snowpipe Streaming Deep Dive](https://blog.yuvalitzchakov.com/snowpipe-streaming-deep-dive/)

✍ [Yuval Itzchakov](https://www.linkedin.com/in/yuvalitzchakov/)

> *In this blog post, we are going to dive into the implementation details of [Snowpipe Streaming](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-streaming-overview).*

#### 📖┆[Serverless ClickHouse Cloud - ASDS Chapter 5 (Part 2)](https://jack-vanlightly.com/analyses/2024/1/23/serverless-clickhouse-cloud-asds-chapter-5-part-2)

✍ [Jack Vanlightly](https://jack-vanlightly.com/home)

> *In part 1 we looked at the open-source ClickHouse architecture, in part 2 we dive into the serverless architecture of ClickHouse Cloud.*

#### 📖┆[Data Storage and Indexing](https://natecornell.com/blog/DDIA/Data-Storage-and-Indexing.html)

✍ [Nate Cornell](https://www.linkedin.com/in/nate-cornell)

> *Welcome to the second installment of my blog series on the system architecture lessons from the book Designing Data-Intensive Applications by Martin Kleppman. In this episode, we're gonna talk about database internals, such as storage, query languages, and indexes.*

#### 📖┆[GitHub’s Engineering Fundamentals program: How we deliver on availability, security, and accessibility](https://github.blog/2024-02-08-githubs-engineering-fundamentals-program-how-we-deliver-on-availability-security-and-accessibility/)

✍ [Deepthi Rao Coppisetty](https://github.com/pegasus1973)

> *How do we ensure over 100 million users across the world have uninterrupted access to GitHub’s products and services on a platform that is always available, secure, and accessible?*

#### 📖┆[Paper Notes: Windows Azure Storage – A Highly Available Cloud Storage Service with Strong Consistency](https://distributed-computing-musings.com/2024/02/paper-notes-windows-azure-storage-a-highly-available-cloud-storage-service-with-strong-consistency/)

✍ [Varun Upadhyay](https://www.linkedin.com/in/varunu28/)

> *Windows Azure Storage (at the time of this paper) is used inside Microsoft for various applications such as social-media search, game content etc. WAS provides strong consistency & even goes on to claim support for all three properties of CAP theorem.*

#### 📖┆[Simple Precision Time Protocol at Meta](https://engineering.fb.com/2024/02/07/production-engineering/simple-precision-time-protocol-sptp-meta/)

✍ [Oleg Obleukhov](https://engineering.fb.com/author/oleg-obleukhov/) + [Ahmad Byagowi](https://engineering.fb.com/author/ahmad-byagowi/)

> *While deploying Precision Time Protocol (PTP) at Meta, we’ve developed a simplified version of the protocol (Simple Precision Time Protocol – SPTP), that can offer the same level of clock synchronization as unicast PTPv2 more reliably and with fewer resources.*

#### 📖┆[DotSlash: Simplified executable deployment](https://engineering.fb.com/2024/02/06/developer-tools/dotslash-simplified-executable-deployment/)

✍ [Michael Bolin](https://engineering.fb.com/author/michael-bolin/) + [Andres Suarez](https://engineering.fb.com/author/andres-suarez/)

> *We’ve open sourced DotSlash, a tool that makes large executables available in source control with a negligible impact on repository size, thus avoiding I/O-heavy clone operations.*

#### 📖┆[Dealing with diverged git branches](https://jvns.ca/blog/2024/02/01/dealing-with-diverged-git-branches/)

✍ [Julia Evans](https://jvns.ca/about/)

> *One of the most common problems I see folks struggling with in Git is when a local branch (like main) and a remote branch (maybe also called main) have diverged.*

#### 📖┆[Why SQL is Unkillable](https://buttondown.email/jaffray/archive/why-sql-is-unkillable/)

✍ [Justin Jaffray](https://justinjaffray.com/)

> *I've thought a lot about the question of why SQL is such a cockroach. It seems surprising to me that we have so, so many different programming languages, but only a handful of query languages, and in the realm of general-purpose data manipulation, really only SQL stands tall.*

#### 📖┆[The Changing “Guarantees” Given by Python's Global Interpreter Lock](https://stefan-marr.de/2023/11/python-global-interpreter-lock/)

✍ [Stefan Marr](https://twitter.com/smarr)

> *In this blog post, I will look into the implementation details of CPython’s Global Interpreter Lock (GIL) and how they changed between Python 3.9 and the current development branch that will become Python 3.13.*

---

# ✏ Data

> *The one thing that this job has taught me is that truth is stranger than fiction. — Predestination (2014)*

#### 📖┆[How I scaled my $1m/year revenue startup's data model](https://blog.dataengineer.io/p/how-i-scaled-my-1myear-revenue-startups)

✍ [Zach Wilson](https://substack.com/@eczachly)

> *When I started building my [learning platform](https://www.dataexpert.io/), I wanted to keep the data model as simple as I possibly could since I was a team of one and couldn’t afford complexity. As my startup grew, I hired more people and realized the simplicity of my original data model started to be a limiting factor!*

#### 📖┆[How Dashboard Trees Work and Why](https://sqlpatterns.com/p/how-dashboard-trees-work-and-why)

✍ [Ergest Xheblaati](https://substack.com/@ergestx)

> *This dashboard sprawl is not free. There are obvious operational costs associated with it: cloud computing costs and data storage costs. Many of the dashboards require long-running, expensive SQL queries executed daily (or even hourly).*

#### 📖┆[This dashboard could've been a… spreadsheet?](https://dramaticanalyst.substack.com/p/this-dashboard-couldve-been-a-spreadsheet)

✍ [Elena Dyachkova](https://substack.com/profile/6307649-elena-dyachkova)

> *Taming dashboard sprawl is a hot topic - I’ve faced this challenge too. Today I will let you in on a secret: my most powerful dashboard ever was built in Google Sheets. And I had to manually update it*

#### 📖┆[Data Dictionary: How I Learned to Stop Worrying and Love Reporting Standardization](https://klaviyo.tech/data-dictionary-how-i-learned-to-stop-worrying-and-love-reporting-standardization-2c756a226549)

✍ [Travis Hansen](https://medium.com/@travishansen23)

> *Klaviyo processes several billion events per day representing everything from email deliveries to in-store visits to loyalty point redemptions. Each of these events can contain any number of arbitrary dimensions, ranging from standard ones like country\_code to user-specified ones like gift\_card\_occasion. With a tremendous amount of data like this comes the need for a large number of reports to allow our customers to understand that data.*

#### 📖┆[The Data ROI Pyramid: A Method for Measuring & Maximizing Your Data Team](https://towardsdatascience.com/the-data-roi-pyramid-a-method-for-measuring-maximizing-your-data-team-cab470b98cf6)

✍ [Barr Moses](https://barrmoses.medium.com/)

> *Struggling to articulate the value of your data team? Learn how to calculate your data team’s return with the Data ROI Pyramid.*

---

# 🤖 AI┆ML┆Data Science

> *You know, Burke, I don’t know which species is worse. — Ripley, Aliens (1986)*

#### 📖┆[Unveiling the Core of Instacart’s Griffin 2.0: A Deep Dive Into the Model Serving Platform](https://tech.instacart.com/unveiling-the-core-of-instacarts-griffin-2-0-a-deep-dive-into-the-model-serving-platform-4a7298c0a54e)

✍ [Zihan Li](https://medium.com/@james.zihan.li)

> *In this post, we will go deeper into how we evolved the model serving system from Griffin 1.0 to Griffin 2.0, to improve the above aspects while also improving ease of use.*

#### 📖┆[The Building Blocks of LLMs: Vectors, Tokens and Embeddings](https://thenewstack.io/the-building-blocks-of-llms-vectors-tokens-and-embeddings/)

✍ [Janakiram MSV](https://thenewstack.io/author/janakiram/)

> *Understanding vectors, tokens and embeddings is fundamental to grokking how large language models process language.*

---

# 🔥 Catch up

> *…Next Saturday night, we're sending you back to the future! — Dr. Emmett Brown, Back to the Future (1985)*

#### 📖┆[BigQuery | Introduction to entity resolution in BigQuery](https://cloud.google.com/bigquery/docs/entity-resolution-intro)

#### 📖┆[BigQuery | Create custom masking routines](https://cloud.google.com/bigquery/docs/user-defined-functions#custom-mask)

#### 📖┆[BigQuery | Can now view query plans to see details of SQL pushdowns in federated queries](https://cloud.google.com/bigquery/docs/query-plan-explanation#explanation_for_federated_queries)

#### 📖┆[BigQuery | Billing for Spark stored procedures begins on March 12, 2024. Until that date, Spark stored procedures are offered at no extra cost.](https://cloud.google.com/bigquery/docs/spark-procedures#pricing)

#### 📖┆[DuckDB | Multi-Database Support in DuckDB](https://duckdb.org/2024/01/26/multi-database-support-in-duckdb.html)

---

# 💠 Previously on Dimension

> *Dimension is my sub-newsletter where I note down things I learn from people smarter than me in the data engineering field.*

Here are the 3 latest articles:

### ***Published on 2024, January 27:***

### ***Published on 2024, February 3:***

### ***Published on 2024, February 10:***

Let me here your voice, for example:

'Your newsletter is so terrible, I can't handle it anymore.'

[Leave a comment](https://vutr.substack.com/p/groupby-22-navigating-the-data-engineering/comments)

---

## “Hasta la vista, baby” -T800, Terminator 2: Judgment Day (1991)

Thanks for scrolling this far! There's a convenient subscribe box here if you want me to annoy you every week. 😄
