---
title: "Let's build a data platform like Spotify! "
channel: vutr
author: "Vu Trinh"
published: 2025-01-23
url: https://vutr.substack.com/p/lets-build-a-data-platform-like-spotify
paid: false
topics: ["Apache Kafka", "Apache Spark", "Apache Flink", "BigQuery", "Streaming", "Data Quality", "ETL"]
tags: [spotify, https, event, delivery, auto, they]
---

# Let's build a data platform like Spotify! 

*How they build and what can we learn.*

> Source: [Open post](https://vutr.substack.com/p/lets-build-a-data-platform-like-spotify)

## Topics

[[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-flink|Apache Flink]] · [[bigquery|BigQuery]] · [[streaming|Streaming]] · [[data-quality|Data Quality]] · [[etl|ETL]]

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=154523636)

[![](https://substackcdn.com/image/fetch/$s_!4liV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1dcb8e03-4e33-4683-8fd9-ae775911f137_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!4liV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1dcb8e03-4e33-4683-8fd9-ae775911f137_2000x1429.png)

Image created by the author.

---

## Intro

Spotify, the human’s digital jukebox.

80+ million songs.

2.6+ million podcasts.

640+ million monthly active users.

1.4+ trillion data points daily

Drawing insight from this data is crucial to their business.

This week, we learned how Spotify built the internal data platform.

---

## The need

Spotify has been a data-driven company since day one. It uses data for many purposes, from payments to experimentation. To manage the vast amount of data, Spotify requires a more streamlined approach.

The need for the data platform was inevitable.

From IBM:

> *A data platform is a technology solution that enables the collection, storage, cleaning, transformation, analysis, and governance of data.*

Here are their motivations:

* They want to streamline searching and using data for data professionals.
* Data quality is the number one priority.
* They must satisfy financial reporting, which requires consolidation from many data pipelines and other reporting.
* The processes and workflows to facilitate the experimentation (e.g., A/B testing) development lifecycle.
* Machine learnings need well-classified data.

Before diving into their data platform, we will explore its most important system, event delivery.

---

## **The event delivery**

### On-prem

Most Spotify data comes from clients who listen to songs or search for artists. Event delivery is the process of transporting all the events from global clients to the Spotify central system.

It is the foundational piece of Spotify’s data infrastructure. It must deliver complete data with a predictable latency.

Spotify gateways capture events that occur in the client via Syslog. The gateways assign the event a timestamp, which the delivery system uses throughout.

The system must route all the data to the central Hadoop cluster. The servers that collect the data are located in multiple data centers on two continents. They had to deliberate on bandwidth planning between data centers. The delivery system writes all data in Avro format on HDFS, following hourly partitions.

Spotify describes the event delivery architecture as follows:

[![](https://substackcdn.com/image/fetch/$s_!8DBd!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F632d5413-9931-4cf3-83ff-e9e31172ad2d_1842x1052.png)](https://substackcdn.com/image/fetch/$s_!8DBd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F632d5413-9931-4cf3-83ff-e9e31172ad2d_1842x1052.png)

Image created by the author.

* They used Kafka 0.7. In this version, Kafka Broker missed the ability to act as a reliable persistent storage, which shaped the rest of the architecture.
* The system did not keep the data persistent between Kafka producers and the Hadoop clusters. Spotify considers events to persist only when the system writes them to HDFS reliably.

This means that Hadoop is the single point of failure.

If Hadoop is down, the whole system will go down. When the Hadoop cluster recovers, Spotify must transfer all the data as soon as possible to let it catch up with the current state; the recovery times depend on the bandwidth between data centers.

The Kafka Producers run on every host that needs to send events to Hadoop. The consumer consumes the message, writes to the HDFS, and sends the ACK to the producer via a dedicated broker. Upon receiving the acknowledgment that the consumers wrote the message to the HDFS, the producers continued with the other batch.

Between the producer and the consumer, there are Kafka Groupers. Spotify developed Grouper to consume all events from the same local data center and then republish compressed, batched messages to a single topic, which the consumers then pull.

ETL jobs will execute on the hourly partition. To check data completeness, the job combines information about which servers to get data from and end-of-file markers. If the job detects the data incompleteness, it delays data processing for that particular hour.

> *Producers send end-of-file markers to confirm the system write a whole files to the HDFS reliably.*

In summary, the main problem with this design is that the local producer must ensure that data persists in the central HDFS. The producer on the US West Coast needs confirmation that the system has written the data to the HDFS cluster in London.

[![](https://substackcdn.com/image/fetch/$s_!zUec!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4103aceb-7422-4692-8e0c-de81daa5953a_1584x986.png)](https://substackcdn.com/image/fetch/$s_!zUec!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4103aceb-7422-4692-8e0c-de81daa5953a_1584x986.png)

Image created by the author.

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=154523636)

---

### Google Cloud

> *Kafka → PubSub, HDFS → Cloud Storage, Hive → BigQuery, MapReduce → BigQuery*

In 2015, Spotify moved its infrastructure to the Google Cloud Platform (GCP) and redesigned the event delivery in the cloud. The four main components of the new system are:

* File Tailer checks the end of the log files, looks for new events, and routes them to the Event Delivery Service.
* Event Delivery Service transforms messages from the Tailer into the desired format and forwards them to the queue.
* The Reliable Persistent Queue acts as a reliable intermediate storage, besides reliable data transporting.
* ETL jobs deduplicate and export events from the Queue to the hourly partition in HDFS.

For the queue, Spotify considered Kafka 0.8 and Google Cloud Pubsub.

[![](https://substackcdn.com/image/fetch/$s_!NIXR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa9fddeb3-294d-4c81-a337-cb1578e9fa91_794x466.png)](https://substackcdn.com/image/fetch/$s_!NIXR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa9fddeb3-294d-4c81-a337-cb1578e9fa91_794x466.png)

Image created by the author.

Kafka 0.8 was a significant improvement over version 0.7, and the project Mirror Maker promised to mirror data between data centers.

However, Kafka 0.8 failed Spotify’s stress test. The Kafka Producer had serious stability issues. If the admin removed one or more brokers from a cluster, the producer would enter a state that couldn’t self-recover. Regarding data mirroring, the Mirror Maker only mirrored data on a best-effort basis.

In addition to these issues, they recognized the need for further efforts to make the system production-ready, such as defining deployment strategies for Kafka Brokers and Mirror Makers or doing capacity modeling and planning for all components.

While struggling with Kafka, many other Spotify teams started using Google Cloud Pub/Sub, a reliable, persistent queue that can retain undelivered data for seven days. It is also globally available and has a simple REST API. Google handles every aspect of Pub/Sub, which can free Spotify from operational overhead.

To evaluate Pub/Sub for the event delivery system, Spotify put it to the test.

On the producer side, they test the workload with 2 million events per second. Spotify developed a Pub/Sub library based on its REST API to facilitate the test. The result?

Pub/Sub passed: It published 2 million messages without service degradation and received almost no server errors from the Pub/Sub backend.

On the consumer side, they focused on the system's end-to-end latency under heavy load. They created a subscription that consumes 1000 messages every time. The median end-to-end latency was around 20 seconds, and they didn’t observe any lost messages during the test period.

Finally, Spotify used Cloud Pub/Sub instead of Kafka 0.8 for the event delivery queue.

[![](https://substackcdn.com/image/fetch/$s_!IQq9!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F76994947-049e-4291-a5a7-28a185cb6f5c_2372x768.png)](https://substackcdn.com/image/fetch/$s_!IQq9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F76994947-049e-4291-a5a7-28a185cb6f5c_2372x768.png)

Image created by the author.

For data processing, Spotify shifted from MapReduce batch jobs to Google Dataflow’s hourly-windowing streaming jobs for the ETL. Spotify also developed a Scala API for Apache Beam and later open-sourced it.

They also switched to Google Cloud Service for other physical components of event delivery, shifting HDFS and Hive to Cloud Storage and BigQuery.

Since rolling the GCP-based event delivery system into production, they have doubled the Monthly active users and reached 1.5 million events per second. At the end of Q1 2019, they produced over 8 millionevents per second at peak, summing up to over 350 TB of raw data from their clients and internal systems daily.

After exploring Spotify’s event delivery, let’s move on to how this system fits into their data platform.

---

## **The data platform**

The platform has the following components:

[![](https://substackcdn.com/image/fetch/$s_!-vfP!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04b5b7a3-4ba4-4fd3-b6e2-0c4a9ab8e152_2330x980.png)](https://substackcdn.com/image/fetch/$s_!-vfP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04b5b7a3-4ba4-4fd3-b6e2-0c4a9ab8e152_2330x980.png)

Image created by the author.

* **Event delivery** collects data from clients.
* **Data processing** manages the data pipelines.
* **Data management** focuses on data attribution and privacy.

### Event delivery

In 2024, Spotify will collect 1 trillion events daily. The event delivery has advanced since moving to the cloud in 2015.

Spotify needs to collect data to:

* Understanding user, including relevant content or their interaction on the app.
* Reacting to user feedback.

When a team wants to collect data via an event delivery system, they must define logic and an event schema. Spotify will streamline infrastructure management, from Cloud PubSub to DataFlow stream jobs.

They achieve a balance between centralized and distributed ownership, allowing event consumers to control the data update without requiring the infrastructure team.

### Data Processing & Data management

Spotify has more than 38,000 actively scheduled pipelines running hourly and daily tasks. The scheduler is an essential component of data processing.

The Scheduler will run the workflow on BigQuery, Flink, or Dataflow. Spotify uses Scio, the Apache Beam Scala API. They developed this API after moving the event delivery to the Google Cloud in 2015.

Data pipelines result in data endpoints, each has a schema and can contain multiple partitions. They set retention policies and access controls, track lineage, and execute quality checks for these endpoints. Spotify also monitors for data lateness and failed pipelines.

To increase the data platform adoption rate, Spotify has the following initiatives:

* They write searchable documents that provide guidelines and information for data users.
* Dedicated teams embed in other teams to streamline data platform usage. They also collect feedback from the users to improve and enhance the platform.
* Automating infrastructure as much as possible.
* Encouraging data users to ask questions and seek support.

---

## Outro

To wrap up, here are the lessons from Spotify that we can apply:

* Aligning organizational needs with the investments.
* Clearing the challenges and goals.
* Embracing user experience and feedback.
* Start small and fail fast.

I just finished my notes after reading five articles by Spotify to learn how they build their data platform. More than 50% of the articles focus on the platform's most crucial component: the event delivery system.

If you have time, I recommend reading all five articles.

Thank you for reading this far. See you on my next pieces.

---

## **References**

*[1] Igor Maravić, [Spotify’s Event Delivery – The Road to the Cloud (Part I)](https://engineering.atspotify.com/2016/02/spotifys-event-delivery-the-road-to-the-cloud-part-i/) (2016)*

*[2] Igor Maravić, [Spotify’s Event Delivery – The Road to the Cloud (Part II)](https://engineering.atspotify.com/2016/03/spotifys-event-delivery-the-road-to-the-cloud-part-ii/) (2016)*

*[3] Igor Maravić, [Spotify’s Event Delivery – The Road to the Cloud (Part III)](https://engineering.atspotify.com/2016/03/spotifys-event-delivery-the-road-to-the-cloud-part-iii/) (2016)*

*[4] Anastasia Khlebnikova, Carol Cunha,* [Data Platform Explained Part I](https://engineering.atspotify.com/2024/04/data-platform-explained/) (2024)

*[5] Anastasia Khlebnikova, Carol Cunha,* [Data Platform Explained Part II](https://engineering.atspotify.com/2024/05/data-platform-explained-part-ii/) (2024)

---

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
