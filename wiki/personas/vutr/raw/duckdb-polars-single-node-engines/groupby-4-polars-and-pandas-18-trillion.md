---
title: "GroupBy #4: Polars and Pandas, 1.8 trillion events, data quality "
channel: vutr
author: "Vu Trinh"
published: 2023-10-10
url: https://vutr.substack.com/p/groupby-4-polars-and-pandas-18-trillion
paid: false
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Kafka", "Apache Spark", "Apache Flink", "Snowflake", "BigQuery", "Data Modeling", "Data Warehouse", "Streaming", "Data Quality"]
tags: [https, auto, media, substackcdn, image, fetch]
---

# GroupBy #4: Polars and Pandas, 1.8 trillion events, data quality 

*Plus: author's SQL execution order note, suggest research topic and a side project,...*

> Source: [Open post](https://vutr.substack.com/p/groupby-4-polars-and-pandas-18-trillion)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-flink|Apache Flink]] · [[snowflake|Snowflake]] · [[bigquery|BigQuery]] · [[data-modeling|Data Modeling]] · [[data-warehouse|Data Warehouse]] · [[streaming|Streaming]] · [[data-quality|Data Quality]]

---

*This is **vutrinh’s GroupBy**, a weekly send of cool resource on data engineering. Not subscribed yet? Here you go:*

[Subscribe now](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!Blyd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a749606-0c01-43ed-b3f7-69e42795d28f_1490x368.png)](https://substackcdn.com/image/fetch/$s_!Blyd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a749606-0c01-43ed-b3f7-69e42795d28f_1490x368.png)

[![](https://substackcdn.com/image/fetch/$s_!WwPa!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcbfa6e13-6438-4648-9d06-9325972f128f_1300x900.png)](https://substackcdn.com/image/fetch/$s_!WwPa!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcbfa6e13-6438-4648-9d06-9325972f128f_1300x900.png)

[![](https://substackcdn.com/image/fetch/$s_!YXtR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67843267-ad25-497e-92ba-47d7cc53b5b3_1490x368.png)](https://substackcdn.com/image/fetch/$s_!YXtR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67843267-ad25-497e-92ba-47d7cc53b5b3_1490x368.png)

…and you need to *consume this:*

### *⚙ Engineering*

*we can validate it somehow*

* [How Agoda manages 1.8 trillion Events per day on Kafka](https://medium.com/agoda-engineering/how-agoda-manages-1-8-trillion-events-per-day-on-kafka-1d6c3f4a7ad1) [📖]
* [From Zero to 50 Million Uploads per Day: Scaling Media at Canva](https://www.canva.dev/blog/engineering/from-zero-to-50-million-uploads-per-day-scaling-media-at-canva/) [📖]
* [Pandas 2.0 vs Polars: The Ultimate Battle](https://medium.com/cuenex/pandas-2-0-vs-polars-the-ultimate-battle-a378eb75d6d1)[📖]
* [Explain like I’m 5 — Vector Database Hype](https://medium.com/geekculture/explain-like-im-5-vector-database-hype-bd936fd319ff) [📖]
* [How Discord Stores Trillions of Messages | Deep Dive](https://www.youtube.com/watch?v=xynXjChKkJc) [📺]
* [Building A Robust Data Pipeline With Great Expectations, dbt and Airflow](https://medium.com/@Sasakky/building-a-robust-data-pipeline-with-great-expectations-dbt-and-airflow-d12b8bba030) [📖]

### *✏ Data*

*the paradox, the strange, the reality*

* [Data Quality Automation at Twitter](https://blog.twitter.com/engineering/en_us/topics/infrastructure/2022/data-quality-automation-at-twitter) [📖]
* [How Google, Uber, and Amazon Ensure High-Quality Data at Scale](https://medium.com/swlh/how-3-of-the-top-tech-companies-approach-data-quality-79c3146fd959) [📖]
* [An appropriately unhinged deep dive into Kimball slowly changing dimensions](https://faithfacts.substack.com/p/an-appropriately-unhinged-deep-dive-1c3) [📖]
* [About Data User Experience](https://substack.timodechau.com/p/about-data-user-experience) [📖]
* [How to pass the data modeling round in big tech data engineering interviews](https://blog.dataengineer.io/p/how-to-pass-the-data-modeling-round) [📖]
* [Data Warehouse Design – Inmon versus Kimball](https://tdan.com/data-warehouse-design-inmon-versus-kimball/20300) [📖]

### *🧠 AI*

*more and more confused*

* [Latest Memo: How is GenAI different from other code generators?](https://martinfowler.com/articles/exploring-gen-ai.html#memo-07:~:text=Latest%20Memo%3A%20How%20is%20GenAI%20different%20from%20other%20code%20generators%3F) [📖]
* [5 Generative AI Use Cases Companies Can Implement Today](https://medium.com/towards-data-science/5-generative-ai-use-cases-companies-can-implement-today-f458707bfbbe) [📖]
* [ChatGPT Prompts for SQL](https://medium.com/artificial-corner/chatgpt-prompts-sql-d311e452f90a) [📖]

### *💣 Catch up*

*back to the future*

* Give it a look on [dbt’s semantic layer](https://docs.getdbt.com/docs/use-dbt-semantic-layer/quickstart-sl). [DBT]
* Now you can [keep track cluster activity in Airflow from the version 2.7.](https://airflow.apache.org/blog/airflow-2.7.0/#cluster-activity-ui) [AIRFLOW]
* [OpenAI said to be considering developing its own AI chips](https://techcrunch.com/2023/10/06/openai-said-to-be-considering-developing-its-own-ai-chips/) [TECHCRUNCH]
* [Dataiku Launches LLM Mesh in Collaboration with Snowflake, Pinecone, and AI21 Labs](https://www.dbta.com/Editorial/News-Flashes/Dataiku-Launches-LLM-Mesh-in-Collaboration-with-Snowflake-Pinecone-and-AI21-Labs-160826.aspx) [DBTA]
* [So long data silos: Announcing BigQuery Omni cross-cloud joins](https://cloud.google.com/blog/products/data-analytics/announcing-bigquery-omni-cross-cloud-joins) [GOOGLE CLOUD]
* Google Cloud [Duet AI](https://cloud.google.com/blog/products/data-analytics/whats-new-with-data-analytics-and-ai-at-next23#:~:text=Boost%20data%20team%20productivity%20with%20Duet%20AI) and [BigQuery Studio](https://cloud.google.com/blog/products/data-analytics/announcing-bigquery-studio) will make you … wow [GOOGLE CLOUD]

[![](https://substackcdn.com/image/fetch/$s_!8to-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F34212f0e-be96-43a9-88a9-916df4ff519c_1490x368.png)](https://substackcdn.com/image/fetch/$s_!8to-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F34212f0e-be96-43a9-88a9-916df4ff519c_1490x368.png)

*Recommended topics for research, concept learning, or side projects*

### *🔎 Research Topic*

*I love to ask “why”. How about you? This section will suggest a random topic related to data engineering that you might want to explore in-depth by yourself.*

**Suggested Topic**

> Is MapReduce actually replaced by Apache Spark? If it’s true, what makes Spark really standout?

**You might want to begin with this:**

> [Is Spark really faster than MapReduce?](https://www.quora.com/Why-is-Hadoop-slower-than-Spark/answer/Travis-Addair?ch=10&oid=173920889&share=8bc70da5&srid=uIVXeO&target_type=answer)

### *📁 Project*

*A side project on the weekend to get you hands dirty?*

This week, you might want to run your own streaming pipeline by [this cool project](https://www.startdataengineering.com/post/data-engineering-project-for-beginners-stream-edition/):

[![Architecture](https://substackcdn.com/image/fetch/$s_!ugMt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8fb92edc-1a0c-4b9c-8c08-2fd251c15b81_1367x724.png "Architecture")](https://substackcdn.com/image/fetch/$s_!ugMt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8fb92edc-1a0c-4b9c-8c08-2fd251c15b81_1367x724.png)

[project’s architecture](https://www.startdataengineering.com/post/data-engineering-project-for-beginners-stream-edition/#:~:text=2.2.-,Architecture,-Our%20streaming%20pipeline)

You’ll get through:

* The **architecture**
* Run your own setup using *[Docker Composer](https://docs.docker.com/compose/#:~:text=Compose%20is%20a%20tool%20for%20defining%20and%20running%20multi%2Dcontainer%20Docker%20applications)*
* **Code design**
* Streaming concept like watermark, [back pressure](https://medium.com/@jayphelps/backpressure-explained-the-flow-of-data-through-software-2350b3e77ce7#:~:text=Resistance%20or%20force%20opposing%20the%20desired%20flow%20of%20data%20through%20software.), join in streaming,…
* How to monitor the Flink pipeline

[![](https://substackcdn.com/image/fetch/$s_!j_Ep!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf04a05b-735f-4534-9c8b-cf5b4ea4f928_1490x368.png)](https://substackcdn.com/image/fetch/$s_!j_Ep!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf04a05b-735f-4534-9c8b-cf5b4ea4f928_1490x368.png)

*author’s work*

[![](https://substackcdn.com/image/fetch/$s_!9Zwc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6b484ba4-ac78-4063-a6ae-8afee9944c98_1080x512.gif)](https://substackcdn.com/image/fetch/$s_!9Zwc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6b484ba4-ac78-4063-a6ae-8afee9944c98_1080x512.gif)

SQL execution

I decided to make a note of the SQL execution order, which I would send to myself in the past if it were possible (to help me pass an interview with my favorite company).

* **FROM:** The journey begins with the `FROM` clause, where you identify the tables you'll work with.
* **JOINs:** If you're joining multiple tables (and you usually are), this is where it happens. The `JOIN` conditions are applied to filter and combine rows from different tables.
* **WHERE:** Next, the `WHERE` clause filters rows from the result set based on specified conditions.
* **GROUP BY:** If you have a `GROUP BY` clause, SQL groups rows with the same values in specified columns into subsets.
* **HAVING:** Following the `GROUP BY`, the `HAVING` clause filters groups created by the `GROUP BY` clause.
* **SELECT:** and here when `SELECT` clause comes into play, specifying which columns to include in the final result set. Here's where calculations, expressions, and aliases are performed.
* **ORDER BY:** If you want your results sorted, the `ORDER BY` clause arranges the rows based on specified columns and order.
* **LIMIT** Finally, if you're fetching only a subset of the result set, you can use the `LIMIT` and `OFFSET` clauses for pagination.

[![](https://substackcdn.com/image/fetch/$s_!U4xl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fac797382-e101-48ca-bc7e-951ea3a10fff_1490x368.png)](https://substackcdn.com/image/fetch/$s_!U4xl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fac797382-e101-48ca-bc7e-951ea3a10fff_1490x368.png)

Thanks for reading this far! Subscribe for free to receive a weekly curated list of cooling resource on data engineering.
