---
title: "GroupBy #21: How to design resilient and large scale data systems, What Data Modeling is NOT"
channel: vutr
author: "Vu Trinh"
published: 2024-02-06
url: https://vutr.substack.com/p/groupby-21-how-to-design-resilient
paid: false
topics: ["Data Engineering", "Apache Kafka", "Apache Spark", "Apache Flink", "BigQuery", "Data Modeling", "Data Warehouse", "Lakehouse", "Streaming", "Change Data Capture"]
tags: [https, engineering, blog, medium, processing, stream]
---

# GroupBy #21: How to design resilient and large scale data systems, What Data Modeling is NOT

*Plus: Using DuckDB in-browser, Rethinking Stream Processing, BigQuery now supports vector search and vector indexes*

> Source: [Open post](https://vutr.substack.com/p/groupby-21-how-to-design-resilient)

## Topics

[[data-engineering|Data Engineering]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-flink|Apache Flink]] · [[bigquery|BigQuery]] · [[data-modeling|Data Modeling]] · [[data-warehouse|Data Warehouse]] · [[lakehouse|Lakehouse]] · [[streaming|Streaming]] · [[change-data-capture|Change Data Capture]]

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

[![](https://substackcdn.com/image/fetch/$s_!gqY8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F305d2a0c-aa71-4191-be13-4f5a6a928bea_1300x900.png)](https://substackcdn.com/image/fetch/$s_!gqY8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F305d2a0c-aa71-4191-be13-4f5a6a928bea_1300x900.png)

---

# 📈 Career

> *Don't let comfort hold you back.*

#### 📖┆[Leaving Google](https://medium.com/@avrukin/leaving-google-bfa390f0a0ec)

✍ [Michael Avrukin](https://medium.com/@avrukin?source=post_page-----bfa390f0a0ec--------------------------------)

> *I’m not entirely sure why I’m writing this piece. Maybe it’s because after spending almost nine years with a company, perceived by many as the ideal employer, one has to qualify their decision to leave. Maybe it is because I need to process my last nine years. Or maybe, it is in part what my wife said, “Besides our marriage, it’s the longest relationship you’ve been in.” Thinking about work as a “relationship” sounds awkward, but in a strange way it is.*

---

# 🚀 Engineering

> *I have to believe in a world outside my own mind. — Memento (2000)*

#### 📖┆[How to design resilient and large scale data systems](https://blog.dataengineer.io/p/how-to-design-resilient-and-large)

✍ [Zach Wilson](https://substack.com/profile/10367987-zach-wilson)

> *In this newsletter, we’ll be going over the considerations you should be thinking about when building out large scale data systems.*

#### 📖┆[Apache Flink and cluster components deep dive](https://www.waitingforcode.com/apache-flink/apache-flink-cluster-components-deep-dive/read)

✍ [Bartosz Konieczny](https://www.linkedin.com/in/bartosz-konieczny-waitingforcode/)

> *In the blog post you will not see any high-level code snippet. Instead, I decided to analyze the internals and see what action Apache Flink performs since submitting the job to the cluster.*

#### 📖┆[Rethinking Stream Processing: Data Exploration](https://engineering.grab.com/rethinking-streaming-processing-data-exploration)

✍ [Shi Kai Ng](https://engineering.grab.com/authors#shikai-ng) · [Calvin Tran](https://engineering.grab.com/authors#calvin-tran) · [Minh Nhat Nguyen](https://engineering.grab.com/authors#nhat-nguyen)

> *With innovations in stream processing technology like Spark and Flink, there is now more interest in unlocking value from streaming data. This form of continuously-generated data in high volume will be referenced within this document as “Online Data”. In the context of Grab, the streaming data is usually materialised as Kafka topics (“Kafka Stream”) as the result of stream processing in its framework.*

#### 📖┆[Don’t Worry About Data Lakehouse Features, Trust in Google Search](https://medium.com/@kywe665/dont-worry-about-data-lakehouse-features-trust-in-google-search-5d8d13675680)

✍ [Kyle Weller](https://medium.com/@kywe665?source=post_page-----5d8d13675680--------------------------------)

> *Under acknowledgement of my bias, my goal here is not to somehow craftily convince you of one table format or another (I have other blogs for that). I am actually just disappointed by the technical inaccuracy and damaging misinformation shared in the mentioned blog. I don’t care what format you might prefer, I hope there is a foundation of truth seeking and a recognition that the information presented and the conclusions drawn stands in need of correction.*

#### 📖┆[Real-time data processing using Change Data Capture and event-driven architecture](https://medium.com/macquarie-engineering-blog/real-time-data-processing-using-change-data-capture-and-event-driven-architecture-006cf30cc449)

✍ [Engineers at Macquarie](https://medium.com/@macquarieengineeringblog?source=post_page-----006cf30cc449--------------------------------)

> *To overcome this challenge, our engineering team in the BFS Wealth division implemented an event-sourcing pattern using what’s known as Change Data Capture (CDC), a modern technique to stream database updates as events that can be consumed by downstream services.*

#### 📖┆[DataCentral: Uber’s Big Data Observability and Chargeback Platform](https://www.uber.com/en-SG/blog/datacentral-ubers-observability-and-chargeback-platform/)

✍ [Uber Engineering Blog](https://www.uber.com/en-SG/blog/engineering/backend/?uclick_id=15b6739c-0acd-406e-bdf6-884992beefa0)

> *In this blog, we will walk you through DataCentral, Uber’s homegrown Big Data Observability, Attribution, and Governance platform. This blog gives a high-level overview of DataCentral’s key features. Before we get into the what and why of DataCentral, let’s do a quick primer of Uber’s Data ecosystem and its challenges.*

#### 📖┆[Cassandra Unleashed: How We Enhanced Cassandra Fleet’s Efficiency and Performance](https://doordash.engineering/2024/01/30/cassandra-unleashed-how-we-enhanced-cassandra-fleets-efficiency-and-performance/)

✍ [Seed Zeng](https://www.linkedin.com/in/seedzeng/)

> *In this blog post, we walk through DoorDash’s Cassandra optimization journey. I will share what we learned as we made our fleet much more performant and cost-effective. Through analyzing our use cases, we hope to share universal lessons that you might find useful.*

#### 📖┆[Using DuckDB-WASM for in-browser Data Engineering](https://tobilg.com/using-duckdb-wasm-for-in-browser-data-engineering)

✍ [Tobias Müller](https://hashnode.com/@TobiLG)

> *DuckDB cannot 'only' be run on a variety of Operating Systems and Architectures, there's also a DuckDB-WASM version, that allows running DuckDB in a browser. This opens up some very interesting use cases, and is also gaining a lot of traction in the last 12 months.*

#### 📖┆[Where does Stream Processing Fit into Your Data Platform?](https://www.decodable.co/blog/where-does-stream-processing-fit-into-your-data-platform)

✍ [Sharon Xie](https://www.linkedin.com/in/sharonxr/)

> *In this blog post, I will start with the current state of data movement within a typical data platform, highlighting scaling and management issues. Subsequently, I will illustrate how incorporating stream processing into the architecture enables lower latency, simpler code, and greater flexibility in data system management.*

---

# ✏ Data

> *The one thing that this job has taught me is that truth is stranger than fiction. — Predestination (2014)*

#### 📖┆[What Data Modeling is NOT](https://practicaldatamodeling.substack.com/p/what-data-modeling-is-not?)

✍ [Joe Reis](https://substack.com/profile/3531217-joe-reis)

> *We need to look at the bigger picture of data modeling*

#### 📖┆[3 Actionable Tactics To Create A Good Data Strategy](https://www.thdpth.com/p/how-to-create-a-good-data-strategy)

✍ [Sven Balnojan](https://substack.com/profile/229923-sven-balnojan)

> *If you only have a few minutes, here’s what will make your business smarter with a good data strategy inspired by Netflix*

#### 📖┆[The business-critical data warehouse](https://medium.com/@mikldd/the-business-critical-data-warehouse-0a8d224c5bf5)

✍ [Mikkel Dengsøe](https://medium.com/@mikldd?source=post_page-----0a8d224c5bf5--------------------------------)

> *How the data warehouse moved on from analytics and the role AI has played in accelerating this*

#### 📖┆[Data Warehouse Design Patterns](https://towardsdatascience.com/data-warehouse-design-patterns-d7c1c140c18b)

✍ [Mike Shakhomirov](https://mshakhomirov.medium.com/?source=post_page-----d7c1c140c18b--------------------------------)

> *How I organize everything in my new data warehouse*

#### 📖┆[From a hack to a data mesh approach: The 18-year evolution of data engineering at Leboncoin](https://medium.com/leboncoin-tech-blog/from-a-hack-to-a-data-mesh-approach-the-18-year-evolution-of-data-engineering-at-leboncoin-b234fc05f091)

✍ [leboncoin tech](https://medium.com/@leboncoin_tech?source=post_page-----b234fc05f091--------------------------------)

> *This article provides a detailed account of those diverse steps undertaken to construct our current data engineering stack and ultimately culminating in the adoption of data mesh principles in our organization.*

---

# 🤖 AI┆ML┆Data Science

> *You know, Burke, I don’t know which species is worse. — Ripley, Aliens (1986)*

#### 📖┆[Improving machine learning iteration speed with faster application build and packaging](https://engineering.fb.com/2024/01/29/ml-applications/improving-machine-learning-iteration-speed-with-faster-application-build-and-packaging/)

✍ [Barys Skarabahaty](https://engineering.fb.com/author/barys-skarabahaty/)

> *In our efforts to maintain efficiency and productivity while empowering our ML/AI engineers to deliver cutting-edge solutions, we found two major challenges that needed to be addressed head-on: slow builds and inefficiencies in packaging and distributing executable files.*

---

# 🔥 Catch up

> *…Next Saturday night, we're sending you back to the future! — Dr. Emmett Brown, Back to the Future (1985)*

#### 📖┆BigQuery | Now supports [vector search](https://cloud.google.com/bigquery/docs/reference/standard-sql/search_functions#vector_search) and [vector indexes](https://cloud.google.com/bigquery/docs/vector-index)

#### 📖┆[AWS Glue | New chat experience for AWS Glue using natural language – Amazon Q data integration](https://aws.amazon.com/blogs/aws/new-chat-experience-for-aws-glue-using-natural-language-amazon-q-data-integration-in-aws-glue-preview/)

---

# 💠 Previously on Dimension

> *Dimension is my sub-newsletter where I note down things I learn from people smarter than me in the data engineering field.*

Here are the 3 latest articles:

### ***Published on 2024, January 20:***

### ***Published on 2024, January 27:***

### ***Published on 2024, February 3:***

Let me here your voice, for example:

'Your newsletter is so terrible, I can't handle it anymore.'

[Leave a comment](https://vutr.substack.com/p/groupby-21-how-to-design-resilient/comments)

---

## “Hasta la vista, baby”

## -T800, Terminator 2: Judgment Day (1991)

Thanks for scrolling this far! There's a convenient subscribe box here if you want me to annoy you every week. 😄
