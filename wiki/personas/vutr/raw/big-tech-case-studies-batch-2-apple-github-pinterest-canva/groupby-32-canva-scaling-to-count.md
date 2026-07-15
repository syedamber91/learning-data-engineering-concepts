---
title: "GroupBy #32: Canva - Scaling to Count Billions, Ensuring Precision and Integrity: A Deep Dive into Uber’s Accounting Data Testing Strategies"
channel: vutr
author: "Vu Trinh"
published: 2024-04-23
url: https://vutr.substack.com/p/groupby-32-canva-scaling-to-count
paid: false
topics: ["Data Engineering", "Apache Airflow", "Apache Kafka", "Apache Flink", "Databricks", "BigQuery", "Data Lake", "Lakehouse", "Orchestration", "Streaming"]
tags: [https, blog, engineering, apache, building, medium]
---

# GroupBy #32: Canva - Scaling to Count Billions, Ensuring Precision and Integrity: A Deep Dive into Uber’s Accounting Data Testing Strategies

*Plus: LLM fine-tuning and evaluation in BigQuery, How We Built Slack AI To Be Secure and Private*

> Source: [Open post](https://vutr.substack.com/p/groupby-32-canva-scaling-to-count)

## Topics

[[data-engineering|Data Engineering]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[apache-flink|Apache Flink]] · [[databricks|Databricks]] · [[bigquery|BigQuery]] · [[data-lake|Data Lake]] · [[lakehouse|Lakehouse]] · [[orchestration|Orchestration]] · [[streaming|Streaming]]

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

[![](https://substackcdn.com/image/fetch/$s_!S6i3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F65aa6a69-d37c-44bb-ba67-5053990d9c00_1400x1000.png)](https://substackcdn.com/image/fetch/$s_!S6i3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F65aa6a69-d37c-44bb-ba67-5053990d9c00_1400x1000.png)

Image created by the Canva Image Generator.

---

# 📈 Career

> *Don't let comfort hold you back.*

#### 📖┆[Principal Engineer](https://blog.alexewerlof.com/p/principal-engineer)

✍ [Alex Ewerlöf](https://substack.com/profile/87732486-alex-ewerlof)

> *Just as going from Senior Engineer to Staff Engineer required a new skill (soft skills), the Principal Engineer requires a new skill: business skills.*

---

# 🚀 Engineering

> *I have to believe in a world outside my own mind. — Memento (2000)*

#### 📖┆[Scaling to Count Billions](https://www.canva.dev/blog/engineering/scaling-to-count-billions/)

✍ [Sangzhuoyang Yu](https://www.linkedin.com/in/yuszy/)

> *Since we launched the program 3 years ago, usage of our creator content has doubled every 18 months. Now we pay creators based on billions of content usages each month. This usage data not only includes templates but also images, videos, and so on. Building and maintaining a service to track this data for payment is challenging. This blog post introduces the various architectures we’ve experimented with and the lessons we learned along the way.*

#### 📖┆[Ensuring Precision and Integrity: A Deep Dive into Uber’s Accounting Data Testing Strategies](https://www.uber.com/en-SG/blog/accounting-data-testing-strategies/)

✍ [Uber Engineering Blog](https://www.uber.com/en-US/blog/engineering/)

> *To maintain these tenets, Financial Accounting Services (FAS) Platform has built robust testing, monitoring, and alerting processes. This encompasses system configuration, business accounting, and external financial report generation.*

#### 📖┆[Lakehouse Data Platform on Kubernetes](https://medium.com/datareply/lakehouse-data-platform-on-kubernetes-e8dca2abc6f4)

✍ [Majid Azimi](https://medium.com/@majidazimi?source=post_page-----e8dca2abc6f4--------------------------------)

> *Building such a modern, cloud-native lakehouse platform is not only possible but has been made more accessible through the use of open-source technologies. Throughout this article, we will explore the intricacies of a data lakehouse platform, emphasizing how it simplifies the transition to and utilization of data lakehouses. We will also provide a comprehensive guide on constructing an entire data lakehouse ecosystem on Kubernetes, highlighting the steps and strategies involved in leveraging this powerful container-orchestration system to deploy and manage a highly scalable and resilient data platform.*

#### 📖┆[Building Scalable Real Time Event Processing with Kafka and Flink](https://doordash.engineering/2022/08/02/building-scalable-real-time-event-processing-with-kafka-and-flink/)

✍ [Allen Wang](https://www.linkedin.com/in/allen-xiaozhong-wang-97a6925/)

> *At DoorDash, real time events are an important data source to gain insight into our business but building a system capable of handling billions of real time events is challenging. Events are generated from our services and user devices and need to be processed and transported to different destinations to help us make data-driven decisions on the platform.*

#### 📖┆[Ten years of improvements in PostgreSQL's optimizer](https://rmarcus.info/blog/2024/04/12/pg-over-time.html)

✍ [Ryan Marcus](https://discuss.systems/@ryanmarcus)

> *As a query optimization researcher, I’ve spent the last 10 years of my life playing with, learning from, and building on top of the most sophisticated open source query optimizer out there, [PostgreSQL](https://postgresql.org/). I recently wondered how much PostgreSQL had improved over the decade since I started working on databases. While changelogs and opinion pieces were plentiful, I couldn’t find any strong empirical comparisons, so I decided to run the [join order benchmark](https://www.vldb.org/pvldb/vol9/p204-leis.pdf) (JOB) on PostgreSQL 8 through 16. I recorded the 90th percentile query latency for each database version.*

#### 📖┆[DuckDB Meets Apache Arrow](https://medium.com/gooddata-developers/duckdb-meets-apache-arrow-169e917a2d8d)

✍ [Jan Kadlec](https://medium.com/@jkadlec?source=post_page-----169e917a2d8d--------------------------------)

> *You may have heard about DuckDB, Apache Arrow, or both. In this article, I’ll tell you about how we (GoodData) are the first analytics (BI) platform powered by the combination of these technologies. I believe the motivation is evident — performance 🏎️ and developer velocity.*

#### 📖┆[Powering real-time magic moments through notifications](https://medium.com/whatnot-engineering/powering-real-time-magic-moments-through-notifications-36cd833f898e)

✍ [Whatnot Engineering](https://medium.com/@whatnotengineering?source=post_page-----36cd833f898e--------------------------------)

> *Whatnot’s notification system had begun to reach its capacity to expand and meet the organization and our user’s needs. It started as a small class hierarchy in our main python codebase then moved to background tasks powered by RabbitMQ. As time passed, the logic and complexity in the operations grew along with the volume of notifications being sent. In this post, we share our journey building the 3rd iteration of a platform we believe will scale for the long term and share our considerations, hurdles, and lessons learned along the way.*

#### 📖┆[How we Improved Database Development and CI/CD with Storage Snapshot](https://medium.com/agoda-engineering/how-we-improved-database-development-and-ci-cd-with-storage-snapshot-fa0300d80f0f)

✍ [Agoda Engineering](https://medium.com/@agoda.eng?source=post_page-----fa0300d80f0f--------------------------------)

> *Database development is an integral part of software development. However, it demands considerable effort and can present challenges throughout the development and testing stages. At Agoda, we’ve adopted specific methodologies and processes to accelerate and simplify the development workflow. In this blog post, we’ll outline the strategies, insights, and implementation techniques of this process.*

#### 📖┆[The Design of Everyday APIs](https://www.roguelynn.com/talks/everyday-apis/)

✍ [Lynn Root](https://www.roguelynn.com/about/)

> *Implementing an API is an art. It’s the connection between the user and the library itself. How can we optimize that connection to make the experience more pleasing? What makes a user reach for one library over another? What goes into an ergonomic API?*

#### 📖┆[Memgraph Storage Modes Explained](https://memgraph.com/blog/memgraph-storage-modes-explained)

✍ [Katarina Supe](https://www.linkedin.com/in/katarina-supe/)

> *Memgraph is an in-memory graph database that ensures data persistence through ACID compliance by default. While it uses snapshots and write-ahead logs (WAL) for data recovery, in some cases, such additional files and insurance are not necessary. Other databases and analytics tools offer snapshots or WAL, but Memgraph offers both with different storage modes.*

#### 📖┆[How to think about Internal Data Products as a Data Engineer](https://blog.det.life/how-to-think-about-internal-data-products-as-a-data-engineer-42cef9081ebf)

✍ [Hugo Lu](https://medium.com/@hugolu87)

> *In this article we’ll dive into how to think about Internal Data Products as a Data Engineer. We’ll answer some common questions about Data Products. I’ll show you how I think about building your first Data Product too.*

#### 📖┆[Origins of Apache Arrow & Its Role Today](https://www.dremio.com/blog/the-origins-of-apache-arrow-its-fit-in-todays-data-landscape/)

✍ [Dipankar Mazumdar](https://www.linkedin.com/in/dipankar-mazumdar/)

> *This blog details the origins of Apache Arrow and shows how it fits in today’s constantly changing data landscape. The libraries and tools using Arrow illustrate that while data consumers may not directly consume Arrow, they probably have interacted with it underneath the covers and have taken advantage of numerous tasks.*

#### 📖┆[Apache Hudi: From Zero To One (10/10)](https://blog.datumagic.com/p/apache-hudi-from-zero-to-one-1010)

✍ [Shiyan Xu](https://substack.com/profile/147107684-shiyan-xu)

> *Throughout the last nine posts, I have explored Hudi concepts pertinent to release 0.14, ideas that are relevant across most of the 0.x versions. For the blog series finale, I aim to cast a glance into the future and delve into the exciting new features in the upcoming 1.0 release. In doing so, this ending post will effectively accomplish the purpose of the series: guiding readers from the foundational beginnings to the groundbreaking future - from zero to one.*

#### 📖┆[Building a Streaming Lakehouse: Performance Comparison Between Paimon and Hudi](https://www.alibabacloud.com/blog/building-a-streaming-lakehouse-performance-comparison-between-paimon-and-hudi_601013)

✍ [Alibaba Cloud Blog](https://www.alibabacloud.com/blog/)

> *Apache Paimon and Apache Hudi are widely used data lake storage formats with high write throughput and low-latency query performance. This article compares the performance of Paimon and Hudi on Alibaba Cloud EMR and explores their respective roles in building quasi-real-time data warehouses.*

---

# ✏ Data

> *The one thing that this job has taught me is that truth is stranger than fiction. — Predestination (2014)*

#### 📖┆[Data-as-a-Product and Data-Contract: An evolutionary approach to data maturity](https://blog.owulveryck.info/2024/04/09/data-as-a-product-and-data-contract-an-evolutionary-approach-to-data-maturity.html)

✍ [Olivier Wulveryck](https://blog.owulveryck.info/about.html)

> *In recapping, I have always grappled with one question: where does one begin when seeking to implement the data mesh paradigm? Through the journey of exploring this concept, my most recent and profound insight is: the most strategic starting point lies with the data product.*

#### 📖┆[Debugging Your Business with Data](https://sqlpatterns.com/p/debugging-your-business-with-data)

✍ [Ergest Xheblati](https://substack.com/@ergestx)

> *How to diagnose the root cause of a 90% drop in pipeline in 5 minutes. An interview with Abhi Sivasailam and Ankur Chawla of Levers Labs*

---

# 🤖 AI┆ML┆Data Science

> *You know, Burke, I don’t know which species is worse. — Ripley, Aliens (1986)*

#### 📖┆[Notes on how to use LLMs in your product](https://lethain.com/mental-model-for-how-to-use-llms-in-products/)

✍ [Will Larson](https://lethain.com/about/)

> *I’ve been working fairly directly on meaningful applicability of LLMs to existing products for the last year, and wanted to type up some semi-disorganized notes. These notes are in no particular order, with an intended audience of industry folks building products.*

#### 📖┆[How We Built Slack AI To Be Secure and Private](https://slack.engineering/how-we-built-slack-ai-to-be-secure-and-private/)

✍ [Slack Engineering Blog](https://slack.engineering/)

> *Instead, to inform how we built out Slack AI, we started from first principles. We began with our requirements: upholding our existing security and compliance offerings, as well as our privacy principles like “Customer Data is sacrosanct.” Then, through the specific lens of generative AI, our team created a new set of Slack AI principles to guide us*

#### 📖┆[Milestones on Our Journey to Standardize Experimentation at The New York Times](https://open.nytimes.com/milestones-on-our-journey-to-standardize-experimentation-at-the-new-york-times-2c6d32db0281?gi=f847ef798c07)

✍ [Kathy Yang](https://medium.com/@kathy.a.yang)

> *At The New York Times, most product experiments use our internal experimentation platform, ABRA, which is short for A/B Reporting and Allocation architecture. Here’s a look at an early version. A lot has changed since those days, and we want to share some of the things we’ve learned on our standardization journey. While we use other types of experimentation, such as contextual multi-armed bandits, this article is focused specifically around the ways we’ve improved our A/B testing processes.*

---

# 🔥 Catch up

> *…Next Saturday night, we're sending you back to the future! — Dr. Emmett Brown, Back to the Future (1985)*

📖┆[Announcing General Availability of Ray on Databricks](https://www.databricks.com/blog/announcing-general-availability-ray-databricks)

📖┆[Apache Airflow 2.9.0: Dataset and UI Improvements](https://medium.com/apache-airflow/apache-airflow-2-9-0-dataset-and-ui-improvements-dfed574ed530)

📖┆BigQuery: The [quantified](https://cloud.google.com/bigquery/docs/reference/standard-sql/operators#like_operator_quantified) `LIKE` operator is [GA](https://cloud.google.com/products#product-launch-stages). With this operator, you can check a search value for matches against a list of patterns or an array of patterns, using one of these conditions:

* `LIKE ANY`: Checks if at least one pattern matches.
* `LIKE SOME`: Synonym for `LIKE ANY`.
* `LIKE ALL`: Checks if every pattern matches.

📖┆BigQuery now supports [subqueries](https://cloud.google.com/bigquery/docs/reference/standard-sql/subqueries) in [row level access policies](https://cloud.google.com/bigquery/docs/managing-row-level-security#create_or_update_a_row-level_access_policy). This feature is now in public [preview](https://cloud.google.com/products/#product-launch-stages).

📖┆[Introducing LLM fine-tuning and evaluation in BigQuery](https://cloud.google.com/blog/products/data-analytics/bigquery-can-now-fine-tune-models-hosted-in-vertex-ai/)

📖┆[Introducing Meta Llama 3: The most capable openly available LLM to date](https://ai.meta.com/blog/meta-llama-3/)

---

# 💠 Previously on Dimension

> *Dimension is my sub-newsletter where I note down things I learn from people smarter than me in the data engineering field.*

Here are the 3 latest articles:

### ***Published on 2024, April 6:***

### ***Published on 2024, April 13:***

### ***Published on 2024, April 20:***

Let me here your voice, for example:

'Your newsletter is so terrible, I can't handle it anymore.'

[Leave a comment](https://vutr.substack.com/p/groupby-32-canva-scaling-to-count/comments)

---

## “Hasta la vista, baby” -T800, Terminator 2: Judgment Day (1991)

Thanks for scrolling this far! There's a convenient subscribe box here if you want me to annoy you every week. 😄
