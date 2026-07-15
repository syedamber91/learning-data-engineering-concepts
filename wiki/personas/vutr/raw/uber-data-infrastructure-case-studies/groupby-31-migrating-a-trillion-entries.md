---
title: "GroupBy #31: Migrating a Trillion Entries of Uber’s Ledger Data from DynamoDB to LedgerStore, Grab Experiment Decision Engine"
channel: vutr
author: "Vu Trinh"
published: 2024-04-16
url: https://vutr.substack.com/p/groupby-31-migrating-a-trillion-entries
paid: false
topics: ["Data Engineering", "Apache Kafka", "Delta Lake", "BigQuery", "Streaming", "ETL"]
tags: [https, blog, engineering, medium, substack, source]
---

# GroupBy #31: Migrating a Trillion Entries of Uber’s Ledger Data from DynamoDB to LedgerStore, Grab Experiment Decision Engine

*Plus: Airbnb open sourced Chronon - ML Feature Platform, BigQuery data canvas*

> Source: [Open post](https://vutr.substack.com/p/groupby-31-migrating-a-trillion-entries)

## Topics

[[data-engineering|Data Engineering]] · [[apache-kafka|Apache Kafka]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[streaming|Streaming]] · [[etl|ETL]]

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

[![](https://substackcdn.com/image/fetch/$s_!vqDk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd616a43b-c869-420b-b5cc-ecdd5aefbf2b_1400x1000.png)](https://substackcdn.com/image/fetch/$s_!vqDk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd616a43b-c869-420b-b5cc-ecdd5aefbf2b_1400x1000.png)

Image created by Canva Image Generator.

---

# 📈 Career

> *Don't let comfort hold you back.*

#### 📖┆[The 2024 breaking into data engineering roadmap](https://blog.dataengineer.io/p/the-2024-breaking-into-data-engineering?utm_source=post-email-title&publication_id=1644342&post_id=139996630&utm_campaign=email-post-title&isFreemail=true&r=2rj6sg&triedRedirect=true&utm_medium=email)

✍ [Zach Wilson](https://substack.com/profile/10367987-zach-wilson)

> *Knowing where to start and how to get a handle on this requires some guidance. This newsletter is going to unveil all the steps needed to break into data engineering in 2024!*

#### 📖┆[Certifications & What It Signals?](https://koopingshung.substack.com/p/certifications-and-what-it-signals)

✍ [Koo Ping Shung](https://substack.com/profile/7906875-koo-ping-shung)

> *I recently had an interesting discussion on certification program, which looking at the current landscape, does feel a strong need for a deeper look into it and where it is needed.*

#### 📖┆[Mental Health in Software Engineering](https://vadimkravcenko.com/shorts/mental-health-in-software-engineering/)

✍[Vadim Kravcenko](https://vadimkravcenko.com/about-me/)

> *I want to talk about something we don't discuss enough in our field: the mental health of software engineers, especially those of us who've taken on the challenge of leadership.*

---

# 🚀 Engineering

> *I have to believe in a world outside my own mind. — Memento (2000)*

#### 📖┆[Migrating a Trillion Entries of Uber’s Ledger Data from DynamoDB to LedgerStore](https://www.uber.com/blog/migrating-from-dynamodb-to-ledgerstore/)

✍ [Uber Engineering Blog](https://www.uber.com/blog/asia/)

> *Last week, we explored LedgerStore (LSG) – Uber’s append-only, ledger-style database. This week, we’ll dive into how we migrated Uber’s business-critical ledger data to LSG. We’ll detail how we moved more than a trillion entries (making up a few petabytes of data) transparently and without causing disruption, and we’ll discuss what we learned during the migration.*

#### 📖┆[The Pragmatic Approach to Data Movement](https://www.decodable.co/blog/pragmatic-approach-to-data-movement)

✍ [Eric Sammer](https://www.decodable.co/blog-author/eric-sammer)

> *Data movement is the most stubborn problem in infrastructure.*

#### 📖┆[Under the Hood of Mixpanel’s Infrastructure](https://engineering.mixpanel.com/under-the-hood-of-mixpanels-infrastructure-0c7682125e9b)

✍ [Vijay Jayaram](https://medium.com/@vijay.jayaram)

> *Mixpanel’s analysis UI is powered by an in-house database called Arb, which is built for ingesting, storing, and querying trillions of events in real-time. This page covers the core aspects of our design, the pain points it eliminates for users, and how it compares to other systems.*

#### 📖┆[Using Clickhouse to scale an events engine](https://github.com/getlago/lago/wiki/Using-Clickhouse-to-scale-an-events-engine) + [the article’s comment wall on HackNews](https://news.ycombinator.com/item?id=40005005)

✍ [Lago Github Repo](https://github.com/getlago/lago)

> *Today, we’re going to explore that decision for a hybrid database stack, and more specifically, why we decided to go with ClickHouse.*

#### 📺┆[Velox Conference 2024 presentations](https://www.youtube.com/playlist?list=PLJvBe8nQAEsEBSoUY0lRFVZr2_YeHYkUR)

#### 📖┆[Grab Experiment Decision Engine - a Unified Toolkit for Experimentation](https://engineering.grab.com/grabx-decision-engine)

✍ [Ruike Zhang](https://www.linkedin.com/in/ruike-zhang-13086053?originalSubdomain=sg) + [Panos Mavrokonstantis](https://www.linkedin.com/in/panos-mavrokonstantis/?originalSubdomain=sg)

> *This article introduces the GrabX Decision Engine, an internal open-source package that offers a comprehensive framework for designing and analysing experiments conducted on online experiment platforms. The package encompasses a wide range of functionalities, including a pre-experiment advisor, a post-experiment analysis toolbox, and other advanced tools. In this article, we explore the motivation behind the development of these functionalities, their integration into the unique ecosystem of Grab’s multi-sided marketplace, and how these solutions strengthen the culture and calibre of experimentation at Grab.*

#### 📖┆[Slack summary pipeline with dlt, Ibis, and Hamilton](https://blog.dagworks.io/p/slack-summary-pipeline-with-dlt-ibis)

✍ [Thierry Jean](https://substack.com/profile/153186724-thierry-jean) + [DagWorks INC](https://substack.com/@dagworks)

> *A lightweight & modern Python ETL stack*

#### 📖┆[How I became an AST convert](https://tobikodata.com/ast_journey.html)

✍ [Afzal Jasani](https://tobikodata.com/author/afzal-jasani.html)

> *AST stands for abstract syntax tree. The team here at Tobiko Data has written a couple different blogs regarding the topic but I want to convey my journey in understanding ASTs and their purpose. It’s fair to say that my past experiences never warranted me to think this deeply about data structures.*

#### 📖┆[Introducing Trio | Part III](https://medium.com/airbnb-engineering/introducing-trio-part-iii-033fbfe2171b?source=rss----53c7c27702d5---4)

✍ [Eli Hart](https://medium.com/@konakid?source=post_page-----033fbfe2171b--------------------------------)

> *Part three on how we built a Compose based architecture with Mavericks in the Airbnb Android app*

#### 📖┆[A Tale of Two Frameworks: The Domain Graph Service Framework Meets Spring GraphQL](https://medium.com/@netflixtechblog/a-tale-of-two-frameworks-the-domain-graph-service-framework-meets-spring-graphql-f8237f09c389)

✍ [Netflix Technology Blog](https://netflixtechblog.medium.com/?source=post_page-----f8237f09c389--------------------------------)

> *Netflix open-sourced the Domain Graph Service (DGS) Framework in early 2021. Since then, the framework has seen widespread adoption across Netflix and many other companies. The DGS Framework provides Java developers with a programming model on top of Spring Boot to create GraphQL services.*

#### 📖┆[Data Engineering: Architectures & Strategies for Handling Sensitive Data](https://blog.det.life/data-engineering-architectures-strategies-for-handling-sensitive-data-83292b997c17)

✍ [Hussein Jundi](https://husseinjundi.medium.com/)

> *Strategies and architectures to handle sensitive data efficiently and securely according to an organization’s data maturity level.*

#### 📖┆[Data Council 2024: The future data stack is composable, and other hot takes](https://medium.com/vvus/data-council-2024-the-future-data-stack-is-composable-and-other-hot-takes-b6c5f2429e22)

✍ [Chase Roberts](https://medium.com/@chsrbrts?source=post_page-----b6c5f2429e22--------------------------------)

> *I wrote the synopsis below for the Vertex Ventures investment team as a debrief to last week’s Data Council conference. The summary wasn’t originally intended to be published as a blog post, but one of my partners suggested I post it publicly. So, here it is — entirely unedited.*

#### 📖┆[My fun journey of managing a large table of PostgreSQL](https://medium.com/@digitake/my-fun-journey-of-managing-a-large-table-of-postgresql-b8d09cb19444)

✍ [digitake](https://medium.com/@digitake?source=post_page-----b8d09cb19444--------------------------------)

> *The consolidator, at first, runs reasonably fast for its size. It takes about a minute to perform an SQL SELECT/GROUP BY/ORDER BY function. One might be surprised that one minute is relatively fast compared to the number of rows in the table. The reason for that is, I do, use an index to keep track of data. I will take you with me through my journey to the data wonderland.*

#### 📖┆[How we’ve saved 98% in cloud costs by writing our own database](https://hivekit.io/blog/how-weve-saved-5000-percent-in-cloud-costs-by-writing-our-own-database/)

✍ [Hivekit Blog](https://hivekit.io/blog/)

> *What is the first rule of programming? Maybe something like “do not repeat yourself” or “if it works, don’t touch it”? Or, how about “do not write your own database!”… That’s a good one.*

---

# ✏ Data

> *The one thing that this job has taught me is that truth is stranger than fiction. — Predestination (2014)*

#### 📖┆[Scalable Data Management with Microsoft Fabric and Microsoft Purview](https://piethein.medium.com/scalable-data-management-with-microsoft-fabric-and-microsoft-purview-7e54456559d9)

✍ [Piethein Strengholt](https://piethein.medium.com/?source=post_page-----7e54456559d9--------------------------------)

> *In this blog post, I aim to demonstrate a practical data transformation using Microsoft Fabric and Microsoft Purview. The target audience includes executives, architects, analysts, and compliance and governance personnel who are interested in creating a comprehensive data platform.*

#### 📖┆[Microsoft Excel in the Era of Big Data](https://fromanengineersight.substack.com/p/microsoft-excel-in-the-era-of-big)

✍ [Benoit Pimpaud](https://substack.com/profile/23621089-benoit-pimpaud)

> *What if we learn about how to build efficient and consistent spreadsheets? More than just getting closer to this engineering stuff, there are a lot of benefits for our daily tasks to strengthen these files with more efficiency, consistency, and reproducibility designs.*

#### 📖┆[How is the state of analytics engineering?](https://roundup.getdbt.com/p/how-is-the-state-of-analytics-engineering)

✍ [Dan Poppy](https://substack.com/profile/152560204-dan-poppy)

> *The 2024 State of Analytics Engineering is in. Let's get into it.*

---

# 🤖 AI┆ML┆Data Science

> *You know, Burke, I don’t know which species is worse. — Ripley, Aliens (1986)*

#### 📖┆[Chronon, Airbnb’s ML Feature Platform, Is Now Open Source](https://medium.com/airbnb-engineering/chronon-airbnbs-ml-feature-platform-is-now-open-source-d9c4dba859e8)

✍ [Varant Zanoyan](https://medium.com/@vzanoyan?source=post_page-----d9c4dba859e8--------------------------------)

> *A feature platform that offers observability and management tools, allows ML practitioners to use a variety of data sources, while handling the complexity of data engineering, and provides low latency streaming.*

#### 📖┆[How machine learning boosted available cash flows for our sellers](https://engineering.backmarket.com/how-machine-learning-boosted-available-cash-flows-for-our-sellers-eddd697269fc)

✍ [Pierre Pessarossi](https://medium.com/@pierre-pessarossi)

> *In this article, we will explain how we created business value by coupling machine learning with a simple sampling technique that bypassed the need to adapt our technical stack.*

#### 📖┆[4 ways GitHub engineers use GitHub Copilot](https://github.blog/2024-04-09-4-ways-github-engineers-use-github-copilot/)

✍ [Holger Staudacher](https://github.blog/author/hstaudacher/)

> *GitHub Copilot increases efficiency for our engineers by allowing us to automate repetitive tasks, stay focused, and more.*

---

# 🔥 Catch up

> *…Next Saturday night, we're sending you back to the future! — Dr. Emmett Brown, Back to the Future (1985)*

📖┆[Announcing Delta Lake support for BigQuery](https://cloud.google.com/blog/products/data-analytics/biglake-now-offers-native-support-for-delta-lake)

📖┆[Apache Kafka for BigQuery](https://cloud.google.com/products/apache-kafka-for-bigquery?hl=en)

📖┆Gemini in [BigQuery](https://cloud.google.com/blog/products/data-analytics/introducing-gemini-in-bigquery-at-next24/) and [Looker](https://cloud.google.com/blog/products/data-analytics/introducing-gemini-in-looker-at-next24/)

📖┆[BigQuery data canvas](https://cloud.google.com/blog/products/data-analytics/get-to-know-bigquery-data-canvas/)

📖┆[BigQuery's continuous queries feature](https://cloud.withgoogle.com/next/session-library?session=ANA211&utm_source=copylink&utm_medium=unpaidsoc&utm_campaign=FY24-Q2-global-ENDM33-physicalevent-er-next-2024-mc&utm_content=next-homepage-social-share&utm_term=-), which provides users the ability to run continuously processing SQL statements that can analyze and transform data as new events arrive in BigQuery. This is only available for [private preview](https://docs.google.com/forms/d/e/1FAIpQLSfeinewVSSFm9pop7O2-Ml6_A7YWbBSUrHI-67Au-SFIFvqEA/viewform).

📖┆[Next-generation Meta Training and Inference Accelerator](https://ai.meta.com/blog/next-generation-meta-training-inference-accelerator-AI-MTIA/)

📖┆[Apache Superset 4.0](https://preset.io/blog/apache-superset-4-0-release-notes/)

📖┆[Introducing Beam YAML: Apache Beam's First No-code SDK](https://beam.incubator.apache.org/blog/beam-yaml-release/)

---

# 💠 Previously on Dimension

> *Dimension is my sub-newsletter where I note down things I learn from people smarter than me in the data engineering field.*

Here are the 3 latest articles:

### ***Published on 2024, March 30:***

### ***Published on 2024, April 6:***

### ***Published on 2024, April 13:***

Let me here your voice, for example:

'Your newsletter is so terrible, I can't handle it anymore.'

[Leave a comment](https://vutr.substack.com/p/groupby-31-migrating-a-trillion-entries/comments)

---

## “Hasta la vista, baby” -T800, Terminator 2: Judgment Day (1991)

Thanks for scrolling this far! There's a convenient subscribe box here if you want me to annoy you every week. 😄
