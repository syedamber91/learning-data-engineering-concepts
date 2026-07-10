---
title: "If you're learning Kafka, this article is for you"
channel: vutr
author: "Vu Trinh"
published: 2025-05-15
url: https://vutr.substack.com/p/if-youre-learning-kafka-this-article
paid: false
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Kafka", "Apache Spark", "Streaming"]
tags: [https, auto, kafka, message, substackcdn, image]
---

# If you're learning Kafka, this article is for you

*A baseline for your Kafka learning and research.*

> Source: [Open post](https://vutr.substack.com/p/if-youre-learning-kafka-this-article)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[streaming|Streaming]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=162735392)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!f5Cu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f29d7a5-fd96-4bea-a7e7-33edab697c38_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!f5Cu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f29d7a5-fd96-4bea-a7e7-33edab697c38_2000x1429.png)

---

## Intro

Fourteen years ago, LinkedIn built [Kafka](https://kafka.apache.org/) to handle its log processing demands.

The system combines the benefits of traditional log aggregators and publish/subscribe messaging systems. Kafka is designed to offer high throughput and scalability. It provides an API similar to a messaging system and allows applications to consume real-time log events.

Now, you see Kafka everywhere. Over the years, Kafka has continued to evolve with many changes and updates. From the [tiered storage](https://cwiki.apache.org/confluence/display/KAFKA/KIP-405%3A+Kafka+Tiered+Storage) to the [Kraft](https://developer.confluent.io/learn/kraft/) or the [queue](https://cwiki.apache.org/confluence/display/KAFKA/KIP-932%3A+Queues+for+Kafka).

But the core has remained the same since the first day. This article summarizes my learning and research on Kafka, hoping it will help you feel less overwhelmed when entering the Kafka world.

---

## Overview

### Messages

Kafka’s unit of data is called a message. A message can have an optional piece of metadata called the *key**.*** The message and the key are just an array of bytes. The key can be used if users want more control in partitioning; for example, Kafka can guarantee that messages with the same key will be placed on the same partition using consistent hashing on the key.

[![](https://substackcdn.com/image/fetch/$s_!TRk0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F335d0ea2-1f02-4140-9d29-ff5cdf6dfacb_546x424.png)](https://substackcdn.com/image/fetch/$s_!TRk0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F335d0ea2-1f02-4140-9d29-ff5cdf6dfacb_546x424.png)

A message stored in Kafka doesn’t have an explicit message ID. Instead, each message is addressed by its logical offset. This avoids the overhead of maintaining index structures that map the message IDs to the actual message locations. To compute the offset of the following message, the consumer has to add the length of the current message to its offset.

### **Topics and Partitions**

Messages in Kafka are organized into topics. A topic can be split into multiple *partitions*. Partitions are how Kafka offers redundancy and scalability. Each partition can be hosted on a different server, meaning a topic can be scaled horizontally across multiple servers.

[![](https://substackcdn.com/image/fetch/$s_!IvmA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1334651a-5ac0-4a68-af95-95149808a8ac_436x408.png)](https://substackcdn.com/image/fetch/$s_!IvmA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1334651a-5ac0-4a68-af95-95149808a8ac_436x408.png)

Each partition of a topic corresponds to a logical log. Physically, a log is implemented as a set of segment files of approximately the same size (e.g., 1GB). Whenever a message is written to the partition, the broker appends that message to the active segment file.

---

## Designs

### Kafka use the Filesystem

Kafka lets the OS filesystem handle the storage layer. It leverages the kernel page cache mechanism to simplify the design.

[![](https://substackcdn.com/image/fetch/$s_!hgKX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F853d9414-780f-4cb3-9b88-a75c4fa33fda_524x544.png)](https://substackcdn.com/image/fetch/$s_!hgKX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F853d9414-780f-4cb3-9b88-a75c4fa33fda_524x544.png)

Modern OS systems usually borrow unused memory (RAM) portions for page cache. This cache populates frequently used disk data, avoiding touching the disk too often. Thus, the system is much faster, mitigating the latency of disk seeks. If some application needs the memory to operate, the kernel will take back memory portions used for page cache. This ensures the page cache does not affect the system's performance.

Rather than implementing a proprietary cache mechanism, Kafka relies on the OS transferring all data to the page cache before flushing it to the disk. This approach also benefits Kafka, given the fact that it was built on the Java Virtual Machine, which has some pain points:

* The [high memory overhead](https://www.javamex.com/tutorials/memory/object_memory_usage.shtml#google_vignette) of stored objects.
* The garbage collector process will be slow when the number of in-heap objects increases.

### Sequential access pattern

“Because the disk is always slower than RAM, is that going to affect the Kafka performance?”, you might wonder.

The key here is the access pattern. There is no doubt that with random access, the disk will be slower than RAM, but it can outperform memory slightly when it comes to sequential access. Let’s take a look at these patterns:

* Random access is a method of retrieving or storing data in which the data can be accessed in any order.
* Sequential access is a method of retrieving or storing data in which the data are accessed in a sequential order.

Kafka is designed to make writing (the producers write data) and reading (the consumers consume data) happen sequentially.

* **Write**:As mentioned, Kafka manages messages as segment files internally. The broker will ***append*** the message to the last segment. Appending at the end of the segment file ensures that data writing in Kafka happens sequentially.
* **Read:**  The consumer always consumes messages from a specific partition sequentially, with the help of the two index files. The first index maps offsets to segment files and positions within the file, allowing brokers to find the message for a given offset quickly. The latter maps timestamps to message offsets; this index is used when searching for messages by timestamp.

### Zero-copy

Using the filesystem also helps Kafka leverage the zero-copy optimization behind the scenes. A zero-copy operation doesn’t mean there are no data copies; it only ensures it does not make unnecessary copies. This optimization was not first invented for Kafka; it just leverages this existing technique from the OS system.

Initially, when a process reads a file from the disk and transfers it over the network, data is usually copied four times with four [context switches](https://www.geeksforgeeks.org/user-mode-and-kernel-mode-switching/) between user and kernel modes. The flow will have the following steps:

[![](https://substackcdn.com/image/fetch/$s_!Jxp0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0bcc47af-e585-4708-bacc-71654568fd19_1248x670.png)](https://substackcdn.com/image/fetch/$s_!Jxp0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0bcc47af-e585-4708-bacc-71654568fd19_1248x670.png)

1. It reads the file content on disk and stores it in the OS page cache. This step requires a context switch from user mode to kernel mode.
2. Data is copied from the cache into the application buffer. This requires the context to switch from kernel mode to user mode.
3. Data is then copied to the [socket buffer](https://flylib.com/books/en/3.475.1.30/1/?utm_source=2minutestreaming.beehiiv.com&utm_medium=referral&utm_campaign=zero-copy-basics). Once again, this requires switching the context from user to kernel mode.
4. The context is switched back to user mode after sending data to the socket buffer. It then copies the data from the socket buffer to the [network interface controller](https://en.wikipedia.org/wiki/Network_interface_controller) (NIC).
5. The NIC sends data to the destination.

With the zero-copy optimization, the data is copied directly from the page cache to the socket buffer. In a Unix-based system, this technique is handled by a [sendfile()](https://man7.org/linux/man-pages/man2/sendfile.2.html) system call. It will copy data directly from one [file descriptor](https://en.wcikipedia.org/wiki/File_descriptor) to another without transferring data to and from user space when using [read()](https://man7.org/linux/man-pages/man2/read.2.html) and [write()](https://man7.org/linux/man-pages/man2/write.2.html) system calls. Thus, this optimization can help Kafka bypass steps two and three from the original transfer flow:

[![](https://substackcdn.com/image/fetch/$s_!Ge_9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F938001f2-0255-4b6a-a831-c2a88033278f_836x464.png)](https://substackcdn.com/image/fetch/$s_!Ge_9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F938001f2-0255-4b6a-a831-c2a88033278f_836x464.png)

1. The data is copied from the disk to the page cache.
2. Then, the data is copied directly from the page cache to the network controller via the sendfile() call.
3. The NIC sends data to the destination (the consumer).

As a result, the context switch is reduced from four to two, and the data doesn’t need to be copied to the Kafka application.

### Batching

To make the client-broker request more efficient, the Kafka protocol has a message set abstraction that helps group messages together. This helps mitigate the network round-trip overhead when sending too many single message requests.

Batching also helps the broker write the message more efficiently; instead of appending the messages one by one, the broker appends a chunk of messages at once. This allows Kafka to achieve larger sequential disk operations.

Moreover, Kafka supports the compression of batches of messages with an efficient batching format in case the network bandwidth is the bottleneck. A batch of messages can be grouped, compressed, and sent to the broker.

This article is sponsored by **Aiven**. Their proposal, [Apache Kafka® KIP-1150: Diskless Topics](https://fnf.dev/43o0CWY), is poised to be a game changer, aiming to reduce Kafka infrastructure costs by up to 80% through offloading disk replication to object storage. [Learn more about the proposal here](https://fnf.dev/43o0CWY) and leave your feedback to help shape the future of Kafka.

[![](https://substackcdn.com/image/fetch/$s_!Qvmj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c067649-c433-4884-bab2-0d4a266c3f0e_1368x707.png)](https://substackcdn.com/image/fetch/$s_!Qvmj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7c067649-c433-4884-bab2-0d4a266c3f0e_1368x707.png)

---

## Producer

### The flow

When you use the Kafka producer API, a few things happen:

[![](https://substackcdn.com/image/fetch/$s_!Ezx4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F25d1ff9a-265a-4c83-8911-ea3e5ef1b9fa_1030x642.png)](https://substackcdn.com/image/fetch/$s_!Ezx4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F25d1ff9a-265a-4c83-8911-ea3e5ef1b9fa_1030x642.png)

* The process creates a ProducerRecord, including the message’s value and the destination topic. The ProducerRecord can contain a key, partition, timestamp, and headers.
* The producer will serialize the ProducerRecord’s key and value objects to byte arrays to send over the network.
* If no partition is specified, the data is routed to the partitioner; this component will choose the message’s partition based on the key.
* After knowing the destination topic and partition, the producer adds the record to the batch of messages sent to the same topic and partition.
* A different thread will send these batches to the appropriate Kafka brokers.
* When the broker receives messages, if successful, it returns a metadata object with the topic, partition, and record offset. If not, it returns an error; in this case, the producer may retry a few times before giving up.

### Sending method

So, can we control the way we want to send the message? The answer is yes:

* **Fire-and-forget**: The producer sends a message to the server and doesn’t check if it arrives. In case of errors or timeout, messages will be lost, and the application won’t be notified.

  [![](https://substackcdn.com/image/fetch/$s_!BMXh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fea4cb8ad-cc97-42e2-9143-c1c5937579b7_584x228.png)](https://substackcdn.com/image/fetch/$s_!BMXh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fea4cb8ad-cc97-42e2-9143-c1c5937579b7_584x228.png)

* **Synchronously**: Sending a message synchronously allows the producer to catch exceptions if Kafka returns an error or retries fail; the producer sends the message and waits for the response. This method is rare in production because it can impact the performance.

  [![](https://substackcdn.com/image/fetch/$s_!DlgQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa81f3949-73dc-48b3-bdf4-470025f5ab64_564x248.png)](https://substackcdn.com/image/fetch/$s_!DlgQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa81f3949-73dc-48b3-bdf4-470025f5ab64_564x248.png)
* **Asynchronously**: The producers send all messages without waiting for replies. They support adding a callback to handle errors while executing an asynchronous send.

  [![](https://substackcdn.com/image/fetch/$s_!6K95!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffcc5d51d-a419-4d8e-9430-f1599b8cabcc_580x286.png)](https://substackcdn.com/image/fetch/$s_!6K95!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffcc5d51d-a419-4d8e-9430-f1599b8cabcc_580x286.png)

### Was the message delivered successfully?

The producer exposes the `acks` parameter to let the user determine the successful message delivery criteria. It controls how many partition replicas must receive the record before the producer considers the writer successful:

* **acks=0:** The producer doesn't wait for a reply from the broker and assumes the message was sent successfully. This setting enables very high throughput. However, the risk of losing data is very high.

  [![](https://substackcdn.com/image/fetch/$s_!-JvT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F64e2d8ea-da71-4238-a1d7-3be3d3abba46_578x240.png)](https://substackcdn.com/image/fetch/$s_!-JvT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F64e2d8ea-da71-4238-a1d7-3be3d3abba46_578x240.png)
* **acks=1:** The producer receives a “yes“ response once the leader gets the message.

  [![](https://substackcdn.com/image/fetch/$s_!Xcot!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7a777c40-6b20-49b7-aeb0-36d6317d5076_648x474.png)](https://substackcdn.com/image/fetch/$s_!Xcot!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7a777c40-6b20-49b7-aeb0-36d6317d5076_648x474.png)
* **acks=all:** The producer gets a “yes“ response only after all replicas receive the message. This mode is the safest, ensuring the message survives even if a broker crashes. However, it increases latency.

  [![](https://substackcdn.com/image/fetch/$s_!XxQH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1d49348e-3ac3-4b3f-8566-572e7dd59e1e_542x402.png)](https://substackcdn.com/image/fetch/$s_!XxQH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1d49348e-3ac3-4b3f-8566-572e7dd59e1e_542x402.png)

### How do we distribute the message?

Kafka messages can optionally have a key, which is null by default. The message’s key is mainly used to decide the message destination partition. When the key is null, and no custom partitioner is defined, Kafka will use the following:

[![](https://substackcdn.com/image/fetch/$s_!o6uE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c90dedc-346e-45d5-bad3-092d682be57a_1058x968.png)](https://substackcdn.com/image/fetch/$s_!o6uE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c90dedc-346e-45d5-bad3-092d682be57a_1058x968.png)

* **Round-Robin partitioner** (with Kafka version ≤ v2.3): It assigns messages to partitions cyclically. It sequentially assigns messages to each partition, one after another, and then starts again from the first partition.
* **Sticky Partitioner (**with Kafka version≥ 2.4**):** It aims to stick to a particular partition for a batch of records, meaning it tries to send as many records as possible to the same partition until a specific condition is met, such as the batch reaching its limit. Once that condition is met, it switches to another partition and continues.

If the message’s key is not null, Kafka will hash it with a hash algorithm and use the result to map the message to a particular partition. Messages with the same key will be routed to the same partition. Kafka also lets users define their custom partitioner to tailor their needs.

[![](https://substackcdn.com/image/fetch/$s_!-SyL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2b35bdd0-3649-401d-8083-137a2dc6d858_928x408.png)](https://substackcdn.com/image/fetch/$s_!-SyL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2b35bdd0-3649-401d-8083-137a2dc6d858_928x408.png)

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=162735392)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

---

## Consumer

When Kafka was developed, other log-based systems, such as [Scribe](https://github.com/facebookarchive/scribe) (from Facebook) or [Flume](https://flume.apache.org/), followed a push-based model where data is pushed to the consumers. However, LinkedIn engineers found the “pull” model more suitable for their applications because consumers can read the messages at a rate ideal for their capacity, allowing them to manage their workload effectively. The consumer can also avoid being flooded by messages pushed faster than they can manage.

[![](https://substackcdn.com/image/fetch/$s_!kuZ-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb1d8e8aa-8f2f-4e3b-911a-9040062c408b_634x458.png)](https://substackcdn.com/image/fetch/$s_!kuZ-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb1d8e8aa-8f2f-4e3b-911a-9040062c408b_634x458.png)

The model has the following advantages:

* **Catching up**: If a consumer falls behind in processing messages, it can catch up at its own pace.
* **Batching**: Consumers can pull batches of messages when ready, enabling efficient data transfer.

### The request

A consumer always consumes messages from a particular partition sequentially. If the consumer acknowledges a message offset, the broker implies that the consumer has received all the previous partition’s messages from this offset.

The Consumer API is an infinite loop for polling the broker for more data. It will issue asynchronous pull requests to the broker to retrieve the data. Each request contains the offset of the message from which the consumption begins.

The broker will use the offset to seek and return the desired data. After receiving the message, the consumer computes the offset of the following message (using the current message’s length and offset) and uses it for the subsequent pull request.

### **Consumer groups**

Kafka has a concept of consumer groups. Each group has one or more consumers who will consume a set of subscribed topics. LinkedIn made a topic’s partition the smallest unit of parallelism; all messages from one partition are consumed only by a single consumer within a group. If the number of consumers in the group is larger than the number of partitions in a topic, some consumers will get no message.

[![](https://substackcdn.com/image/fetch/$s_!FhuK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb7211252-efdf-4daf-8a5d-8365d306bcdd_868x896.png)](https://substackcdn.com/image/fetch/$s_!FhuK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb7211252-efdf-4daf-8a5d-8365d306bcdd_868x896.png)

Consumers in the same group have the same group ID. When a group ID is assigned, any new consumer instance added to the group will automatically receive this same group ID.

Kafka uses the Group Coordinator (one of the brokers) to balance the load within the group. The coordinator, determined by the group ID, ensures that messages from subscribed topics are evenly distributed among the group members. It also keeps the workload balanced when there are changes in the group membership.

When a consumer wants to join a group, they send a request to the coordinator. The first one to join the group becomes the leader. The leader gets a list of all active consumers from the coordinator and assigns a subset of partitions to each consumer. Consumers maintain membership in a consumer group and partition ownership by sending heartbeats to the group coordinator.

### Partition Assignment

Each member of the consumer group will be assigned partitions to consume. Kafka has the following assignment strategies:

* **Range**: This is the default strategy, and it’s applied to each topic independently. It assigns a consecutive subset of partitions from each topic to each consumer. The assignor divides the number of partitions of each topic by the number of consumers to determine the assigned partitions. If it is not evenly divided, the first few consumers will have more partitions (more burden on these instances).

  [![](https://substackcdn.com/image/fetch/$s_!wLue!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbb12c8d6-7630-4d5a-9ff8-e457f793ff6e_588x492.png)](https://substackcdn.com/image/fetch/$s_!wLue!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbb12c8d6-7630-4d5a-9ff8-e457f793ff6e_588x492.png)
* **Round Robin**: This strategy works across all the subscribed topics and assigns them to the group’s members sequentially. This approach's advantage is that it maximizes the number of consumers used. If we add one more consumer to the group, each consumer will have two partitions. However, this requires a lot of partition movement in case of rebalancing.

  [![](https://substackcdn.com/image/fetch/$s_!4e_x!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F217be28a-d843-4dcd-85d3-f69ecc85a79f_576x496.png)](https://substackcdn.com/image/fetch/$s_!4e_x!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F217be28a-d843-4dcd-85d3-f69ecc85a79f_576x496.png)
* **Sticky**: This strategy is similar to the round-robin one used at the first assignment, but is different regarding reassignment. It tries to preserve as many existing assignments as possible when the partition reassignment occurs in the group. The strategy has two main goals: achieving a balanced assignment of partitions and minimizing the overhead during rebalancing by keeping as many assignments in place as possible.

[![](https://substackcdn.com/image/fetch/$s_!TxE-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F20656751-f3bd-4d46-a973-367ba7433475_1816x806.png)](https://substackcdn.com/image/fetch/$s_!TxE-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F20656751-f3bd-4d46-a973-367ba7433475_1816x806.png)

### Rebalancing

When the number of consumers changed (a member added or a member crashed), the remaining group’s consumers started consuming messages from partitions previously assigned to other consumers. The process of moving the partition’s ownership between consumers is called rebalancing. There are two types:

* **Eager rebalancing**: All consumers stop consuming, give up **all** their partition ownership, and rejoin the group to get a brand-new partition assignment. This causes a short amount of unavailability time for the entire consumer group.
* **Cooperative rebalancing:** This type only moves ownership of a subset of the partitions from one consumer to another and allows consumers to continue handling messages from partitions that are not reassigned.

### **Consumption tracking and commit offset**

The unique thing about Kafka is that the consumer does not need to keep track of which message it consumes; instead, it uses the broker to track the message-consumed position. This process of updating the current position between the consumer and broker is called offset commit. The consumer will send a message to inform them that they have successfully processed messages up to a certain point. The broker will assume that the consumer processes all messages before this point. The broker updates this confirmation message to an internal topic.

---

## The object storage trend

We learned that the Kafka design relies on the OS page cache for the storage system. This means compute and storage are tightly coupled. We can’t scale these two components independently. Scaling storage always requires adding more machines, leading to inefficient resource usage.

The design of this share-nothing architecture made sense since, in the past, networks were not as fast as they are now, and local data centers were more common than cloud resources. However, in the cloud era, Kafka’s design makes it hard to leverage the pay-as-you-go pricing. In addition, a Kafka setup could have high cross-availability-zone transfer costs due to Kafka data replication.

Although the initial designs make Kafka a very high-throughput and reliable system, it might not fit well with the cloud era. Many efforts are being made to solve these challenges. The early one is the tiered storage proposal from Uber, which allows Kafka to store messages in a two-tiered storage system:

* Local storage (broker disk) stores the most recent data.
* Remote storage (HDFS/S3/GCS) stores historical data.

However, brokers are not entirely stateless. Replication still happens, and messages still need to be moved around when the cluster’s membership changes.

Until recently, the trend of using object storage for Kafka has been emerging, from WarpStream, AutoMQ, Bufstream, to Redpanda. They made Kafka operate directly on object storage.

This approach has many benefits. Object storage is cheaper, compute and storage are separate, and data replication is eliminated because object storage ensures data availability and durability.

Recently, [Aiven](https://aiven.io/) introduced a very powerful feature with the [KIP-1150](https://lists.apache.org/thread/ljxc495nf39myp28pmf77sm2xydwjm6d), which would forever change how we operate the open-source Kafka deployment. The KIP proposes a new class of topics in Apache Kafka that delegates replication to object storage. Users can tell Kafka to store data from a particular topic, whether on disk or in object storage.

---

## Outro

Thank you for reading this far.

In this article, we explored Kafka’s basics, its technical designs, how the producer and consumer interact with the broker, and finally, a glimpse into the current trend of using object storage to deal with Kafka's limitations when operating on the cloud.

Now, see you in my next article.

---

## Reference

*[1] Jay Kreps, Neha Narkhede, Jun Rao, [Kafka: a Distributed Messaging System for Log Processing](https://www.microsoft.com/en-us/research/wp-content/uploads/2017/09/Kafka.pdf) (2011)*

*[2] Gwen Shapira, Todd Palino, Rajini Sivaram, Krit Petty, [Kafka The Definitive Guide Real-Time Data and Stream Processing at Scale](https://www.confluent.io/resources/ebook/kafka-the-definitive-guide/) (2021)*

*[3] [Kafka Official Documentation](https://kafka.apache.org/documentation/)*

*[4] Wikipedia - [Memory-mapped file](https://en.wikipedia.org/wiki/Memory-mapped_file)*

*[5] Wikipedia - [Page cache](https://en.wikipedia.org/wiki/Page_cache)*

*[6] [Linux ate my ram](https://www.linuxatemyram.com/)*

*[7] Andriy Zabolotnyy, [How Kafka Is so Performant If It Writes to Disk?](https://andriymz.github.io/kafka/kafka-disk-write-performance/#) (2021)*

*[8] Stanislav Kozlovski, [Zero Copy Basics](https://2minutestreaming.beehiiv.com/p/apache-kafka-zero-copy-operating-system-optimization) (2023)*

*[9] Travis Jeffery, [How Kafka’s Storage Internals Work](https://medium.com/the-hoard/how-kafkas-storage-internals-work-3a29b02e026) (2016)*

*[10] Confluent Document, [Kafka Consumer Design: Consumers, Consumer Groups, and Offsets](https://docs.confluent.io/kafka/design/consumer-design.html)*

*[11] Conduktor Blog, [Kafka Partition Assignment Strategy](https://www.conduktor.io/blog/kafka-partition-assignment-strategy/) (2022)*

*[12] Redpanda Blog, [Kafka partition strategy](https://redpanda.com/guides/kafka-tutorial/kafka-partition-strategy)*

*[13] Filip Yonov, [Diskless Kafka: 80% Leaner, 100% Open](https://fnf.dev/43o0CWY) (2025)*
