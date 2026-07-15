---
title: "GroupBy #17: Pinterest’s new wide column database using RocksDB, Fault tolerance Kafka on Kubernetes at Grab"
channel: vutr
author: "Vu Trinh"
published: 2024-01-09
url: https://vutr.substack.com/p/groupby-17-pinterests-new-wide-column
paid: false
topics: ["Data Engineering", "Apache Airflow", "Apache Kafka", "BigQuery", "Data Modeling", "Streaming"]
tags: [https, kubernetes, auto, time, medium, airflow]
---

# GroupBy #17: Pinterest’s new wide column database using RocksDB, Fault tolerance Kafka on Kubernetes at Grab

*Plus: Deploying Apache Airflow on a K8s, Data Modeling in the Modern Data Stack*

> Source: [Open post](https://vutr.substack.com/p/groupby-17-pinterests-new-wide-column)

## Topics

[[data-engineering|Data Engineering]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[bigquery|BigQuery]] · [[data-modeling|Data Modeling]] · [[streaming|Streaming]]

---

*This is **GroupBy**, the place where I share with you guys the resources I learn from people smarter than me in data engineer field.*

*Not subscribed yet? Here you go:*

[Subscribe now](https://vutr.substack.com/subscribe?)

![](https://substackcdn.com/image/fetch/$s_!D8N-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fvutr.substack.com%2Fimg%2Fsubstack.png)

Get more from Vu Trinh in the Substack app

Available for iOS and Android

[Get the app](https://substack.com/app/app-store-redirect?utm_campaign=app-marketing&utm_content=author-post-insert&utm_source=vutr)

[![](https://substackcdn.com/image/fetch/$s_!JdnZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04096358-e795-4f6e-b189-b95e802d531e_1300x900.png)](https://substackcdn.com/image/fetch/$s_!JdnZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04096358-e795-4f6e-b189-b95e802d531e_1300x900.png)

> *👋 Hi, my name is Vu Trinh, a data engineer.*
>
> *I enjoy reading **good stuff** (related to data and engineering), and this newsletter is my effort on the journey to seek the "good stuff" across the entire Internet.*
>
> *Hope this issue find you well.*

---

# 🥷 It will take you 1 minutes and 47 seconds

> *You can skip this*.

> But I hope you could stay for a little while…

> …to read my thoughts

I rarely place this section at the beginning because I worry that I will waste your time.

But this time, allow me to steal some time from you.

—

2023 is an important year for me, although I didn't achieve anything significant last year.

However, 2023 marks a milestone where I finally have a gut to start something new.

In September 2023 (sorry, I don’t remember the exact day), I began this newsletter with a simple goal: to help you find valuable data engineering resources to consume.

There are a total of 16 GroupBy issues, and we've gained 173 subscribers.

I never imagined that I would write a weekly email for 10 people, but now, over 150 people choose to receive my email every week.

This means a lot to me. Your support keeps me moving forward despite hard days.

In 2024, alongside the weekly GroupBy issues, I will launch a brand new kind of content with the ultimate goal is sharing my knowledge with the community (something I've wanted to do for a long time).

My newsletter will also undergo some changes in the way it organizes content:

It will be renamed to the **VuTrinh**. newsletter and contains two sub-newsletters:

1. **GroupBy. - Every Tuesday:** Weekly curated data engineering resources (similar to the one you're reading).
2. **Dimension. - Every Saturday:** Blog-style writing about everything I've learned.

Let me clarify a little bit:

* **All subscribers before January 5th, 2024**, will only receive emails from GroupBy.

  + → I truly care about your experience, so I've decided not to send additional emails that you're not expecting. I'll let you decide whether you want to receive additional emails or not.
* **All subscribers after January 5th, 2024**, will receive emails from both GroupBy. and Dimension.

You can control which emails from which sub-newsletter to receive by clicking this button, and toggling ON/OFF the option will allow you to adjust:

[Sub-newsletter options](https://vutr.substack.com/account)

By the way, If you want to take a look, here are my latest article from Dimension.

—

That’s all I want to say.

Once again, I truly appreciate your support all the time.

Hope to receive your embrace for my new kind of content.

Now it time to say goodbye.

See you in my future emails.

— Vu Trinh —

---

# 🎯 Side Project

> *40+ hours of debugging and you still want some more?*

## 📖┆[Deploying Apache Airflow on a Kubernetes Cluster](https://www.clearpeaks.com/deploying-apache-airflow-on-a-kubernetes-cluster/)

[![Deploying Apache Airflow on a Kubernetes Cluster](https://substackcdn.com/image/fetch/$s_!uLUr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F486998e1-4734-457d-b72a-42fd2d88b5e9_2501x1251.png "Deploying Apache Airflow on a Kubernetes Cluster")](https://substackcdn.com/image/fetch/$s_!uLUr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F486998e1-4734-457d-b72a-42fd2d88b5e9_2501x1251.png)

[source](https://www.clearpeaks.com/deploying-apache-airflow-on-a-kubernetes-cluster/)

✍ [Tomislav Novosel](https://www.linkedin.com/in/tonovosel/)

> *In this blog series, we will dive deep into Airflow: first, we will show you how to create the essential Kubernetes resources to be able to deploy Apache Airflow on two nodes of the Kubernetes cluster.*

This project is different from previous ones I shared: you only play around with Airflow and Kubernetes this time.

After getting your Airflow up on Kubernetes, you will learn almost necessary knowledge for effectively working with Airflow and Kubernetes in the future.

Trust me.😉

---

# 🐙 Learning resource

> *I love to learn, and I assume you do too.*

## 🎓┆**[100 Days of Code with Apache Kafka®](https://developer.confluent.io/100-days-of-code/)**

✍ [Confluent Developer](https://developer.confluent.io/)

> *100 Days Of Code is a challenge that helps developers build strong coding habits with a self-directed learning path. This page is tailored to developers interested in event streaming who want to use the 100 Days Of Code model as a way to learn about Apache Kafka®.*

---

# 🚀 Engineering

> *I have to believe in a world outside my own mind. — Memento (2000)*

## 📖┆[Building Pinterest’s new wide column database using RocksDB](https://medium.com/pinterest-engineering/building-pinterests-new-wide-column-database-using-rocksdb-f5277ee4e3d2)

✍ [Pinterest Engineering](https://medium.com/@Pinterest_Engineering?source=post_page-----f5277ee4e3d2--------------------------------)

[![](https://substackcdn.com/image/fetch/$s_!8sKv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F30804f58-f199-44fb-9c6b-5e1605e21d87_570x378.png)](https://substackcdn.com/image/fetch/$s_!8sKv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F30804f58-f199-44fb-9c6b-5e1605e21d87_570x378.png)

Logical view of a wide column database with versioned values. [Source](https://medium.com/pinterest-engineering/building-pinterests-new-wide-column-database-using-rocksdb-f5277ee4e3d2)

> *While KVStore was the client facing abstraction, we also built a storage service called Rockstorewidecolumn: a wide column, schemaless NoSQL database built using RocksDB. This blog post goes into the details of how we built this massively scalable, highly available wide column database using RocksDB...*

## 📖┆[MySQL Speed Hacks: Indexes and EXPLAIN Statement](https://medium.com/insiderengineering/mysql-speed-hacks-indexes-and-explain-statement-eddc856b24a2)

✍ [Ertugrul AKCA](https://medium.com/@akcauser?source=post_page-----eddc856b24a2--------------------------------)

> *In this blog, I will explain why indexes are crucial for databases. Additionally, I will provide some examples and outline best practices for querying tables in a manner that is both faster and cost-effective.*

## 📖┆[Designing Low Latency Segmentation Platform Using Upstash Kafka and Source MongoDB Connector](https://levelup.gitconnected.com/designing-low-latency-segmentation-platform-using-upstash-kafka-and-source-mongodb-connector-223b19591c2b)

✍ [Mahesh Saini](https://medium.com/@maheshsaini.sec)

> *In this blog post, we've explored the design principles of a low-latency segmentation platform leveraging cutting-edge technologies provided by Upstash.*

## 📖┆[Design a Real-Time Leaderboard system for millions of users](https://medium.com/@mayilb77/design-a-real-time-leaderboard-system-for-millions-of-users-08b96b4b64ce)

✍ [Mayil Bayramov](https://medium.com/@mayilb77?source=post_page-----08b96b4b64ce--------------------------------)

> *Let's assume we have an online gaming platform, where a user plays games and earns points. Our marketing team announced a new campaign for a certain period. At the end of the period, we will have special gifts for the top 10 players based on their rank in Leaderboard.*

## 📖┆[Kafka on Kubernetes: Reloaded for fault tolerance](https://engineering.grab.com/kafka-on-kubernetes)

✍ [Fabrice Harbulot · Thang Le](https://engineering.grab.com/)

> *Coban - Grab's real-time data streaming platform - has been operating Kafka on Kubernetes with Strimzi in production for about two years.In this article, we are going to describe how we improved the fault tolerance of our initial design, to the point where we no longer need to intervene if a Kafka broker is unexpectedly terminated.*

---

# ✏ Data

> *The one thing that this job has taught me is that truth is stranger than fiction. — Predestination (2014)*

## 📖┆[Normalization Vs Denormalization - Taking A Step Back](https://medium.com/coriers/normalization-vs-denormalization-taking-a-step-back-c1362bcb2fc5)

✍ [Ben Rogojan](https://medium.com/@SeattleDataGuy?source=post_page-----c1362bcb2fc5--------------------------------)

> *If you touch a database, whether it's for analytics or it's a document-oriented one, there are key concepts you should be aware of.*

## 📖┆[Data Modeling in the Modern Data Stack](https://towardsdev.com/data-modeling-in-the-modern-data-stack-d29be964b3a7)

✍ [Franklyne Kibet](https://medium.com/@franklyne-kibet)

> In this article, we will explore:
>
> * Why is data modeling (still) important?
> * What are the common approaches?
> * What things should you consider?\*

## 📖┆[What You Must Know About Real-Time Data](https://www.thdpth.com/p/what-you-must-know-about-real-time)

✍ [Sven Balnojan](https://substack.com/profile/229923-sven-balnojan)

> *Let me repeat: real-time data and fast actions only collide in one world: The financial world of quantitative trading and hedges*

## 📖┆[How Analytics Can Make a Massive Impact on the Bottom Line](https://sqlpatterns.com/p/how-analytics-can-make-a-massive)

✍ [Ergest Xheblati](https://substack.com/@ergestx)

> *A case study on building an operating model using metric trees*

## 📖┆[You Don't Know Data! (The Importance of Sound Definitions)](https://tdan.com/you-dont-know-data-the-importance-of-sound-definitions/31455)

✍ [William Burkett](https://tdan.com/author/william-burkett)

> *The purpose of this essay is to apply a little of what I've learned about defining things to two terms that are very fundamental to our practice of data management and frequently appear conjoined in data management literature: “data and information.*

---

# 🤖 AI┆ML┆Data Science

> *You know, Burke, I don’t know which species is worse. — Ripley, Aliens (1986)*

## 📖┆[5 Hard Truths About Generative AI for Technology Leaders](https://towardsdatascience.com/5-hard-truths-about-generative-ai-for-technology-leaders-4b119336bc85)

✍ [Barr Moses](https://towardsdatascience.comhttps//barrmoses.medium.com/?source=post_page-----4b119336bc85--------------------------------)

> *GenAI that drives real business value takes real work. But it's worth it.*

## 📖┆[BigQuery integrates with Doc AI to help build document analytics and generative AI use cases](https://cloud.google.com/blog/products/data-analytics/add-gen-ai-to-your-apps-with-bigquery-and-document-ai-integration/)

✍ [Oliver Zhuang](https://www.linkedin.com/in/lezhuang/)

> *...we're excited to announce an integration between BigQuery and Document AI, letting you easily extract insights from document data and build new large language model (LLM) applications.*

Let me here your voice, for example:

'Your newsletter is so terrible, I can't handle it anymore.'

[Leave a comment](https://vutr.substack.com/p/groupby-17-pinterests-new-wide-column/comments)

---

# “Hasta la vista, baby”

# -T800, Terminator 2: Judgment Day (1991)

Thanks for scrolling this far! There's a convenient subscribe box here if you want me to annoy you every week. 😄
