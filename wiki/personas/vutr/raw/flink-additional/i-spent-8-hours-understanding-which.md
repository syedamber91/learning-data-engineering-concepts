---
title: "I spent 8 hours understanding which factors make Flink a robust stream processing engine."
channel: vutr
author: "Vu Trinh"
published: 2026-01-27
url: https://vutr.substack.com/p/i-spent-8-hours-understanding-which
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Kafka", "Apache Spark", "Apache Flink", "Databricks", "Streaming"]
tags: [https, auto, flink, substackcdn, image, fetch]
---

# I spent 8 hours understanding which factors make Flink a robust stream processing engine.

*This article is my 8-mins note of my finding*

> Source: [Open post](https://vutr.substack.com/p/i-spent-8-hours-understanding-which)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-flink|Apache Flink]] · [[databricks|Databricks]] · [[streaming|Streaming]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=185147908)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!PKIS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F81d62645-437a-4d9b-bd18-a9ace2cfb1c2_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!PKIS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F81d62645-437a-4d9b-bd18-a9ace2cfb1c2_2000x1429.png)

---

## Intro

Apache Flink is famous for its true stream processing capability. It’s always the people’s top choice for super-low-latency performance, robust state management, fault tolerance at scale, and tons of other features a stream-processing application needs.

In this week’s article, I try to dive into Flink and explore some of its pillar features that underpin its robustness and reliability, including its cluster-based architecture (tasks are handled on multiple workers), memory management (efficient data representation), network data exchange (robust exchange mechanism), and checkpointing (ensures fault tolerance).

---

## The flow

When defining the processing-data logic, the user must express it in the dataflow paradigm where the program is treated as a directed graph, with nodes representing operators (computations) and edges representing data dependencies.

[![](https://substackcdn.com/image/fetch/$s_!QLOr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feb3f3c2b-c033-4674-97ea-56e059527664_1128x668.png)](https://substackcdn.com/image/fetch/$s_!QLOr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feb3f3c2b-c033-4674-97ea-56e059527664_1128x668.png)

An operator receives data from external sources or upstream operators, performs computations, and delivers the results to destinations, which can be external sinks or downstream operators.

The graph can exist on two levels: a logical and a physical graph.

The logical graph provides a high-level view of the computation logic, while the physical graph (derived from the logical graph by the JobManager, which we will discuss later, along with other Flink setup components) details how the program will be executed.

[![](https://substackcdn.com/image/fetch/$s_!AVnE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fafb6937e-0c5a-481e-8256-ba0486babf94_1192x686.png)](https://substackcdn.com/image/fetch/$s_!AVnE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fafb6937e-0c5a-481e-8256-ba0486babf94_1192x686.png)

Just for illustration purposes, it does not reflect the details of the logical and physical plans in Flink.

In Flink, there is a set of operators for ingesting, transforming, and outputting data streams. An operator can be stateless or stateful. Each could have one or more tasks, which operate on a subset of data in parallel.

The stateless one doesn’t keep any state; the processing event does not depend on historical events. The independence of stateless data processing means that parallelization or restarts are more straightforward, as the engine can freely distribute the data across workers and process it in any order.

[![](https://substackcdn.com/image/fetch/$s_!Jxmw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb258e4a-257b-400e-953f-7fcfd2272ccb_1164x478.png)](https://substackcdn.com/image/fetch/$s_!Jxmw!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffb258e4a-257b-400e-953f-7fcfd2272ccb_1164x478.png)

Stateful operations maintain information about processed data (e.g., an accumulated count). This type is more challenging to parallelize or restart as data must be handled in order and be distributed to the right workers.

> *You can think of the state as a variable that needs to be maintained and updated with new data to produce the final result. For example, the accumulated count needs to be updated with the new “click count” from upcoming events. In the scope of this article, we won’t dive much into the stateful processing in Flink.*

## The architecture

A typical Flink setup includes four components, all of which are JVM processes (like a Spark driver-executors cluster):

[![](https://substackcdn.com/image/fetch/$s_!kXBD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F097473a6-f6ca-4068-a14b-abe48a27771b_1240x918.png)](https://substackcdn.com/image/fetch/$s_!kXBD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F097473a6-f6ca-4068-a14b-abe48a27771b_1240x918.png)

* The **Dispatcher** provides a REST interface for users to submit Flink applications. It also exposes a dashboard to monitor the job executions.
* The **JobManager** (like **Spark’s Driver**) is the master that controls the execution of a Flink application; a different JobManager controls each application.
* Flink has different **ResourceManagers** (like **Spark’s Cluster Manager**) for different resource providers, such as YARN or Kubernetes. This component’s primary responsibility is to manage TaskManager slots, Flink’s processing unit.
* **Task Managers** (like **Spark’s executors**) are Flink workers. There are multiple TaskManagers for a Flink setup. Each provides several slots. The number of slots caps the number of tasks a TaskManager can handle. It can be understood that tasks are executed in a multi-threaded model within a TaskManager.

  [![](https://substackcdn.com/image/fetch/$s_!Gu5N!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4f124fba-3e11-4535-a8d9-cf365d770239_1352x528.png)](https://substackcdn.com/image/fetch/$s_!Gu5N!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4f124fba-3e11-4535-a8d9-cf365d770239_1352x528.png)

  This strategy helps achieve better resource utilization; however, the trade-off is isolation, as tasks on the same TaskManagers cannot access the same resource. If users prioritize isolation, they can configure TaskManagers with a single task slot each.

Here is a typical flow of a Flink application:

[![](https://substackcdn.com/image/fetch/$s_!GQ0D!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96b7d10b-ebb7-4a50-87b3-f777f70528bf_1768x774.png)](https://substackcdn.com/image/fetch/$s_!GQ0D!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96b7d10b-ebb7-4a50-87b3-f777f70528bf_1768x774.png)

* When a TaskManager starts, it registers its slots to the Resource Manager.
* An application is submitted to the Dispatcher.
* The Dispatcher starts the JobManager.

> *An application includes the logical dataflow graph and a JAR file that packs all required dependencies to execute the graph.*

* When the JobManager receives an application, it converts the logical plan into the physical one, which includes tasks that can be executed in parallel.
* After that, the JobManager asks the resource managers for resources (TaskManager slots).
* The ResourceManager instructs the TaskManager with idle slots and offers them to the JobManager. If the ResourceManager does not have enough slots to fulfill the JobManager’s request, it communicates to a resource provider to initiate more TaskManager processes.
* When the JobManager gets the required slots, it distributes tasks from the physical graph to the TaskManager slots.
* TaskManagers start executing the task.
* During execution, the JobManager is also responsible for all actions that require central coordination, such as checkpointing.

Some notes on the task execution of the Task Managers. It can execute multiple tasks simultaneously. These tasks can be:

* The tasks are from the same operator
* The tasks are from a different operator.
* The tasks are from a different application.

## The memory management

Discussing one of the most robust stream processing engines without addressing how it manages memory internally would be incomplete, as this is where data is presented and processed in Flink. The memory management has a significant impact on Flink's low-latency and low-throughput performance.

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=185147908)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

### Custom serialization/deserialization framework

Although a TaskManager is a JVM process, Flink doesn’t store data directly in a Java object (like Spark’s project [Tungsten](https://www.databricks.com/blog/2015/04/28/project-tungsten-bringing-spark-closer-to-bare-metal.html)).

[![](https://substackcdn.com/image/fetch/$s_!hboV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffd5f637a-a6d9-4166-8a5e-f6ac3959aaea_880x570.png)](https://substackcdn.com/image/fetch/$s_!hboV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffd5f637a-a6d9-4166-8a5e-f6ac3959aaea_880x570.png)

The creators developed a custom serialization/deserialization framework for Flink to control the binary representation of data.

[![](https://substackcdn.com/image/fetch/$s_!ySR8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9a51f7c0-90f3-4c0e-a3dd-5f9c9c35291a_942x346.png)](https://substackcdn.com/image/fetch/$s_!ySR8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9a51f7c0-90f3-4c0e-a3dd-5f9c9c35291a_942x346.png)

The goal is to present the physical data more efficiently (JVM objects have significant memory overhead; [a 4-byte string would have over 48 bytes in a JVM object](https://www.databricks.com/blog/2015/04/28/project-tungsten-bringing-spark-closer-to-bare-metal.html)) and allow operations such as comparison or grouping to be executed **directly** on binary data, which significantly boosts performance.

### The MemorySegment

The fundamental unit of memory in Flink is the **MemorySegment**. When Flink processes data in memory, they live in those Segments.

[![](https://substackcdn.com/image/fetch/$s_!fgzg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8f0f04bb-d858-4b68-8b96-f1b718cef6b3_1060x770.png)](https://substackcdn.com/image/fetch/$s_!fgzg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8f0f04bb-d858-4b68-8b96-f1b718cef6b3_1060x770.png)

These are fixed-size memory blocks, typically 32 KB in size. Instead of creating a new Java object for every incoming record, Flink allocates a massive pool of these segments at the TaskManager startup.

[![](https://substackcdn.com/image/fetch/$s_!x42i!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb059ea1a-cfd6-4ea4-86ed-ece6e659b2d0_1124x646.png)](https://substackcdn.com/image/fetch/$s_!x42i!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb059ea1a-cfd6-4ea4-86ed-ece6e659b2d0_1124x646.png)

When the TaskManager is torn down, these Segments are also cleaned up. In other words, the **MemorySegments** are reused throughout the lifetime of the TaskManager, helping Flink reduce garbage collection pressure on the JVM.

The amount of memory used for the MemorySegments allocation is configurable.

## The networking

### Multiplexing

Since Flink is a distributed processing engine, tasks need to exchange data. The TaskManagers are responsible for these processes.

If the two tasks live in the same TaskManager, data exchange is lightweight because they don’t need to communicate over the network; the sender serializes the data into byte buffers and adds them to the queue, and the receiver simply picks them up from the queue and deserializes them to consume the actual data.

[![](https://substackcdn.com/image/fetch/$s_!ZuzB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff610f761-e4e2-410b-b0d0-8de038982ed8_732x730.png)](https://substackcdn.com/image/fetch/$s_!ZuzB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff610f761-e4e2-410b-b0d0-8de038982ed8_732x730.png)

For remote tasks, each connection will have its own TCP channel. However, this might cause the number of connections to blow up due to the involved tasks. For example, 4 tasks in TaskManager A need to pass data to 4 tasks in TaskManager B, resulting in 16 connections.

[![](https://substackcdn.com/image/fetch/$s_!gFGB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1b86753d-7976-4358-aead-a5792bba60e3_1164x588.png)](https://substackcdn.com/image/fetch/$s_!gFGB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1b86753d-7976-4358-aead-a5792bba60e3_1164x588.png)

Thus, Flink multiplexes connections to the same TaskManagers into a single, physical TCP channel. This means that each pair of TaskManagers maintains a TCP connection.

> *In computer networking, multiplexing is a method for combining multiple digital signals into a single signal over a shared medium. [—Source—](https://en.wikipedia.org/wiki/Multiplexing)*

[![](https://substackcdn.com/image/fetch/$s_!yPew!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa03d2857-01b6-4a0e-8a91-b5a6ecb7c1ba_1412x716.png)](https://substackcdn.com/image/fetch/$s_!yPew!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa03d2857-01b6-4a0e-8a91-b5a6ecb7c1ba_1412x716.png)

### Credit-Based Flow Control

In most I/O and networking operations, data is batched and sent to reduce the overhead of processing each record individually.

[![](https://substackcdn.com/image/fetch/$s_!X6dR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F78064647-b774-468f-842c-d86ad53f20e6_1598x784.png)](https://substackcdn.com/image/fetch/$s_!X6dR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F78064647-b774-468f-842c-d86ad53f20e6_1598x784.png)

Flink takes a similar approach: records are accumulated in the network buffer (default: 32KB, which is also a **MemorySegment**) before they are sent to the receiver tasks. Each task will have its own buffers for sending and receiving data.

However, buffering will surely affect the low-latency performance.

Flink implements the **Credit-Based Flow Control** mechanism to deal with this.

The receiving task will notify the sending task about its ready-to-receive buffer slots (the credit)

[![](https://substackcdn.com/image/fetch/$s_!0JaC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F563cd60a-f6ae-4379-9f89-025b9a3ba9fc_1484x482.png)](https://substackcdn.com/image/fetch/$s_!0JaC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F563cd60a-f6ae-4379-9f89-025b9a3ba9fc_1484x482.png)

Then the sending task will send the data as much as possible, within the credit limitations. Alongside the data, the sender also notifies the receiver that its data is ready to be shifted next in the buffer (the backlog)

Then the receiver processes the data from the sender and uses the backlog information from all senders to calculate the credits for each sender.

This strategy helps reduce the latency and increase the throughput. The senders can now send data right after the receiver gives the nod. In addition, the Credit-Based Flow Control optimizes throughput by allowing the receiver to use backlog information to prioritize credits for the busiest senders.

[![](https://substackcdn.com/image/fetch/$s_!-ORp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feb90dd77-cbcd-4160-9b91-4e2270269ad5_1476x1096.png)](https://substackcdn.com/image/fetch/$s_!-ORp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feb90dd77-cbcd-4160-9b91-4e2270269ad5_1476x1096.png)

If one sender is overwhelmed with data (skew), the receiver sees that the sender has a large backlog and allocates more network resources (a larger receiving buffer) to clear it faster.

By giving more "lane space" to the most congested paths, Flink prevents bottlenecks that would otherwise affect global throughput and latency.

---

## Checkpoint process

People do not only expect Flink to be fast and high-throughput, but also reliable; it must run (potentially) non-stop to serve real-time data applications, even in the face of failures.

And failures are inevitable. It’s impossible to prevent failures. The only thing we can do is prepare well enough so that when they happen, we can deal with them gracefully.

Flink prepares for failures through the checkpoint process (and other mechanisms).

> ***Note:** The checkpoint process also contributes to [Flink’s exactly-once delivery guarantees](https://flink.apache.org/2018/02/28/an-overview-of-end-to-end-exactly-once-processing-in-apache-flink-with-apache-kafka-too/).*

Flink achieves fault tolerance by allowing the state and stream positions to be recovered without restarting from the beginning.

[![](https://substackcdn.com/image/fetch/$s_!lPV8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1be441c9-4088-4e88-b28d-6833077a3422_1008x622.png)](https://substackcdn.com/image/fetch/$s_!lPV8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1be441c9-4088-4e88-b28d-6833077a3422_1008x622.png)

The most straightforward approach to taking a checkpoint is:

* Pausing the application
* Checkpointing the current processing stream position.
* If a failure occurs, resume from where the application fails using the information from the checkpoint.

However, this approach is impractical; it requires the whole pipeline to stop before checkpointing, resulting in higher latency. So, Flink must take a different approach.

It uses the Chandy-Lamport algorithm, which does not force the application to pause.

Flink uses a special record called a checkpoint barrier. The JobManager creates the barrier and injects it into the data stream. The barrier contains a checkpoint ID to define the checkpoint it belongs to and split the stream into two parts:

* Preceded-barrier state modifications belong to this checkpoint.
* Followed-barrier state modifications belong to the next checkpoint.

Here is how the checkpoint process in Flink looks:

[![](https://substackcdn.com/image/fetch/$s_!wp4m!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ecd2558-a920-49a1-856e-7c76c51d959c_1946x1000.png)](https://substackcdn.com/image/fetch/$s_!wp4m!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ecd2558-a920-49a1-856e-7c76c51d959c_1946x1000.png)

* The JobManager initiates a checkpoint; it sends a checkpoint barrier with the checkpoint ID to every source operator. (Each operator’s task handles data partition(s), which are simply subsets of data. Each partition has an associated barrier.)
* When a source receives this message, it pauses emitting events to downstreams and triggers a checkpoint of its local state to the state backend. It then broadcasts the barrier to all outgoing partitions.
* The backend notifies the task once it has completed checkpointing the state. The task sends the checkpoint confirmation to the Job Manager.
* After broadcasting the barriers, the source gets back to its regular operation.
* When a connected operator receives the broadcast barrier, it waits for barriers from all its task’s partitions (a task can handle more than one partition) for the checkpoint. Task continues processing data from the partition that did not receive the barrier. On the partition with the barrier, incoming data isn’t processed; instead, it is buffered. This avoids mixing records from before and after the checkpoint barrier.
* When a task receives barriers from all its data partitions, it starts the checkpoint of the state to the local state backend and broadcasts the checkpoint to its downstream tasks.
* Once all partitions’ checkpoint barriers are emitted, the task returns to processing buffered data. When buffered data is processed, the task returns to processing its input stream.
* In the end, the barriers reach the sink task. It also executes the checkpoint process like the above: waiting for all partition barriers, checkpointing their state, and sending confirmation to the JobManager.
* The JobManager only considers the application checkpoint successful once it receives all acknowledgments from all task applications.

---

## Outro

In this article, I tried my best to understand and note down the core designs that contribute most to Apache Flink's robustness. We first discuss Flink’s cluster-based architecture, with the JobManager-TaskManagers as the brain and muscles, and the ResourceManager as the resource broker.

Then we explore how Flink manages memory itself using its custom serialization/deserialization framework and organizing data in MemorySegments.

Next, we discuss Flink’s data exchange processes between local and remote tasks. We learn about buffering, multiplexing, and the Credit-Based Flow Control mechanism, all of which make Flink’s data exchange resource-efficient, low-latency, and high-throughput.

Finally, we see how Flink prepares for failure with a checkpointing strategy that doesn’t require the entire application to be paused during checkpointing.

Thank you for reading this far. See you in my next article.

---

## Reference

*[1] [Flink Official Documentation](https://nightlies.apache.org/flink/flink-docs-master/)*

*[2] Fabian Hueske, Vasiliki Kalavri, [Stream Processing with Apache Flink: Fundamentals, Implementation, and Operation of Streaming Applications](https://www.amazon.com/Stream-Processing-Apache-Flink-Implementation/dp/149197429X) (2019)*

*[3] Flink official blog, [Juggling with Bits and Bytes](https://flink.apache.org/2015/05/11/juggling-with-bits-and-bytes/)*

*[4] Flink official blog, [A Deep-Dive into Flink’s Network Stack](https://flink.apache.org/2019/06/05/a-deep-dive-into-flinks-network-stack/)*
