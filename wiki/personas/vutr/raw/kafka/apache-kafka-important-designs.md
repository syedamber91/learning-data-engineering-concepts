---
title: "Apache Kafka - Important Designs"
channel: vutr
author: "Vu Trinh"
published: 2024-07-13
url: https://vutr.substack.com/p/apache-kafka-important-designs
paid: false
topics: ["Data Engineering", "Apache Kafka", "Streaming"]
tags: [https, kafka, auto, image, message, copy]
---

# Apache Kafka - Important Designs

*Filesystem, Zero-copy, and Batching*

> Source: [Open post](https://vutr.substack.com/p/apache-kafka-important-designs)

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

[![](https://substackcdn.com/image/fetch/$s_!auzF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F88080c69-93ac-4db9-aedd-07208e67c91c_1397x1000.png)](https://substackcdn.com/image/fetch/$s_!auzF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F88080c69-93ac-4db9-aedd-07208e67c91c_1397x1000.png)

Image created by the author.

---

## Intro

As promised in the last article, we will continue learning Apache Kafka this week. In this article, I will present my research on some of Kafka’s important designs: Filesystem, Zero-copy, and Batching.

---

## Kafka use the Filesystem

Before going further, let’s understand the Operating System (OS) page cache concept.

[![](https://substackcdn.com/image/fetch/$s_!JFJF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fca3bf7f8-ad9b-4b33-9413-e8c687353521_863x984.png)](https://substackcdn.com/image/fetch/$s_!JFJF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fca3bf7f8-ad9b-4b33-9413-e8c687353521_863x984.png)

Image created by the author.

Modern OS systems usually borrow unused memory (RAM) portions for page cache. The frequently used disk data is populated to this cache, avoiding touching the disk directly too often. Thus, the system is much faster, mitigating the latency of disk seeks. If some application needs the memory to run, the kernel will take back memory portions used for page cache. This ensures the page cache does not affect the system's performance.

Kafka uses the OS filesystem for data storage, thus also leveraging the kernel page cache mechanism. Rather than trying to keep as much data in memory and flush it to the filesystem when running out of RAM, the OS transfers all data to the page cache before flushing it to the disk.

As a result, this approach helps Kafka simplify the code base because the OS system handles the page cache logic. Moreover, this approach also benefits Kafka given the fact that it was built on the Java Virtual Machine, which has some pain points:

* The [high memory overhead](https://www.javamex.com/tutorials/memory/object_memory_usage.shtml#google_vignette) of stored objects.
* The garbage collector process will be slow when the number of in-heap objects increases.

Leveraging the OS filesystem instead of buffering messages in memory using Java objects, Kafka can avoid the two pain points mentioned above.

---

## Sequential access pattern

After learning that Kafka uses a filesystem for its data storage and caching, you might wonder, “ Because the disk is always slower than RAM, is that going to affect the Kafka performance?”

The key here is the access pattern. There is no doubt that with random access, the disk will be slower than RAM, but it can outperform memory slightly when it comes to sequential access. Let’s take a look at these patterns:

* Random access is a method of retrieving or storing data in which the data can be accessed in any order.
* Sequential access is a method of retrieving or storing data in which the data are accessed in a sequential order.

Kafka is designed to make writing (the producers write data) and reading (the consumers consume data) happen sequentially. Let's find out how they achieve this.

### Write

[![](https://substackcdn.com/image/fetch/$s_!1Trk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb407e991-e2ad-4ceb-b526-54e6e1575e6b_451x466.png)](https://substackcdn.com/image/fetch/$s_!1Trk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb407e991-e2ad-4ceb-b526-54e6e1575e6b_451x466.png)

Image created by the author.

In Kafka, messages are grouped using topic. Each topic is split into multiple partitions. Each partition of a topic corresponds to a logical log. Physically, a log is a set of segment files of approximately the same size (e.g., 1GB). Whenever the producer publishes a message to a partition, the broker will ***append*** the message to the last segment file. At any point, only one active segment file accepts the data write; all files that reach the size limit will be closed, and Kafka will open a new segment file for the subsequent writes.

[Appending at the end of](https://www.geeksforgeeks.org/file-access-methods-in-operating-system/) the segment file ensures that data writing in Kafka happens sequentially.

### Read

[![](https://substackcdn.com/image/fetch/$s_!Pcr2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F112d9d3f-1ace-404f-a83e-704d91bafe1e_858x455.png)](https://substackcdn.com/image/fetch/$s_!Pcr2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F112d9d3f-1ace-404f-a83e-704d91bafe1e_858x455.png)

Image created by the author.

The consumer always consumes messages from a specific partition sequentially. A message stored in Kafka doesn’t have a message ID; each message has a logical offset. This avoids the overhead of maintaining additional index structures that map the message IDs to the physical message locations. Kafka message’s offset is increasing but not consecutive; to retrieve the offset of the following message, it has to add the length of the current message to the current offset (like how array data structure handles random access)

Besides the log files containing actual data, brokers have two additional index files that help locate the needed segment files faster. The first index maps offsets to segment files and positions within the file, allowing brokers to quickly find the message for a given offset. The latter maps timestamps to message offsets; this index is used when searching for messages by timestamp. Kafka uses [memory-mapped file](https://en.wikipedia.org/wiki/Memory-mapped_file) techniques for these index files, which helps Kafka read the index files as if they are located directly in the memory.

[![](https://substackcdn.com/image/fetch/$s_!l5JQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd123d209-60c5-4219-a5f0-37070c87c36f_1400x414.png)](https://substackcdn.com/image/fetch/$s_!l5JQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd123d209-60c5-4219-a5f0-37070c87c36f_1400x414.png)

The segment index maps offsets to their message’s position in the segment log. How Kafka’s Storage Internals Work, by Travis Jeffery (2016). [Source](https://medium.com/the-hoard/how-kafkas-storage-internals-work-3a29b02e026)

When beginning to pull messages, the consumers initially request the broker with the start offset at which they want to start consuming. Then, the broker locates the segment file with the requested message by searching the index file and sending the data back to the consumer. After a consumer receives a message, it computes the offset of the following message to consume and uses it in the subsequent request to the broker.

---

## Zero-copy

Using the filesystem also helps Kafka leverage the zero-copy optimization behind the scenes. It needs to be noted that a zero-copy operation doesn’t mean there are no data copies. It only ensures it does not make unnecessary copies. This optimization was not first invented for Kafka; it just leverages this existing technique from the OS system.

Let’s see the original data transfer flow, and then we will see how things work with zero-copy.

### Original Data Transfer Flow

[![](https://substackcdn.com/image/fetch/$s_!BkE2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0f486424-e4b5-4e20-85e6-888c10fffbf5_985x489.png)](https://substackcdn.com/image/fetch/$s_!BkE2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0f486424-e4b5-4e20-85e6-888c10fffbf5_985x489.png)

Image created by the author.

In the typical flow that reads the file from the disk and transfers it over the network, data is usually copied four times with four context switches between user and kernel modes. The flow will have the following steps:

1. It reads the file content on disk and stores it in the OS page cache (the read buffer). This step requires a context switch from user mode to kernel mode.
2. Data is copied from the read buffer into the application buffer. This requires the context to switch from kernel mode to user mode.
3. Data is then copied to the socket buffer. Once again, this requires switching the context from user to kernel mode.
4. After sending data to the socket buffer, the context is switched back to user mode. It then copies the data from the socket buffer to the [network interface controller](https://en.wikipedia.org/wiki/Network_interface_controller) (NIC).
5. The NIC sends data to the destination.

> *To make it more transparent:*
>
> ***[User mode and kernel mode context switch](https://www.geeksforgeeks.org/user-mode-and-kernel-mode-switching/):** In modern OS, the software operates in user and kernel mode. User mode restricts access to system resources, while the latter allows full access. When a user application needs kernel-level access, such as accessing hardware devices, it makes a system call, asking the OS to switch from user mode to kernel mode. This switching, called context switching, involves saving the current processor state, changing modes, and loading the new state.*
>
> ***[A Network Interface Controller (NIC)](https://en.wikipedia.org/wiki/Network_interface_controller)** manages the interface between a computer and a network, converting data into signals for network transmission and receiving incoming data to be processed by the computer.*
>
> ***[A socket Buffer](https://flylib.com/books/en/3.475.1.30/1/?utm_source=2minutestreaming.beehiiv.com&utm_medium=referral&utm_campaign=zero-copy-basics)** is a memory space used by the kernel to temporarily store incoming and outgoing data packets for a network socket, managing data flow between the application and the network.*

### Zero-copy flow

[![](https://substackcdn.com/image/fetch/$s_!95N8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F28765b14-5c1e-4db9-85db-a7ea538cd62f_985x488.png)](https://substackcdn.com/image/fetch/$s_!95N8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F28765b14-5c1e-4db9-85db-a7ea538cd62f_985x488.png)

Image created by the author.

With the zero-copy optimization, the data is copied directly from the page cache to the socket buffer. In a Unix-based, this technique is handled by a [sendfile()](https://man7.org/linux/man-pages/man2/sendfile.2.html) system call. It will copy data directly from one [file descriptor](https://en.wcikipedia.org/wiki/File_descriptor) to another without transferring data to and from user space when using [read()](https://man7.org/linux/man-pages/man2/read.2.html) and [write()](https://man7.org/linux/man-pages/man2/write.2.html) system calls. Thus, this optimization can help Kafka bypass steps two and three from the original data transfer flow. When Kafka leverages the zero-copy technique, the flow can be summarized as below:

1. The data is copied from the disk to the page cache.
2. Then, the data is copied directly from the page cache to the network controller via the sendfile() call.
3. The NIC sends data to the destination (the consumer).

As a result, the context switch is reduced from four to two, and the data copy isn’t needed to copy to the Kafka application. Besides that, in step one, data is copied into the page cache exactly once and reused when required instead of being moved in memory and copied out to user space every time it is read.

The essential thing is that the Kafka data format on the disk is kept the same throughout, from when the producer sends it to when it is sent from the broker to the consumer. Using the same message format allows Kafka to use zero-copy techniques efficiently and avoid decompressing and recompressing messages.

---

## Batching

Due to using the filesystem at the back, too many small requests from the client to the broker can harm the Kafka performance. To deal with this, the Kafka protocol has a message set abstraction that helps group messages together. This helps mitigate the network roundtrip overhead when sending too many single message requests.

Besides the network performance benefit, batching also helps the broker write the message more efficiently; instead of appending the messages one by one, the broker appends a chunk of messages at once. This allows Kafka to achieve larger sequential disk operations.

Moreover, Kafka supports the compression of batches of messages with an efficient batching format in case the network bandwidth is the bottleneck. A batch of messages can be grouped, compressed, and sent to the broker.

---

## Outro

We’ve just gone through some Kafka design decisions in this article. First, it is backed by an OS filesystem for read/write data. Second, thanks to using the filesystem and keeping the physical data format unchanged, Kafka can leverage the zero-copy technique to make the data transfer more efficient. Finally, we see how batching messages helps Kafka boost overall performance. Next week, we will continue to learn Kafka by diving deep into the producer.

So, see you next week :)

---

## **References**

*[1] [Kafka Official Documentation](https://kafka.apache.org/documentation/)*

*[2] Gwen Shapira, Todd Palino, Rajini Sivaram, Krit Petty, [Kafka The Definitive Guide Real-Time Data and Stream Processing at Scale](https://www.confluent.io/resources/ebook/kafka-the-definitive-guide/) (2021)*

*[3] Wikipedia- [Memory-mapped file](https://en.wikipedia.org/wiki/Memory-mapped_file)*

*[4] Wikipedia - [Page cache](https://en.wikipedia.org/wiki/Page_cache)*

*[5] [Linux ate my ram](https://www.linuxatemyram.com/)*

*[6] Andriy Zabolotnyy, [How Kafka Is so Performant If It Writes to Disk?](https://andriymz.github.io/kafka/kafka-disk-write-performance/#) (2021)*

*[7] Stanislav Kozlovski, [Zero Copy Basics](https://2minutestreaming.beehiiv.com/p/apache-kafka-zero-copy-operating-system-optimization) (2023)*

*[8] Travis Jeffery, [How Kafka’s Storage Internals Work](https://medium.com/the-hoard/how-kafkas-storage-internals-work-3a29b02e026) (2016)*

---

## Before you leave

Leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/) or [Email](http://vutrinh2704@gmail.com) if you:

* Are interested in this article and want to discuss it further.
* Would you like to correct any mistakes in this article or provide feedback?

  + This includes writing mistakes like grammar and vocabulary. I happily admit that I'm not so proficient in English :D

[Leave a comment](https://vutr.substack.com/p/apache-kafka-important-designs/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
