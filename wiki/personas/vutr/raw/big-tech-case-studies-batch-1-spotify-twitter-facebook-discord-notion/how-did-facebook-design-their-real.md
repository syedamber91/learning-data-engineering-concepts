---
title: "How did Facebook design their Real-Time Processing ecosystem"
channel: vutr
author: "Vu Trinh"
published: 2024-08-17
url: https://vutr.substack.com/p/how-did-facebook-design-their-real
paid: false
topics: ["Apache Kafka", "Apache Spark", "Apache Flink", "Data Warehouse", "Streaming", "Batch Processing"]
tags: [https, auto, image, processing, state, facebook]
---

# How did Facebook design their Real-Time Processing ecosystem

*Hundreds of GBs per Second*

> Source: [Open post](https://vutr.substack.com/p/how-did-facebook-design-their-real)

## Topics

[[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-flink|Apache Flink]] · [[data-warehouse|Data Warehouse]] · [[streaming|Streaming]] · [[batch-processing|Batch Processing]]

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=147275191)

[![](https://substackcdn.com/image/fetch/$s_!2k3o!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F46a27b5d-4b3e-4f49-a207-89043f3ba329_1400x997.png)](https://substackcdn.com/image/fetch/$s_!2k3o!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F46a27b5d-4b3e-4f49-a207-89043f3ba329_1400x997.png)

Image created by the author.

---

## Intro

This week, we will explore Facebook’s real-time processing system [through their](https://research.facebook.com/publications/realtime-data-processing-at-facebook/) 2018 paper. The paper does not provide all the specific components of their architecture. Instead, it introduced crucial decisions that Facebook engineers have made when building the real-time data processing ecosystem. Now, let’s get started.

> *The paper is published in 2018 so it might not reflect the current Facebook infrastructure. Depsite being rebranded to Meta, I still used “Facebook” to align with the paper.*

---

## Overview

Real-time data processing backed many essential applications at Facebook, including real-time reporting of the aggregated, analytics for mobile applications, and Facebook page insights. Their requirement for real-time processing was a few seconds of latency with hundreds of gigabytes per second throughput. The following qualities are crucial in the real-time data system design:

* Ease of use: How fast can a user write, test, and deploy a new application?
* Performance: How low is the latency, and how high is the throughput?
* Fault-tolerance: What kinds of failures can the system tolerate?
* Scalability: How well does the system adapt to changes in volume?
* Correctness: Does dropping some message affect the result?

Let's take a closer look at their real-time data architecture.

[![](https://substackcdn.com/image/fetch/$s_!em8y!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F103ba2fa-c54e-4650-b9ab-e9a4cbc83a4c_1228x645.png)](https://substackcdn.com/image/fetch/$s_!em8y!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F103ba2fa-c54e-4650-b9ab-e9a4cbc83a4c_1228x645.png)

Facebook real-time architecture overview. Image created by the author.

Facebook decouples the data transport from the processing. At the heart is the persistent message bus for data exchange between services. The data mainly originates in mobile and web products; it is ingested into Scribe—a distributed data transport system for further processing. Real-time stream processing systems like Puma, Stylus, and Swift consume data from the Scribe to apply transformation logic. There are data stores like Laser, Scuba, and Hive for the destination. Let's walk through the systems mentioned above.

### Scribe

[![](https://substackcdn.com/image/fetch/$s_!f_C8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F65ce0a8e-4d70-4c3c-8dd9-2f59d3d5e39e_977x422.png)](https://substackcdn.com/image/fetch/$s_!f_C8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F65ce0a8e-4d70-4c3c-8dd9-2f59d3d5e39e_977x422.png)

Scribe Overview. Image created by the author.

This distributed messaging system delivers high volumes of log data with a few seconds of latency and high throughput (imagine Kafka). Scribe organizes data into categories (like topics in Kafka). A category has multiple buckets; each bucket is the processing unit for stream processing systems. Unlike Kafka, where consumers pull data from a partition, Scribe pushes different buckets to different processes to parallelize the application. The system achieves durability by storing data in the HDFS; Scribe can replay the data for up to a few days.

### Puma

[![](https://substackcdn.com/image/fetch/$s_!7U7n!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff4192406-4aac-4693-bcab-44fcf36d386f_587x369.png)](https://substackcdn.com/image/fetch/$s_!7U7n!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff4192406-4aac-4693-bcab-44fcf36d386f_587x369.png)

Image created by the author

Puma is a stream processing system that lets users write applications in an SQL-like language with Java UDFs. Unlike ad-hoc workloads, the system is designed for long-term deployments, running for months or years. Puma applications store state in a shared HBase cluster. At Facebook, Puma serves two primary purposes:

* Providing pre-computed query results for simple aggregation queries and
* Providing filtering and processing of Scribe streams.

### Swift

[![](https://substackcdn.com/image/fetch/$s_!wVAQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd9f58843-bf6b-4ecb-8d31-0849786a8601_587x374.png)](https://substackcdn.com/image/fetch/$s_!wVAQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd9f58843-bf6b-4ecb-8d31-0849786a8601_587x374.png)

Image created by the author

Swift is a stream processing engine that provides Scribe with checkpointing functionalities. It offers a simple interface, allowing users to read from a Scribe stream with checkpoints set for every N string or B bytes. If an app crashes, data reading can restart from the latest checkpoint, ensuring all data is read at least once. Users mainly write Swift applications using scripting languages like Python.

### Stylus

[![](https://substackcdn.com/image/fetch/$s_!QmlN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec8c3795-5732-4aab-a2d0-22a9d0aa9524_587x374.png)](https://substackcdn.com/image/fetch/$s_!QmlN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec8c3795-5732-4aab-a2d0-22a9d0aa9524_587x374.png)

Image created by the author

Stylus is a low-level stream processing framework written in C++. Its core component is a stream processor that takes input from a Scribe stream and outputs it to another Scribe stream or a data store. When using Stylus, application developers must identify the event time data in the stream. In return, Stylus offers a function to estimate the event time watermark with a given confidence interval.

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=147275191)

---

### Laser

Laser is a high-throughput, low-latency key-value storage service built on RocksDB. It can read data from real-time sources like Scribe categories or offline sources like Hive tables.

[![](https://substackcdn.com/image/fetch/$s_!bJG2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c8f960d-a5c4-4dd9-a770-a5bc4ec0e691_951x780.png)](https://substackcdn.com/image/fetch/$s_!bJG2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c8f960d-a5c4-4dd9-a770-a5bc4ec0e691_951x780.png)

Image created by the author

Laser has two common use cases:

* Serving the output stream of a Puma or Stylus app to Facebook products.
* Making the results of complex Hive queries or Scribe streams available to Puma or Stylus apps.

### Scuba

[![](https://substackcdn.com/image/fetch/$s_!h6zx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F238bc82a-ce73-4fe9-aa6c-64faba8607e5_1080x544.png)](https://substackcdn.com/image/fetch/$s_!h6zx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F238bc82a-ce73-4fe9-aa6c-64faba8607e5_1080x544.png)

Image created by the author

Scuba is Facebook’s real-time analytics system, capable of ingesting millions of new rows per second. Data usually flows from products through Scribe into Scuba with less than one minute delay. Scuba can also accept output from any Puma, Stylus, or Swift app. It supports ad-hoc queries with the most response times under 1 second.

### Hive data warehouse

[![](https://substackcdn.com/image/fetch/$s_!Ylqh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2f415cbc-04b4-4c75-89a0-0161da7080fe_964x494.png)](https://substackcdn.com/image/fetch/$s_!Ylqh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2f415cbc-04b4-4c75-89a0-0161da7080fe_964x494.png)

Image created by the author

Hive is Facebook’s data warehouse solution. It manages multiple petabytes of new data daily, with about half coming from raw event data ingested via Scribe. Tables in Hive are usually partitioned by day. Puma, Stylus, or Swift applications handle real-time processing of this data. Users can use Presto to query Hive data with full ANSI SQL support.

### Example Application

[![](https://substackcdn.com/image/fetch/$s_!G50H!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff9603734-0862-4dc1-9ba5-430730b3baaf_974x337.png)](https://substackcdn.com/image/fetch/$s_!G50H!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff9603734-0862-4dc1-9ba5-430730b3baaf_974x337.png)

Image created by the author

Let’s continue with an example of Facebook’s real-time pipeline. This application identifies trending events in an input stream of events. The events contain an event type, a dimension ID, and text. The application output is a list of ranked topics (ordered by event count) for each 5-minute interval. The application has four processing nodes, each with multiple processes that handle disjoint partitions of their input in parallel:

* The filter node processes the input stream by event type and shards the output based on the dimension ID for parallel processing by the next node.
* The Joiner queries external systems for information using the dimension ID and classifies events by topic based on text (left join).
* The Scorer maintains a sliding window of event counts per topic and tracks long-term trends. Based on these trends and current counts, it computes a score for each (event, topic) pair and sends the scores to the Ranker.
* The Ranker calculates the top K events for each topic within N-minute time buckets.

In this example, the first two nodes, Filter and Joiner, are stateless, while the subsequent nodes are stateful.

The following sections will outline Facebook’s five critical design decisions for real-time processing systems.

## Language paradigm

The first design decision is the language users will use to develop applications. This affects the ease of development, and the level of control developers have over performance.

[![](https://substackcdn.com/image/fetch/$s_!673E!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb8cd3f0b-de25-4d66-b587-64ab72e13032_960x399.png)](https://substackcdn.com/image/fetch/$s_!673E!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb8cd3f0b-de25-4d66-b587-64ab72e13032_960x399.png)

Image created by the author

There are three common choices:

* Declarative: SQL is simple and fast to write but has limited expressiveness.
* Functional: Functional programming models represent applications as sequences of predefined operators.
* Procedural: Languages like C++, Java, and Python offer the most flexibility and performance, giving complete control over data structures and execution. However, they take longer to write and test.

Puma applications are written in SQL, allowing quick development and testing within an hour. Swift applications, primarily written in Python, are ideal for prototyping and low-throughput tasks. Stylus applications are written in C++ and offer the most flexibility for complex stream processing, but they take longer to develop, often requiring a few days of work. When the paper was written, they didn’t offer any functional paradigms.

---

## Data transfer

The second design decision is the mechanism for transferring data between nodes. This decision impacts system fault tolerance, performance, and scalability and also affects the ease of debugging.

Typical choices for data transfer include:

[![](https://substackcdn.com/image/fetch/$s_!AOaf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6163f9b2-a4de-42aa-8d3e-c40e15115cd9_1267x473.png)](https://substackcdn.com/image/fetch/$s_!AOaf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6163f9b2-a4de-42aa-8d3e-c40e15115cd9_1267x473.png)

Image created by the author

* Direct message transfer: This mechanism uses RPC or in-memory queues for direct data transfer, achieving end-to-end latency in the tens of milliseconds.
* Broker-based message transfer: A separate broker sits between processing nodes, forwarding messages between them. While this adds overhead, it improves scalability by multiplexing input streams to multiple output processors and applying back pressure when needed.
* Persistent storage-based message transfer: One processor writes the output stream to a persistent store, and the next processor reads data from that store. This method is the most reliable; it allows the processors to write and read at different speeds and to read the same data multiple times, which is very helpful in case processing recovery.

In more detail, there are two types of dependency when transferring data between consecutive nodes; if you’ve learned Spark before, you might find this familiar:

* Narrow dependency connections link a fixed number of sender partitions to receiver partitions (one-to-one)
* Wide dependency connections link every sender partition to each receiver partition (one-to-many).

Facebook uses Scribe as a persistent message bus to implement data transfer between nodes. As mentioned, Facebook aims to optimize for second latency in their real-time systems. Thus, the minor latency of data writing to/ reading from Scribe is acceptable. Furthermore, a persistent store requires additional hardware and network bandwidth. On the other hand, leveraging a persistent message bus gives Facebook multiple advantages:

* Fault tolerance: A stream node failure will not affect the overall systems. They need to be replaced with a new node because the data is persisted on Scribe. The message bus also allows running duplicate downstream nodes to output redundant data for recovery purposes.
* Performance: If a processing node is slow, it doesn’t impact the previous node. If a machine is overloaded, some jobs are moved to a new machine, which resumes processing the input stream from where it left off.
* Ease of use: Debugging is easier since users can reproduce issues by reprocessing the same input stream from a new node. They also have flexibility in application design, allowing them to connect components within the same DAG. For instance, Puma output can be used as input for Stylus, and Stylus output can be fed into Scuba or Hive data stores.v
* Scalability: They can adjust the number of partitions up or down by changing the bucket count per Scribe category.

## Processing semantics

In general, a stream processor performs three main activities: (1) Processing input events, (2) Generating output, and (3) Saving checkpoints for failure recovery. Checkpoints may include (a) The state of the processing node, (b) The current offset in the input stream, and (c) The output value. How these activities are implemented defines the processor’s semantics. There are two key semantics:

* **State semantics:** Can each input event be counted at least once, at most once, or exactly once?
* **Output semantics:** Can a given output value appear in the output stream at least once, at most once, or exactly once?

Stateless processors have only output semantics, while stateful processors have both output and state semantics. State semantics vary based on the order of saving the state:

* At-least-once state semantics save the in-memory state first, then save the offset.
* At-most-once state semantics save the offset first, then save the in-memory state.
* Exactly-once state semantics save the in-memory state and the offset atomically.

Output semantics depend on saving the output value in the checkpoint, in addition to the in-memory state and offset.

* At-least-once output semantics emit output to the output stream, then save a checkpoint of the offset and in-memory state.
* At-most-once output semantics save a checkpoint of the offset and in-memory state, then emit output.
* Exactly-once output semantics save a checkpoint of the offset and in-memory state and emit output value(s) atomically.

In Facebook’s environment, different applications often have different state and output semantics requirements; for example, the Puma application guarantees at-least-once state and output semantics with checkpoints to HBase.

## State-saving mechanisms

The state-saving mechanism for stateful processors determines their fault tolerance. It must allow recovery of the processing state in case of machine failure. Some notable solutions include:

[![](https://substackcdn.com/image/fetch/$s_!ufWy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5650059f-03d8-416d-a921-a57d5d76e97a_1445x500.png)](https://substackcdn.com/image/fetch/$s_!ufWy!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5650059f-03d8-416d-a921-a57d5d76e97a_1445x500.png)

Image created by the author

* Replication: The stateful nodes are replicated with two or more copies. This approach requires more hardware because of node duplication.
* Local database persistence: Apache Samza stores the state in a local database and writes the mutation to Kafka simultaneously.
* Remote database persistence: The processor saves the checkpoint and states it in a remote database.
* Upstream backup: Those systems buffer events in the upstream nodes and replay after a failure.
* Global consistent snapshot: Apache Flink uses a distributed snapshot algorithm to ensure a globally consistent state. After a failure, multiple machines are restored to this consistent snapshot.

Facebook has different demands for fault tolerance for each stream processing system. Puma provides fault tolerance for stateful aggregation, while Stylus provides multiple fault-tolerant solutions for stateful processing.

Their engineer implemented two state-saving mechanisms in Stylus: a local database model and a remote database model. The first model leverages an embedded RocksDB database instance. The processor saves the state to this local database at fixed intervals. RocksDB then asynchronously copies data to HDFS at longer intervals. If the processor fails, it can restore the state from the local database to resume processing. If the machine fails, the processor will use data from HDFS instead.

[![](https://substackcdn.com/image/fetch/$s_!q1oQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2274c980-64f4-4545-a84e-99f2798d7723_957x488.png)](https://substackcdn.com/image/fetch/$s_!q1oQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2274c980-64f4-4545-a84e-99f2798d7723_957x488.png)

Two state-saving mechanisms in Stylus. Image created by the author.

In the remote database model, the processors update the state whenever they receive the event. If the needed state isn’t in memory, it’s fetched from the remote database, modified, and saved back. This process of reading, modifying, and writing can be optimized for monoid processors.

> *A monoid is an algebraic structure that has an identity element (an element when combined with any other element leaves the other element unchanged) and is associative (the order of applied operation does not matter. e.g a+b is the same as b+a)*

For monoid processors, instead of immediately modifying the state from the database directly, processors first apply changes to a default empty state (the identity element). Periodically, the state in memory is combined with the existing state from the database and then saved back to the database. This method can be done less frequently than the direct read-modify-write process, making it more efficient for certain types of state management.

## Backfill processing

There are situations requiring reprocessing data:

* Testing the application against old data.
* When adding a new metric, they want to reprocess old data to generate historical metric data.
* Reprocessing the data to reproduce the bug.

For this requirement, there are a few approaches:

[![](https://substackcdn.com/image/fetch/$s_!vZFV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2c9409cd-2258-4764-8e8c-d5cf19c2f72e_1404x499.png)](https://substackcdn.com/image/fetch/$s_!vZFV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2c9409cd-2258-4764-8e8c-d5cf19c2f72e_1404x499.png)

Backfill options. Image created by the author.

* Stream only: The data from the data transport layer must be retained long enough to replay the input streams for reprocessing.
* Two separate systems: one for batch and one for stream processing. This approach makes it difficult to maintain consistency between the two systems.
* Stream processing systems that can also run in a batch environment: Spark Streaming and Flink are systems designed to work in both environments.

Facebook uses the standard MapReduce framework to read from Hive and run stream processing applications in a batch environment. Puma applications can operate as Hive UDFs (user-defined functions) and UDAFs (user-defined aggregation functions), so the Puma app code remains the same whether it processes streaming or batch data.

Creating a Stylus application generates two binaries: one for streaming and one for batch processing. The batch binary for a stateless processor runs in Hive as a custom mapper, while the batch binary for a general stateful processor runs as a custom reducer, using an aggregation key plus event timestamp.

The following sections will note some lessons learned from Facebook.

## Lesson learned

### Moving fast by leveraging multiple systems

Offering a range of systems with varying performance, fault tolerance, and scalability has worked well with Facebook’s ‘move fast and iterate’ culture. They’ve seen many applications start in Puma or Swift and then transition to Stylus as users needed more control over the application or higher throughput. This approach allows users to quickly deploy a simple application, prove its value, and then invest in developing a more complex and robust system.

### Ease of debugging

Thanks to the persistent Scribe streams, the user can replay data from a specific period, making debugging much more straightforward.

### Ease of deployment

Facebook deploys Laser and Puma apps as a service, while Stylus apps are owned by the individual teams that write them.

Laser apps are easy to set up, deploy, and delete. There is a UI to configure the app: the user chooses the desired configuration, and then the UI returns a single command to deploy and another command to delete the application.

A Puma app update needs to be reviewed. The UI generates a code diff that must be checked. The app is automatically deployed or deleted once the diff is approved and committed.

### Ease of monitoring and operation

In the future, they plan to offer dashboards and alerts that are automatically set up to monitor both Puma and Stylus apps. They also want to enable automatic scaling of these apps based on specific thresholds or conditions.

---

## **Outro**

We’ve just explored the architecture of Facebook’s real-time processing systems and the crucial decisions made by their engineers to achieve high throughput and acceptable latency.

I haven’t had the chance to work on real-time data analytics projects yet, which is why I find reading about how big tech companies handle real-time processing so fascinating.

Now it’s your turn: have you had experience building a real-time analytics project for production? If so, I’d love to hear about your experiences in the comments.

---

## **References**

*[1] Guoqiang Jerry Chen, Janet Wiener, Shridhar Iyer, Anshul Jaiswal, Ran Lei, Nikhil Simha, Wei Wang, Kevin Wilfong, Tim Williamson, Serhat Yilmaz, **[Real-time Data Processing at Facebook](https://research.facebook.com/publications/realtime-data-processing-at-facebook/)** (2016)*

---

## Before you leave

Leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/) or [Email](http://vutrinh2704@gmail.com) if you:

* Are interested in this article and want to discuss it further.
* Would you like to correct any mistakes in this article or provide feedback?

  + This includes writing mistakes like grammar and vocabulary. I happily admit that I'm not so proficient in English :D

[Leave a comment](https://vutr.substack.com/p/how-did-facebook-design-their-real/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
