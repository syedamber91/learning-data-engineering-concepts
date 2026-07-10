---
title: "GroupBy #5: The story of S3, Kafka at scale and the boring is back"
channel: vutr
author: "Vu Trinh"
published: 2023-10-17
url: https://vutr.substack.com/p/groupby-5-the-story-of-s3-kafka-at
paid: false
topics: ["Data Engineering", "Apache Kafka", "Apache Spark", "Apache Flink", "Databricks", "BigQuery", "Data Quality"]
tags: [https, engineering, auto, good, substackcdn, image]
---

# GroupBy #5: The story of S3, Kafka at scale and the boring is back

*With bunch of movie quotes.*

> Source: [Open post](https://vutr.substack.com/p/groupby-5-the-story-of-s3-kafka-at)

## Topics

[[data-engineering|Data Engineering]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-flink|Apache Flink]] · [[databricks|Databricks]] · [[bigquery|BigQuery]] · [[data-quality|Data Quality]]

---

*This is **vutrinh’s GroupBy**, a weekly send of cool resource on data engineering. Not subscribed yet? Here you go:*

[Subscribe now](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!d5-q!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F454858d9-527a-4e98-bca7-d07e38948717_1490x368.png)](https://substackcdn.com/image/fetch/$s_!d5-q!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F454858d9-527a-4e98-bca7-d07e38948717_1490x368.png)

[![](https://substackcdn.com/image/fetch/$s_!n4qc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F889f1537-ad79-4de0-9431-688fd7e01ea0_1300x900.png)](https://substackcdn.com/image/fetch/$s_!n4qc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F889f1537-ad79-4de0-9431-688fd7e01ea0_1300x900.png)

---

> *👋 Hi, my name is Vu Trinh, a data engineer currently working at a mobile game company. I enjoy reading **good stuff** (related to data and engineering), and this newsletter is my effort on the journey to seek the "good stuff" across the entire Internet.*
>
> *Hope this issue finds you well.*

---

[![](https://substackcdn.com/image/fetch/$s_!9ce3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa698e46b-f8a4-4c64-ba55-a02c2712cca6_1490x368.png)](https://substackcdn.com/image/fetch/$s_!9ce3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa698e46b-f8a4-4c64-ba55-a02c2712cca6_1490x368.png)

…and you need to *consume this:*

### *⚙ Engineering*

*we can validate it somehow*

> *Engineering is the practice of using natural science, mathematics, and the engineering design process to solve technical problems, increase efficiency and productivity, and improve systems.* — *wikipedia —*

* [Building and operating a pretty big storage system called S3](https://www.allthingsdistributed.com/2023/07/building-and-operating-a-pretty-big-storage-system.html) [📖]

  + ⭐⭐ This is my most favorite on of the week, in the world where short content is everywhere, this article is a gem.⭐⭐
* [GitHub Pull Request Templates: Streamlining Code Reviews with Style and Efficiency](https://luminousmen.com/post/github-pull-request-templates) [📖]
* [How Pinterest runs Kafka at scale](https://medium.com/pinterest-engineering/how-pinterest-runs-kafka-at-scale-ff9c6f735be) [📖]

  + This is from 2018, but dealing with partition reassignment and failed brokers (with Kafka) is never outdated.
* [Data engineering at Meta: High-Level Overview of the internal tech stack](https://medium.com/@AnalyticsAtMeta/data-engineering-at-meta-high-level-overview-of-the-internal-tech-stack-a200460a44fe) [📖]
* [How we made our reporting engine 17x faster](https://medium.com/teads-engineering/how-we-made-our-reporting-engine-17x-faster-652b9e316ca4) [📖]

  + Excellent example of the “*focusing on simplicity and removing complexity“* .
* [Brief History of Data Engineering](https://www.jesse-anderson.com/2022/12/brief-history-of-data-engineering/) [📖]

---

### *✏ Data*

*the paradox, the strange, the reality*

> *The one thing that this job has taught me is that truth is stranger than fiction.*
>
> *— Predestination (2014) —*

* [Improving Meta’s SLO workflows with data annotations](https://engineering.fb.com/2022/08/29/developer-tools/improving-metas-slo-workflows-with-data-annotations/) [📖]
* [Metis: Building Airbnb’s Next Generation Data Management Platform](https://medium.com/airbnb-engineering/metis-building-airbnbs-next-generation-data-management-platform-d2c5219edf19) [📖]
* [From Big Data to Better Data: Ensuring Data Quality with Verity](https://eng.lyft.com/from-big-data-to-better-data-ensuring-data-quality-with-verity-a996b49343f6) [📖]
* [Boring is Back - The Longer Rant](https://joereis.substack.com/p/boring-is-back-the-longer-rant) [📖]
* [The data delivery checklist: principles to design data products](https://uxdesign.cc/the-data-delivery-checklist-principles-to-design-data-products-b644e2333467) [📖]
* [Data is not a Microservice](https://dataproducts.substack.com/p/data-is-not-a-microservice) [📖]
* [Building Better Data Warehouses with Dimensional Modeling: A Guide for Data Engineers](https://towardsdatascience.com/building-better-data-warehouses-with-dimensional-modeling-a-guide-for-data-engineers-422b3cd52df4) [📖]

---

### *🧠 AI*

*more and more confused*

> *You know, Burke, I don’t know which species is worse.*
>
> *— Ripley, Aliens (1986) —*

* [GPT and LLMs from a Data Engineering Perspective](https://www.jesse-anderson.com/2023/09/gpt-and-llms-from-a-data-engineering-perspective/) [📖]
* [Prompting GitHub Copilot Chat to become your personal AI assistant for accessibility](https://github.blog/2023-10-09-prompting-github-copilot-chat-to-become-your-personal-ai-assistant-for-accessibility/) [📖]
* [Andrew Ng: Opportunities in AI - 2023](https://www.youtube.com/watch?v=5p248yoa3oE) [📺]
* [Gartner’s AI Hype Cycle is Way Passed its Due Date — And Are We Entering a Classical ML Winter?](https://olivermolander.medium.com/gartners-ai-hype-cycle-way-passed-its-due-date-and-are-we-entering-a-classical-ml-winter-7c09041c72c4) [📖]
* [Build AI/ML and generative AI applications in Python with BigQuery DataFrames](https://cloud.google.com/blog/products/data-analytics/building-aiml-apps-in-python-with-bigquery-dataframes) [📖]
* [Cool and free resource from Google](https://www.cloudskillsboost.google/journeys/118) if you want to get start with Generative AI

---

### *💣 Catch up with the world*

> *…Next Saturday night, we're sending you back to the future!*
>
> *— Dr. Emmett Brown, Back to the Future (1985) —*

* [Apache Kafka 3.6.0 release](https://kafka.apache.org/blog#apache_kafka_360_release_announcement) [📖] with following features:

  + Tiered Storage.
  + Cluster migration from [Zookeeper](https://zookeeper.apache.org/) to [KRaft](https://developer.confluent.io/learn/kraft/) with no downtime
* [Announcing BigQuery Omni cross-cloud joins](https://cloud.google.com/blog/products/data-analytics/announcing-bigquery-omni-cross-cloud-joins/) [📖]
* [Introducing Apache Spark™ 3.5](https://www.databricks.com/blog/introducing-apache-sparktm-35) [📖]
* [Managed Apache Flink on Azure](https://techcommunity.microsoft.com/t5/analytics-on-azure-blog/introducing-apache-flink-on-azure-hdinsight-on-aks/ba-p/3936611) [📖]

---

> *Hasta la vista, baby.*
>
> *— T800, Terminator 2 (Judgment Day, 1991) —*

I apologize, but I can't resist quoting from movies.

[![](https://substackcdn.com/image/fetch/$s_!d5-q!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F454858d9-527a-4e98-bca7-d07e38948717_1490x368.png)](https://substackcdn.com/image/fetch/$s_!d5-q!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F454858d9-527a-4e98-bca7-d07e38948717_1490x368.png)

---

Thanks for reading this far! Subscribe for free to receive a weekly curated list of cooling resource on data engineering.
