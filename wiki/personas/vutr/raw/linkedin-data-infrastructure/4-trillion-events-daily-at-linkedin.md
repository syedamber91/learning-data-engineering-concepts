---
title: "4 Trillion Events Daily at LinkedIn"
channel: vutr
author: "Vu Trinh"
published: 2024-06-08
url: https://vutr.substack.com/p/4-trillion-events-daily-at-linkedin
paid: false
topics: ["Apache Kafka", "Apache Spark", "Streaming", "Batch Processing"]
tags: [linkedin, https, beam, processing, apache, time]
---

# 4 Trillion Events Daily at LinkedIn

*Key insights on how LinkedIn leverages Apache Beam for real-time processing*

> Source: [Open post](https://vutr.substack.com/p/4-trillion-events-daily-at-linkedin)

## Topics

[[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[streaming|Streaming]] · [[batch-processing|Batch Processing]]

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=145014385)

[![](https://substackcdn.com/image/fetch/$s_!oE8M!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ff4879d-fe91-4f06-a1a1-2c3e829a9d61_1404x1010.png)](https://substackcdn.com/image/fetch/$s_!oE8M!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ff4879d-fe91-4f06-a1a1-2c3e829a9d61_1404x1010.png)

Image created by the author

---

## Table of contents

* *Context*
* *Unified Streaming And Batch Pipelines*
* *Anti-abuse & Near Real-Time AI Modeling*
* *Notifications Platform*
* *Managed Streaming Processing Platform*
* *Real-Time ML Feature Generation*

---

## Intro

I don’t know why I am always fascinated by stream/real-time processing. Maybe it is an entirely new world when compared with the batch paradigm. Maybe achieving nearly instant results is more attractive than waiting for a while with the batch pipeline.

By the way, instead of figuring out why I’m so into stream/real-time processing, let’s deep dive into another real-time case study from big tech companies. This time, we will see how LinkedIn handles trillions of real-time events daily with Apache Beam's help.

---

## Context

Every day, LinkedIn's real-time infrastructure has to process about 4 trillion events, with 3000 data pipelines across the data center to serve over 950 million users worldwide. In late 2023, LinkedIn Engineering released an excellent article on how they revolutionized their streaming processing with the help of [Apache Beam](https://beam.apache.org/about/). The framework unified stream and batch processing at Linkedin via the capability of running on [Apache Samza](https://samza.apache.org/) (engine for real-time processing) and [Apache Spark](https://spark.apache.org/) (engine for batch processing), which helps reduce the development cycle for new pipelines from months to days.

> *Apache Beam is a programming model that defines batch and streaming data parallel processing. In other words, Beam lets you specify the desired Dataflow model - a famous real-time processing model from Google for both bound and unbound data sets. I released a detailed article on the Dataflow model not long ago; if you’re interested, you can find it here:*

Before going further, let's see how LinkedIn processes real-time data before adopting Apache Beam. To handle the data ingestion and real-time processing, LinkedIn built a custom stream processing ecosystem primarily with internal tools:

* In 2010, they developed Apache Kafka, an ingestion backbone for its real-time infrastructure.
* They build an in-house distributed streaming processing framework: Samza.
* For the batch processing, they leveraged Spark.
* Spark and Samza build up their lambda architecture.
* Gradually, LinkedIn's engineering team expanded the stream processing ecosystem with [Brooklin](https://github.com/linkedin/Brooklin/) and [Venice](https://github.com/linkedin/venice).
* The first helps internal users easily handle data streaming across multiple stores and messaging systems.
* The latter is a storage system for ingesting batch and stream processing results.

[![](https://substackcdn.com/image/fetch/$s_!e2Ad!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b59e6b7-ac9f-4edb-87b8-79d0bd5dfb9c_1352x785.png)](https://substackcdn.com/image/fetch/$s_!e2Ad!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b59e6b7-ac9f-4edb-87b8-79d0bd5dfb9c_1352x785.png)

Image created by the author. [Reference](https://www.linkedin.com/blog/engineering/data-streaming-processing/revolutionizing-real-time-streaming-processing--4-trillion-event)

However, lambda has a signature disadvantage: it requires maintaining two codebases and two batch and streaming data engines. Thus, the release of Apache Beam in 2016 proved to be a game-changer for LinkedIn. Apache Beam offers an open-source, unified programming model for batch and streaming processing with Python, Go, and Java support. It provided the ideal solution for building and running multi-language pipelines on any engine. LinkedIn began onboarding its first use cases and developed the [Apache Samza runner for Beam](https://beam.apache.org/documentation/runners/samza/) in 2018. By 2019, Beam pipelines were powering several critical use cases.

---

> *To celebrate the launch of **learn-spark** for paid subscribers, the CLI tool that helps you learn Spark faster and more affordably right on your laptop. I’m offering you a **50% discount** on the annual plan—grab it now to get access to the **learn-spark** tool!*
>
> *After becoming a paid subscriber, [visit this link](https://substack-github-sync.vutrinh2704.workers.dev/verify) to get invited to the **learn-spark repo.***
>
> *The offer ends **VERY SOON!***
>
> [50% Annual Plan](https://vutr.substack.com/subscribe?coupon=db8dad0e&utm_content=145014385)

---

## Unified Streaming And Batch Pipelines

[![](https://substackcdn.com/image/fetch/$s_!EOpi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c7b5112-b8a9-4064-b0b2-27bef63b03b4_1346x544.png)](https://substackcdn.com/image/fetch/$s_!EOpi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c7b5112-b8a9-4064-b0b2-27bef63b03b4_1346x544.png)

Image created by the author. [Reference](https://www.linkedin.com/blog/engineering/data-streaming-processing/revolutionizing-real-time-streaming-processing--4-trillion-event)

One of the first use cases in which LinkedIn used Apache Beam involved real-time computations and periodic backfilling requirements. One example is LinkedIn's standardization process; it has a series of pipelines that use AI models to map user inputs, such as job titles or skills, into predefined internal IDs for job recommendations. (e.g., standardize between “a data engineer” and “big data engineer”). This process requires real-time processing capability to adapt to user updates and backfill capability when new AI models are released.

Initially, the backfilling job required over *5,000 GB hours in memory and nearly 4,000 hours of total CPU time.* So, LinkedIn engineers wonder if "is it possible to maintain one codebase but with the ability to run it as either a batch job or streaming job?". Now you can guess the solution to this.

It is Apache Beam.

The Apache Beam APIs enabled LinkedIn engineers to implement business logic once, which can be efficiently run on real-time standardization and backfilling processes. The Beam’s flexibility lets users customize various aspects, such as the pipeline runner and runner-specific configurations. It abstracts away the underlying infrastructure and seamlessly lets LinkedIn switch between data processing engines.

Here are some impressive numbers after they migrated the standardized pipeline to Apache Beam:

* The batch pipeline migration to a unified Apache Beam pipeline resulted in a significant 50% improvement in memory and CPU usage (from ~5000 GB RAM hours and ~4000 CPU hours to ~2000 RAM GB hours and ~1700 CPU hours)
* The processing time improved from 7.5 hours to 25 minutes.

## Anti-Abuse & Near Real-Time AI Modeling

[![](https://substackcdn.com/image/fetch/$s_!orEp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F57eab79a-be6b-470a-bc91-e71955f3042b_1583x378.png)](https://substackcdn.com/image/fetch/$s_!orEp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F57eab79a-be6b-470a-bc91-e71955f3042b_1583x378.png)

Image created by the author. [Reference](https://www.linkedin.com/blog/engineering/data-streaming-processing/revolutionizing-real-time-streaming-processing--4-trillion-event)

The Anti-Abuse AI Team at LinkedIn is responsible for creating, deploying, and maintaining AI and deep learning models that can detect and prevent different forms of abuse, such as fake account creation or member profile scraping. The platform relies on two streaming Apache Beam pipelines:

* The filter pipeline consumes user activity events from Kafka, extracts needed fields, aggregates and filters the events, and outputs them for the downstream pipeline.
* The model pipeline consumes these filtered messages and aggregates member activity in defined time windows. After that, the pipeline triggers AI scoring models and writes the abuse scores to various applications.

Thanks to the flexibility of Apache Beam's pluggable architecture and the support for various I/O options, anti-abuse platform engineers could integrate the pipelines with Kafka and key-value stores. LinkedIn has reduced the time to label abusive actions from 1 day to 5 minutes, with a throughput of over 3 million queries per second.

## Notifications Platform

Apache Beam and Apache Samza power LinkedIn’s large-scale Notifications Platform at Linkedin. The Apache Beam pipelines consume, aggregate, and process events from all LinkedIn users and feed the data to downstream machine-learning models. Then, the models help personalized notifications for LinkedIn members based on their historical actions. As a result, LinkedIn members receive relevant and actionable activity-based notifications.

## Managed Streaming Processing Platform

[![](https://substackcdn.com/image/fetch/$s_!X8dZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3a56d905-6c9c-434e-899d-24d233043c6a_980x683.png)](https://substackcdn.com/image/fetch/$s_!X8dZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3a56d905-6c9c-434e-899d-24d233043c6a_980x683.png)

Image created by the author. [Reference](https://www.linkedin.com/blog/engineering/data-streaming-processing/revolutionizing-real-time-streaming-processing--4-trillion-event)

After some successful pilots, the demand for using Beam for pipeline development increased internally at LinkedIn. Thus, they created the Managed Beam, a platform designed to streamline and automate internal processes of Beam pipeline development. This platform helps users develop Beam pipelines in multiple ways:

* The Beam SDK lets LinkedIn engineers create reusable custom pipelines and expose them as standard [PTransforms](https://beam.apache.org/releases/javadoc/2.0.0/org/apache/beam/sdk/transforms/PTransform.html). These serve as building blocks for new pipelines.
* The platform has a control plane that provides features like deployment UI, operational dashboard, administrative tools, and automated pipeline lifecycle management.
* To ensure the independence of runner processes and user-defined functions (UDFs), Managed Beam packages them as two separate JAR files executed in a Samza container as two distinct processes that communicate through gRPC. This setup enabled LinkedIn to take advantage of automated framework upgrades (The framework upgrades without the concern of broken user logic).
* Manage Beam support auto-sizing controller tool with the help of Beam pipeline report diagnostic information in the form of Kafka topics. The dedicated Beam pipelines process LinkedIn's internal monitoring events and logs before passing them to the auto-sizing controller and writing them to [Apache Pinot](https://open.substack.com/pub/vutr/p/a-glimpse-of-apache-pinot-the-real?r=2rj6sg&utm_campaign=post&utm_medium=web), which is used for Managed Beam's operational and analytics dashboards.
* The Managed Beam control plane then scales LinkedIn's streaming applications and clusters based on the signal from the auto-sizing controller.

## Real-Time ML Feature Generation

[![](https://substackcdn.com/image/fetch/$s_!jtSu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe714996a-7078-4830-b219-516018c5cddb_970x693.png)](https://substackcdn.com/image/fetch/$s_!jtSu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe714996a-7078-4830-b219-516018c5cddb_970x693.png)

Image created by the author. [Reference](https://www.linkedin.com/blog/engineering/data-streaming-processing/revolutionizing-real-time-streaming-processing--4-trillion-event)

At LinkedIn, core functionalities, such as job recommendations and search feeds, heavily rely on ML models. However, before Apache Beam, the original offline machine learning (ML) feature generation pipeline was delayed 24 to 48 hours after LinkedIn member actions.

LinkedIn used Managed Apache Beam to address the challenge.

LinkedIn built a hosted platform for ML feature generation with the Managed Beam as the foundation. The platform provides AI engineers with real-time features while abstracting away deployment and operational complexities:

* First, they create feature definitions and deploy them using Managed Beam.
* The streaming Apache Beam pipeline generates machine learning features by pre-processing the events from Kafka in real-time and output to the feature store.
* Another Beam pipeline is responsible for reading data from the feature store, processing it, and routing the result into the recommendation system.
* This new platform helps them achieve impressive low latency of just a few seconds (instead of 24-48 hours).

---

## Outro

One of the problems with the original real-time solution at LinkedIn is the complexity of the lambda architecture; they have to maintain two codebases and two separate environments.

Apache Beam is first developed to solve problems like this.

Compared to [Twitter's approach](https://vutr.substack.com/p/how-twitter-processes-4-billion-events?r=2rj6sg) when dealing with the challenges of lambda architecture (which I wrote a blog about not long ago, LinkedIn did not choose to pivot the whole solution to the kappa architecture like Twitter did; instead, LinkedIn kept the current architecture, optimized and improved it with the help of Apache Beam.

Thank you for reading this far. Now, see you on the next blog.

---

## **References**

[1] Bingfeng Xia, Xinyu Liu, [Revolutionizing Real-Time Streaming Processing: 4 Trillion Events Daily at LinkedIn](https://www.linkedin.com/blog/engineering/data-streaming-processing/revolutionizing-real-time-streaming-processing--4-trillion-event) (2023)

---

## Before you leave

Leave a comment or contact me via [LinkedIn](https://www.linkedin.com/in/vutr27/) or [Email](http://vutrinh2704@gmail.com) if you:

* Are interested in this article and want to discuss it further.
* Would you like to correct any mistakes in this article or provide feedback?

  + This includes writing mistakes like grammar and vocabulary. I happily admit that I'm not so proficient in English :D

[Leave a comment](https://vutr.substack.com/p/4-trillion-events-daily-at-linkedin/comments)

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
