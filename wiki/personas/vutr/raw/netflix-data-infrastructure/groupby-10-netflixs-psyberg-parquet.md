---
title: "GroupBy #10: Netflix's Psyberg, Parquet format, SQL is not Designed for Analytics"
channel: vutr
author: "Vu Trinh"
published: 2023-11-21
url: https://vutr.substack.com/p/groupby-10-netflixs-psyberg-parquet
paid: false
topics: ["Data Engineering", "Apache Airflow", "Apache Spark", "Apache Iceberg", "Apache Flink", "Snowflake", "Databricks", "BigQuery", "Streaming", "Data Quality"]
tags: [https, auto, linkedin, engineering, good, psyberg]
---

# GroupBy #10: Netflix's Psyberg, Parquet format, SQL is not Designed for Analytics

*Plus: Data Engineering Stream Project, Distributed System Course from MIT*

> Source: [Open post](https://vutr.substack.com/p/groupby-10-netflixs-psyberg-parquet)

## Topics

[[data-engineering|Data Engineering]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[apache-flink|Apache Flink]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[bigquery|BigQuery]] · [[streaming|Streaming]] · [[data-quality|Data Quality]]

---

*This is **GroupBy**, the place where I share with you guys the resources I learn from people smarter than me in data engineer field.*

*Not subscribed yet? Here you go:*

[Subscribe now](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!3Ia_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fae953b9d-a0fe-44aa-a02e-e625a97dbbb1_1300x900.png)](https://substackcdn.com/image/fetch/$s_!3Ia_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fae953b9d-a0fe-44aa-a02e-e625a97dbbb1_1300x900.png)

---

> *👋 Hi, my name is Vu Trinh, a data engineer.*
>
> *I enjoy reading **good stuff** (related to data and engineering), and this newsletter is my effort on the journey to seek the "good stuff" across the entire Internet.*
>
> *Hope this issue find you well.*

---

# 🎯 Side Project

> *40+ hours of debugging and you still want some more?*

To get your hand dirty (more), this week I will bring you a project:

## **[Data Engineering Project: Stream Edition](https://www.startdataengineering.com/post/data-engineering-project-for-beginners-stream-edition/)**

✍ [Joseph Machado](https://www.linkedin.com/in/josephmachado1991/)

[![](https://substackcdn.com/image/fetch/$s_!QUO0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb775849b-6555-4a01-9396-e5d570447059_1698x818.png)](https://substackcdn.com/image/fetch/$s_!QUO0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb775849b-6555-4a01-9396-e5d570447059_1698x818.png)

[author’s github repo](https://github.com/josephmachado/beginner_de_project_stream)

> *Our objectives are:*
>
> 1. *Enrich checkout data with the user name. The user data is in a transactional database.*
> 2. *Identify which click leads to a checkout (aka attribution). For every product checkout, we consider **the earliest click a user made on that product in the previous hour to be the click that led to a checkout**.*
> 3. *Log the checkouts and their corresponding attributed clicks (if any) into a table.*
>
>    — [author’s Github Repo](https://github.com/josephmachado/beginner_de_project_stream)—

> *The author's blog [Start Data Engineering](https://www.startdataengineering.com/) is a good place if you want to enhance you DE skill*

## Suggestion from me

> *If you're a fan of stream processing and looking for a resource to deep dive, here's a book that helped me a lot:*

## 📚┆[Streaming Systems: The What, Where, When, and How of Large-Scale Data Processing](https://www.amazon.com/Streaming-Systems-Where-Large-Scale-Processing/dp/1491983876)

✍ [Tyler Akidau](https://www.linkedin.com/in/takidau/), [Slava Chernyak](https://www.linkedin.com/in/slava-chernyak-2004b667/), [Reuven Lax](https://www.linkedin.com/in/reuven-lax-a82818/)

> *Expanded from [Tyler Akidau’s](https://www.linkedin.com/in/takidau/) popular blog posts "[Streaming 101](https://www.oreilly.com/radar/the-world-beyond-batch-streaming-101/)" and "[Streaming 102](https://www.oreilly.com/radar/the-world-beyond-batch-streaming-102/)", this book takes you from an introductory level to a nuanced understanding of the what, where, when, and how of processing real-time data streams.*

---

# 🐙 Learning resource

> *I love to learn, and I assume you do too.*

## 🎓 ┆📺┆[Distributed system course from MIT](https://www.youtube.com/playlist?list=PLrw6a1wE39_tb2fErI4-WkMbsvGQk9_UB) 🆓

> *80.123% (not an official statistic from me) of the tools that you use daily is a distributed system: Spark, Airflow, Flink, BigQuery, Snowflake, Redshift, S3, Databricks... you tell me.*

## 📖┆**[9 Fabulous Python Tricks That Make Your Code More Elegant](https://medium.com/techtofreedom/9-fabulous-python-tricks-that-make-your-code-more-elegant-bf01a6294908)**

✍ [Yang Zhou](https://medium.com/@yangzhou1993/about)

> *Talk is cheap. This article will demonstrate 9 fabulous Python tricks with beginner-friendly examples to help you write more Pythonic programs in your daily work.*

---

# 🚀 Engineering

> *I have to believe in a world outside my own mind.* — Memento *(2000)*

## 📖┆[Netflix](https://netflixtechblog.com/) technical blog series: **Incremental Data Processing with Late Arriving Data**

✍ *[Abhinaya Shetty](https://www.linkedin.com/in/abhinaya-shetty-ab871418/)*, *[Bharath Mummadisetty](https://www.linkedin.com/in/bharath-chandra-mummadisetty-27591a88/)*

> *In this three-part blog post series, we introduce you to Psyberg, our incremental data processing framework*

[![](https://substackcdn.com/image/fetch/$s_!uM1K!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc70d0400-7a40-43c0-baae-09e1c10b522e_1600x391.png)](https://substackcdn.com/image/fetch/$s_!uM1K!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc70d0400-7a40-43c0-baae-09e1c10b522e_1600x391.png)

**[Psyberg: The Game Changer.](https://netflixtechblog.com/1-streamlining-membership-data-engineering-at-netflix-with-psyberg-f68830617dd1#:~:text=Psyberg%3A%20The%20Game%20Changer!)**

**[1/3]**┆**[Streamlining Membership Data Engineering at Netflix with Psyberg](https://netflixtechblog.com/1-streamlining-membership-data-engineering-at-netflix-with-psyberg-f68830617dd1)**

**[2/3]**┆ **[Diving Deeper into Psyberg: Stateless vs Stateful Data Processing](https://netflixtechblog.com/2-diving-deeper-into-psyberg-stateless-vs-stateful-data-processing-1d273b3aaefb)**

**[3/3]**┆ **[Psyberg: Automated end to end catch up](https://netflixtechblog.com/3-psyberg-automated-end-to-end-catch-up-260fbe366fe2)**

## 📖┆[How to process extremely large (> 100TBs) data sets without burning millions](https://blog.dataengineer.io/p/how-to-optimize-100-tb-data-pipelines)

✍ [Zach Wilson](https://substack.com/@eczachly)

> *Facebook sends 50 BILLION NOTIFICATIONS every single day*

## 📺┆[The Parquet Format and Performance Optimization Opportunities](https://www.youtube.com/watch?v=1j8SdS7s_NY)┆[Databricks](https://www.databricks.com/)

🎙[Boudewijn Braams](https://www.linkedin.com/in/boudewijnbraams/)

> *…we will provide context around the Parquet format, covering the basics of structured data formats and the underlying physical data storage model alternatives (row-wise, columnar and hybrid).*

> 😉 *I highly recommend this for anyone who wants to deep dive in Parquet file format.*

---

# ✏ Data

> *The one thing that this job has taught me is that truth is stranger than fiction.*
>
> *— Predestination (2014)*

## 📖┆**[Data Documentation 101: Why? How? For Whom?](https://towardsdatascience.com/data-documentation-101-why-how-for-whom-927311354a92)**

✍ [Marie Lefevre](https://marielefevre.medium.com/about)

> *Will I find complete and reliable data documentation? And if so, where?*

## 📖┆[Data Observability vs. Data Quality](https://tdan.com/data-observability-vs-data-quality/31330)

✍ [Hazel Raoult](https://tdan.com/author/hraoult001)

> *This article covers the concepts of data observability vs. data quality, their key roles and benefits, differences and similarities, and how they can improve data usefulness.*

## 📖┆**[How we compute data lineage at Criteo](https://medium.com/criteo-engineering/how-we-compute-data-lineage-at-criteo-b3f09fc5c577)**

✍ [Miguel Liroz](https://medium.com/@mliroz)

> *At Criteo, lineage enables multiple use cases that are similar to the [usages in the industry](https://atlan.com/data-lineage-explained/):*
>
> *Impact analysis┆Root cause analysis┆Usage analysis┆Regulatory compliance┆Enhance metadata*

## 📖┆**[The Rise of the Semantic Layer: Metrics On-The-Fly](https://airbyte.com/blog/the-rise-of-the-semantic-layer-metrics-on-the-fly)**

✍ [Simon Späti](https://www.linkedin.com/in/sspaeti/)

> *You can think of a semantic layer as a **translation layer** between any data presentation layer (BI, notebooks, data apps) and the data sources.*

## 📖┆**[SQL is not Designed for Analytics](https://medium.pimpaudben.fr/sql-is-not-designed-for-analytics-079fc97b139c)**

✍ [Benoit Pimpaud](https://fromanengineersight.substack.com/)

> *It sounds like a hot take. But does a language created more than 30 years ago is still relevant to our analytics need?*

---

# 🤖 AI┆ML┆Data Science

> *You know, Burke, I don’t know which species is worse.*
>
> *— Ripley, Aliens (1986)*

## 📖┆**[Recommender systems: When they fail, who are you gonna call?](https://www.canva.dev/blog/engineering/recommender-systems-when-they-fail-who-are-you-gonna-call/)**┆[Canva](https://www.canva.dev/blog/engineering/)

✍ [Mayur Panchal](https://www.linkedin.com/in/panchalm), [Thien Bui](https://www.linkedin.com/in/ducthienbui/)

> *Unexpected results come in two forms: empty recommendations and irrelevant results. Recommendation models aren't always perfect, our models are no exception.*

## 📖┆[AI is coming for your favorite product's good user experience](https://benn.substack.com/p/ai-is-coming-for-your-favorite-products)

✍ [Benn Stancil](https://substack.com/@benn)

> *If you’re the CEO of a public company, Wall Street is probably going to [ask you questions](https://www.bloomberg.com/news/articles/2023-05-05/ai-scores-as-hot-topic-on-earnings-calls-as-interest-deepens) about how you plan to use AI to make your business better.*

## 📖┆**[Surprise, surprise: the data shows the impact of ChatGPT on the creative professions](https://medium.com/enrique-dans/surprise-surprise-the-data-shows-the-impact-of-chatgpt-on-the-creative-professions-b725ff28b40c)**

✍ [Enrique Dans](https://medium.com/@edans/about)

> *…the introduction of the ChatGPT generative algorithm a year ago has had significant negative effects on creative professions such as graphic designers and copywriters.*

## 📖┆[AI is Data Management’s Hail Mary Pass](https://joereis.substack.com/p/ai-and-data-managements-hail-mary)

✍ [Joe Reis](https://substack.com/@joereis)

> *I believe we’re going to see AI-driven data management.*

## 📖┆**[Speak Only About What You Have Read: Can LLMs Generalize Beyond Their Pretraining Data?](https://pub.towardsai.net/speak-only-about-what-you-have-read-can-llms-generalize-beyond-their-pretraining-data-041704e96cd5)**

✍ [Salvatore Raieli](https://salvatore-raieli.medium.com/about)

> *... What are the limits of this incredible capability? Where does it come from? Is it the secret ingredient to allows LLMs to bring us closer to artificial general intelligence?*

---

# 🔥 Catch up

> *…Next Saturday night, we're sending you back to the future!*
>
> *— Dr. Emmett Brown, Back to the Future (1985)*

## [📖] **[AWS Glue Data Catalog](https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html)**┆**[Now supports automatic compaction of Apache Iceberg tables](https://aws.amazon.com/blogs/aws/aws-glue-data-catalog-now-supports-automatic-compaction-of-apache-iceberg-tables/?sc_channel=sm&sc_campaign=DB_Blog&sc_publisher=LINKEDIN&sc_geo=GLOBAL&sc_outcome=awareness&trk=DB_Blog&linkId=248326984)**

## [📖] [BigQuery](https://cloud.google.com/bigquery?hl=en)┆Can now see query performance insights about [partition skew](https://cloud.google.com/bigquery/docs/query-insights#partition_skew).

## [📖] [Looker](https://cloud.google.com/looker?utm_source=google&utm_medium=cpc&utm_campaign=japac-SG-all-en-dr-SKWS-all-all-trial-DSA-dr-1605216&utm_content=text-ad-none-none-DEV_c-CRE_655856181323-ADGP_Hybrid+%7C+SKWS+-+BRO+%7C+DSA+~+All+Webpages-KWID_39700076131766622-aud-1596662388934:dsa-1456167871416&userloc_1028581-network_g&utm_term=KW_&gad_source=1&gclid=Cj0KCQiAmNeqBhD4ARIsADsYfTfLnkjrU3hJFil5XmpyGzjU6U9vC019qbdrN9Iu5IMiDCbf9zRHJJEaAqpQEALw_wcB&gclsrc=aw.ds&hl=en)┆[Powerful explorations, fresher data and faster filtering](https://cloud.google.com/blog/products/business-intelligence/looker-studio-brings-powerful-explorations-fresher-data-and-faster-filtering/)

## [📖] [Apache Hudi](https://hudi.apache.org/)┆[Release 1.0.0-beta1](https://hudi.apache.org/releases/release-1.0.0-beta1)

## [📖] [Apache Flink](https://flink.apache.org/)┆**[Disaggregated State Management roadmap for Flink 2.x](https://flink.apache.org/what-is-flink/roadmap/#disaggregated-state-management)**

`🚨 The next section contain my own writing. Don't blame me if you feel distressed after reading this; you chose to read it, although you can skip without thinking twice.`

# 🥷 It will steal 77 seconds from you

> *Random thoughts, ideas.*

[![](https://substackcdn.com/image/fetch/$s_!OpKI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F00497ef4-e566-47fd-a2d2-3d4d6a7e94d5_1538x382.png)](https://substackcdn.com/image/fetch/$s_!OpKI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F00497ef4-e566-47fd-a2d2-3d4d6a7e94d5_1538x382.png)

no flexing intention

79,713 people viewed my single post on LinkedIn, 468 liked it, 19 commented, and somehow 72 individuals wanted to put my boring stuff on their personal space.

These numbers used to be my motivation.

But it’s not anymore.

It soon makes me feel exhausted and empty.

I need something.

Something for me to pursue…

Then:

> *Ex-Stranger DM me on LinkedIn:*
>
> *"It might sound strange if I say this, but I'm having trouble with my Data Engineer career. Could you give me some advice?*
>
> *Hey, we were in the same university; let's hang out sometime and talk about DE stuff."*

People come and talk to me.

This is the thing that makes me truly happy now.

I have the chance to help those who struggle in their first steps in the DE path.

I have the chance to learn from awesome people.

More important,

I have the chance to speak out my thoughts.

Connection. Human connection.

The most rewarding reward.

The only thing I’m chasing now.

So when you're having trouble with your first steps on the DE path…

…or simply want to have a nerd to argue with you on some DE topics.

Feel free to reach me through: [Linkedin](https://www.linkedin.com/in/vutr27/) or [Email](http://vutrinh2704@gmail.com)

> *I’m not an expert, but I like to share my experience and listen to your thoughts.*

# “Hasta la vista, baby”

# -T800, Terminator 2: Judgment Day (1991)

Thanks for scrolling this far ! Convenient subscribe box here in case you want to scroll my newsletter right in your mailbox :D
