---
title: "Netflix’s Trillions Scale Real-time Data Infrastructure"
channel: vutr
author: "Vu Trinh"
published: 2024-12-17
url: https://vutr.substack.com/p/netflixs-trillions-scale-real-time
paid: false
topics: ["Apache Kafka", "Apache Spark", "Apache Iceberg", "Apache Flink", "Data Warehouse", "Streaming", "Change Data Capture", "Data Quality", "ETL"]
tags: [https, they, netflix, time, platform, real]
---

# Netflix’s Trillions Scale Real-time Data Infrastructure

*4 phases, each phase's lessons learned and strategies*

> Source: [Open post](https://vutr.substack.com/p/netflixs-trillions-scale-real-time)

## Topics

[[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[apache-flink|Apache Flink]] · [[data-warehouse|Data Warehouse]] · [[streaming|Streaming]] · [[change-data-capture|Change Data Capture]] · [[data-quality|Data Quality]] · [[etl|ETL]]

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=153027694)

[![](https://substackcdn.com/image/fetch/$s_!PVDN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F74896829-924e-4147-9f21-bc5561fdd380_1400x997.png)](https://substackcdn.com/image/fetch/$s_!PVDN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F74896829-924e-4147-9f21-bc5561fdd380_1400x997.png)

Image created by the author.

---

## Intro

This week, we’ll explore the innovation journey of Netflix's real-time data infrastructure.

> ***Note:** This article my notes after reading an insightful piece by an ex-Netflix engineer. If you have time, I highly recommend reading the [original article](https://zhenzhongxu.com/the-four-innovation-phases-of-netflixs-trillions-scale-real-time-data-infrastructure-2370938d7f01).*

Each of the following sections corresponds to a phase in Netflix's real-time data evolution.

Now, let’s begin.

---

## Phase 1: Moving from the Batch pipelines

In 2015, Netflix had about 60 million monthly subscribers and continued expanding.

At that time, Netflix had approximately 500 microservices, generating more than 10PB data daily.

They needed to collect these data to serve:

* Analytics Insights (e.g., user retention)
* Operation Insights (to understand Netflix systems)

Data must be moved from user-edge devices to Netflix’s internal data warehouse.

By 2015, the data volume had increased to 500 billion events/day (1PB of data ingestion), up from 45 billion events/day in 2011.

The existing batch pipeline platform built with Chukwa, Hadoop, and Hive), failed to handle the increasing data.

> *[Chukwa](https://github.com/apache/chukwa) is an open source data collection system for monitoring large distributed systems. Chukwa is built on top of the Hadoop Distributed File System (HDFS) and Map/Reduce framework.*

[![](https://substackcdn.com/image/fetch/$s_!oIxr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9fcd3d29-4c03-4e00-b667-3d8bdec84fdc_1368x598.png)](https://substackcdn.com/image/fetch/$s_!oIxr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9fcd3d29-4c03-4e00-b667-3d8bdec84fdc_1368x598.png)

Image created by the author. [Reference](https://zhenzhongxu.com/the-four-innovation-phases-of-netflixs-trillions-scale-real-time-data-infrastructure-2370938d7f01)

Based on their estimation then, they only had 6 months to deliver a streaming-first architecture solution.

Despite the strict deadline, they delivered the MVP of [Keystone](https://netflixtechblog.com/keystone-real-time-stream-processing-platform-a3ee651812a), Netflix's real-time processing platform for analytics use cases. Here’s an overview of its architecture:

[![](https://substackcdn.com/image/fetch/$s_!q8Y9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff02541c9-f2db-4c79-ae09-5a8214004d3a_1570x610.png)](https://substackcdn.com/image/fetch/$s_!q8Y9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff02541c9-f2db-4c79-ae09-5a8214004d3a_1570x610.png)

Image created by the author. [Reference](https://zhenzhongxu.com/the-four-innovation-phases-of-netflixs-trillions-scale-real-time-data-infrastructure-2370938d7f01)

There were some reasons for the streaming-first architecture:

* Reducing significantly the developer and operation feedback loop. (Clearly, waiting for a batch pipeline caused some pain here.)
* Providing better product experience. Many of Netflix’s features, such as personalized or “what is trending, “ can significantly benefit from fresher data.

However, shifting a whole data architecture paradigm was not an easy task.

### Challenges

* Limited Resource: They only had 6 months and 6 team members.
* Immature Streaming Ecosystem**:** Back in 2015, Apache Flink and Apache Kafka were not as mature as they are today.
* Concern Difference: Analytical stream processing focuses on correctness and predictability, while operational stream processing cares more about cost-effectiveness, latency, and availability.
* Building a stateful data platform on the cloud is hard: Operating across hundreds of thousands of physical machines in each data center, hardware failures are inevitable at this scale. Ensuring availability and consistency under these conditions is daunting, particularly in an unbounded, low-latency stream processing environment.

Let’s move on to see how Netflix deals with these challenges in the first phases:

### Strategies

* **Focusing on the high-priorities**: Netflix prioritized a few high-volume internal customers, delaying broader scaling for later. This approach allowed them to focus on the product's core while staying mindful of what not to invest in.
* **Working with technology partners:** Netflix collaborated with industry leaders driving stream processing efforts, such as LinkedIn and Confluent. For containerization, they partnered with their internal container infrastructure team—Titus. Built on top of Apache Mesos, Titus provided compute resource management, scheduling, and isolated deployment through an abstracted API. In early 2020, Titus evolved to leverage Kubernetes (K8s), with the team successfully migrating all workloads transparently.
* **Separations**: Netflix separated concerns between producers and consumers to decouple their development workflows. They also distinguished between operational and analytics use cases by developing **[Mantis](https://netflixtechblog.com/stream-processing-with-mantis-78af913f51a6)** (focused on operational use cases) and **[Keystone](https://netflixtechblog.com/keystone-real-time-stream-processing-platform-a3ee651812a)** (focused on analytics). Additionally, Netflix adopted a microservice architecture, dividing the entire infrastructure into three key components: **Messaging** (Streaming Transport), **Processing** (Stream Processing), and **Control Plane**.
* **Failures Expectation:** Netflix embraced DevOps practices, such as design for failure scenarios, automation, continuous deployment, shadow testing, automated monitoring, alerting, etc.

### Lessons

A psychologically safe environment is essential for teams to navigate failure and drive change.

They experienced a significant failure on product launch day, resulting in massive data loss. Despite carefully estimating traffic growth, their Kafka cluster, which had over 200 brokers, hit the limits. When one broker failed, the cluster couldn’t recover due to Kafka’s limitations at the time, ultimately degrading beyond repair.

Thanks to open communication, they addressed the incident transparently and implemented lasting solutions, such as smaller Kafka clusters with isolated Zookeeper instances for better resilience. They recognized the unpredictability of managed cloud environments and adopted the principle of preparing for worst-case scenarios.

To strengthen its operations, Netflix introduced weekly Kafka cluster failover drills. These simulations ensure failover automation can seamlessly migrate traffic to healthy clusters, minimizing user impact and reinforcing system reliability.

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=153027694)

---

## Phase 2: 100s Use Cases

Thanks to the MVP of Keystone, moving logs for analytical processing and gaining operational insights became easier.

The real-time data infrastructure team scaled the architecture to serve more users.

[![](https://substackcdn.com/image/fetch/$s_!gE0v!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feabec18f-3f7a-4722-872e-594208b7b146_1526x968.png)](https://substackcdn.com/image/fetch/$s_!gE0v!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feabec18f-3f7a-4722-872e-594208b7b146_1526x968.png)

Image created by the author. [Reference](https://zhenzhongxu.com/the-four-innovation-phases-of-netflixs-trillions-scale-real-time-data-infrastructure-2370938d7f01)

### Challenges

* **Increased operation burden:**Netflix needed to evolve the MVP to support more than a dozen customers, so some components needed to be rebuilt.
* **More diverse needs:** As demand grew, they began noticing two significant categories of customer requests. One group preferred a fully managed service that was simple and easy to use. The other valued flexibility and required complex computation capabilities to address advanced business problems. This second group was also willing to take on responsibilities like managing some infrastructure and handling pagers.
* **Everything was broken**: They encountered significant challenges during their journey. They broke S3 once and discovered numerous bugs in Kafka and Flink. They also experienced multiple failures with Titus, their managed container infrastructure. Additionally, they broke Spinnaker, the continuous deployment platform, as they began programmatically managing hundreds of customer deployments.

### Strategies

* **Simplicity**: Netflix decided to focus on a highly abstracted, fully managed service for general streaming use cases for two reasons. First, it allows them to address most data movement and simple streaming ETL use cases. Providing such simple, high-level abstraction for data routing would enable engineers across all Netflix organizations to use data routing as a building block in conjunction with other Platform services. Second, it allows their users to focus on business logic.
* **Multi-tenancy**: One customer’s workload should not interfere with another.
* **They will continue to invest in DevOps**. They want to ship platform changes reliably and let customers ship changes anytime they need**.** Deployment should be automatic and safe.

### Learnings

They learned that deciding what *not* to work on is as crucial as prioritizing tasks. While addressing customer requests is essential, some can be distractions. Saying no is difficult but necessary—it’s a temporary decision, unlike the permanence of saying yes. By clearly communicating what’s being deprioritized, they maintained focus and efficiency.

After achieving product-market fit, Netflix found that scaling velocity requires a delicate balance. Scaling too quickly risks tech debt, team burnout, and broken customer trust, while scaling too slowly leaves customers waiting and teams unmotivated. To manage this, Netflix monitored signals like software quality, customer sentiment, and operational overhead, ensuring sustainable growth without compromising reliability or morale.

The team also encountered misconceptions about stream processing, such as concerns over event loss or correctness under failure. They focused on educating users with data and relatable stories to improve the situation. This helped correct misunderstandings and build trust.

---

## Phase 3: Custom Needs and 1000s Use case

After one year of launching Keystone, internal real-time data movement use cases rose from less than 10 in 2015 to a few hundred in 2017.

At this point, they had built a solid operational foundation. The platform team carefully monitored and handled all infrastructure issues. Furthermore, with the efficient delivery platform, the internal user could quickly and safely make changes to the production environment.

However, real-time data infrastructure teams always encounter new needs for more complex processing capabilities, such as streaming joins and event windowing.

They needed to continue expanding the platform.

### Challenges

* Custom use cases require different things: New use cases require more advanced stream processing functions (event-time-based processing, windowing, data lateness control, state management, …). They also require more operational support for observability, recovery, or troubleshooting. In addition, new developer experiences and capabilities are needed, such as more flexible programming interfaces, data backfill support, or infrastructure to handle TBs of the local state.
* The team found it hard to **balance between the flexibility and the simplicity**. If they expose all the low-level APIs, it can offer more flexibility for the users; however, they will find it more challenging to operate. In contrast, if they abstract all the complexities from the users, the operations will be more pleasant; the trade-off is, of course, the flexibility.
* **Operation Complexity Increasing:**Netflix had to improve operation observability in many scenarios to adapt the platform to more custom use cases. Moreover, as the platform must communicate with many other data products, more operational coordination with other teams is required to serve its users better.
* **Centralization vs. Localization:**The real-time data infrastructure team had to convince other teams to use the centralized stream processing platform. Those teams already had a local platform that could use unsupported technology, such as Spark Streaming.

### Strategies

* **New product entry point but refactoring existing architecture:** They created a new platform from the original architecture to provide stream processing capabilities with Apache Flink. The lower Flink platform supports Keystone and custom use cases in this new architecture.
* They began with **the most challenging streaming ETL (analytics) and observability (operational) use cases**. As mentioned in the first point, Netflix would separate stream processing into a dedicated platform, so it makes sense for them to tackle and learn from the most difficult ones first.

### Lessons

Introducing a new product entry point to support custom use cases is a necessary evolution. This transition also presents an opportunity to re-architect and integrate into the existing ecosystem. However, they learned to avoid building new systems in isolation.

Simplicity often meets 80% of use cases, while flexibility addresses the bigger, more complex ones. Netflix observed that deciding whether to prioritize simplicity for the majority or flexibility for high-impact use cases depends on specific business needs. Simplicity and flexibility aren’t opposites but are part of an innovation loop. Flexibility drives co-innovation with select customers, which, once proven, can evolve into a simplified experience as these innovations attract more users and new demands for flexibility emerge, restarting the cycle.

They also emphasized treating early adopters well. These loyal customers often become vocal advocates, helping the product gain traction.

---

## **Phase 4: Expanding**

At this time, processing use cases has expanded to all Netflix organizations. As Netflix's business grew, new challenges emerged for the real-time data infrastructure.

[![](https://substackcdn.com/image/fetch/$s_!rwCv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa5a57bbb-d600-464f-be3c-11aff3f95604_1288x858.png)](https://substackcdn.com/image/fetch/$s_!rwCv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa5a57bbb-d600-464f-be3c-11aff3f95604_1288x858.png)

Image created by the author. [Reference](https://zhenzhongxu.com/the-four-innovation-phases-of-netflixs-trillions-scale-real-time-data-infrastructure-2370938d7f01)

### Challenges

* **Diverse data technologies**: Netflix's internal teams used various data technologies. The transactional databases were Cassandra, Postgres, CockroachDB, and MySQL. There were Iceberg, Presto, Spark, and Druid for the analytics side. Data can be copied into multiple data stores. They found working with data across technology boundaries to be incredibly challenging.
* **Learning Curve**: The growing number of data tools makes it harder for users to learn and choose the right technology for specific use cases. This complexity often slows adoption and decision-making.
* **Machine learning efforts often fail to capitalize on the data platform's potential fully**. Long feedback loops for data scientists, reduced productivity for data engineers, and difficulties in data sharing for product engineers create inefficiencies. These hurdles can cost businesses valuable opportunities to adapt to a rapidly changing market.
* As the central data platform grows to support many use cases, a single point of contact becomes unsustainable. Shifting toward a model that empowers local-central platforms—built on top of the central platform—provides leverage and scalability, ensuring better support and adaptability.

### **Opportunities for the future**

Streams are powerful connectors in modern data platforms. It enables seamless data exchange across diverse technologies. Tools like Change Data Capture (CDC), streaming materialized views, and Data Mesh concepts highlight its growing role in creating interconnected systems.

Raising abstraction is another critical opportunity. While understanding data technology internals is valuable, not everyone needs that depth. With cloud-first infrastructures becoming commodities, simplifying advanced capabilities for broader accessibility is essential. Technologies like streaming SQL lower the barrier to entry, but the potential goes further. Blurring boundaries like streaming versus batch can deliver a unified, user-friendly data platform experience.

Modern data platforms must pay more attention to machine learning. While ML is among the most impactful technologies for businesses, ML teams often lack the tools to thrive. Data platforms can better support ML and unlock its full potential by enhancing data quality, scalability, real-time observability, dev-to-prod feedback loops, and efficiency.

---

## Outro

In this article, I’ve shared my notes on the four phases of Netflix’s real-time data infrastructure journey, from replacing batch pipelines to supporting thousands of use cases across the company.

If you have time, I highly recommend reading the [original article](https://zhenzhongxu.com/the-four-innovation-phases-of-netflixs-trillions-scale-real-time-data-infrastructure-2370938d7f01)—you’ll surely learn much more from it.

Now, it’s time to say goodbye.

---

## Reference

*[1] Zhenzhong Xu, [The Four Innovation Phases of Netflix’s Trillions Scale Real-time Data Infrastructure](https://zhenzhongxu.com/the-four-innovation-phases-of-netflixs-trillions-scale-real-time-data-infrastructure-2370938d7f01) (2022)*

---

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
