---
title: "How Did LinkedIn Handle 7 Trillion Messages Daily With Apache Kafka?"
channel: vutr
author: "Vu Trinh"
published: 2024-08-13
url: https://vutr.substack.com/p/how-did-linkedin-handle-7-trillion
paid: false
topics: ["Apache Kafka", "Apache Spark", "Streaming"]
tags: [https, kafka, linkedin, auto, image, branch]
---

# How Did LinkedIn Handle 7 Trillion Messages Daily With Apache Kafka?

*Was adding more machines enough?*

> Source: [Open post](https://vutr.substack.com/p/how-did-linkedin-handle-7-trillion)

## Topics

[[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[streaming|Streaming]]

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=147526484)

[![](https://substackcdn.com/image/fetch/$s_!Xh7N!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc155ff5e-ec64-4517-8a2d-aaf897270248_1398x1001.png)](https://substackcdn.com/image/fetch/$s_!Xh7N!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc155ff5e-ec64-4517-8a2d-aaf897270248_1398x1001.png)

Image created by the author.

---

## Intro

I spent a decent amount of time learning the Apache Kafka concept, theory, and architecture. Observing Kafka from the perspective of the ski driver falling at 10,000 feet, it has a dead simple architecture: the brokers contain the topic, the producers are responsible for data writing, and the consumer is responsible for reading the data. Even with its simplicity, Kafka has become a core part of the infrastructure for companies of all sizes.

In this week's newsletter, we will learn how the company that created Kafka — LinkedIn, operates the message system to help them handle 7 trillion messages daily. (The number is referenced from an article in 2019. Thus, the statistic must be more significant now)

---

## Overview

If you have not impressed with the statistics yet, here are some more numbers:

[![](https://substackcdn.com/image/fetch/$s_!jqSK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdca39dd2-3f4b-4ec1-aeee-48a99438ccee_1800x1800.png)](https://substackcdn.com/image/fetch/$s_!jqSK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdca39dd2-3f4b-4ec1-aeee-48a99438ccee_1800x1800.png)

Image created by the author.

* 100 Kafka Cluster
* 4000 Kafka Brokers
* 100,000 topics
* 7,000,000 partitions

At LinkedIn, Kakfa is leveraged for a wide range of use cases; here are some large categories:

[![](https://substackcdn.com/image/fetch/$s_!rGjh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F01570242-4b4d-43c6-b0e8-fe58cfc19cb5_2000x500.png)](https://substackcdn.com/image/fetch/$s_!rGjh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F01570242-4b4d-43c6-b0e8-fe58cfc19cb5_2000x500.png)

Image created by the author.

* **Decoupling the sender and receiver**: one part of the application produces messages, while another part consumes them.
* **Monitoring**: Kafka acts as the event bus to receive monitoring metrics from the agents. LinkedIn installs agents in the servers to collect application-generated measurements, such as CPU, RAM utilization, etc…
* **Logging**: LinkedIn routes application, system, and public access logs to Kafka.
* **Tracking**: Tracking involves every action, whether by users or applications. This data is crucial for keeping search indices current, tracking paid service usage, and measuring growth in real time. LinkedIn uses stream processing systems like Samza to process action data from Kafka.

LinkedIn needs to operate Kafka in the most reliable and scalable way to manage its vast data and support a variety of use cases. In the following sections, we'll explore how LinkedIn achieves these goals.

## Tiers and Aggregation

[![](https://substackcdn.com/image/fetch/$s_!IZPa!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa283681b-788d-43a7-823f-772961306125_1454x784.png)](https://substackcdn.com/image/fetch/$s_!IZPa!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa283681b-788d-43a7-823f-772961306125_1454x784.png)

Image created by the author.

An internet-scaled company like LinkedIn runs its infrastructure across multiple data centers.

Some applications only care about what is happening in a single data center, while others, such as building search indexes, need to operate across multiple data centers.

LinkedIn has a local cluster deployed in each data center for each message category. There is an aggregate cluster, which consolidates messages from all local clusters for a given category. With this strategy, the producer and consumer can interact with the local Kafka cluster without reaching across data centers.

Initially, they used Kafka Mirror Maker to copy data from the local to the aggregate cluster. Later, they encountered a scaling issue with this replication tool, so they switched to [Brooklin](https://www.linkedin.com/blog/engineering/open-source/brooklin-open-source), an internal solution that allows data to be streamed across different data stores.

When reading data, LinkedIn deploys consumers to consume data from the brokers in the same data center when reading data. This approach simplifies the configuration and avoids cross-datacenter network issues.

We can now see the tier of Kafka deployment at LinekdIn:

* **First tier:** Producer
* **Second tier:** Local cluster (across all data centers)
* **Additional tiers:** Aggregate clusters
* **Final tier:** Consumer

Operating at the many tiers raises a concern: the completeness of Kafka's message when it has gone through many tiers. LinkedIn needs a way of auditing.

## Auditing Completeness

[![](https://substackcdn.com/image/fetch/$s_!wubj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F340d4837-3d4b-46fd-84d5-59888ef15e6a_1137x684.png)](https://substackcdn.com/image/fetch/$s_!wubj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F340d4837-3d4b-46fd-84d5-59888ef15e6a_1137x684.png)

Image created by the author.

Kakfa Audit is an internal tool at LinkedIn that ensures sent messages do not disappear when copied through tiers.

When the producer sends messages to Kafka, it tracks the count of messages sent during the current time interval. Periodically, the producer sends this count as a message to a special auditing topic.

On the consumption side, audit consumers from the Kafka Console Auditor application will consume messages from all topics alongside the consumers from other applications.

Like the producer, audit consumers periodically send messages into the auditing topic, recording the number of messages they consume for each topic.

The LinkedIn engineers will compare the message count from producers and audit consumers to check if the message has landed in Kafka.

If the numbers are different, there must be a problem with the producer. Their engineers can trace the specific service and host responsible to them.

Tracing is possible because the Kafka message’s schema at LinkedIn contains a header that includes metadata like the timestamp, the originating physical server, and the service.

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=147526484)

---

## LinkedIn Kafka release branches

LinkedIn maintained internal Kafka release branches to deploy their production environment.

[![](https://substackcdn.com/image/fetch/$s_!njFl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe93862e7-a56b-411d-b299-49e1c4073cc8_690x492.png)](https://substackcdn.com/image/fetch/$s_!njFl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe93862e7-a56b-411d-b299-49e1c4073cc8_690x492.png)

Image created by the author.

Their goal is to keep their internal branch close to the open-source Kafka release branch, which helps them leverage new features or hotfixes from the community and allows LinkedIn to contribute to Apache Kafka's open source.

LinkedIn engineers create an internal release branch by [branching](https://git-scm.com/docs/git-branch) from the associated Apache Kafka branch; they call this the upstream branch.

They have two different approaches to commit Kafka patches developed at LinkedIn:

[![](https://substackcdn.com/image/fetch/$s_!_X6z!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc1cda4d6-746a-438e-9dd1-5a89126bb457_659x450.png)](https://substackcdn.com/image/fetch/$s_!_X6z!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc1cda4d6-746a-438e-9dd1-5a89126bb457_659x450.png)

Image created by the author.

* They commit changes to the upstream first, and if necessary, they issue a [Kafka Improvement Proposal (KIP)](https://cwiki.apache.org/confluence/display/KAFKA/Kafka+Improvement+Proposals). Then, they cherry-pick them to their current LinkedIn release branch. This method is suitable for changes with low to medium urgency.
* They commit to the internal release branch first, then to upstream later. This method is suitable in high-urgency scenarios.

Keeping their release branch close to the upstream branch is a two-way process; in addition to syncing their internal patch to the upstream branch, they also need to cherry-pick patches from upstream branches to their internal ones. There are the following types of patches in the LinkedIn release branch:

* Patches from the upstream Kafka branch up to the branch point.
* Cherry-picked patches from the upstream branch after the branch point.
* Hotfix patches that are committed to the internal branch first and are prepared to be committed to the upstream branch.
* LinkedIn-only patches appear only in the internal release branches. They tried to commit to upstream branches but were rejected by the open-source community.

Here is the LinkedIn Kafka development workflow:

[![LinkedIn-development-workflow](https://substackcdn.com/image/fetch/$s_!e-pw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4138c719-5913-40e7-adc9-f0370021c1e0_982x1104.png "LinkedIn-development-workflow")](https://substackcdn.com/image/fetch/$s_!e-pw!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4138c719-5913-40e7-adc9-f0370021c1e0_982x1104.png)

LinkedIn’s Kafka development workflow*,* [How LinkedIn customizes Apache Kafka for 7 trillion messages per day](https://www.linkedin.com/blog/engineering/open-source/apache-kafka-trillion-messages) (2019)

* If there is a new issue:

  + If the patch exists in the open-source Apache Kafka branch, they can cherry-pick from the upstream branch or catch up with this patch later in the next rebase.
  + If the patch does not exist in the upstream branch, it is attempted to be committed to both the upstream and internal branches.
* If there is a new feature:

  + They will attempt to commit the patch to the upstream and internal branches. When committing to the upstream, they will issue the KIP if needed.

The LinkedIn engineers will choose the Upstream First route or LinkedIn First route based on the urgency of the patch. Typically, patches addressing production issues are committed as hotfixes first. Feature patches for approved KIPs should go to the upstream branch first.

---

## **Outro**

Efficiently operating the data infrastructure that can process a massive scale of data is not a simple task. Adding more machines can not solve all the problems. Through the article, we’ve learned how LinkedIn operates Kafka to handle trillions of messages daily: from how they organize Kafka clusters across their data centers, how they ensure message completeness, and finally, their Kafka deployment workflow.

---

## **References**

*[1] Todd Palino, [Running Kafka At Scale](https://engineering.linkedin.com/kafka/running-kafka-scale) (2015)*

*[2] Jon Lee, [How LinkedIn customizes Apache Kafka for 7 trillion messages per day](https://www.linkedin.com/blog/engineering/open-source/apache-kafka-trillion-messages) (2019)*

---

## Before you leave

If you want to discuss this further, please leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/), [Email](http://vutrinh2704@gmail.com), or [Twitter](https://x.com/_vutrinh).

[Leave a comment](https://vutr.substack.com/p/how-did-linkedin-handle-7-trillion/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
