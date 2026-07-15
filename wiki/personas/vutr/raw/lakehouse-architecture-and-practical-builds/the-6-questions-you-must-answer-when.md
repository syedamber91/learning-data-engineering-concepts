---
title: "The 6 questions you must answer when building a Lakehouse from scratch"
channel: vutr
author: "Vu Trinh"
published: 2026-01-20
url: https://vutr.substack.com/p/the-6-questions-you-must-answer-when
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Apache Iceberg", "Apache Flink", "Snowflake", "Databricks", "Delta Lake", "BigQuery", "Data Warehouse", "Lakehouse", "Streaming"]
tags: [https, auto, substackcdn, image, fetch, good]
---

# The 6 questions you must answer when building a Lakehouse from scratch

*From table format, query engines, storage layout to developer experience*

> Source: [Open post](https://vutr.substack.com/p/the-6-questions-you-must-answer-when)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[apache-flink|Apache Flink]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]] · [[lakehouse|Lakehouse]] · [[streaming|Streaming]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=184279378)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!9Y0C!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3aefcfe3-5ddf-4520-950d-fc40836a0c74_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!9Y0C!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3aefcfe3-5ddf-4520-950d-fc40836a0c74_2000x1429.png)

---

## Intro

Just imagine you are tasked to build a whole data lakehouse platform from scratch. You don’t have any experience except for some minutes watching vendors bragging about how cool their lakehouse offerings are.

So what would you do?

I was putting myself in that situation last weekend and tried my best to ask some questions that guided the process of building a lakehouse platform. I will share them in this article.

> ***Note 1**: What you’re reading is based entirely on my current knowledge and experience, and it might not cover all the aspects and the details we need to consider when building a lakehouse architecture. Feel free to correct me or add your ideas in the comment section.*
>
> ***Note 2**: You won’t see any tool-specific advice here, as I aimed to deliver the general concerns when building a lakehouse.*
>
> ***Note 3:** This article is my discussion of building a lakehouse solution from zero, with no vendor support, to show the real challenges we might face.*

---

## The lakehouse

Let's first revisit the lakehouse paradigm so we can have a mental model of what we're gonna build. In 2020, Databricks published a paper introducing the term “lakehouse” to refer to a data management system built on low-cost storage that enhances the management and performance of traditional analytical DBMS.

[![](https://substackcdn.com/image/fetch/$s_!pjFc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5e8750e6-34ce-4fb1-9f23-edde1b40d079_894x796.png)](https://substackcdn.com/image/fetch/$s_!pjFc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5e8750e6-34ce-4fb1-9f23-edde1b40d079_894x796.png)

At a high level, there are two main components: a giant storage (object storage) system that can store your data indefinitely (except for your budget), and your favorite query engines for the party.

---

## Which table format(s)?

### Why is this the most important decision?

This is the most important decision you have to make when building any data lakehouse.

Let me explain why.

You must know Snowflake and BigQuery. The two giant solutions, which were first introduced as cloud data warehouse systems, have actually been implementing the architecture that shares some properties with the lakehouse paradigm we have heard about.

[![](https://substackcdn.com/image/fetch/$s_!Hu6u!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F376750fb-d608-4d49-ad7d-981b0d009c6b_1420x742.png)](https://substackcdn.com/image/fetch/$s_!Hu6u!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F376750fb-d608-4d49-ad7d-981b0d009c6b_1420x742.png)

They both work on the principle of decoupling compute and storage. The storage is a giant storage system (S3 for Snowflake and Colossus for BigQuery), and the compute engine is a set of stateless servers. The differences are that:

* The vendors control the storage layer.
* The vendors don’t promise the ability to bring any query engine you like (they’re offering more options)

To enable this compute-storage decoupling, there must be a translation layer. The giant storage manages data as files/objects.

[![](https://substackcdn.com/image/fetch/$s_!H7TL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9617341f-dd15-486b-a851-aa3d1be91a04_544x446.png)](https://substackcdn.com/image/fetch/$s_!H7TL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9617341f-dd15-486b-a851-aa3d1be91a04_544x446.png)

However, data users need to observe the data at a higher level of abstraction, usually in tables. A metadata layer must exist to translate “this table = these files. “

Beyond the table abstraction, these layers must also handle many other functions: ACID guarantees, table versioning, time travel, efficient CRUD operations, query performance optimization, schema evolution, access control, …

[![](https://substackcdn.com/image/fetch/$s_!6dzd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F21986a59-bc92-4d0f-82dd-4c157090d8e8_922x676.png)](https://substackcdn.com/image/fetch/$s_!6dzd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F21986a59-bc92-4d0f-82dd-4c157090d8e8_922x676.png)

If you use BigQuery or Snowflake, you won’t see these layers as well as the files in the storage system, because the vendors have to manage all these things behind the scenes to ease the operation burden for us.

That’s a gift.

—

### Choosing the table format(s)

However, that gift comes with a trade-off. It’s hard to onboard users’ preferred query engines, since the metadata layers were initially designed only for BigQuery and Snowflake. There are two solutions for this:

[![](https://substackcdn.com/image/fetch/$s_!SrSx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa54afc6d-5969-4b97-90a2-c488d11392a6_610x400.png)](https://substackcdn.com/image/fetch/$s_!SrSx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa54afc6d-5969-4b97-90a2-c488d11392a6_610x400.png)

* Wait for the vendors to add support for the external engines (they might write some adapters, for example)

  [![](https://substackcdn.com/image/fetch/$s_!Xs5Z!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb4729d35-0f93-494b-9cc5-316fdcfc180f_1104x722.png)](https://substackcdn.com/image/fetch/$s_!Xs5Z!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb4729d35-0f93-494b-9cc5-316fdcfc180f_1104x722.png)
* Exporting the data to other destinations that the external engines can work with (e.g., object storage or the solution’s proprietary storage)

—

Databricks, Netflix, and Uber believe in a more open solution as they decide to commoditize the translation layers. That results in the big three table formats you might have heard of: Delta Lake, Apache Iceberg, and Apache Hudi.

[![](https://substackcdn.com/image/fetch/$s_!qv2c!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F92c01903-e145-4441-9513-514f34a34e26_1038x704.png)](https://substackcdn.com/image/fetch/$s_!qv2c!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F92c01903-e145-4441-9513-514f34a34e26_1038x704.png)

Recently, there have been several table formats joining the race with the big three; they are DuckLake (promise to be more lean), and Apache Paimon (helping with streaming workload)

All those formats also handle the functions I mentioned above, from table abstraction and ACID guarantees to query performance optimization and access control.

The great part is that you have to pick.

[![](https://substackcdn.com/image/fetch/$s_!xS37!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe6b7a9e0-2fb0-437f-9b93-91f87f627351_994x704.png)](https://substackcdn.com/image/fetch/$s_!xS37!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe6b7a9e0-2fb0-437f-9b93-91f87f627351_994x704.png)

—

I read somewhere on the internet that if you use Databricks, you should go with Delta Lake; if you prefer many integration options, you should go with Iceberg; and if you require incremental processing, you should go with Hudi.

That might be true. But I believe that’s not the whole story.

Every data solution should serve the business. Thus, the decision on the table format(s) must be made based on the business requirement:

[![](https://substackcdn.com/image/fetch/$s_!9Sbc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F95ea38c8-c9b0-4754-ba26-0776d23049a5_1136x412.png)](https://substackcdn.com/image/fetch/$s_!9Sbc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F95ea38c8-c9b0-4754-ba26-0776d23049a5_1136x412.png)

* Your business evolves quite rapidly; the data schema must evolve to reflect the reality. Can the table formats support this kind of schema evolution?
* Many teams need access to the data. Can the table formats enable fine-grained access control?
* Your company needs real-time data ingestion/serving. Can the open table format support that?
* Many users want to read a table at a time. Can the open table format support high-concurrency?
* The company needs to process 5, 10, 15 TBs a day. Can the chosen format handle that?
* many more…

If you look at any document in the big three table formats, you will see many features that help you manage your entire data life cycle. All promise to solve your problems and make you think it is your choice.

[![](https://substackcdn.com/image/fetch/$s_!yry2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb97f5738-bf67-44e3-8a9a-cdae55083e40_912x792.png)](https://substackcdn.com/image/fetch/$s_!yry2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb97f5738-bf67-44e3-8a9a-cdae55083e40_912x792.png)

However, choosing any technical solution based only on its reputation is a bad decision. We need a measurable and tangible approach.

A most straightforward way is to develop an MVP to evaluate your choices. You don’t need to fully re-implement or migrate your current data platform; only a few typical use cases are enough. The process of building the MVP helps you answer the ultimate question: Can the table format potentially solve your business requirement?

[![](https://substackcdn.com/image/fetch/$s_!1z39!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F07a8d4db-a6bd-4a3d-b544-61a83c68b3ca_1048x740.png)](https://substackcdn.com/image/fetch/$s_!1z39!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F07a8d4db-a6bd-4a3d-b544-61a83c68b3ca_1048x740.png)

The MVP could be measured by:

* A list of successful criteria. For example, renamed column capability? Processing 1TB of data in 7 minutes? Row-level access control?. The key is that the criteria must be derived from your business requirements.
* Benchmarking. The MVP must meet your expectations about time and resources, or perform at least as well as the current solution, or what you expect.

The choice doesn’t need to be a single format. In theory, you can mix it. You can “orchestrate” the use of distinct formats based on each use case (e.g., Hudi for incremental processing and Iceberg for the rest), or leverage project XTable to enable interoperability among the big three formats. In return, more than one format definitely increases the complexity.

[![](https://substackcdn.com/image/fetch/$s_!UHmV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcf2c447d-36b0-4991-892a-8a12702a1705_982x404.png)](https://substackcdn.com/image/fetch/$s_!UHmV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcf2c447d-36b0-4991-892a-8a12702a1705_982x404.png)

The key is to make sure your choice aligns with the business’s needs (an important thing must be repeated again and again). (There is a chance that after careful evaluation, you see none of the available table formats that suit your needs and go back with a cloud data warehouse vendor.)

—

Choosing the table format(s) without careful evaluation is dangerous. If your boss decides to go with Iceberg just because everyone is talking about it, run right away.

---

## Which query engines?

Then, we have to make another decision. The one about the query engines.

Although lakehouse architecture separates the query engine and storage, the decision for these two layers should be evaluated together.

The reason is quite simple: you can’t just pick and onboard the query engine you think could satisfy the business requirements; you must also check whether your chosen formats have maturity support for the target engines.

[![](https://substackcdn.com/image/fetch/$s_!BrUB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F357ad3a6-434c-4f60-bea6-2b0fd26abc26_1464x462.png)](https://substackcdn.com/image/fetch/$s_!BrUB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F357ad3a6-434c-4f60-bea6-2b0fd26abc26_1464x462.png)

An MVP for evaluation and benchmarking is also needed here. But the criteria are not only about whether it can solve business problems or improve performance, but also about how well the engine performs in your specific use cases when working with your chosen table format.

This is very important. Although all table formats promise that you can put any query engine on top, the maturity of the support for different engines is not the same. It can work great with Spark, but Flink is another story, for example.

---

## How to manage the storage layout?

A lakehouse gives you greater control by letting you manage the entire storage layer, not just the table abstraction, but also the underlying files.

Spider-Man’s Uncle Ben said, “With great power comes great responsibility”.

[![r/Spiderman - With great power comes great responsibility.](https://substackcdn.com/image/fetch/$s_!kiRk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F02ab3dfa-21c2-4d2c-896f-9078d1e48540_600x453.jpeg "r/Spiderman - With great power comes great responsibility.")](https://substackcdn.com/image/fetch/$s_!kiRk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F02ab3dfa-21c2-4d2c-896f-9078d1e48540_600x453.jpeg)

from [here](https://www.reddit.com/r/Spiderman/comments/1c40dml/are_there_any_villains_that_put_a_dark_spin_on/)

This is especially true when it comes to self-managing the lakehouse storage. You might not know this, but your query performance depends a lot on how your data (files) are organized physically. So, we have to manage it carefully.

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=184279378)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

There are two main approaches you can use to intervene in the data's physical layout:

* **Colocation**: You might have heard of partitioning and clustering. The first splits the table into smaller portions, allowing the query engine to interact only with the required portion.

  [![](https://substackcdn.com/image/fetch/$s_!eFKa!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96fe9165-c823-4bd8-a6a9-c9ee8e3834cb_660x374.png)](https://substackcdn.com/image/fetch/$s_!eFKa!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96fe9165-c823-4bd8-a6a9-c9ee8e3834cb_660x374.png)

  The latter collocates data in finer-grained form by techniques such as sorting or z-ordering. However, clustering requires continuous management as new data might not follow the clustering scheme.

  [![](https://substackcdn.com/image/fetch/$s_!fVb1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdcc4c438-bac1-4cb6-81ce-450bc4f919c9_1042x556.png)](https://substackcdn.com/image/fetch/$s_!fVb1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdcc4c438-bac1-4cb6-81ce-450bc4f919c9_1042x556.png)

  + For example, data is sorted by column A in storage; however, the new batch of data is only sorted locally within that batch, not globally across the table. This requires a re-arrangement process (e.g., reading the whole data, sorting it, and writing it back)
* **File size controlling**: The smaller the file, the faster the write and the less the write engine’s memory pressure.

  [![](https://substackcdn.com/image/fetch/$s_!YpAq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7808fea9-089b-41b1-8961-107b8c0d9d5d_932x666.png)](https://substackcdn.com/image/fetch/$s_!YpAq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7808fea9-089b-41b1-8961-107b8c0d9d5d_932x666.png)

  However, read operations don’t like small files as they must open/read/close tons of files, which eventually impacts the performance. Thus, the open table format and query engine provide methods to compact files, optimizing file size without affecting data integrity during other read/write operations.

Most table formats let you define partitioning and clustering schemes. Some query engines allow you to configure the target ingest files based on your needs. Some table format - engine integrations also expose an API for the compaction process.

The hard part is making decisions:

[![](https://substackcdn.com/image/fetch/$s_!9lQB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa1b13f32-ba00-4f32-838b-d7e29d698ae4_1414x770.png)](https://substackcdn.com/image/fetch/$s_!9lQB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa1b13f32-ba00-4f32-838b-d7e29d698ae4_1414x770.png)

* Which partition scheme suits my needs? What if the partition scheme changes in the future (e.g., hourly to daily)
* Sorting is enough, or I have to use z-ordering or other advanced methods for clustering.
* How do I keep data together as new data keeps coming up?
* Which is the target file size I need to configure?
* How to manage the compaction process? A dedicated service? The frequency? The target file size?
* many more…

As with decisions about storage formats and query engines, these questions should be resolved based on business needs. Building an MVP can also help clarify and evaluate the options.

—

You don’t need to ask most of those questions when you work with BigQuery or Snowflake, as the vendors maintain everything related to the physical data layout. Your job is to tell them which partitioning and clustering schema you choose, and they will take care of the rest.

[![](https://substackcdn.com/image/fetch/$s_!W1pP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3bf70865-5fb0-4de3-a116-7ea71c80a785_1468x810.png)](https://substackcdn.com/image/fetch/$s_!W1pP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3bf70865-5fb0-4de3-a116-7ea71c80a785_1468x810.png)

During my research on OLAP systems, keeping the physical data layout optimal is not easy, as many steps are involved, from defining the file size to the compaction process.

Now, we, the lakehouse builder, have to take care of this.

---

## How do you manage table format metadata?

As discussed above, lakehouse architecture requires a translator, a metadata layer, to help the query engine/users view data files as tables. However, this layer could also become a bottleneck if it is not managed carefully.

Essentially, this layer is a set of metadata files that is stored alongside the data files.

> ***Note:** This is not true for DuckLake as it manages metadata via a dedicated transactional database.*

Before the query engine can touch the data files, it must visit the metadata files to understand the table structure, including the schema, partitioning/clustering schemes, available data snapshots, and data statistics such as column value min/max.

[![](https://substackcdn.com/image/fetch/$s_!Ptb9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa41dbe93-acc3-400a-8126-6f4ac28ece2d_1448x676.png)](https://substackcdn.com/image/fetch/$s_!Ptb9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa41dbe93-acc3-400a-8126-6f4ac28ece2d_1448x676.png)

And because the metadata is stored in files, it must also affect the query engine's performance if there are too many files to open/read/close. The longer you operate the lakehouse, the more metadata files will be created as data is ingested.

There must be a strategy to keep the number of metadata files optimal. You can find this from the documentation of your chosen table formats/query engines. And, like the data files compaction process, you also have to decide how to manage it and what frequency best suits your needs.

---

## How do you manage access control?

The lakehouse should be the access point for the whole organization. Many teams with different authorizations need to dive into the data. Because you now control the entire storage system layer, you must also handle security at a more granular level.

[![](https://substackcdn.com/image/fetch/$s_!tMD2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F46277fc5-a25a-460f-80ff-48496de59d3d_1150x568.png)](https://substackcdn.com/image/fetch/$s_!tMD2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F46277fc5-a25a-460f-80ff-48496de59d3d_1150x568.png)

BigQuery or Snowflake lets you do this by specifying the security policy right on the UI. But when you have to manage the lakehouse by yourself, you need to do more than that:

* Users can bypass the table format layer and query the data in the object storage directly. How do you deal with that?
* What security scheme will you choose? Access rules or credential vending (temporary credentials for accessing underlying data files)? Role-Based Access Control (RBAC) or/and Attribute-Based Access Control (ABAC)?
* How do you collect all data access and system activities for incident detection?
* How do you protect PII data?
* many more

Hours of reading the table-format documentation, adopting a third-party service, or even self-developing a custom solution are needed, as data is your company's most valuable asset, regardless of the architecture you implement.

---

## How about user/developer experience?

You build a fancy data lakehouse, but only you and your team understand how to interact with it.

Great, your lakehouse adds no value.

### Discoverable data

As your lakehouse accumulates more data assets, it will become increasingly complex for users to understand what’s happening in the organization’s data systems. We must provide the user with the capability to search data, expose business glossaries, definitions, and lineage to explain the data’s meaning and origin.

[![](https://substackcdn.com/image/fetch/$s_!otXY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F71e4b373-f56a-48c6-8512-cd7276a2d6a5_1092x418.png)](https://substackcdn.com/image/fetch/$s_!otXY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F71e4b373-f56a-48c6-8512-cd7276a2d6a5_1092x418.png)

These functionalities also require you to spend time consuming the table format documentation on how to integrate with platforms such as Datahub and OpenMetadata (or self-develop a custom solution)

### Local development

What if a user wants to develop a new data report pipeline? How do they develop, test, and validate what she has done locally? As data practitioners apply more and more software engineering best practices to data engineering, the ability to iterate quickly on the developer’s laptop is crucial.

[![](https://substackcdn.com/image/fetch/$s_!ivIA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe98418d5-bc2f-4f00-8b05-0c030c557258_698x498.png)](https://substackcdn.com/image/fetch/$s_!ivIA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe98418d5-bc2f-4f00-8b05-0c030c557258_698x498.png)

So how do you offer that ability?

Thanks to the nature of the lakehouse, you can bring different storage engines on top of the storage layer. You can leverage this to onboard local-friendly engines such as Polars or DuckDB. However, different query engines in different environments might cause problems due to mismatched syntax.

Another approach is to provide a development kit to users so they can easily deploy the necessary service directly on their laptops with a few simple copy-and-run commands.

No matter which approach you choose, providing a seamless local development experience is a time-consuming and highly user-oriented process.

### UI/UX

Most of us are used to the convenient UI/UX that lets us run SQL queries, list tables, browse running history, monitor jobs, grant permissions, … from vendors such as BigQuery, Snowflake, or Databricks.

When you build the data lakehouse, you must also address this, as most users have very high standards for UI/UX on a data platform (vendors have been doing a great job here).

[![](https://substackcdn.com/image/fetch/$s_!KY7f!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd003b419-7732-433e-a8d5-d5b061fd317f_1290x880.png)](https://substackcdn.com/image/fetch/$s_!KY7f!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd003b419-7732-433e-a8d5-d5b061fd317f_1290x880.png)

Ensuring the lakehouse user experience might require a dedicated web-app project (involving backend and frontend developers) to build a portal that includes everything from an SQL editor to a place to register a new query engine, for example. Delivering the user experience with BigQuery, Snowflake, or Databricks is not easy.

Somebody thinks when they’re done with the core component under the hood, they’re done. But that’s only 50% of the story. How users interact with and use your lakehouse determines whether your project succeeds.

---

## Some of my thoughts

After writing about my concerns with building a lakehouse from scratch in this article, I realized that managing all the aspects/components of a lakehouse on your own is highly resource-intensive. This is even more challenging if your team is small (maybe just you) and has no experience with lakehouse table formats.

If, after trying other solutions, your team still sees Lakehouse as the most suitable option at that moment, I personally recommend handing over some parts of your tech stack to vendors; for example, let a vendor manage the Iceberg implementation and use Spark and Flink on cloud platforms. Some people worry that relying on vendors will lead to vendor lock-in (that’s not the spirit of the lakehouse)

[![](https://substackcdn.com/image/fetch/$s_!exv0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F42960362-063a-4c46-afb2-b80b54b24975_830x498.png)](https://substackcdn.com/image/fetch/$s_!exv0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F42960362-063a-4c46-afb2-b80b54b24975_830x498.png)

That’s true if you require a complete openness solution. I believe that only exists in a very big company with a diverse range of use cases that require many query engines (which they self-develop) and sharing methods to adapt to their requirements. They have sufficient resources to self-manage their whole solution.

If I were required to build a lakehouse solution, but all the use cases could be resolved with BigQuery, Spark, and DuckDB, I would have Google Cloud manage it for me instead of managing it myself, because I believe the vendor could provide sufficient integration points across the whole stack to make it work.

> *This is just a personal example and is not sponsored by Google.*

## Outro

In this article, I listed some big questions and tried to provide tool-agnostic answers on important aspects of lakehouse architecture, from compute and storage to governance and user experience.

If you want to give me feedback, feel free to leave comments or inbox me. Thank you for reading this far. See you in my following articles.
