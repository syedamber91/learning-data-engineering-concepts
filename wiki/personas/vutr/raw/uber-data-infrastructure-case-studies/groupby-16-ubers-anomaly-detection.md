---
title: "GroupBy #16: Uber's Anomaly Detection & Alerting System, many layers of data lineage"
channel: vutr
author: "Vu Trinh"
published: 2024-01-02
url: https://vutr.substack.com/p/groupby-16-ubers-anomaly-detection
paid: false
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Iceberg", "Delta Lake", "Data Modeling"]
tags: [https, auto, engineering, blog, image, good]
---

# GroupBy #16: Uber's Anomaly Detection & Alerting System, many layers of data lineage

*Plus: Data modeling side project, Data Engineer roadmap 2024.*

> Source: [Open post](https://vutr.substack.com/p/groupby-16-ubers-anomaly-detection)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-iceberg|Apache Iceberg]] · [[delta-lake|Delta Lake]] · [[data-modeling|Data Modeling]]

---

*This is **GroupBy**, the place where I share with you guys the resources I learn from people smarter than me in data engineer field.*

*Not subscribed yet? Here you go:*

[Subscribe now](https://vutr.substack.com/subscribe?)

![](https://substackcdn.com/image/fetch/$s_!D8N-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fvutr.substack.com%2Fimg%2Fsubstack.png)

Get more from Vu Trinh in the Substack app

Available for iOS and Android

[Get the app](https://substack.com/app/app-store-redirect?utm_campaign=app-marketing&utm_content=author-post-insert&utm_source=vutr)

[![](https://substackcdn.com/image/fetch/$s_!er_r!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fabb3f8f2-ddc8-4679-b20b-6bc30aa96801_1300x900.png)](https://substackcdn.com/image/fetch/$s_!er_r!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fabb3f8f2-ddc8-4679-b20b-6bc30aa96801_1300x900.png)

Robot trying to be a human, human trying to be a robot.

---

> *👋 Hi, my name is Vu Trinh, a data engineer.*
>
> *I enjoy reading **good stuff** (related to data and engineering), and this newsletter is my effort on the journey to seek the "good stuff" across the entire Internet.*
>
> *Hope this issue find you well.*

---

# 🥷 It will steal 37 seconds from you

---

NEWSLETTER UPDATE.

FOR READER THAT ALREADY SUBSCRIBED:

THIS UPDATE **WILL NOT** AFFECT YOU READING EXPERIENCE AND NUMBER OF EMAIL YOU WILL RECEIVE WEEKLY.

You still receive only **ONE EMAIL EVERY WEEK:**

**The GROUPBY WEEKLY issue.**

(like the one you’re reading)

---

From beginning of 2024, I will launch a sub-newsletter with co-exist with this newsletter . This mean my newsletter will contain two sub-newsletter:

* ***GroupBy.***

  + Weekly compiled resource of data engineer (like the one you’re reading).
  + Every **Tuesday**
* ***Dimensions.***

  + My blog-style writing about what I've learned in data engineering field.
  + Every **Saturday**

> Subscriber who subscribed:
>
> * **Before 2024 January 06**, will receive emails **only** from ***GroupBy.***
> * **After 2024 January 06,** will receive emails **both** from ***GroupBy. and Dimensions.***

> Subscriber **have the control over** which newsletter they want to receive**:**
>
> * Access this link: <https://vutr.substack.com/account>
> * Toggle ON or OFF to choose which newsletter would like to receive the email:
>
>   [![](https://substackcdn.com/image/fetch/$s_!CMZ2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9be05d7d-3a5a-4505-af84-4484059115d1_1500x592.png)](https://substackcdn.com/image/fetch/$s_!CMZ2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9be05d7d-3a5a-4505-af84-4484059115d1_1500x592.png)

> FOR READER THAT ALREADY SUBSCRIBED:
>
> * You’re having option **“Dimensions“** being turned **OFF.**
>
>   → You will only receive email from **GroupBy.**

---

# 🎯 Side Project

> *40+ hours of debugging and you still want some more?*

## 📖┆[Data Modeling Project: Design For Global Superstore Sales](https://medium.com/art-of-data-engineering/my-first-data-modeling-project-design-for-global-superstore-sales-7dceda5e2575)

✍ [Nnamdi Samuel](https://medium.com/@nnamdisammie?source=post_page-----7dceda5e2575--------------------------------)

> *This project's central goal is creating a structured database design that includes a central table of facts and the required dimension tables to establish connections between different elements. This will enable meaningful comparisons and analysis.*

[![](https://substackcdn.com/image/fetch/$s_!h4bW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc7296454-6758-46ab-9b2f-02dc4e0a1a4a_888x646.jpeg)](https://substackcdn.com/image/fetch/$s_!h4bW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc7296454-6758-46ab-9b2f-02dc4e0a1a4a_888x646.jpeg)

[source](https://medium.com/art-of-data-engineering/my-first-data-modeling-project-design-for-global-superstore-sales-7dceda5e2575)

I am always looking for a data modeling project. Finally, I found one.

---

# 🐙 Learning resource

> *I love to learn, and I assume you do too.*

## 🎓┆[The Ultimate Roadmap for Data Engineers in 2024](https://medium.com/@vishalbarvaliya/roadmap-for-data-engineers-in-2024-4692ae3c9558)

✍ [Vishal Barvaliya](https://medium.com/@vishalbarvaliya?source=post_page-----4692ae3c9558--------------------------------)

> *In this blog, we'll reveal the layers of the ultimate roadmap for eager newcomers through the essential skills that define the data engineering.*

I agree with most steps in this roadmap; just want to add data modeling and dbt into it.

---

# 🚀 Engineering

> *I have to believe in a world outside my own mind. — Memento (2000)*

## 📖┆[Understanding Parquet, Iceberg and Data Lakehouses at Broad](https://davidgomes.com/understanding-parquet-iceberg-and-data-lakehouses-at-broad/)

✍ [David Gomes](https://davidgomes.com/about-me/)

> *I've heard a lot about Avro, Parquet, ORC, Arrow and Feather, but I also keep hearing about Iceberg and Delta Lake. As a "database person", I’ve been struggling to understand all of these different things, and how they relate to Data Lakes and Data Lakehouses (and what exactly are these?). So, I’ve decided to study them, and consolidate my knowledge in writing.*

## 📖┆[Deployment of Exabyte-Backed Big Data Components](https://engineering.linkedin.com/blog/2023/deployment-of-exabyte-backed-big-data-components)

✍ [Anuj Maurice](https://engineering.linkedin.com/blog/authors/a/anuj-maurice)

> *In this post, we'll explain how we built our RU (rolling update) framework to power a frictionless deployment experience on a large-scale Hadoop cluster, achieving a >99% success rate free from interruptions or downtime and reducing significant toil for our SRE and Dev teams.*

## 📖┆[uVitals - An Anomaly Detection & Alerting System](https://www.uber.com/en-SG/blog/uvitals-an-anomaly-detection-alerting-system/)

✍ [Uber Engineering Blog](https://www.uber.com/en-SG/blog/engineering/data/)

> *But what about the long tail of issues that lurk in the shadows, sometimes remaining undetected until they cause chaos? For these, traditional strategies may not suffice.*
>
> *This is where uVitals steps onto the stage, ready to seize the opportunity to detect sooner and detect more.*

[![Image](https://substackcdn.com/image/fetch/$s_!N-2N!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde955474-4dba-487a-ad3e-489097d2ac62_1024x605.jpeg "Image")](https://substackcdn.com/image/fetch/$s_!N-2N!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde955474-4dba-487a-ad3e-489097d2ac62_1024x605.jpeg)

Failure frequency vs Time to Detect. [Source](https://www.uber.com/en-SG/blog/uvitals-an-anomaly-detection-alerting-system/)

## 📖┆[Apache Airflow at Adyen: Our journey and challenges to achieve reliability at scale](https://medium.com/apache-airflow/apache-airflow-at-adyen-our-journey-and-challenges-to-achieve-reliability-at-scale-c5535a7061bf)

✍ [Natasha S](https://medium.com/@natashamayashroff?source=post_page-----c5535a7061bf--------------------------------)

> *In this blogpost, we shared a few challenges that we encountered while aiming to achieve reliability at scale at Adyen with Airflow.*

## 📖┆[3 years managing Kubernetes clusters, my 10 lessons.](https://hervekhg.medium.com/3-years-managing-kubernetes-clusters-my-10-lessons-b565a5509f0e)

✍ [Herve Khg](https://hervekhg.medium.com/?source=post_page-----b565a5509f0e--------------------------------)

> *In this article, I wish to share with you the ten most valuable lessons I've learned as a Kubernetes cluster manager.*

---

# ✏ Data

> *The one thing that this job has taught me is that truth is stranger than fiction. — Predestination (2014)*

## 📖┆[Super Tables: The road to building reliable and discoverable data products](https://engineering.linkedin.com/blog/2022/super-tables--the-road-to-building-reliable-and-discoverable-dat?)

✍ [Cliff Leung](https://engineering.linkedin.com/blog/authors/c/cliff-leung)

> *Super Tables (ST) are pre-computed, denormalized, and consistently consolidated attributes and insights of entities or events that are optimized for common and efficient analytic use cases.*

## 📖┆[How to plan to data roadmap for 2024 - elevating your data strategy](https://www.theseattledataguy.com/how-to-plan-to-data-roadmap-for-2024-elevating-your-data-strategy/)

✍ [Benjamin Rogojan](https://www.linkedin.com/in/benjaminrogojan/)

> *...I wanted to provide some tips to help those either in leadership positions or who want to break into these positions plan out their data roadmap for 2024.*

[![data team consulting](https://substackcdn.com/image/fetch/$s_!afsF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e9ee8d0-424a-48ff-83e7-bd7f317114e2_1024x384.jpeg "data team consulting")](https://substackcdn.com/image/fetch/$s_!afsF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e9ee8d0-424a-48ff-83e7-bd7f317114e2_1024x384.jpeg)

[source](https://www.theseattledataguy.com/how-to-plan-to-data-roadmap-for-2024-elevating-your-data-strategy/#page-content)

## 📖┆[The many layers of data lineage](https://medium.com/data-monzo/the-many-layers-of-data-lineage-2eb898709ad3)

✍ [Borja Vazquez](https://medium.com/@borjavazquez?source=post_page-----2eb898709ad3--------------------------------)

> *In this post we’ll discuss how we can learn from the field of cartography and Google Maps to extract the untapped potential of data lineage, and build this ideal interface to improve data literacy and observability.*

## 📖┆[Discovery and Consumption of Analytics Data at Twitter](https://blog.twitter.com/engineering/en_us/topics/insights/2016/discovery-and-consumption-of-analytics-data-at-twitter)

✍ [Sriram Krishnan](https://www.twitter.com/krishnansriram)

> *In this blog, we will discuss the higher-level design and usage of of Data Access Level, how it fits in within the overall data platform ecosystem, and share some observations and lessons learned.*

[![](https://substackcdn.com/image/fetch/$s_!2Jde!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04fe81ec-14e0-4639-8205-467b56c86daf_1003x621.png)](https://substackcdn.com/image/fetch/$s_!2Jde!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04fe81ec-14e0-4639-8205-467b56c86daf_1003x621.png)

[source](https://blog.twitter.com/engineering/en_us/topics/insights/2016/discovery-and-consumption-of-analytics-data-at-twitter)

---

# 🤖 AI┆ML┆Data Science

> *You know, Burke, I don’t know which species is worse. — Ripley, Aliens (1986)*

## 📺┆[[1hr Talk] Intro to Large Language Models](https://www.youtube.com/watch?v=zjkBMFhNj_g)

🎙️ [Andrej Karpathy](https://karpathy.ai/)

> *And so now, we return to the original question that took us down this long and winding path - should we even care about connecting enterprise data to natural language queries by LLMs?*

## 📖┆[How To Train Your Own GenAI Model](https://developer.squareup.com/blog/how-to-train-your-own-genai-model/)

✍ [Alessandro Joabar](https://www.linkedin.com/in/alessandro-joabar/)

> *If I was to summarize the goal of this article, it's that we're going to learn to light a campfire with a lighter (GPT2) and not a flamethrower (GPT3.5).*

## 📖┆[Running demand forecasting machine learning models at scale](https://blog.picnic.nl/running-demand-forecasting-machine-learning-models-at-scale-bd058c9d4aa7)

✍ [Maarten Sukel](https://medium.com/@maartensukel)

> *This blog post delves into the learnings and challenges on our journey towards implementing and scaling state-of-the-art deep learning approaches. We’ll shed light on how to use the newest machine-learning approaches in a controlled and reliable manner.*

## 📖┆[Airbnb at KDD 2023](https://medium.com/airbnb-engineering/airbnb-at-kdd-2023-9084ad244d8c)

✍ [Alex Deng](https://medium.com/@adeng?source=post_page-----9084ad244d8c--------------------------------)

> *Airbnb had a significant presence at KDD 2023 with two papers accepted into the main conference proceedings and 11 talks and presentations. In this blog post, we’ll summarize our team’s contributions and share highlights from an exciting week of research talks, workshops, panel discussions, and more.*

## 📖┆[Monte Carlo, Puppetry and Laughter: The Unexpected Joys of Prompt Engineering](https://tech.instacart.com/monte-carlo-puppetry-and-laughter-the-unexpected-joys-of-prompt-engineering-4b9272e0c4eb)

✍ [Ben Bernard](https://benbernard.medium.com/)

> *This article will be an exploration of prompt techniques we’ve used for our internal productivity tooling at Instacart.*

Let me here your voice, for example:

'Your newsletter is so terrible, I can't handle it anymore.'

[Leave a comment](https://vutr.substack.com/p/groupby-16-ubers-anomaly-detection/comments)

---

# “Hasta la vista, baby”

# -T800, Terminator 2: Judgment Day (1991)

Thanks for scrolling this far! There's a convenient subscribe box here if you want me to annoy you every week. 😄
