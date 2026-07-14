---
title: "I spent 8 hours learning the CAP theorem. Here’s what I found."
channel: vutr
author: "Vu Trinh"
published: 2026-06-02
url: https://vutr.substack.com/p/i-spent-8-hours-learning-the-cap
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Kafka", "Apache Spark", "Apache Flink", "Snowflake", "Databricks", "BigQuery", "Streaming"]
tags: [https, auto, fetch, substackcdn, image, good]
---

# I spent 8 hours learning the CAP theorem. Here’s what I found.

*Did you know that the CAP theorem is the main motivation behind Lambda Architecture?*

> Source: [Open post](https://vutr.substack.com/p/i-spent-8-hours-learning-the-cap)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-flink|Apache Flink]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[bigquery|BigQuery]] · [[streaming|Streaming]]

---

> *I invite you to join my paid membership list for only **7$/month** (pay annually) to get access to:*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: 65 LeetCode-style problems to practice Spark SQL/DataFrame
> * ***learn-spark**: a CLI tool to master Apache Spark internals*
> * ***learn-dbt**: a CLI tool to master dbt from the ground up*
> * ***learn\_airflow:** a CLI tool that equips you with all the Airflow fundamentals*
> * *All future learning tools → [Tools Demo](https://substack-github-sync.vutrinh2704.workers.dev/)*
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!cQWx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F91c2c86c-b494-4fe0-87c7-238a6459d444_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!cQWx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F91c2c86c-b494-4fe0-87c7-238a6459d444_2000x1429.png)

---

# Intro

I intend to write about CAP for a long time, in the early days of this newsletter. I hesitated because I thought it was too technical and barely brought value to data engineers.

Thus, I put it aside until last weekend.

I revisited my “idea” repository, scrolled a bit, and don’t know why I stopped at CAP. This time, I did more research and gained insights into data engineering, especially the Lambda and Kappa Architectures. Thus, I believe I can deliver my understanding of CAP in a more useful way to you guys.

That’s why this article was written.

---

# What is CAP?

Let’s start with a single machine: one database node, a client writes a value, and another client reads it back. The machine either works or it doesn’t.

Simple, right?

Now, let’s add a node to make things fun.

We want both nodes to serve reads for availability and throughput. To do that, both must stay in sync. And you want the system to keep working even when the network between them drops.

That's where the CAP exists.

## The C, A, and P

[![](https://substackcdn.com/image/fetch/$s_!QWse!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c2d523b-7bbb-4c77-a391-f55c3fbf2aa9_1194x782.png)](https://substackcdn.com/image/fetch/$s_!QWse!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c2d523b-7bbb-4c77-a391-f55c3fbf2aa9_1194x782.png)

**The C, the Consistency,** means all nodes see the same data at the same time. If a change is made, clients querying any node will get the most recent write. The moment a write is acknowledged, every node in the system reflects it.

> ***Note**: this is not the same as the C in ACID. ACID consistency means your transactions don’t violate constraints: referential integrity, unique keys, that kind of thing. CAP consistency means linearizability across nodes. Two different things that somehow share a name and confuse us.*

[![](https://substackcdn.com/image/fetch/$s_!o_cr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe7b8791e-be3a-4e4b-8500-6809cc671ddd_1038x690.png)](https://substackcdn.com/image/fetch/$s_!o_cr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe7b8791e-be3a-4e4b-8500-6809cc671ddd_1038x690.png)

**Availability** means every request gets a response. If a node is up, it answers back.

[![](https://substackcdn.com/image/fetch/$s_!7nCv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F50ea2b3b-5bfa-445e-b7cf-d5a0fb5b5b19_1040x654.png)](https://substackcdn.com/image/fetch/$s_!7nCv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F50ea2b3b-5bfa-445e-b7cf-d5a0fb5b5b19_1040x654.png)

**Partition Tolerance** means the system keeps operating even when the network between nodes breaks, and messages get lost. Some nodes can’t “talk” to others.

The computer scientist [Eric Brewer](https://en.wikipedia.org/wiki/Eric_Brewer_(scientist)), who proposed CAP, states that any [distributed data store](https://en.wikipedia.org/wiki/Distributed_data_store) can provide at most two of the C, A, and P.

## Pick twos

In the three, partition tolerance isn’t a knob you can tune.

You can’t predict network failures, cables get unplugged, and cloud availability zones lose connectivity, or a heavy garbage collection pause on one node can look exactly like a network partition to its neighbors.

This fact, plus Eric Brewer’s statement about “can provide at most two”, we can say that in any distributed data store, we can only pick between CP and AP.

In a two-node setup, if partition tolerance happens (Node A and B can’t talk to each other), and you:

[![](https://substackcdn.com/image/fetch/$s_!ajMj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F722033e5-5cd5-4aee-a3ba-5a8e6172cb3a_620x430.png)](https://substackcdn.com/image/fetch/$s_!ajMj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F722033e5-5cd5-4aee-a3ba-5a8e6172cb3a_620x430.png)

* **Choose consistency:** Node A refuses the write/read until it can confirm with Node B. This is to ensure that all nodes see the same data at the same time and that the query gets the most recent write. The system becomes partially unavailable during the partition, which means you can’t have the “**availability**“.

  [![](https://substackcdn.com/image/fetch/$s_!TUrF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2c11b39b-2032-4ac2-ac45-c1f4a5aceed4_986x638.png)](https://substackcdn.com/image/fetch/$s_!TUrF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2c11b39b-2032-4ac2-ac45-c1f4a5aceed4_986x638.png)
* **Choose availability**: Node A still answers the query and accepts the write. Node B will also do the same. However, they’re not kept in sync; B is not aware of A’s write and vice versa, which means you can’t have the “**consistency**“.

Imagine you insist on having both. The partition tolerance happens. Node A and Node B cannot talk.

[![](https://substackcdn.com/image/fetch/$s_!dd-l!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F84066b39-0142-42da-9bb2-c26d5e2babed_1150x418.png)](https://substackcdn.com/image/fetch/$s_!dd-l!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F84066b39-0142-42da-9bb2-c26d5e2babed_1150x418.png)

* A client writes `x = 1` to Node A.
* Another client reads `x` from Node B.
* For availability to hold, Node B must respond; it can’t say “try again later.”
* For consistency to hold, Node B must return `x = 1`, the value that was just written to Node A. But Node B hasn’t received that write because it can communicate with Node A.
* So Node B either responds with a stale value: violating **consistency**, or refuses to respond: violating **availability**.

There is no world where Node B answers correctly and immediately. This means, in CAP, you can choose either Consistency-Partition or Availability-Partition.

[![](https://substackcdn.com/image/fetch/$s_!R7kp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5b12c01a-66b7-4035-8049-f47de59f94d0_1496x426.png)](https://substackcdn.com/image/fetch/$s_!R7kp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5b12c01a-66b7-4035-8049-f47de59f94d0_1496x426.png)

> *I invite you to join my paid membership list for only **7$/month** (pay annually) to get access to:*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: 65 LeetCode-style problems to practice Spark SQL/DataFrame
> * ***learn-spark**: a CLI tool to master Apache Spark internals*
> * ***learn-dbt**: a CLI tool to master dbt from the ground up*
> * ***learn\_airflow:** a CLI tool that equips you with all the Airflow fundamentals*
> * *All future learning tools → [Tools Demo](https://substack-github-sync.vutrinh2704.workers.dev/)*
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=199030261)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

---

# Eventual consistency

Regarding the AP, your system can be inconsistent for a while, but not forever; there must be an auto-correct mechanism to sync changes from Node A to B and vice versa.

[![](https://substackcdn.com/image/fetch/$s_!Wki9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdcf23e9b-eb4c-4797-ae89-74c249aa67dc_1312x566.png)](https://substackcdn.com/image/fetch/$s_!Wki9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdcf23e9b-eb4c-4797-ae89-74c249aa67dc_1312x566.png)

In other words, your system will be fine, eventually.

This is called eventual consistency (EC).

When a system is eventually consistent, it makes one promise: all nodes will *eventually* converge to the same value.

Imagine you update your profile picture. The write lands on Node A. You refresh the page. The request hits Node B. Node B hasn’t received the update yet. You still see the old photo. You wait a while, then refresh again and see the new picture. The gap between the two avatars has little impact; eventual consistency is acceptable.

Now imagine the same scenario, but instead of a profile picture, it’s an inventory count. Node A says 1 item left in stock. Node B also says 1 item left. Two customers simultaneously buy the last item, one from each node. Both writings are accepted. You’ve now sold the same item twice. Unlike the previous case, the eventual consistency is not acceptable.

Eventual consistency trades “right-now” data synchronization for higher availability and faster read/write speeds (since the system doesn’t need to sync).

EC can sometimes impact your pipeline.

Imagine you’re building a pipeline on top of DynamoDB, an AP system, eventually consistent by default. Your pipeline reads user activity records to compute daily engagement metrics. DynamoDB serves reads from the nearest replica. During high-write periods, that replica might still receive all new data when the pipeline read occurs.

[![](https://substackcdn.com/image/fetch/$s_!QIIx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf22c2cc-3919-4786-a77e-5222eec71264_1732x618.png)](https://substackcdn.com/image/fetch/$s_!QIIx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf22c2cc-3919-4786-a77e-5222eec71264_1732x618.png)

Your pipeline runs, pulls records, and computes aggregates, but some of the most recent writes haven’t propagated yet. Although it might be a rare case, you still need to keep it in mind.

In the past, S3 supported EC for overwrites and deletes (AWS moved S3 to strong consistency in December 2020), which meant: you write a new version of a file, immediately read it back, and get the old version. You delete a file, immediately list the bucket, and it’s still there. A Spark job writes output files to S3, and a downstream job then reads those files. If the downstream job started too quickly, it could read a stale file listing.

An annoying thing is that the EC bug is almost impossible to reproduce reliably.

---

# Making the trade-off in tools

So far, we’ve been talking about CAP as a choice you make. In reality, the choice is already made by the people who built the tools you're using.

## The CP systems

[![](https://substackcdn.com/image/fetch/$s_!QSk0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb1025000-d239-4030-8b79-257be03d60f5_692x416.png)](https://substackcdn.com/image/fetch/$s_!QSk0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb1025000-d239-4030-8b79-257be03d60f5_692x416.png)

* **Zookeeper**, which many data systems (e.g, Kafka, Clickhouse) use for coordination, is a CP. It’s designed to be the source of truth for distributed configuration, leader election, and service discovery. Thus, inconsistent data is not acceptable.

* **SQL OLTP** databases like Postgres also fall under this category. This is understandable, as these databases are used to handle critical transactional data for user-facing applications (e.g., banking apps, shopping websites).

## The AP systems

[![](https://substackcdn.com/image/fetch/$s_!Qxsx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdc9d0063-4ce8-40cc-b92b-246eb3bec8e0_714x400.png)](https://substackcdn.com/image/fetch/$s_!Qxsx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdc9d0063-4ce8-40cc-b92b-246eb3bec8e0_714x400.png)

* **DynamoDB**: By default, reads are eventually consistent; they’re served from any replica, which may not have the most recent data.
* **Cassandra** was designed at Facebook for availability at a massive scale. It uses a peer-to-peer architecture with no single master. During a partition, every node keeps accepting writes. When the partition heals, it uses last-write-wins reconciliation based on timestamps to resolve conflicts.

## OLAP systems

[![](https://substackcdn.com/image/fetch/$s_!OBo_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa07b1b8b-1918-4e97-bb3b-338971fc744c_818x810.png)](https://substackcdn.com/image/fetch/$s_!OBo_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa07b1b8b-1918-4e97-bb3b-338971fc744c_818x810.png)

For most OLAP systems we use, such as Clickhouse, BigQuery, Snowflake, or Redshift, you won’t see the CAP discussion as much as in the transactional world because the workload is different. Saying that does not mean those systems don’t make the choices. Here are the two examples:

> *For the same reason, the OLAP systems don’t explicitly tell whether they are AP or CP. What you’re going to read is my own interpretation; correct me if I’m wrong.*

* **ClickHouse** (AP) uses eventual consistency for replicated tables by default: replicas sync asynchronously. A freshly written row may not be immediately visible on all replicas.

  [![](https://substackcdn.com/image/fetch/$s_!hoUS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd089e883-41d7-4b13-83fa-744eb5278fca_1586x446.png)](https://substackcdn.com/image/fetch/$s_!hoUS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd089e883-41d7-4b13-83fa-744eb5278fca_1586x446.png)
* **BigQuery** sits closer to CP. The storage engine underlying BigQuery is called Vortex and is described in a 2024 paper. Vortex guarantees ACID properties for all API operations. When a write is acknowledged on an UNBUFFERED stream, any subsequent read is guaranteed to see it. The engine synchronously replicates to two Colossus clusters before returning success to the client. Where it gets nuanced is at the ingestion boundary:

  + Vortex exposes three stream types: UNBUFFERED (commit immediately, visible right away), BUFFERED (written but invisible until you flush), and PENDING (nothing visible until you BatchCommit all streams atomically).

---

# CP vs AP choice

Once you know whether a system is CP or AP, the next step is to evaluate it for your use case. For data engineers specifically, there are two distinct situations in which such an evaluation is needed.

## Source

> *You rarely control it.*

Your pipeline reads from Kafka, DynamoDB, Cassandra, an operational database, and a SaaS API. You didn’t pick those systems. You consumed them and are directly impacted by their CP or AP properties.

Our job is to design the consuming logic to tolerate whatever guarantees it offers.

A few things worth considering for some scenarios:

[![](https://substackcdn.com/image/fetch/$s_!eX_5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff20c0e86-ac08-489b-9363-539da1633839_1054x550.png)](https://substackcdn.com/image/fetch/$s_!eX_5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff20c0e86-ac08-489b-9363-539da1633839_1054x550.png)

* If your source is **AP**, eventually consistent, like Cassandra or DynamoDB with default settings: keep in mind that reads can be stale, and you might need extra work to ensure what you’re reading is up-to-date, such as the read-repair or quorum reads.

  [![](https://substackcdn.com/image/fetch/$s_!vjUL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec3613b5-14d0-4c39-9a7b-19186f391be7_1064x542.png)](https://substackcdn.com/image/fetch/$s_!vjUL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec3613b5-14d0-4c39-9a7b-19186f391be7_1064x542.png)
* If your source is **CP**: like Postgres, HBase, or Zookeeper, you get consistency, but you need to respect the availability trade-off. During a partition tolerance, your source will stop responding rather than return stale data. Pay more attention to the retry policy. Don’t assume the source is always reachable.

  [![](https://substackcdn.com/image/fetch/$s_!oJh4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F793145b8-10c7-4941-87c0-ad24cce02bae_1268x796.png)](https://substackcdn.com/image/fetch/$s_!oJh4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F793145b8-10c7-4941-87c0-ad24cce02bae_1268x796.png)

* If your source is **Kafka**, be aware of your producer’s `acks` setting. `acks=1` means the leader acknowledged the message, but replicas may not have received it yet. A leader's failure somewhere between means a message your pipeline never saw. `acks=all` gives you more guarantee. If business records need to process all the records, the producer configuration upstream matters as much as anything you do downstream here.

## Sink

You’re writing pipeline output to a data store that serves the data to users. CAP trade-off is yours to make.

But here’s something worth saying first: for most OLAP use cases, this choice is invisible.

If you’re writing to Snowflake, BigQuery, Redshift, or Databricks for dashboarding and reporting, the consistency model is largely handled for you. These systems are built for read-heavy analytical workloads where the data is written in bulk, transformations run on a schedule, and the consumer is a BI tool, a notebook, a scheduled report, or queries data that’s already settled.

[![](https://substackcdn.com/image/fetch/$s_!zcwt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fab5224a4-6472-4bb1-a0c2-3a5edf997bb5_906x834.png)](https://substackcdn.com/image/fetch/$s_!zcwt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fab5224a4-6472-4bb1-a0c2-3a5edf997bb5_906x834.png)

In this world, CAP is mostly invisible. Your data arrives in batches. The writing comes first. The readers come after. The consistency window between when a write finishes and when a read occurs is measured in hours, days, or weeks.

—

However, modern data engineering is more than that. Real-time dashboards. Operational analytics. Product features backed by a data pipeline output.

In these cases, the delay between a write and a reader is narrow to seconds or sometimes less. And this is when the choice between AP and CP matters.

> *Although network partitions are rare, they still have a >0 chance of occurring.*

For example, you're running a Flink job, writing aggregates to Cassandra, Redis, or DynamoDB. A product dashboard refreshes every 5 seconds. An operations team makes decisions based on what it shows. The consistency model of your serving store now directly affects those decisions.

If a partition tolerance happens, you need to decide whether to show stale data (prefer availability) or return an error (prefer consistency).

For the decision, I personally have 2 questions to guide us here:

[![](https://substackcdn.com/image/fetch/$s_!eYJa!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb56376a1-0a59-4755-a5cc-f80e4b7b91c1_914x686.png)](https://substackcdn.com/image/fetch/$s_!eYJa!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb56376a1-0a59-4755-a5cc-f80e4b7b91c1_914x686.png)

* **What does a wrong answer cost?** If downstream systems act on your output to make real-world decisions, stale or conflicting data will cause a business problem. Prioritizing CP.

  [![](https://substackcdn.com/image/fetch/$s_!Hmnt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbc4c371b-241f-4d34-a854-7db7f1149cc0_1166x410.png)](https://substackcdn.com/image/fetch/$s_!Hmnt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbc4c371b-241f-4d34-a854-7db7f1149cc0_1166x410.png)
* **What does your availability requirement actually mean?** “The sink needs to be fast” and “the sink needs to be available” are not the same thing. A well-operated CP system can have very high availability under normal conditions. Going for AP when you need fast reads introduces side effects (e.g., stale data) but does not solve the right problem (low latency).

---

# PACELC

> *The model that explains what CAP leaves out*

CAP has a missing point. It assumes that the P will happen all the time. However, in real life, 99% of the time (stats made up by me), the network works perfectly.

And that's where [Daniel Abadi's PACELC](https://www.cs.umd.edu/~abadi/papers/abadi-pacelc.pdf) comes and extends the CAP.

Think about two requests hitting a distributed database under normal operating conditions. No network partition.

To serve a strongly consistent read, the system has to coordinate across replicas to confirm that what it returns is the most recent value. That process takes time. Network round-trip times and quorum checks (e.g., check other replicas to see if a new version of the record exists).

[![](https://substackcdn.com/image/fetch/$s_!eLBd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd707079b-3e63-4ab9-a152-ebd8a999bf5a_1024x916.png)](https://substackcdn.com/image/fetch/$s_!eLBd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd707079b-3e63-4ab9-a152-ebd8a999bf5a_1024x916.png)

The query has more latency. But the consistency is ensured.

If the query doesn’t require a strongly consistent read, the system simply returns whatever the current replica has and skips that coordination entirely.

[![](https://substackcdn.com/image/fetch/$s_!Teaq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7474d1f4-edbc-4d6a-b68e-82b301aac054_896x400.png)](https://substackcdn.com/image/fetch/$s_!Teaq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7474d1f4-edbc-4d6a-b68e-82b301aac054_896x400.png)

Way faster. But the data is potentially stale.

—

PACELC was introduced to model this observation.

[![](https://substackcdn.com/image/fetch/$s_!VVoM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9930e983-1cad-4e23-bc52-24261cbd5151_784x414.png)](https://substackcdn.com/image/fetch/$s_!VVoM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9930e983-1cad-4e23-bc52-24261cbd5151_784x414.png)

* If there is a Partition (P): choose between Availability (A) and Consistency (C), still CAP here.
* Else (E), when the system is running normally: choose between Latency (L) and Consistency (C).

## Why does this matter?

As I said, partitions are rare in practice. The CAP is a choice that surely matters when it happens; however, it still is the edge cases.

The more problems we, data engineers, might encounter more frequently are the ELC trade-off. For example:

* When working with DynamoDB’s, you can choose eventually consistent reads vs strongly consistent reads. The first is cheaper and has lower latency, while the latter is more expensive and takes longer.
* When you query a Cassandra database, the `ONE`, `QUORUM`, `ALL` consistent level is the way you tune the ELC trade-off. `ONE` returns the first replica that responds. Fast, but you may have gotten stale data. `QUORUM` waits for a majority of nodes to agree. Slower, but you got a stronger guarantee. `ALL` waits for every replica. Most safe but with the highest latency.

[![](https://substackcdn.com/image/fetch/$s_!D46I!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec98cd06-5742-4757-ae1b-b86812ba4aa5_1420x626.png)](https://substackcdn.com/image/fetch/$s_!D46I!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec98cd06-5742-4757-ae1b-b86812ba4aa5_1420x626.png)

* When Snowflake or BigQuery serves a query from a cached result rather than re-scanning the table, it's a kind of trading consistency for latency. In most cases, this is a valid trade, as data in most OLAP use cases arrives in batches at predefined intervals. Serving data outside this period is safe to assume that no new data has come in until the next ingest period. However, in rare cases, such as the backfill, the cache might serve stale data.

---

# Lambda and Kappa Architecture

> *Two answers to the same CAP problem*

## Lambda

As data engineers, we are familiar with or at least have heard of Lambda. But do you know that the Lambda architecture was introduced to “beat“ the CAP?

In 2011, Nathan Marz wrote an essay called "[How to beat the CAP theorem](https://nathanmarz.com/blog/how-to-beat-the-cap-theorem.html)." And what he proposed was a fundamentally different way of thinking about data.

Marz observed that the complexity comes from two things working together: mutable state and incremental updates. Not the CAP itself.

Traditional databases let you update data in place (at the time, OLAP systems with an immutable storage layer were uncommon). When you combine that with a distributed system, complexity arises because the update must remain consistent across nodes.

His solution is to eliminate mutable state and treat data as immutable and append-only. From there, Lambda Architecture is the practical system built on top of it.

The architecture has three layers.

[![](https://substackcdn.com/image/fetch/$s_!W4U1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F93b595a3-5c91-4f39-89b1-0713adc48856_1390x528.png)](https://substackcdn.com/image/fetch/$s_!W4U1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F93b595a3-5c91-4f39-89b1-0713adc48856_1390x528.png)

**The Batch Layer** deals with the complete, immutable datasets. On top of that, it precomputes query results by running functions across these datasets on a schedule (every few hours).

This layer is straightforward. No mutable state, thus no pressure to keep data in sync. If a bug produces wrong output, fix the bug, and simply rerun the computation on the immutable data.

However, batch layer can’t offer a more recent view of the data.

**The Speed Layer** fills the gap. It processes recent data using a stream processing framework/tool and a fast read/write store sink (e.g., Cassandra). This is where the CAP complexity lives: mutable state or eventual consistency. But it’s acceptable, as every X interval, a fresh batch run overrides the result made by the speed layer. Any inconsistency is self-correcting.

**The Serving Layer** merges results at query time. For the historical result, fetch from the batch layer; for the more recent view, fetch from the speed layer. The system then merges these two results to form a complete view for the user.

To me, Lambda doesn’t beat the CAP; it's just a workaround for the CAP.

## Kappa

Three years later, in 2014, Jay Kreps, the Kafka author, published an article on O’Reilly titled [“Questioning the Lambda Architecture.”](https://www.oreilly.com/radar/questioning-the-lambda-architecture/)

He agreed with the core principles: retain input data unchanged, model transformations as a series of materialized stages, and take reprocessing seriously.

But he points out a problem with Lambda: it requires us to implement the same logic twice: one for batch and one for stream. We need to keep them in sync. Two codebases, two different programming paradigms, and two systems to operate and debug.

—

Kreps proposed a simpler alternative, observing that if the stream processing system can replay historical data, we don’t need a batch layer.

[![](https://substackcdn.com/image/fetch/$s_!kE65!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6b747b67-bccb-4b42-a398-f09c3d60b5cd_1162x416.png)](https://substackcdn.com/image/fetch/$s_!kE65!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6b747b67-bccb-4b42-a398-f09c3d60b5cd_1162x416.png)

Kafka can already do this. When your processing code changes, you only need to start a second instance of the same streaming job, point it to the historical Kafka offset, consume data from that point, apply the new logic, and write out the result.

The CAP doesn’t disappear here.

You still have to decide what your streaming system does during a partition. But you’re making that decision once, in one place, not in two separate systems.

---

# Outro

In this article, I delivered my understanding and research on CAP. We first see what it is and why both A and C cannot exist when P happens. Then we move on to discuss eventual consistency and look at some example systems that are AP or CP. Next, I share my evaluation to choose between consistency and availability and see a CAP’s extension called PACELC. Finally, we cover the Lambda and Kappa architectures. The first motivation is to overcome the CAP limitation.

Thank you for reading this far. See you in my next article.

---

# Reference

*[1] Nathan Marz, [How to beat the CAP theorem](http://nathanmarz.com/blog/how-to-beat-the-cap-theorem.html) (2011)*

*[2] Jay Kreps, [Questioning the Lambda Architecture](https://www.oreilly.com/radar/questioning-the-lambda-architecture/) (2014)*
