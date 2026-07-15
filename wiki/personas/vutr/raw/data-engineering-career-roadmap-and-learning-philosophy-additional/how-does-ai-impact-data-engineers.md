---
title: "How does AI impact data engineers?"
channel: vutr
author: "Vu Trinh"
published: 2026-05-12
url: https://vutr.substack.com/p/how-does-ai-impact-data-engineers
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Snowflake", "Data Modeling", "Data Warehouse", "Orchestration", "Data Quality"]
tags: [https, auto, good, image, substackcdn, fetch]
---

# How does AI impact data engineers?

*Will we lost our jobs?*

> Source: [Open post](https://vutr.substack.com/p/how-does-ai-impact-data-engineers)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[snowflake|Snowflake]] · [[data-modeling|Data Modeling]] · [[data-warehouse|Data Warehouse]] · [[orchestration|Orchestration]] · [[data-quality|Data Quality]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=196281687)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!MQNL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F50baa8dc-477b-4a7f-a5c1-7c5ba11131a9_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!MQNL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F50baa8dc-477b-4a7f-a5c1-7c5ba11131a9_2000x1429.png)

---

# Intro

The main theme of Internet discussion about jobs right now: “AI will replace us, it will take our jobs…“

The second main theme of Internet discussion about jobs is: “AI is not smart enough to handle our jobs, we are safe (now). “

You will read about a big tech company that laid off X% of its employees because they can leverage 20$ subscriptions (or it’s just that the company is going downhill and using AI as a fancy reason)

Or you might read about a piece of sci-fi vibe movie like: “X% of our code is written by AI“.

—

The rise of LLMs and their wrapper applications like ChatGPT, Gemini, and Claude clearly improves life in some ways, but it also instills fear in people.

Let’s temporarily put the in-the-future fear, [where AI will have its own mind, create an army of T-800, and wipe us out](https://www.imdb.com/title/tt0088247/), aside.

The more obvious and evidence-based fear is that AI will take our jobs. Many time-travelers predict that jobs A, B, and C will disappear in X, Y, and Z years. Or some industries are seeing AI actually taking people's jobs.

—

At least 10 times this year, I have had folks reach out to me to express their concern that AI will disrupt data engineering: some were afraid that AI would replace them when they saw it could write PySpark jobs, and some were struggling to find a junior position.

My answer is always generic like this: “Focus on fundamentals and know the right way to do something, as AI will need our feedback to do well.“

Thinking back, that’s a fine answer, but it is not detailed enough to answer the question “How does AI impact data engineers?”

So I decided to sit down and write this article.

—

In this article, we will discuss my personal observations and experiences regarding how AI will impact us (data engineers). We will dive into two big sections: the first examines the angle at which AI can boost our productivity (or replace us), and the second explores how our mindset changes when the customer is now also the AI.

> ***Note**: This is purely my train of thought. Also, I’m somewhat out of date on recent AI innovations, and I’m more on the ‘not-so-hyped-about AI’ side. So, take it with a grain of salt.*

---

# tl;dr

* Using AI is not optional anymore.
* If you stop understanding problems, making decisions, evaluating trade-offs based on the current context and constraints, and communicating with others, you will be replaced by AI. → Learning aggressively to become a senior.

  + ***If somehow AI can do these in the future, we will be doomed; not just data engineers, but all humans.***
* The demand for leveraging AI in organizations (fine-tuning or making them an analytics serving layer) forces us, as data engineers, to update our mindset and skill set. From implementing the semantic layer and understanding the vector database to advanced techniques for making AI consistent and reliable.
* From that, I personally believe the data engineer role won’t be replaced soon. There will be two dominant statuses of those who pursue the data engineer career:

  + They won’t get a job: their experience and skill set can be replaced by AI.
  + They’re having a job with more tasks to do than ever. The CEO might think: “AI can help a person do many things now, so that we can save labor costs. “ The tasks of the remaining data engineers increase by the following factors:

    - The number of the company’s data engineers decreases
    - The high pressure from the company board because they believe AI can significantly boost an individual’s productivity → more tasks for an individual.
    - Sloppy AI’s work causes bugs or disasters. We now spend more time than ever reviewing. (e.g., commit with 50+ file changes and 1000+ code diffs)

AI boosts our productivity.

In each section below, we will discuss a main data engineering task. In some tasks, we discuss the two sub-processes: decision making and implementation, to see the clear AI impact on the entire process. The order of these sections does not reflect the actual order of those steps in the real-life data engineering process.

Keep in mind: the impact evaluation is my own.

# Ingest and move data.

One of the most obvious data engineering tasks. Your business user wants some insight; you “link” the insight to the source data, reach the source, and “move” the data.

[![](https://substackcdn.com/image/fetch/$s_!8T84!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19afab5f-df49-40cd-b70d-57123a6c5461_1060x496.png)](https://substackcdn.com/image/fetch/$s_!8T84!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19afab5f-df49-40cd-b70d-57123a6c5461_1060x496.png)

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=196281687)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

## Decision making

It’s not as easy as “hey, source, here are things I need, provide me“.

Tons of things need to be decided here: efficient way to work with different source types, setting the ingestion frequency, understanding source availability and retention, assessing the impact your reads have on the source, or handling the read correctness (e.g., de-duplicating or handling hard delete records)

### AI Impact

These decisions require understanding systems that AI has no visibility into, or that need a lot of effort from us to provide information for AI.

[![](https://substackcdn.com/image/fetch/$s_!eQvB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff43d2298-044b-4a4c-a293-94c8fc53e0c7_884x440.png)](https://substackcdn.com/image/fetch/$s_!eQvB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff43d2298-044b-4a4c-a293-94c8fc53e0c7_884x440.png)

How the source behaves under load or what the upstream team actually does versus what they document. The evaluation here is based on operational experience and human-to-human discussion. The cost of letting the AI guess is high; if it makes a bad ingestion decision, it propagates through downstream systems or degrades the source systems’ performance.

## Implementation

Once the decisions are made, you write Python scripts to consume the source (e.g., call the API, execute the query,…), define the orchestration logics, or handle failures.

If you used a wrapper tool such as Airbyte, you need to configure and manage the integrations.

And when moving data from a source to a destination, we need to manage credentials/configurations for both the source and the destination.

### AI Impact

AI can be really useful here as long as you can actually describe what you need. Writing code to execute a query or call an API, with complete implementation of retrying and pagination, is totally doable for AI.

[![](https://substackcdn.com/image/fetch/$s_!kU6m!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2558ceac-3bd9-4d04-9fdf-a66cd637ecad_1106x888.png)](https://substackcdn.com/image/fetch/$s_!kU6m!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2558ceac-3bd9-4d04-9fdf-a66cd637ecad_1106x888.png)

The risk of getting implementation wrong can be mitigated by having AI write tests (even one to simulate the real-world workload to see the impact on the source) to catch the issue and fix it. Some iterations are needed between human and AI, but it is not so complicated and time-consuming to get AI to do what you want here.

---

# Model and transform data

[![](https://substackcdn.com/image/fetch/$s_!eAWx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F07230894-506b-45e9-a03d-83892c979b9b_1814x340.png)](https://substackcdn.com/image/fetch/$s_!eAWx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F07230894-506b-45e9-a03d-83892c979b9b_1814x340.png)

Source data is rarely in an optimized state for extracting insights or consumption. We need to apply some logic to transform it and present it as predefined data models.

## Decision making

Before any transformation logic is written, there’s a “modeling conversation” to have. Conceptual/physical data modeling, Star schema or one big table? How normalized should this be?

[![](https://substackcdn.com/image/fetch/$s_!iJsJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa8edd987-4aab-4d65-abe1-db499b90c3e0_1112x494.png)](https://substackcdn.com/image/fetch/$s_!iJsJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa8edd987-4aab-4d65-abe1-db499b90c3e0_1112x494.png)

These decisions are the contract for data transformation and consumption. A poorly designed model or (no model at all ) causes miscommunication. You will see things get worked around, patched, untrusted, and complained about for years.

Once you have that alignment, you can answer this question: How should revenue be calculated? Should refunds be excluded, and from which date? How is an active/inactive customer defined?

This process requires conversations (and your sympathy) with business users across the company.

### AI Impact

I doubt AI can do this well.

If done correctly, data modeling requires organizational alignment, getting the business, analysts, and engineers to agree on what a concept is and how concepts relate to and impact one another.

[![](https://substackcdn.com/image/fetch/$s_!_5LR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3f2bb3fa-4c22-4664-a2d6-8fc3dc2b7485_894x490.png)](https://substackcdn.com/image/fetch/$s_!_5LR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3f2bb3fa-4c22-4664-a2d6-8fc3dc2b7485_894x490.png)

That requires negotiation, domain understanding, and requirement translation. Negotiation is something we have to do ourselves. AI can help with domain understanding and requirement translation, but it still relies heavily on our feedback and the company context.

Business rules have the same problem.

AI can suggest a transformation pattern given a clear spec. But the spec itself: gross/net, refunds, which date field contributes to the calculation,… comes from a human conversation (or exists in a guy’s head, and he left the company)

## Implementation

Once the model is agreed upon, the first job is to shape it. That means turning the design into physical tables, schemas, and relationships, and documenting it so others can work with it. Examples of needed items include ERD diagrams, data dictionaries, and schema definitions.

This is the artifact that bridges the modeling conversation and the engineering work.

Then comes implementing the logic aligned with the model. SQL, dbt models, or PySpark jobs, for example.

### AI Impact

AI can partially assist here, depending on the kind of task.

Scaffolding physical schemas, generating ERD drafts from existing definitions, or documenting data models are all AI-doable with minimum human intervention.

Given a clear model, unambiguous business rules, your organization's best practices, and detailed configurations (e.g., a data warehouse connection for dbt or a Spark master address), AI can also help with transformation code here.

[![](https://substackcdn.com/image/fetch/$s_!aB4l!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffd0ec5ab-0cb7-4f53-989b-6ac66c1ba525_1012x732.png)](https://substackcdn.com/image/fetch/$s_!aB4l!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffd0ec5ab-0cb7-4f53-989b-6ac66c1ba525_1012x732.png)

The risk lies in the validation step: an incorrect transformation can be caught during review or testing before it causes damage. AI might need a lot of curated information and context to cover all edge cases (e.g., AI might not know about the 3rd party occasionally sending duplicate transactions) and run tests on a meaningful dataset (e.g., the normal distribution and cardinality of the data)

My point here is that, although verification is AI-doable, it requires human input, supervision, and feedback to be reliable.

---

# Ensure data quality

[![](https://substackcdn.com/image/fetch/$s_!PQRY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F142f2f6b-afac-4c0d-8f26-362dd7ca1206_1566x602.png)](https://substackcdn.com/image/fetch/$s_!PQRY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F142f2f6b-afac-4c0d-8f26-362dd7ca1206_1566x602.png)

Data quality is one of those things everyone agrees on, but we rarely do it comprehensively because it’s very hard to know what the “good form” of data looks like at the very beginning.

## Decision making

How do we detect a schema change? What rules should we check? Which is the bad pattern of the data? How late is actual late? These all require business context and data profiling.

### AI Impact

[![](https://substackcdn.com/image/fetch/$s_!FUgW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F22e55b75-dfc3-4f1b-9711-b43321250fb0_868x598.png)](https://substackcdn.com/image/fetch/$s_!FUgW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F22e55b75-dfc3-4f1b-9711-b43321250fb0_868x598.png)

AI can partially help here. You can provide enough context or let it profile the data to suggest checks/validations. However, to do that, we need to update the context and ask the AI to profile continuously, as the business context and data characteristics will surely change. Another concern is that … we don’t have, or don't know, all the context to input. (e.g., we don’t even know what “good“ data looks like)

After AI provides the suggestions, we must be the ones who review and approve. The cost of getting it wrong is high: bad data that passes because the checks were defined incorrectly is worse than no checks at all.

## Implementation

Now that we know what to check, we can write the rules and detect patterns using dbt checks, explicit Python/SQL validation scripts, or anomaly-detection logic.

### AI Impact

AI can help a lot here.

They can generate a dbt test or a test script. Anomaly-detection logic based on third-party libraries (e.g., Bollinger bands implementation) can also be generated by AI here, as long as you can give them the abnormal pattern (e.g., lower than an X threshold)

The way the AI can do wrong lies mostly in the decision-making process.

---

# Serve data to consumers

[![](https://substackcdn.com/image/fetch/$s_!ngTs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcac06be4-e334-49e0-a997-f96319492478_810x486.png)](https://substackcdn.com/image/fetch/$s_!ngTs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcac06be4-e334-49e0-a997-f96319492478_810x486.png)

The task is usually the one that determines whether our effort is gonna pay off. Business users care about insights; they are less concerned with your Spark job.

## Decision making

There are a lot of things we need to decide here: What’s the acceptable level of staleness? What happens when incorrect data has already reached the dashboard, and someone has made a decision based on it? How many concurrent users access it?

Choosing a serving architecture, defining freshness SLAs, understanding usage patterns, preparing for concurrency expectations, and working on safe-write guarantees (e.g., atomicity, idempotency)

### AI Impact

[![](https://substackcdn.com/image/fetch/$s_!uGy3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd0361e66-66da-4a5f-960c-fadcf6c155d2_572x448.png)](https://substackcdn.com/image/fetch/$s_!uGy3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd0361e66-66da-4a5f-960c-fadcf6c155d2_572x448.png)

If the provided context is poor, AI can only guess here. These decisions require conversations with business users, listening to their problems, and translating them into technical decisions.

The cost of getting it wrong is immediately visible: users see stale numbers, the serving layer goes down under heavy load, and executives make decisions based on bad data.

Thus, I believe we can’t rely too much on AI for end-to-end decision-making here. Treating it as a colleague to discuss, break things down, and make the decision ourselves is more reliable and safer.

## Implementation

We need to choose a partitioning/clustering schema, expose views/tables/materialized views, prepare a dashboard, implement the API endpoints, convert data to the desired format, and plan for a high-concurrent scenario.

### AI Impact

By clarifying what you need here, I believe AI can handle all the tasks listed above pretty well (by interacting via tools, APIs, or MCP if needed to create, for example, a day-partition table)

A concern is that the technical requirements might change over time, such as a change in query patterns or increased concurrency. To keep AI aware of changes, we need constant input, such as query logs, access patterns, or database performance metrics.

Another part I think AI is doing better and better is that they treat them as a “data analyst”: we ask them an analytics question, and it answers back with the insight (text + chart)

[![](https://substackcdn.com/image/fetch/$s_!EPHl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd3889ad9-8cef-475f-a0f4-3ae7879d2dc0_686x404.png)](https://substackcdn.com/image/fetch/$s_!EPHl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd3889ad9-8cef-475f-a0f4-3ae7879d2dc0_686x404.png)

Context is important here; during the serving phase, it’s easier to provide comprehensive context to AI than in the previous tasks. With a semantic layer, a knowledge graph, a data modeling documentation, or a constraint on using a subset of a defined dataset, AI can impress you with its answer.

> *We will discuss this point more in the “**Our customers are not only human anymore**“ section.*

---

# Manage and operate data systems

[![](https://substackcdn.com/image/fetch/$s_!bFkJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe1926911-0a76-43fa-9235-e72f80fba320_1558x684.png)](https://substackcdn.com/image/fetch/$s_!bFkJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe1926911-0a76-43fa-9235-e72f80fba320_1558x684.png)

Making a pipeline or any data solution up and running is not enough.

We have to think like a software engineer here:

Deployment strategy, environment management, versioning strategy for datasets/pipelines/schemas, and incident response process.

How do you deploy changes to the pipeline or transformation logic? How to roll back to a version for debugging. How do you handle a schema migration that needs to be backward compatible with consumers you don't control? How to manage three environments (dev/staging/production) and keep them in sync.

### AI Impact

AI can help with the “structured/templated“ tasks here:

* Writing CI/CD pipelines
* Managing infrastructure as code
* Setting up deployment workflows across dev, staging, and production environments

As these tasks are likely to have available templates and practices, and don’t rely so much on the data/business context. For data-related tasks (e.g., coordinating schema migrations) or user-related processes (e.g., who will be notified when an incident occurs), AI can actually do them; however, it requires more detailed input and proactive feedback from us.

---

# Observe and monitor systems

[![](https://substackcdn.com/image/fetch/$s_!cL2T!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd0e4c611-c8eb-4e1a-9e70-a23269e76574_1336x654.png)](https://substackcdn.com/image/fetch/$s_!cL2T!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd0e4c611-c8eb-4e1a-9e70-a23269e76574_1336x654.png)

## Decision making

CPU usage, memory consumption, job duration, queue depth, failed task counts, which piece of log should I read, which alert threshold should I set? Deciding what to monitor and what “hints “at the failure is crucial, as there are tons of signals from different tools; you can’t keep an eye on all of them.

### AI Impact

AI can suggest best-practice infrastructure monitoring patterns (e.g., the ideal Spark worker memory consumption) and reasonable starting thresholds for job duration or resource utilization.

[![](https://substackcdn.com/image/fetch/$s_!VaSZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc94c9adc-aaac-4b63-aa44-8e8d71d86972_720x460.png)](https://substackcdn.com/image/fetch/$s_!VaSZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc94c9adc-aaac-4b63-aa44-8e8d71d86972_720x460.png)

But calibration/adjustment requires more context: knowing how your Spark job behaves on a normal Monday versus at the end of the month, when data volume spikes, or knowing that a particular pipeline always takes 40% longer on the first run after a deployment.

This behavioral knowledge needs to be input by us.

## Implementation

For implementation, you need to analyze logs to trace failures and unexpected behavior, configure alerts for job failures, SLA violations, or resource usage exceeding thresholds, and create/observe dashboards to monitor infrastructure health (e.g., Airflow, Snowflake, Spark, …).

### AI Impact

AI can help a lot here: writing log queries, setting up alerting rules, and gathering monitor metric charts.

It can read through thousands of log lines to find the root cause (depends on how informative the logs are). If we give AI enough historical run data, it can also flag when a job is taking unusually long or when resource consumption deviates from its expected pattern.

However, for the action after the findings, we still need to provide input, as AI can’t decide the next step. For example, increase a worker's memory if utilization exceeds a threshold.

---

# Secure and govern data

[![](https://substackcdn.com/image/fetch/$s_!_IZi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9915df58-de5b-48b4-be3c-3dad702e193c_1072x702.png)](https://substackcdn.com/image/fetch/$s_!_IZi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9915df58-de5b-48b4-be3c-3dad702e193c_1072x702.png)

## Decision making

In this task, you need to control access to the data and manage the data’s life cycle. Who should access which data, at what level of granularity? Are there any regulations applied to this dataset? How long should this data be retained? When does it get archived, and when does it get deleted?

### AI Impact

AI can’t help with this.

[![](https://substackcdn.com/image/fetch/$s_!FL6n!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa2014dc2-9575-4a5a-ac93-1d0117b1f8ff_1652x602.png)](https://substackcdn.com/image/fetch/$s_!FL6n!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa2014dc2-9575-4a5a-ac93-1d0117b1f8ff_1652x602.png)

The decisions must be agreed upon at the organization level. Getting them wrong will cause compliance violations, data leaks, resource waste, or data being deleted while users are still using it. And unlike a bad transformation that gets caught in testing, the governance gap usually happens when the (serious) incidents happen.

## Implementation

Things we need to do here: drafting access control policies, configuring role-based permissions, setting up audit logging, implementing data masking and encryption, implementing retention schedules, automating data archival and deletion pipelines.

### AI Impact

AI can generate policy templates, configure roles, set up audit logging, or draft retention rule definitions. Those tasks are “structured” enough that AI produces the drafts.

But the risk remains; every output needs us to review carefully to avoid some disasters, like:

* Governance edge cases are invisible until they become incidents.
* A permission that's too broad gets exploited.
* A masking rule that misses one column leaks PII.
* A retention job that deletes the table should not be deleted.
* …

---

# Optimize for cost and performance

[![](https://substackcdn.com/image/fetch/$s_!-C05!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa83ecee4-dc4a-48b7-8eef-37c633094a6a_1286x406.png)](https://substackcdn.com/image/fetch/$s_!-C05!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa83ecee4-dc4a-48b7-8eef-37c633094a6a_1286x406.png)

Your company budget is not unlimited. The concern is achieving the desired performance while maintaining reasonable billing.

## Decision making

We need to decide:

* How many resources do we need?
* How can I make these queries faster under the fixed resource?
* Which partition and clustering should we employ?
* Does this use case require pre-aggregate data?
* Are there any wasteful points we can optimize?
* …

### AI Impact

AI can identify bottlenecks, highlight expensive patterns, and suggest trade-offs. But the final action requires more context from us: for example, the company budget, the desired performance, or the final confirmation on whether a table is actually no longer needed. The cost of getting it wrong is cumulative: a bad optimization decision gradually adds up the cloud bill or degrades query performance.

## Implementation

Some “exciting“ jobs here are: tuning slow SQL queries, optimizing partitioning and clustering strategies, configuring compute resources, detecting unused services or datasets, or resolving bottlenecks in a transformation job.

### AI Impact

If you pass a query to AI (with additional information such as the tables’ schema or partition scheme), there's a very high chance the AI can output a more optimized version.

> ***Note**: If you tell them to write an optimized query from scratch, that’s a different story, as I didn’t have a good experience when telling AI to do that.*

Most cloud data warehouses can now suggest to you (via AI) a partitioning or clustering scheme based on your table’s usage patterns.

For resource usage, I believe a safer approach is to let AI write the rule, such as “If workers’ memory utilization exceeds 70%, add a worker.” I don’t think letting AI directly call the API to add or remove resources based on real-time metrics is a good idea here.

---

# Communicate and document

[![](https://substackcdn.com/image/fetch/$s_!Rocg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c261aa6-6e60-413e-940d-46af6a9fa3e3_958x440.png)](https://substackcdn.com/image/fetch/$s_!Rocg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c261aa6-6e60-413e-940d-46af6a9fa3e3_958x440.png)

To collaborate effectively with others, communication is crucial.

Negotiating requirements with stakeholders (yeah, if you accept everything they ask for, you will be miserable), expressing the idea, asking for feedback, or giving input on other works

These processes usually require human-human interaction.

### AI Impact

As discussed thoroughly in this article, AI can’t handle the communication for us. It can summarize a meeting or polish our email/Slack message, but the intention and the way we express it should be done only by a human.

[![](https://substackcdn.com/image/fetch/$s_!Shly!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c3ac2a9-a9f2-4898-ba3f-0f399b5bccf9_434x486.png)](https://substackcdn.com/image/fetch/$s_!Shly!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c3ac2a9-a9f2-4898-ba3f-0f399b5bccf9_434x486.png)

AI can do well on the documenting here, especially for technical documents. However, humans’ context and intention (e.g., this doc is for engineers only…) should be clear.

The new customer

# Our customers are not only human anymore

The demand for feeding data to AI models such as GPT, Gemini, Opus, or a self-hosted model is real. That fact requires data engineers to update their mindset and skill set compared to what they needed 10 years ago.

## Customize the AI model

[![](https://substackcdn.com/image/fetch/$s_!Vfjg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9d18a992-0dd8-4d22-be92-a220baa28bc0_1254x724.png)](https://substackcdn.com/image/fetch/$s_!Vfjg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9d18a992-0dd8-4d22-be92-a220baa28bc0_1254x724.png)

For some specific use cases, your organization needs to fine-tune an existing model or enable it to access external knowledge via RAG (Retrieval-Augmented Generation).

In this case, most of the concerns we have when serving data to humans apply. However, we must apply with a new mindset:

* Besides the data, the pipeline now centers on the model. Versioning model, testing model, and deploying it. (with the help of AI engineers, if you’re lucky)
* Data might be more unstructured than ever; it doesn’t stop at a nested field in a table, it could be a PDF, an image, or even a video.
* It’s no longer only point lookup and history scan; it’s now an approximate nearest neighbors index to help AI models find the relevant vectors faster. Besides the OLAP database, we might need to spend time on a vector database.

  [![](https://substackcdn.com/image/fetch/$s_!QNbT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5157f9c9-6341-4314-9a90-e56d57417dac_490x258.png)](https://substackcdn.com/image/fetch/$s_!QNbT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5157f9c9-6341-4314-9a90-e56d57417dac_490x258.png)
* The AI model will need to operate on continuous data with low latency (real-time processing) to improve the response latency.

## AI is the serving layer

Suppose you’re a data engineer in this era, a very high chance that your CEO is asking for the ability to “ask AI about last month's revenue. “ The incentive of “AIs can do anything, so they can also answer my analytics questions” is everywhere.

[![](https://substackcdn.com/image/fetch/$s_!qVql!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbee168a3-b2c4-48b7-ac73-2f4da0c07fcd_860x416.png)](https://substackcdn.com/image/fetch/$s_!qVql!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbee168a3-b2c4-48b7-ac73-2f4da0c07fcd_860x416.png)

In this case, things get more complicated. An AI model could indeed give you the answer, as long as (again) you make sure it has the context to understand and the tools to execute. And, this opens a whole new world.

Just imagine you’re building a chat interface that lets business users input questions. The AI model analyzes the input, gathers information, generates SQL, executes the SQL, and creates a report or chart. To ensure a reliable answer, we must:

* Ensure there is enough context: we can provide the guidelines via the system prompts, provide them with the MCPs to read the document somewhere, or equip them with a semantic layer, [which acts as the information repository as well as the guardrail](https://open.substack.com/pub/vutr/p/i-spent-8-hours-learning-the-semantic?utm_campaign=post-expanded-share&utm_medium=web), or give them a knowledge graph(?).

  [![](https://substackcdn.com/image/fetch/$s_!FXSX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1018a285-ee1a-4faa-8086-b65f3c2a16d2_1476x688.png)](https://substackcdn.com/image/fetch/$s_!FXSX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1018a285-ee1a-4faa-8086-b65f3c2a16d2_1476x688.png)
* Ensure there are enough tools: we provide them with the permissions to execute the queries, create the dashboard, or run some code.
* Coordinate agents: some complex queries/questions might require a set of agents working together, and the agent can encounter different kinds of challenges: complex tracing and debugging, memory overflow, lack of permission, or stay idle without any clear reasons.

  [![](https://substackcdn.com/image/fetch/$s_!zewm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F256a8fed-4f62-426a-9c2b-ec5dd9c12598_1208x786.png)](https://substackcdn.com/image/fetch/$s_!zewm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F256a8fed-4f62-426a-9c2b-ec5dd9c12598_1208x786.png)
* Consistency: Because LLM is simply a giant probabilistic text generator, ask it for the same daily report twice, and you might get two different stories, two different framings, and even two different sets of insights. For business decision-making, it's a serious problem. Solving it requires feedback loops, prompt tuning, and a degree of output governance, all of which require significant expertise and effort. And we, data engineers, usually have to cover these things.

---

# Outro

In this article, I listed the main data engineering tasks to assess how well AI can handle them, and then we discuss what a data engineer needs to prepare to work with server AI and to make the AI server more robust.

For the first point, we saw that most of the task’s decision-making process still needs to involve humans heavily, as data engineering is a complex field that requires working with many departments to understand data needs. For the implementation process, AI can help with most of them; however, I’m not confident enough to hand it off completely to AI without any supervision.

From that, I believe the data engineer role won’t be replaced soon. As long as you can understand the requirement, communicate with others, and make decisions. Also, if you develop new skill sets and mindsets that enable you to serve AI and make AI serve, you will still be a valuable data engineer.

Thank you for reading this far. See you in my next article.
