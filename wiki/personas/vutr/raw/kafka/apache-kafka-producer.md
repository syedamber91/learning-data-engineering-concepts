---
title: "Apache Kafka - Producer"
channel: vutr
author: "Vu Trinh"
published: 2024-07-20
url: https://vutr.substack.com/p/apache-kafka-producer
paid: false
topics: ["Data Engineering", "Apache Kafka", "Streaming"]
tags: [https, auto, image, message, kafka, producer]
---

# Apache Kafka - Producer

*The clients who write*

> Source: [Open post](https://vutr.substack.com/p/apache-kafka-producer)

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

[![](https://substackcdn.com/image/fetch/$s_!Cyl7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F292fd8eb-0e3a-4492-b6e9-e7edd7ab1fe7_1397x1000.png)](https://substackcdn.com/image/fetch/$s_!Cyl7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F292fd8eb-0e3a-4492-b6e9-e7edd7ab1fe7_1397x1000.png)

Image created by the author.

---

## Intro

To continue with Kafka’s learning series, this week, we will learn about Kafka’s producer: the client in charge of writing the message for us.

The article is structured as follows: first, we will provide an overview of the message production process. Next, we will discuss Kafka's message-sending methods, acknowledgment behavior, and partition schemes.

---

## Before we move on

Let's review some of Kafka’s terminology:

* **Broker**: A Kafka server that stores Kafka’s topic.
* **Cluster**: Kafka brokers work as part of a *cluster*
* **Topic**: Messages in Kafka are organized into topics.
* **Partition**: Each topic can be broken down into multiple partitions to help Kafka achieve scalability and redundancy.
* **Leader**: A partition is owned by a single broker in the cluster, called the leader.
* **Followers**: A replicated partition is assigned to different brokers, called partition followers

---

## The message production overview

> *Behind the scenes, when sending the message to the Kafka broker*

[![](https://substackcdn.com/image/fetch/$s_!Ws_C!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faaf3ee45-2a2d-45b2-a348-0247dea1f7c8_1068x665.png)](https://substackcdn.com/image/fetch/$s_!Ws_C!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faaf3ee45-2a2d-45b2-a348-0247dea1f7c8_1068x665.png)

Image created by the author.

When you use the Kafka producer API, there are a few things happen:

* The process begins by creating a ProducerRecord, which must include the message’s value and the destination topic. The ProducerRecord can optionally contain a key, partition, timestamp, and headers.
* Next, the producer will serialize the ProducerRecord’s key and value objects to byte arrays to send over the network.
* If no partition is specified, the data is routed to the partitioner; this component will choose the message’s partition based on the key.
* After knowing the destination topic and partition, the producer adds the record to the batch of messages sent to the same topic and partition.

  > As mentioned in my [previous blog](https://vutr.substack.com/p/apache-kafka-important-designs?r=2rj6sg), Kafka sends messages in batches to achieve larger sequential disk operations and avoid too many small requests, which can harm performance. The Kafka producer tries to accumulate data in memory and sends larger batches in a single request. The batching behavior can be controlled by the [batch’s limit size](https://docs.confluent.io/platform/current/installation/configuration/producer-configs.html#batch-size) or [the waiting time before sending the batch to the Kafka broker](https://docs.confluent.io/platform/current/installation/configuration/producer-configs.html#linger-ms).
* A different thread will send these batches to the appropriate Kafka brokers.
* When the broker receives messages: if successful, it returns a metadata object with the topic, partition, and record offset. If unsuccessful, it returns an error; in this case, the producer may retry sending the message a few times before giving up.

---

## Sending method

> *So, can we control the way we want to send the message?*

### Fire-and-forget

[![](https://substackcdn.com/image/fetch/$s_!aONM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb6d089b5-754d-4927-8ae0-e34aa7f60d74_505x190.png)](https://substackcdn.com/image/fetch/$s_!aONM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb6d089b5-754d-4927-8ae0-e34aa7f60d74_505x190.png)

Image created by the author.

The producer sends a message to the server and doesn’t check if it arrives. In case of errors or timeout, messages will be lost, and the application won’t be notified.

### Synchronously

[![](https://substackcdn.com/image/fetch/$s_!Rw5m!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F26d71f41-be7b-4701-8a5c-c1aad0230264_505x247.png)](https://substackcdn.com/image/fetch/$s_!Rw5m!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F26d71f41-be7b-4701-8a5c-c1aad0230264_505x247.png)

Image created by the author.

Sending a message synchronously allows the producer to catch exceptions if Kafka returns an error or retries fail; the producer sends the message and waits for the response, potentially impacting the performance. Thus, synchronous send is rare in production.

### Asynchronously

[![](https://substackcdn.com/image/fetch/$s_!ciAf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a31cc21-2863-4ca7-a9ed-ab803d12c8ec_505x241.png)](https://substackcdn.com/image/fetch/$s_!ciAf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a31cc21-2863-4ca7-a9ed-ab803d12c8ec_505x241.png)

Image created by the author.

In contrast to the above method, sending all messages without waiting for replies takes almost no time. The producer supports adding a callback to handle errors while executing asynchronous send.

---

## Was the message delivered successfully?

> *“We got your message !“*

The producer exposes the `acks` parameter to let the user determine the successful message delivery criteria. It controls how many partition replicas must receive the record before the producer considers the writer successful. Here are the three values for the `acks` parameter:

* **acks=0:** The producer doesn't wait for a reply from the broker and assumes the message was sent successfully. This setting enables very high throughput. However, the risk of losing data is very high. If the broker doesn't receive the message, the producer won't know; the data… disappears.

[![](https://substackcdn.com/image/fetch/$s_!lZY7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9392a8b2-bddd-4d49-a5d9-b7ccc8609dac_505x232.png)](https://substackcdn.com/image/fetch/$s_!lZY7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9392a8b2-bddd-4d49-a5d9-b7ccc8609dac_505x232.png)

Image created by the author.

* **acks=1:** The producer receives a “yes“ response once the leader gets the message. If the leader can't write the message (e.g., if it crashes before a new leader is elected), the producer receives an error and can retry, reducing data loss risk. However, messages can still be lost if the leader crashes before replication to the new leader.

[![](https://substackcdn.com/image/fetch/$s_!1_EM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb51041c2-3a22-4ca1-b68d-274a17fa11f2_652x477.png)](https://substackcdn.com/image/fetch/$s_!1_EM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb51041c2-3a22-4ca1-b68d-274a17fa11f2_652x477.png)

Image created by the author.

* **acks=all:** The producer gets a “yes“ response only after all replicas receive the message. This mode is the safest, ensuring the message survives even if a broker crashes. However, it increases latency because it waits for all the brokers that hold the replicas to receive the message.

[![](https://substackcdn.com/image/fetch/$s_!T3sU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6772dc43-6952-49bb-9932-bbb24767d319_675x477.png)](https://substackcdn.com/image/fetch/$s_!T3sU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6772dc43-6952-49bb-9932-bbb24767d319_675x477.png)

Image created by the author.

---

## How do we distribute the message?

From the “The message production overview“ section, we know that Kafka messages can optionally have a key, which is null by default. The message’s key is mainly used to decide the message destination partition.

When the key is null, and no custom partitioner is defined, Kafka will use the following:

[![](https://substackcdn.com/image/fetch/$s_!nvQf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fed61bd13-8bc0-4234-8aa7-df86a839f591_772x746.png)](https://substackcdn.com/image/fetch/$s_!nvQf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fed61bd13-8bc0-4234-8aa7-df86a839f591_772x746.png)

Image created by the author.

* **Round-Robin partitioner** (with Kafka version ≤ v2.3): It assigns messages to partitions cyclically, which means it sequentially assigns messages to each partition, one after another, and then starts over again from the first partition.
* **Sticky Partitioner (**with Kafka version≥ 2.4**):** It aims to stick to a particular partition for a batch of records, meaning it tries to send as many records as possible to the same partition until a specific condition is met, such as the batch reaching its limit. Once that condition is met, it switches to another partition and continues.

[![](https://substackcdn.com/image/fetch/$s_!W2cs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc70e452c-72a9-4352-bd35-db28ff77fd71_862x375.png)](https://substackcdn.com/image/fetch/$s_!W2cs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc70e452c-72a9-4352-bd35-db28ff77fd71_862x375.png)

Image created by the author.

If the message’s key is not null, Kafka will hash it with its hash algorithm and use the result to map the message to a particular partition. This means that the same key will be routed to the same partition.

Besides the default partitioner, Kafka lets users define their custom partitioner to tailor their needs.

---

## Outro

To sum up, we have just learned the overview of Kafka producer, its message delivery method, how to ensure the message arrives safely, and how to control the partition scheme.

In the next post, we will continue the Kafka series from the other side of the system: the Consumer.

So, see you next week.

---

## **References**

*[1] Gwen Shapira, Todd Palino, Rajini Sivaram, Krit Petty, [Kafka The Definitive Guide Real-Time Data and Stream Processing at Scale](https://www.confluent.io/resources/ebook/kafka-the-definitive-guide/) (2021)*

---

It might take you five minutes to read, but it took me days to prepare, so it would greatly motivate me if you considered increasing my subscriber count.

[Subscribe now](https://vutr.substack.com/subscribe?)
