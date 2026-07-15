---
title: "GroupBy #12: AWS re:Invent 2023, Druid and ClickHouse at Lyft, Apache Hudi History"
channel: vutr
author: "Vu Trinh"
published: 2023-12-05
url: https://vutr.substack.com/p/groupby-12-aws-reinvent-2023-druid
paid: false
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Kafka", "BigQuery", "Data Quality", "ETL"]
tags: [https, amazon, medium, quality, blogs, blog]
---

# GroupBy #12: AWS re:Invent 2023, Druid and ClickHouse at Lyft, Apache Hudi History

*Plus: 7 Free Apache Kafka Tutorials and Courses, An end-to-end Data Engineer Project*

> Source: [Open post](https://vutr.substack.com/p/groupby-12-aws-reinvent-2023-druid)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[bigquery|BigQuery]] · [[data-quality|Data Quality]] · [[etl|ETL]]

---

*This is **GroupBy**, the place where I share with you guys the resources I learn from people smarter than me in data engineer field.*

*Not subscribed yet? Here you go:*

[Subscribe now](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!IU6W!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F61c92954-0572-4718-b059-c7db9ecbf883_1300x900.png)](https://substackcdn.com/image/fetch/$s_!IU6W!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F61c92954-0572-4718-b059-c7db9ecbf883_1300x900.png)

big fan of [Back to the Future](https://www.imdb.com/title/tt0088763/)

---

> *👋 Hi, my name is Vu Trinh, a data engineer.*
>
> *I enjoy reading **good stuff** (related to data and engineering), and this newsletter is my effort on the journey to seek the "good stuff" across the entire Internet.*
>
> *I have been delivering this newsletter for more than 10 consecutive weeks.*
>
> *The last time I did something for 10 consecutive weeks was watching [Game of Thrones](https://www.imdb.com/title/tt0944947/), to finally realized I had just wasted 0.2% of my life.*

---

# 🎯 Side Project

> *40+ hours of debugging and you still want some more?*

## 📺┆[Data Engineer Project: An end-to-end Airflow data pipeline with BigQuery, dbt Soda, and more!](https://www.youtube.com/watch?v=DzxtCxi4YaA)

🎙️ [Marc Lamberti](https://www.linkedin.com/in/marclamberti/)

Step by step can be found ***[Here](https://robust-dinosaur-2ef.notion.site/PUBLIC-Retail-Project-af398809b643495e851042fa293ffe5b)***.

---

# 🐙 Learning resource

> *I love to learn, and I assume you do too.*

## 🎓┆[Top 7 Free Apache Kafka Tutorials and Courses for Beginners in 2023](https://www.confluent.io/blog/best-kafka-tutorials-examples-and-learning-resources/)

✍ [Peter Moskovits](https://www.confluent.io/blog/author/peter-moskovits/)

> *…Luckily, I work at Confluent, where we’ve built a huge library of educational content authored by some of the most well-known names in Kafka. There are loads of great Kafka resources out there—for full transparency, I’ve picked the top beginner resources from our library because these were the most helpful to me.*

[![apache-kafka-partitioned-topic](https://substackcdn.com/image/fetch/$s_!X37k!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7d05ceec-bba0-47a8-9c54-d8aa7e70654c_1999x1122.png "apache-kafka-partitioned-topic")](https://substackcdn.com/image/fetch/$s_!X37k!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7d05ceec-bba0-47a8-9c54-d8aa7e70654c_1999x1122.png)

[source](https://www.confluent.io/blog/best-kafka-tutorials-examples-and-learning-resources/)

## 📖┆[10 Python Anti-Patterns You Must Avoid When Writing Clean Code](https://medium.com/python-in-plain-english/10-python-anti-patterns-you-must-avoid-when-writing-clean-code-ff3635ca1510)

✍ [Serop Baghdadlian](https://medium.com/@seropbaghdadlian)

> *Don’t Repeat My Mistakes — Here is a List of the Most Common Python Pitfalls That Lower Your Code Quality and Efficiency.*

---

# 🔥 Catch up

> *…Next Saturday night, we're sending you back to the future!*
>
> *— Dr. Emmett Brown, Back to the Future (1985)*

## 🧨 [AWS](https://aws.amazon.com/free/?gclid=CjwKCAiApaarBhB7EiwAYiMwqjIIoGRWuth47Hrr3tqXqBcJ7La-r13G2tIfDGOdxTMWTJr9Qy706RoCYa8QAvD_BwE&all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=categories%23compute&trk=8014cb37-c229-4411-8532-8c82b3e4c615&sc_channel=ps&ef_id=CjwKCAiApaarBhB7EiwAYiMwqjIIoGRWuth47Hrr3tqXqBcJ7La-r13G2tIfDGOdxTMWTJr9Qy706RoCYa8QAvD_BwE:G:s&s_kwcid=AL!4422!3!477013439213!e!!g!!aws%20cloud!11543056225!112002957029)┆**[Top announcements of AWS re:Invent 2023](https://aws.amazon.com/blogs/aws/top-announcements-of-aws-reinvent-2023/)**

> *I just mention some announcement , for the full list, you could click the link above ↑*

### 🔑 Storage

* [Announcing the new Amazon S3 Express One Zone high performance storage class](https://aws.amazon.com/blogs/aws/new-amazon-s3-express-one-zone-high-performance-storage-class/)

> *The new Amazon S3 Express One Zone storage class is designed to deliver up to 10x better performance than the S3 Standard storage class and is a great fit for your most frequently accessed data and your most demanding applications.*

> [Ananth Packkildurai](https://substack.com/@dataengineeringweekly) from [Data Engineering Weekly](https://www.dataengineeringweekly.com/) give a very [interesting article about it.](https://www.dataengineeringweekly.com/p/thoughts-on-amazon-express-one-and)

### 🔑 Analytics

* [New generative AI capabilities for Amazon DataZone further simplify data cataloging and discovery (preview)](https://aws.amazon.com/blogs/aws/new-generative-ai-capabilities-for-amazon-datazone-to-further-simplify-data-cataloging-and-discovery-preview/)
* [New Amazon Q in QuickSight uses generative AI assistance for quicker, easier data insights (preview)](https://aws.amazon.com/blogs/aws/new-amazon-q-in-quicksight-uses-generative-ai-assistance-for-quicker-easier-data-insights-preview/)
* [Use anomaly detection with AWS Glue to improve data quality (preview)](https://aws.amazon.com/blogs/aws/use-anomaly-detection-with-aws-glue-to-improve-data-quality-preview/)
* […](https://aws.amazon.com/blogs/aws/top-announcements-of-aws-reinvent-2023/)

### 🔑 Database

* [Amazon Redshift adds new AI capabilities, including Amazon Q, to boost efficiency and productivity](https://aws.amazon.com/blogs/aws/amazon-redshift-adds-new-ai-capabilities-to-boost-efficiency-and-productivity/)
* [Amazon DynamoDB zero-ETL integration with Amazon OpenSearch Service is now available](https://aws.amazon.com/blogs/aws/amazon-dynamodb-zero-etl-integration-with-amazon-opensearch-service-is-now-generally-available/)
* [Join the preview of Amazon Aurora Limitless Database](https://aws.amazon.com/blogs/aws/join-the-preview-amazon-aurora-limitless-database/)
* […](https://aws.amazon.com/blogs/aws/top-announcements-of-aws-reinvent-2023/)

## 🧨 [Airflow](https://github.com/apache/airflow)┆ **[6 New AI / LLM Airflow Providers](https://www.linkedin.com/posts/marclamberti_apacheairflow-airflow-dataengineering-activity-7135266953350262785-mtWB?utm_source=share&utm_medium=member_desktop)**

---

# 🚀 Engineering

> *I have to believe in a world outside my own mind.* — Memento *(2000)*

## 📖┆[Apache Hudi (Part 1): History, Getting Started](https://dipankar-tnt.medium.com/apache-hudi-part-1-history-getting-started-95030b003759)

✍ [Dipankar Mazumdar](https://dipankar-tnt.medium.com/?source=post_page-----95030b003759--------------------------------)

> *Hudi (pronounced “Hoodie”) emerged from Uber Engineering in 2017 as their ‘incremental processing’ framework on Hadoop.*

## 📖┆[Data Ingestion — Part 1: Architectural Patterns](https://medium.com/@meskensjan/the-art-of-data-ingestion-powering-analytics-from-operational-sources-467552d6c9a2)

✍ [janmeskens](https://medium.com/@meskensjan?source=post_page-----467552d6c9a2--------------------------------)

> *Ingestion is critical for transporting data from a multitude of sources in its original operational environment — often referred to as the ‘operational plane’ — to the sphere of analysis, or the ‘analytical plane’.*

## 📖┆[Druid Deprecation and ClickHouse Adoption at Lyft](https://eng.lyft.com/druid-deprecation-and-clickhouse-adoption-at-lyft-120af37651fd)

✍ [Ritesh Varyani](https://www.linkedin.com/in/riteshvaryani/) and [Jeana Choi](https://www.linkedin.com/in/jeana-choi/) at [Lyft](https://eng.lyft.com/?source=post_page-----120af37651fd--------------------------------).

> *In this particular blog post, we explain how Druid has been used at Lyft and what led us to adopt ClickHouse for our sub-second analytic system.*

## 📖┆[Write throughput differences in B-Tree vs LSM-Tree](https://www.reddit.com/r/databasedevelopment/comments/187cp1g/write_throughput_differences_in_btree_vs_lsmtree/?share_id=Uf4M9JdU8vybVIUcqSRui&utm_content=2&utm_medium=android_app&utm_name=androidcss&utm_source=share&utm_term=1)

🧵 Reddit Thread

> *B-tree: To perform a write on the B-tree, you need to binary search through the index and find the appropriate leaf to insert your key-value pair.*
>
> *LSM: For the LSM to perform a write, you have to write a memory structure usually called memtable.*

## 📖┆[Tech predictions for 2024 and beyond](https://www.allthingsdistributed.com/2023/11/tech-predictions-for-2024-and-beyond.html?utm_campaign=inbound&utm_source=rss)

✍ [Dr. Werner Vogels, CTO, amazon.com](https://www.allthingsdistributed.com/about.html)

> *The coming years will be filled with innovation in areas designed to democratize access to technology and help us keep up with the increasing pace of every-day life—and it starts with Generative AI.*

---

# ✏ Data

> *The one thing that this job has taught me is that truth is stranger than fiction. — Predestination (2014)*

## 📖┆[Everyone is a CDP now](https://substack.timodechau.com/p/everyone-is-a-cdp-now)

✍ [Timo Dechau](https://substack.com/profile/29441309-timo-dechau)

> *Whenever CDP is mentioned somewhere, the big talk is about the customer data you collect from the different sources, put it in a central place, create some valuable audiences, and then pass them on to any tool that might use them.*

## 📖┆[Data Quality Score: The next chapter of data quality at Airbnb](https://medium.com/airbnb-engineering/data-quality-score-the-next-chapter-of-data-quality-at-airbnb-851dccda19c3)

✍ [Clark Wright](https://medium.com/@clark.j.wright?source=post_page-----851dccda19c3--------------------------------)

> *In this blog post, we share our innovative approach to scoring data quality, Airbnb’s Data Quality Score (“DQ Score”). We’ll cover how we developed the DQ Score, how it’s being used today, and how it will power the next chapter of data quality at Airbnb.*

## 📖┆[Metadata: Definition, Examples, Benefits & Use Cases](https://atlan.com/what-is-metadata/)

✍ [Atlan Blog](https://atlan.com/what-is-metadata/)

> *…So, it can help you understand the relevance of a particular data set and guide you on how to use it. In a nutshell: Metadata is a cornerstone of a modern enterprise data stack.*

## 📖┆[Data Vault vs Bill Inmon: a comparison of data warehousing methods](https://www.data-vault.co.uk/data-vault-vs-bill-inmon-a-comparison-of-data-warehousing-methods/)

✍ Rhys Hanscombe

> *While the [Bill Inmon](https://en.wikipedia.org/wiki/Bill_Inmon) method remains a solid choice for large-scale corporate analytics solutions, Data Vault method emerges as an agile alternative that rectifies the shortcomings of traditional approaches.*

## 📖┆[Through the Looking Glass: Data Provenance in the Age of Generative AI](https://tdan.com/through-the-looking-glass-data-provenance-in-the-age-of-generative-ai/31135)

✍ [Randall Gordon](https://tdan.com/author/randall-gordon)

> *Data provenance is the documentation of where a piece of data comes from and the processes and methodology by which it was produced.*

---

# 🤖 AI┆ML┆Data Science

> *You know, Burke, I don’t know which species is worse. — Ripley, Aliens (1986)*

## 📖┆[Augmenting our content moderation efforts through machine learning and dynamic content prioritization](https://engineering.linkedin.com/blog/2023/augmenting-our-content-moderation-efforts-through-machine-learni)

✍ [Abhishek Chandak](https://engineering.linkedin.com/blog/authors/a/abhishek-chandak)

> *In this blog post, we will discuss how we use machine learning to augment our content moderation efforts at LinkedIn.*

## 📖┆[Philosophy and Data Science - Thinking Deeply About Data](https://towardsdatascience.com/philosophy-and-data-science-thinking-deeply-about-data-222cc9fbdcc5)

✍ [Jarom Hulet](https://medium.com/@jarom.hulet)

> *After reading this article, I hope that you will have a practical understanding of how thousands of years of deep thinking about knowledge applies to your daily work as a data scientist.*

## 📖┆[Semantic Layer as the Data Interface for LLMs](https://roundup.getdbt.com/p/semantic-layer-as-the-data-interface)

✍ [Jason Ganz](https://substack.com/profile/73769889-jason-ganz)

> *A new benchmark for natural language questions against databases dropped last week. What does it mean and how does the dbt Semantic Layer stack up?*

## 📖┆[How to actually regulate AI [Thoughts]](https://artificialintelligencemadesimple.substack.com/p/how-to-actually-regulate-ai-thoughts)

✍ [Devansh](https://substack.com/profile/8101724-devansh)

> *How governments, policy makers, and regulators can actually step in to make a difference*

## 📖┆[How to tackle unreliability of coding assistants](https://martinfowler.com/articles/exploring-gen-ai.html#memo-08)

✍ [Birgitta Böckeler](https://twitter.com/birgitta410)

> *One of the trade-offs to the usefulness of coding assistants is their unreliability*

---

# 🥷 It will steal 27 seconds from you

> *Random thoughts, ideas.*

The progress of making my newsletter:

The old one:

* Bookmarking cool stuff.
* Manually compiling it.

The new one:

* Bookmarking cool stuff.
* (70%) Automatically compiling it using Python.

For the first time in my life, I really thank my past self for learning how to write a computer program. 😁

Automate your life as much as possible, especially if you're a Data Engineer.

# “Hasta la vista, baby”

# -T800, Terminator 2: Judgment Day (1991)

Thanks for scrolling this far ! Convenient subscribe box here in case you want to scroll my newsletter right in your mailbox :D
