---
title: "GroupBy #19: How Apple built iCloud to store billions of databases, Palette-Uber feature store, Definition of Data Modeling"
channel: vutr
author: "Vu Trinh"
published: 2024-01-23
url: https://vutr.substack.com/p/groupby-19-how-apple-built-icloud
paid: false
topics: ["Data Engineering", "Apache Airflow", "Apache Iceberg", "Snowflake", "Databricks", "Delta Lake", "BigQuery", "Data Modeling", "Data Quality"]
tags: [https, blog, cloud, engineering, medium, substack]
---

# GroupBy #19: How Apple built iCloud to store billions of databases, Palette-Uber feature store, Definition of Data Modeling

*Plus: Machine Learning Pipelines with Airflow and Mlflow, How to craft the perfect data engineer resume*

> Source: [Open post](https://vutr.substack.com/p/groupby-19-how-apple-built-icloud)

## Topics

[[data-engineering|Data Engineering]] · [[apache-airflow|Apache Airflow]] · [[apache-iceberg|Apache Iceberg]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[data-modeling|Data Modeling]] · [[data-quality|Data Quality]]

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

[![](https://substackcdn.com/image/fetch/$s_!JSG4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff2ee6b15-e629-4eea-b20e-a569b9721331_1300x900.png)](https://substackcdn.com/image/fetch/$s_!JSG4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff2ee6b15-e629-4eea-b20e-a569b9721331_1300x900.png)

---

# 🎯 Side Project

> *40+ hours of debugging and you still want some more?*

#### 📖┆[Build Machine Learning Pipelines with Airflow and Mlflow: Reservation Cancellation Forecasting](https://towardsdatascience.com/build-machine-learning-pipelines-with-airflow-and-mlflow-reservation-cancellation-forecasting-da675d409842)

✍ [Jeremy Arancio](https://medium.com/@jeremyarancio?source=post_page-----da675d409842--------------------------------)

> *Learn how to create reproducible and ready-for-production Machine Learning pipelines through a Senior Machine Learning assignment*

---

# 📈 Career

> *Don't let comfort hold you back.*

#### 📖┆[How to craft the perfect data engineer resume and LinkedIn profile in 2024](https://blog.dataengineer.io/p/how-to-craft-the-perfect-data-engineer)

✍ [Zach Wilson](https://substack.com/profile/10367987-zach-wilson)

> *2024 is a time to stay nimble in your employee journey and remember that no job is so good that you’re immune to being laid off!*

---

# 🐙 Learning resource

> *I love to learn, and I assume you do too.*

#### 📖┆[Ten new generative AI trainings to upskill in 2024 with Duet AI](https://cloud.google.com/blog/topics/training-certifications/ten-new-generative-ai-trainings-to-upskill-in-2024-with-duet-ai/)

> *Check out our recommended top ten list of short trainings available on Duet AI, for developers, data analysts, cloud engineers, architects, security engineers, and Workspace users.*

---

# 🚀 Engineering

> *I have to believe in a world outside my own mind. — Memento (2000)*

#### 📖┆[Improving Recruiting Efficiency with a Hybrid Bulk Data Processing Framework](https://engineering.linkedin.com/blog/2023/improving-recruiting-efficiency-with-a-hybrid-bulk-data-processi)

✍ [Aditya Hegde](https://engineering.linkedin.com/blog/authors/a/aditya-hegde)

> *With our new data processing framework, we were able to observe a multitude of benefits, including 99.9% request success rates, 78% reduction in customer escalations, and automatic recovery from transient errors. In this post, we will cover unique challenges we faced, our solutions design and architecture, the tech stack used, and the performance results we achieved.*

#### 📖┆[The Evolution of Enforcing our Professional Community Policies at Scale](https://engineering.linkedin.com/blog/2023/the-evolution-of-enforcing-our-professional-community-policies-a)

✍ [Amit Mathapati](https://engineering.linkedin.com/blog/authors/a/amit-mathapati)

> *In this blog post, we'll go deeper into how we manage account restrictions. We'll talk about the changes we've made over the years to keep up with LinkedIn's growth and scale our infrastructure quickly.*

#### 📖┆[How Apple built iCloud to store billions of databases](https://read.engineerscodex.com/p/how-apple-built-icloud-to-store-billions)

✍ [Engineer’s Codex](https://read.engineerscodex.com/)

> *Apple uses Cassandra and FoundationDB for CloudKit, their cloud backend service. We take a look into how exactly each is used within their cloud and the problems they've solved.*

#### 📖┆[Shallow Copy For Data: What Are Your Options?](https://lakefs.io/blog/shallow-copy-data/)

✍ [Idan Novogroder](https://lakefs.io/author/idan-novogroder/)

> *Keep reading to learn more about the concept of data shallow copy and dive into the use cases from Databricks Delta Lake, Iceberg, Snowflake, and lakeFS.*

#### 📖┆[Advice to my younger self and you after 20 years in programming](https://medium.com/@alexey.inkin/advice-to-my-younger-self-and-you-after-20-years-in-programming-a3a2ccc7a942)

✍ [Alexey Inkin](https://medium.com/@alexey.inkin?source=post_page-----a3a2ccc7a942--------------------------------)

> *In the first part, I will briefly describe my career for the context. In the second part, I will go through each separate piece of advice that I think would have the strongest impact.*

#### 📖┆[Lazy is the new fast: How Lazy Imports and Cinder accelerate machine learning at Meta](https://engineering.fb.com/2024/01/18/developer-tools/lazy-imports-cinder-machine-learning-meta/)

✍ [Germán Méndez Bravo](https://engineering.fb.com/author/german-mendez-bravo/)

> *At Meta, we've been able to significantly improve our model training times, as well as our overall developer experience (DevX) by adopting Lazy Imports and the Python Cinder runtime.*

#### 📖┆[Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html)

✍ [Martin Fowler](https://martinfowler.com/)

> *I rewrote this article again in 2023 to better address the development teams of that time, with twenty years of experience to confirm the value of Continuous Integration.*

#### 📖┆[Scalable OLTP in the Cloud: What’s the BIG DEAL?](https://muratbuffalo.blogspot.com/2024/01/scalable-oltp-in-cloud-whats-big-deal.html)

✍ [Murat Demirbas](https://twitter.com/muratdemirbas)

> *The motivating question behind this work is: 'What are the asymptotic limits to scale for cloud OLTP (OnLine Transaction Processing) systems?'*

#### 📖┆[The Scary Thing About Automating Deploys](https://slack.engineering/the-scary-thing-about-automating-deploys/)

✍ [Sean McIlroy](https://www.linkedin.com/in/sean-mcilroy-8a8624b6/)

> *But what does continuous deployment mean when you’re looking at 150 changes on a normal day?*

---

# ✏ Data

> *The one thing that this job has taught me is that truth is stranger than fiction. — Predestination (2014)*

#### 📖┆[My Definition of Data Modeling (for today)](https://joereis.substack.com/p/my-definition-of-data-modeling-for)

✍ [Joe Reis](https://substack.com/profile/3531217-joe-reis)

> *What is a data model? I like to ask this question during my conference talks, and answers are all over the place. I’ve never seen a group of people consistently give a single definition. Before I give my working definition, let’s look at a few ways data modeling is defined by some notable experts.*

#### 📖┆[Measuring data quality: bringing theory into practice](https://medium.com/@mikldd/measuring-data-quality-bringing-theory-into-practice-41742e54d62f)

✍ [Mikkel Dengsøe](https://medium.com/@mikldd?source=post_page-----41742e54d62f--------------------------------)

> *If you're like most people, you don't want to measure data quality for the fun of it. Instead, you have a clear business need, e.g.,*

#### 📖┆[Introduction to Data Modeling - 2024 Guide With Problems](https://medium.com/@brilliantprogrammer/introduction-to-data-modeling-2024-guide-with-problems-8f89edfa3b8b)

✍ [Deepanshu tyagi](https://brilliantprogrammer.medium.com/)

> *Data modeling is the process of creating the conceptual representation of data and its relationship within an organisation.*

#### 📖┆[Data-Driven Proptech: GoodData - Breakthrough in Room Utilization Analytics](https://medium.com/gooddata-developers/data-driven-proptech-gooddatas-breakthrough-in-room-utilization-analytics-6426bf174d46)

✍ [Jan Panský](https://medium.com/@xpanj19)

> *This article delves into a specific Proptech use case, painting a vivid picture of gathering data through strategically placed sensors, processing it meticulously in a robust data pipeline, and ultimately leveraging GoodData’s advanced tools to craft insightful visualizations that redefine how we perceive and optimize workspace environments.*

#### 📖┆[Every data transform is technical debt](https://andrew-jones.medium.com/every-data-transform-is-technical-debt-a6d09d3961e5)

✍ [Andrew Jones](https://andrew-jones.medium.com/?source=post_page-----a6d09d3961e5--------------------------------)

> *The only solution is to reduce the amount of data transformations we do.*

#### 📖┆[Using Data to Find Growth Levers](https://sqlpatterns.com/p/using-data-to-find-growth-levers)

✍ [Ergest Xheblati](https://substack.com/@ergestx)

> *I recently read an article where the DuoLingo team reignited user growth to the tune of 350% so I decided to turn it into a case study of how to use data to find growth levers in your business.*

---

# 🤖 AI┆ML┆Data Science

> *You know, Burke, I don’t know which species is worse. — Ripley, Aliens (1986)*

#### 📖┆[Palette Meta Store Journey](https://www.uber.com/en-SG/blog/palette-meta-store-journey/)

✍ [Uber Engineering Blog](https://www.uber.com/en-SG/blog/engineering/ai/?uclick_id=15b6739c-0acd-406e-bdf6-884992beefa0)

> *The Uber Michelangelo feature store, called Palette, is a database of Uber-specific curated and internally crowd-sourced features that are easy to use in machine learning projects.*

#### 📖┆[New tool, dataset help detect hallucinations in large language models](https://www.amazon.science/blog/new-tool-dataset-help-detect-hallucinations-in-large-language-models)

✍ [Xiangkun Hu](https://www.amazon.science/author/xiangkun-hu), [Dongyu Ru](https://www.amazon.science/author/dongyu-ru)

> *Representing facts using knowledge triplets rather than natural language enables finer-grained judgments.*

#### 📖┆[A developer’s second brain: Reducing complexity through partnership with AI](https://github.blog/2024-01-17-a-developers-second-brain-reducing-complexity-through-partnership-with-ai/)

✍ [Eirini Kalliamvakou](https://github.blog/author/ikaliam/)

> *As we look to empower developers with AI tools, we inadvertently integrate AI deeper into the way developers work. How do developers feel about that? And what are the most impactful ways to introduce more AI into workflows? We recently conducted 25 in-depth interviews with developers to understand exactly that.*

#### 📖┆[Solving the weekly menu puzzle: recommendations at Picnic](https://blog.picnic.nl/solving-the-weekly-menu-puzzle-recommendations-at-picnic-42da16b281ad)

✍ [Giorgia Tandoi](https://giosh-tandoi.medium.com/?source=post_page-----42da16b281ad--------------------------------)

> *With that goal in mind, we have recently introduced a brand new recommender algorithm, and in this blog post, we’ll take you behind the scenes: revealing how we do it, what factors we consider, our plans for future enhancements and, most importantly, which lessons we learned.*

#### 📖┆[An “AI Breakthrough” on Systematic Generalization in Language?](https://aiguide.substack.com/p/an-ai-breakthrough-on-systematic)

✍ [Melanie Mitchell](https://substack.com/profile/15187849-melanie-mitchell)

> *...this is a very interesting proof-of-principle paper on systematic generalization in neural networks.*

---

# 🔥 Catch up

> *…Next Saturday night, we're sending you back to the future! — Dr. Emmett Brown, Back to the Future (1985)*

#### 📖┆[BigQuery | Cross-cloud joins to run queries that span both Google Cloud and BigQuery Omni regions.](https://cloud.google.com/bigquery/docs/biglake-intro#cross-cloud_joins)

> *You can use [GoogleSQL](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#join_types)* `JOIN` *operations to analyze data across many different storage solutions, such as AWS, Azure, public datasets, and other Google Cloud services. Cross-cloud joins eliminate the need to copy data across sources before running queries.*

---

# 💠 Previously on Dimension

> *Dimension is my sub-newsletter where I note down things I learn from people smarter than me in the data engineering field.*

Currently, I’m focus on learning OLAP databases, here are 3 the latest articles (about BigQuery):

### ***Published on 2024, January 06:***

### ***Published on 2024, January 13:***

### ***Published on 2024, January 20:***

Let me here your voice, for example:

'Your newsletter is so terrible, I can't handle it anymore.'

[Leave a comment](https://vutr.substack.com/p/groupby-19-how-apple-built-icloud/comments)

---

## “Hasta la vista, baby”

## -T800, Terminator 2: Judgment Day (1991)

Thanks for scrolling this far! There's a convenient subscribe box here if you want me to annoy you every week. 😄
