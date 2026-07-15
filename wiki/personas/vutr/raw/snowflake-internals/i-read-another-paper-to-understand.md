---
title: "I spent 7 hours reading another paper to understand more about Snowflake's internal. Here's what I found."
channel: vutr
author: "Vu Trinh"
published: 2024-03-02
url: https://vutr.substack.com/p/i-read-another-paper-to-understand
paid: false
topics: ["Data Engineering", "Snowflake", "BigQuery", "Data Warehouse"]
tags: [snowflake, https, storage, auto, query, image]
---

# I spent 7 hours reading another paper to understand more about Snowflake's internal. Here's what I found.

*A note from Snowflake's paper: Building an elastic query engine on disaggregated storage.*

> Source: [Open post](https://vutr.substack.com/p/i-read-another-paper-to-understand)

## Topics

[[data-engineering|Data Engineering]] · [[snowflake|Snowflake]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]]

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

[![](https://substackcdn.com/image/fetch/$s_!bxVB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7814dfda-092b-4017-a41b-03a002fba86e_1393x993.png)](https://substackcdn.com/image/fetch/$s_!bxVB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7814dfda-092b-4017-a41b-03a002fba86e_1393x993.png)

Image created by the author

---

> *Table of contents:*
>
> * *Context*
> * *Revisit Snowflake’s System Architecture*
> * *Ephemeral Storage System*
> * *Query Scheduling*
> * *Resource Elasticity*
> * *Multi-tenancy*
> * *Resource Sharing*

---

## Intro

From [my previous blog post on Snowflake design principles](https://open.substack.com/pub/vutr/p/i-spent-another-6-hours-understanding?r=2rj6sg&utm_campaign=post&utm_medium=web), I noted down some insights from the Snowflake paper: [The Snowflake Elastic Data Warehouse](https://event.cwi.nl/lsde/papers/p215-dageville-snowflake.pdf) (2016):

* The three layers of Snowflake architecture: Object Storage, Virtual Warehouse, and Cloud Service.
* Concurrency implementation using Snapshot Isolation.
* Data skipping technique instead of traditional index.
* Handling Semi-structured data effortlessly.

After finishing this blog, I realized that there is [another Snowflake paper which was released in 2020](https://www.usenix.org/system/files/nsdi20-paper-vuppalapati.pdf). The paper gives a closer look at Snowflake’s internal and discusses how a change in cloud infrastructure affects *“many assumptions that guided the design and optimization of Snowflake system.”*

Because I was so excited about this paper, I wrote another blog post about Snowflake design and implementation. (I intended to write on a different topic for this week).

And now, let’s jump on the boat. All the content of the below sections is derived from the paper and crafted by myself (with my illustration).

***Before you read**: I will deliver Snowflake’s knowledge from the paper [Building An Elastic Query Engine on Disaggregated Storage](https://www.usenix.org/system/files/nsdi20-paper-vuppalapati.pdf) and won’t cover additional knowledge from different sources. The paper was released in 2020 and describes Snowflake’s implementation and future directions for some design problems that might be solved or still need to be addressed. Any information about the current state of Snowflake to supplement my article is welcome; besides that, if you find that I have a wrong understanding of some points from the paper, correct me in the comment section or DM me. Thank you in advance for your feedback.*

## Convention

> *Some words are repeated in multiple place, so I will use abbreviations for more convenience. This convention is used based on the paper convention.*

* **CS**: Cloud Service
* **VW**: Virtual Warehouse

---

## Context

Snowflake’s system design has two key ideas:

* Custom-designed storage for intermediate data. (temporary results or data need to be exchanged between operators, e.g., Join..)
* This storage system stores intermediate and cache data (downloaded from persistent storage like S3 to improve performance). With the data cache strategy plus a custom-designed query scheduling mechanism, Snowflake can reduce the additional network load caused by compute-storage separation.

This paper focuses on ephemeral storage system design, query scheduling, elasticity, and efficiently supporting multi-tenancy.

---

## Revisit Snowflake’s **System Architecture**

> *The overall architecture.*

[![](https://substackcdn.com/image/fetch/$s_!2QQ_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbaa255e9-2896-432a-9e6c-8ab668759e47_973x691.png)](https://substackcdn.com/image/fetch/$s_!2QQ_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbaa255e9-2896-432a-9e6c-8ab668759e47_973x691.png)

Image created by the author

Snowflake's overall architecture has four main components

### **Centralized Control via Cloud Services**

* All queries must go through the cloud service for query parsing, optimization, planning, and scheduling. This layer is also responsible for access control, transaction management, and concurrency control. The cloud service layer is designed to be high availability by implementing replication, so just in case one node fails, it will not affect the availability of the whole system.
* CS also tracks the query's progress, collects performance metrics, detects a node failure, and reschedules the query. Once the query is done, the result is returned to the CS, which will then be returned to the end user.

### **Elastic Compute via Virtual Warehouse (VW) abstraction**

* Each VW has multiple cloud virtual machines (AWS EC2, for example). Customers will interact with VW without knowing the detailed implementation below; give the VW size they need, and that’s all !!
* VW can scale based on customer demand, and Snowflake manages a pool of pre-warmed (already up, so remove the machine start-up time whenever the customer needs) EC2 instances to back the scaling process.

### **Elastic Local Ephemeral Storage**

* Intermediate data is generated by query operators and can be accessed from nodes that execute that query. So, this kind of data only needs to persist during the query’s life. Moreover, this data must be accessed in low latency and high throughput.
* With all these characteristics, Snowflake decides to build a distributed ephemeral storage system custom-designed to meet the requirements of intermediate data. The system is co-located with compute nodes in VWs and can scale automatically as nodes are added or removed.

### **Elastic Remote Persistent Storage**

* Snowflake stores all its persistent data in remote and persistent storage (S3, GCS, …). Table data is divided horizontally into large, immutable files similar to blocks in traditional databases.
* In each file, values from individual columns are grouped and compressed. The file also has a header that stores the offset of columns in that file, enabling the system to retrieve only necessary columns when processing data.

---

## **Ephemeral Storage System**

After revisiting the high-level architecture of Snowflake, let go of the exciting part: EphemeralStorage. (Remote Persistent Storage uses existing services like S3, so it might not cause significant system design challenges like the EphemeralStorage; maybe this is why the paper is not going too deep into the Remote Persistent Storage).

### **Storage Architecture and Provisioning**

[![](https://substackcdn.com/image/fetch/$s_!0eWX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff26927f7-a80e-43c0-8a3f-0e271c93d2a0_567x472.png)](https://substackcdn.com/image/fetch/$s_!0eWX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff26927f7-a80e-43c0-8a3f-0e271c93d2a0_567x472.png)

Image created by the author

Snowflake made two essential design decisions in our ephemeral storage system (which stores intermediate and cache data):

* Using both memory and local SSDs, intermediate data will be written as possible to their local memory; when memory is full, data is spilled to local SSDs. Even though the in-memory system can achieve better performance, fitting hundred GBs or TBs of intermediate data into memory is impossible.
* Allowing intermediate data to spill into remote data storage if the local SSD is at full capacity. Spilling intermediate data to S3 instead of other compute nodes helps the system not have to keep track of intermediate data location (which can potentially make the other nodes out of memory and disk memory), and overall, it allows Snowflake to preserve the ephemeral storage system thin and performant.

**Future direction from Snowflake:** They want data intermediate data to fit entirely in memory, or at least in SSDs, and not spill to remote storage. This requires precise resource provisioning. However, provisioning resources while achieving high utilization encounters some challenges:

* The significant diverse resource demands across queries compared to a limited number of available node instances.
* Second, if they could match node hardware resources with query demands, precisely provisioning memory and storage requires a priori knowledge of intermediate data size generated by the query, which is quite impossible.
* Decoupling compute from ephemeral storage can resolve the first challenge. ([Like Google’s Dremel - BigQuery processing engine.](https://open.substack.com/pub/vutr/p/bigquery-processing-engine-shuffle?r=2rj6sg&utm_campaign=post&utm_medium=web))
* However, Snowflake admits the unpredictable intermediate data sizes problem is more complex to resolve.

### **Persistent Data Caching**

Snowflake observes that intermediate data is only needed during the query execution process, so storage and memory capacity need to store immediate data only high at some moment, and the demand space need is low on average.

This allows Snowflake to store cache data besides intermediate data in ephemeral storage. Cache data is downloaded from the persistent S3 base, one of the frequently accessed persistent data files. Snowflake prioritizes the space for the immediate data over cache data. (If you need space for immediate data, Snowflake will discard the cache data; correct me if I’m wrong here.)

[![](https://substackcdn.com/image/fetch/$s_!xBGv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc89c7a76-3a81-4ea4-8735-581f79f20b0e_451x478.png)](https://substackcdn.com/image/fetch/$s_!xBGv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc89c7a76-3a81-4ea4-8735-581f79f20b0e_451x478.png)

Image created by the author

Snowflake decides which input file sets belong to which nodes using consistent hashing over persistent data file names. A simple [LRU (Least Recently Used)](https://en.wikipedia.org/wiki/Cache_replacement_policies#:~:text=Least%20recently%20used%20(LRU)) policy is used to evict persistent data files.

Given the performance gap between our ephemeral storage system (co-located to the compute node) and remote persistent data storage (compute node must communicate through the network), such a caching strategy of persistent data files improves the many queries’s execution time in Snowflake.

For consistency, the data of persistent files in an ephemeral storage system must be consistent with those in the remote persistent data store. Snowflake enforces an ephemeral storage system to act as a [write-through cache](https://en.wikipedia.org/wiki/Cache_(computing)#:~:text=Write%2Dthrough%3A%20write%20is%20done%20synchronously%20both%20to%20the%20cache%20and%20to%20the%20backing%20store.) for persistent data files.

Consistent hashing helps assign cache files to compute nodes, but this can cause moving data around (reshuffle) when scaling up and down the cluster. Snowflake implements a lazy, consistent hashing optimization in our ephemeral storage system that avoids such data reshuffling.

Snowflake implements a lazy, consistent hashing mechanism by exploiting the fact that a copy of cached data is stored at a remote persistent data store. Let’s look at an example here for a better understanding:

[![](https://substackcdn.com/image/fetch/$s_!uqS3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F53edf9db-7f20-4998-a754-a892a3984f01_788x750.png)](https://substackcdn.com/image/fetch/$s_!uqS3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F53edf9db-7f20-4998-a754-a892a3984f01_788x750.png)

Image created by the author

* At t1, the cluster has four nodes: files 1–4 are stored on nodes 1–4 while file 5 is placed on node 1 (node 1 has two files: 1 and 5, while other nodes have one file for each node) and five tasks: Task 1–4 are placed on node 1–4, and task 5 is placed on node 1 (because node 1 also has file 5)
* At time *t1* > *t*0, a node 5 is added to the cluster. Then, instead of immediately reshuffling the files (resulting in File 5 being moved from node 1 to node 5), Snowflake will wait until Task 5 is executed again. When task 5 is scheduled, Snowflake will schedule it on node 5 because consistent hashing will now place file 5 on that node. At this time, file 5 will be read by node 5 directly from the remote persistent store and cached locally. File 5 on node 1 will no longer be accessed and will eventually be evicted from the cache.

As I delivered, lazy consistent hashing prevents data that needs to be reshuffled when resizing the cluster; this helps Snowflake achieve efficient elasticity in the compute layer, which I will cover in the following sections.

**Future direction from Snowflake:** The cache hit rate also depends on the cache size available to the query relative to the amount of persistent data accessed by the query. The cache size depends on both the VW size and the volume of intermediate data generated by the executing queries (Because cache and intermediate data are both stored in ephemeral storage). People from Snowflake said they need more fine-grained analysis to understand more about the two factors that impact cache hit rates.

They also introduce two more technical challenges:

* Scenario when cache data is in need more than the immediate data (as from the above section, we know that Snowflake prioritizes the immediate data over cache data)
* As the appearance of [non-volatile memory](https://en.wikipedia.org/wiki/Non-volatile_memory) plus recent designs on remote ephemeral storage systems mature, the storage hierarchy in the cloud will get increasingly deeper. To leverage this storage hierarchy, Snowflake’s new caching mechanisms are needed to coordinate caching across multiple storage tiers efficiently.

---

## **Query Scheduling**

Now, let’s get into how Snowflake schedules query tasks.

### **Locality-aware task scheduling**

[![](https://substackcdn.com/image/fetch/$s_!Horl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F470d3bd3-2166-4de3-87ca-7109ae8af84a_772x582.png)](https://substackcdn.com/image/fetch/$s_!Horl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F470d3bd3-2166-4de3-87ca-7109ae8af84a_772x582.png)

Image created by the author

* Recall that Snowflake uses consistent hashing on data files’s names to assign cache files to the compute node. Snowflake will schedule the task that operates on a persistent data file to the node on which its file consistently hashes. This is called the locality-aware scheduling mechanism (from the paper)
* As a result of this scheduling mechanism, query parallelism is tightly coupled with consistent hashing of files on nodes. This leads to the query being distributed across all the nodes in the VW. An example from the paper:

  > *For instance, consider a customer with 1 million files worth of persistent data running a VW with ten nodes. Consider two queries, where the first query operates on 100 files, and the second query works on 100,000 files; then, with high likelihood, both queries will run on all the ten nodes because files are consistently hashed onto all the ten nodes.*

### **Work stealing**

[![](https://substackcdn.com/image/fetch/$s_!K7ML!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbfbfe034-8318-4bf8-8d6f-efad05ff51b9_714x462.png)](https://substackcdn.com/image/fetch/$s_!K7ML!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbfbfe034-8318-4bf8-8d6f-efad05ff51b9_714x462.png)

Image created by the author

* Consistent hashing can lead to hotspots where many tasks land in the same compute node. To help overloaded nodes, Snowflake uses work stealing, a strategy that allows a finished-running node to steal a task from the slow node.
* When work stealing occurs, the persistent data files needed to execute the task are read from a remote persistent data store instead of directly from the node at which the task was initially scheduled. This prevents increasing additional burden on an already overloaded node.

**Future direction from Snowflake:**

Schedulers can place tasks onto nodes using two extremes:

[![](https://substackcdn.com/image/fetch/$s_!q3lN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19ff64a3-2980-4e3e-8198-c46fcf6a6194_771x192.png)](https://substackcdn.com/image/fetch/$s_!q3lN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19ff64a3-2980-4e3e-8198-c46fcf6a6194_771x192.png)

Image created by the author

* Place tasks with their cached persistent data (their current implementation); this approach will schedule queries on all nodes (based on consistent hashing); while this minimizes network traffic for reading persistent data, it may lead to increased overhead for intermediate data exchange.
* Place all tasks on a single node. This would remove the need for network transfers for intermediate data exchange but would increase network traffic for persistent data reads.

Snowflake found it helpful to re-design query schedulers that only pick the right set of nodes to balance the two extremes.

---

## **Resource Elasticity**

The Stateless compute layer can be independently scaled thanks to data being stored in persistent storage. Compute elasticity is achieved using a pre-warmed pool of nodes that can be added/removed to/from customer VWs on an on-demand basis. Pre-warmed pool allow providing compute elasticity at the granularity of tens of seconds.

[![](https://substackcdn.com/image/fetch/$s_!ACwf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F348010fe-2550-49e5-a2a4-829739adf605_980x473.png)](https://substackcdn.com/image/fetch/$s_!ACwf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F348010fe-2550-49e5-a2a4-829739adf605_980x473.png)

Image created by the author

On the other hand, storage elasticity is handled by persistent data store services like AWS S3 or Google Cloud Storage.

**Future direction from Snowflake:**

* Achieving elasticity at intra-query granularity, people behind Snowflake would like to support some level of query task-level elasticity during the execution of a query for better utilization.
* Exploring serverless infrastructures such as AWS Lambda, Azure Functions, and Google Cloud Functions provide auto-scaling, high elasticity, and fine-grained billing.

---

## **Multi-tenancy**

Snowflake supports multi-tenancy through the VW abstraction. Each VW operates on an isolated set of nodes with its ephemeral storage system, which allows Snowflake to provide performance isolation to its customers.

The VW abstraction in Snowflake leads to the performance isolation versus utilization tradeoff. VW achieves fairly good average CPU utilization; however, other resources are usually underutilized on average. Some reasons are observed for this case:

> *The variability of resource usage across VW; specifically, we observe that for up to 30% of VW, the standard deviation of CPU usage over time is as large as the mean itself. This results in underutilization as customers tend to provision VWs to meet peak demand. Regarding peak utilization, several of our VWs experience periods of heavy utilization, but such high-utilization periods are not necessarily synchronized across VWs.*

People behind Snowflake are already aware of this performance isolation versus utilization tradeoff, but recent trends (at the time of paper writing) are making them revisit this design. Specially per-second pricing billing from all major cloud vendors has raised exciting challenges.

Previously, in the hourly billing model, as long as at least one customer VW used a particular node from a pre-warmed pool during a one-hour duration, Snowflake could charge that customer for the entire duration. However, with per-second billing, Snowflake cannot charge unused cycles on pre-warmed nodes to any particular customer.

This cost inefficiency encourages Snowflake to move to a sharing-based model, where compute and ephemeral storage resources are shared across customers. In the next section, let's check out some challenges Snowflake has to resolve before moving to the shared architecture.

---

## **Resource Sharing**

Snowflake's observation shows that several customer workloads are bursty at some moment instead of maintaining the busy state all over time, so moving to a shared architecture would enable Snowflake to achieve better resource utilization.

The abstraction of VW is so convenient for the user to operate with, so Snowflake doesn’t want to change that. The people behind Snowflake only want to change the under-the-hood implementation, which is used as a shared resource instead of the isolated nodes.

The challenge is to achieve isolation logical properties while implementing the shared architecture. The two essential resources that need to be isolated in VWs are compute and ephemeral storage.

The centralized task scheduler in Snowflake makes the problem more straightforward when dealing with the compute layer. On the other hand, ephemeral storage systems are more complex; the ultimate goal is to design a shared ephemeral storage system that supports elasticity without sacrificing isolation properties across tenants. It has some challenges following the paper:

* First, because ephemeral storage stores both cached persistent and intermediate data, these entities need to be jointly shared while ensuring cross-tenant isolation. Evicting idle cache entries from one tenant and providing them to other tenants while guaranteeing isolation is hard because we cannot predict when a tenant will access the cache data next.
* The second challenge is achieving elasticity without affecting cross-tenant: Because all cache data in Snowflake are consistently hashed onto the same global address space, scaling up the ephemeral storage would trigger the lazy, consistent hashing process for all tenants. This may result in cache misses and degraded performance. Resolving this challenge would require the ephemeral storage system to provide private address spaces to each tenant and, upon scaling of resources, to reorganize data only for those tenants that have been allocated additional resources.

---

## Outro

Snowflake is doing a fascinating job when helping users operate and interact with it effortlessly. I’ve heard about Snowflake’s convenient interface for a long time but still have not had a chance to use it (in production).

But we can not praise the “outside“ without bringing up the “inside“ of Snowflake. The system architectures and design principles of Snowflake are worth studying. (At least to me). I’ve learned a lot when researching and writing two articles about Snowflake.

Not counting BigQuery, Snowflake currently is the OLAP database, which I spend the most time researching about. I’m not going to compare BigQuery and Snowflake or any OLAP databases; I want to deliver excellent system design lessons or challenge solutions when researching how people build very cool OLAP databases.

Besides that, through articles about Snowflake, I hope to learn more from experts and professionals who use Snowflake more than I do; if you want to discuss or correct some information, please leave a comment.

## Questions still in my head

After finishing this article, I did some additional research from the Snowflake documents, but still found the desired answer to these questions (there is a high chance that I missed some things when reading the documents):

* Does the ephemeral storage still prioritize the intermediate result over the cache data, or has the policy changed, or does Snowflake allow flexibility depending on use cases?
* I read [that the Virtual Warehouse is now hourly billing](https://docs.snowflake.com/en/user-guide/cost-understanding-compute): “Warehouses are only billed for credit usage while running, “but how does Snowflake deal with pre-running machine cost duration in the pre-warm period?
* Does Snowflake support compute resource adjustment during the query execution duration?
* Does the Snowflake currently disaggregate the ephemeral storage and the compute note?

If you know the question or want to discuss it more, please leave a comment or contact me through [Linkedin](https://www.linkedin.com/in/vutr27/) or by [Email](http://vutrinh2704@gmail.com). I will try to look at the document (again) in the meantime.

Now, it’s time to say goodbye, see you next Saturday.

---

***Reference**: [Building An Elastic Query Engine on Disaggregated Storage, 2020](https://www.usenix.org/system/files/nsdi20-paper-vuppalapati.pdf).*

---

## Before you leave

I’m launching a referral program to grow the community by giving you guys valuable gifts whenever you reach a referral milestone. The condition is simple: you refer friends to subscribe to my newsletter, and you will receive a gift based on the number of friends you refer. Here are the reward milestones:

[![](https://substackcdn.com/image/fetch/$s_!lf_-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4c72d52-a2c4-4e24-9714-04e72a4dc087_756x361.png)](https://substackcdn.com/image/fetch/$s_!lf_-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4c72d52-a2c4-4e24-9714-04e72a4dc087_756x361.png)

Now, let’s refer friends and claim exciting rewards ;)

[Refer a friend](https://vutr.substack.com/leaderboard?&referrer_token=1xrjxy&utm_source=post)

---

Leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/) or [Email](http://vutrinh2704@gmail.com) if you:

* Are interested in this article and want to discuss it further.
* Would you like to correct any mistakes in this article or provide feedback?

  + This includes writing mistakes like grammar and vocabulary. I happily admit that I'm not so proficient in English :D

[Leave a comment](https://vutr.substack.com/p/i-read-another-paper-to-understand/comments)

It might take 3 minutes to read, but it took me more than three days to prepare, so it will motivate me greatly if you consider subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
