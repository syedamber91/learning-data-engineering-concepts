---
title: "GroupBy #27: Balancing HDFS DataNodes in the Uber DataLake, How Figma’s databases team lived to tell the scale"
channel: vutr
author: "Vu Trinh"
published: 2024-03-19
url: https://vutr.substack.com/p/groupby-27-balancing-hdfs-datanodes
paid: false
topics: ["Data Engineering", "Apache Airflow", "Apache Kafka", "Apache Spark", "Data Warehouse", "Lakehouse", "Streaming"]
tags: [https, engineering, blog, linkedin, time, building]
---

# GroupBy #27: Balancing HDFS DataNodes in the Uber DataLake, How Figma’s databases team lived to tell the scale

*Plus: Building Meta’s GenAI Infrastructure, How to save millions by optimizing data pipeline shuffling*

> Source: [Open post](https://vutr.substack.com/p/groupby-27-balancing-hdfs-datanodes)

## Topics

[[data-engineering|Data Engineering]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[data-warehouse|Data Warehouse]] · [[lakehouse|Lakehouse]] · [[streaming|Streaming]]

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

[![](https://substackcdn.com/image/fetch/$s_!WZ3Z!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F440e5362-8510-48ef-a235-a99171dfdb4b_1400x1000.png)](https://substackcdn.com/image/fetch/$s_!WZ3Z!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F440e5362-8510-48ef-a235-a99171dfdb4b_1400x1000.png)

Image created by the [Canvas Image Generator](https://www.canva.com/ai-image-generator/).

---

# 📈 Career

> *Don't let comfort hold you back.*

#### 📖┆[The demise of coding is greatly exaggerated](https://muratbuffalo.blogspot.com/2024/03/the-demise-of-coding-is-greatly.html)

✍ [Murat Demirbas](https://cse.buffalo.edu/~demirbas/)

> *I like to mention that a career in computer science and software technology (practicing coding) gives you vital and generally applicable skills: hacking, debugging, abstract thinking, quick learning/adaptation, and organizational skills.*

#### 📖┆[40 years of programming](https://liw.fi/40/)

✍ [Lars Wirzenius](https://liw.fi/)

> *In April, 1984, my father bought a computer for his home office, a Luxor ABC-802, with a Z80 CPU, 64 kilobytes of RAM, a yellow-on-black screen with 80 by 25 text mode, or about 160 by 75 pixels in graphics mode, and two floppy drives. It had BASIC in its ROM, and came with absolutely no games. If I wanted to play with it, I had to learn how to program, and write my own games. I learned BASIC, and over the next few years would learn Pascal, C, and more. I had found my passion. I was 14 years old and I knew what I wanted to do when I grew up.*

#### 📖┆[Measuring Developer Productivity via Humans](https://martinfowler.com/articles/measuring-developer-productivity-humans.html)

✍ [Abi Noda](https://www.linkedin.com/in/abinoda/) + [Tim Cochran](https://www.linkedin.com/in/timcochran/)

> *Measuring developer productivity is a difficult challenge. Conventional metrics focused on development cycle time and throughput are limited, and there aren't obvious answers for where else to turn. Qualitative metrics offer a powerful way to measure and understand developer productivity using data derived from developers themselves.*

---

# 🚀 Engineering

> *I have to believe in a world outside my own mind. — Memento (2000)*

#### 📖┆[Balancing HDFS DataNodes in the Uber DataLake](https://www.uber.com/en-SG/blog/balancing-hdfs-datanodes-in-the-uber-datalake/)

✍ [Uber Engineering Blog](https://www.uber.com/blog/asia/)

> *Uber has one of the largest HDFS deployments in the world, with exabytes of data across tens of clusters. It is important, but also challenging, to keep scaling our data infrastructure with the balance between efficiency, service reliability, and high performance.*

#### 📖┆[We built a new SQL Engine on Arrow and DataFusion](https://www.arroyo.dev/blog/why-arrow-and-datafusion)

✍ [Micah Wylde](https://www.linkedin.com/in/wylde/)

> *Arroyo 0.10 has an entirely new SQL engine built with Apache Arrow and DataFusion. It's much faster, smaller, and easier to run. Read on for why and how we're making this change.*

#### 📖┆[Differential storage: a key building block for a DuckDB-based data warehouse](https://motherduck.com/blog/differential-storage-building-block-for-data-warehouse/)

✍ [Joseph Hwang](https://motherduck.com/authors/joseph-hwang/)

> *Today we’d like to talk about Differential Storage, a key infrastructure-level enabler of new capabilities and stronger semantics for MotherDuck users. Thanks to Differential Storage, features like efficient **[data sharing](https://motherduck.com/docs/key-tasks/managing-shared-motherduck-database)** and **[zero-copy clone](https://motherduck.com/docs/motherduck-sql-reference/create-database)** are now available in MotherDuck. Moreover, Differential Storage unlocks other features, like snapshots, branching and time travel which we’ll release in the coming months.*

#### 📖┆[Improving Efficiency Of Goku Time Series Database at Pinterest (Part 2)](https://medium.com/pinterest-engineering/improving-efficiency-of-goku-time-series-database-at-pinterest-part-2-08130f25b874)

✍ [Pinterest Engineering](https://medium.com/@Pinterest_Engineering?source=post_page-----08130f25b874--------------------------------)

> *This 2nd blog post focuses on how Goku time series queries were improved. We will provide a brief overview of Goku’s time series data model, query model, and architecture. We will follow up with the improvement features we added including rollup, pre-aggregation, and pagination.*

#### 📖┆[Scaling Models And Multi-Tenant Data Systems - ASDS Chapter 6](https://jack-vanlightly.com/analyses/2024/3/12/scaling-models-and-multi-tenant-data-systems-asds-chapter-6)

✍ [Jack Vanlightly](https://jack-vanlightly.com/home)

> *What is scaling in large-scale multi-tenant data systems, and how does that compare to single-tenant data systems? How does per-tenant scaling relate to system-wide scaling? How do scale-to-zero and cold starts come into play? Answering these questions is chapter 6 of The Architecture of Serverless Data Systems.*

#### 📖┆[How Figma’s databases team lived to tell the scale](https://www.figma.com/blog/how-figmas-databases-team-lived-to-tell-the-scale/)

✍ [Sammy Steele](https://www.linkedin.com/in/samantha-steele-b9a41aa3/)

> *Figma’s database stack has grown almost 100x since 2020. This is a good problem to have because it means our business is expanding, but it also poses some tricky technical challenges*

#### 📖┆[Data Engineering Best Practices - #2. Metadata & Logging](https://www.startdataengineering.com/post/de_best_practices_log/)

✍ [Joseph M.](https://www.linkedin.com/in/josephmachado1991/)

> *Dealing with breaking pipelines, debugging why they failed, and putting up a fix are everyday tasks for a data engineer.*

#### 📖┆[S3 is files, but not a filesystem](https://calpaterson.com/s3.html)

✍ [Cal Paterson](https://calpaterson.com/about.html)

> *"Deep" modules, mismatched interfaces - and why SAP is so painful*

#### 📖┆[Building data abstractions with streaming at Yelp](https://engineeringblog.yelp.com/2024/03/building-data-abstractions-with-streaming-at-yelp.html)

✍ [Hakampreet Singh Pandher](https://www.linkedin.com/in/hakampreet-singh-pandher-88a50484/)

> *This blog post covers how we leverage Yelp’s extensive streaming infrastructure to build robust data abstractions for our offline and streaming data consumers. We will use Yelp’s Business Properties ecosystem (explained in the upcoming sections) as an example.*

#### 📖┆[Airflow & Kestra: a Simple Benchmark](https://medium.pimpaudben.fr/airflow-kestra-a-simple-benchmark-ffc5a533aa85)

✍ [Benoit Pimpaud](https://medium.pimpaudben.fr/?source=post_page-----ffc5a533aa85--------------------------------)

> *This post compares Airflow and Kestra, focusing on installation, configuration, pipeline syntax, and performance.*

#### 📖┆[Postgres Aurora DB major version upgrade with minimal downtime](https://eng.lyft.com/postgres-aurora-db-major-version-upgrade-with-minimal-downtime-4e26178f07a0)

✍ [Jay Patel](https://medium.com/@pjay5334?source=post_page-----4e26178f07a0--------------------------------)

> *Our payment platform team had the unique challenge to upgrade our Aurora Postgres DB from v10 to v13. This DB was responsible for storing transactions within Lyft and contains ~400 tables (with partitions) and ~30TB of data. Upgrading the database in-place would have resulted in ~30 mins of downtime. Such significant downtime is untenable — it would cause cascading failures across multiple downstream services, requiring a large amount of engineering effort to remediate.*

#### 📖┆[Apache Druid’s Architecture – How Druid Processes Data In Real Time At Scale](https://www.theseattledataguy.com/apache-druids-architecture-how-druid-processes-data-in-real-time-at-scale/)

✍ [Ben Rogojan](https://www.theseattledataguy.com/data-science-consultants/#page-content)

> *Apache Druid has several unique features that allow it to be used as a real-time OLAP. Everything from its various nodes and processes that each have unique functionality that let it scale to the fact that the data is indexed to be pulled quickly and efficiently.*

#### 📖┆[How to save millions by optimizing data pipeline shuffling](https://blog.dataengineer.io/p/how-to-save-millions-by-optimizing)

✍ [Zach Wilson](https://substack.com/profile/10367987-zach-wilson)

> *In this article we will be going over: - Why does shuffle happen and what SQL keywords trigger shuffle and which do not? - Some techniques you can use to minimize shuffle especially in Apache Spark*

#### 📖┆[A Look Back at Key Trends in Data Infrastructure in 2023 by Four Industry Founders](https://medium.com/illuminations-mirror/a-look-back-at-key-trends-in-data-infrastructure-in-2023-by-four-industry-founders-7d1f7ae0d46f)

✍ [RisingWave Labs](https://medium.com/@RisingWave_Engineering?source=post_page-----7d1f7ae0d46f--------------------------------)

> *The discussion with the four founders of data infrastructure startups focused on key trends in the industry for 2023.*

#### 📖┆[Unlocking Kafka's Potential: Tackling Tail Latency with eBPF](https://blog.allegro.tech/2024/03/kafka-performance-analysis.html)

✍ [Maciej Mościcki](https://www.linkedin.com/in/moscickimaciej/) + [Piotr Rżysko](https://www.linkedin.com/in/piotrrzysko/)

> *At Allegro, we use Kafka as a backbone for asynchronous communication between microservices. With up to 300k messages published and 1M messages consumed every second, it is a key part of our infrastructure. A few months ago, in our main Kafka cluster, we noticed the following discrepancy: while median response times for produce requests were in single-digit milliseconds, the tail latency was much worse. Namely, the p99 latency was up to 1 second, and the p999 latency was up to 3 seconds. This was unacceptable for a new project that we were about to start, so we decided to look into this issue. In this blog post, we would like to describe our journey — how we used Kafka protocol sniffing and eBPF to identify and remove the performance bottleneck.*

---

# ✏ Data

> *The one thing that this job has taught me is that truth is stranger than fiction. — Predestination (2014)*

#### 📖┆[Scalable Automated Config-Driven Data Validation with ValiData](https://www.linkedin.com/blog/engineering/data-management/scalable-automated-config-driven-data-validation)

✍ [Bharadwaj Jayaraman](https://www.linkedin.com/in/bhar2201)

> *ValiData is a scalable automated config-driven data validation tool extensively used in LinkedIn that compares metric values of test datasets against production or source-of-truth datasets and highlights differences in metric values across dimensions.*

---

# 🤖 AI┆ML┆Data Science

> *You know, Burke, I don’t know which species is worse. — Ripley, Aliens (1986)*

#### 📖┆[How Meta tests products with strong network effects](https://medium.com/@AnalyticsAtMeta/how-meta-tests-products-with-strong-network-effects-96003a056c2c)

✍ [Analytics at Meta](https://medium.com/@AnalyticsAtMeta?source=post_page-----96003a056c2c--------------------------------)

> *I’m a member of a team that’s been applying cluster experimentation to products with strong network effects, such as chat and calling, since 2018. Today, I’d like to give an overview of the challenges we face in these highly-interactive domains, and how one solution — cluster experiments — has become a go-to method for addressing these challenges.*

#### 📖┆[Best practices for building LLMs](https://stackoverflow.blog/2024/02/07/best-practices-for-building-llms/)

✍ [Nitzan Gado](https://stackoverflow.blog/author/nitzan-gado/) + [Oren Dar](https://stackoverflow.blog/author/oren-dar/)

> *Intuit shares what they've learned building multiple LLMs for their generative AI operating system.*

#### 📖┆[Improving ETAs with Multi-Task Models, Deep Learning, and Probabilistic Forecasts](https://doordash.engineering/2024/03/12/improving-etas-with-multi-task-models-deep-learning-and-probabilistic-forecasts/)

✍ [Doordash Engineering Blog](https://doordash.engineering/blog/)

> *The DoorDash ETA team is committed to providing an accurate and reliable estimated time of arrival (ETA) as a cornerstone DoorDash consumer experience. We want to ensure that every customer can trust our ETAs, ensuring a high-quality experience in which their food arrives on time every time.*

#### 📖┆[Building Meta’s GenAI Infrastructure](https://engineering.fb.com/2024/03/12/data-center-engineering/building-metas-genai-infrastructure/)

✍ [Kevin Lee](https://engineering.fb.com/author/kevin-lee/) + [Adi Gangidi](https://engineering.fb.com/author/adi-gangidi/) + [Mathew Oldham](https://engineering.fb.com/author/mathew-oldham/)

> *Marking a major investment in Meta’s AI future, we are announcing two 24k GPU clusters. We are sharing details on the hardware, network, storage, design, performance, and software that help us extract high throughput and reliability for various AI workloads. We use this cluster design for Llama 3 training.*

---

# 🔥 Catch up

> *…Next Saturday night, we're sending you back to the future! — Dr. Emmett Brown, Back to the Future (1985)*

#### 📖┆LinkedIn [Open Sources OpenHouse](https://www.linkedin.com/blog/engineering/open-source/open-sourcing-openhouse): A Control Plane for Managing Tables in a Data Lakehouse

#### 📖┆[OpenTable now changes name to Apache XTable](https://www.linkedin.com/posts/apache-xtable_onetable-is-now-apache-xtable-incubating-activity-7173282583730962432-AGGi?utm_source=share&utm_medium=member_desktop)

#### 📖┆**[Announcing Apache Arrow DataFusion Comet](https://arrow.apache.org/blog/2024/03/06/comet-donation/)**

---

# 💠 Previously on Dimension

> *Dimension is my sub-newsletter where I note down things I learn from people smarter than me in the data engineering field.*

Here are the 3 latest articles:

### ***Published on 2024, March 2:***

### ***Published on 2024, March 9:***

### ***Published on 2024, March 16:***

Let me here your voice, for example:

'Your newsletter is so terrible, I can't handle it anymore.'

[Leave a comment](https://vutr.substack.com/p/groupby-27-balancing-hdfs-datanodes/comments)

---

## “Hasta la vista, baby” -T800, Terminator 2: Judgment Day (1991)

Thanks for scrolling this far! There's a convenient subscribe box here if you want me to annoy you every week. 😄
