---
title: "I spent 7 hours learning Amazon S3"
channel: vutr
author: "Vu Trinh"
published: 2025-08-12
url: https://vutr.substack.com/p/amazon-s3-for-data-engineers
paid: true
topics: ["Data Engineering", "Apache Kafka", "Apache Iceberg", "Delta Lake", "Data Warehouse", "Data Lake", "Lakehouse", "Streaming"]
tags: [https, auto, storage, object, good, media]
---

# I spent 7 hours learning Amazon S3

*S3 for data engineers: what it is, why it's popular in data engineering, and how to use it effectively. These insights can also help you work with other object storage services.*

> Source: [Open post](https://vutr.substack.com/p/amazon-s3-for-data-engineers)

## Topics

[[data-engineering|Data Engineering]] · [[apache-kafka|Apache Kafka]] · [[apache-iceberg|Apache Iceberg]] · [[delta-lake|Delta Lake]] · [[data-warehouse|Data Warehouse]] · [[data-lake|Data Lake]] · [[lakehouse|Lakehouse]] · [[streaming|Streaming]]

---

> *I will publish a paid article every Tuesday. I wrote these with one goal in mind: to offer my readers, whether they are feeling overwhelmed when beginning the journey or seeking a deeper understanding of the field, 15 minutes of practical lessons and insights on nearly everything related to data engineering.*
>
> *I invite you to join the club with a **50% discount on the yearly package.** Let’s not be suck as data engineering together.*
>
> [Upgrade subscription](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!jFEl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe433d752-70f7-4e4a-91cd-d1a013b9e905_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!jFEl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe433d752-70f7-4e4a-91cd-d1a013b9e905_2000x1428.png)

---

## Intro

The rise of cloud computing brings a new approach to software development, eliminating the need for planning how many servers or which licenses need to be purchased. With a few clicks on the AWS or Google Cloud console, companies can have their backends, databases, or AI models up and running.

Cloud vendors want to make sure they can adapt to this rapidly changing world. They add new services, support more features for the existing ones, catch up with the most advanced hardware, or even deprecate less adopted services.

Things we’re seeing on AWS or Google Cloud are very different compared to 15 years ago. However, there is undoubtedly one service that has been there from the very beginning. It’s not obsolete; it even evolves to serve an increasing number of use cases, playing a crucial part in the data infrastructure of many organizations.

In this article, we will delve into the infamous object storage, specifically Amazon S3, exploring what it is under the hood, its key characteristics, why it is gaining increasing attention in the data engineering field, and finally, some essential considerations for using it effectively.

> ***Note:** Although the article primarily focuses on Amazon S3, I believe the insights listed could help you work with other cloud object storage services.*

---

## What is it

Object storage is a technology that manages data as units called **objects**. Unlike a file hierarchy on a computer, this storage organizes objects in a **flat structure** within containers called **buckets**.

[![](https://substackcdn.com/image/fetch/$s_!iTbG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fecc0c8a6-7363-44d5-8d3c-4c4282a97650_354x410.png)](https://substackcdn.com/image/fetch/$s_!iTbG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fecc0c8a6-7363-44d5-8d3c-4c4282a97650_354x410.png)

**Amazon Simple Storage Service (S3)** is AWS's pioneering object storage service. It was first introduced in 2006. Since then, it has become the most widely used object storage platform globally. Each S3 object has:

[![](https://substackcdn.com/image/fetch/$s_!Pm7I!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e3fd55f-8e58-4364-be13-e84de73da268_464x452.png)](https://substackcdn.com/image/fetch/$s_!Pm7I!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e3fd55f-8e58-4364-be13-e84de73da268_464x452.png)

* **Keys:** Every object within a bucket is assigned a **unique key**, which serves as its identifier.
* **Prefix:** Object storage does not have folders. However, users can organize the data using a prefix to **make it look like folders**. A prefix is a string of characters at the beginning of the object key.

  + For example, two objects with the keys `reports/2025/sales.csv` and `reports/2025/inventory.csv` will appear to be in a `2025` folder, which is inside a `reports` folder.
  + However, they are just two distinct objects in the bucket that happen to share the `reports/2025/` prefix. No actual folders here.
  + Prefix plays a crucial role in how S3 distributes the workload; we will dive into that later.
* **Version ID:** S3 lets users preserve multiple versions of the same object. When object versioning is enabled, S3 will generate a not-null version ID for that object’s version. To identify an object in the bucket, S3 uses the object key + version ID.
* **Value:** The actual content in the object. S3 virtually supports any data in any format, as it views the object’s value as a sequence of bytes.
* **Metadata:** There are two types of metadata:

  + System metadata: This metadata is assigned by S3 to manage the object
  + User-defined metadata: This metadata is assigned by users.

We interact with S3 not like a local hard drive, but through a set of APIs to manage objects. (Even if you can interact with this service via the console, the frontend is calling the APIs on your behalf.)

## High-level services

[S3 has 350+ microservices in each of AWS’s region](https://youtu.be/sYDJYqvNeXU?t=417)s. At a high level, S3 has the [following services](https://www.allthingsdistributed.com/2023/07/building-and-operating-a-pretty-big-storage-system.html?ref=highscalability.com):

[![](https://substackcdn.com/image/fetch/$s_!O73c!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F54ea618c-bfe2-48ab-b882-5da213fd9b0c_664x452.png)](https://substackcdn.com/image/fetch/$s_!O73c!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F54ea618c-bfe2-48ab-b882-5da213fd9b0c_664x452.png)

Reference: [Building and operating a pretty big storage system called S3](https://www.allthingsdistributed.com/2023/07/building-and-operating-a-pretty-big-storage-system.html?ref=highscalability.com)

* The frontend fleet to serve the REST API
* The namespace services
* A storage fleet with a lot of hard disks (millions of drives)
* The storage management fleet that takes care of all the background operations (e.g., expiring objects, replicating objects…)

## How does it distribute the load?

When users want to upload objects, they issue `PUT` requests, which are handled by the front end. The objects are mapped to the storage server by [partitioning the objects’ keys (more specifically, the prefixes) over multiple servers in a lexicographically ordered manner](https://youtu.be/sYDJYqvNeXU?t=1024). Therefore, when clients want to read these objects, the workload can be distributed among multiple servers.

[![](https://substackcdn.com/image/fetch/$s_!EAau!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff065c945-f18c-4b4f-95ca-e8c49f9645e1_1046x516.png)](https://substackcdn.com/image/fetch/$s_!EAau!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff065c945-f18c-4b4f-95ca-e8c49f9645e1_1046x516.png)

For example, S3 might use the first character of the prefix to map objects to servers; [objects with prefixes](https://youtu.be/sYDJYqvNeXU?t=1091) that have the first character in this range will belong to the same partition:

[![](https://substackcdn.com/image/fetch/$s_!f01N!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff8fca7db-ea74-4681-8671-2198fc1f7c25_972x316.png)](https://substackcdn.com/image/fetch/$s_!f01N!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff8fca7db-ea74-4681-8671-2198fc1f7c25_972x316.png)

Reference: [AWS re:Invent 2023 - Dive deep on Amazon S3 (STG314)](https://www.youtube.com/watch?v=sYDJYqvNeXU&t=417s)

* From A-F
* From G-M
* From N-S
* From T-Z

The important thing is that the load must be distributed evenly. Amazon S3 can detect that a partition may have experienced a significant workload due to a high number of keys. In that case, S3 can further split that partition into smaller ones.

[![](https://substackcdn.com/image/fetch/$s_!RdqV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F912f6d15-1af3-4925-9b98-58ca29abf2c2_806x528.png)](https://substackcdn.com/image/fetch/$s_!RdqV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F912f6d15-1af3-4925-9b98-58ca29abf2c2_806x528.png)

Amazon [encourages us](https://youtu.be/sYDJYqvNeXU?t=1259) to have as much diversity as possible in the characters at the beginning of the prefix to help them distribute the workload more effectively. Google Cloud [also recommends](https://cloud.google.com/storage/docs/request-rate#naming-convention) this approach to help them with the auto-scaling feature.

The vendor enables us to scale our S3 throughput via prefixes, [allowing us to achieve at least 3,500 PUT/COPY/POST/DELETE or 5,500 GET/HEAD requests per second per partitioned Amazon S3 prefix. There is no limit on the number of prefixes that can be added to the bucket.](https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance.html) Given your bucket has ten prefixes, we can achieve a total of 35,000 PUT requests or 55,000 GET requests per second.

[![](https://substackcdn.com/image/fetch/$s_!ZJh4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F02f16b44-6a10-4449-a36b-0831651d4caf_596x258.png)](https://substackcdn.com/image/fetch/$s_!ZJh4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F02f16b44-6a10-4449-a36b-0831651d4caf_596x258.png)

## How does it ensure durability?

S3 is famous for the 99.999999999% (eleven 9s) data durability. To achieve these impressive numbers, Amazon has to:

* Ensure end-to-end data integrity
* Store data on multiple devices

### Ensure end-to-end data integrity

When an object is uploaded to S3, a checksum is calculated to ensure that its content remains unchanged during its time on S3. Clients can specify the checksum algorithm they want.

[![](https://substackcdn.com/image/fetch/$s_!dotc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F590b8e5d-e7d4-4ef6-8855-b2b5196cdd48_820x400.png)](https://substackcdn.com/image/fetch/$s_!dotc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F590b8e5d-e7d4-4ef6-8855-b2b5196cdd48_820x400.png)

Clients can optionally include the pre-calculated checksum as part of the upload requests. S3 then compares its calculated checksum with the client-provided checksum; if the two don’t match, it indicates data corruption during transfer, and S3 will reject the upload. If they match, the checksum is stored as immutable metadata with the object in S3.

[![](https://substackcdn.com/image/fetch/$s_!q5UG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5b0fc8be-6839-4b4d-93e3-fc56cf3e1939_654x334.png)](https://substackcdn.com/image/fetch/$s_!q5UG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5b0fc8be-6839-4b4d-93e3-fc56cf3e1939_654x334.png)

When downloading the object, the client can validate its integrity by comparing a locally calculated checksum of the downloaded data with the checksum stored in the object's metadata in S3.

### Store data on multiple devices

An object is persisted redundantly by leveraging erasure coding. It is a data protection technique that splits data into fragments, adds redundant pieces, and distributes them across multiple locations. The high-level process looks like this:

[![](https://substackcdn.com/image/fetch/$s_!IE0k!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f28626b-7a70-4a2d-b61c-af0833679c40_1036x718.png)](https://substackcdn.com/image/fetch/$s_!IE0k!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f28626b-7a70-4a2d-b61c-af0833679c40_1036x718.png)

* The users specify the number of primary [X] and parity [Y] fragments
* The data is broken down into X fragments.
* Y parity data fragments are mathematically generated (e.g., using [Reed-Solomon codes](https://en.wikipedia.org/wiki/Reed%E2%80%93Solomon_error_correction)).
* The primary and parity fragments are then stored across storage nodes.
* If some fragments are lost or corrupted, the original data can be reconstructed from the remaining pieces using the redundancy information.

Erasure coding enables the system to recover the complete data as long as no more than Y parity fragments are lost. This is the most significant advantage. Naive replication requires N complete copies of the data, meaning N times the original storage space. For example, 3-way replication uses 300% storage overhead.

Erasure coding, on the other hand, adds a smaller percentage of parity data. A typical configuration, such as (X=4, Y=2), only requires 150% of the original data size.

Back to S3, Amazon uses erasure coding with tailored X and Y configurations to distribute object values to multiple devices. Other vendors, [such as Google, also use this technique to ensure data durability](https://cloud.google.com/storage/docs/availability-durability#key-concepts).

## Atomicity Guarantee

In the context of a database, atomicity means that if multiple changes are made, all of them must succeed or fail as a whole. This simplifies the retrying process.

Amazon S3 only guarantees atomicity for individual object operations. If a `PUT` operation for an object is successful, the entire object data, along with its associated metadata, is durably stored. If it fails, no data is persisted.

[![](https://substackcdn.com/image/fetch/$s_!quRZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa625e086-a5df-442c-9e03-3df297be5ec0_524x238.png)](https://substackcdn.com/image/fetch/$s_!quRZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa625e086-a5df-442c-9e03-3df297be5ec0_524x238.png)

Multiple-object operations could fail or succeed partially. [Google Cloud Storage also only supports atomic operations for individual objects](https://cloud.google.com/storage/docs/consistency#atomic_operations).

[![](https://substackcdn.com/image/fetch/$s_!vdwx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd09b8d05-0252-4697-8445-eb9c9b93abcf_588x254.png)](https://substackcdn.com/image/fetch/$s_!vdwx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd09b8d05-0252-4697-8445-eb9c9b93abcf_588x254.png)

An important feature worth mentioning here is that S3 or GCS supports conditional write, which checks if a specified condition or set of conditions is met before executing a request.

This is crucial in preventing one writer from unknowingly overwriting changes made by another, especially when multiple clients attempt to write the same data concurrently. [The Delta Lake or Apache Hudi table format relies heavily on conditional write operations to execute lightweight atomic operations that create the metadata object, thus ensuring the atomicity of the data write operations.](https://open.substack.com/pub/vutr/p/how-do-iceberg-delta-lake-and-hudi?r=2rj6sg&utm_campaign=post&utm_medium=web&showWelcomeOnShare=false)

[![](https://substackcdn.com/image/fetch/$s_!hW_V!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc3cc20e9-4c66-473d-bf57-0ee387415d07_1042x470.png)](https://substackcdn.com/image/fetch/$s_!hW_V!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc3cc20e9-4c66-473d-bf57-0ee387415d07_1042x470.png)

## Consistency Guarantee

Initially, S3 offered:

* **Read-after-write consistency for new objects:** If the client uploads a new object, others could read it immediately.
* **Eventual consistency for overwrites and deletes:** There was a small time window (typically milliseconds to a few seconds) during which a subsequent read might return the old version, or the object might be available in the list operation.

  [![](https://substackcdn.com/image/fetch/$s_!8Hs4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F356233bf-2c30-4089-9d3f-e105a1bcae79_850x364.png)](https://substackcdn.com/image/fetch/$s_!8Hs4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F356233bf-2c30-4089-9d3f-e105a1bcae79_850x364.png)

Currently, Amazon S3 offers strong read-after-write consistency for all operations.

[![](https://substackcdn.com/image/fetch/$s_!ii1U!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F992304a9-22ac-43b5-bc08-263eaced817e_984x374.png)](https://substackcdn.com/image/fetch/$s_!ii1U!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F992304a9-22ac-43b5-bc08-263eaced817e_984x374.png)

S3 was designed with a metadata cache mechanism so that subsequent requests on the same objects won’t need to go to the persistent layer to retrieve the metadata. However, this can introduce metadata lag, as metadata from PUT or DELETE requests is not yet populated in the cache, which could cause clients to read stale metadata.

[![](https://substackcdn.com/image/fetch/$s_!CNQT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fecb6c729-deaf-4199-b7d2-0995bbcee23a_770x392.png)](https://substackcdn.com/image/fetch/$s_!CNQT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fecb6c729-deaf-4199-b7d2-0995bbcee23a_770x392.png)

If they return in the future, the cache might be updated, and they will see the current state of the data. This is why S3 initially provides eventual consistency. [To ensure strong consistency, Amazon implemented a new component to check if the metadata cache is stale](https://www.allthingsdistributed.com/2021/04/s3-strong-consistency.html). If the cached value is not stale, it can be used; otherwise, it can be read from the persistence layer, and the cache will be updated.

[![](https://substackcdn.com/image/fetch/$s_!sdpy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0a5b42ad-9d14-49cb-bebd-7cbd6e6cd8b5_588x350.png)](https://substackcdn.com/image/fetch/$s_!sdpy!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0a5b42ad-9d14-49cb-bebd-7cbd6e6cd8b5_588x350.png)

[Google Cloud Storage also provides read-after-write consistency.](https://cloud.google.com/storage/docs/consistency)

## How to use it effectively

In this section, I will share some of my experience working on object storage. I believe these can be applied to any object storage service out there.

### Object storage is not always your choice

While object storage, such as S3, is incredibly versatile and cost-effective for many scenarios, it's not a one-size-fits-all solution. Other storage types might be better suited for specific use cases. For example, if your application requires strict file-system semantics or extremely low latency, you should consider alternative storage options.

### Choose the storage class

Cloud vendors offer multiple storage classes designed to optimize costs and performance based on data access patterns. The higher storage class typically incurs a higher storage cost, but the request cost is lower in return. This implies that you need to keep hot data in high class (e.g, S3 standard) and keep cold data in low class (e.g., S3 Glacier Deep Archive)

[![](https://substackcdn.com/image/fetch/$s_!ypST!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa3ca5f8a-0b13-4857-86fd-2c02b891c7ee_494x278.png)](https://substackcdn.com/image/fetch/$s_!ypST!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa3ca5f8a-0b13-4857-86fd-2c02b891c7ee_494x278.png)

All vendors will provide guidelines on how to choose a storage class based on your needs, so I won’t go into the details here. Just keep these things in mind:

* Don’t blindly choose the default storage class for every use case. The data access pattern is crucial.
* Fully aware of the constraints of the low storage class, for example, [S3 Glacier Deep Archive](https://aws.amazon.com/s3/storage-classes/) will charge you extra money if the objects are deleted in 180 days.
* Leverage the lifecycle management feature to move data to different storage classes as needed.

### Version control

Object storage services enable you to store multiple versions of an object within the same bucket. When we allow versioning on a bucket, a unique version ID is assigned to each new object.

If the client uploads a new object with the same key as an existing object, the new object becomes the "current" version, but the old version is retained in the bucket with its unique version ID.

[![](https://substackcdn.com/image/fetch/$s_!ZFd_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa3b07887-47b7-4469-9406-95904870fd0e_450x248.png)](https://substackcdn.com/image/fetch/$s_!ZFd_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa3b07887-47b7-4469-9406-95904870fd0e_450x248.png)

This protects against accidental overwrites, deletions, or unintended application bugs, allowing the user to always recover a previous version. However, this feature increases storage costs.

Object versioning can be combined with the lifecycle management feature to delete older, non-current versions after a specified period automatically.

### Life cycle management

As discussed in the two sections above, you can configure your object to be moved to a different storage class or expire the objects or their old versions using the lifecycle management feature.

Please note that every vendor will provide you with this tool. Read the document and use it to meet your needs.

### Understand the pricing model

I believe all object storage services will have these commonalities in their pricing models:

[![](https://substackcdn.com/image/fetch/$s_!rB-o!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0cab73dc-9174-42f6-8d66-584c12370340_634x290.png)](https://substackcdn.com/image/fetch/$s_!rB-o!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0cab73dc-9174-42f6-8d66-584c12370340_634x290.png)

* They charge you for the amount of data you store.
* They charge you for the request you make (typically per 1000 requests)

First, understand your object storage pricing models in general (those three bullet points above are a good start). Then, understand how a specific storage class charges you, as different classes charge differently for the same amount of data and number of requests.

### Read and Write

For a large object, consider how your vendor can help you optimize the object reading and writing performance. For example, S3 and GCS support multi-part uploading, in which the object’s continuous parts can be uploaded simultaneously to increase performance. Or, they supported reading a byte range of an object to save bandwidth.

[![](https://substackcdn.com/image/fetch/$s_!rWM9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2c8858c4-5f66-4ec8-9931-5fce0a40dfa0_468x402.png)](https://substackcdn.com/image/fetch/$s_!rWM9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2c8858c4-5f66-4ec8-9931-5fce0a40dfa0_468x402.png)

### Security

Do not expose your object storage resources publicly in any circumstance.

Follow the least privilege access principle. Anyone who needs to access the object storage resource must be granted only the minimum level of access and permissions required to perform their specific task.

[![](https://substackcdn.com/image/fetch/$s_!RMqz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3dd2e7cb-2870-4f2c-a5fe-13a56a7da5b2_696x284.png)](https://substackcdn.com/image/fetch/$s_!RMqz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3dd2e7cb-2870-4f2c-a5fe-13a56a7da5b2_696x284.png)

Generating temporary, time-limited URLs for sharing objects is ideal for granting temporary read access without granting permission to the object storage resource.

Keep in mind that security is crucial, not only in object storage. Ensuring security might take more time as you need to read more documents or consult the SRE teams, but it's worth it, given the fact that you’re working with one of the most valuable company assets: the data.

## Why is it popular

S3, or object storage in general, has been utilized for a wide range of use cases, from disaster recovery and media hosting to serving as the storage layer for many advanced systems, such as lakehouses, OLAP databases, or event streaming platforms (e.g., WarpStream). Recently, S3 has introduced native support for storing and querying vector embeddings directly, enabling clients to streamline their AI workloads.

The question is: why is it so popular?

I think the answer is simple: it is nearly impossible for an organization to operate the storage infrastructure with the same durability and availability guarantee as these vendors provide.

[![](https://substackcdn.com/image/fetch/$s_!7Ik7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2e815edf-2600-4ee8-a5d9-f8b9fab983d8_486x314.png)](https://substackcdn.com/image/fetch/$s_!7Ik7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2e815edf-2600-4ee8-a5d9-f8b9fab983d8_486x314.png)

With just a few clicks on the console, you will have the most robust object storage up and running. The pay-as-you-go model, everything is handled by the vendors, a friendly set of API, all of them make object storage a compelling option for any organization.

Historically, HDFS has been the primary choice for data lakes. However, with the introduction of cloud object storage, HDFS soon handed over the crown to services like S3 or GCS. The advantage of object storage is emphasized here.

[![](https://substackcdn.com/image/fetch/$s_!tGQx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7be2ac26-0220-4ae7-b8e1-0bbbc0025d37_408x224.png)](https://substackcdn.com/image/fetch/$s_!tGQx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7be2ac26-0220-4ae7-b8e1-0bbbc0025d37_408x224.png)

There is no management overhead, the ability to store any data (exactly what a data lake aims to achieve), and extremely high durability + scalability.

In the 2020s, the emergence of the lakehouse paradigm, which promises to combine the strengths of data lakes and data warehouses, has led to object storage gaining even more attention. Object storage could ensure Durability in the ACID. However, recalling that it does not support multi-object atomic transactions, making it work like the data warehouse storage layer requires more effort.

[![](https://substackcdn.com/image/fetch/$s_!vu7M!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F98e63dee-c38b-4e09-b139-91f9e9e09a79_380x460.png)](https://substackcdn.com/image/fetch/$s_!vu7M!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F98e63dee-c38b-4e09-b139-91f9e9e09a79_380x460.png)

Table formats, such as Apache Iceberg or Delta Lake, provide a table abstraction on top of objects in the bucket. Object storage no longer acts as a dumping ground for data or archiving; it has become the backbone of many organizations’ data architecture.

Object storage is also used in systems that used to rely heavily on local disk in the past:

* Kafka Alternative: Solutions like WarpStream, AutoMQ, or Bufstream build their Kafka-compatible solution that operates on object storage.
* Database: Neon reimagine Postgres with object storage, turbopuffer is a vector and full-text search database built on object storage.

All of these happen because cloud vendors are doing a great job of offering a super simple and robust storage service.

---

## Outro

In this article, we first explore what Amazon S3 is, examine its high-level service, investigate how it distributes the load, and ensure data durability. Next, we discover S3’s atomicity and consistency guarantees. Then, I share some of my experience working with object storage. Finally, I attempt to explain why it is so popular, particularly in the context of data engineering.

Thank you for reading this far. See you next time.

---

## Reference

*[1] [Amazon S3 official documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)*

*[2] Dr. Werner Vogels, [Building and operating a pretty big storage system called S3](https://www.allthingsdistributed.com/2023/07/building-and-operating-a-pretty-big-storage-system.html?ref=highscalability.com) (2023)*

*[3] Dr. Werner Vogels, [Diving Deep on S3 Consistency](https://www.allthingsdistributed.com/2021/04/s3-strong-consistency.html) (2021)*

*[4] Stanislav Kozlovski, [Behind AWS S3’s Massive Scale](https://highscalability.com/behind-aws-s3s-massive-scale/) (2024)*

*[5] [AWS re:Invent 2023 - Dive deep on Amazon S3 (STG314)](https://www.youtube.com/watch?v=sYDJYqvNeXU&t=417s)*
