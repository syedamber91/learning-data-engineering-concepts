---
title: "A strategy for doing a side project that would actually get you a job."
channel: vutr
author: "Vu Trinh"
published: 2026-01-06
url: https://vutr.substack.com/p/the-best-way-to-do-a-data-engineering
paid: true
topics: ["Data Engineering", "Apache Airflow", "Apache Kafka", "Apache Spark", "Apache Iceberg", "Apache Flink", "Snowflake", "Databricks", "Delta Lake", "BigQuery", "Data Modeling", "Data Warehouse", "Lakehouse", "Streaming", "Data Quality", "ETL"]
tags: [https, auto, good, substackcdn, image, fetch]
---

# A strategy for doing a side project that would actually get you a job.

*Having fun, learning skills and getting (a better) job*

> Source: [Open post](https://vutr.substack.com/p/the-best-way-to-do-a-data-engineering)

## Topics

[[data-engineering|Data Engineering]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[apache-flink|Apache Flink]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[data-modeling|Data Modeling]] · [[data-warehouse|Data Warehouse]] · [[lakehouse|Lakehouse]] · [[streaming|Streaming]] · [[data-quality|Data Quality]] · [[etl|ETL]]

---

> *I invite you to join my paid membership list to read this writing and 150+ high-quality data engineering articles:*
>
> [Upgrade subscription](https://vutr.substack.com/subscribe)
>
> * *If that price isn’t affordable for you, check this [DISCOUNT](https://vutr.substack.com/subscribe?coupon=c08a9839)*
> * *If you’re a student with an education email, use this [DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)*
> * *You can also claim this post for free (one post only).*
> * *Or take the [7-day trial](https://vutr.substack.com/7d8f19f0) to get a feel for what you’ll be reading.*

[![](https://substackcdn.com/image/fetch/$s_!eE6P!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F72467b81-ec30-46e6-816a-ef2ce7b7d379_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!eE6P!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F72467b81-ec30-46e6-816a-ef2ce7b7d379_2000x1429.png)

---

# Intro

Not long ago, a college student asked me on LinkedIn to give some feedback on his side project.

He first stores data in MySQL, uses Spark to read, transform, and load it into MinIO and Delta Lake, then uses Trino as the analytical engine and Superset for visualization.

I took a look and asked him two questions:

* What (fake) business questions does he want to answer with data from this setup?
* Why did he choose those tech stacks?

He couldn’t answer. He said he just searched on the internet for the popular data engineering tools and glued them together.

—

I used to be like him.

Just stick all the famous tools and call it a side project. The definitions of done are:

* All stacks are up.
* Some data is transformed
* Some chard is displayed.

I put it into my resume. The interviewer saw it. He asked me some similar questions to the ones I asked the college student.

Of course, I couldn’t answer.

—

Doing a side project is fun.

But joy is not enough. It must be done with strategies so you can actually:

* Learn things
* Show what you’ve learned

This is especially important when you want to decorate your resume.

In this article, I will share my strategy to do a side project that can actually get you a (better) job.

---

# 3s TL;DR

Just imagine you’re doing a real-life data engineering project.

---

# Do a project to solve your own problem.

First things first, start with a problem you want to solve with the data.

If it could, solve your own problem or at least ones you’re actually interested in. Because when doing that, you have the natural motivation and curiosity.

[![](https://substackcdn.com/image/fetch/$s_!-wff!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F17b2b0f0-e96a-408f-aae1-62b9d0716394_540x374.png)](https://substackcdn.com/image/fetch/$s_!-wff!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F17b2b0f0-e96a-408f-aae1-62b9d0716394_540x374.png)

Problem-driven or business-driven is always the right approach for any data project in real life. Companies hire data engineers to help them solve real business problems with data; we store, transform, and organize it so that, at the end of the day, it can provide insights that drive business decisions.

[![](https://substackcdn.com/image/fetch/$s_!Pqju!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2fa08979-f86a-4acf-8adc-b70e6385b818_914x866.png)](https://substackcdn.com/image/fetch/$s_!Pqju!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2fa08979-f86a-4acf-8adc-b70e6385b818_914x866.png)

This requires us not only to have technical skills but also to understand the business domain.

Solving the problem that actually matters to you will naturally lead you to dive into understanding it, though it might require time and effort (you can leverage AI tools to assist you in this process).

[![](https://substackcdn.com/image/fetch/$s_!lMIO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9e423a24-d673-4861-9802-9feb2cf7347c_1008x708.png)](https://substackcdn.com/image/fetch/$s_!lMIO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9e423a24-d673-4861-9802-9feb2cf7347c_1008x708.png)

At least, you enjoy and have fun when doing that, because you know you solve a problem you care about (e.g., based on the statistics, is my favorite football player doing well?)

(You can try to solve somebody’s problem or answer random questions, for example, how many Uber rides per day in Singapore. However, you will get bored soon.)

Understanding what you’re trying to solve will define the rest of what you’re going to do for the project:

* Which question do you need to be answered via data?
* How do you model the data?
* What is the related source data? Or is the required data available?
* How fast do you want the data to be available?
* …

In addition, understanding what your side project is trying to solve will make it easier to introduce what you’ve done and learned to the interviewer. They will always have a good impression of a candidate who really cares about solving problems rather than just listing tools in the project.

[![](https://substackcdn.com/image/fetch/$s_!5Plf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F592d4b60-09db-40d5-9cdd-dedcdbc41e9a_1190x400.png)](https://substackcdn.com/image/fetch/$s_!5Plf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F592d4b60-09db-40d5-9cdd-dedcdbc41e9a_1190x400.png)

Starting a side project at this stage will put you ahead of most candidates.

> *I invite you to join my paid membership list to read this writing and 150+ high-quality data engineering articles:*
>
> [Upgrade subscription](https://vutr.substack.com/subscribe)
>
> * *If that price isn’t affordable for you, check this [DISCOUNT](https://vutr.substack.com/subscribe?coupon=c08a9839)*
> * *If you’re a student with an education email, use this [DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)*
> * *You can also claim this post for free (one post only).*
> * *Or take the [7-day trial](https://vutr.substack.com/7d8f19f0) to get a feel for what you’ll be reading.*

---

# Data modeling

Not fewer than five times in this newsletter, I’ve stressed the importance of data modeling to an organization’s data foundation.

It facilitates communication between the data and business teams and guides how we transform, organize, and serve data.

—

The rise of more powerful OLAP systems, including Snowflake, BigQuery, Databricks, and ClickHouse.

These innovations often lead people to believe that data no longer needs to be modeled: throw in large amounts of data from different sources, and the system will handle it in the end (by paying more for processing power).

[![](https://substackcdn.com/image/fetch/$s_!mqTe!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F44da8979-fad4-4a70-84e6-69dac501ae0c_1160x646.png)](https://substackcdn.com/image/fetch/$s_!mqTe!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F44da8979-fad4-4a70-84e6-69dac501ae0c_1160x646.png)

As a result, data modeling is sometimes seen as a thing that belonged only to an era when companies used OLTP databases for analytics and hardware resources were expensive.

But that’s wrong.

People only care about the performance and resource utilization stories and forget the ultimate goals of data modeling:

[![](https://substackcdn.com/image/fetch/$s_!qHv1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6953f70e-9146-49ce-a206-a83fcc2aeda6_1060x718.png)](https://substackcdn.com/image/fetch/$s_!qHv1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6953f70e-9146-49ce-a206-a83fcc2aeda6_1060x718.png)

* Facilitating communication
* Guiding how we transform, organize, and serve data

—

Back to the side project, please model the data.

[![](https://substackcdn.com/image/fetch/$s_!uvnB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F947a32a7-2868-4f0c-8298-336d5e8fdff2_1504x682.png)](https://substackcdn.com/image/fetch/$s_!uvnB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F947a32a7-2868-4f0c-8298-336d5e8fdff2_1504x682.png)

From the section above, you can identify questions you want to answer.

From those questions, define related entities and their relationships (conceptual modeling), add attributes, primary keys, and data types to each entity (logical modeling), and finally translate them to tables, columns, constraints, or optimization techniques, such as clustering or partitioning (physical modeling)

[![](https://substackcdn.com/image/fetch/$s_!o8RY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe050d1f9-a0be-43be-b16e-4b39fd1c1227_1270x444.png)](https://substackcdn.com/image/fetch/$s_!o8RY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe050d1f9-a0be-43be-b16e-4b39fd1c1227_1270x444.png)

Kimball dimensional modeling is always my recommendation for those who want to learn data modeling, thanks to its popularity. In addition, the approach is pretty straightforward to get started.

However, designing a good data model is never an easy task. You can validate the robustness of your model in the following ways:

* From your questions, can you easily answer them with the help of the data model you designed?

  [![](https://substackcdn.com/image/fetch/$s_!ccqF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa370cb0f-9d7d-41c1-a682-e00ea20e01ca_976x376.png)](https://substackcdn.com/image/fetch/$s_!ccqF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa370cb0f-9d7d-41c1-a682-e00ea20e01ca_976x376.png)
* When you need to expand the data model to answer more questions, do you have any trouble doing that?

  [![](https://substackcdn.com/image/fetch/$s_!tLDV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb91a3c24-481e-47ee-b410-d6a1ad9ef16a_1412x390.png)](https://substackcdn.com/image/fetch/$s_!tLDV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb91a3c24-481e-47ee-b410-d6a1ad9ef16a_1412x390.png)

You can leverage AI tools for this validation step.

They can act as the senior data engineers or business users to give you some feedback on the modeling, as long as you provide these tools with enough context.

---

# Choose the tools

When doing a side project, I believe most of us will jump right into this step first. The dopamine hit of successfully running a Spark job on the cluster we just deployed, or of seeing numbers start to dance on a dashboard in Superset, is hard to resist.

Sadly, those joys were not enough.

In an interview or a real-life task, when speaking about tools, they must be aligned with the design and requirements, not about the quantity of tools you successfully get up and running.

—

That said, from the previous sections about problems and data modeling, you can now translate business requirements to technical requirements. You will now know:

[![](https://substackcdn.com/image/fetch/$s_!JlbI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd08abb33-c54c-4fad-87d4-237d12a9aee3_956x880.png)](https://substackcdn.com/image/fetch/$s_!JlbI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd08abb33-c54c-4fad-87d4-237d12a9aee3_956x880.png)

* The shape of the output tables
* How will the output be served (e.g., dashboards, CSV files,…)
* The latency of the output (e.g., daily or 2 seconds)
* What type of source is this? (e.g., api, database, Kafka...)
* ..

From there, you design your side project based on these requirements.

But let's start with a tool-agnostic architecture with only high-level components: ingestion component, the orchestrator, the ETL engine, the data warehouse, the BI tool…

[![](https://substackcdn.com/image/fetch/$s_!L9Kg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3c507538-9f48-413c-accc-824cc9ad7f60_1488x524.png)](https://substackcdn.com/image/fetch/$s_!L9Kg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3c507538-9f48-413c-accc-824cc9ad7f60_1488x524.png)

This is quite hard to do at first because you have to resist the temptation to choose tools here. In return, with the high-level design, you can think and communicate (to your future boss and interviewer) clearly about your ideas to solve the problem.

—

[![](https://substackcdn.com/image/fetch/$s_!bVGW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4aeee940-d896-4348-b6f3-3506279682b2_1448x540.png)](https://substackcdn.com/image/fetch/$s_!bVGW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4aeee940-d896-4348-b6f3-3506279682b2_1448x540.png)

Then comes the tools. Choose tools based on requirements and your designs.

If the output needs to be pulled from the API, use vanilla Python or [dlt](https://dlthub.com/) for that.

If you need an orchestrator, you can use Airflow, Dagster, or Prefect.

If you need a lakehouse, use Iceberg, Delta Lake, or Hudi on top of an object store such as S3 or GCS.

If you need an ETL engine, you can choose Spark, Spark Structured Streaming, Flink, or Polars

If you need BI tools, you can choose Superset.

If you need an analytical engine, you can choose Spark SQL, Trino, or DuckDB

If you need a data warehouse, you can go with BigQuery, Snowflake, Databricks or DuckDB.

…

—

The key things of choosing tools in a side project are to make sure:

* You understand the reason behind your choice of a single tool; again, you have to make sure it aligns with the requirements and design.

  [![](https://substackcdn.com/image/fetch/$s_!Z1HC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c3c8d32-4056-4318-b177-638838f77973_1386x484.png)](https://substackcdn.com/image/fetch/$s_!Z1HC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c3c8d32-4056-4318-b177-638838f77973_1386x484.png)
* Secondly, you must understand the purpose of a tool and its trade-off. Everything in the world has trade-offs. You must understand them and make choices. When you choose to go with a tool/solution, you must ensure that it can actually solve your problem, and you must also anticipate its disadvantages. That’s how system design looks in the real world, and you should also apply it when you’re just doing a side project.

  [![](https://substackcdn.com/image/fetch/$s_!64d4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19e5215e-e0a7-481d-9a2b-f2f6968ac8de_1296x414.png)](https://substackcdn.com/image/fetch/$s_!64d4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19e5215e-e0a7-481d-9a2b-f2f6968ac8de_1296x414.png)

Again, AI can also help you with this step; you can discuss with the AI tools for a second opinion on your choices. Make sure you don’t let AI choose the tools for you at the first steps.

---

# Break things

When discussing a side project, people usually share success stories.

[![](https://substackcdn.com/image/fetch/$s_!ndtv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c6f9bde-6577-4997-b2ca-154bc4f63b0b_1260x580.png)](https://substackcdn.com/image/fetch/$s_!ndtv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c6f9bde-6577-4997-b2ca-154bc4f63b0b_1260x580.png)

Tools are up and running, data is ingested, logics are applied, and numbers are displayed.

That’s cool.

But from my experience, you can learn even more from failures.

This might be weird advice, but trust me, try to break things.

[![](https://substackcdn.com/image/fetch/$s_!bP7Y!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffae04e68-6794-41cb-8e61-982977a167ab_1292x502.png)](https://substackcdn.com/image/fetch/$s_!bP7Y!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffae04e68-6794-41cb-8e61-982977a167ab_1292x502.png)

Inject a bad record in your pipeline, scale up the data volume, or kill a worker.

Then there is a new set of problems that occur, and when you solve them, you will learn tons of other things, things that actually matter in real-life projects:

* When the failures happen, will you know about it? → You learn about observability: logging, monitoring, alerting
* What happens when the pipeline fails? → You learn about fault-tolerance: can be the pipeline self-heal, is there any corrupt data in my sink when retry happens (idempotency). You also learn about data backfilling here.
* When the volume data increases, how do you deal with it? → You learn about resource planning: does the solution support horizontal scaling, and how many resources should I add to ensure the data latency requirement
* When bad records appear, what will you do? → You learn about data quality.
* …

Just break things, in any creative way you can imagine.

(don’t forget to solve them)

---

# Software engineering practices

The main theme of the article so far is to suggest mimicking a real-life project when doing a side project.

[![](https://substackcdn.com/image/fetch/$s_!kGje!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7b978b04-0530-4383-bc5e-a022b9242d96_834x584.png)](https://substackcdn.com/image/fetch/$s_!kGje!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7b978b04-0530-4383-bc5e-a022b9242d96_834x584.png)

And in real-world projects, we apply software engineering practices.

Use Git to version-control your project. Build a CI/CD pipeline to automatically apply changes. Write tests. Write clean code. Handle sensitive information (e.g., token, secret, credentials) properly.

You can ask AI to assist you with these tasks. Just make sure you don’t store your project in Google Drive.

---

# Tell the world

Make sure others understand what you’ve done. You might think you’re doing a side project and that only you understand is enough.

Yeah, that might be true.

Until you need to show the interviewer what you’ve done and learned, invite friends to join the project or ask for feedback from someone online.

Understanding is the very first step of collaboration, recognition, and giving feedback.

Try to document everything you’ve done. Your design, your tech stack decisions, your data model, the README, your debug process, …

[![](https://substackcdn.com/image/fetch/$s_!gSud!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe924e30-8569-4286-a2ed-75238017a810_1164x504.png)](https://substackcdn.com/image/fetch/$s_!gSud!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe924e30-8569-4286-a2ed-75238017a810_1164x504.png)

—

Then, share what you’ve done with the world. 10% is for bragging about your project; 90% is for getting feedback.

[![](https://substackcdn.com/image/fetch/$s_!aTYe!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd6f161ae-cbd4-48d3-bedc-60e7010713d8_950x610.png)](https://substackcdn.com/image/fetch/$s_!aTYe!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd6f161ae-cbd4-48d3-bedc-60e7010713d8_950x610.png)

Reddit, LinkedIn, and Twitter are good ways to do this.

—

And, the best way to tell the world is not the GitHub repo. Try to make your work more tangible and visible.

You can expose your dashboard to the public domain and build an interactive app (e.g., via Streamlit) to showcase what you’ve done.

(The video below is a demo of my SQL editor in Streamlit, it’s cool, huh?)

(Be careful about the security here; you only want your work to be exposed, not the sensitive data or the credentials.)

Imagine someone asks you about the side project you’ve just done; opening the browser and showing them what you’ve done is far more impressive than a boring GitHub repo.

---

# Outro

In this article, I share my strategy for a side project, especially the one I would include in my resume to increase my chances of getting a job. From starting with the problem, invest in data modeling, designing, and making decisions about tools, breaking things, and applying software engineering best practices to tell the world.

Thank you for reading this far. See you in my next article.
