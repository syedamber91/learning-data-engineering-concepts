---
title: "GroupBy #9: FDAP stack, Iceberg and Hudi ACID Guarantees, Data Driven Management"
channel: vutr
author: "Vu Trinh"
published: 2023-11-14
url: https://vutr.substack.com/p/groupby-9-iceberg-and-hudi-acid-guaranteesfdap
paid: false
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Apache Iceberg", "Snowflake", "Databricks", "BigQuery", "Data Modeling", "Data Quality", "ETL"]
tags: [https, auto, good, image, media, github]
---

# GroupBy #9: FDAP stack, Iceberg and Hudi ACID Guarantees, Data Driven Management

*Plus: uber data analytics side project, dbt learning resource *

> Source: [Open post](https://vutr.substack.com/p/groupby-9-iceberg-and-hudi-acid-guaranteesfdap)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[bigquery|BigQuery]] · [[data-modeling|Data Modeling]] · [[data-quality|Data Quality]] · [[etl|ETL]]

---

*This is **GroupBy**, the place where I share with you guys the resources I learn from people smarter than me in data engineer field.*

*Not subscribed yet? Here you go:*

[Subscribe now](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!n_pC!,w_5760,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3a163344-18cc-4779-9b03-b43b58776ec8_1300x900.png)](https://substackcdn.com/image/fetch/$s_!n_pC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3a163344-18cc-4779-9b03-b43b58776ec8_1300x900.png)

---

> *👋 Hi, my name is Vu Trinh, a data engineer.*
>
> *I enjoy reading **good stuff** (related to data and engineering), and this newsletter is my effort on the journey to seek the "good stuff" across the entire Internet.*
>
> *Hope this issue find you well.*

---

# 🎯 Side Project

> *40+ hours of debugging and you still want some more?*

To get your hand dirty (more), this week I will bring you a project:

## **🚖 [Uber Data Analytics | End-To-End Data Engineering Project](https://www.youtube.com/watch?v=WpQECq5Hx9g)**

✍ [Darshil Parmar](http://linkedin.com/in/darshil-parmar)

[![](https://substackcdn.com/image/fetch/$s_!qfC6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F454d29c6-ca8b-45e0-85aa-2afc1f619aea_1426x446.png)](https://substackcdn.com/image/fetch/$s_!qfC6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F454d29c6-ca8b-45e0-85aa-2afc1f619aea_1426x446.png)

From author’s [github repo](https://github.com/darshilparmar/uber-etl-pipeline-data-engineering-project)

> *The goal of this project is to perform data analytics on Uber data using various tools and technologies, including GCP Storage, Python, Compute Instance, Mage Data Pipeline Tool, BigQuery, and Looker Studio.*
>
> — From Author’s [Github repo](https://github.com/darshilparmar/uber-etl-pipeline-data-engineering-project) —

## Suggestions from me to get life harder

> *Self-learn data modeling, concept like [scd type](https://chengzhizhao.com/unlocking-the-secrets-of-slowly-changing-dimension-scd-a-comprehensive-view-of-8-types), [Kimball data modeling approach](https://www.amazon.com/Data-Warehouse-Toolkit-Definitive-Dimensional/dp/1118530802), [different between Kimball and Inmon approach](https://tdan.com/data-warehouse-design-inmon-versus-kimball/20300),…*
>
> *Try to switch between [Mage](https://github.com/mage-ai/mage-ai) and [Airflow](https://airflow.apache.org/).*

---

# 🐙 Learning resource

> *I love to learn, and I assume you do too.*

[![](https://substackcdn.com/image/fetch/$s_!mtlL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0bbf96ff-8bc3-4add-83af-f62f3acb740f_1300x900.png)](https://substackcdn.com/image/fetch/$s_!mtlL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0bbf96ff-8bc3-4add-83af-f62f3acb740f_1300x900.png)

[dbt](https://github.com/dbt-labs/dbt-core), a popular tool for abstraction transforming and modeling data.

Learning dbt is essential for streamlining data processes, ensuring data quality, and accelerating analytics development, making it a valuable skill for anyone involved in data analysis and management.

Here some (FREE) learning resource:

## 🎓 | [dbt Fundamentals](https://courses.getdbt.com/courses/fundamentals)

> *Learn the Fundamentals of dbt including modeling, sources, testing, documentation, and deployment. (approximately 5 hours)*

## **🎓** | **[Jinja, Macros, Packages](https://courses.getdbt.com/courses/jinja-macros-packages)**

> *Extend the functionality of dbt with Jinja/macros and leverage models and macros from packages. (approximately 2 hours)*

## **🎓** | **[Advanced Materializations](https://courses.getdbt.com/courses/advanced-materializations)**

> *Learn about the advanced materializations built into dbt Core - ephemeral models, incremental models, and snapshots. (approximately 2 hours)*

## **🎓** | **[Refactoring SQL for Modularity](https://courses.getdbt.com/courses/refactoring-sql-for-modularity)**

> *Learn with the analytics engineers of dbt Labs how to migrate legacy transformation code into modular dbt data models. Useful if you're porting stored procedures or SQL scripts into your dbt project. (approximately 3.5 hours)*

## **🎓** | **[Advanced Testing](https://courses.getdbt.com/courses/advanced-testing)**

> *Learn more about the theory of data testing and the practice of creating custom generic tests, leveraging tests in packages, and applying test configurations. (approximately 4 hours).*

Approximately 16.5 hours for you to understand that “dbt is not just a SQL generator“

---

# 🚀 Engineering

> *Engineering is the practice of using natural science, mathematics, and the engineering design process to solve technical problems, increase efficiency and productivity, and improve systems.* — *wikipedia*

## 📖┆**[Flight, DataFusion, Arrow, and Parquet: Using the FDAP Architecture to build InfluxDB 3.0](https://www.influxdata.com/blog/flight-datafusion-arrow-parquet-fdap-architecture-influxdb/)**

✍ [Andrew Lamb](https://www.linkedin.com/in/andrewalamb/)

> [![2 FDAP Diagram 10.25.2023v1](https://substackcdn.com/image/fetch/$s_!LewP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7db41c9e-6439-488b-b94c-2c1e313bf77a_1004x628.png "2 FDAP Diagram 10.25.2023v1")](https://substackcdn.com/image/fetch/$s_!LewP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7db41c9e-6439-488b-b94c-2c1e313bf77a_1004x628.png)
>
> The ***FDAP*** Stack

## 📖┆**[Iceberg and Hudi ACID Guarantees](https://tabular.io/blog/iceberg-hudi-acid-guarantees/)**┆Tablular

✍ **[Ryan Blue](https://www.linkedin.com/in/rdblue/)**

> *In this post, I make the case that Iceberg is reliable and Apache Hudi is not.*

## 📖┆**[Running Unified PubSub Client in Production at Pinterest](https://medium.com/pinterest-engineering/running-unified-pubsub-client-in-production-at-pinterest-64ae2e721daa)**

✍ [Pinterest Engineering](https://medium.com/@Pinterest_Engineering)

> *In a distributed PubSub environment, complexities related to client-server communication can often be hard blockers for application developers, and solving them often require a joint investigation between the application and platform teams.*

## 📖┆**[How we Built the Ingestion Framework](https://blog.open-metadata.org/how-we-built-the-ingestion-framework-1af0b6ff5c81)**┆[OpenMetadata](https://github.com/open-metadata/OpenMetadata)

✍ [Pere Miquel Brull](https://www.linkedin.com/in/pmbrull/)

> *Without metadata, there are no discovery, collaboration, or quality tests. The ingestion process is a requirement that unlocks the rest of the features, and we are constantly pushing for improvements.*

## 📖┆[Scheduling Jupyter Notebooks at Meta](https://engineering.fb.com/2023/08/29/security/scheduling-jupyter-notebooks-meta/)

✍ **[Steve Dini](https://www.linkedin.com/in/sdini/)**

> *At Meta, [Bento](https://developers.facebook.com/blog/post/2021/09/20/eli5-bento-interactive-notebook-empowers-development-collaboration-best-practices/) is our internal [Jupyter](https://jupyter.org/) notebooks platform that is leveraged by many internal users. Notebooks are also being used widely for creating reports and workflows (for example, performing [data ETL](https://en.wikipedia.org/wiki/Extract,_transform,_load)) that need to be repeated at certain intervals.*

---

# ✏ Data

> *The one thing that this job has taught me is that truth is stranger than fiction.*
>
> *— Predestination (2014)*

## 📖┆**[Data Driven Management: The Why, Who, What and How?](https://medium.com/@meskensjan/data-driven-management-the-why-who-what-and-how-3566ba1f028a)**

✍ [janmeskens](https://medium.com/@meskensjan/about)

> [![](https://substackcdn.com/image/fetch/$s_!b5ig!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8d8183dc-2c15-4f2b-be6c-5be0449726d8_1400x1018.png)](https://substackcdn.com/image/fetch/$s_!b5ig!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8d8183dc-2c15-4f2b-be6c-5be0449726d8_1400x1018.png)
>
> **Why? Who? How? What?** (Image: Article’s Author).

## 📖┆**[Going All-In On Data Quality](https://medium.com/@matt_weingarten/going-all-in-on-data-quality-5dce26095834)**

✍ [Matthew Weingarten](https://www.linkedin.com/in/matthewweingarten201/)

> *A principle that I think is useful to follow when it comes to data quality is the idea of staging tables*

## 📖┆[Data Quality ≠ Data Trust: Bridging the Data Trust Gap](https://metadataweekly.substack.com/p/data-quality-data-trust-bridging)

✍ **[Prukalpa](https://substack.com/@metadataweekly)**

> *A broken pipeline. A source system gone down. A change made to a column name. Three unique root causes, but the same end result: broken trust.*

## 📖┆[The Clash Between Data Quality and AI: Unisphere’s Latest Findings](https://www.dbta.com/Editorial/News-Flashes/The-Clash-Between-Data-Quality-and-AI-Unispheres-Latest-Findings-161192.aspx)

✍ [Sydney Blanchard](https://www.dbta.com/Authors/Sydney-Blanchard-9611.aspx)

> *Data quality issues have been a looming threat for any and all enterprises, often surfaced by the proliferation of new data analytics and AI projects that, incidentally, rely on good data to succeed.*

## 📖┆**[5 Signs That Your Data is Modeled Poorly](https://towardsdatascience.com/5-signs-that-your-data-is-modeled-poorly-a646e8d33be0)**

✍ [Matthew Gazzano](https://www.linkedin.com/in/matthewgazzano/)

> *To be able to model your teams data properly, you need to be able to conceptualize relevant business entities and organize them in a way that is conducive to common questions asked within your organization.*

---

# 🤖 AI┆ML┆Data Science

> *You know, Burke, I don’t know which species is worse.*
>
> *— Ripley, Aliens (1986)*

## 📖┆[The architecture of today’s LLM applications](https://github.blog/2023-10-30-the-architecture-of-todays-llm-applications/)┆[GitHub](https://github.com/)

✍ [Nicole Choi](https://github.com/nicchoi29)

> [![Diagram that lists the five steps to building a large language model application. Data source for diagram is detailed here: https://github.blog/?p=74969&preview=true#five-steps-to-building-an-llm-app](https://substackcdn.com/image/fetch/$s_!Uhyt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F17fbed75-819d-440a-9cef-a9b8d49fcade_1022x537.png "Diagram that lists the five steps to building a large language model application. Data source for diagram is detailed here: https://github.blog/?p=74969&preview=true#five-steps-to-building-an-llm-app")](https://substackcdn.com/image/fetch/$s_!Uhyt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F17fbed75-819d-440a-9cef-a9b8d49fcade_1022x537.png)

## 📖┆**[What I’m Reading on the Rise of Artificial Intelligence](https://barackobama.medium.com/what-im-reading-on-the-rise-of-artificial-intelligence-72e088918de2)**

✍ [Barack Obama](https://medium.com/@barackobama)

> *…I wanted to share some of the books, articles, and podcasts that have helped shape my perspective over the past year. This list offers a range of viewpoints on the threats, opportunities, and challenges posed by AI and some thoughtful ideas on how to respond.*

## 📖┆**[AI ‘breakthrough’: neural net has human-like ability to generalize language](https://www.nature.com/articles/d41586-023-03272-3)**

✍ [Max Kozlov](https://www.nature.com/search?author=Max+Kozlov) & [Celeste Biever](https://www.nature.com/search?author=Celeste+Biever)

> *Scientists have created a neural network with the human-like ability to make generalizations about language.*

## 📖┆**[Harvard professor Lawrence Lessig on why AI and social media are causing a free speech crisis for the internet](https://www.theverge.com/23929233/lawrence-lessig-free-speech-first-amendment-ai-content-moderation-decoder-interview)**

✍ [Nilay Patel](https://www.theverge.com/authors/nilay-patel)

> *After 30 years teaching law, the internet policy legend is as worried as you’d think about AI and TikTok — and he has surprising thoughts about balancing free speech with protecting democracy.*

---

# 🔥 Catch up

> *…Next Saturday night, we're sending you back to the future!*
>
> *— Dr. Emmett Brown, Back to the Future (1985)*

## [📖] [Airflow](https://airflow.apache.org/)┆[Release of Airflow 2.7.3](https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html#airflow-2-7-3-2023-11-04)

## [📖] [BigQuery](https://cloud.google.com/bigquery/?hl=en)┆[Work with text analyzers](https://cloud.google.com/bigquery/docs/text-analysis-search)

## [📖] [Spark](https://spark.apache.org/)┆**[Arrow-optimized Python UDFs in Apache Spark™ 3.5](https://www.databricks.com/blog/arrow-optimized-python-udfs-apache-sparktm-35)**

## [📖] [Google Cloud](https://cloud.google.com/free/?utm_source=google&utm_medium=cpc&utm_campaign=japac-VN-all-vi-dr-BKWS-all-core-trial-EXA-dr-1605216&utm_content=text-ad-none-none-DEV_c-CRE_602400826505-ADGP_Hybrid%20%7C%20BKWS%20-%20EXA%20%7C%20Txt%20~%20GCP_General_core%20brand_main-KWID_43700071566406837-aud-1640178259900%3Akwd-6458750523&userloc_1028581-network_g&utm_term=KW_google%20cloud&gad_source=1&gclid=CjwKCAiAxreqBhAxEiwAfGfndOPJ3d5EZRRhdqTpUSx72vDbrhCVBS_4J5gQFslRauoylYLgiePDcBoCdbEQAvD_BwE&gclsrc=aw.ds)┆[Cloud Functions now supports the Python 3.12 runtime.](https://cloud.google.com/functions/docs/concepts/python-runtime)

## [📖] [Snowflake](https://www.snowflake.com/en/)┆**[Search Optimization: Support for Substring Search in Semi-Structured Data](https://docs.snowflake.com/en/release-notes/2023/7_40#search-optimization-support-for-substring-search-in-semi-structured-data-general-availability)**

`🚨 The next section contain my own writing. Don't blame me if you feel distressed after reading this; you chose to read it, although you can skip without thinking twice.`

# 🥷 It will steal 97 seconds from you

> *Random thoughts, ideas.*

The hardest truth I’ve learned as a data engineer is this: No matter how fancy your pipeline or infrastructure is, if your data foundation doesn't have the ability to support the business, everything you do is just 💩.

You put in all your effort to deliver an internal tool to support analytics, but nobody uses it.

Your tool is 💩.

You tune your SQL script to run 2.5x faster, but the data output is “wrong” and leads to “really bad“ decisions.

Your SQL script is 💩.

The lesson here is that anything you do, if you want it to bring value (so that you can lead a meaningful life), make sure it can help your “customer” solve problems.

Put yourself in your customer’s shoes.

Before developing an internal tool, sit down and talk to your DAs and DSs.

When developing a data pipeline, talk to the business to help define “constraints” and “rules” to control the quality and correctness of your data.

So, to apply this lesson and save this newsletter from being 💩…

…I need you…

…yes, you, the “customers” of this newsletter.

I need your feedback on which aspects I need to improve and things that you expect from this newsletter to help me grow as a DE.

(In the comment section or directly contact me through my [mail](http://vutrinh2704@gmail.com) or [linkedIn](https://www.linkedin.com/in/vutr27/))

I will adjust my work.

Promise. (Unless your ideas is too “wild”)

> *Switching the context between “your DE work is 💩 if … “ to “I need your feedback“ is… weird."*

# “Hasta la vista, baby”

# -T800, Terminator 2: Judgment Day (1991)

Thanks for scrolling this far ! Convenient subscribe box here in case you want to scroll my newsletter right in your mailbox :D
