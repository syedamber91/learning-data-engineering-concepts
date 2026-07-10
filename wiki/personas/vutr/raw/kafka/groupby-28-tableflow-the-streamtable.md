---
title: "GroupBy #28: Tableflow - The Stream/Table, Kafka/Iceberg Duality, Kafka tiered storage deep dive"
channel: vutr
author: "Vu Trinh"
published: 2024-03-26
url: https://vutr.substack.com/p/groupby-28-tableflow-the-streamtable
paid: false
topics: ["Data Engineering", "dbt", "Apache Kafka", "Apache Iceberg", "Apache Flink", "BigQuery", "Streaming", "Change Data Capture", "Data Quality", "Data Governance"]
tags: [https, kafka, substack, blog, medium, engineering]
---

# GroupBy #28: Tableflow - The Stream/Table, Kafka/Iceberg Duality, Kafka tiered storage deep dive

*Plus: dbt’s Model Contracts for Dummies, The Problem with Data Governance*

> Source: [Open post](https://vutr.substack.com/p/groupby-28-tableflow-the-streamtable)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-kafka|Apache Kafka]] · [[apache-iceberg|Apache Iceberg]] · [[apache-flink|Apache Flink]] · [[bigquery|BigQuery]] · [[streaming|Streaming]] · [[change-data-capture|Change Data Capture]] · [[data-quality|Data Quality]] · [[data-governance|Data Governance]]

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

[![](https://substackcdn.com/image/fetch/$s_!e4RU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F845b4265-23a9-4ebd-8157-f66831b89c97_1400x1000.png)](https://substackcdn.com/image/fetch/$s_!e4RU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F845b4265-23a9-4ebd-8157-f66831b89c97_1400x1000.png)

Image created by the Canva Image Generator.

---

# 📈 Career

> *Don't let comfort hold you back.*

#### 📖┆[How to Start Google](https://paulgraham.com/google.html)

✍ [Paul Graham](https://paulgraham.com/bio.html)

> *Starting your own company can mean anything from starting a barber shop to starting Google. I'm here to talk about one extreme end of that continuum. I'm going to tell you how to start Google.*

#### 📖┆[How to convert your yearly review to a promotion in big tech](https://blog.dataengineer.io/p/how-to-convert-your-yearly-review)

✍ [Zach Wilson](https://substack.com/@eczachly)

> *The dreaded review cycle usually comes once or twice a year at companies. For most this process is annoying or anxiety-provoking. It is also one of the most critical moments for advancing your career with interviewing well being the only one thing that’s more critical!*

#### 📖┆[Leadership requires taking some risk](https://lethain.com/leadership-requires-risk/)

✍ [Will Larson](https://lethain.com/about/)

> *At a recent offsite with Carta’s Navigators, we landed on an interesting topic: leadership roles sometimes mean that making progress on a professional initiative requires taking some personal risk.*

---

# 🚀 Engineering

> *I have to believe in a world outside my own mind. — Memento (2000)*

#### 📖┆[Unexplanations: sql is syntactic sugar for relational algebra](https://www.scattered-thoughts.net/writing/unexplanations-sql-is-syntactic-sugar-for-relational-algebra/)

✍ [Jamie Brandon](https://www.scattered-thoughts.net/)

> *This idea is particularly sticky because it was more or less true 50 years ago, and it's a passable mental model to use when learning sql. But it's an inadequate mental model for building new sql frontends, designing new query languages, or writing tools likes ORMs that abstract over sql.*

#### 📖┆[Tableflow: The Stream/Table, Kafka/Iceberg Duality](https://t.co/r8Op8DakEm)

✍ [Jack Vanlightly](https://jack-vanlightly.com/home)

> *Confluent just announced Tableflow, the seamless materialization of Apache Kafka topics as Apache Iceberg tables. This announcement has to be the most impactful announcement I’ve witnessed while at Confluent. This post is about why Iceberg tables aren’t just another destination to sync data to; they fundamentally change the world of streaming. It’s also about the macro trends that have led us to this point and why Iceberg (and the other table formats) are so important to the future of streaming.*

#### 📖┆[Kafka tiered storage deep dive](https://developers.redhat.com/articles/2024/03/13/kafka-tiered-storage-deep-dive)

✍ [Federico Valeri](https://developers.redhat.com/author/federico-valeri) + [Luke Chen](https://developers.redhat.com/author/luke-chen)

> *Tiered storage is a new early access feature available as of Apache Kafka 3.6.0 that allows you to scale compute and storage resources independently, provides better client isolation, and allows faster maintenance of your Kafka cluster. Let's dive into this new feature to see the motivations, design, and implementation details. In this post, we will focus on Tiered storage implementation, so it is assumed a good understanding of the Kafka architecture and main components*

#### 📖┆[Consumer-Driven Contract Testing (CDCT)](https://medium.com/insiderengineering/consumer-driven-contract-testing-cdct-b6c05c18ba25?source=rss----80f9de3e9a8a---4)

✍ [Mihriban Kumarci](https://medium.com/@mihribankmrci?source=post_page-----b6c05c18ba25--------------------------------)

> *Consumer-Driven Contract (CDC) Testing is gaining prominence in microservices architecture. It offers an efficient way to ensure that services meet their contracts without exhaustive end-to-end tests..*

#### 📖┆[TimescaleDB and the Quest for the Ultimate Time Series Database: Growth, Challenges, and Strategic Moves](https://www.thdpth.com/p/timescaledb-and-the-quest-for-the)

✍ [Sven Balnojan PhD](https://substack.com/profile/229923-sven-balnojan-phd)

> *The one key question I want to dive into today is…. Is Timescale able to handle the coming torrent? Will they be swept away or catch the current and grow absurdly quickly?*

#### 📖┆[Python @ Picnic](https://medium.com/picnic-engineering/python-picnic-590819d066d8)

✍ [Sven Arends](https://medium.com/@svena33)

> *From Machine Learning to black box testing of Java services, Picnic uses Python throughout its tech stack. Learn why Picnic chose Python and how we leverage its flexibility at scale.*

#### 📖┆**[Every dunder method in Python](https://www.pythonmorsels.com/every-dunder-method/)**

✍ [Trey Hunner](https://www.pythonmorsels.com/)

> *Python includes tons of [dunder methods](https://www.pythonmorsels.com/what-are-dunder-methods/) ("double underscore" methods) which allow us to deeply customize how our custom classes interact with Python's many features. What dunder methods could you add to your class to make it friendly for other Python programmers who use it?*

#### 📖┆[Real-time Fraud Detection with Yoda and ClickHouse](https://medium.com/tech-at-instacart/real-time-fraud-detection-with-yoda-and-clickhouse-bd08e9dbe3f4)

✍ [Nick Shieh](https://medium.com/@nicholas.shieh)

> *Our Fraud Platform team developed Yoda, a decision platform service, to detect such fraudulent activities quickly and take appropriate measures.To enable fraud decisions in fractions of a second, Yoda uses ClickHouse as its primary real-time datastore. ClickHouse is a fast and highly performant analytical database, widely used across Instacart to power other use-cases such as critical retailer and ads dashboards, calculating results for A/B testing, and machine learning signals.*

---

# ✏ Data

> *The one thing that this job has taught me is that truth is stranger than fiction. — Predestination (2014)*

#### 📖┆[dbt’s Model Contracts for Dummies](https://faithfacts.substack.com/p/dbts-model-contracts-for-dummies)

✍ [Faith Lierheimer](https://substack.com/profile/11412853-faith-lierheimer)

> *So yeah. The Data Contracts Content Explosion on the Data Internet was fucking exhausting. Unfortunately, it was on to an important idea.*

#### 📖┆[The Problem with Data Governance](https://eric-sandosham.medium.com/the-problem-with-data-governance-2570f0573f3a)

✍ [Eric Sandosham, Ph.D.](https://eric-sandosham.medium.com/?source=post_page-----2570f0573f3a--------------------------------)

> *Over the years, Data Governance has lost much of its lustre having been unable to show much business impact. But what exactly is Data Governance? Has it evolved beyond data quality and data access? How does it square up with the emergence of AI solutioning? And so I dedicate my 29th weekly article to discussing the topic of whether Data Governance as a practice still makes sense.*

---

# 🤖 AI┆ML┆Data Science

> *You know, Burke, I don’t know which species is worse. — Ripley, Aliens (1986)*

#### 📖┆[Let's talk about AI...](https://roundup.getdbt.com/p/lets-talk-about-ai)

✍ [Tristan Handy](https://substack.com/@jthandy)

> *The integration of structured data and AI will be driven by metadata. And dbt’s biggest role to play in the AI revolution will be as the source of truth for that metadata.*

#### 📖┆[Logarithm: A logging engine for AI training workflows and services](https://engineering.fb.com/2024/03/18/data-infrastructure/logarithm-logging-engine-ai-training-workflows-services-meta/)

✍ [Partha Kanuparthy](https://engineering.fb.com/author/partha-kanuparthy/)

> *Logarithm is a hosted, serverless, multitenant service, used only internally at Meta, that consumes and indexes these logs and provides an interactive query interface to retrieve and view logs. In this post, we present the design behind Logarithm, and show how it powers AI training debugging use cases.*

#### 📖┆[Model Excellence Scores: A Framework for Enhancing the Quality of Machine Learning Systems at Scale](https://www.uber.com/blog/enhancing-the-quality-of-machine-learning-systems-at-scale/)

✍ [Uber Engineering Blog](https://www.uber.com/blog/)

> *By integrating the Service Level Agreement (SLA) concept, we aim to establish a standard for measuring and ensuring ML model quality.*

#### 📖┆[Optimizing RTC bandwidth estimation with machine learning](https://engineering.fb.com/2024/03/20/networking-traffic/optimizing-rtc-bandwidth-estimation-machine-learning/)

✍ [Santhosh Sunderrajan](https://engineering.fb.com/author/santhosh-sunderrajan/)

> *We’ve adopted a machine learning (ML)-based approach that allows us to solve networking problems holistically across cross-layers such as BWE, network resiliency, and transport. We’re sharing our experiment results from this approach, some of the challenges we encountered during execution, and learnings for new adopters.*

#### 📖┆[Sequential A/B Testing Keeps the World Streaming Netflix Part 2: Counting Processes](https://medium.com/netflix-techblog/sequential-testing-keeps-the-world-streaming-netflix-part-2-counting-processes-da6805341642)

✍ [Netflix Technology Blog](https://netflixtechblog.medium.com/)

> *Netflix monitors a large suite of metrics, many of which can be classified as counts. These include metrics such as the number of logins, errors, successful play starts, and even the number of customer call center contacts. In this second installment, we describe our sequential methodology for testing count metrics, outlined in the NeurIPS paper Anytime Valid Inference for Multinomial Count Data.*

#### 📖┆[Bye Bye Bye...: Evolution of repeated token attacks on ChatGPT models](https://dropbox.tech/machine-learning/bye-bye-bye-evolution-of-repeated-token-attacks-on-chatgpt-models)

✍ [Mark Breitenbach](https://www.linkedin.com/in/markbreitenbach/) + [Adrian Wood](https://www.linkedin.com/in/adrian-wood-threlfall/)

> *This blog will discuss the steps taken to execute the repeated token attack on ChatGPT models at various points from October 2023 through March 2024—before, during, and after OpenAI’s filtering mitigation was deployed.*

---

# 🔥 Catch up

> *…Next Saturday night, we're sending you back to the future! — Dr. Emmett Brown, Back to the Future (1985)*

📖┆[dbt 1.8.0](https://github.com/dbt-labs/dbt-core/blob/v1.8.0b1/CHANGELOG.md?ref=blef.fr)

📖┆[Apache Flink 1.19](https://www.confluent.io/blog/exploring-apache-flink-1-19/)

📖┆[Apache Kafka 3.7](https://www.confluent.io/blog/introducing-apache-kafka-3-7/)

📖┆[BigQuery | Incremental materialized views now support](https://cloud.google.com/bigquery/docs/materialized-views-create#left-union) `LEFT OUTER JOIN` and `UNION ALL`.

📖┆[Microsoft introduces Garnet, a new remote cache-store](https://www.microsoft.com/en-us/research/blog/introducing-garnet-an-open-source-next-generation-faster-cache-store-for-accelerating-applications-and-services/)

📖┆[X AI open-sources Grok](https://github.com/xai-org/grok-1)

📖┆[Confluent introduces Tableflow](https://www.confluent.io/blog/introducing-tableflow/)

---

# 💠 Previously on Dimension

> *Dimension is my sub-newsletter where I note down things I learn from people smarter than me in the data engineering field.*

Here are the 3 latest articles:

### ***Published on 2024, March 9:***

### ***Published on 2024, March 16:***

### ***Published on 2024, March 23:***

Let me here your voice, for example:

'Your newsletter is so terrible, I can't handle it anymore.'

[Leave a comment](https://vutr.substack.com/p/groupby-28-tableflow-the-streamtable/comments)

---

## “Hasta la vista, baby” -T800, Terminator 2: Judgment Day (1991)

Thanks for scrolling this far! There's a convenient subscribe box here if you want me to annoy you every week. 😄
