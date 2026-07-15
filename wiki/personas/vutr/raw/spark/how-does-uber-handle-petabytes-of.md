---
title: "How does Uber handle petabytes of Spark shuffle data every day?"
channel: vutr
author: "Vu Trinh"
published: 2024-06-22
url: https://vutr.substack.com/p/how-does-uber-handle-petabytes-of
paid: false
topics: ["Apache Spark", "BigQuery", "Streaming"]
tags: [shuffle, uber, spark, https, service, server]
---

# How does Uber handle petabytes of Spark shuffle data every day?

*The Remote External service (RSS)*

> Source: [Open post](https://vutr.substack.com/p/how-does-uber-handle-petabytes-of)

## Topics

[[apache-spark|Apache Spark]] · [[bigquery|BigQuery]] · [[streaming|Streaming]]

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=145445763)

[![](https://substackcdn.com/image/fetch/$s_!HglH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F42e26302-86d9-450a-92b0-9d6df846cbd8_1400x1000.png)](https://substackcdn.com/image/fetch/$s_!HglH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F42e26302-86d9-450a-92b0-9d6df846cbd8_1400x1000.png)

Image created by the author.

---

## Table of contents

* *Apache Spark at Uber*
* *The original shuffle*
* *The new way to think about MapReduce*
* *RSS architecture*

---

## TL;DR

The large scale of Spark shuffle data causes Uber some trouble. To address this, Uber decides to manage shuffle data remotely using Remote Shuffle Service (RSS). The main idea of RSS is to let the Spark executor send shuffle data from the map task to the remote server; then, the reducer will fetch data from there. Moreover, Uber had to reverse the MapReduce paradigm from the original to make the solution more efficient.

---

## Intro

Looking back on my writing history, my first blog is an article on [how BigQuery handles shuffle operations](https://open.substack.com/pub/vutr/p/bigquery-processing-engine-shuffle?r=2rj6sg&utm_campaign=post&utm_medium=web). In that blog, I shared my notes on the exciting approach from Google when they built dedicated in-memory shuffle servers to address Dremel's shuffle challenges; instead of writing the shuffle records to local disks, the Dremel map workers will write its result to a remote server then the `reduce` workers will pull the data from them. Although Google said that this way helps them deal with the shuffle scaling challenge, they did not go into the details of its remote shuffle solutions.

One of the factors that the shuffle operations of Dremel cause trouble to Google is the enormous volume of data they have to process. This made me wonder: “Are there other companies that have to deal with large-scale data that have the same trouble with shuffle operations?”. After researching, I found that Uber has a problem with Spark, just like Google with Dremel. Uber’s article also said they developed a dedicated server to handle Spark shuffle operations. Luckily, the article shows how the solutions work behind the scenes.

This week's article is my note after reading the excellent blog post from Uber: [Highly Scalable and Distributed Shuffle as a Service](https://www.uber.com/en-SG/blog/ubers-highly-scalable-and-distributed-shuffle-as-a-service/).

---

## Apache Spark at Uber

[Spark](https://spark.apache.org/) is Uber's primary computing engine, supporting operations like rides, Uber Eats or Maps. It is crucial for data warehousing, data science, and AI/ML. Uber's Spark usage has grown exponentially, running on over 10,000 production nodes and processing hundreds of petabytes of data daily. Spark jobs now use over 95% of analytics cluster compute resources. Operating Spark at Uber's scale presents challenges despite its benefits, especially with data transfers between job stages, famously known as shuffle. The following section will explore the original Spark shuffle and its significant challenges for Uber.

## The original shuffle

[![](https://substackcdn.com/image/fetch/$s_!tDLZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8f554301-ede6-4d7a-bc7c-fca19056c383_1142x953.png)](https://substackcdn.com/image/fetch/$s_!tDLZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8f554301-ede6-4d7a-bc7c-fca19056c383_1142x953.png)

Image created by the author. [Reference](https://www.uber.com/en-SG/blog/ubers-highly-scalable-and-distributed-shuffle-as-a-service/)

Historically, Spark shuffler has two sets of tasks: `map`and `reduce`*.* The first produces the shuffle data, and the latter consumes it. In Sparks, task exchange shuffles data using pull models. The `Map` tasks write the shuffle data to the local disk. Then, `reduce` tasks reach **multiple** `map` tasks to pull that data.

### Shuffle Write

[![](https://substackcdn.com/image/fetch/$s_!X5JZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3531b837-415f-446b-a37f-a32f9775f218_699x482.png)](https://substackcdn.com/image/fetch/$s_!X5JZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3531b837-415f-446b-a37f-a32f9775f218_699x482.png)

Image created by the author. [Reference](https://www.uber.com/en-SG/blog/ubers-highly-scalable-and-distributed-shuffle-as-a-service/)

The initial Spark shuffle implementation at Uber lets `map` tasks write shuffle data to the executor’s local disk. They first write data to a memory buffer. When the buffer is full, they spill data to disk temporary files. Later, they merge all spill files into the final shuffle files. Uber realized that the process was not optimized. In many cases, they must do multiple disk operations (read and write) on the spill files, which incur the latency.

### Shuffle Read

[![](https://substackcdn.com/image/fetch/$s_!TXvO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdc818347-4940-40b9-be2d-370b7913c0e4_1440x960.gif)](https://substackcdn.com/image/fetch/$s_!TXvO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdc818347-4940-40b9-be2d-370b7913c0e4_1440x960.gif)

Image created by the author. [Reference](https://www.uber.com/en-SG/blog/ubers-highly-scalable-and-distributed-shuffle-as-a-service/)

In the `map` host, multiple data files are coming from many partitions. The host also maintains an index file that keeps the partition offset to track which file belongs to which partition.

The `reduce` tasks talk to the shuffle service running on each mapper host to get the shuffle partition output on that host. When the shuffle service receives the request, it reads the offset from the index file, finds the desired data for the `reduce` task, and returns it. After that, the `reduce` task will pull the data into the memory buffer and then generate the iterator for the reducer process to consume. This process is inefficient because the reducer has to ask many mapper hosts to get a partition’s data, which can incur network overhead and make the mapper hosts do a lot of disk operations.

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=145445763)

---

### The challenge

When Uber operates Spark shuffle at scale, there have been multiple challenges:

* **Hardware Reliability:** Due to the large volumes of shuffle data being written to the SSD daily, Uber disks were worn out faster than the initial design. Instead of being sustained for three years, the disk at Uber wears out in 6 months.
* **Shuffle failure:** when the reducer fetches the data from all mapper tasks on the same machine, the service becomes unavailable, which causes a lot of shuffle failures.
* **Noisy Neighbor Issue:** An application that writes more significant shuffle data will potentially take all the disk space volume in the machine, which causes other applications on this machine to fail due to disk full exceptions.
* **Shuffle Service Unreliability:** Uber user external shuffle service in YARN and Mesos for Spark. They often experienced the shuffle service being unavailable in a set of nodes.

### Uber’s effort to solve the problem

Realizing that storing data locally is one of the root causes of the above issues, Uber tried multiple approaches to storing shuffle data on remote machines:

* **Plugin Different Storage:** They wrote a shuffle manager for Spark that supports different storage plugins and developed plugins to write shuffle files to [HDFS](https://hadoop.apache.org/docs/r1.2.1/hdfs_design.html) or [NFS](https://en.wikipedia.org/wiki/Network_File_System). However, their testing shows the Spark jobs’ run time increased by 2 to 5 times.
* **Streaming Writes:** They built a streaming server that could accept streams from Spark executors. They use HDFS and local storage for the sink destination for those streams; however, job latencies increased by 1.5 to 3 times.

The following sections describe the Spark Remote Shuffle Service (RSS) at Uber.

## The new way to think about MapReduce

After several experiments, Uber figured out that streaming writes from the mapper to the remote servers could solve the problem. However, the performance of this approach can not compare to the current local machine performance (where the `map` task writes data to the local disk). Thus, Uber reversed the map-reduce paradigm for remote writes.

Initially, `map` tasks would write data locally on the machine and then reduce tasks, reaching multiple mapper machines to fetch data for a single partition. This way, reducers spent much time going to each map machine, fetching data, and finally merging them for the `reduce` process.

To implement the Remote Shuffle Service (RSS) for Apache Spark, mappers must write shuffle data to the remote servers. Uber specified that the mapper would write data from the same partition to the unique RSS server, so the reducer would only need to fetch data from one RSS server. By doing this, Uber could mitigate the Spark job latencies on the remote shuffle server because the reducer now doesn’t need to communicate to multiple mappers.

## RSS architecture

[![](https://substackcdn.com/image/fetch/$s_!WZGA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd1f2cc4a-d3e2-43e0-88f5-c6c95b9ef1ce_1536x960.gif)](https://substackcdn.com/image/fetch/$s_!WZGA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd1f2cc4a-d3e2-43e0-88f5-c6c95b9ef1ce_1536x960.gif)

Image created by the author. [Reference](https://www.uber.com/en-SG/blog/ubers-highly-scalable-and-distributed-shuffle-as-a-service/)

Here is the overall architecture of the RSS:

* In RSS, all Spark executors will use clients to talk to the service registry and RSS servers.
* Initially, the Spark driver leverages Zookeeper to identify the unique RSS server instances for the same partitions.
* The drivers pass this information to all mappers and reducers.
* The mappers and reducers use this information to handle the shuffle data process.

### **RSS Client**

RSS has a client-side [jar](https://docs.oracle.com/javase/8/docs/technotes/guides/jar/jarGuide.html) file that implements the shuffle manager interface, which Apache Spark provides. The driver chooses a list of RSS servers to handle the shuffle by querying the service registry. Then, the driver encodes this metadata within the shuffle handle. The Spark machine will pass the shuffle handle (another interface) to map-reduce tasks.

As mentioned above, all the mappers send the shuffle data from a given partition to a single RSS server. So, reducers only need to reach out to a single RSS server to read shuffle data for a given partition.

RSS clients can also specify the replication factor of the shuffle data on multiple RSS servers. Instead of writing to a single server, the mapper will write data to more than one server to add fault tolerance against servers going down.

The entire client is implemented in the shuffle manager interface, so there are no code changes in the Spark codebase. From the view of the Spark job, everything is the same, except that the mappers now need to send the shuffle data to the RSS servers instead of writing to the local disk.

### **Service Registry**

In RSS, a service registry maintains a list of available RSS servers. Uber uses Zookeeper as a service registry. Each RSS server keeps a long-running connection with the ZooKeeper to update its status periodically. During shuffle registering, the Spark driver retrieves the list of all available RSS servers from Zookeepers. Then, the driver picks up the servers based on several factors, such as latency, shuffle partitions, and active connections. After finishing this process, the driver passes the list of available servers to mappers and reducers within the shuffle handle.

This approach requires that each RSS instance register itself to the service registry. The instance is automatically deregistered if it fails and loses its connection to the service registry. The executors communicate with the service registry for the information of available instances and the data shuffle location.

### **Shuffle Manager**

Shuffle Manager in RSS is the component that implements Spark’s shuffle manager interface. It is responsible for selecting and tracking remote shuffle service instances for uploading (mapper) and downloading (reducer) data.

### **RSS Server**

[![](https://substackcdn.com/image/fetch/$s_!HFOF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbc6c26aa-42b3-48d9-b738-44a604994388_1122x1059.png)](https://substackcdn.com/image/fetch/$s_!HFOF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbc6c26aa-42b3-48d9-b738-44a604994388_1122x1059.png)

Image created by the author. [Reference](https://www.uber.com/en-SG/blog/ubers-highly-scalable-and-distributed-shuffle-as-a-service/)

Each mapper writes the shuffle data to unique RSS servers. If there are replicated configurations from the client, the data will be written to more than one server for fault tolerance.

The shuffle data stream is a sequence of shuffle records, where each record has a partition ID and the actual data. When an RSS server receives a shuffle record from a mapper, it chooses the local file based on that partition ID and appends the record to the end of the file.

In RSS servers, a clean-up thread runs on the machine to periodically look for shuffle data that has not been accessed in the last 36 hrs and delete it. Uber limits the total number of concurrent connections per RSS server to guarantee that no RSS server is overloaded.

### **Fault Tolerance**

* **RSS servers busy**: If the clients cannot reach the RSS server, it exponentially backs off retry to avoid burdening the servers.
* **RSS servers restart:** The servers will recover their prior state after restarting by reading the shuffle data files onto the local disk. If map tasks fail under such circumstances, the Spark application will try to reattempt these failed tasks with a new task attempt ID. The RSS server maintains a task attempted in each shuffle record stored in the file. The servers store only the final successful task attempt ID. The reducer will accept only the shuffle records with the last successful attempt.
* **Server Goes Down:** Replication is useful when RSS servers are unavailable. The shuffle data can be served from more than one RSS server. Under such circumstances, if needed, the Spark driver re-schedules the affected mapper/reducer stages.

So, does this help Uber solve the challenges of Spark shuffle? Let’s find out in the following section.

## **Hardware Reliability**

Offloading nearly 10 PB disk writes to remote servers with optimized I/O- hardware with RSS helps Uber improve the wear-out time of the SSD on the YARN cluster from three to thirty-six months. Instead of having a life cycle of 3 months with the original shuffle implementation, SSD disks can now last for nearly three years after onboarding the RSS server.

## **Application Reliability**

After RSS was deployed to production, the failure of the Spark jobs was reduced significantly; the failure rates due to shuffle failures were reduced to almost 95%. Uber also achieves reliability above 99.99% thanks to adding fault tolerance in case RSS servers go down.

## **Scalability**

Currently, RSS at Uber handles nearly 220k applications, with approximately 80k shuffles and 10 PB of data daily. They have production jobs that process almost 40 TBs of data for a single shuffle. RSS can easily handle such large shuffles by getting more RSS servers involved in the shuffle process. This was impossible with Spark’s native external shuffle, which is bound by the disk size for each machine, usually a 1 TB SSD.

---

## Outro

Throughout this article, I’ve documented the key insights from Uber's blog post. We discussed the challenges of Spark's original shuffle operations and then explored how Uber overcame them by introducing the Remote Shuffle Service. The shift to remote writing and reading of shuffle data does introduce the potential for increased latencies, as these operations must now be conducted via the network.

However, this change also brings significant benefits. For instance, the `reduce` worker now only needs to read from one server for its input data, eliminating the need for communication with multiple `map` workers. Moving the shuffled data to local disks opens up numerous engineering opportunities for Uber. For instance, if a `map` worker fails, its processed data remains unaffected as the data is stored remotely on the RSS server.

I think that’s all for this week. Thank you for reading this far.

Now, see you next week.

---

## **References**

*Mayank Bansal, Bo Yang, Mayur Bhosale, Kai Jiang, [Uber’s Highly Scalable and Distributed Shuffle as a Service](https://www.uber.com/en-SG/blog/ubers-highly-scalable-and-distributed-shuffle-as-a-service/) (2022)*

---

## Before you leave

Leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/) or [Email](http://vutrinh2704@gmail.com) if you:

* Are interested in this article and want to discuss it further.
* Would you like to correct any mistakes in this article or provide feedback?

  + This includes writing mistakes like grammar and vocabulary. I happily admit that I'm not so proficient in English :D

[Leave a comment](https://vutr.substack.com/p/how-does-uber-handle-petabytes-of/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
