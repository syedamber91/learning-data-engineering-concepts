---
title: "9 lessons that will put you 3 years ahead as a data engineer"
channel: vutr
author: "Vu Trinh"
published: 2025-12-09
url: https://vutr.substack.com/p/9-lessons-that-will-put-you-3-years
paid: true
topics: ["Data Engineering", "Apache Airflow", "Apache Kafka", "Apache Spark", "Snowflake", "Databricks", "BigQuery", "Data Modeling", "Data Warehouse", "Orchestration", "Change Data Capture"]
tags: [https, auto, substackcdn, image, fetch, good]
---

# 9 lessons that will put you 3 years ahead as a data engineer

*It took me six years to distill these insights, but you can read them in just 10 minutes.*

> Source: [Open post](https://vutr.substack.com/p/9-lessons-that-will-put-you-3-years)

## Topics

[[data-engineering|Data Engineering]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[bigquery|BigQuery]] · [[data-modeling|Data Modeling]] · [[data-warehouse|Data Warehouse]] · [[orchestration|Orchestration]] · [[change-data-capture|Change Data Capture]]

---

> *I will publish a paid article every Tuesday. I wrote these with one goal in mind: to offer my readers, whether they are feeling overwhelmed when beginning the journey or seeking a deeper understanding of the field, 15 minutes of practical lessons and insights on nearly everything related to data engineering.*
>
> [Upgrade subscription](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!0vrG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9bd6b0b2-8499-4cb9-94b2-423608565877_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!0vrG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9bd6b0b2-8499-4cb9-94b2-423608565877_2000x1428.png)

---

## Intro

It has been 6 years since I started this journey. Six years is not very long, but it’s not short either.

I’ve learned a lot from my work and from many great colleagues. There were happy times when I felt enthusiastic, but there were also difficult times when I felt stuck. I don’t know whether what I was doing was right or how to make myself move forward.

I was stuck for three years.

In this article, I will list my 9 lessons that could help you avoid the three years of being stuck like I was as a data engineer.

## Knowing what a data engineer’s responsibility is

I always give this advice to anyone who comes to me asking how to start learning for a data engineer position. I also included this advice in my previous article, but I think it needs to be repeated again and again, given its importance.

[![](https://substackcdn.com/image/fetch/$s_!TDIy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9e60518f-b67a-4587-86a0-14e93163acf5_1264x360.png)](https://substackcdn.com/image/fetch/$s_!TDIy!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9e60518f-b67a-4587-86a0-14e93163acf5_1264x360.png)

The role of a data engineer might be vague. It might depend on your current company status and data maturity. You expect to tune a 6 PB Spark job or deliver insight in under 2 microseconds. But the reality is very different:

You might build dashboards most of the time at company A.

You might build data pipelines extensively at company B.

You might prepare data for ML models (or even train them) at company C.

You might work with a team of more than 30 data engineers at company D

You might be the first one on the data team at company E.

At a different company, the things you will do as a data engineer are different.

The key is to understand the true responsibility of a data engineer. If you’re learning to become a data engineer, this should be the first thing you need to learn.

It helps three things:

[![](https://substackcdn.com/image/fetch/$s_!V6cG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F07520d97-0bd6-43b9-84b9-744d4cdda635_1340x358.png)](https://substackcdn.com/image/fetch/$s_!V6cG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F07520d97-0bd6-43b9-84b9-744d4cdda635_1340x358.png)

* Knowing how to contribute.
* Knowing which knowledge and skills to learn
* Knowing how to avoid tasks that could be done better by other colleagues (e.g., training model should be handled by AI engineers.)

This is important because at the end of the day, when you go to work, you want two things:

* Bringing value to the company
* Growing yourself.

To understand the role of a data engineer, I always suggest reading the first chapter of the book [Fundamentals of Data Engineering: Plan and Build Robust Data Systems](https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/). Here is the author’s definition of data engineering and the data engineer role:

> *Data engineering is the development, implementation, and maintenance of systems and processes that take in raw data and produce high-quality, consistent information that supports downstream use cases, such as analysis and machine learning. Data engineering is the intersection of security, data management, DataOps, data architecture, orchestration, and software engineering. — [Joe Reis](https://www.oreilly.com/search/?query=author:%22Joe%20Reis%22&sort=relevance&highlight=true), [Matt Housley](https://www.oreilly.com/search/?query=author:%22Matt%20Housley%22&sort=relevance&highlight=true)*
>
> *A data engineer manages the data engineering lifecycle, beginning with getting data from source systems and ending with serving data for use cases, such as analysis or machine learning — [Joe Reis](https://www.oreilly.com/search/?query=author:%22Joe%20Reis%22&sort=relevance&highlight=true), [Matt Housley](https://www.oreilly.com/search/?query=author:%22Matt%20Housley%22&sort=relevance&highlight=true).*

## Everything can fail

Although no one wants it, failure can happen in one form or another: bugs in your code, failed machines, bad designs, or low-quality data. The key is not to try to build perfect software that will never fail (that’s impossible). Instead, you must aim to create software that is resilient and easy to investigate when it fails.

[![](https://substackcdn.com/image/fetch/$s_!jRqc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd70e30ae-f53a-4bd2-a483-878f977d1552_1334x520.png)](https://substackcdn.com/image/fetch/$s_!jRqc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd70e30ae-f53a-4bd2-a483-878f977d1552_1334x520.png)

> *I invite you to upgrade your subscription to access my high-quality, human-written data engineering articles.*
>
> [Upgrade subscription](https://vutr.substack.com/subscribe?)

A happy life is when the file arrives on time, the schema matches, the values are not null, and the Spark job runs successfully. In reality, the upstream API will time out. The CSV file will suddenly have a footer row that breaks your parser. The Spark cluster is failing as AWS Spot instances are reclaimed.

When failures occur, your pipeline must be fault-tolerant.

[![](https://substackcdn.com/image/fetch/$s_!G_pJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe3c37c43-1056-4704-b0a3-86bb6874ab1a_836x626.png)](https://substackcdn.com/image/fetch/$s_!G_pJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe3c37c43-1056-4704-b0a3-86bb6874ab1a_836x626.png)

It should continue working as usual or be retried. Gracefully handling exceptions is required, such as filtering out bad input and letting everybody know about it (e.g., via detailed logging). You should also consider the effects of re-runs after the pipeline comes back from recovery: does a re-run produce duplicate data, or did the previous failure cause corrupted data to be persisted?

Additionally, when a failure occurs, there must be a way to investigate the cause. Make sure you:

* **Monitor:** What is the resource utilization when it fails?
* **Log errors clearly:** Why did it fail? Where did it happen? What was the context? What do the tracing spans show?
* **Invest in data lineage:** Which data sources contribute to this dashboard?

## Your work must be understandable.

Speaking of making your pipeline easy to investigate when it fails, that’s also part of this lesson: when you do something, make sure at least one colleague understands what you’re doing:

[![](https://substackcdn.com/image/fetch/$s_!zzkJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff64eec84-9462-49ce-8ef7-a9aa319f14cc_792x496.png)](https://substackcdn.com/image/fetch/$s_!zzkJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff64eec84-9462-49ce-8ef7-a9aa319f14cc_792x496.png)

* Writing documents: the designs, the how-to, the PR/commit messages,…
* Writing readable code: adding comments if it’s complex logic, naming meaningful variables,…

  [![](https://substackcdn.com/image/fetch/$s_!2Dxx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F69c4f968-1cfa-42e8-879b-c9ff9ca8031d_586x410.png)](https://substackcdn.com/image/fetch/$s_!2Dxx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F69c4f968-1cfa-42e8-879b-c9ff9ca8031d_586x410.png)

I have to admit that it’s sometimes really boring. It doesn’t increase your dopamine. However, it’s crucial, and it helps with three things:

* **Collaboration**: You rarely work alone. You need to collaborate. The first factor in successful collaboration is understanding what everyone is doing.
* **Your career path**: Before helping others understand what you’re doing, you must first understand it. This process enables you to think more clearly, which allows you to deliver your work more efficiently. As a result, your work becomes more visible to your boss or to interviewers.
* **Your conscience**: When you take a day off or leave the company, you don’t want to be the only one who knows how to operate the most critical pipeline that supports 90% of the business operations.

Sometimes, the important things are not the exciting ones.

## The simplicity wins

I was responsible for building a data pipeline that provided users with daily insights. You know what I used?

[![](https://substackcdn.com/image/fetch/$s_!4NeM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9376e002-9904-45e2-8add-e502702e2bbe_1124x536.png)](https://substackcdn.com/image/fetch/$s_!4NeM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9376e002-9904-45e2-8add-e502702e2bbe_1124x536.png)

* A CDC pipeline that continuously monitors changes in a PostgreSQL database, routes them to Kafka brokers, and finally syncs the changes to BigQuery tables.
* A real-time pipeline on Google Cloud, using Pub/Sub for message ingestion and Dataflow for data processing.

You know why? That was just because I had just read a book about real-time processing and dreamt of building such a system. The results:

* The team had more things to manage: Debezium, Kafka, Pub/Sub, BigQuery, Dataflow, plus a bunch of Python scripts containing data ingestion and processing logic.
* The billing was high, especially with Dataflow, as we didn’t have much experience working with it.

Given the requirement to refresh the dashboard daily, we could have used a simple batch pipeline orchestrated by Airflow to dump data from the PostgreSQL database and load it into BigQuery. The performance concerns addressed by the CDC pipeline could be handled similarly by running the data export on a read replica.

The key here is to keep everything simple.

[![keep it simple meme](https://substackcdn.com/image/fetch/$s_!_NAG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa21b2e1c-cb32-4241-8d23-0782f393dbbf_679x517.jpeg "keep it simple meme")](https://substackcdn.com/image/fetch/$s_!_NAG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa21b2e1c-cb32-4241-8d23-0782f393dbbf_679x517.jpeg)

[Source](https://www.brendanconnolly.net/keep-it-simple-theres-more-to-it/)

That’s harder than it sounds. Choosing the right tools, along with providing well-designed abstractions to make the code cleaner, requires a lot of time to get right.

You don’t need to rush it. You just need to be aware that complexity doesn’t help, but simplicity does. Simplicity gives you a better chance of creating scalable, understandable, and maintainable solutions.

## Fundamentals > Tools

In the first year of my career, I had FOMO. Every single job description said I needed to know tools A, B, C, and D to get the job.

So, I spent a lot of time learning tools. I ran many Docker containers to get Kafka, Spark, Airflow, HDFS, Trino, MinIO,… up and running. It was fun, but I barely learned any of the tools in depth. I knew that Kafka absorbs data streams, Spark is better than MapReduce because it keeps data in memory, and Airflow lets you write DAGs.

But that was it. I still failed the interviews.

After six years as a data engineer, I’ve realized that learning tools is not wrong, but learning only tools is wrong because tools can become obsolete and be replaced, especially in the AI era, where everything is moving so fast.

You know what never becomes obsolete? The fundamentals.

[![](https://substackcdn.com/image/fetch/$s_!XxTj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4166c9f7-bdb7-4222-8da7-1f49ff31ebb4_786x758.png)](https://substackcdn.com/image/fetch/$s_!XxTj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4166c9f7-bdb7-4222-8da7-1f49ff31ebb4_786x758.png)

Data engineering fundamentals will never change; you need to turn raw data into valuable insights for business users.

The way data is processed, which is not fed into a single machine, will always be split across multiple machines.

The decoupling of storage and compute in cloud data warehouse systems won’t go anywhere soon.

Columnar format always performs better than row format for analytical-heavy read workloads.

And many more.

The advantages of learning fundamentals are:

[![](https://substackcdn.com/image/fetch/$s_!MfRI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e38d065-6d3b-4f00-84e9-1795781a5330_1160x448.png)](https://substackcdn.com/image/fetch/$s_!MfRI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e38d065-6d3b-4f00-84e9-1795781a5330_1160x448.png)

* You can “scale” your learning.

  + For example, you can apply your understanding of OLAP systems to different services from different vendors.
* You can pick up a tool faster.

  + For example, when you understand the fundamentals of OLAP systems, it doesn’t matter much if you work with Snowflake today and BigQuery tomorrow.
* You can point out ‘that’s just marketing.’

  + For example, when a vendor says they have built a ‘super-fast OLAP database with a columnar format,’ you will know most OLAP systems use that columnar format. This is very important, as these days every new solution claims to be the most innovative on the market. (The truth is, they’re not)
* You can create better abstractions.

  + Snowflake, BigQuery, Databricks, Trino? OLAP systems. Airflow, Dagster? Orchestrators. Kafka, Google PubSub, Amazon Kinesis? Message systems. You become tool agnostic. When you design or plan, you don’t see fifty different tools; you see fundamental patterns: messaging systems, OLTP databases, OLAP databases, processing engines…

Speaking of designing and planning, you need to look from a higher level.

## Start to look from a higher place

When you are starting, your world is small.

It consists of a Jira ticket, a Python or SQL script, a specific bug, an Airflow DAG, or a Spark job. You are looking at the ground, ensuring every detail works as expected.

Then, you need to get in the helicopter to understand two things:

[![](https://substackcdn.com/image/fetch/$s_!e4Z-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0e6a9f06-bc2a-471c-a4ae-3719c92b513d_1924x992.png)](https://substackcdn.com/image/fetch/$s_!e4Z-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0e6a9f06-bc2a-471c-a4ae-3719c92b513d_1924x992.png)

* **Why you’re doing this**: Some tasks bring value, and some don’t. Some tasks can be delivered more efficiently. Being curious about what you’re doing is the first step toward focusing on work that truly contributes to your company’s success, along with your own growth. That curiosity also motivates you to find better solutions to problems.
* **The bigger picture**: you’re not just coding a pipeline that someone else designed forever. You have to step up to design and plan things. That’s the fastest way to climb the career ladder.

  [![](https://substackcdn.com/image/fetch/$s_!NbeI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3700f70f-7f28-4fce-a887-fc993a75b09f_1308x614.png)](https://substackcdn.com/image/fetch/$s_!NbeI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3700f70f-7f28-4fce-a887-fc993a75b09f_1308x614.png)

  + When you do that, you become responsible for bigger problems, which means you have a greater chance to make a huge impact. But to do that, you must rise above the details, temporarily forget the ground-level work, and draw the bigger picture.
  + Only then can you communicate your ideas (business users don’t care what your Spark jobs look like), design the architecture, choose the tech stacks, and connect everything. When you stand from a higher place, your view becomes broader.

## The problem is not always clear.

When you look from a higher place, the problem isn’t always as straightforward as it appears in your Jira ticket. The problem is shifting more to the business side than the technical side. The problems are not about how to run your Spark job or how to reduce the execution time of an Airflow task; it will get more and more vague:

[![](https://substackcdn.com/image/fetch/$s_!9sXr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8b74ce67-c496-47a4-b036-754233629b42_930x744.png)](https://substackcdn.com/image/fetch/$s_!9sXr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8b74ce67-c496-47a4-b036-754233629b42_930x744.png)

* Why don’t users trust our data?
* Finance says revenue is $1M, while marketing says it’s $1.2M—both pulled from the data warehouse. Why is there a discrepancy?
* Is there a way to improve Spark and Airflow development productivity in our team?
* The data trend is dropping, but the pipeline ran successfully. Why is that?

And even more strategic ones:

* How to build a data foundation that backs our business operations in the next 10 years
* How to enable a better data analytics company for non-technical users.

All these questions share two things:

* It’s hard to grab all the aspects of the problems at the first sign: why it happens and how to solve it.
* If you solve it, a very high chance that you’re making a big impact.

It’s more vague than ‘how to run your Spark job’ because the problems happen at a larger scale. They no longer live only in your IDE; they involve your whole team, multiple other teams, or even the entire company. This also explains why, when you solve these problems, you provide more value.

[![](https://substackcdn.com/image/fetch/$s_!qAPE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6a7590d0-a7e5-4b7b-b374-fdb1d68f1f49_924x452.png)](https://substackcdn.com/image/fetch/$s_!qAPE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6a7590d0-a7e5-4b7b-b374-fdb1d68f1f49_924x452.png)

Then, when it involves more people, you have to communicate, and human language is not binary like your code; it’s fuzzy. That makes understanding and solving the problem even harder.

But as I said, it’s worth it. You will make a bigger impact. A bigger impact always goes along with salary raises and promotions.

Crystal-clear problems are always more comfortable than vague ones, because you feel great when you understand the problem and how to solve it. But to grow, you must embrace vague problems, learn how to frame them, break them into smaller parts, and prioritize what needs to be done.

## The fastest way to learn a thing: do, fail, have someone point out, and repeat

As the section title says, if you want to learn anything new, you have to do it, get feedback, and repeat what you’ve done using the lessons you learn from that feedback.

Don’t do things silently. Don’t be afraid to expose what you’re doing to the world.

Unlike those with experience, when we’re learning something, there’s little chance we’ll do it correctly or know what the ‘right way’ looks like. You have to show your work to others—maybe your senior colleagues, your boss, your friends, or an online community—so they can point out what you’re doing wrong and you can adjust right away. The sooner you get feedback, the sooner you learn.

[![](https://substackcdn.com/image/fetch/$s_!dbCA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb529f226-4014-47c1-bf74-7e2cce60f4ff_488x436.png)](https://substackcdn.com/image/fetch/$s_!dbCA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb529f226-4014-47c1-bf74-7e2cce60f4ff_488x436.png)

This is also true when you’re learning new concepts. Even if you can’t show a tangible result like code or pipelines, you can still share your current understanding of the concept. You don’t need to explain the concept perfectly; just share what your brain is thinking about it.

The rise of AI tools such as Gemini and ChatGPT makes it even easier to create a feedback loop. In the past, you had to join a company, bravely ask someone on the internet (who often wouldn’t reply), or join an online community while fearing judgment. But now you can open your browser, go to Gemini, show your work, and ask for feedback.

However, using AI for feedback must be done with caution. As you might know, they are also ‘learners’, they learn from large amounts of data on the internet to generate answers, so there’s a chance that what they show you might not be the ‘right’ way of doing a thing.

Learning new things is essential for a data engineer, as we work in a field that requires knowledge across many domains, from software engineering and DevOps to distributed systems and business.

## Data modeling is important.

From my experience, data modeling is one of the first things your company should address when building a data foundation. I borrow the definition of data modeling from Joe Reis here:

> A data model is a structured representation that organizes and standardizes data to enable and guide human and machine behavior, inform decision-making, and facilitate actions. — [Joe Reis](https://joereis.substack.com/p/my-definition-of-data-modeling-for)

I believe explaining the importance of data modeling and the consequences of doing it incorrectly deserves an entire dedicated article. In brief, data modeling facilitates communication between the data and business teams and guides how the organization transforms, organizes, and serves data.

It’s like a blueprint.

[![](https://substackcdn.com/image/fetch/$s_!Tk45!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd82fe821-b505-4bf5-b320-f7d14e4781c6_930x448.png)](https://substackcdn.com/image/fetch/$s_!Tk45!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd82fe821-b505-4bf5-b320-f7d14e4781c6_930x448.png)

If your company doesn’t have it, you will soon see:

* It takes a lot of time to figure out the business rules for a new pipeline.
* It takes a lot of time to find the required data.
* There are multiple ways to calculate the same metric.
* There are multiple ways to represent an entity (e.g., country, address).
* It’s hard to reuse anything
* …

Some might argue that data modeling was only required in the past when OLAP systems were not as fast as they are today. That’s not true. Although data modeling could improve query performance, its ultimate goal is to “enable and guide human and machine behavior, inform decision-making, and facilitate actions.”

Some might also see data modeling as time-consuming and skip it to deliver results faster. That’s true, it requires significant effort and involves many people from different departments. But it’s not true that your organization doesn’t need data modeling. You will see results faster, but the side effects and costs will appear as your company grows and scales with more business flows and entities.

[![](https://substackcdn.com/image/fetch/$s_!eLH-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa64d870b-8690-43e4-8004-252339a9c3d6_1004x630.png)](https://substackcdn.com/image/fetch/$s_!eLH-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa64d870b-8690-43e4-8004-252339a9c3d6_1004x630.png)

Data modeling isn’t going anywhere anytime soon, especially in the age of AI. If we don’t understand how to transform, organize, and serve the data, how can the machine know?

## Outro

In summary, keep these lessons in mind:

* Know what a data engineer should do
* Embrace and prepare for failure
* Explain clearly what you’re doing
* Simplicity > Complexity
* Fundamentals > Tools
* Look at the bigger picture to tackle higher-impact problems
* Understanding a problem is an essential skill
* When learning, create a feedback loop
* Data modeling is not dead

Thank you for reading this far. See you in my next article.
