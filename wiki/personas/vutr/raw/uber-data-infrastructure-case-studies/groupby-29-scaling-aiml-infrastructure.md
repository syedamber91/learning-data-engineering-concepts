---
title: "GroupBy #29: Scaling AI/ML Infrastructure at Uber, The Sisyphean struggle and the new era of data infrastructure"
channel: vutr
author: "Vu Trinh"
published: 2024-04-02
url: https://vutr.substack.com/p/groupby-29-scaling-aiml-infrastructure
paid: false
topics: ["Data Engineering", "Apache Kafka", "Apache Spark", "Apache Flink", "Databricks", "BigQuery", "Lakehouse", "Streaming"]
tags: [https, blog, medium, infrastructure, source, engineering]
---

# GroupBy #29: Scaling AI/ML Infrastructure at Uber, The Sisyphean struggle and the new era of data infrastructure

*Plus: Netflix- The Imperative of Effective Data Management, The Data Streaming Landscape 2024*

> Source: [Open post](https://vutr.substack.com/p/groupby-29-scaling-aiml-infrastructure)

## Topics

[[data-engineering|Data Engineering]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-flink|Apache Flink]] · [[databricks|Databricks]] · [[bigquery|BigQuery]] · [[lakehouse|Lakehouse]] · [[streaming|Streaming]]

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

[![](https://substackcdn.com/image/fetch/$s_!UdwB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fff78c1a6-1a98-4cfe-b362-c8bef2d58627_1400x1000.png)](https://substackcdn.com/image/fetch/$s_!UdwB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fff78c1a6-1a98-4cfe-b362-c8bef2d58627_1400x1000.png)

Image created by the Canva Image Generator.

---

# 🚀 Engineering

> *I have to believe in a world outside my own mind. — Memento (2000)*

#### 📖┆[The Sisyphean struggle and the new era of data infrastructure](https://jack-vanlightly.com/blog/2024/3/26/the-sisyphean-struggle-and-the-new-era-of-data-infrastructure)

✍ [Jack Vanlightly](https://jack-vanlightly.com/home)

> *For a while now, I’ve been spending a lot of time thinking about technology trends in the data infrastructure space (as a researcher at Confluent). These trends are making some previously difficult things easy and therefore, commodity. I would go as far as to say that we are witnessing a kind of phase change, a regime shift, at least in the cloud. Almost inevitably, the quote above brought me back to this topic as it revolves around the subject of commodity and competition.*

#### 📖┆[Ce n'est pas un Kafka: Kafka is a Protocol](https://materializedview.io/p/ce-nest-pas-un-kafka)

✍ [Chris Riccomini](https://substack.com/profile/69592459-chris-riccomini)

> *Apache Kafka is an aging open source project. It's time to accept that Kafka's protocol is what matters.*

#### 📖┆[The Data Streaming Landscape 2024](https://kai-waehner.medium.com/the-data-streaming-landscape-2024-6e078b1959b5)

✍ [Kai Waehner](https://kai-waehner.medium.com/?source=post_page-----6e078b1959b5--------------------------------)

> *This blog post explores the data streaming landscape of 2024 to summarize existing solutions and market trends. The end of the article gives an outlook to potential new entrants in 2025.*

#### 📖┆[GrafLI - An out-of-the-box Azure monitoring and visualization platform](https://www.linkedin.com/blog/engineering/analytics/grafli-an-out-of-the-box-azure-monitoring-visualization-platform)

✍ [Prateek Singh](https://www.linkedin.com/in/prateekkumarsingh)

> *Recognizing these challenges, the Productivity Engineering team at LinkedIn crafted GrafLI, a cloud-native data visualization tool designed to transform the visualization of Azure and on-premises services. In this post, we delve into the intricacies of GrafLI and how it enhances the developer experience and increases engineering velocity.*

#### 📖┆[Navigating the Netflix Data Deluge: The Imperative of Effective Data Management](https://netflixtechblog.medium.com/navigating-the-netflix-data-deluge-the-imperative-of-effective-data-management-e39af70f81f7)

✍ [Netflix Technology Blog](https://netflixtechblog.medium.com/?source=post_page-----e39af70f81f7--------------------------------)

> *In this article, we, the Media Infrastructure Platform team, outline the development of a Garbage Collector, our solution for effectively managing production data.*

#### 📖┆[Columnar DB File Reader V2: A Complete Rewrite](https://engineering.mixpanel.com/columnar-db-file-reader-v2-a-complete-rewrite-64acdb62a223)

✍ [John Mikhail](https://medium.com/@johnfmikhail)

> *One of the main pillars of Mixpanel is our proprietary columnar store database, ARB, which we specifically designed to meet the needs of our customers. In this blog post, we delve into a comprehensive rewrite of the event reader code responsible for parsing the columnar files. The primary objective is to significantly enhance query performance, particularly for those with selective filters.*

#### 📖┆[Anatomy of a lakeFS Repository: Practical Example of Git for Data](https://lakefs.io/blog/lakefs-repository-git-for-data/)

✍ [Oz Katz](https://www.linkedin.com/in/oz-katz-4b3b389)

> *To help you understand the value of Git for data, here’s an overview of the tools that are part of every lakeFS repository. They’re bound to help with your data strategy and ensure that your organization meets its compliance, quality, and safety requirements.*

#### 📖┆[Introducing Trio | Part I](https://medium.com/airbnb-engineering/introducing-trio-part-i-7f5017a1a903)

✍ [Eli Hart](https://medium.com/@konakid?source=post_page-----7f5017a1a903--------------------------------)

> *A three-part series on how we built a Compose-based architecture with Mavericks in the Airbnb Android app.*

#### 📖┆[Using GitHub Copilot in your IDE: Tips, tricks and best practices](https://github.blog/2024-03-25-how-to-use-github-copilot-in-your-ide-tips-tricks-and-best-practices/)

✍ [Kedasha Kerr](https://github.blog/author/ladykerr/)

> *In this blog post, I’ll share some of the daily things I do to get the most out of GitHub Copilot. I hope these tips will help you become a more efficient and productive user of the AI assistant.*

#### 📖┆[Building a Modern Data Service Layer with Apache Arrow](https://medium.com/gooddata-developers/building-a-modern-data-service-layer-with-apache-arrow-33ace768e3f1)

✍ [Jan Soubusta](https://medium.com/@zupabusta?source=post_page-----33ace768e3f1--------------------------------)

> *Our journey, led by Lubomir (lupko) Slivka, aims to revolutionize GoodData’s analytics offerings, transforming our traditional BI platform into a robust Analytics Lake. This transformation was motivated by the need to modernize our stack, taking full advantage of open-source technologies and modern architectural principles to better integrate with cloud platforms.*

#### 📖┆[Cost Optimization Strategies for scalable Data Lakehouse](https://blogs.halodoc.io/data-lake-cost-optimisation-strategies/amp/)

✍ [Suresh Hasundi](https://www.linkedin.com/in/imsuresh/overlay/about-this-profile/)

> *In this blog, we will be discussing about the cost related challenges we had faced when our Data Lakehouse scaled and how we have overcome such costs by optimizing the process.*

#### 📖┆[Why Do Python Lists Multiply Oddly? Exploring the CPython Source Code](https://codeconfessions.substack.com/p/why-do-python-lists-multiply-oddly)

✍ [Abhinav Upadhyay](https://substack.com/@abhinavupadhyay)

> *We will start by a high level answer by just doing some inspection in the REPL, then we will go one level deeper and see the details of the list implementation in CPython to see why that happens, and finally we will go another level down to see how CPython invokes this behavior.*

#### 📖┆[PySpark in 2023: A Year in Review](https://www.databricks.com/blog/pyspark-2023-year-review)

✍ [Databricks Blog](https://www.databricks.com/blog)

> *With the releases of Apache Spark 3.4 and 3.5 in 2023, we focused heavily on improving PySpark performance, flexibility, and ease of use. This blog post walks you through the key improvements.*

#### 📖┆[Setting Up Kafka Multi-Tenancy](https://doordash.engineering/2024/03/27/setting-up-kafka-multi-tenancy/)

✍ [Yunji Zhong](https://www.linkedin.com/in/yunji-zhong-73810812/) + [Amit Gud](https://www.linkedin.com/in/amitgud/) + [Carlos Herrera](https://www.linkedin.com/in/carlosh/)

> *In such a multi-tenant architecture, the isolation is implemented at the infrastructure layer. We will delve here into how we set up multi-tenancy with a messaging queue system based on Kafka.*

#### 📖┆**[Data Platforms : Good Architect — Bad Architect](https://medium.com/dcsfamily/data-platforms-good-architect-bad-architect-cb9bdee35c34)**

✍ [Nilay Shah](https://medium.com/@shah.nilay02?source=post_page-----cb9bdee35c34--------------------------------)

> *Data Engineering is a dynamic field that requires a deep understanding of both technical skills and overarching principles. This transition is often marked by a shift from focusing on immediate technical challenges to embracing a broader perspective on data architecture. If you are Data Architect and want to learn some basic practices — This Article is for you!*

#### 📖┆**[Many Articles Tell You Python Tricks, But Few Tell You Why](https://medium.com/towards-data-science/many-articles-tell-you-python-tricks-but-few-tell-you-why-d4953d24e80b)**

✍ [Christopher Tao](https://medium.com/@christophertao)

> *In my opinion, it is more important to understand the reason why these tricks are there, so we can understand when to use and when not to use them. In this article, I’ll pick up three of them and provide a detailed explanation of the mechanisms under the hood.*

---

# 🤖 AI┆ML┆Data Science

> *You know, Burke, I don’t know which species is worse. — Ripley, Aliens (1986)*

#### 📖┆[Scaling AI/ML Infrastructure at Uber](https://www.uber.com/en-SG/blog/scaling-ai-ml-infrastructure-at-uber/)

✍ [Uber Engineering Blog](https://www.uber.com/blog/asia/)

> *As the complexity and scale of AI/ML models continue to surge, there’s a growing demand for highly efficient infrastructure to support these models effectively. Over the past few years, we’ve strategically implemented a range of infrastructure solutions, both CPU- and GPU-centric, to scale our systems dynamically and cater to the evolving landscape of ML use cases. This evolution has involved tailored hardware SKUs, software library enhancements, integration of diverse distributed training frameworks, and continual refinements to our end-to-end Michaelangelo platform.*

#### 📖┆[The race between positive and negative applications of Generative AI is on – and not looking pretty](https://garymarcus.substack.com/p/the-race-between-positive-and-negative)

✍ [Gary Marcus](https://substack.com/profile/14807526-gary-marcus)

> *OpenAI’s VP of Global Affairs Anna Makanju is exactly right - the race is on. I have some concerns, partly about the way that race is going, partly about (in)justice in who is likely to pay for the costs.*

---

# 🔥 Catch up

> *…Next Saturday night, we're sending you back to the future! — Dr. Emmett Brown, Back to the Future (1985)*

📖┆[Databricks: Announcing the State Reader API: The New "Statestore" Data Source](https://www.databricks.com/blog/announcing-state-reader-api-new-statestore-data-source)

📖┆[Apache Flink Kubernetes Operator 1.8.0 Release Announcement](https://flink.apache.org/2024/03/21/apache-flink-kubernetes-operator-1.8.0-release-announcement/)

📖┆BigQuery [Query optimization using search indexes](https://cloud.google.com/bigquery/docs/search#operator_and_function_optimization) is now (GA) applied to comparisons of string literals and indexed data, including the equal (`=`), `IN`, and `LIKE` operators and the `STARTS_WITH` function.

📖┆The [Help me code tool](https://cloud.google.com/bigquery/docs/write-sql-duet-ai#use_the_help_me_code_tool) lets user use natural language to generate a SQL query that can then be run in BigQuery.

---

# 💠 Previously on Dimension

> *Dimension is my sub-newsletter where I note down things I learn from people smarter than me in the data engineering field.*

Here are the 3 latest articles:

### ***Published on 2024, March 16:***

### ***Published on 2024, March 23:***

### ***Published on 2024, March 30:***

Let me here your voice, for example:

'Your newsletter is so terrible, I can't handle it anymore.'

[Leave a comment](https://vutr.substack.com/p/groupby-29-scaling-aiml-infrastructure/comments)

---

## “Hasta la vista, baby” -T800, Terminator 2: Judgment Day (1991)

Thanks for scrolling this far! There's a convenient subscribe box here if you want me to annoy you every week. 😄
