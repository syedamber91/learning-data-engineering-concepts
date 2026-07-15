---
title: "I spent 4 hours learning how Netflix operates Apache Iceberg at scale."
channel: vutr
author: "Vu Trinh"
published: 2024-11-16
url: https://vutr.substack.com/p/i-spent-4-hours-learning-how-netflix
paid: false
topics: ["Apache Kafka", "Apache Spark", "Apache Iceberg", "Apache Flink", "Data Lake", "Lakehouse", "Data Governance"]
tags: [iceberg, netflix, https, auto, table, image]
---

# I spent 4 hours learning how Netflix operates Apache Iceberg at scale.

*Iceberg The Backbone At Netflix Data Platform Architecture*

> Source: [Open post](https://vutr.substack.com/p/i-spent-4-hours-learning-how-netflix)

## Topics

[[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[apache-flink|Apache Flink]] · [[data-lake|Data Lake]] · [[lakehouse|Lakehouse]] · [[data-governance|Data Governance]]

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=151653732)

[![](https://substackcdn.com/image/fetch/$s_!eauF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F908afb73-357a-4cfb-9ee1-30a578572728_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!eauF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F908afb73-357a-4cfb-9ee1-30a578572728_2000x1429.png)

Image created by the author.

---

## Intro

At Netflix, every feature, from personalized recommendations to real-time analytics on trending shows, is backed by extensive data pipelines and analytics. To support this, Netflix has built a sophisticated data platform capable of scaling and evolving with the increasing demands of a global audience.

Apache Iceberg is a crucial component in this system. It is an open table format initially designed to overcome the limitations of Netflix’s previous Hive-based warehouse.

This week, we will learn more about how Netflix operates Apache Iceberg internally and how they migrated around 1.5 million Hive tables to the Iceberg format.

---

## The Netflix data platform architecture

> *The overview*

Netflix’s data platform architecture is cloud-native, designed with principles of storage-compute separation and component modularity.

[![](https://substackcdn.com/image/fetch/$s_!quBI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F31db8ad7-da6e-4838-aae8-9ebf8b386be4_2184x1214.png)](https://substackcdn.com/image/fetch/$s_!quBI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F31db8ad7-da6e-4838-aae8-9ebf8b386be4_2184x1214.png)

Image created by the author.

Data flows into the platform from many sources, including Cassandra, RDS, or CockroachDB. These data stores feed Netflix’s stream-processing platform, which is built on open-source technologies like Kafka and Flink. The platform processes trillions of daily events. The data lands in the lakehouse backed by S3 and Apache Iceberg, making it accessible for Netflix’s analytics and product development teams.

There is a metadata services layer. A metadata store called Metacat provides a unified API for accessing metadata about the datasets. It abstracts away all of the data stored behind the scenes, and users only need to use a three-part name (prod.full.bar) to refer to a table; they don’t need to care about the details such as the table type (Hive or Iceberg). Other services, such as Netflix's data catalog and policy engine, are part of Netflix's data governance process.

For the computing layer, they are services that serve specific use cases: Trino for interactive query, Spark for data pipeline, Druid to power real-time dashboards, and Elasticsearch for the search engine. Titus, Netflix’s container management system, manages most of the services on AWS EC2.

Finally, there are services like Tableau or Jypter Notebook for the data serving layer.

---

## Why Iceberg At The First Place

Historically, Netflix relied heavily on Hive.

> *600,000 Hive tables and 250 million partitions*

However, as data volumes grew to hundreds of petabytes, Netflix encountered some challenges with Hive. It lacked ACID transactions, atomicity, time traveling, and rollback. Common tasks like changing partitioning schemes or updating schemas require rewriting the whole table.

Recognizing these challenges, Netflix developed Iceberg. Iceberg is designed with ACID transactions, compatibility across various processing engines, and a rich metadata layer, which can provide features like time travel, schema, and partition evolution…

The table format offered Netflix the scalability and flexibility needed to keep up with the data demands.

If you want to learn more about the Iceberg table format, you can check out my two articles here:

Netflix built the Iceberg ecosystem while keeping the Hive warehouse running in production. Later, they gracefully migrated most Hive tables to Iceberg tables. We will learn about the Netflix Hive-Iceberg migration later, but next, we will explore how Netflix built an ecosystem around the Iceberg.

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=151653732)

---

## Netflix Iceberg Ecosystem

### Polaris

> *Iceberg Catalog*

[![](https://substackcdn.com/image/fetch/$s_!J2pr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd5cf3575-5962-4182-9161-654387aa42da_502x428.png)](https://substackcdn.com/image/fetch/$s_!J2pr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd5cf3575-5962-4182-9161-654387aa42da_502x428.png)

Image created by the author.

Initially, Netflix used the Hive Metastore for both Hive and Iceberg tables. The metastore was backed by an RDS MySQL. This approach soon showed limitations due to the difference in metadata commit patterns of Hive (pessimistic-locking) and Iceberg (optimistic-concurrency), which put much pressure on the RDS instances.

Thus, Netflix built Polaris, a custom metastore designed specifically for Iceberg tables. Thanks to its robust horizontal scalability support, Netflix chose CockroachDB to back this metastore.

In addition, Polaris was developed to support the Iceberg REST catalog specification, which standardizes the Iceberg table metadata management. With the REST catalog endpoint, any third-party engine compatible with the standard can connect directly to the warehouse. This was a significant improvement over Hive, as it now exposes a single endpoint to connect to the warehouse and execute queries.

### Janitors

> *Clean-up service*

Netflix built a service called Janitors, which is responsible for cleaning up expired data from the Iceberg. The service can be configured to run with three options:

* TTL (Time-to-live) Janitor: It cleans up data that has passed a specific expiration date.
* Snapshot Janitor: It cleans up Iceberg snapshots based on a TTL.
* Orphaned File Janitor cleans up orphaned files in the bucket. These files can’t be referenced from any Iceberg table. Most of them are from failed metadata commits.

Here is the typical process of the Janitors:

[![](https://substackcdn.com/image/fetch/$s_!pPoG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F52e61c3e-5618-47ea-87df-b218d9e1ee90_1678x872.png)](https://substackcdn.com/image/fetch/$s_!pPoG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F52e61c3e-5618-47ea-87df-b218d9e1ee90_1678x872.png)

Image created by the author.

* The user configures the TTL for the Janitors.
* Spark Jobs retrieves the information on expired tables.
* Then, it sends the information to the Amazon SQS.
* An Amazon S3 deletion service pulls table information from the SQS. It will execute a soft deletion of the data in S3. Data will be hard deleted after 5 to 7 days. The deletion service also writes to the audit log. In case of accidentally dropping a table, the user can restore data using this log.

### Autotune

Netflix built this service to optimize the Iceberg's physical data layout in the background. The write operations can write many smaller files for an Iceberg table, which could degrade the data read performance when the operation needs to open and close too many small files.

Autotune service will run in the background to optimize the data files for the Iceberg tables. Some techniques include merging small files into larger ones or handling low-level delete file compactions.

Here is the typical process of Autotune:

[![](https://substackcdn.com/image/fetch/$s_!uRYN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F49b6537e-3dea-47d4-b4ee-2545c61c3c61_1890x852.png)](https://substackcdn.com/image/fetch/$s_!uRYN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F49b6537e-3dea-47d4-b4ee-2545c61c3c61_1890x852.png)

Image created by the author.

* The user writes data to the Iceberg Table
* The metastore detects it and sends an event to SQS.
* The Autotune service listens to these events.
* If the table needs to be compacted, Autotune will use the compaction config to understand how files should be compacted.
* It then launches the Spark job to rewrite the data files.

### Autolift

They allow data to be streamed into multiple regions. However, much of Netflix’s computing runs in the US-East-1 region, so Netflix developed the Autolift service - which helps localize data files to reduce cross-region bandwidth costs.

This service migrates up to three petabytes of data daily, leveraging Iceberg’s replace commit API. It scans incoming snapshot data and finds all the files that need to be brought to the US-East-1 region. Then, it uses the replace commit API to remove files from remote regions and replace them with local ones atomically.

### Secure Iceberg tables

For security, Netflix introduced Iceberg’s table-level access controls. Each table is treated as a distinct resource with specific S3 prefixes, where access permissions metadata like the ACLs (e.g., which users have access to this table) is also stored in the Iceberg table.

[![](https://substackcdn.com/image/fetch/$s_!HJSg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F14d43a27-7439-4264-9653-943aa4ea1cf0_1228x802.png)](https://substackcdn.com/image/fetch/$s_!HJSg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F14d43a27-7439-4264-9653-943aa4ea1cf0_1228x802.png)

Image created by the author.

Here is a typical process when a user needs to access an Iceberg table:

* The user executed the query on table “abc”.
* The Spark driver then contacts the external signer service. Netflix built this service as the policy enforcement point for secure Iceberg tables.
* The Spark driver asks the signer service whether this user has permission on table ”abc”, the service reaches out to the metastore to check if the user is included in the ACL; if yes, it issues an [AWS STS](https://docs.aws.amazon.com/STS/latest/APIReference/welcome.html) token.
* The signer service returns this token to the Spark driver.
* The token is passed to the Spark executors so they can start reading the “abc“ table.

This approach allows Netflix to secure data without requiring users to interact with low-level S3 settings, maintaining a high-level abstraction.

---

## Hive → Iceberg

Iceberg is great. Everything with Iceberg is improved significantly compared with Hive. But here was the reality at Netflix: at that time, a large amount of data was still in Hive formats.

Netflix still had hundreds of petabytes of data, with around 1.5 million Hive tables awaiting to be migrated.

They decided to build a migration tooling to handle the heavy lifting on behalf of their users, migrating these tables into Iceberg transparently and with minimal downtime. One of the top priorities of this tool is minimizing data movement as much as possible. To achieve this, Netflix designed a procedure that creates an Iceberg metadata layer on top of the data files from the Hive table instead of physically copying the data from Hive to Iceberg. Netflix migrated most of the Hive tables using this approach. However, a small number of tables had to be migrated using the actual copy operation.

[![](https://substackcdn.com/image/fetch/$s_!Bjar!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8907dc29-46fd-4d1f-bc88-eba855fab9cb_1028x630.png)](https://substackcdn.com/image/fetch/$s_!Bjar!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8907dc29-46fd-4d1f-bc88-eba855fab9cb_1028x630.png)

Image created by the author.

Netflix promises that the Hive-to-Iceberg migration tooling will manage all the user migration-related tasks. This tooling has five components:

[![](https://substackcdn.com/image/fetch/$s_!QDGM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F287544b2-83f2-4ba3-a5da-6e90bc38f38a_720x502.png)](https://substackcdn.com/image/fetch/$s_!QDGM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F287544b2-83f2-4ba3-a5da-6e90bc38f38a_720x502.png)

Image created by the author.

* **The Processor**: It wakes up after an interval and identifies all tables that must be scheduled for migration. This component also extracts these table’s metadata, such as the table owner.
* **The Communicator**: The information on scheduled tables is passed to the Communicator. It then notifies the table’s owner and downstream users about the migration.
* **The Migrator**: This component is responsible for the table migration. It will run the procedure to create Iceberg metadata on top of Hive data files or execute the physical copy operations. If things go well, the migrator finalizes the migration; if they don’t, the reverter can step in.
* **The Reverter**: This component will revert the tables back to Hive format if the issues arise. To make the revert feasible, Netflix keeps the original Hive table in sync with the migrated Iceberg table for some time after the migration.
* **The Shadow**: This component handles the synchronization mentioned in the reverter. It performs delta copying using Iceberg's metadata layer to keep the two tables in sync.

These components communicate via a shared state but operate asynchronously to ensure others do not block them. Each component's typical workflow involves waking up, performing a specific task, and returning to sleep.

Each component of the migration tool can be run with multiple instances, allowing for parallelization of the migration process. The tables are distributed across these instances using consistent hashing.

---

## Outro

Thank you for reading this far.

In this article, we explored an overview of Netflix’s data platform architecture and the motivation behind their creation of Iceberg. We then delved into the ecosystem around Iceberg, from optimization and cleaning services to Netflix’s secure Iceberg model. Finally, we examined how Netflix designed a migration tool that minimizes data movement and business interruptions.

See you next time!

---

## **References**

*[1] [AWS re:Invent 2023 - Netflix’s journey to an Apache Iceberg–only data lake (NFX306)](https://www.youtube.com/watch?v=jMFMEk8jFu8)*

---

## Before you leave

If you want to discuss this further, please leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/), [Email](http://vutrinh2704@gmail.com), or [Twitter](https://x.com/_vutrinh).

[Leave a comment](https://vutr.substack.com/p/i-spent-4-hours-learning-how-netflix/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
