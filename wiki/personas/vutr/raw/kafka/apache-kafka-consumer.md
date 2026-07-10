---
title: "Apache Kafka - Consumer"
channel: vutr
author: "Vu Trinh"
published: 2024-07-27
url: https://vutr.substack.com/p/apache-kafka-consumer
paid: false
topics: ["Data Engineering", "Apache Kafka", "Streaming"]
tags: [consumer, https, auto, kafka, group, consumers]
---

# Apache Kafka - Consumer

*The clients who read*

> Source: [Open post](https://vutr.substack.com/p/apache-kafka-consumer)

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

[![](https://substackcdn.com/image/fetch/$s_!7EgI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1e86514f-e378-4572-9135-436f7b6802b6_1397x1000.png)](https://substackcdn.com/image/fetch/$s_!7EgI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1e86514f-e378-4572-9135-436f7b6802b6_1397x1000.png)

Image created by the author.

---

## Intro

To continue with Kafka’s series, this week, we will learn about Kafka’s consumer: the client in charge of reading the message for us.

This article will explore why Kafka opted for the pull model. Then, we'll dive into consumer groups, group membership, partition assignments, rebalancing, and how consumers track their consumption.

---

## **Pull**

[![](https://substackcdn.com/image/fetch/$s_!CymU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc17db363-dc53-4f40-b432-4c6b00bbb053_650x538.png)](https://substackcdn.com/image/fetch/$s_!CymU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc17db363-dc53-4f40-b432-4c6b00bbb053_650x538.png)

Image created by the author.

When Kafka was developed, other log-based systems, such as [Scribe](https://github.com/facebookarchive/scribe) (from Facebook ) or [Flume](https://flume.apache.org/), followed a push-based model where data is pushed to the consumers. However, LinkedIn engineers found the “pull” model more suitable for their applications because consumers can retrieve the messages at a rate ideal for their capacity, allowing them to manage their workload effectively. The consumer can also avoid being flooded by messages pushed faster than it can manage. The model has the following advantages:

* **Catching-up**: If a consumer falls behind in processing messages, it can catch up at its own pace.
* **Batching**: Consumers can pull batches of messages when ready, enabling efficient data transfer.

A consumer always consumes messages from a particular partition sequentially. If the consumer acknowledges a particular message offset, the broker implies that the consumer has received all the previous messages in the partition. Behind the scenes, the Consumer API is an infinite loop for polling the broker for more data. It will issue asynchronous pull requests to the broker to retrieve the data.

Each request contains the offset of the message from which the consumption begins. The broker will use the offset to seek and return the desired data. After receiving the message, the consumer computes the offset of the following message (using the current message’s length and offset) and uses it for the subsequent pull request.

---

## **Consumer groups**

Suppose you want to read data from a Kafka topic. First, you initiate a consumer object and subscribe to the topic you wish to read. The message flows smoothly from the broker to your consumer. After a while, the producers write more data on the topic, giving your consumer trouble catching the message rate.

It needs some “friends” to share the workload.

[![](https://substackcdn.com/image/fetch/$s_!Clj6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fabef805e-d2ba-4088-a127-ade1945f2add_739x780.png)](https://substackcdn.com/image/fetch/$s_!Clj6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fabef805e-d2ba-4088-a127-ade1945f2add_739x780.png)

Image created by the author.

In Kafka, there is a concept of consumer groups. Each group has one or more consumers that will consume a set of subscribed topics. LinkedIn made a partition in a topic the smallest unit of parallelism, so at any given time, all messages from one partition are consumed only by a single consumer within a consumer group. If the number of consumers in the group is larger than the number of partitions in a topic, some consumers will get no message. Different consumer groups will independently consume the topic.

Consumers in the same group have the same group ID. When a group ID is assigned, any new consumer instance added to the group will automatically receive this same group ID.

Kafka uses the Group Coordinator (one of the brokers chosen for this responsibility; different groups will have different brokers) to balance the load within the group. The coordinator, determined by the group ID, ensures that messages from subscribed topics are evenly distributed among the group members. It also keeps the workload balanced when there are changes in the group membership.

---

## Group Membership

[![](https://substackcdn.com/image/fetch/$s_!s70I!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F27005817-d035-4545-90dc-968a8c46caff_774x456.png)](https://substackcdn.com/image/fetch/$s_!s70I!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F27005817-d035-4545-90dc-968a8c46caff_774x456.png)

Image created by the author.

When a consumer wants to join a group, it sends a “Hey, I want to join the party“ request to the coordinator. The first one who joins the group becomes the leader. The leader gets a list of all active consumers from the coordinator and assigns a subset of partitions to each consumer.

Consumers maintain membership in a consumer group and partition ownership by sending heartbeats to the group coordinator. Consumers use a background thread to send these heartbeats, and as long as the coordinator receives the heartbeat at regular intervals, it assumes the consumer to be alive. If the coordinator does not receive the heartbeats from a consumer, it will consider the consumer unavailable and trigger a rebalancing (which will be covered in the upcoming sections).

If a consumer is unavailable, the group coordinator will take a few seconds to decide it is dead. During those seconds, this consumer won’t process any message from its in-charge partition. The consumer will notify the group coordinator that it is leaving, and the coordinator will immediately trigger a rebalancing. Kafka lets the user control the heartbeat frequency and other consumer configuration parameters.

---

## Partition Assignment

As mentioned in the above section, each member of the consumer group will be assigned partitions to consume. Kafka has the following assignment strategies:

### Range

Range is the default strategy, and it’s applied to each topic independently. It assigns a consecutive subset of partitions from each topic to each consumer. The assignor divides the number of partitions of each topic by the number of consumers to determine the assigned partitions. If it is not evenly divided, the first few consumers will have more partitions (more burden on these instances). Let's see an example for a better understanding:

[![](https://substackcdn.com/image/fetch/$s_!b_WE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F30c24181-b27e-4c34-aa4d-cd4e3d8f9515_695x869.png)](https://substackcdn.com/image/fetch/$s_!b_WE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F30c24181-b27e-4c34-aa4d-cd4e3d8f9515_695x869.png)

Image created by the author.

Imagine we have two topic T1 and T2, each have three partitions: T1: [P1, P2, P3] and T2: [P1, P2, P3] and two consumer in the group: C1, C2. Due to working on each topic independently, we’ll first go with topic T1: there are a total of three partitions and two consumers; thus, the number of partitions assigned to each consumer is 3/2=1; it’s not evenly divided so that C1 (the first consumer) will be assigned one more partition, the process is the same with topic T2

* C1 will have T1[P1, P2] and T2[P1, P2]
* C2 will have T1[P3] and T2[P3]

If the number of consumers is larger than the number of partitions in a topic, some consumers won’t be responsible for any partition.

### Round Robin

[![](https://substackcdn.com/image/fetch/$s_!7K1l!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc6e9176b-1cbd-45f9-9ca5-c59868d9f5aa_695x869.png)](https://substackcdn.com/image/fetch/$s_!7K1l!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc6e9176b-1cbd-45f9-9ca5-c59868d9f5aa_695x869.png)

Image created by the author.

Unlike the range assignor, this strategy works across all the subscribed topics and assigns them to the group’s members sequentially. Let’s go back to the above example with round robin; here’s the in-charge partition list of consumers:

* C1 will have T1-P1, T1-P3, T2-P2
* C2 will have T1-P2, T2-P1, T2-P3

This approach's advantage is that it maximizes the number of consumers used. If we add one more consumer to the group, each consumer will have two partitions. However, this requires a lot of partition movement in case of rebalancing.

### Sticky

This strategy is similar to the round-robin one used at the first assignment, but it is different regarding reassignment. It tries to preserve as many existing assignments as possible when the partition reassignment occurs in the group. Let’s revisit the example we used on previous approaches: two topics, T1: [P1, P1, P3] and T2: [P1, P2, P3], and two consumers in the group: C1 and C2

[![](https://substackcdn.com/image/fetch/$s_!qwSD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc2805675-54fa-4dd8-82f6-1e6d89cba74f_1510x976.png)](https://substackcdn.com/image/fetch/$s_!qwSD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc2805675-54fa-4dd8-82f6-1e6d89cba74f_1510x976.png)

Image created by the author.

* First, it will assign as the round-robin fashion: C1 will have T1-P1, T1-P3, T2-P2, C2 will have T1-P2, T2-P1, T2-P3
* After a while, the consumer C2 is down and is replaced by the C3.
* The reassignment occurs, which only requires taking the partitions in charge by C2 and assigning them to C3. The partitions in-charged by C1 will be left alone, which helps reduce the number of partitions involved in the reassignment.

The strategy has two main goals: achieving a balanced assignment of partitions and minimizing the overhead during rebalancing by keeping as many assignments in place as possible.

### Cooperative Sticky

This strategy is the same as the Sticky Assignor but supports cooperative rebalancing, allowing consumers to continue consuming from partitions that are not reassigned. We will discover the “cooperative rebalancing “ in the next section.

---

## Rebalancing

When the number of consumers changed (member added or member crashed), the remaining group’s consumers started consuming messages from partitions previously in charge by other consumers. The process of moving the partition’s ownership between consumers is called rebalancing. There are two types:

* **Eager rebalancing**: All consumers stop consuming, give up **all** their partition ownership, and rejoin the group to get a brand-new partition assignment. This causes a short amount of unavailability time for the entire consumer group.

[![](https://substackcdn.com/image/fetch/$s_!Fjtv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee556c0a-ceea-42d4-8e92-d4538965fca6_1083x1069.png)](https://substackcdn.com/image/fetch/$s_!Fjtv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee556c0a-ceea-42d4-8e92-d4538965fca6_1083x1069.png)

Image created by the author.

* **Cooperative rebalancing:** This type only moves ownership of a subset of the partitions from one consumer to another and allows consumers to continue handling messages from partitions that are not reassigned. First, the consumer group leader notifies all the consumers in the group that they will **lose ownership of some** **partitions**; next, the consumers stop processing from these partitions and give up their ownership. In the next phase, the group leader assigns the orphaned partitions to the new owners. This approach is processed incrementally a few times until the assignment is stable. The important thing is that it does not require total consumers to stop like the eager type; this is very crucial in large consumer groups.

[![](https://substackcdn.com/image/fetch/$s_!tZff!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F526d90e4-e2b8-4e35-88d6-940d9ff59277_1087x1168.png)](https://substackcdn.com/image/fetch/$s_!tZff!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F526d90e4-e2b8-4e35-88d6-940d9ff59277_1087x1168.png)

Image created by the author.

---

## **Consumption tracking and commit offset**

[![](https://substackcdn.com/image/fetch/$s_!dolb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F59123f81-f1b5-40bc-ac24-dd3c90d1d967_813x353.png)](https://substackcdn.com/image/fetch/$s_!dolb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F59123f81-f1b5-40bc-ac24-dd3c90d1d967_813x353.png)

Image created by the author.

In Kafka, the broker and consumer must agree on the messages consumed. If a broker actively considers a message consumed right after sending it and the consumer crashes, the message is lost and not processed by any instance. In contrast, if the broker waits for the consumer's confirmation before marking the message as consumed, other instances can pre-consume the message if the designated consumer fails to send an acknowledgment.

The unique thing about Kafka is that the consumer does not need to keep track of which message it consumes; instead, it uses the Kafka broker to track the message-consume position. This process of updating the current position between the consumer and broker is called offset commit. The consumer will send a message to inform they have successfully processed messages up to a certain point. The broker will assume that the consumer processes all messages before this point. The broker updates this confirmation message to the internal topic: \_\_consumer\_offsets. Kafka supports the following commit behaviors:

* **Automatic Commit**: Users can configure the option `enable.auto.commit=true` to use this behavior. Kafka consumers can be configured to commit offsets at regular intervals automatically.
* **Manual Offset Committing:** Users can configure the option `enable.auto.commit=false` to use this behavior. Consumers can manually commit offsets to control when commits occur. This behavior can be used with the [commitSync()](https://kafka.apache.org/090/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html#commitSync(java.util.Map)) or [commitAsync()](https://kafka.apache.org/090/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html#commitAsync(org.apache.kafka.clients.consumer.OffsetCommitCallback)). The first is a synchronous commit that will wait until either the commit succeeds or there is an error. The latter is an asynchronous call that will not wait; errors are either passed to the callback or ignored (if the callback is not provided.)

---

## **Outro**

Thank you for reading this far! In this article, I've shared some key points about the Kafka consumer.

By the way, this article marks the last one in my Kafka series; if you think I've missed anything or have additional insights about Kafka, please leave a comment. I'd love to do more research and update the series.

Now, it’s time to say goodbye, see you next week.

---

## **References**

*[1] Confluent Document, [Kafka Consumer Design: Consumers, Consumer Groups, and Offsets](https://docs.confluent.io/kafka/design/consumer-design.html)*

[2] Jay Kreps, Neha Narkhede, Jun Rao, *[Kafka: a Distributed Messaging System for Log Processing](https://notes.stephenholiday.com/Kafka.pdf) (2011)*

*[3] Gwen Shapira, Todd Palino, Rajini Sivaram, Krit Petty, [Kafka The Definitive Guide Real-Time Data and Stream Processing at Scale](https://www.confluent.io/resources/ebook/kafka-the-definitive-guide/) (2021)*

*[4] Conduktor Blog, [Kafka Partition Assignment Strategy](https://www.conduktor.io/blog/kafka-partition-assignment-strategy/) (2022)*

*[5] Redpanda Blog, [Kafka partition strategy](https://redpanda.com/guides/kafka-tutorial/kafka-partition-strategy)*

---

## Before you leave

Leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/) or [Email](http://vutrinh2704@gmail.com) if you:

* Are interested in this article and want to discuss it further.
* Would you like to correct any mistakes in this article or provide feedback?

  + This includes writing mistakes like grammar and vocabulary. I happily admit that I'm not so proficient in English :D

[Leave a comment](https://vutr.substack.com/p/apache-kafka-consumer/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
