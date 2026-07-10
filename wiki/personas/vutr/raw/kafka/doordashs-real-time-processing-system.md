---
title: "DoorDash's real-time processing system"
channel: vutr
author: "Vu Trinh"
published: 2024-12-03
url: https://vutr.substack.com/p/doordashs-real-time-processing-system
paid: false
topics: ["Apache Kafka", "Apache Spark", "Apache Flink", "Snowflake", "Data Warehouse", "Streaming"]
tags: [https, kafka, doordash, auto, flink, image]
---

# DoorDash's real-time processing system

*Apache Kafka + Apache Flink*

> Source: [Open post](https://vutr.substack.com/p/doordashs-real-time-processing-system)

## Topics

[[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-flink|Apache Flink]] · [[snowflake|Snowflake]] · [[data-warehouse|Data Warehouse]] · [[streaming|Streaming]]

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=152347480)

[![](https://substackcdn.com/image/fetch/$s_!TpvQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7739b50b-5fba-47e2-9dc3-b2c16fc84c2d_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!TpvQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7739b50b-5fba-47e2-9dc3-b2c16fc84c2d_2000x1429.png)

Image created by the author.

---

## Intro

This week, we will return to my hidden series “How do the Big Tech manage their data“ by exploring how DoorDash, one of the largest food delivery platforms in the United States, manages its real-time processing with Apache Kafka and Flink.

This piece is my short note after reading the article: [Building scalable real-time event processing with Kafka and Flink](https://careersatdoordash.com/blog/building-scalable-real-time-event-processing-with-kafka-and-flink/) from DoorDash.

---

## Overview

At DoorDash, real-time data is crucial.

However, building a system to handle billions of events is not simple.

The data from DoorDash’s services or user devices must be processed and routed to different sinks in real-time:

* Most events need to be ingested into the Snowflake data warehouse.
* Some events will be fed into the ML platform.
* Monitoring and alerting based on some mobile events.

Let's check out the legacy real-time processing system at DoorDash.

---

## The legacy system

Initially, the company had different data pipelines that extracted data from the web application and ingested it data into Snowflake. Each pipeline is built to adapt to a specific kind of event. An example pipeline:

[![](https://substackcdn.com/image/fetch/$s_!yQjm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F61b77efe-a52a-4b3e-be6e-3a3977bef66a_670x442.png)](https://substackcdn.com/image/fetch/$s_!yQjm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F61b77efe-a52a-4b3e-be6e-3a3977bef66a_670x442.png)

Image created by the author.

There are some problems with this approach:

* It is inefficient to build multiple same-purpose pipelines (e.g., ingesting data into Snowflake; the pipelines are only different based on the type of events they serve)
* Challengings in operations.

DoorDash decided to build a new system.

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=152347480)

---

## The new system

The next generation of the DoorDash real-time event processing system must meet the following criteria:

* Supporting data from many different sources.
* Reliable and low-latency Snowflake data ingesting.
* The new platform must let different teams and services easily access the data stream.
* Supporting schema evaluation and schema enforcement.
* Scalable and fault-tolerant.

To meet these goals, DoorDash has shifted its strategy from relying on AWS and third-party services to open-source solutions: it chose Kafka and Flink as the backbone to build its new system.

Here is the overall architecture of DoorDash’s new real-time processing:

[![](https://substackcdn.com/image/fetch/$s_!S-nH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F024a4954-3fca-4c0e-805d-218e5c7421c1_1718x674.png)](https://substackcdn.com/image/fetch/$s_!S-nH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F024a4954-3fca-4c0e-805d-218e5c7421c1_1718x674.png)

Image created by the author.

Next, let’s dive deep into the details of the system.

### Event Producing

DoorDash chose Apache Kafka as the middleware for the streaming data.

A common way to produce data in Kafka is to create the client, connect to the set of bootstrap brokers, and retrieve the topic leader information. Only then can the client start sending messages to a broker.

However, operating Kafka at the scale of DoorDash, the above flow might encounter some challenges:

* Every service that produces messages to Kafka must set the flow like above, resulting in more overhead.
* It isn't easy to unify Kafka producer configuration across different services.
* The mobile and web applications can’t connect to Kafka directly.

Thus, DoorDash leverages [Confluent Kafka Rest Proxy](https://github.com/confluentinc/kafka-rest).

> *[From the official Github](https://github.com/confluentinc/kafka-rest): The Kafka REST Proxy provides a RESTful interface to a Kafka cluster. It makes it easy to produce and consume data, view the state of the cluster, and perform administrative actions without using the native Kafka protocol or clients.*

The proxy allows DoorDash to centralize and optimize the production of Kafka messages. It eliminates the need to configure Kafka connections and makes event publishing much more straightforward. DoorDash builds and deploys the proxy in their Kubernetes clusters using internal CI/CD processes

The REST proxy also provides some out-of-the-box features:

* Supporting different kinds of payload.
* Supporting batching events before sending them to Kafka brokers
* Native integration with the schema registry.

To make the proxy meet more DoorDash needs, they make some customization:

* Allowing the proxy to produce messages to multiple clusters.
* The ability to send data asynchronously to the broker without waiting for acknowledgment. This feature helps reduce significantly the response time.
* Pre-fetching Kafka topic metadata.
* Producing test records.

Besides levering the REST proxy, Doordash made some adjustments to achieve higher throughput:

* Kafka replicates the topic’s partition over the brokers to ensure data durability. Typically, a partition is replicated three times: one leader and two followers. DoorDash reduces the replication factor from 3 to 2. This decision is because DoorDash prioritizes throughput and availability over data consistency. Reducing the replication factor helps DoorDash save disk space and CPU workload used for replication.
* They set the [ack configuration](https://open.substack.com/pub/vutr/p/apache-kafka-producer?r=2rj6sg&utm_campaign=post&utm_medium=web) to 1, which means the producer will receive the acknowledgment as soon as the leader receives the message. This helps reduce the response time because it doesn’t have to wait for the data replicated to the follower.
* DoorDash also leverages Kafka's sticky partitioner, which aims to stick the produced message to a particular partition for a batch of records. It tries to send as many records as possible to the same partition until a specific condition is met, such as the batch reaching its limit.

All the tuning above contributed to the Kafka broker CPU utilization decreasing by 30 to 40%.

### Event Processing

DoorDash chose Apache Flink for real-time data processing thanks to its native support for event-time-based processing, fault tolerance, and rich integration with many sources and sinks.

DoorDash leverages Flink Stream API and Flink SQL to build the real-time processing application.

They provide a base Flink docker image for internal users with all necessary configurations.

To achieve isolation between applications, they deploy each Flink application as a separate Kubernetes pod.

[![](https://substackcdn.com/image/fetch/$s_!GceP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F37a2e639-d2a3-4e83-b7fa-9d37ca927f04_364x392.png)](https://substackcdn.com/image/fetch/$s_!GceP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F37a2e639-d2a3-4e83-b7fa-9d37ca927f04_364x392.png)

Image created by the author.

When using Flink data stream APIs, internal users must follow these steps:

[![](https://substackcdn.com/image/fetch/$s_!X7R0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7a7abcc0-e6ca-4b2c-b97f-5e376c7b4ddd_1396x706.png)](https://substackcdn.com/image/fetch/$s_!X7R0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7a7abcc0-e6ca-4b2c-b97f-5e376c7b4ddd_1396x706.png)

Image created by the author.

* Cloning the Flink application template.
* Adjusting the template with the required logic.
* Defining application and Flink’s job configuration (e.g., the parallelism) using a terraform template.
* The deployment process takes the terraform template and the application docker image and deploys the Flink application in the K8s cluster from a generated **[Helm Chart](https://helm.sh/)**.

With data users, data stream API might not be so familiar with them. DoorDash lets these users create the Flink application using SQL:

* Users define the processing logic in the YAML, including the SQL logic, the source, the sinks, etc
* The users then create the Pull Request with the YAML file.
* The CD pipeline compiles the YAML into the Flink application and deploys it.

### Event Format

As the first step in building the new platform, DoorDash defined a unified format for produced and processed messages and developed serialization/deserialization libraries for event producers and consumers to work with this format.

All events that flow through the system have a standard envelope and payload.

The first contains the event's context (e.g., created time), metadata (e.g., encoding method), and references to the schema. The envelope is stored as the Kafka record header.

The latter contains the actual content of the event and is stored as the Kafka record value. The payload will be schema-validated and encoded.

The producer will drop the invalid payloads, preventing sending it to the broker.

Events produced from web or mobile devices are in raw JSON format, and DoorDash uses a dedicated Flink application to validate and transform it to the schema-validated format.

### Data Warehouse Integration

The integration is implemented as follows:

[![](https://substackcdn.com/image/fetch/$s_!BcOF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F946b1952-6bb3-4245-9d95-c2f21cccb573_534x488.png)](https://substackcdn.com/image/fetch/$s_!BcOF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F946b1952-6bb3-4245-9d95-c2f21cccb573_534x488.png)

Image created by the author.

* The Flink application will consume the data from Kafka and upload it to S3 in the Parquet format. Landing data to S3 has several benefits: it keeps data for longer retention (than Kafka), makes the ingest pipeline less dependent on the Snowflake (can backfill data in case of failures), and allows other analytic services, such as the DoorDash in-house Trino service, to access these data.
* Using [Snowpie](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-intro) (Snowflake’s feature) to copy data from S3 to Snowflake. Based on the [notifications from the Amazon SQS](https://docs.snowaflake.com/en/user-guide/data-load-snowpipe-auto-s3), Snowpie will load data from S3 to Snowflake as soon as it is available using the [COPY statement](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table).

To achieve isolation, each type of event has a dedicated Flink Job—Snowpie pipeline.

---

## Outro

Thank you for reading this far.

We’ve taken a glimpse into the real-time processing system at DoorDash, with Kafka and Flink as its backbone.

If you’re interested in learning more about Kafka, I’ve written a dedicated series on this messaging system, which you can find [here](https://vutr.substack.com/t/kafka).

As for Flink, it’s been on my backlog for a while. If you’d like to read about it, please comment so I can bump it up on my list!

---

## **References**

*[1] Allen Wang, [Building scalable real-time event processing with Kafka and Flink](https://careersatdoordash.com/blog/building-scalable-real-time-event-processing-with-kafka-and-flink/) (2022)*

---

## Before you leave

If you want to discuss this further, please leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/), [Email](http://vutrinh2704@gmail.com), or [Twitter](https://x.com/_vutrinh).

[Leave a comment](https://vutr.substack.com/p/doordashs-real-time-processing-system/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
