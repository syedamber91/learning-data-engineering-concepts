---
title: "GroupBy #25: From Samza to Flink: A Decade of Stream Processing, DoorDash’s In-House Search Engine,Meta's DotSlash, Designing Metrics Trees"
channel: vutr
author: "Vu Trinh"
published: 2024-03-05
url: https://vutr.substack.com/p/groupby-25-from-samza-to-flink-a
paid: false
topics: ["Data Engineering", "dbt", "Apache Kafka", "Apache Spark", "Apache Flink", "Databricks", "BigQuery", "Lakehouse", "Streaming", "Batch Processing"]
tags: [https, blog, databricks, apache, substack, auto]
---

# GroupBy #25: From Samza to Flink: A Decade of Stream Processing, DoorDash’s In-House Search Engine,Meta's DotSlash, Designing Metrics Trees

*Plus: How to go from senior to staff data engineer in big tech, Apache Kafka 3.7, PyAirbyte*

> Source: [Open post](https://vutr.substack.com/p/groupby-25-from-samza-to-flink-a)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-flink|Apache Flink]] · [[databricks|Databricks]] · [[bigquery|BigQuery]] · [[lakehouse|Lakehouse]] · [[streaming|Streaming]] · [[batch-processing|Batch Processing]]

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

## Referral Program

I’m launching a referral program to grow the community by giving you guys valuable gifts whenever you reach a referral milestone. The condition is simple: you refer friends to subscribe to my newsletter, and you will receive a gift based on the number of friends you refer. Here are the reward milestones:

[![](https://substackcdn.com/image/fetch/$s_!lf_-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4c72d52-a2c4-4e24-9714-04e72a4dc087_756x361.png)](https://substackcdn.com/image/fetch/$s_!lf_-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4c72d52-a2c4-4e24-9714-04e72a4dc087_756x361.png)

Now, let’s refer friends and claim exciting rewards ;)

[Refer a friend](https://vutr.substack.com/leaderboard?&referrer_token=1xrjxy&utm_source=post)

---

[![](https://substackcdn.com/image/fetch/$s_!NYLk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc8f97dde-1b1e-4cfd-a4a2-9816665c1e68_1400x1000.png)](https://substackcdn.com/image/fetch/$s_!NYLk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc8f97dde-1b1e-4cfd-a4a2-9816665c1e68_1400x1000.png)

---

# 📈 Career

> *Don't let comfort hold you back.*

#### 📖┆[Career Pathways of Data Engineers](https://blog.det.life/career-pathways-of-data-engineers-2bc4465483d0)

✍ [Ravi Ganta](https://medium.com/@grkumar82?source=post_page-----2bc4465483d0--------------------------------)

> *The career progression for Data Engineers is not a linear journey, unlike what might be expected. A straightforward trajectory, similar to that of Software Engineers ascending from entry-level individual contributors to executive leadership roles, does not necessarily apply to Data Engineers. This discourse delves into the intricate pathways that Data Engineers can undertake as they advance in their careers.*

#### 📖┆[How to go from senior to staff data engineer in big tech](https://blog.dataengineer.io/p/how-to-go-from-senior-to-staff-data)

✍ [Zach Wilson](https://substack.com/profile/10367987-zach-wilson)

> *In big tech, less than 3% of engineers make it to the staff level! If you want to beat the odds and actually become an L6+ engineer, this newsletter is for you. In my time in big tech, I went from junior to staff data engineer in four years. I’ll unveil the learnings I have from that journey.*

---

# 🚀 Engineering

> *I have to believe in a world outside my own mind. — Memento (2000)*

#### 📖┆[From Samza to Flink: A Decade of Stream Processing](https://materializedview.io/p/from-samza-to-flink-a-decade-of-stream)

✍ [Chris Riccomini](https://substack.com/profile/69592459-chris-riccomini)

> *I started Apache Samza twelve years ago during my tenure at LinkedIn. Samza was a stream processing framework built for Apache Kafka. The team grew to include all-stars like Martin Kleppmann, Chinmay Soman, Jakob Homan, Yi Pan, and many other talented engineers. Together, we added support for stateful processing, batch processing, SQL, YARN, standalone deployment, and many other features you see in modern stream processing systems. I learned a lot building Samza. In this post, I want to review Samza’s history, look at lessons learned, and talk about how these lessons affect my thinking on Apache Flink.*

#### 😉 Two-parts article:

#### Part 1: 📖┆[Performance Improvements for Stateful Pipelines in Apache Spark Structured Streaming](https://www.databricks.com/blog/performance-improvements-stateful-pipelines-apache-spark-structured-streaming)

✍ [Mojgan Mazouchi](https://www.databricks.com/blog/author/mojgan-mazouchi) + [Mrityunjay Kumar](https://www.databricks.com/blog/author/mrityunjay-kumar) + [Anish Shrigondekar](https://www.databricks.com/blog/author/anish-shrigondekar) + [Karthikeyan Ramasamy](https://www.databricks.com/blog/author/karthikeyan-ramasamy)

> *Apache Spark™ [Structured Streaming](https://spark.apache.org/streaming/) is a popular open-source stream processing platform that provides scalability and fault tolerance, built on top of the Spark SQL engine. Most incremental and [streaming workloads](https://www.databricks.com/product/data-streaming) on the Databricks Lakehouse Platform are powered by Structured Streaming, including [Delta Live Tables](https://www.databricks.com/product/delta-live-tables) and [Auto Loader](https://docs.databricks.com/en/ingestion/auto-loader/index.html).*

#### Part 2: 📖┆[A Deep Dive into the Latest Performance Improvements of Stateful Pipelines in Apache Spark Structured Streaming](https://www.databricks.com/blog/deep-dive-latest-performance-improvements-stateful-pipelines-apache-spark-structured-streaming)

✍ [Mojgan Mazouchi](https://www.databricks.com/blog/author/mojgan-mazouchi) + [Mrityunjay Kumar](https://www.databricks.com/blog/author/mrityunjay-kumar) + [Anish Shrigondekar](https://www.databricks.com/blog/author/anish-shrigondekar) + [Karthikeyan Ramasamy](https://www.databricks.com/blog/author/karthikeyan-ramasamy)

> *In this section, we will dig deeper into the various issues we observed while analyzing performance and outline specific enhancements we have implemented to address those issues.*

#### 📖┆[Everything Ops: Beyond the Hype](https://medium.pimpaudben.fr/everything-ops-beyond-the-hype-e19d2f763b40)

✍ [Benoit Pimpaud](https://medium.pimpaudben.fr/?source=post_page-----e19d2f763b40--------------------------------)

> *Integrating “Ops” into our job titles and conceptual terms may come across as trendy, and indeed, it is.*

#### 📖┆[lakeFS: Where’s my data?](https://lakefs.io/blog/where-is-my-data/)

✍ [Ariel Shaqed (Scolnicov)](https://www.linkedin.com/in/ariels)

> *For a data management platform, sometimes it may seem as though lakeFS takes pains to hide your data. Indeed, one very common question on our Slack #help channel is a polite variation on “where’s my data?”. lakeFS does indeed keep your data and it does so inside your namespace. This core functionality works and is well-tested. But lakeFS does such a great job of abstracting away all of these details that it’s hard to find the data!*

#### 📖┆[Introducing DoorDash’s In-House Search Engine](https://doordash.engineering/2024/02/27/introducing-doordashs-in-house-search-engine/)

✍ [Konstantin Shulgin](https://www.linkedin.com/in/kostya-shulgin/) + [Satish Subhashrao Saley](https://www.linkedin.com/in/satish-saley-65527525/) + [Anish Walawalkar](https://www.linkedin.com/in/anish-walawalkar-a9221989/)

> *We decided the best way to address these challenges was to move away from Elasticsearch to a homegrown search engine. We chose Apache Lucene as the core of the new search engine. The Search Engine uses a segment-replication model and separates indexing and searching traffic. We designed the index to store multiple types of documents with relations between them. Following the migration to DoorDash’s Search Engine, we saw a 50% p99.9 latency reduction and a 75% hardware cost decrease.*

#### 📖┆[Query Builder Package: From Individual Chaos to Collective Consistency](https://medium.com/insiderengineering/query-builder-package-from-individual-chaos-to-collective-consistency-669503cb3696)

✍ [Sinem Elif Haseki](https://medium.com/@sinem.haseki?source=post_page-----669503cb3696--------------------------------)

> *In the dynamic world of software development, aligning multiple products with consistent and efficient service request protocols is a critical challenge. This article delves into the role of a new query builder package in revolutionizing this process, emphasizing its necessity, benefits, and drawbacks.*

#### 📖┆[How DotSlash makes executable deployment simpler](https://engineering.fb.com/2024/02/26/developer-tools/dotslash-meta-tech-podcast/)

✍ [Pascal Hartig](https://engineering.fb.com/author/pascal-hartig/)

> *Andres Suarez and Michael Bolin, two software engineers at Meta, join Pascal Hartig (@passy) on the Meta Tech Podcast to discuss the ins and outs of DotSlash, a new open source tool from Meta.*

#### 📖┆[We Need a Data Engineering-Specific Language](https://juhache.substack.com/p/we-need-a-data-engineering-specific)

✍ [Julien Hurault](https://substack.com/profile/35734446-julien-hurault)

> *In this article, I explore the present state of standardization within the industry.*

---

# ✏ Data

> *The one thing that this job has taught me is that truth is stranger than fiction. — Predestination (2014)*

#### 📖┆[Designing Metrics Trees](https://sqlpatterns.com/p/designing-metrics-trees)

✍ [Ergest Xheblati](https://substack.com/@ergestx)

> *A metric tree is a logical representation of a business’ growth model in a graph form. It’s a simplified representation of how inputs flow into outputs.*

#### 📖┆[How the New York Times Games Data Team Revamped Its Reporting](https://open.nytimes.com/how-the-new-york-times-games-data-team-revamped-its-reporting-8af7e7c7bc97)

✍ [CJ Robinson](https://medium.com/@cj-robinson)

> *Ultimately, our goal is to make the data generation, ingestion, processing, and reporting pipeline as effortless and evergreen as possible.*

#### 📖┆[10 Common Data Visualization Mistakes and How to Avoid Them](https://medium.com/agoda-engineering/10-common-data-visualization-mistakes-and-how-to-avoid-them-e3896fe8e104)

✍ [Agoda Engineering](https://medium.com/@agoda.eng?source=post_page-----e3896fe8e104--------------------------------)

> *When creating data visualizations, it can be easy to make mistakes that lead to wrong interpretations. This article will look at bad data visualization and how to avoid it.*

#### 📖┆[When a Data Mesh Doesn’t Make Sense for Your Organization](https://medium.com/@barrmoses/when-a-data-mesh-doesnt-make-sense-for-your-organization-20de8f3f48bd)

✍ [Barr Moses](https://barrmoses.medium.com/when-a-data-mesh-doesnt-make-sense-for-your-organization-20de8f3f48bd)

> *In this article, we’ll revisit data mesh to discuss what it is, why it makes sense for some teams, and when it doesn’t make sense for yours!*

#### 📖┆[dbt’s Semantic Layer for Dummies](https://faithfacts.substack.com/p/dbts-semantic-layer-for-dummies)

✍ [Faith Lierheimer](https://substack.com/profile/11412853-faith-lierheimer)

> *What’s dbt’s Semantic Layer (powered by MetricFlow baby) supposed to do anyways?*

---

# 🤖 AI┆ML┆Data Science

> *You know, Burke, I don’t know which species is worse. — Ripley, Aliens (1986)*

#### 📖┆[2023 in Review: Recapping the Post-ChatGPT Era and What to Expect for 2024](https://medium.com/towards-data-science/2023-in-review-recapping-the-post-chatgpt-era-and-what-to-expect-for-2024-bb4357a4e827)

✍ [Leonie Monigatti](https://medium.com/@iamleonie)

> *How the LLMOps landscape has evolved and why we haven’t seen many Generative AI applications in the wild yet — but maybe in 2024.*

#### 📖┆[Happy New Year: GPT in 500 lines of SQL](https://explainextended.com/2023/12/31/happy-new-year-15/)

✍ [Quassnoi](https://explainextended.com/)

> *It just proves that if you want something done right, you have to do it yourself. Encouraged by this optimistic forecast, today we will implement a large language model in SQL.*

#### 📖┆[Meta's new LLM-based test generator is a sneak peek to the future of development](https://read.engineerscodex.com/p/metas-new-llm-based-test-generator)

✍ [Engineer’s Codex](https://read.engineerscodex.com/)

> *Meta's TestGen-LLM is a sneak peek to the future of developer productivity: specialized, orchestrated, and rigorously filtered.*

---

# 🔥 Catch up

> *…Next Saturday night, we're sending you back to the future! — Dr. Emmett Brown, Back to the Future (1985)*

#### 📖┆**[Introducing Apache Kafka 3.7](https://www.confluent.io/blog/introducing-apache-kafka-3-7/)**

#### 📖┆[Copilot in PowerBI](https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-evaluate-data)

#### 📖┆[PyAirbyte: Airbyte’s New Python Library for Moving Data.](https://thenewstack.io/pyairbyte-airbytes-new-python-library-for-moving-data/)

#### 📖┆The following BigQuery cross-cloud features are now [generally available](https://cloud.google.com/products/#product-launch-stages) (GA):

> * *You can take advantage of the benefits of [materialized views over Amazon S3 metadata cache-enabled BigLake tables](https://cloud.google.com/bigquery/docs/materialized-views-intro#biglake).*
> * *You can create [materialized view replicas](https://cloud.google.com/bigquery/docs/materialized-views-intro#materialized_view_replicas) of materialized views over Amazon S3 metadata cache-enabled Biglake tables. Materialized view replicas let you use the materialized view data in queries while avoiding data egress costs and improving query performance.*
> * *You can [get information about materialized view replicas](https://cloud.google.com/bigquery/docs/materialized-view-replicas-manage#get-info) by using SQL, the bq command-line tool, or the BigQuery API.*
> * *You can use [cross-cloud joins](https://cloud.google.com/bigquery/docs/biglake-intro#cross-cloud_joins) to run queries that span both Google Cloud and BigQuery Omni regions.*

#### 📖┆BigQuery Materialized views can now [reference logical views](https://cloud.google.com/bigquery/docs/materialized-views-create#reference_logical_views). This feature is in [preview](https://cloud.google.com/products#product-launch-stages).

#### 📖┆BigQuery [GROUP BY ALL clause, which groups rows by inferring grouping keys from the SELECT items, is now in preview](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#group_by_all)

---

# 💠 Previously on Dimension

> *Dimension is my sub-newsletter where I note down things I learn from people smarter than me in the data engineering field.*

Here are the 3 latest articles:

### ***Published on 2024, February 17:***

### ***Published on 2024, February 24:***

### ***Published on 2024, March 2:***

Let me here your voice, for example:

'Your newsletter is so terrible, I can't handle it anymore.'

[Leave a comment](https://vutr.substack.com/p/groupby-25-from-samza-to-flink-a/comments)

---

## “Hasta la vista, baby” -T800, Terminator 2: Judgment Day (1991)

Thanks for scrolling this far! There's a convenient subscribe box here if you want me to annoy you every week. 😄
