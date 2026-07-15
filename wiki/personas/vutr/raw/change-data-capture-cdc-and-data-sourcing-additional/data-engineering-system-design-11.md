---
title: "Data engineering system design: 11 data sourcing problems"
channel: vutr
author: "Vu Trinh"
published: 2026-04-29
url: https://vutr.substack.com/p/data-engineering-system-design-11
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Kafka", "Apache Spark", "Orchestration", "Streaming", "Change Data Capture", "Data Quality"]
tags: [https, auto, source, fetch, good, substackcdn]
---

# Data engineering system design: 11 data sourcing problems

*The part of the pipeline you don't control*

> Source: [Open post](https://vutr.substack.com/p/data-engineering-system-design-11)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[orchestration|Orchestration]] · [[streaming|Streaming]] · [[change-data-capture|Change Data Capture]] · [[data-quality|Data Quality]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=194761871)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!gpor!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F716f76f7-5a14-4ef3-95aa-b82f5c1ae0de_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!gpor!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F716f76f7-5a14-4ef3-95aa-b82f5c1ae0de_2000x1429.png)

---

# Intro

After writing about [orchestration](https://vutr.substack.com/p/data-engineering-system-design-orchestration) and [serving layer](https://open.substack.com/pub/vutr/p/data-engineering-system-design-9?r=2rj6sg&utm_campaign=post&utm_medium=web) in data engineering system designs, the next part of the series will be about sourcing, the beginning of any data pipeline, and also the root cause of most of the problems.

In this article, I discussed 11 source problems:

1. What is the type of the source?
2. How often do I need to touch the source?
3. How will the source performance be impacted?
4. How long does the source retain the data?
5. Does the source have the fields I need?
6. If the schema changes, how will I know?
7. How do I access the data?
8. Can I read the source exactly once?
9. How does the source handle deletes?
10. What is the data quality contract with the source?
11. Is the source available when I need it?

In each section, I will explain what information we could have when we answer the question, and from that, we can design a better data system.

> ***Note 1**: What is discussed in this article is based solely on my observations and experience; feel free to provide feedback on anything you see I may have missed.*

---

# The mental model

The source is the one part of your pipeline you don’t fully control.

In most cases, you don’t own and build it. Or maybe you don’t know where it came from. There's a very high chance you won’t know what changes and breaks until they're reflected in the downstream.

But the team/vendor responsible for the source might know.

[![](https://substackcdn.com/image/fetch/$s_!BUX8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7a708e60-9d07-4dee-b2d6-8a741a5c225c_670x602.png)](https://substackcdn.com/image/fetch/$s_!BUX8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7a708e60-9d07-4dee-b2d6-8a741a5c225c_670x602.png)

Who owns the source?

That reality shapes every question in this article. This is why clear communication with the source team/vendor matters as much as the technical setup. So before you design or write code, find out who owns the source.

Is it a supported product with an on-call team, or a side project someone built two years ago and hasn’t touched since? Is there a documented SLA? Will they tell you before they deprecate an API version, change a field, or even migrate to a new database?

—

The questions in this article are the ones I keep asking whenever I design an ingestion pipeline.

Let’s go with the first one: What is the type of the source?

---

# What is the type of the source?

API, database, or someone (aggressively) pushes data into our systems.

[![](https://substackcdn.com/image/fetch/$s_!XNqb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0db2bf11-c4bb-4214-9c63-3fcb8520c82e_400x600.png)](https://substackcdn.com/image/fetch/$s_!XNqb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0db2bf11-c4bb-4214-9c63-3fcb8520c82e_400x600.png)

This is the first question because the answer changes everything: the infrastructure you need, the kind of connection to leverage, or the failure modes you have to prepare for.

The main categories are:

**Pull-based**: “knock, knock, give me some data. “

[![](https://substackcdn.com/image/fetch/$s_!JARd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F05f95bac-af7d-4231-a2dc-75fe2ce0fe47_590x306.png)](https://substackcdn.com/image/fetch/$s_!JARd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F05f95bac-af7d-4231-a2dc-75fe2ce0fe47_590x306.png)

* Databases (Postgres, MySQL): you query them directly or export from them
* APIs (REST or GraphQL): you call endpoints, handle pagination, follow rate limits, and parse the result to the desired format.
* File: Someone lands an object in the S3, you wake up and pick up the file.
* Kafka: Even consuming Kafka is a pulling model; you, the consumers, continuously poll the broker (“knock, knock”) for new messages.

**Push-based**: “shut up and receive the data. “ An example is the webhook: the source calls your endpoint when something happens.

[![](https://substackcdn.com/image/fetch/$s_!LjGo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6db8acf6-6589-472c-8b66-08e2aa642356_564x148.png)](https://substackcdn.com/image/fetch/$s_!LjGo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6db8acf6-6589-472c-8b66-08e2aa642356_564x148.png)

Why does this matter?

Because each type requires a different setup. A database source might need a read replica to avoid affecting production query performance. An API source needs pagination logic and rate limit handling. A push-based source requires you to run a receiver that’s always available and can “absorb” the peak workload.

---

# How often do I need to touch the source?

This question is tightly connected to one in [the article which we discussed about serving: “How old can the data be before it is considered stale?”](https://vutr.substack.com/p/data-engineering-system-design-9?r=2rj6sg&utm_campaign=post&utm_medium=web&triedRedirect=true)

[![](https://substackcdn.com/image/fetch/$s_!FyqP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2631faa3-ea8a-4858-80b6-a8c9d0f70b65_788x608.png)](https://substackcdn.com/image/fetch/$s_!FyqP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2631faa3-ea8a-4858-80b6-a8c9d0f70b65_788x608.png)

If the answer is hourly, daily, or weekly, a scheduled batch job (e.g., Cron, Airflow) is fine. If the answer is near real-time, you might need continuous extraction from the source: CDCs, streaming consumers (e.g., Kafka consumer), or sensors that react to new data as it arrives. (e.g., Airflow sensor)

My principle is simple here: **don’t over-engineer the freshness**. (or anything in life)

If the user views the dashboard once a day (and calls the daily data update “real-time”), there’s no reason to build a streaming pipeline. However, keep in mind that there’s a harder question hiding inside:

### How do I know what’s new?

On each run, which records should I actually fetch? Reading the entire table every time is wasteful, and for super-large tables, it’s often impractical.

The common approaches:

* **Timestamp-based extraction** (`WHERE updated_at > last_run_time`): simple, and it works until someone updates a record and forgets advancing the timestamp (the **updated\_at** usually gets the current timestamp when the record is updated if the database admin configures it correctly).

  [![](https://substackcdn.com/image/fetch/$s_!Fm3K!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd1030ffa-262f-4ce9-a9cd-bada8df4fcc5_500x326.png)](https://substackcdn.com/image/fetch/$s_!Fm3K!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd1030ffa-262f-4ce9-a9cd-bada8df4fcc5_500x326.png)
* **Overlap date range**: In today, you will fetch data from X days ago. Tomorrow, you will do the same. There will be overlap in the date range across executions; however, this ensures you can capture data changes within the X interval. Usually, deduplication happens downstream incrementally with the last-come, first-served approach. (e.g., January 1st data in today's execution will be kept, and the one from yesterday's execution will be discarded)

  [![](https://substackcdn.com/image/fetch/$s_!_-FZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7b7c2410-c023-4c1e-b42f-27ac27a37bab_1138x536.png)](https://substackcdn.com/image/fetch/$s_!_-FZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7b7c2410-c023-4c1e-b42f-27ac27a37bab_1138x536.png)
* **Offset-based**: Kafka offsets are an example; the consumer will tell the broker which offset it consumed and continuously poll the broker for new messages.

  [![](https://substackcdn.com/image/fetch/$s_!Ofgx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc7c30535-17f5-4007-93c6-2cfd57986a34_834x392.png)](https://substackcdn.com/image/fetch/$s_!Ofgx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc7c30535-17f5-4007-93c6-2cfd57986a34_834x392.png)
* **CDC**: the source emits every change as an event. The most reliable option when available. (also the most complicated one)

  [![](https://substackcdn.com/image/fetch/$s_!mxhS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F09a40666-f4aa-4639-9301-8ede8b0fa4ea_1198x388.png)](https://substackcdn.com/image/fetch/$s_!mxhS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F09a40666-f4aa-4639-9301-8ede8b0fa4ea_1198x388.png)
* **Full refresh**: sometimes the right answer for small, stable reference tables.

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=194761871)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

# How will the source’s performance be impacted?

This question is about being a good consumer. This will help you retrieve data more reliably for both your pipeline and the source. A full table scan on a production database at peak time (and crash it) is not a great idea.

The impact depends on the type of source. For example:

* **For databases**, the risk is query pressure. Full-table scans can spike CPU usage or lock rows in a production database. Work with the backend team to set up a read replica; your pipeline reads from the replica, leaving the master (the one that accepts writes) untouched. CDC via logical replication is gentler (but requires more setup) than periodic bulk exports because it leverages the replication log rather than querying live data.

  [![](https://substackcdn.com/image/fetch/$s_!_M-Y!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1461b8cb-14d9-425a-9b79-a26faea34067_756x366.png)](https://substackcdn.com/image/fetch/$s_!_M-Y!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1461b8cb-14d9-425a-9b79-a26faea34067_756x366.png)
* **For APIs**, rate limiting is the concern. Implement exponential backoff and retry logic. Use bulk endpoints when available; don’t fetch a million records by one call at a time when a bulk export endpoint exists. Concurrent calls can hit rate limits faster than you expect. For example, running backfill in Airflow with hundreds of DAGs running concurrently could easily hit the API rate limit.

  [![](https://substackcdn.com/image/fetch/$s_!s_hM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5b5b8d30-b9b8-45e7-84a2-8c6cb8342a98_978x514.png)](https://substackcdn.com/image/fetch/$s_!s_hM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5b5b8d30-b9b8-45e7-84a2-8c6cb8342a98_978x514.png)
* **For files in object storage**, the source itself is rarely the bottleneck. But listing large buckets frequently or making unnecessary GET requests could increase your billing.
* **For streams like Kafka**, a slow consumer that can’t keep up with the producer causes the lag (the comparison between the message producing and consuming speed; a high lag indicates your consumer is having some trouble keeping up). At some point, the broker has to retain more data than its retention policy allows, or your consumer falls so far behind that it misses data entirely. Monitor consumer lag. Size your consumers to keep up.

  [![](https://substackcdn.com/image/fetch/$s_!g2s4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F12335855-393c-487f-8610-1880d1da5c2b_2192x316.png)](https://substackcdn.com/image/fetch/$s_!g2s4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F12335855-393c-487f-8610-1880d1da5c2b_2192x316.png)

The principle here is that the source team should not see your pipeline appear at an abnormal point in their monitoring dashboard.

---

# How long does the source retain the data?

If you need 30 days of data but the source only keeps the last 48 hours, no pipeline design can fix it.

[![](https://substackcdn.com/image/fetch/$s_!SIVv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe370199f-9462-471e-9db7-c4d1baeb5a9a_818x502.png)](https://substackcdn.com/image/fetch/$s_!SIVv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe370199f-9462-471e-9db7-c4d1baeb5a9a_818x502.png)

This question is important in two ways.

* First, it tells you whether the source can give you the data range you need. If there’s a mismatch between what the business needs and what the source retains, that’s when you need to negotiate with the source team or/and the business users.
* Second, it guides your recovery options. For this purpose, we can first land the data in object storage and leave it as such, so we can retain the source data longer without relying on the source.

One small consideration is whether the source is replayable.

A Kafka topic with 7-day retention lets you replay any event in that window by resetting the consumer offset. However, a REST API that only returns the current state of a report doesn't let you replay changes; once you’ve missed a change, it’s gone. Again, storing the data in object storage and leaving it as such could also help with the non-replayable source.

---

# Does the source have the fields I need?

This question might sound silly, but there are cases where I plan everything to build a pipeline, only to postpone it because I can’t find a required field in the source.

[![](https://substackcdn.com/image/fetch/$s_!M3ID!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F93e5890d-0a78-4bdb-b2ed-c126f5073021_1216x446.png)](https://substackcdn.com/image/fetch/$s_!M3ID!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F93e5890d-0a78-4bdb-b2ed-c126f5073021_1216x446.png)

If you design correctly, you will start from the user requirement and the desired output. You will know what the [serving layer](https://open.substack.com/pub/vutr/p/data-engineering-system-design-9?r=2rj6sg&utm_campaign=post&utm_medium=web) needs. From there, we work backward and see what we need to collect from the source.

* Does the source actually contain the fields required to produce that output? Are they at the right grain?
* Sometimes “the source” isn’t one instance. It’s a database, an API, and a file drop, and you need all three to gather all the required fields. That’s worth knowing at design time, not after you’ve built half the pipeline.

  + This information also affects other decisions. For example, when you develop the orchestration logic, if it requires data from three different sources, we can have three tasks pull data simultaneously and only proceed to the next task if all three have passed.

---

# If the schema changes, how will I know?

Knowing the schema today is only 50% of the story.

Schemas will change. Columns will be renamed. A field that was a string yesterday, then becomes an integer today, or a column that 10 pipelines depend on is removed.

[![](https://substackcdn.com/image/fetch/$s_!xdKm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc1d7e3fc-ceef-4c03-81ef-8d975f752198_1834x802.png)](https://substackcdn.com/image/fetch/$s_!xdKm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc1d7e3fc-ceef-4c03-81ef-8d975f752198_1834x802.png)

All of them can happen without any prior warning or notification. The flow looks something like this: the source team changes the schema, your pipeline fails that day, you violate the business SLA, and only then do you know about the changes.

The types of schema changes and their “severity”:

* **Additive** (new column added): usually safe, your existing queries usually ignore it if you don’t SELECT \*.
* **Rename or Drop**: breaks any query that references the column.
* **Type change**: breaks casts, comparisons, or order behavior. (e.g., ordering a look-like-number string values shows a different result compared to ordering number values)
* **Semantic change**: the column still exists, the type is the same, but the meaning has changed. This is the hardest one to catch, and it usually silently causes failures. It might only be detected when the dashboard shows a weird trend.

How to prepare:

* **Schema registry** (Confluent, AWS Glue): for streaming sources, producers register their schema, and compatibility rules are enforced at publish time, and those rules will reject incompatible schema changes.

  [![](https://substackcdn.com/image/fetch/$s_!EH9R!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe29df0a3-e300-41c3-a927-9d050444c596_1970x598.png)](https://substackcdn.com/image/fetch/$s_!EH9R!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe29df0a3-e300-41c3-a927-9d050444c596_1970x598.png)
* **Selective reads**: `SELECT specific_columns` instead of `SELECT *`. This helps you prevent errors when the source adds or drops columns that you don’t actually need.
* **Validation at ingestion time**: check the incoming schema against what you expect. (you can do with dbt)
* **Official channel for changes**: if you consume the API or source from a third party, a very high chance that they will provide the change log. If the source is internal, we should meet with the source team to ensure we receive notifications about schema changes that affect the pipelines.

---

# How do I access the data?

This question helps us prepare the materials we need to pass all firewalls and reach the source safely and reliably**.**

### Network reachability

Before authentication, you need to know the “path” and whether the “path” is clear to go. Is the source on the public internet, or inside a private network? If private, you might need to sit down with the infrastructure team to determine a suitable approach to reach the private endpoint.

[![](https://substackcdn.com/image/fetch/$s_!Mp1v!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feefaf4ac-c24e-4bc2-a88d-06421b710ccf_1028x552.png)](https://substackcdn.com/image/fetch/$s_!Mp1v!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feefaf4ac-c24e-4bc2-a88d-06421b710ccf_1028x552.png)

You might find this familiar: you might test the connection locally on a corporate VPN, and everything works. Your production server doesn’t have the same network path. Thus, the pipeline will fail immediately.

### Authentication

[![](https://substackcdn.com/image/fetch/$s_!60Lh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F26043265-ae40-4a6a-b334-29426e92fd57_606x150.png)](https://substackcdn.com/image/fetch/$s_!60Lh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F26043265-ae40-4a6a-b334-29426e92fd57_606x150.png)

Then, you have to answer the question “Who am I? “ from the source. You must authenticate with:

* **Static credentials** simple username/password, API, or secret keys).
* **Service accounts**: scoped to a specific workload, easier to manage centrally
* **OAuth / token-based**: in case of tokens expiring, your pipeline needs refresh logic
* …

Questions worth asking: Where are the credentials stored? (Secrets manager, not a `.env` file in the repo.) How can I access the credentials? What happens when they expire mid-run?

### Authorization

[![](https://substackcdn.com/image/fetch/$s_!Qdp7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F70147892-c723-4fb5-9b9c-7fbef730bb03_684x138.png)](https://substackcdn.com/image/fetch/$s_!Qdp7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F70147892-c723-4fb5-9b9c-7fbef730bb03_684x138.png)

Access granted doesn’t mean full access. You might have table-level access but not column-level. Row-level policies might filter what you see based on your identity.

The principle is that you should have the fewest permissions possible to get what you need.

This is surely more annoying than the “A over-privileged credentials that can do all, “ and you might think this is the responsibility of the source team, not mine. However, in my experience, having a powerful credential could bring you comfort at first, but it will be very dangerous if the credentials leak.

---

# Can I read the source exactly once?

In an ideal case, for a given event in the real world, there should be a single data record reflecting it, not zero, not more than once. This is called the exact once guarantee. But, we’re not in the ideal case most of the time:

* **Duplicates**: the same record might arrive more than once. Common in streaming systems (at-least-once delivery is the default in Kafka). Also, data is ingested into the source twice for some reason, for example, a retry.

  [![](https://substackcdn.com/image/fetch/$s_!ke_5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3bada830-0a73-4aba-a303-0a916bd2ff10_772x362.png)](https://substackcdn.com/image/fetch/$s_!ke_5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3bada830-0a73-4aba-a303-0a916bd2ff10_772x362.png)
* **Missing data**: records that should have arrived never did. This is the quieter failure. A batch window that silently drops records. An API that paginates incorrectly and skips a page. If a Kafka consumer commits offsets before processing completes and then crashes, those records are marked as consumed but never actually processed.

  [![](https://substackcdn.com/image/fetch/$s_!Yjbv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdacd4241-178c-4ade-b461-25c93182822e_628x362.png)](https://substackcdn.com/image/fetch/$s_!Yjbv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdacd4241-178c-4ade-b461-25c93182822e_628x362.png)

Missing data is harder to catch than duplicates because we don’t actually know it’s missing until we cross-check with the source.

We can handle this by following:

* You might need deduplication on read here; the challenge is not the logic, it’s about the key you will use for deduplication. In some sources, this information might not be explicit; you will need to profile the data (or go around asking who knows it).
* Track record counts at ingestion and compare against source counts
* For APIs, validate that pagination returns the expected total
* For streams, prefer committing offsets only after successful processing
* …

---

# How does the source handle deletes?

When a record is updated, there’s a new row to detect.

When it’s updated, we can rely on the `updated_timestamp` and keep only the latest version.

But when it is deleted, it’s a different story.

If the source implements soft deletion, where removed records have a special flag indicating they were deleted, we can rely on that flag to “skip” those records downstream.

[![](https://substackcdn.com/image/fetch/$s_!BOs8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F72acd8cb-3234-4131-9f10-8dcafecc184d_1708x284.png)](https://substackcdn.com/image/fetch/$s_!BOs8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F72acd8cb-3234-4131-9f10-8dcafecc184d_1708x284.png)

With hard deletion, the row is just gone.

Your pipeline runs fine, accumulates records, and slowly drifts from source. Nobody notices until someone (is hard-working enough) manually reconciles with the source months later.

[![](https://substackcdn.com/image/fetch/$s_!aExv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F61bc229a-4d9e-4205-a89c-e5911e78457d_1074x274.png)](https://substackcdn.com/image/fetch/$s_!aExv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F61bc229a-4d9e-4205-a89c-e5911e78457d_1074x274.png)

Hard deletion could be handled in the following way (not comprehensive):

* **CDC** captures delete events as they happen; the most complete and reliable option.
* **Might apply a special mechanism to detect changes, such as SCD 2**: for example, if the record with that ID doesn’t appear in today's snapshot, consider it deleted.
* **Negotiate soft deletes with the source team**: if you can negotiate only. Hard deletes become a flag instead of a disappearance into the air.

---

# What is the data quality contract with the source?

Your pipelines can run technically correctly, all the tasks, and still produce the wrong output. If the source sends bad data, your pipeline delivers bad data downstream.

[![](https://substackcdn.com/image/fetch/$s_!3US4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c03731d-d868-4d6e-98fd-aed079783dcb_662x558.png)](https://substackcdn.com/image/fetch/$s_!3US4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c03731d-d868-4d6e-98fd-aed079783dcb_662x558.png)

We can ask those questions to clarify things a bit:

* Are there known bad records the source team is aware of but hasn’t fixed?
* Are fields that should be non-null actually nullable in practice?
* Are there late records that belong to last week's update but arrived today?
* …

What to do with the answers:

* Add validation at ingestion: check null rates, value distributions, record counts against expectations
* Build alerts for when incoming data looks different from the history runs.
* If you could, form a “contract” between you and the source.

---

# Is the source available when I need it?

All the questions above are asked and answered; you then write a task to pull the data, no rate-limiting hit, just a normal, healthy call with the right params, and you receive a “service unavailable“ error.

[![](https://substackcdn.com/image/fetch/$s_!Lt3f!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F781e477d-dd67-4f96-9482-cc2e7d4f097a_896x542.png)](https://substackcdn.com/image/fetch/$s_!Lt3f!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F781e477d-dd67-4f96-9482-cc2e7d4f097a_896x542.png)

Besides the quality of the data, the availability of the infrastructure that provides the data is also important. We need to ask:

* **What is the source’s uptime guarantee?** A documented SLA of 99.9% sounds reassuring. What matters more is whether they actually meet it, and what happens when they don’t.
* **How long can my pipeline wait?** If the source is down for 2 hours and your pipeline runs daily, you probably have time to wait and retry. If your pipeline runs every 30 minutes and feeds a real-time dashboard, a 2-hour outage is a serious incident.

A common way to handle it:

* Always Retries with exponential backoff.
* Alerting for runs that exhaust retries.
* For critical sources, a circuit breaker: stop retrying after N consecutive failures and wait for manual intervention.
* Work with the source team if you can to ensure the availability of the source based on your needs, and require clear announcements for the source unavailability.

---

# Outro

In this article, I shared my top concern when consuming data from a source to build a data pipeline. We have gone through 11 questions:

1. What is the type of the source?
2. How often do I need to touch the source?
3. How will the source performance be impacted?
4. How long does the source retain the data?
5. Does the source have the fields I need?
6. If the schema changes, how will I know?
7. How do I access the data?
8. Can I read the source exactly once?
9. How does the source handle deletes?
10. What is the data quality contract with the source?
11. Is the source available when I need it?

In each one, I share the motivation behind it and solutions/patterns to solve the related problems.

Thank you for reading this far. See you in my next article.
