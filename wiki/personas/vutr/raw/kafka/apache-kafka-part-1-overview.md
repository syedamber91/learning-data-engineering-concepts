---
title: "Apache Kafka - Overview"
channel: vutr
author: "Vu Trinh"
published: 2024-07-06
url: https://vutr.substack.com/p/apache-kafka-part-1-overview
paid: false
topics: ["Data Engineering", "Apache Kafka", "Streaming"]
tags: [kafka, https, auto, message, image, messages]
---

# Apache Kafka - Overview

*The terminology and the architecture.*

> Source: [Open post](https://vutr.substack.com/p/apache-kafka-part-1-overview)

## Topics

[[data-engineering|Data Engineering]] · [[apache-kafka|Apache Kafka]] · [[streaming|Streaming]]

---

> *My name is Vu Trinh, and I am a data engineer.*
>
> *I’m trying to make my life less dull by spending time learning and researching “how it works“ in the data engineering field.*
>
> *Here is a place where I share everything I’ve learned.*
>
> *Not subscribe yet? Here you go:*
>
> [Subscribe now](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!RHVR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3308d4f0-eb14-4b4b-9e37-207b499a5489_1397x1001.png)](https://substackcdn.com/image/fetch/$s_!RHVR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3308d4f0-eb14-4b4b-9e37-207b499a5489_1397x1001.png)

Image created by the author.

---

## Intro

I have wanted to learn Apache Kafka for a while, but I always put it aside because I have higher priority topics to research.

(Such a fancy way to justify the procrastination)

While searching for a topic for this blog post, I finally decided to write about Kafka, which is also a chance to learn about this system seriously.

I plan to write a series of Kafka blog posts that align with my learning process.

This blog is the first part of the series; the scope of this article will cover a high-level overview of Kafka and its usage in LinkedIn’s data infrastructure.

---

## High-level overview

Internet companies like LinkedIn generate vast amounts of log data, including user activity events (like logins, page views, and clicks) and operational metrics (service call latency, errors, or system resource utilization). Traditionally used for tracking user engagement and system performance, this log data is now leveraged for production features such as search relevance, recommendations, and ad targeting.

To deal with LinkedIn’s demands of log processing, the internal development team at LinkedIn, led by [Jay Kreps](https://www.linkedin.com/in/jaykreps/), built a messaging system called [Kafka](https://kafka.apache.org/). The system combines the benefits of traditional log aggregators and publish/subscribe messaging systems. Kafka is designed to offer high throughput and scalability. It provides an API similar to a messaging system and allows applications to consume real-time log events.

> *The publish/subscribe messaging system is a communication model where publishers send messages to a topic without knowing the subscribers. Subscribers will subscribe to the specific topics and receive published messages. This helps decouple the producers and consumers.*

Moreover, at the time of Kafka's development, most existing systems used a “push” model in which the broker pushed data to consumers. The team at LinkedIn found the “pull” model more suitable for their need because the consumer can retrieve the messages at the maximum rate it can afford and avoid being flooded by messages pushed faster than it can handle.

In the following sections, we will examine some of the terminologies so it will be easier to grasp the idea behind Kafka's architecture.

## **Message**

[![](https://substackcdn.com/image/fetch/$s_!fWXX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb2d32567-4593-41db-8e3d-6be8d16ebaa2_485x393.png)](https://substackcdn.com/image/fetch/$s_!fWXX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb2d32567-4593-41db-8e3d-6be8d16ebaa2_485x393.png)

Image created by the author.

The Kafka’s unit of data is called a message. You can think of this as similar to a row or a record from the database world. A message can have an optional piece of metadata called the *key**.*** Internally, the message and the key are just an array of byte. The key can be used if users want more control in partitioning; for example, Kafka can guarantee that messages with the same key will be placed on the same partition using consistent hashing on the key.

A message stored in Kafka doesn’t have an explicit message ID. Instead, each message is addressed by its logical offset. This avoids the overhead of maintaining index structures that map the message IDs to the actual message locations. To compute the offset of the following message, the consumer has to add the length of the current message to its offset.

## **Topics and Partitions**

[![](https://substackcdn.com/image/fetch/$s_!5sE9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F18b54c77-0ba0-4969-8363-70c996103402_482x490.png)](https://substackcdn.com/image/fetch/$s_!5sE9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F18b54c77-0ba0-4969-8363-70c996103402_482x490.png)

Image created by the author.

Messages in Kafka are organized into topics. You can consider it like the table in the database system. A topic can be split into multiple *partitions*.

Partitions are the way that Kafka offers redundancy and scalability. The partition can be hosted on a different server, meaning a topic can be scaled horizontally across multiple servers.

Each partition of a topic corresponds to a logical log. Physically, a log is implemented as a set of segment files of approximately the same size (e.g., 1GB). Whenever a message is written to the partition, the broker appends that message to the last segment file.

## **Producers**

[![](https://substackcdn.com/image/fetch/$s_!t7hg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9e19cadc-53e0-483e-a1f4-9305a4b54145_541x480.png)](https://substackcdn.com/image/fetch/$s_!t7hg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9e19cadc-53e0-483e-a1f4-9305a4b54145_541x480.png)

Image created by the author.

The clients who publish the message to the topics are called producers. The producers will write the message to a particular partition. This is done using the message key and a partitioner to generate a hash of the key and map it to a specific partition. By default, the producer will evenly balance messages to all topic partitions. In some cases, the producer can direct messages to specific partitions. This is achieved by applying a specific partition scheme on the message key.

> *I will dedicate a separate article to discuss Kafka’s producer in the upcoming weeks.*

## **Consumers**

The clients read the message by pulling it from one or more subscribed topics. The consumer will read the messages in the order they were written in the partition. The consumer tracks its consumption using the message offset. If the consumer acknowledges a particular message offset, it implies that the consumer has received all messages before that offset in the partition.

Consumers work as part of a consumer group, one or more consumers working together to consume a topic. The group is designed to ensure that only one consumer will be responsible for each partition. Let’s look for an example; in the following illustration, there is a message topic with four partitions (p0,p1,p2,p3) and consumer groups having three consumers (c0,c1,c2); a possible mapping partitions-consumer is: c0 with p0, c1 with p1, p2, c2 with p3.

[![](https://substackcdn.com/image/fetch/$s_!5-iM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3299fb05-18a5-489b-b3e1-17a7445ddcf3_605x474.png)](https://substackcdn.com/image/fetch/$s_!5-iM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3299fb05-18a5-489b-b3e1-17a7445ddcf3_605x474.png)

Image created by the author.

> *Like the “producers, “I plan to write a whole article for Kafka consumers soon.*

## **Brokers**

The published messages are stored at a set of servers called brokers. The broker receives messages from producers, assigns offsets, and writes them on disk. It also serves consumers by responding to the message fetch requests.

## **Clusters**

Kafka brokers work as part of a *cluster*. One broker will act as the cluster controller within a cluster. The controller is responsible for administrative operations.

In Kafka, replication provides redundancy of messages in the partition, such that one of the followers can take over leadership if a broker fails. All producers must connect to the leader to publish messages, but consumers may fetch from either the leader or one of the followers.

There is a single broker in the cluster who owns a partition. This broker is called the partition's leader. Replicated partitions are assigned to additional brokers, called followers of the partition.

## The architecture

[![](https://substackcdn.com/image/fetch/$s_!fuYT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8a3dc1b6-0c89-488c-92c6-2a19d8f16196_866x582.png)](https://substackcdn.com/image/fetch/$s_!fuYT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8a3dc1b6-0c89-488c-92c6-2a19d8f16196_866x582.png)

Image created by the author.

A Kafka cluster typically consists of multiple brokers. To balance the load, a topic is divided into various partitions, and each broker stores one or more of those partitions. Numerous producers and consumers can publish and retrieve messages at the same time.

After a glimpse of Apache Kafka, the next section will describe how Kafka is used at LinkedIn.

## Kafka at LinkedIn

> *For this section, I refer to a Kafka paper written in 2011, which might not reflect LinkedIn Kafka's current usage.*

[![](https://substackcdn.com/image/fetch/$s_!Mlx8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe55979f1-6d21-4162-92cb-f1490af3f095_1445x971.png)](https://substackcdn.com/image/fetch/$s_!Mlx8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe55979f1-6d21-4162-92cb-f1490af3f095_1445x971.png)

Image created by the author.

At LinkedIn, each data center has a co-located Kafka cluster. Frontend services generate log data and publish it to local Kafka brokers in batches. There was a load-balancer that evenly distributed publish requests. Consumers who retrieve messages from this cluster also run in the same data center.

LinkedIn had a separate Kafka cluster for offline analysis near their Hadoop cluster. This Kafka instance replicates data using embedded consumers to pull data from the main cluster. Data from the offline cluster is used to serve reporting, analysis workload, and ad hoc queries.

LinkedIn engineers developed an auditing system to ensure no data loss. Each message has a timestamp and server name when the message is created. Periodically, the producers create monitoring events that record the number of published messages per topic in a fixed time window. The producers then publish these messages to a separate Kafka topic. Dedicated consumers then count messages per topic and validate them against the monitoring events to ensure correctness.

Data and message offsets are stored in HDFS. The data loading into the Hadoop cluster from Kafka uses a special Kafka input format for MapReduce jobs to read data directly from Kafka.

They chose Avro as the serialization protocol since it is efficient and supports schema evolution. For each message, they store the ID of its Avro schema and the serialized bytes in the payload. This schema ensures compatibility between data producers and consumers. In addition, LinkedIn used a lightweight schema registry service to map the schema ID to the schema.

---

## Outro

Through the article, we just visited the high level of Apache Kafka, its terminology and architecture, and finally saw how LinkedIn uses Kafka internally.

The following article of the series will cover some important Kafka design decisions.

So, see you next week.

---

## **References**

*[1] Jay Kreps, Neha Narkhede, Jun Rao, [Kafka: a Distributed Messaging System for Log Processing](https://www.microsoft.com/en-us/research/wp-content/uploads/2017/09/Kafka.pdf) (2011)*

*[2] Gwen Shapira, Todd Palino, Rajini Sivaram, Krit Petty, [Kafka The Definitive Guide Real-Time Data and Stream Processing at Scale](https://www.confluent.io/resources/ebook/kafka-the-definitive-guide/) (2021)*

---

## Before you leave

Leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/) or [Email](http://vutrinh2704@gmail.com) if you:

* Are interested in this article and want to discuss it further.
* Would you like to correct any mistakes in this article or provide feedback?

  + This includes writing mistakes like grammar and vocabulary. I happily admit that I'm not so proficient in English :D

[Leave a comment](https://vutr.substack.com/p/apache-kafka-part-1-overview/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
