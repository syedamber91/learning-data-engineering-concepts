---
title: "GroupBy #20: How Google takes the pain out of code reviews, The Difficulties of Senior Engineer are not Engineering"
channel: vutr
author: "Vu Trinh"
published: 2024-01-30
url: https://vutr.substack.com/p/groupby-20-how-google-takes-the-pain
paid: false
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Kafka", "Apache Spark", "Delta Lake", "BigQuery", "Data Quality", "ETL"]
tags: [https, engineering, medium, github, blog, code]
---

# GroupBy #20: How Google takes the pain out of code reviews, The Difficulties of Senior Engineer are not Engineering

*Plus: End-to-End Data Engineering System on Real Data with Kafka, Spark, Airflow, Postgres, and Docker, Uplevel your dbt workflow*

> Source: [Open post](https://vutr.substack.com/p/groupby-20-how-google-takes-the-pain)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[data-quality|Data Quality]] · [[etl|ETL]]

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

[![](https://substackcdn.com/image/fetch/$s_!f_sK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fabb45b10-6add-4605-b4a9-e5a6407286f8_1300x900.png)](https://substackcdn.com/image/fetch/$s_!f_sK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fabb45b10-6add-4605-b4a9-e5a6407286f8_1300x900.png)

a sad astronaut

---

# 🎯 Side Project

> *40+ hours of debugging and you still want some more?*

#### 📖┆[End-to-End Data Engineering System on Real Data with Kafka, Spark, Airflow, Postgres, and Docker](https://towardsdev.com/end-to-end-data-engineering-system-on-real-data-with-kafka-spark-airflow-postgres-and-docker-a70e18df4090)

✍ [Hamza Gharbi](https://medium.com/@hamzagharbi_19502?source=post_page-----a70e18df4090--------------------------------)

> *This article is part of a project that’s split into two main phases. The first phase focuses on building a data pipeline. This involves getting data from an API and storing it in a PostgreSQL database. In the second phase, we’ll develop an application that uses a language model to interact with this database.*

---

# 📈 Career

> *Don't let comfort hold you back.*

#### 📖┆[Manager = Promotion?](https://koopingshung.substack.com/p/manager-promotion)

✍ [Koo Ping Shung](https://substack.com/profile/7906875-koo-ping-shung)

> *My opinion is becoming a manager should not be seen as ‘rewarding’ someone who has performed well in his/her current role. Rather, being put on a managing position is seen as giving someone a change of environment and/or new challenges.*

#### 📖┆[The Difficulties of Senior Engineer …. are not Engineering](https://www.confessionsofadataguy.com/the-difficulties-of-senior-engineer-are-not-engineering/)

✍ [Daniel Beach](https://www.linkedin.com/in/daniel-beach-6ab8b4132/)

> *I decided I wanted to write code for a living so I didn’t have to talk and deal with other people much. Let my work speak for itself. Write perfect code, let the rest of the world worship at my feet, all for the wonderful and fantastical abstractions and problems I solved. Yet something changed.*

#### 📖┆[Things Data Teams Overlook](https://medium.com/@matt_weingarten/things-data-teams-overlook-e72d3625eb00)

✍ [Matt Weingarten](https://medium.com/@matt_weingarten?source=post_page-----e72d3625eb00--------------------------------)

> *I wanted to share what I thought were the most important ones from my experience in the data world so far.*

#### 📖┆[The Most Important Soft Skill in Tech](https://leo-godin.medium.com/the-most-important-soft-skill-in-tech-4316ca84a453)

✍ [Leo Godin](https://leo-godin.medium.com/?source=post_page-----4316ca84a453--------------------------------)

> *Let’s talk about the most important soft skill in tech. Interviewing*

#### 📖┆[10 unconventional lessons from 10 years working as a software engineer](https://levelup.gitconnected.com/10-unconventional-lessons-from-10-years-working-as-a-software-engineer-873d5d4ae4a2)

✍ [Pablo Porto](https://medium.com/@pablo.porto?source=post_page-----873d5d4ae4a2--------------------------------)

> *Whether your are just starting or your are experienced engineer, I think you can find these lessons useful to build an effective, meaningful and sustainable career as a software engineer.*

---

# 🚀 Engineering

> *I have to believe in a world outside my own mind. — Memento (2000)*

#### 📖┆[How to get in the flow while coding (and why it’s important)](https://github.blog/2024-01-22-how-to-get-in-the-flow-while-coding-and-why-its-important/)

✍ [Gwen Davis](https://github.blog/author/purpledragon85/)

> *In this blog, we’ll explore what flow state entails, its benefits, and three tips for reaching it the next time you sit down to code. Let’s go.*

#### 📖┆[Meeting DoorDash Growth with a Self-Service Logistics Configuration Platform](https://doordash.engineering/2024/01/23/meeting-doordash-growth-with-a-self-service-logistics-configuration-platform/)

✍ [Saurabh Gupta, Reid Arwood](http://127.0.0.1:5500/reminder.com)

> *DoorDash has grown from executing simple restaurant deliveries to working with a wide variety of businesses, ranging from grocery and retail to parcels and pet supplies. Each business faces its own set of constraints as it strives to meet its goals. Our logistics teams — which range across a number of functions, including Dashers, assignment, payment processes, and time estimations — seek to achieve these goals by tuning a variety of configurations for each use case and type of business.*

#### 📖┆[Airflow Evolution at Snap](https://medium.com/apache-airflow/airflow-evolution-at-snap-c988cdd95abd)

✍ [Yuri Desyatnik](https://medium.com/@ydesyatnik_29285?source=post_page-----c988cdd95abd--------------------------------)

> *Snap uses Airflow to power all the business needs of our products. We have over 3,000 DAGs that run over 330 thousand task instances every day, including ETL, reporting/analytics, some ML workloads and others.*

#### 📖┆[Migrating Policy Delivery Engines with (almost) Nobody Knowing](https://medium.com/pinterest-engineering/migrating-policy-delivery-engines-with-almost-nobody-knowing-839f3cf996bc)

✍ [Pinterest Engineering](https://medium.com/@Pinterest_Engineering?source=post_page-----839f3cf996bc--------------------------------)

> *This blog post is focused on how the Security team moved hundreds of policies and dozens of customers from the Zookeeper model to a safer, more reliable, and more configurable config deployment approach.*

#### 📖┆[Which is Cheaper: Serverless or Servers?](https://mikaelvesavuori.medium.com/which-is-cheaper-serverless-or-servers-1b18816ce7f6)

✍ [Mikael Vesavuori](https://mikaelvesavuori.medium.com/?source=post_page-----1b18816ce7f6--------------------------------)

> *Taking a simplified look at the costs of running workloads on common AWS compute services. TL;DR? “It depends”.*

#### 📖┆[How Google takes the pain out of code reviews, with 97% dev satisfaction](https://read.engineerscodex.com/p/how-google-takes-the-pain-out-of)

✍ [Engineer’s Codex](https://read.engineerscodex.com/about)

> In this article, I dive into:
>
> * Google’s guidelines for efficient code review
> * Critique, their code review tooling, and AI-powered improvements
> * Internal statistics on Google code reviews
> * Why Critique seems to be so loved by Googlers

#### 📖┆[Uplevel your dbt workflow with these tools and techniques](https://www.startdataengineering.com/post/uplevel-dbt-workflow/)

✍ [Start Data Engineering](https://www.startdataengineering.com/)

> *In this post, we will go over some approaches you can quickly set up in your dbt project to improve development speed, confidently deploy while ensuring that your changes will not break datasets, enhance code quality, reduce feedback loop time, and ensure data quality.*

#### 📖┆[Hive Metastore - Did We Replace It With A Vendor Lock?](https://lakefs.io/blog/hive-metastore-vendor-lock/)

✍ [Oz Katz](https://www.linkedin.com/in/oz-katz-4b3b389), [Einat Orr](https://www.linkedin.com/in/einat-orr-359ba6)

> *In this blog we will consider in what sense Hive’s Metastore is “open” and why we believe the leading candidates to replace it are closed, in a way that is meant to limit us to using a specific vendor’s data ecosystem.*

#### 📖┆[Serverless ClickHouse Cloud - ASDS Chapter 5 (Part 1)](https://jack-vanlightly.com/analyses/2024/1/23/serverless-clickhouse-cloud-asds-chapter-5-part-1)

✍ [Jack Vanlightly](https://jack-vanlightly.com/home)

> *ClickHouse is an open-source, column-oriented, distributed (real-time) OLAP database management system. ClickHouse Cloud offers serverless Clickhouse clusters, billed according to the compute and storage resources consumed.*

#### 📖┆[Stopping Uber Fraudsters Through Risk Challenges](https://www.uber.com/en-SG/blog/stopping-uber-fraudsters-through-risk-challenges/)

✍ [Stephanie Yen](https://www.linkedin.com/in/steph-yen/)

> *As a marketplace-based, consumer-facing app, Uber encounters a multitude of sources of fraud across its platform. In one of the most common cases of fraud, bad actors use various methods to attempt to bypass payments for Uber rides, Eats orders, and other services, like Uber for Business. When this happens, failed transactions can occur, incurring losses that affect the drivers and businesses operating on Uber.*

#### 📖┆[How GitHub’s Developer Experience team improved innerloop development](https://github.blog/2024-01-24-how-githubs-developer-experience-team-improved-innerloop-development/)

✍ [Belal Taher](https://github.blog/author/belaltaher8/)

> *Solving the ecosystem problem is always a balancing act. Luckily, thanks to GitHub’s push towards containerization, and tooling such as repository automation and publishing/consuming releases through the GitHub CLI, we were adequately equipped to develop a solution with HCS.*

---

# ✏ Data

> *The one thing that this job has taught me is that truth is stranger than fiction. — Predestination (2014)*

#### 📖┆[Getting Rid of Dashboard Sprawl](https://sqlpatterns.com/p/getting-rid-of-dashboard-sprawl)

✍ [Ergest Xheblati](https://substack.com/@ergestx)

> *The beauty of the dashboard tree is that it reveals knowledge through structure, so over time it becomes a living document for how the business works. It shows how value flows in the organization.*

#### 📖┆[A Deep Dive into Agoda's Generic Reconciliation Platform](https://medium.com/agoda-engineering/a-deep-dive-into-agodas-generic-reconciliation-platform-06cab9a98145)

✍ [Songkun Viriyavaree](https://www.linkedin.com/in/songkun-viriyavaree/)

> *This article will explore how we approach the creation of a reconciliation system. Our goal is to build a system that is both scalable and reliable. We plan to achieve this by effectively utilizing Spark.*

#### 📖┆[Taking the leap towards building trusted data sets](https://roundup.getdbt.com/p/taking-the-leap-towards-building)

✍ [Doug Beatty](https://substack.com/@dbeatty10)

> *In analytics engineering, software-inspired unit tests serve as these practice run-ups. They ensure each transformation performs as expected before integrating it into the larger project. Just as a long jumper will use practice run-ups to make sure they are ready to compete, developers can use unit tests beforehand to make sure their code is ready for a variety of scenarios when it’s “go time” for building production data.*

---

# 🤖 AI┆ML┆Data Science

> *You know, Burke, I don’t know which species is worse. — Ripley, Aliens (1986)*

#### 📖┆[10 unexpected ways to use GitHub Copilot](https://github.blog/2024-01-22-10-unexpected-ways-to-use-github-copilot/)

✍ [Kedasha Kerr](https://github.blog/author/ladykerr/)

> *In this post, we’ll explore 10 use cases where GitHub Copilot can help reduce friction during your developer workflow. This includes pull requests, working from the command line, debugging CI/CD workflows, and much more!*

#### 📖┆[Why is machine learning 'hard'?](https://ai.stanford.edu/~zayd/why-is-machine-learning-hard.html)

✍ [S. Zayd Enam](https://twitter.com/zaydenam)

> *However, machine learning remains a relatively ‘hard’ problem. There is no doubt the science of advancing machine learning algorithms through research is difficult. It requires creativity, experimentation and tenacity. Machine learning remains a hard problem when implementing existing algorithms and models to work well for your new application. Engineers specializing in machine learning continue to command a salary premium in the job market over standard software engineers.*

---

# 🔥 Catch up

> *…Next Saturday night, we're sending you back to the future! — Dr. Emmett Brown, Back to the Future (1985)*

#### 📖┆[BigQuery | now natively supports the Delta Lake format for Amazon S3 and Azure tables. This feature is now in preview.](https://cloud.google.com/bigquery/docs/omni-aws-create-external-table#delta-lake-tables)

---

# 💠 Previously on Dimension

> *Dimension is my sub-newsletter where I note down things I learn from people smarter than me in the data engineering field.*

Here are 3 the latest articles:

### ***Published on 2024, January 13:***

### ***Published on 2024, January 20:***

### ***Published on 2024, January 27:***

Let me here your voice, for example:

'Your newsletter is so terrible, I can't handle it anymore.'

[Leave a comment](https://vutr.substack.com/p/groupby-20-how-google-takes-the-pain/comments)

---

## “Hasta la vista, baby”

## -T800, Terminator 2: Judgment Day (1991)

Thanks for scrolling this far! There's a convenient subscribe box here if you want me to annoy you every week. 😄
