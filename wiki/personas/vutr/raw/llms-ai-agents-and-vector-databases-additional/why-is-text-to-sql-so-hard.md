---
title: "Why is Text-to-SQL so hard?"
channel: vutr
author: "Vu Trinh"
published: 2025-10-16
url: https://vutr.substack.com/p/why-is-text-to-sql-so-hard
paid: false
topics: ["Data Engineering", "Data Modeling"]
tags: [https, auto, substackcdn, image, fetch, good]
---

# Why is Text-to-SQL so hard?

*Why is there a need for it? What are its challenges? Is there a way to make it easier?*

> Source: [Open post](https://vutr.substack.com/p/why-is-text-to-sql-so-hard)

## Topics

[[data-engineering|Data Engineering]] · [[data-modeling|Data Modeling]]

---

> *I will publish a paid article every Tuesday. I wrote these with one goal in mind: to offer my readers, whether they are feeling overwhelmed when beginning the journey or seeking a deeper understanding of the field, 15 minutes of practical lessons and insights on nearly everything related to data engineering.*
>
> [Upgrade subscription](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!ntvL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf489800-9e74-445b-bc01-5f055c6d801c_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!ntvL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf489800-9e74-445b-bc01-5f055c6d801c_2000x1428.png)

---

## Intro

As Joe Reis and Matt Housley once said in the infamous book, [Fundamentals of Data Engineering](https://www.amazon.com/Fundamentals-Data-Engineering-Robust-Systems/dp/1098108302/ref=sr_1_1?adgrpid=116133839923&dib=eyJ2IjoiMSJ9.lYwfG6Cki9cIzZbbw-FkBLEGg8qxUMl8FddVr7cn3e53N5udUjs7b4Xw8dLmLC6PGFLeiu__B-8NQ3wXIYhVyEPbcg8uack-H3mXmSlnlOq03C-h9r-vAqimHYUHjeWDK5M0PDMpMm1vRjNLyn0lNEyy1K1YC4wfv1rfBRuxkjD_dMF6_EGdjKUD3aRjguPjldg1wmleWvAJk8jOE30xBiy4UispBaZe5IfRIW05prE.MyZpTE-b63KM3R6ZHK5T7A1Nfdy7SjwIihQnUHj3w5U&dib_tag=se&hvadid=585479350700&hvdev=c&hvlocphy=9198559&hvnetw=g&hvqmt=e&hvrand=16285984323524444922&hvtargid=kwd-902459765949&hydadcr=28046_14525503&keywords=fundamentals+of+data+engineering&mcid=1e34ef84df94373dafcb2867abec2b05&qid=1754635317&sr=8-1):

> *A data engineer manages the data engineering lifecycle, starting with extracting data from source systems and concluding with serving data for specific use cases.*

The data serving is the primary interface through which we provide our service to end users (e.g., data analysts, data scientists, business stakeholders). No matter how well we store, process, and manage the data, if users cannot access or use it reliably, we have failed.

Today, I want to discuss one of the hottest methods for serving data in the era of AI: natural language to SQL. We will first understand why text-to-SQL is receiving a lot of attention recently, what its challenges are, and then attempt to find a solution that addresses them.

## Why Text-to-SQL

In the past, if business users wanted to gain insight from the data, they had to communicate with the IT department so that these technical experts could assist them.

[![](https://substackcdn.com/image/fetch/$s_!tTOS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F16cb83ea-b843-4f1d-bf5b-7fa57ce034c5_484x462.png)](https://substackcdn.com/image/fetch/$s_!tTOS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F16cb83ea-b843-4f1d-bf5b-7fa57ce034c5_484x462.png)

The business intelligence tools have evolved since then. More functionalities, a shinier UI, the ability to connect to more systems, and most importantly, more friendly to non-technical users.

[![](https://substackcdn.com/image/fetch/$s_!MOK9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feb9bc64c-e111-4c3f-beae-8866a57f3b5b_1032x456.png)](https://substackcdn.com/image/fetch/$s_!MOK9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feb9bc64c-e111-4c3f-beae-8866a57f3b5b_1032x456.png)

From asking the technical team for help, business users can now build their own charts or create reports with the assistance of modern business intelligence tools, which allow them to drag-and-drop the data fields they want.

[![](https://substackcdn.com/image/fetch/$s_!AvDi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6be01640-b15b-40df-b7c5-a94231f1270c_556x288.png)](https://substackcdn.com/image/fetch/$s_!AvDi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6be01640-b15b-40df-b7c5-a94231f1270c_556x288.png)

But it seems like that’s not enough. The rise of AI chat interfaces like ChatGPT or Gemini makes people realize that “oh, using natural language is even more productive compared to the visual drag-and-drop.“ BI tools on the market are starting to integrate the ability to answer human questions with the help of AI models.

[![](https://substackcdn.com/image/fetch/$s_!tAiW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0a3c88a6-7fbf-415c-a5fc-8ba6cef7a10e_630x296.png)](https://substackcdn.com/image/fetch/$s_!tAiW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0a3c88a6-7fbf-415c-a5fc-8ba6cef7a10e_630x296.png)

The key is to enable the AI models to translate user input into SQL queries. Then, the tool will send the SQL to the database and create a chart/report based on the results.

Instead of choosing the `total\_sales` and `country` fields, a simple text, “Show me the total sales breakdown by country in the last month,” is more intuitive for the users. Integrating with AI makes a solution more compelling.

## Challenges of Text-to-SQL

> *I refer to the paper [“A Survey of Text-to-SQL in the Era of LLMs: Where are we, and where are we going?”](https://arxiv.org/html/2408.05109v5) for this section.*

Instructing AI models to accept natural language input and output a reliable SQL query is not easy to achieve. To better understand the challenges, let’s first revisit some steps that humans take to write SQL:

* We begin with the business question, the natural language query: for example, all countries with sales greater than 2,000 on Independence Day.

  [![](https://substackcdn.com/image/fetch/$s_!r4RV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb15250fb-05f2-487b-accb-65d51e605533_524x264.png)](https://substackcdn.com/image/fetch/$s_!r4RV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb15250fb-05f2-487b-accb-65d51e605533_524x264.png)
* In our brain, we identify the entities: the countries, the sales, the context: June, and the condition: sales greater than 2,000.

  [![](https://substackcdn.com/image/fetch/$s_!lT_I!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F06ea3302-444e-4221-9c27-e2887a677ccf_438x314.png)](https://substackcdn.com/image/fetch/$s_!lT_I!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F06ea3302-444e-4221-9c27-e2887a677ccf_438x314.png)
* We find the relevant tables, columns, and records by examining the database schema. The human interpretation is essential here, which kind of sales (assume the company has more than one product), and what date is Independence Day? (This varies in countries.) This step may require us to revisit the business users to request additional information.

  [![](https://substackcdn.com/image/fetch/$s_!j6_-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F13545902-789c-4812-893c-d1516cd259a7_472x406.png)](https://substackcdn.com/image/fetch/$s_!j6_-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F13545902-789c-4812-893c-d1516cd259a7_472x406.png)
* Then, we write SQL based on our understanding. We Select, Join, Group By, Where…

We, humans, despite knowing what we are trying to do, still have some challenging problems while handling the “text-to-SQL “ process: the uncertainty of the natural language, the database’s complexity, and the translation from the “flexible” natural language queries to the “strict” SQL queries.

### Natural language uncertainty

We use natural language from the day we learn to say our first words, such as “mama” or “papa“. We practice it every day, and the way we communicate depends significantly on who we are, how we grew up, and how we perceive the world.

It’s normal for us to say a thing, and others understand it in different ways. This is called ambiguity. It could happen when a single word has multiple meanings, …

[![](https://substackcdn.com/image/fetch/$s_!BwjF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc1da933c-0b47-4313-a40b-3542764f09b3_620x394.png)](https://substackcdn.com/image/fetch/$s_!BwjF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc1da933c-0b47-4313-a40b-3542764f09b3_620x394.png)

…or a sentence can be parsed in various ways.

[![](https://substackcdn.com/image/fetch/$s_!jQNr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F77c3e0b1-1adc-4ef9-9c9f-7334137e45d4_456x286.png)](https://substackcdn.com/image/fetch/$s_!jQNr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F77c3e0b1-1adc-4ef9-9c9f-7334137e45d4_456x286.png)

The uncertainty also stemmed from under-specification, which occurs when expressions lack sufficient detail or context to convey their intended meanings. For example, Independence Day in Vietnam is different from Independence Day in the United States of America.

We can ask others, observe around, or leverage our experience and understanding to resolve the ambiguity. Meanwhile, the AI models might only have a natural language query.

[![](https://substackcdn.com/image/fetch/$s_!32Up!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F22652ae7-c2e5-48e6-8c01-bbf560453772_480x248.png)](https://substackcdn.com/image/fetch/$s_!32Up!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F22652ae7-c2e5-48e6-8c01-bbf560453772_480x248.png)

### The database’s complexity

It’s common for us, data engineers, to handle messy data systems. Lack of robust data modeling, complex relationships between tables, ambiguous columns, or more than one way to calculate a metric.

[![](https://substackcdn.com/image/fetch/$s_!dT35!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcf58bb8f-7b5a-4e77-a840-081252c37bbd_602x382.png)](https://substackcdn.com/image/fetch/$s_!dT35!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcf58bb8f-7b5a-4e77-a840-081252c37bbd_602x382.png)

Let’s confess here, it is tough for us to do the right thing the first time with this data system. We might run around the companies to ask for more clarification, cause some bugs, and create some weird reports before learning how to do it right. An AI model, somewhere on the internet, knows nothing about your company’s data system. How could we expect it to do better than us?

### Text-to-SQL Translation

For the machine to understand, our Python or Java code must be translated into low-level machine language. This is a complex task, but at a high level, things are straightforward, as each language has a kind of dictionary to facilitate a one-to-one mapping between programming language code and machine code.

[![](https://substackcdn.com/image/fetch/$s_!ItYm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F373d505e-7721-4ed1-a755-9722606301c3_650x270.png)](https://substackcdn.com/image/fetch/$s_!ItYm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F373d505e-7721-4ed1-a755-9722606301c3_650x270.png)

However, converting text to SQL is more challenging than that, as it typically involves a one-to-many mapping between the input natural language query ←→ database entities and natural language query ←→ SQL query.

[![](https://substackcdn.com/image/fetch/$s_!Bvfj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffbeb04c8-cc7c-4563-b268-cc56aea90cd3_654x446.png)](https://substackcdn.com/image/fetch/$s_!Bvfj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffbeb04c8-cc7c-4563-b268-cc56aea90cd3_654x446.png)

Natural language is flexible, whereas SQL queries must adhere to a strict syntax. Even SQL queries could have different syntax depending on the standard and the database implementation.

We require not only that the queries be executable, but also that they be readable, optimized, and reliable. Placing this responsibility on the AI models seems to overwhelm them, given that they may return low-performance queries, hard-to-debug ones, inaccurate results, or multiple SQL queries for the same prompt.

This article is sponsored by [Holistics](http://holistics.io/), a self-service BI tool built for the AI era.

## So, is there a way for us to deal with these problems?

It turns out that there is a promising approach.

In the paper “[A benchmark to understand the role of knowledge graphs on large language models’ accuracy for question answering on enterprise SQL databases](https://arxiv.org/pdf/2311.07509)”, the author created a robust benchmark series of questions with different levels of complexity using a standardized insurance dataset. They asked ChatGPT to answer the questions in two ways:

* Generate the SQL directly
* Generate the SQL with the help of a knowledge graph

They observed that leveraging the knowledge graph indeed helps improve the accuracy of results:

[![](https://substackcdn.com/image/fetch/$s_!RgiW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffc97906f-7dca-4473-98a0-dbb4a8a628f9_1004x266.png)](https://substackcdn.com/image/fetch/$s_!RgiW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffc97906f-7dca-4473-98a0-dbb4a8a628f9_1004x266.png)

The benchmark result, the third column, presents the accuracy when using the knowledge graph. [Source](https://arxiv.org/pdf/2311.07509)

Essentially, a knowledge graph is a structured way to represent knowledge about entities and their relationships, utilizing a graph-based data model. There is a popular solution that offers the same benefit.

### Yes, it is the semantic layer

As a company’s business expands, the volume and variety of data increase; more decisions need to be made, more data must be stored, and more source data must be captured. Despite how well we prepare, data users might struggle to understand what they need to use the data effectively. We need a better abstraction layer that can lower the barrier for people.

The semantic layer is an abstraction layer that sits between the underlying data (e.g., data warehouses) and end-user applications (e.g., BI tools, data applications, or business users). From a high level, a semantic layer solution requires us to map business-friendly concepts to underlying data assets and specify the relationships between them.

[![](https://substackcdn.com/image/fetch/$s_!ZbLj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F747723bb-54b7-4675-ab12-2f6ff3bf26ad_1456x458.png)](https://substackcdn.com/image/fetch/$s_!ZbLj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F747723bb-54b7-4675-ab12-2f6ff3bf26ad_1456x458.png)

Thanks to that, the layer acts as a translator between the data and its users. It abstracts all the complexity to ensure that only understandable and business-friendly concepts are presented to users.

## Semantic layer’s role in Text-to-SQL tasks

Recall that ambiguity and database complexity affect the accuracy of the text-to-SQL system. With the help of the semantic layer, the Text-to-SQL output could be more reliable:

* AI models don’t need to understand the database complexity anymore, as all the information they require is baked into the semantic layer, from the tables needed to the right way to join them. In other words, an AI model is enriched with context through the semantic layer.

  [![](https://substackcdn.com/image/fetch/$s_!Jcto!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f1f6979-810b-45f7-b8d0-5325c96ab039_530x486.png)](https://substackcdn.com/image/fetch/$s_!Jcto!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f1f6979-810b-45f7-b8d0-5325c96ab039_530x486.png)
* When a user requests “total sales,” the AI does not need to infer or guess the logic; it can simply reference the predefined “Total Sales” metric in the semantic layer, which already contains the calculation. This limits the ambiguity.

## A real-world example

The semantic layer has emerged lately, given its ability to abstract the complexity of the underlying data systems. As discussed, this is not only a benefit to business users but also to the AI models. The layer is an indispensable part of modern BI tools, such as Tableau, Looker, and Power BI, as well as an interesting solution called [Holistics](https://www.holistics.io/).

[![](https://substackcdn.com/image/fetch/$s_!ikWQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F12d2e1ce-c1b4-4ca9-afb0-49078a25cc5e_276x88.png)](https://substackcdn.com/image/fetch/$s_!ikWQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F12d2e1ce-c1b4-4ca9-afb0-49078a25cc5e_276x88.png)

Established in 2015, the platform enables **self-service data access for the entire organization**. Compared to other BI tools, if users want to extract insight on Holistics, they must define their mapping between business concepts and the underlying tables via the semantic layer. Only after that, users can start presenting and organizing data using concepts exposed from the semantic layer.

[![](https://substackcdn.com/image/fetch/$s_!Xb91!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7ac5e474-5047-46c7-8dfc-4a0c2cffb53f_626x388.png)](https://substackcdn.com/image/fetch/$s_!Xb91!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7ac5e474-5047-46c7-8dfc-4a0c2cffb53f_626x388.png)

To work with the semantic layer, Holistics introduces the concept of “model“, which is an abstract representation on top of a table/query. A model should have the source (a physical table or a SQL query), the dimensions and measures, and the relationships to other models. Holistics uses relationships for constructing the join.

[![](https://substackcdn.com/image/fetch/$s_!tasX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffef594f9-382f-438e-97c1-413788587113_1078x746.png)](https://substackcdn.com/image/fetch/$s_!tasX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffef594f9-382f-438e-97c1-413788587113_1078x746.png)

An example of Holistics’s model’s dimension and measure definition. [Source](https://docs.holistics.io/docs/model-fields)

[![](https://substackcdn.com/image/fetch/$s_!rwOO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04853595-b4ba-4bc0-933a-bfb135771589_604x454.png)](https://substackcdn.com/image/fetch/$s_!rwOO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04853595-b4ba-4bc0-933a-bfb135771589_604x454.png)

An example of Holistics’s model’s relatitionship. [Source](https://docs.holistics.io/docs/relationships)

With Holistic’s vision of the semantic layer from the beginning, it would be easier for them to develop the text-to-SQL feature. They’ve tried several approaches, including letting the AI models offload the generation of SQL to the semantic layer by translating the user’s natural language input to a format that the semantic layer could understand, such as a JSON payload.

[![](https://substackcdn.com/image/fetch/$s_!UIKG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F23228cb8-31e4-4780-a222-b792ebe20319_930x498.png)](https://substackcdn.com/image/fetch/$s_!UIKG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F23228cb8-31e4-4780-a222-b792ebe20319_930x498.png)

By doing it this way, the text-to-SQL process can become even more reliable, as the SQL queries are now controlled by the semantic layer, which is designed to generate output queries based on well-tested logic and predefined entities within the semantic layer. Compared to the fact that the AI model has to guess, this way is more reliable.

## Even with the semantic layer, it might not be enough for text-to-SQL

Although relying entirely on the semantic layer could be beneficial, this approach may be limited by the fact that the input format, such as JSON, doesn’t provide users with the necessary flexibility in cases of complex analytics requirements.

For example, with the pseudo-format like this:

```
{ "metrics": ["total_sales"], "dimensions": ["country"]}
```

It serves well for simple questions. However, the key-value formats could cause users trouble when expressing queries that require more advanced techniques, such as nested aggregation or period-over-period comparison.

[![](https://substackcdn.com/image/fetch/$s_!tvdf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F58cf029a-e11b-4a85-9b70-cc99180d0104_758x434.png)](https://substackcdn.com/image/fetch/$s_!tvdf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F58cf029a-e11b-4a85-9b70-cc99180d0104_758x434.png)

So, letting the AI model generate the SQL directly is less reliable, but interacting via the semantic layer with the intermediate format is less flexible. What do we do?

[![](https://substackcdn.com/image/fetch/$s_!KX9I!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F95f45fc9-3374-4955-9ecd-765b60f55446_790x308.png)](https://substackcdn.com/image/fetch/$s_!KX9I!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F95f45fc9-3374-4955-9ecd-765b60f55446_790x308.png)

Holistics chooses to let the AI model generate the queries, but in a more reliable and controllable way. The model still leverages the help of the semantic layer for the business context and understanding; however, it has been trained to generate a new kind of query language instead of SQL. They call this AQL. s. Let’s delve into this language before moving on.

### The AQL language

When the platform was first built, the creator behind Holistics had already developed a proprietary language for analytics, known as [AQL](https://docs.holistics.io/as-code/aql/). This language is designed to leverage the defined semantic layer, allowing us to query data at a higher level of abstraction.

AQL treats metrics as first-class citizens, making metric definition composable and reusable. This differs from SQL, where everything is a query. If you want to reuse a piece of metrics, you must save the query that calculates it somewhere, such as in a CTE, a view, or a table. When adjusting the metric logic, you must modify the query.

[![](https://substackcdn.com/image/fetch/$s_!MuFh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9bd6bc41-69d0-419e-8d18-59418541bd6e_804x920.png)](https://substackcdn.com/image/fetch/$s_!MuFh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9bd6bc41-69d0-419e-8d18-59418541bd6e_804x920.png)

AQL queries are written using business concepts (dimensions and measures) defined in the semantic layer, not raw table and column names. A user can ask for `total\_revenue` by `user\_country` without having to write the complex JOIN statements. This abstraction simplifies query writing and drastically improves the readability and maintainability of analytics code.

Additionally, AQL introduces the pipe operator `|`, which takes the result of the expression on its left and uses it as the input for the function on its right. This creates a clear, sequential, top-to-bottom flow of logic.

[![](https://substackcdn.com/image/fetch/$s_!5bUh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F809780ae-dad0-401e-9865-35a721bfeed9_808x94.png)](https://substackcdn.com/image/fetch/$s_!5bUh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F809780ae-dad0-401e-9865-35a721bfeed9_808x94.png)

Count the number of male users. [Source](https://docs.holistics.io/as-code/reference/metric-expression)

[![](https://substackcdn.com/image/fetch/$s_!8f6p!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5ae9f3d8-c8de-44fd-90c9-ee33af08edc9_870x160.png)](https://substackcdn.com/image/fetch/$s_!8f6p!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5ae9f3d8-c8de-44fd-90c9-ee33af08edc9_870x160.png)

The running total of the number of orders in 2023. [Source](https://docs.holistics.io/as-code/reference/expression)

Users express their metrics using AQL; then, Holistics converts them to SQL queries and executes them on the defined database.

## The solution

Back to Holistics, the way they build the text-to-SQL will look like this: they trained their AI models to accept natural language input and output the AQL queries with the help of the semantic layer. The AQL query is then converted to a SQL query.

[![](https://substackcdn.com/image/fetch/$s_!Hy88!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe4fc26d3-4d41-4249-ae20-dcf47205bdd2_994x546.png)](https://substackcdn.com/image/fetch/$s_!Hy88!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe4fc26d3-4d41-4249-ae20-dcf47205bdd2_994x546.png)

The outcomes are AI-generated queries that are fundamentally more verifiable, reliable, and governed than those produced by systems that attempt direct text-to-SQL translation:

* **Verifiable & Readable:** Because AQL is a high-level language that operates on business logic, the queries it generates are far more compact and intuitive than raw SQL. A user can look at a piped AQL query and immediately understand the logical steps the AI is taking and ensure that AI really gets what the intent of the question is about

  [![](https://substackcdn.com/image/fetch/$s_!IbOn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F74702200-ed0d-4d2a-a8b4-e1c52caff799_552x380.png)](https://substackcdn.com/image/fetch/$s_!IbOn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F74702200-ed0d-4d2a-a8b4-e1c52caff799_552x380.png)

  + This human-readability is critical for verification; it allows the model trainer or the end users to understand what the AI is doing. This is an improvement compared to spending time reading messy SQL queries.
  + The high level abstraction AQL provides reduces risks of errors and hallucination as compared to the risk of AI errors from interpreting and using low level SQL queries from scratch.
  + Because the AQL-to-SQL conversion is managed by Holistics’ well-tested system, the generated SQL query is guaranteed once the AQL is correct.
* **Reliable:** By abstracting away the most error-prone aspects of query generation—such as dialect-specific syntax, complex join logic, and the formulas for advanced analytics—the system significantly increases its reliability.

  [![](https://substackcdn.com/image/fetch/$s_!hQJh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F65fbdb8a-edd8-4d7c-b62f-320ed6d441bb_532x262.png)](https://substackcdn.com/image/fetch/$s_!hQJh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F65fbdb8a-edd8-4d7c-b62f-320ed6d441bb_532x262.png)

  + The AI’s task is simplified to mapping intent to predefined metrics and dimensions in AQL. This leads to more accurate and dependable results.
* **Governed:** Because every AQL query must operate through the semantic layer, it automatically inherits the organization’s single source of truth for business definitions.

  [![](https://substackcdn.com/image/fetch/$s_!rg-C!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff3621057-2207-4b7d-a587-cc369c1d61c7_338x228.png)](https://substackcdn.com/image/fetch/$s_!rg-C!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff3621057-2207-4b7d-a587-cc369c1d61c7_338x228.png)

  + The AI won’t invent its metric calculations. Furthermore, access controls defined in the semantic layer are automatically enforced, ensuring that users can only query data to which they are authorized.
* **Flexibility**: AQL is designed to express complex metrics seamlessly, including AI; the capability of a text-to-SQL system will not be limited to simple queries only due to the limitation of the intermediate format, such as JSON.

---

## Outro

In this article, we first explore why extracting data insights using natural language is gaining increasing attention. Next, we examine the challenges of Text-to-SQL and find out that there is a promising solution to improve the accuracy with the help of the semantic layer.

Finally, we examine a real-life example: Holistics, which understands its solution to Text-to-SQL by leveraging semantic layers and its self-developed analytics language, AQL.

Thank you for reading this far. See you next time.

---

## Reference

*[1] Phuc Nguyen, [The Ideal Semantic Layer and Metric-Centric Paradigm](https://community.holistics.io/t/the-ideal-semantic-layer-and-metric-centric-paradigm-blog-post/1507), 2023*

*[2] Tan Huynh, [Metrics Deserve Better Composition Than What SQL Allows](https://www.holistics.io/blog/metrics-deserve-better-composition/#composition-in-sql), 2024*

*[3] [Holistics AI Architecture](https://docs.holistics.io/docs/ai/architecture)*

*[4] [Holistics Official Documentation](https://docs.holistics.io/docs/)*

*[5] Justin Heinze, [History of Business Intelligence](https://www.betterbuys.com/bi/history-of-business-intelligence/), 2020*
