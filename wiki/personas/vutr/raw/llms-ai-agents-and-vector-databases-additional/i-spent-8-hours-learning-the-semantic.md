---
title: "I spent 8 hours learning the semantic layer"
channel: vutr
author: "Vu Trinh"
published: 2025-12-23
url: https://vutr.substack.com/p/i-spent-8-hours-learning-the-semantic
paid: true
topics: ["Data Engineering", "Snowflake", "Databricks", "BigQuery", "Data Modeling", "Data Warehouse"]
tags: [https, auto, layer, semantic, substackcdn, image]
---

# I spent 8 hours learning the semantic layer

*Can it resolve messy data problems for your organization?*

> Source: [Open post](https://vutr.substack.com/p/i-spent-8-hours-learning-the-semantic)

## Topics

[[data-engineering|Data Engineering]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[bigquery|BigQuery]] · [[data-modeling|Data Modeling]] · [[data-warehouse|Data Warehouse]]

---

> *I will publish a paid article every Tuesday. I wrote these with one goal in mind: to offer my readers, whether they are feeling overwhelmed when beginning the journey or seeking a deeper understanding of the field, 15 minutes of practical lessons and insights on nearly everything related to data engineering.*
>
> [Upgrade subscription](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!c2PW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9c216245-e00a-4136-a09c-efaa7b312bcf_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!c2PW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9c216245-e00a-4136-a09c-efaa7b312bcf_2000x1429.png)

---

## Intro

If you’re a data engineer, you’ve likely been in a situation where business users aggressively ask for insights from data. They don’t know that you’re designing the data architecture or coding the pipeline.

The only thing they care about is the report, the dashboard, or the analysis that answers their business questions, or, even more, the ability to answer those questions themselves using data.

It might be unfair to us, but it’s… reasonable for them.

They need information to drive the business. Rising competition and market shifts don’t allow them to relax, especially at a time when everything seems more productive with AI.

In the 2020s, a rising term, a concept, promises to deliver self-serve analytics capabilities for organizations.

It’s called the semantic layer.

In this week’s article, I take a deep dive into this layer: what it is, whether it’s a new concept, whether it delivers the value it promises, and how it can help organizations better leverage and adopt AI models.

---

## What you can expect

This article won’t dive into any particular semantic layer solution on the market. Instead, it shares my perspective and experience with the semantic layer. I will spend a fair amount of time discussing how it can help, its relationship to a company’s data modeling practices, and how it can enable AI models to understand and extract an organization’s analytical data.

Because what you’re about to read comes from my own perspective, there are certainly areas that could be improved. Please feel free to let me know.

---

## Semantic Layer

There are many definitions of the semantic layer online, and I don’t believe there’s a standard one. (Each vendor has their own version.)

Here, I try to explain it from my own perspective.

The semantic layer acts as the translator between the data and its users. It abstracts the complexity of the insight extraction process, ensuring only understandable, business-friendly concepts are exposed to users.

[![](https://substackcdn.com/image/fetch/$s_!Kt8y!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b843f66-573a-4a15-a698-a5d7397e19e7_1238x444.png)](https://substackcdn.com/image/fetch/$s_!Kt8y!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b843f66-573a-4a15-a698-a5d7397e19e7_1238x444.png)

Every data-driven company wants the ability to capture, store, process, serve, and use data efficiently. The demand brings challenges, especially in a time when data can come from anywhere, no longer limited to in-house OLTP systems as in the past.

The amount of data grows in both volume and variety; more decisions need to be made, more data needs to be stored, and more source data needs to be captured. The complexity of the data warehouse definitely increases.

[![](https://substackcdn.com/image/fetch/$s_!zoP2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F335e33aa-f436-473a-b969-6cbac97263db_1556x728.png)](https://substackcdn.com/image/fetch/$s_!zoP2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F335e33aa-f436-473a-b969-6cbac97263db_1556x728.png)

Business users, or even data users, will surely struggle to understand the warehouse, slowing down the process of deriving insights from the data. Just imagine a CEO trying to figure out how to calculate revenue by looking at the ERD diagram to check how to join two tables together.

Organizations need a better abstraction layer that can lower the barrier for people to enter the complex data world.

That’s where the semantic layer comes.

> *I invite you to join my paid membership list to read this writing and 150+ high-quality data engineering articles:*
>
> [Upgrade subscription](https://vutr.substack.com/subscribe)
>
> * *If that price isn’t affordable for you, check this [DISCOUNT](https://vutr.substack.com/subscribe?coupon=c08a9839)*
> * *If you’re a student with an education email, use this [DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)*
> * *You can also claim this post for free (one post only).*
> * *Or take the [7-day trial](https://vutr.substack.com/7d8f19f0) to get a feel for what you’ll be reading.*

With a semantic layer, users specify only “where they want to go,” and the layer automatically determines the correct “roads” to take—seamlessly translating their intent into queries that deliver “User Active Count,” “Date,” and “Country.”

To do that, there are two typical processes in the semantic layer:

[![](https://substackcdn.com/image/fetch/$s_!4tCr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b410b39-6800-4856-8b6d-34ea70cd86b1_762x490.png)](https://substackcdn.com/image/fetch/$s_!4tCr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b410b39-6800-4856-8b6d-34ea70cd86b1_762x490.png)

* **Declaration**: Admins onboard data assets along with their relationships, define calculations, and might perform lightweight transformations for metrics and dimensions. Each tool will have its own “model”, the specific syntax that helps you define. Here is an example from CubeJS:

  [![](https://substackcdn.com/image/fetch/$s_!-MuE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe37de713-c5fd-41ab-bf05-9badd980c927_772x838.png)](https://substackcdn.com/image/fetch/$s_!-MuE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe37de713-c5fd-41ab-bf05-9badd980c927_772x838.png)

  [CubeJS official documentation](https://cube.dev/docs/product/data-modeling/overview).
* **Consumption**: Users navigate and select the desired metrics and dimensions exposed by the semantic layer (with more user-friendly names). The input is then converted into an SQL query that leverages the physical locations of data assets, their relationships, and other logic defined during the declaration stage. The SQL queries will be run on the configured database.

In other words, the semantic layer automates most of the insight extraction process:

* Finding the data entities
* Applying the SQL logic on these entities.
* Generating the SQL query and submitting it to the configured database.

---

## Types of the semantic layer

In the past, BI semantic layers might have been enough when reporting and dashboarding were the main ways users consumed data in an organization. Over time, more users wanted to use data in ways that were valuable to them, including AI models, A/B tests, and other data applications.

[![](https://substackcdn.com/image/fetch/$s_!ZtY5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee472fb4-727a-4bb9-b5b0-4460557707ef_1208x514.png)](https://substackcdn.com/image/fetch/$s_!ZtY5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee472fb4-727a-4bb9-b5b0-4460557707ef_1208x514.png)

Many users outside BI tools want the same benefits of the semantic layer.

A semantic layer that only serves BI might not be enough. Modern semantic layers like Cube.js were introduced because they recognized the need for a solution that not only meets BI demands and consistent data consumption across, but also enables many other data applications, a universal semantic layer.

---

## Other functions

Besides the semantic providing function, the semantic layer can have more functions now, given the fact that it will act like the centralized endpoint for the data consumption process:

[![](https://substackcdn.com/image/fetch/$s_!D_PV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f83c182-e956-4a29-ac35-d4267614effb_1232x452.png)](https://substackcdn.com/image/fetch/$s_!D_PV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f83c182-e956-4a29-ac35-d4267614effb_1232x452.png)

* The gatekeeper: because all the data access must go through the semantic layer, users can enforce that a piece of data can only be accessed by authorized clients.
* Performance optimizer: the user can establish caching or pre-aggregation strategies to optimize the data access performance.

---

## So, we don’t need data modeling anymore?

People began bringing back the idea of a semantic layer in the 2020s, in hopes of addressing the reality of messy data in organizations.

(It was not a new concept.)

Coincidentally, this period also saw the rise of more powerful OLAP systems, including Snowflake, BigQuery, Databricks, and ClickHouse. These innovations often lead people to believe that data no longer needs to be modeled: throw in large amounts of data from different sources, and the system will handle it in the end (by paying more for processing power).

[![](https://substackcdn.com/image/fetch/$s_!I-QZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F60487ce3-40db-4faa-8d90-100894748432_928x628.png)](https://substackcdn.com/image/fetch/$s_!I-QZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F60487ce3-40db-4faa-8d90-100894748432_928x628.png)

As a result, data modeling is sometimes seen as a thing that belonged only to an era when companies used OLTP databases for analytics and software was expensive. In reality, a company’s data warehouse is more likely to become a mess without proper data modeling.

I believe this factor contributes to the comeback of the semantic layer in the 2020s.

They hope the semantic layer could be the savior of their unmaintainable, unscalable, and untrustworthy data warehouse.

But is that true?

[![](https://substackcdn.com/image/fetch/$s_!-d5J!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3a96b36a-e6f6-452a-a8f7-308cf98d30c7_1054x488.png)](https://substackcdn.com/image/fetch/$s_!-d5J!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3a96b36a-e6f6-452a-a8f7-308cf98d30c7_1054x488.png)

To answer that question, let us first understand the role of data modeling and the semantic layer in an organization’s data architecture.

### Data modeling

> A data model is a structured representation that organizes and standardizes data to enable and guide human and machine behavior, inform decision-making, and facilitate actions. — [Joe Reis](https://joereis.substack.com/p/my-definition-of-data-modeling-for)

The data model defines many things:

[![](https://substackcdn.com/image/fetch/$s_!qHv1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6953f70e-9146-49ce-a206-a83fcc2aeda6_1060x718.png)](https://substackcdn.com/image/fetch/$s_!qHv1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6953f70e-9146-49ce-a206-a83fcc2aeda6_1060x718.png)

* Which entities are there? Customer? Device? Subscription Package?
* What is the relationship between them?
* Which data will be collected? Source A? Source B? Extract all the fields or just five fields?
* How to calculate a metric?
* Which constraints and business rules does this table have? Thus, it defines what quality data looks like.
* …

In brief, data modeling facilitates communication between the data and business teams and guides how the organization transforms, organizes, and serves data.

### Semantic Layer

On the other hand, the semantic layer doesn’t guide you through the whole data lifecycle.

It only provides a “translator” between the data system and the data client, which is responsible for giving the data meaning.

[![](https://substackcdn.com/image/fetch/$s_!RCHv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb4ffbb94-dc96-43e7-a120-c49a50ec2c70_714x836.png)](https://substackcdn.com/image/fetch/$s_!RCHv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb4ffbb94-dc96-43e7-a120-c49a50ec2c70_714x836.png)

In the absence of a semantic layer, business logic is fragmented across the consumption layer. A definition for “Gross Margin” might exist in a Tableau calculated field, a Power BI DAX formula, a Python script in a Jupyter notebook, and a stored procedure in Snowflake.

The semantic layer steps in to define what “Gross Margin” means, abstracting away the underlying complexity of finding tables, joining them, and applying formulas. It provides a friendlier abstraction and acts as a single point of access for metrics.

### The relationship between data modeling and the semantic layer

For me, data modeling is the core of any analytical data foundation, while the semantic layer sits on top, providing context and meaning.

Data modeling handles physical complexity, while the semantic layer provides logical simplicity. Remember, there are two stages in a semantic layer: **declaration** and **consumption**.

[![](https://substackcdn.com/image/fetch/$s_!Wgz2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fac941736-1f7e-4e66-8e22-a9a9406a6c23_1070x580.png)](https://substackcdn.com/image/fetch/$s_!Wgz2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fac941736-1f7e-4e66-8e22-a9a9406a6c23_1070x580.png)

The performance and usability of the consumption stage depend on the declaration stage, as it uses the information defined there to resolve physical table locations, define join logic, push down filters, and enforce security.

[![](https://substackcdn.com/image/fetch/$s_!ZyxS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F388bead8-db6e-43d9-a79a-f17b44361e4d_788x616.png)](https://substackcdn.com/image/fetch/$s_!ZyxS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F388bead8-db6e-43d9-a79a-f17b44361e4d_788x616.png)

The declaration stage, in turn, depends on how your company stores and organizes data.

And guess what controls how data is stored and organized?

**Data modeling.**

With a clean data model, you can easily determine:

* How to calculate a metric
* How to find a piece of contextual information
* How to join table A, table B, and table C

You already know how to do these things without a semantic layer.

The layer’s role becomes clearer: to abstract data assets and the methods used to extract them, processes that are already guided by the underlying data modeling.

If your data modeling can’t guide these processes, or if you don’t have data modeling at all, your semantic layer will also be a mess.

It might work fine at the beginning when you have only one or two tables. But as the business scales to hundreds of tables, problems start to appear: Which way of calculating a metric is correct (inconsistency)? Which table should be used to retrieve a piece of information (redundancy)? How should two tables be joined (ambiguity)?

When you then place a semantic layer on top of this, you are forced to handle the following in the declaration stage:

[![](https://substackcdn.com/image/fetch/$s_!PvUL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9feee396-1572-4ecc-81ef-288889a58125_760x404.png)](https://substackcdn.com/image/fetch/$s_!PvUL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9feee396-1572-4ecc-81ef-288889a58125_760x404.png)

* **Enforcing consistency:** You must choose a single approach to calculate a metric, which may not be agreed upon by all users.
* **Resolving redundancy:** For example, a contextual attribute like “country” may appear in multiple tables. Which table should I choose to back the “country” concept? Does the semantic layer allow us to use if/else to retrieve “country” from table A under one condition and from table B under another?
* **Resolving ambiguity:** You have to explicitly define primary keys and foreign keys to enable correct table joins, while your tables don’t actually have them.

All of these concerns should be handled in the data modeling layer. The semantic layer should serve only as a lightweight abstraction, not as a layer full of heavy data logic.

If you introduce a semantic layer hoping it will resolve an existing mess, you’ll only end up with another mess.

[![](https://substackcdn.com/image/fetch/$s_!eP8u!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fba05872f-b3ef-4779-9ab5-81fc5ea8ed81_596x570.png)](https://substackcdn.com/image/fetch/$s_!eP8u!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fba05872f-b3ef-4779-9ab5-81fc5ea8ed81_596x570.png)

When your organization’s data system is challenging to maintain, produces inconsistent results, and contains redundant entities, the first thing you should focus on is data modeling. Fix that foundation so data analysts can confidently examine the model and extract the necessary information, metrics, and dimensions on their own. Only then does it make sense to add a semantic layer to enable self-service analytics for non-technical users.

---

## Semantic layer and AI models

> *This section discusses how the semantic layer could help an AI model on its journey to understand your data.*

### AI models and the problem of understanding your data

In the past, business users seeking data insights had to contact the IT department for assistance. The business intelligence tools have evolved since then. Business users can now build their own charts or create reports with modern business intelligence tools, allowing them to drag-and-drop the data fields they want.

[![](https://substackcdn.com/image/fetch/$s_!_1sM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F374a329c-55c7-4bb9-9c61-208717552e4d_1498x832.png)](https://substackcdn.com/image/fetch/$s_!_1sM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F374a329c-55c7-4bb9-9c61-208717552e4d_1498x832.png)

The rise of AI chat interfaces like ChatGPT or Gemini makes people realize that “oh, using natural language is the most productive way to ask for insight”.

People want the AI models to understand the data system and answer their questions just like a data analyst. However, instructing AI models to accept natural-language input and generate reliable SQL queries is not easy.

Let’s first revisit some steps that humans take to write SQL:

[![](https://substackcdn.com/image/fetch/$s_!wWkF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5e1cae3a-bf16-4e15-a00c-2167e332e2bf_1216x706.png)](https://substackcdn.com/image/fetch/$s_!wWkF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5e1cae3a-bf16-4e15-a00c-2167e332e2bf_1216x706.png)

* We begin with the business question, the natural language query: for example, all countries with sales greater than 2,000 on Independence Day.
* We identify the entities: the countries, the sales, the context: June, and the condition: sales greater than 2,000.
* We find the relevant tables, columns, and records by looking at the database schema. The human interpretation is essential here, which kind of sales (assume the company has more than one product), and what date is Independence Day? (This varies in countries.) This step may require us to revisit the business users to request additional information.
* Then, we write SQL based on our understanding. We Select, Join, Group By, Where…

We humans, despite knowing what we are trying to do, still face challenging problems in handling the “text-to-SQL “ process: the uncertainty of the natural language, the database’s complexity, and the translation from the “flexible” natural language queries to the “strict” SQL queries.

* **Natural language uncertainty**: It’s normal for us to say a thing, and others understand it in different ways. This is called ambiguity. It could happen when a single word has multiple meanings, or a sentence can be parsed in various ways. We can ask others, observe around, or leverage our experience and understanding to resolve the ambiguity. Meanwhile, the AI models might only have a natural language query.

  [![](https://substackcdn.com/image/fetch/$s_!BwjF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc1da933c-0b47-4313-a40b-3542764f09b3_620x394.png)](https://substackcdn.com/image/fetch/$s_!BwjF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc1da933c-0b47-4313-a40b-3542764f09b3_620x394.png)
* **The database’s complexity**: Lack of robust data modeling, complex relationships between tables, ambiguous columns, or more than one way to calculate a metric. We might run around to ask for more clarification, cause some bugs, and create some weird reports before learning how to do it right. An AI model, somewhere on the internet, knows nothing about your company’s data system. How could we expect it to do better?

  [![](https://substackcdn.com/image/fetch/$s_!dT35!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcf58bb8f-7b5a-4e77-a840-081252c37bbd_602x382.png)](https://substackcdn.com/image/fetch/$s_!dT35!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcf58bb8f-7b5a-4e77-a840-081252c37bbd_602x382.png)
* **Text-to-SQL Translation**: Natural language is flexible, whereas SQL queries must adhere to a strict syntax. Even SQL queries could have different syntax depending on the standard and the database implementation. We require not only that the queries be executable, but also that they be readable, optimized, and reliable. Placing this responsibility on the AI models seems to overwhelm them, given that they may return low-performance queries, hard-to-debug ones, inaccurate results, or multiple SQL queries for the same prompt.

  [![](https://substackcdn.com/image/fetch/$s_!Bvfj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffbeb04c8-cc7c-4563-b268-cc56aea90cd3_654x446.png)](https://substackcdn.com/image/fetch/$s_!Bvfj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffbeb04c8-cc7c-4563-b268-cc56aea90cd3_654x446.png)

### The semantic layer can help.

In the paper “[A benchmark to understand the role of knowledge graphs on large language models’ accuracy for question answering on enterprise SQL databases](https://arxiv.org/pdf/2311.07509)”, the author created a robust benchmark series of questions with different levels of complexity using a standardized insurance dataset. They asked ChatGPT to answer the questions in two ways:

* Generate the SQL directly
* Generate the SQL with the help of a metadata layer called the knowledge graph

They observed that leveraging the knowledge graph improves result accuracy: the benchmark result in the third column shows the accuracy when using the knowledge graph. [Source](https://arxiv.org/pdf/2311.07509)

[![](https://substackcdn.com/image/fetch/$s_!RgiW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffc97906f-7dca-4473-98a0-dbb4a8a628f9_1004x266.png)](https://substackcdn.com/image/fetch/$s_!RgiW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffc97906f-7dca-4473-98a0-dbb4a8a628f9_1004x266.png)

Essentially, a knowledge graph is a structured way to represent knowledge about entities and their relationships, utilizing a graph-based data model.

And, the semantic layer can provide that information to some extent.

Recall that ambiguity and database complexity affect the accuracy of the text-to-SQL system. With the help of the semantic layer, the Text-to-SQL output could be more reliable:

* AI models don’t need to understand the database complexity anymore, as all the information they require is baked into the semantic layer, from the tables needed to the right way to join them. In other words, an AI model is enriched with context through the semantic layer.

  [![](https://substackcdn.com/image/fetch/$s_!Jcto!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f1f6979-810b-45f7-b8d0-5325c96ab039_530x486.png)](https://substackcdn.com/image/fetch/$s_!Jcto!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f1f6979-810b-45f7-b8d0-5325c96ab039_530x486.png)
* When a user requests “total sales,” the AI does not need to infer or guess the logic; it can simply reference the predefined “Total Sales” metric in the semantic layer, which already contains the calculation. This limits the ambiguity.
* The process of SQL generator could now be handled entirely in the semantic layer; the AI model's role is now to extract the entities from the human-language question and input them into the semantic layer. It’s more robust than having the AI model generate the SQL query from scratch.

  [![](https://substackcdn.com/image/fetch/$s_!CqYX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8b316b1c-3bc8-4768-9aa1-ae333857b0b9_1144x412.png)](https://substackcdn.com/image/fetch/$s_!CqYX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8b316b1c-3bc8-4768-9aa1-ae333857b0b9_1144x412.png)

The semantic layer can improve data understanding and AI-generated SQL.

> ***Note:** Saying this does not mean that only a semantic layer can help. A robust semantic layer does help, but recall from the previous section that the quality of the semantic layer also depends on the data modeling.*

That’s why I predict semantic models will receive more and more attention in the near future, as AI model adoption shows no signs of slowing.

---

## Outro

In this article, I try to deliver my understanding of the semantic layer. After an overview, we spent a fair amount of time discussing its role in analytical data architecture, especially when considering it alongside data modeling. Then we wrap up the article by discussing how the semantic layer could help AI models better understand our data system.

Thank you for reading this far. See you in my next articles.

---

## Reference

[1] Simon Späti, [Semantic Layer](https://www.ssp.sh/brain/semantic-layer#:~:text=sema/)
