---
title: "Kafka Migration with Zero-Downtime"
channel: vutr
author: "Vu Trinh"
published: 2025-07-24
url: https://vutr.substack.com/p/kafka-migration-with-zero-downtime
paid: false
topics: ["Data Engineering", "Apache Kafka", "Apache Spark", "Apache Flink"]
tags: [https, auto, kafka, automq, fetch, substackcdn]
---

# Kafka Migration with Zero-Downtime

*From AutoMQ, a cloud-native solution offering 100% Kafka compatibility while storing data entirely on object storage.*

> Source: [Open post](https://vutr.substack.com/p/kafka-migration-with-zero-downtime)

## Topics

[[data-engineering|Data Engineering]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-flink|Apache Flink]]

---

> *I will publish a paid article every Tuesday. I wrote these with one goal in mind: to offer my readers, whether they are feeling overwhelmed when beginning the journey or seeking a deeper understanding of the field, 15 minutes of practical lessons and insights on nearly everything related to data engineering.*
>
> *I invite you to join the club with a **50% discount on the yearly package.** Let’s not be suck as data engineering together.*
>
> [Upgrade subscription](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!E6w2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7bdb81ac-013f-4c36-8472-79ecc7611b7f_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!E6w2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7bdb81ac-013f-4c36-8472-79ecc7611b7f_2000x1428.png)

---

## Intro

In today's data-driven world, Apache Kafka has become an indispensable piece in organizations’ data infrastructure. From processing financial transactions and IoT data to powering user activity tracking and microservices communication, Kafka has become the first choice.

However, as organizations scale, upgrade infrastructure, or optimize costs, the need to migrate Kafka clusters inevitably arises. This could involve transitioning from on-premises deployments to managed cloud services, switching between cloud providers, upgrading to newer Kafka versions, or adopting a more efficient alternative solution.

Such migrations present a unique set of challenges that require a reliable Kafka migration solution to deal with. The core problem lies in Kafka's fundamental role as a central nervous system for data: any disruption can have cascading effects on business continuity.

In this article, we first examine the typical approach of available Kafka migration tools and then explore a refreshing solution from [AutoMQ](https://github.com/AutoMQ/automq?utm_source=vu_kafkalinking) that ensures the migration process can happen without downtime.

To learn more about [AutoMQ](https://github.com/AutoMQ/automq?utm_source=vu_kafkalinking), you can check my previous articles [here](https://vutr.substack.com/t/automq).

---

## Why downtime

[![](https://substackcdn.com/image/fetch/$s_!h86U!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F72b6813d-bcbd-4b40-9a8e-5fb88b9f3787_916x382.png)](https://substackcdn.com/image/fetch/$s_!h86U!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F72b6813d-bcbd-4b40-9a8e-5fb88b9f3787_916x382.png)

Traditional Kafka cluster synchronization tools, such as Kafka’s MirrorMaker 2, focus on replicating data to a separate, target cluster. To ensure no data is lost or processed out of order during the transition, the producers are typically required to stop producing new messages and wait for all remaining messages to settle on the new cluster. Only after that can the producer resume on the new cluster. The consumers also don’t have more messages to consume during the waiting period for the producer.

[![](https://substackcdn.com/image/fetch/$s_!SpgS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5a57f088-f883-4fe8-961c-89c6b61a6c87_1008x618.png)](https://substackcdn.com/image/fetch/$s_!SpgS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5a57f088-f883-4fe8-961c-89c6b61a6c87_1008x618.png)

The most immediate impact is downtime for the applications reliant on the Kafka cluster. During the migration time, producers must stop sending messages; thus, consumers don’t have messages to consume. Furthermore, the "wait" period is inherently **unpredictable and uncontrollable**, as it depends on factors like the volume of data, network latency, and the processing speed of the synchronization tool.

[![](https://substackcdn.com/image/fetch/$s_!nlqy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F733dd185-84b1-40e0-9409-91a757c3e96a_1246x758.png)](https://substackcdn.com/image/fetch/$s_!nlqy!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F733dd185-84b1-40e0-9409-91a757c3e96a_1246x758.png)

This process also introduces considerable **operational complexity and manual overhead**. Teams must carefully orchestrate the stopping and starting of numerous application instances, coordinate across different teams, and often manually verify data consistency before giving the "all clear" for restarts.

This increases the chances of human error and extends the maintenance window. The lack of a native client redirection mechanism introduces complexity that is prone to mistakes and makes the entire migration more risky than necessary, especially for large-scale Kafka deployments with numerous dependent services.

Moreover, [the widely adopted MirrorMaker2 solution doesn't preserve message offsets effectively](https://www.warpstream.com/blog/kafka-replication-without-the-offset-gaps) because it relies on an **imprecise offset mapping** system rather than direct replication. This mapping is not maintained for every single record due to the high cost, which can lead to potential data reprocessing when consumers are migrated.

Furthermore, this offset translation doesn't work for applications like Flink or Spark that manage offsets externally, making MirrorMaker2 unsuitable for seamlessly migrating all Kafka applications.

This means that solutions like MirrorMaker can’t ensure safe migration in every use case.

So, is there a solution that could address all the above problems?

---

## AutoMQ Kafka linking

AutoMQ introduces Kafka Linking for the Kafka-AutoMQ migration purpose. It is the **first** zero-downtime Kafka migration solution in the industry while ensuring message offset preservation. It was built with two key principles in mind: dual write and rolling upgrade.

[![](https://substackcdn.com/image/fetch/$s_!YA40!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F198ea474-1d7f-4d99-ac83-4ec1cf7222ef_978x442.png)](https://substackcdn.com/image/fetch/$s_!YA40!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F198ea474-1d7f-4d99-ac83-4ec1cf7222ef_978x442.png)

Its goal is to ensure a reliable migration process and native client redirection without downtime.

[![](https://substackcdn.com/image/fetch/$s_!jI1H!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdedeff79-7df6-4d75-85b3-cf49347c8d2f_690x374.png)](https://substackcdn.com/image/fetch/$s_!jI1H!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdedeff79-7df6-4d75-85b3-cf49347c8d2f_690x374.png)

> *Currently, the solution only supports Kafka-AutoMQ migration; I personally look forward to the support for Kafka-Kafka migration in the future.*

---

## Dual write

The key to ensuring continuous operation for the Kafka cluster and clients lies in the dual write mechanism. Written data in Kafka will be synced to AutoMQ, and written data in AutoMQ will also be synced back to Kafka, allowing administrators to roll back safely if the migration process encounters problems.

[![](https://substackcdn.com/image/fetch/$s_!n5u5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0f5a3f67-e70a-40b4-b126-dd3da17e4f5d_426x224.png)](https://substackcdn.com/image/fetch/$s_!n5u5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0f5a3f67-e70a-40b4-b126-dd3da17e4f5d_426x224.png)

The AutoMQ’s partition leaders are the ones who handle the migration process. They could act as consumers that pull messages from Kafka’s partition leaders for the Kafka-AutoMQ syncing process. In a different direction, they also produce messages back to Kafka’s partition leaders to ensure dual-write.

For each responsibility, the partition leader will be referred to by different roles:

[![](https://substackcdn.com/image/fetch/$s_!LO9O!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7e27dd5b-fe66-4d75-9fbb-f17b194f24ac_746x410.png)](https://substackcdn.com/image/fetch/$s_!LO9O!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7e27dd5b-fe66-4d75-9fbb-f17b194f24ac_746x410.png)

* Syncing Kafka data to AutoMQ: the fetcher, the AutoMQ’s partition leader, acts as a consumer that fetches data from Kafka.
* Forwarding AutoMQ data to Kafka: the router, the AutoMQ’s partition leader, acts as a producer that publishes data to Kafka.

---

## Kafka → AutoMQ.

To begin the migration process, Kafka Linking requires the source Kafka cluster details, the topics to be migrated, and initial synchronization points (e.g., a complete historical migration, only new data, or at a specific timestamp). AutoMQ will then provision the corresponding topics and partitions within its cluster.

Imagine we have two Kafka topics that need to be migrated:

[![](https://substackcdn.com/image/fetch/$s_!TJyk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6bd22d99-912e-4749-9056-30b6b59cebe2_524x434.png)](https://substackcdn.com/image/fetch/$s_!TJyk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6bd22d99-912e-4749-9056-30b6b59cebe2_524x434.png)

* `topic-1`: with 2 partitions (`topic-1:0`, `topic-1:1`)
* `topic-2`: with 1 partition (`topic-2:0`)

The Kafka Linking continuously monitors the cluster's state. It detects the changes in the partition leader status to ensure AutoMQ is always interacting with the up-to-date partition leader for the migration process. If the leaders change in the source Kafka cluster, this event is immediately detected. The affected partition is then placed into a "pre-processing queue."

[![](https://substackcdn.com/image/fetch/$s_!3V9F!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbf0d5bc7-49a8-4ee4-853e-db3f0b9bc508_630x306.png)](https://substackcdn.com/image/fetch/$s_!3V9F!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbf0d5bc7-49a8-4ee4-853e-db3f0b9bc508_630x306.png)

For the initial setup, the Kafka Link places `topic-1:0`, `topic-1:1,` and `topic-2:0` in the queue. Then it asynchronously pre-processes these in-queue partitions in the background. For each partition, the Kafka Link:

[![](https://substackcdn.com/image/fetch/$s_!UQb3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F78857a20-14a2-40a8-a298-b8d5d03f676e_634x494.png)](https://substackcdn.com/image/fetch/$s_!UQb3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F78857a20-14a2-40a8-a298-b8d5d03f676e_634x494.png)

* Checks its metadata to confirm it's part of the migration and truly needs synchronization from Kafka → AutoMQ.
* Establishes a connection to the Kafka cluster and fetches the partition’s current leader and replica distribution to avoid cross-az traffic when fetching data.
* After that, the AutoMQ partition leaders (in this case, the Fetchers) start pulling data from the associated Kafka partition leaders. AutoMQ also prioritizes fetching data on the same rack. The Fetcher then:

  [![](https://substackcdn.com/image/fetch/$s_!06zQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1d72d5de-7283-409d-8dfa-7e978b1af888_1000x634.png)](https://substackcdn.com/image/fetch/$s_!06zQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1d72d5de-7283-409d-8dfa-7e978b1af888_1000x634.png)

* Determines the partition start offset for the data copying process: If the user chooses `earliest`, it gets the offset of the very first message. Fetcher gets the offset of the current last message if `latest` is selected. With the `timestamp` option, it gets the offset corresponding to that time.
* If a partition is being created in AutoMQ for the first time and the user chooses the `latest` or `timestamp` options, the Fetcher might internally "truncate" the AutoMQ partition to ensure its starting point aligns with the chosen offset from the source.
* The Fetcher continuously builds fetch requests for a partition to send to its respective leaders in the source Kafka cluster.
* Like a regular consumer, Fetcher makes these requests incrementally and only asks for new data since its last successful fetch.

* When the Fetcher receives a response from the source Kafka, it will append the retrieved data to the object storage. If it was a failed response, the Fetcher will retry or take action based on the error type (e.g., requesting the new partition leader if the leader has changed).
* After the partition’s data is successfully appended to AutoMQ's storage, the Fetcher ensures that the subsequent request it sends for this partition will pick up precisely from where it left off, guaranteeing no data is missed and preventing duplication. (like a regular consumer)
* This entire cycle then repeats continuously.

---

## AutoMQ → Kafka

As mentioned, a dual-write mechanism like this enables Kafka Linking to reliably carry out the migration process while keeping clients operational normally. It not only syncs data from Kafka to AutoMQ but also forwards data from AutoMQ back to Kafka:

* When the producers are operating only on Kafka, the data only needs to be synced from Kafka → AutoMQ.

  [![](https://substackcdn.com/image/fetch/$s_!1Bj6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F237ea7a4-a615-4435-b961-f49e885a0444_958x418.png)](https://substackcdn.com/image/fetch/$s_!1Bj6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F237ea7a4-a615-4435-b961-f49e885a0444_958x418.png)
* After rolling upgrade (will be covered soon), some producers start sending messages to AutoMQ, while remaining producers still process data to Kafka. At this time, data also needs to be forwarded from AutoMQ to Kafka.

[![](https://substackcdn.com/image/fetch/$s_!i9oD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0392928b-c961-4188-9cf6-81005284a365_1080x408.png)](https://substackcdn.com/image/fetch/$s_!i9oD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0392928b-c961-4188-9cf6-81005284a365_1080x408.png)

The AutoMQ’s partition leaders (in this case, the Routers) are responsible for the AutoMQ → Kafka message forwarding:

[![](https://substackcdn.com/image/fetch/$s_!zhZL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe9ac803d-ba5d-4553-9e04-5939d481389b_1534x800.png)](https://substackcdn.com/image/fetch/$s_!zhZL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe9ac803d-ba5d-4553-9e04-5939d481389b_1534x800.png)

* The Router first maps the received messages to an **in-memory message map** that allows for efficient processing and, most importantly, **preserves the ordering guarantees.**
* The key for this map is the partition, and the value is a message pool containing all messages pending for sending back to Kafka.
* Within each partition's message pool, messages are further grouped by their source producer.
* Kafka guarantees FIFO (First-In, First-Out) order per producer per partition. By grouping messages by producer within a partition's pool, the Router can strictly ensure that messages from a producer are forwarded in the exact order they were received.
* The Router understands that the messages it receives have often already been grouped into **batches by the original Kafka producer**. It avoids unnecessary re-aggregation of these existing batches for the same partition.
* When it's time to construct a new send request to Kafka, it selects one or more *complete batches* from the relevant partition's message pool.
* When the Router completes constructing requests, it sends them to Kafka and starts creating new requests right away. Batches from different producers could be sent concurrently to improve throughput, while batches from the same producer must be sent sequentially to preserve order.

---

## Rolling upgrade

A rolling upgrade is a software deployment strategy that updates a running system to a new version with minimal or zero downtime and reduced risk. Instead of taking the entire system offline to apply the update, a rolling upgrade works by:

[![](https://substackcdn.com/image/fetch/$s_!9Np3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7cffc582-df73-4fb9-9628-caaa328bd8e3_810x362.png)](https://substackcdn.com/image/fetch/$s_!9Np3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7cffc582-df73-4fb9-9628-caaa328bd8e3_810x362.png)

* **Incremental Replacement:** Updating a small batch or a single instance of the system at a time.
* **Maintaining Service Availability:** During the update, the majority of the system continues to serve requests using the old version.
* **Health Checks and Verification:** Each newly updated instance is checked to ensure it's healthy and functioning correctly before it's allowed to serve live traffic.
* **Gradual Traffic Shift:** Once a new instance is verified, traffic is gradually directed to it, and an old instance can then be safely dropped or updated.
* **Iteration:** This process repeats in batches until all instances are running the new version.
* **Easy Rollback:** If any issues arise during a batch update, the problematic batch can be quickly rolled back to the previous stable version, limiting the impact to a small subset of the system.

AutoMQ's Kafka Linking applies the principle of rolling upgrades to the challenging task of Kafka cluster migration, aiming for proper zero-downtime client transitions.

### Producer Migration

In traditional migrations, administrators stop all producers, wait for the data to sync, and then restart them, pointing them to the new cluster. This causes downtime.

With Kafka Linking, a subset of producers is rolling upgraded to point to the destination AutoMQ cluster at a time. The rest of the producers continue to send messages to the original Kafka cluster.

[![](https://substackcdn.com/image/fetch/$s_!HaZ5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F110d4fd8-f751-4bd7-a1f8-4feecf769239_1248x740.png)](https://substackcdn.com/image/fetch/$s_!HaZ5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F110d4fd8-f751-4bd7-a1f8-4feecf769239_1248x740.png)

When producers are updated to send messages to the AutoMQ cluster, all messages received from these migrated producers are immediately forwarded back to the source Kafka cluster. This ensures admins can safely roll back these producers to the point where they are back in the Kafka cluster.

This ensures the producers continue to send messages (either to the old cluster or via AutoMQ back to the old cluster). No messages are dropped. The Consumers still connect to the source cluster at this phase and continue to consume all messages, regardless of whether they originated directly from the old producers or were forwarded via AutoMQ. This creates a seamless flow where the Kafka source cluster remains the single source of truth for consumption during this phase.

### Consumer Migration

Similar to producers, users perform a rolling upgrade on their consumer applications, one by one or in batches, to point them to the AutoMQ cluster.

Crucially, when a consumer connects to the AutoMQ cluster during this phase, AutoMQ disables reading for that consumer to prevent duplicate data consumption. If AutoMQ immediately allowed reading and the consumer group was still partially active on the source, it could result in consuming messages more than once.

[![](https://substackcdn.com/image/fetch/$s_!wbko!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd755c3f0-dae0-4b17-b793-ca1404cb4d20_858x502.png)](https://substackcdn.com/image/fetch/$s_!wbko!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd755c3f0-dae0-4b17-b793-ca1404cb4d20_858x502.png)

Once all consumers in a specific Consumer Group have been successfully redirected (via rolling upgrade) and are detected as offline from the source cluster, Kafka Linking synchronizes the consumer offset of that Consumer Group from the source cluster. This ensures the AutoMQ-connected consumers can pick up exactly where they left off in the original cluster, preventing duplicates or missed messages.

After that, Kafka linking enables reading for that consumer group. Consumers now connected to AutoMQ can resume consumption seamlessly from the correct offset.

The above process is managed by the AutoMQ control plane. It can monitor the status and automatically promote the consumer group, which makes the process seamless.

### Topic Migration

Once producers and consumers for a specific topic (e.g., topic-a) have fully completed their rolling upgrades and are operating via AutoMQ (meaning producers are forwarding to AutoMQ, which then forwards back to the source, and consumers are reading via AutoMQ after group promotion), the user can manually promote the topic:

[![](https://substackcdn.com/image/fetch/$s_!1lqg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb6a5a734-6736-4610-a860-b96fb13a0fc8_1378x750.png)](https://substackcdn.com/image/fetch/$s_!1lqg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb6a5a734-6736-4610-a860-b96fb13a0fc8_1378x750.png)

* AutoMQ stops copying messages from the source cluster for this topic
* AutoMQ stops forwarding new messages back to the source cluster for this topic
* The AutoMQ cluster now becomes the definitive, standalone cluster for this topic, handling both reads and writes directly without relying on the source cluster.

Other topics can follow the same rolling migration process in batches, ensuring a controlled, zero-downtime transition for the entire Kafka deployment.

---

## Outro

Thank you for reading this far.

In this article, we learn about the typical approach of the available Kafka migration tool, which could cause data downtime and increase operational complexity. Then, we explore the solution from AutoMQ, the Kafka Linking, which guarantees a reliable migration process while keeping related applications operational without downtime.

Now, see you next time.

---

## Reference

*[1] AutoMQ, [Beyond MirrorMaker 2: Kafka Migration with Zero-Downtime](https://www.automq.com/blog/beyond-mm2-kafka-migration-with-zero-downtime) (2025)*
