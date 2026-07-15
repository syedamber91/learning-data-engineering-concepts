---
title: "GroupBy #14: What it takes to be a Senior IC at Meta, Netflix Data Engineering Summit"
channel: vutr
author: "Vu Trinh"
published: 2023-12-19
url: https://vutr.substack.com/p/groupby-14-what-it-takes-to-be-a
paid: false
topics: ["Data Engineering", "dbt", "Apache Airflow", "BigQuery", "Data Modeling", "Data Warehouse", "Data Quality", "ETL"]
tags: [https, engineering, blog, auto, substack, medium]
---

# GroupBy #14: What it takes to be a Senior IC at Meta, Netflix Data Engineering Summit

*Plus: GCP Data Engineering Project, Conceptual vs logical vs physical data models*

> Source: [Open post](https://vutr.substack.com/p/groupby-14-what-it-takes-to-be-a)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[bigquery|BigQuery]] · [[data-modeling|Data Modeling]] · [[data-warehouse|Data Warehouse]] · [[data-quality|Data Quality]] · [[etl|ETL]]

---

*This is **GroupBy**, the place where I share with you guys the resources I learn from people smarter than me in data engineer field.*

*Not subscribed yet? Here you go:*

[Subscribe now](https://vutr.substack.com/subscribe?)

---

![](https://substackcdn.com/image/fetch/$s_!D8N-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fvutr.substack.com%2Fimg%2Fsubstack.png)

Get more from Vu Trinh in the Substack app

Available for iOS and Android

[Get the app](https://substack.com/app/app-store-redirect?utm_campaign=app-marketing&utm_content=author-post-insert&utm_source=vutr)

[![](https://substackcdn.com/image/fetch/$s_!_wmj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0f95e709-ff16-43c5-8acb-49257bbba215_1300x900.png)](https://substackcdn.com/image/fetch/$s_!_wmj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0f95e709-ff16-43c5-8acb-49257bbba215_1300x900.png)

Santa Claus is drinking hot chocolate in the egg-like spaceship while shipping gifts for the entire universe. [credit](https://www.canva.com/ai-image-generator/)

---

> *👋 Hi, my name is Vu Trinh, a data engineer.*
>
> *I enjoy reading **good stuff** (related to data and engineering), and this newsletter is my effort on the journey to seek the "good stuff" across the entire Internet.*
>
> *Hope this issue find you well.*

---

> *I won't be able to see you guys until next Tuesday, the 26th, so...*
>
> *🎄🎄 Merry Christmas, everyone! ☃️☃️*
>
> *Our job is tough, guys.*
>
> *We handle “where-is-my-data” and “why-is-my-report-so-weird” every day.*
>
> *That needs a lot of bravery and energy.*
>
> *So, during a vacation like this, make sure to spend quality time with family and the ones you love…*
>
> *… and be ready for more “where-is-my-data” and “why-is-my-report-so-weird.”*
>
> *(It’s a loop)*

---

# 🎯 Side Project

> *40+ hours of debugging and you still want some more?*

## 🗃️┆[GCP Data Engineering Project: Building and Orchestrating an ETL Pipeline with Apache Beam and Apache Airflow](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow)

✍ [Jana Polianskaja](https://www.linkedin.com/in/jana-polianskaja/)

> *The pipeline is designed to handle batch transactional data and leverages various Google Cloud Platform (GCP) services:*
>
> * *GCS is used to store and manage the transactional data*
> * *Composer, a managed Apache Airflow service, is utilized to orchestrate Dataflow jobs*
> * *Dataflow, based on Apache Beam, is responsible for data processing, transformation, and loading into BigQuery*
> * *BigQuery serves as a serverless data warehouse*
> * *Looker, a business intelligence and analytics platform, is employed to generate daily reports*

[![](https://substackcdn.com/image/fetch/$s_!jo6O!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F359e6f11-0426-4942-9950-a5798a3b9327_876x412.jpeg)](https://substackcdn.com/image/fetch/$s_!jo6O!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F359e6f11-0426-4942-9950-a5798a3b9327_876x412.jpeg)

[source](https://github.com/janaom/gcp-data-engineering-etl-with-composer-dataflow)

---

# 🐙 Learning resource

> *I love to learn, and I assume you do too.*

## 🎓┆**[Distributed Systems lecture series](https://www.youtube.com/playlist?list=PLeKd45zvjcDFUEv_ohr_HdUFe97RItdiB)**

✍ [Dr. Martin Kleppmann](https://martin.kleppmann.com/)

> *These videos form an 8-lecture series on distributed systems, given as part of the undergraduate computer science course at the University of Cambridge.*

If you looking for recommendation on Data Engineering Books (by Google, Chat GPT, Reddit, Twitter, whatever…), [Designing Data-Intensive Applications](https://www.amazon.com/Designing-Data-Intensive-Applications-Reliable-Maintainable/dp/1449373321) will surely be in the list.

I read the book not too long ago and searched for more resources by the author on the internet. Somehow (I forgot how), I discovered a YouTube playlist about distributed systems by from the author.

It’s pirate’s treasure.

You’ll not regret after consuming this.

Trust me.

---

# 🚀 Engineering

> *I have to believe in a world outside my own mind.* — Memento *(2000)*

## 📖┆[The 7 rules for successful job hopping in data engineering](https://blog.dataengineer.io/p/the-7-rules-for-successful-job-hopping)

✍ [Zach Wilson](https://substack.com/profile/10367987-zach-wilson)

> *Remember, the job hopping rules are:*
>
> * *Onboard quickly and deliver value in the first 1-2 months*
> * *Within the first year, start working on the highest priority work in your domain area*
> * *Always have a measurable impact everywhere that you go!*
> * *Don’t force yourself to get a promotion from a manager who doesn’t believe in you! It’s a losing battle!*
> * *Be a glue person. Do the work nobody wants to do and save your new teammates headaches!*
> * *Remember to live a life you enjoy, don’t just be obsessed with work*
> * *When interviewing, ALWAYS say you’re interviewing with other companies even if you aren’t. It makes negotiations easier and you’ll be treated better in the interview process*

## 📖┆[Kubernetes for Data Engineers](https://dataengineeringcentral.substack.com/p/kubernetes-for-data-engineers?utm_source=substack&utm_medium=email&utm_content=share)

✍ [Daniel Beach](https://substack.com/profile/21715962-daniel-beach)

> *We want to give Data Engineers an introduction to Kubernetes. It's a tool everyone talks about, but not that many folks get a chance to get their hands dirty with.*

## 📖┆**[ClickHouse is in the house](https://medium.com/vimeo-engineering-blog/clickhouse-is-in-the-house-413862c8ac28)**

✍ [zeev](https://medium.com/@ZeevFeldbeine) - [Vimeo Engineering Blog](https://medium.com/vimeo-engineering-blog?source=post_page-----413862c8ac28--------------------------------)

> *In this post, I’ll outline our journey from a traditional architecture anchored in [Apache Phoenix](https://phoenix.apache.org/) on [HBase](https://hbase.apache.org/) to our embrace of [ClickHouse](https://clickhouse.com/docs/en/development/architecture) just eighteen months ago.*

## 📖┆**[What it takes to be a Senior IC at Meta](https://medium.com/@AnalyticsAtMeta/being-a-senior-ic-59ee705ba3c1)**

✍ [Analytics at Meta](https://medium.com/@AnalyticsAtMeta?source=post_page-----59ee705ba3c1--------------------------------)

> *At Meta, senior individual contributors (ICs) are an important part of how we think about growing careers and building effective organizations in data science and data engineering.*

## 📖┆[Our First Netflix Data Engineering Summit](https://netflixtechblog.com/our-first-netflix-data-engineering-summit-f326b0589102)

✍ [Netflix Technology Blog](https://netflixtechblog.medium.com/)

> *Earlier this summer Netflix held our first-ever Data Engineering Forum. Engineers from across the company came together to share best practices on everything from Data Processing Patterns to Building Reliable Data Pipelines.*

---

# ✏ Data

> *The one thing that this job has taught me is that truth is stranger than fiction. — Predestination (2014)*

## 🎙️┆[Data Ecosystems, Moats, Semantic Layers, and More w/ Tristan Handy](https://www.linkedin.com/events/dataecosystems-moats-semanticla7139774552993144832/theater/)

🎤 [Joe Reis](https://www.linkedin.com/in/josephreis/), [Matthew Housley](https://www.linkedin.com/in/housleymatthew/) ,[Tristan Handy](https://www.linkedin.com/in/tristanhandy/)

> *Tristan Handy (CEO of dbt Labs) joins the show to chat about the data tooling landscape, business moats, semantic layers, the data engineering ecosystem, and much more.*

## 📖┆[Conceptual vs logical vs physical data models](https://www.thoughtspot.com/data-trends/data-modeling/conceptual-vs-logical-vs-physical-data-models?fbclid=IwAR23G0vOHxATthOyLfHWRp_16528I_b5DXg8Ubz23-gMjM7Lqlcb3BUC9Rg)

✍ [Sonny Rivera](https://www.thoughtspot.com/author/sonny-rivera)

> *Data modeling is not about creating diagrams for documentation sake. It's about creating a shared understanding between the business and the data teams, building trust, and delivering value with data.*

[![](https://substackcdn.com/image/fetch/$s_!x-_-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb835d0de-cd19-4b8a-9309-15bb7be5b0de.avif)](https://substackcdn.com/image/fetch/$s_!x-_-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb835d0de-cd19-4b8a-9309-15bb7be5b0de.avif)

[source](https://www.thoughtspot.com/data-trends/data-modeling/conceptual-vs-logical-vs-physical-data-models?fbclid=IwAR23G0vOHxATthOyLfHWRp_16528I_b5DXg8Ubz23-gMjM7Lqlcb3BUC9Rg)

## 📖┆[Unstructured Data Unravelled](https://www.thdpth.com/p/unstructured-data-unravelled)

✍ [Sven Balnojan](https://substack.com/profile/229923-sven-balnojan)

> *Key lesson: Never discard data because you think it's “unstructured.” All data is, and no data is.*

## 📖┆[How we built consistent product launch metrics with the dbt Semantic Layer.](https://docs.getdbt.com/blog/product-analytics-pipeline-with-dbt-semantic-layer)

✍ [Jordan Stein](https://www.linkedin.com/in/jstein5/)

> *This blog post walks through the end-to-end process we used to set up product analytics for the dbt Semantic Layer using the dbt Semantic Layer.*

## 📖┆[The Data Quality Resolution Process](https://dataproducts.substack.com/p/the-data-quality-resolution-process)

✍ [Mark Freeman](https://substack.com/profile/139605027-mark-freeman)

> *Below I provide details, code examples, diagrams, and communication strategies to help you resolve data quality issues when you are a low-data maturity company.*

---

# 🤖 AI┆ML┆Data Science

> *You know, Burke, I don’t know which species is worse. — Ripley, Aliens (1986)*

## 📖┆[Extracting skills from content to fuel the LinkedIn Skills Graph](https://engineering.linkedin.com/blog/2023/extracting-skills-from-content-to-fuel-the-linkedin-skills-graph)

✍ [Ji Yan](https://engineering.linkedin.com/blog/authors/j/ji-yan)

> *In this blog, we'll examine how we use AI to extract skills from various content sources across LinkedIn and map these skills to our Skills Graph.*

## 📖┆[Why Meta is fighting for Open Source LLMs while Microsoft wants to regulate them.](https://medium.datadriveninvestor.com/why-meta-is-fighting-for-open-source-llms-while-microsoft-wants-to-regulate-them-a8f598ff0abf)

✍ [Devansh](https://medium.datadriveninvestor.comhttps//machine-learning-made-simple.medium.com/?source=post_page-----a8f598ff0abf--------------------------------)

> *How Open Source vs Licensed Debate became important for Big Tech business strategy*

## 📖┆[Declarative Feature Engineering at PayPal](https://medium.com/paypal-tech/declarative-feature-engineering-at-paypal-eddcae81c06d)

✍ [Marina Lyan](https://medium.com/@maralyan?source=post_page-----eddcae81c06d--------------------------------)

> *The idea is to allow data scientists to write a declaration of what their features look like rather than explicitly specify how to construct them on top of different execution platforms.*

## 📖┆[Improving Uber Eats Home Feed Recommendations via Debiased Relevance Predictions](https://www.uber.com/en-SG/blog/improving-uber-eats-home-feed-recommendations/)

✍ [Uber Engineering Blog](https://www.uber.com/en-SG/blog/engineering/?uclick_id=15b6739c-0acd-406e-bdf6-884992beefa0)

> *In this blog post, we focus on tackling arguably one of the most important such biases: the position bias. Position bias refers to the phenomenon in which users tend to order more from stores ranked higher compared to stores that are ranked lower, irrespective of how relevant that store truly is to the user.*

## 📖┆[Personalizing the DoorDash Retail Store Page Experience](https://doordash.engineering/2023/12/12/personalizing-the-doordash-retail-store-page-experience/)

✍ **[Luming Chen, Yuan Meng, Anthony Zhou](https://doordash.engineering/2023/12/12/personalizing-the-doordash-retail-store-page-experience/#)**

> *In this post, we show how we built a personalized shopping experience for our new business vertical stores, which include grocery, convenience, pets, and alcohol, among many others.*

---

# 🔥 Catch up

> *…Next Saturday night, we're sending you back to the future!*
>
> *— Dr. Emmett Brown, Back to the Future (1985)*

## 📖┆BigQuery

* [cross-cloud](https://cloud.google.com/blog/products/data-analytics/introducing-bigquery-omni-cross-cloud-materialized-views/) materialized view

  + You can now take advantage of the benefits of [materialized views over Amazon S3 metadata cache-enabled BigLake tables](https://cloud.google.com/bigquery/docs/materialized-views-intro#biglake).
  + You can create [materialized view replicas](https://cloud.google.com/bigquery/docs/materialized-views-intro#materialized_view_replicas) of materialized views over Amazon S3 metadata cache-enabled BigLake tables. Materialized view replicas let you use the materialized view data in queries while avoiding data egress costs and improving query performance.
* Integration

  + The BigQuery Data Transfer Service now supports [federated workforce identities](https://cloud.google.com/iam/docs/workforce-identity-federation) when creating a data transfer from most data sources. This feature is [generally available](https://cloud.google.com/products/#product-launch-stages) (GA).
  + The [Apache Hive connector](https://cloud.google.com/bigquery/docs/programmatic-analysis#apache_hadoop_apache_spark_and_apache_hive) is now [generally available](https://cloud.google.com/products/#product-launch-stages) (GA) for data analytics pipeline migration.

---

# 🥷 It will steal 7 seconds from you

> *Random thoughts, ideas.*

I’m planning for a new kind of content for my newsletter.

I will let you guys know soon.

> *If one of these things happens in the next months:*
>
> * *Existential crisis*
> * *My Substack gets hacked*
> * *I get fired from my current job.*
> * *The Internet is down*
>
> *…I don’t know if it can be considered “soon” anymore.*

🤨 “Soon” is a dangerous word.

Let me here your voice, for example:

'Your newsletter is so terrible, I can't handle it anymore.'

[Leave a comment](https://vutr.substack.com/p/groupby-14-what-it-takes-to-be-a/comments)

---

# “Hasta la vista, baby”

# -T800, Terminator 2: Judgment Day (1991)

Thanks for scrolling this far! There's a convenient subscribe box here if you want me to annoy you every week. 😄
