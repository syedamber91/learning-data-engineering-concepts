---
title: "GroupBy #42: Paypal - Scaling Kafka"
channel: vutr
author: "Vu Trinh"
published: 2024-07-02
url: https://vutr.substack.com/p/groupby-42-paypal-scaling-kafka
paid: false
topics: ["Data Engineering", "Apache Airflow", "Apache Kafka", "Apache Spark", "Apache Flink", "Orchestration", "Streaming"]
tags: [kafka, https, paypal, auto, scaling, clusters]
---

# GroupBy #42: Paypal - Scaling Kafka

*Plus: Introduction to Kafka Tiered Storage at Uber, Modern Good Practices for Python Development*

> Source: [Open post](https://vutr.substack.com/p/groupby-42-paypal-scaling-kafka)

## Topics

[[data-engineering|Data Engineering]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-flink|Apache Flink]] · [[orchestration|Orchestration]] · [[streaming|Streaming]]

---

*This is **GroupBy**, the weekly compiled resources for data engineers.*

*Not subscribed yet? Here you go:*

[Subscribe now](https://vutr.substack.com/subscribe?)

> *👋 Hi, my name is Vu Trinh, a data engineer.*
>
> *I share my lesson and excellent resources to read in this newsletter.*
>
> *Hope this issue finds you well.*

[![](https://substackcdn.com/image/fetch/$s_!qm74!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6aef1d57-4862-440e-8b04-ed52b8b8ed73_1400x1000.png)](https://substackcdn.com/image/fetch/$s_!qm74!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6aef1d57-4862-440e-8b04-ed52b8b8ed73_1400x1000.png)

---

# **Paypal - Scaling Kafka**

> *This week, we will see how PayPal manages and operates Kafka to support its data growth. This mini-blog is based on the article **[Scaling Kafka to Support PayPal’s Data Growth (2023)](https://medium.com/paypal-tech/scaling-kafka-to-support-paypals-data-growth-a0b4da420fab).***

## Kafka at Paypal

At the time of the article writing, Paypal’s Kafka fleet consists of over 85+ clusters with 1,500 brokers that host over 20,000 topics and close to 2,000 Mirror Makers (used to mirror the data among the clusters). During the 2022 Retail Friday, Kafka traffic volume peaked at about **1.3 trillion messages daily**.

[![Fig 4. Kafka cluster deployments in security zones within a data center](https://substackcdn.com/image/fetch/$s_!wiFg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbdfb92f5-fef8-43ab-b7f1-d54a109640ad_956x444.png "Fig 4. Kafka cluster deployments in security zones within a data center")](https://substackcdn.com/image/fetch/$s_!wiFg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbdfb92f5-fef8-43ab-b7f1-d54a109640ad_956x444.png)

Kafka cluster deployments in security zones — Scaling Kafka to Support PayPal’s Data Growth (2023). [Source](https://medium.com/paypal-tech/scaling-kafka-to-support-paypals-data-growth-a0b4da420fab)

PayPal's infrastructure is spread across multiple geographical data centers and security zones. They deploy Kafka clusters across these zones and use Mirror Makers to replicate data between clusters. Client applications connect to the topics on these brokers to publish (write) or subscribe (read) the data in the same or different zone. PayPal internally supports various Kafka’s clients such as Java, Python, Spark, Node,…

Operating Kafka at PayPal had its own set of challenges. With different frameworks and tech stacks, they must invest in building robust tools that help them reduce operational overhead. Each section below will describe the era in which PayPay invested.

## Cluster Management

PayPal introduced a few improvements:

* **Kafka Config Service:** If clients want to interact with the Kafka cluster, they must hardcode the broker IPs in the code. When the brokers are replaced due to upgrades, patching, disk failures, etc., the clients must change the broker IP manually. Kafka Config Service pushes information about a set of bootstrap servers (brokers that host the topics) to all the Kafka clients during initialization. If the broker's details change, the Kafka application only needs to restart so that the config service can push the new configuration for them.
* **Kafka Access Control Lists (ACLs):** ACLs were onboarded at PayPal to help control access to Kafka clusters via the Simple Authentication and Security Layer (SASL) port. Initially, Kafka allowed connections on plain text ports, and any application could connect to any existing topic.
* **PayPal Kafka Libraries:** PayPal introduced a set of libraries to ensure security, interoperability and user experience:

  + **Resilient Client Library:** The resilient client library integrates with the discovery service.
  + **Monitoring Library**: The monitoring library publishes critical metrics for client applications, which helps monitor the applications’ health.
  + **Kafka Security Library**: All the applications need SSL authentication to connect to the Kafka clusters. This library pulls the required certificates and tokens to authenticate the application during the startup.
* **Kafka QA Platform:** The older QA environment has a lot of ad-hoc topics, all hosted on a handful of clusters. PayPal redesigned and introduced a new QA platform that provides a one-to-one mapping between production and QA clusters, following the same security standards as the production setup.

## **Monitoring and Alerting**

PayPal's Kafka platform is tightly integrated with its monitoring and alerting systems. Although Apache Kafka provides many metrics by default, they have optimized a subset for quicker issue identification with minimal overhead. Key metrics from brokers, zookeepers, MirrorMakers, and clients monitor application health and underlying machines, triggering alerts at abnormal thresholds. PayPal also developed a custom Kafka Metrics library to filter metrics.

## **Enhancements and Automation**

PayPal automated CRUD operations for clusters and topics, metadata management:

* **Patching security vulnerabilities**: All hosts in the Kafka platform must be patched frequently to resolve any security vulnerabilities. Patching usually requires broker restarts, risking under-replicated partitions and data loss. To prevent this, they developed a plugin to check under-replicated partitions before patching, allowing clusters to be patched in parallel while ensuring only one broker is patched at a time.
* **Topic Onboarding:** Application teams must submit a request via the Onboarding Dashboard to create a new topic. The team reviews the capacity requirements and assigns the topic to an available cluster, determined by the capacity analysis tool integrated into the workflow. A unique token is generated for each new application to authenticate access to the Kafka topic, and ACLs are created based on roles. The application can then successfully connect to the Kafka topic.

  [![](https://substackcdn.com/image/fetch/$s_!Zfig!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F68d57f13-605d-446c-9f6f-60cba03b7eb6_960x600.png)](https://substackcdn.com/image/fetch/$s_!Zfig!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F68d57f13-605d-446c-9f6f-60cba03b7eb6_960x600.png)

  Topic Onboarding workflow — Scaling Kafka to Support PayPal’s Data Growth (2023). [Source](https://medium.com/paypal-tech/scaling-kafka-to-support-paypals-data-growth-a0b4da420fab)
* **MirrorMaker Onboarding**:

  [![](https://substackcdn.com/image/fetch/$s_!9kgE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcf8f5eb2-cbfa-4711-a6e4-e6af0d4325de_1400x924.png)](https://substackcdn.com/image/fetch/$s_!9kgE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcf8f5eb2-cbfa-4711-a6e4-e6af0d4325de_1400x924.png)

  MirrorMaker onboarding workflow — Scaling Kafka to Support PayPal’s Data Growth (2023). [Source](https://medium.com/paypal-tech/scaling-kafka-to-support-paypals-data-growth-a0b4da420fab)
* **Repartition Assignment Enhancements:** By default, Kafka repartitions all partitions, including those on healthy brokers. PayPal modified this to reassign only under-replicated partitions on affected brokers, avoiding long re-partitioning times. Previously, re-partitioning could make clusters unavailable for days, severely impacting availability.

## PayPal’s lessons learned.

* Operating Kafka at a large scale requires tools for regular operations.
* Critical health metrics such as CPU and disk utilization are monitored to ensure high availability and business continuity.
* They introduced ACLs to improve application tracking and security and are on the way to developing automation tools to enhance ACL management.
* Benchmarking cluster performance across various environments (on-premises and cloud) with different configurations has provided insights for operational efficiency.

---

# 📋 The list

────────

[Introduction to Kafka Tiered Storage at Uber](https://www.uber.com/en-SG/blog/kafka-tiered-storage/) — 9 mins, by Uber Engineering Blog

> *Uber proposed Kafka Tiered Storage ([KIP-405](https://cwiki.apache.org/confluence/display/KAFKA/KIP-405%3A+Kafka+Tiered+Storage?uclick_id=15b6739c-0acd-406e-bdf6-884992beefa0)) to avoid tight coupling of storage and processing in a broker. It provides two tiers of storage, called local and remote.*

────────

[The Rise of the Data Platform Engineer](https://databased.pedramnavid.com/p/the-rise-of-the-data-platform-engineer) — 6 mins, by Pedram Navid

> *The next evolution of the role is more akin to a Data Platform Engineer.*

────────

[Why use Apache Airflow (or any orchestrator)?](https://www.startdataengineering.com/post/why-to-use-orchestrators/) — 7 mins, by Start Data Engineering

> *Understanding the needs of complex data pipelines can help you understand the need for a tool like Airflow. This post will cover the three main concepts of running data pipelines: scheduling, orchestration, and Observability.*

────────

[Modern Good Practices for Python Development](https://www.stuartellis.name/articles/python-modern-practices/) — 13 mins, by Stuart Ellis

> *[Python](https://www.python.org/) has a long history, and it has evolved over time. This article describes some agreed modern best practices.*

────────

[Datadog - Timeseries Indexing at Scale](https://www.datadoghq.com/blog/engineering/timeseries-indexing-at-scale/) — 20 mins, Artem Krylysov and May Lee

> *This blog post provides an overview of the Datadog time-series databaseseries indexing at scale. We’ll compare the performance and reliability of two generations of indexing services.*

────────

[No Such Thing As Dirty Data](https://sqlpatterns.com/p/no-such-thing-as-dirty-data) — 3 mins, by Ergest Xheblati

> *There’s no such thing as “dirty data.” Data is either "fit for purpose" or "unfit for purpose." Data "fit for purpose" requires no changes and can be used as is. Data "unfit for purpose" requires "retrofitting" which will ALWAYS cause problems.*

────────

[Deploy Python Stream Processing App on Kubernetes](https://jaehyeon.me/blog/2024-05-30-beam-deploy-1/) — 13 mins, by Jaehyeon Kim

> *The Flink Kubernetes Operator manages the entire deployment lifecycle of Apache Flink applications, simplifying the deployment and management of Python stream processing applications. This series covers deploying a PyFlink application and a Python Apache Beam pipeline on the Flink Runner on Kubernetes.*

---

## 😉 Previously on Dimension

> *Dimension is my sub-newsletter, where I note down things I learn from people smarter than me in the data engineering field. Here is the latest article*

Let me hear your voice, for example:

'Your newsletter is so terrible, I can't handle it anymore.'

[Leave a comment](https://vutr.substack.com/p/groupby-42-paypal-scaling-kafka/comments)

Thanks for scrolling this far! There's a convenient subscribe box here if you want me to annoy you every week. 😄
