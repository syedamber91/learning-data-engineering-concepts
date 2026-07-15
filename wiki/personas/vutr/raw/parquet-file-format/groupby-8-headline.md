---
title: "GroupBy #8: Demystifying the Parquet File, the future of the data engineer, intro to data modeling."
channel: vutr
author: "Vu Trinh"
published: 2023-11-06
url: https://vutr.substack.com/p/groupby-8-headline
paid: false
topics: ["Data Engineering", "dbt", "Apache Kafka", "Apache Spark", "Apache Iceberg", "Delta Lake", "BigQuery", "Data Modeling", "Change Data Capture"]
tags: [https, auto, engineering, medium, good, project]
---

# GroupBy #8: Demystifying the Parquet File, the future of the data engineer, intro to data modeling.

*Plus: Building a Data Engineering Project in 20 Minutes.*

> Source: [Open post](https://vutr.substack.com/p/groupby-8-headline)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[data-modeling|Data Modeling]] · [[change-data-capture|Change Data Capture]]

---

*This is **vutrinh’s GroupBy**, a weekly send of cool resource on data engineering. Not subscribed yet? Here you go:*

[Subscribe now](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!d5-q!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F454858d9-527a-4e98-bca7-d07e38948717_1490x368.png)](https://substackcdn.com/image/fetch/$s_!d5-q!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F454858d9-527a-4e98-bca7-d07e38948717_1490x368.png)

[![](https://substackcdn.com/image/fetch/$s_!kjYY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2d69f6e8-2b7b-4bc0-9c54-c6c49c706991_1300x900.png)](https://substackcdn.com/image/fetch/$s_!kjYY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2d69f6e8-2b7b-4bc0-9c54-c6c49c706991_1300x900.png)

---

> ***UPDATE**: Side Project Suggestion.*

> *👋 Hi, my name is Vu Trinh, a data engineer currently working at a mobile game company. I enjoy reading **good stuff** (related to data and engineering), and this newsletter is my effort on the journey to seek the "good stuff" across the entire Internet.*
>
> *Hope this issue finds you well.*

---

### 🎯 Side Project

*Get you hand dirty.*

#### ⤷ **[Building a Data Engineering Project in 20 Minutes](https://www.ssp.sh/blog/data-engineering-project-in-twenty-minutes/)**

📖 | ✍ [Simon Späti](https://www.linkedin.com/in/sspaeti/)

> *Author’s note : the project uses a very old version, 0.9 of [Dagster](https://github.com/dagster-io/dagster)*

So, you might find it a little bit difficult to get it up and running for the first time. But a little challenge can be fun, right?

(Yeah, Simon and I had a short conversation. 😄)

> *You'll learn web-scraping with real-estates, uploading them to S3, Spark and Delta Lake, adding Data Science with Jupyter, ingesting into Druid, visualising with Superset and managing everything with Dagster.*

[![Building a Data Engineering Project in 20 Minutes](https://substackcdn.com/image/fetch/$s_!00lg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F47692e4a-8ac5-4f82-8fbc-8be836ec5ea8_1182x526.png "Building a Data Engineering Project in 20 Minutes")](https://substackcdn.com/image/fetch/$s_!00lg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F47692e4a-8ac5-4f82-8fbc-8be836ec5ea8_1182x526.png)

Originally from author’s article

### 💡What you will learn

> *✅ Scraping with Beautiful Soup.*
>
> *✅ Change Data Capture (CDC) with Scraping.*
>
> *✅ How to use an S3-Gateway / Object Storage*
>
> *✅ UPSERTs and ACID Transactions.*
>
> *✅ Automatic Schema Evolution.*
>
> *✅ Integrating Jupyter Notebooks - the right way*
>
> *✅ Learning about Apache Druid.*
>
> *✅ Open-Source dashboarding with Apache Superset.*
>
> *✅ DevOps with Kubernetes.*
>
> *✅ Introduction to features of Dagster.*

---

### *🚀 Engineering*

> *Engineering is the practice of using natural science, mathematics, and the engineering design process to solve technical problems, increase efficiency and productivity, and improve systems.* — *wikipedia —*

#### ⤷ Dremio┆[Exploring the Architecture of Apache Iceberg, Delta Lake, and Apache Hudi](https://www.dremio.com/blog/exploring-the-architecture-of-apache-iceberg-delta-lake-and-apache-hudi/)

📖 | ✍ [Alex Merced](https://www.dremio.com/authors/alex-merced/)

#### ⤷ Meta┆[The future of the data engineer](https://medium.com/@AnalyticsAtMeta/the-future-of-the-data-engineer-part-i-32bd125465be)

📖 | ✍ [Analytics at Meta](https://medium.com/@AnalyticsAtMeta)

#### ⤷ [Demystifying the Parquet File Format](https://towardsdatascience.com/demystifying-the-parquet-file-format-13adb0206705)

📖 | ✍ [Michael Berk](https://www.linkedin.com/in/michael-berk-48783a146/overlay/about-this-profile/)

#### ⤷ Udemy┆[Introducing Hot and Cold Retries on Apache Kafka®](https://medium.com/udemy-engineering/introducing-hot-and-cold-retries-on-apache-kafka-f2f23595627b)

📖 | ✍ [Berat Cankar](https://medium.com/@berat.cankar?source=post_page-----f2f23595627b--------------------------------)

#### ⤷ Metaphor┆[The Grand Rewrite of DataHub](https://medium.com/metaphor-data/the-grand-rewrite-of-datahub-78cf989c7af8)

📖 | ✍ [Mars Lan](https://medium.com/@mars-lan)

#### ⤷ Agoda┆[Python GIL. Past and Future](https://medium.com/agoda-engineering/python-gil-past-and-future-8aff04061642)

📖 | ✍ [Agoda Engineering](https://medium.com/@agoda.eng)

---

### *✏ Data*

*the paradox, the strange, the reality*

> *The one thing that this job has taught me is that truth is stranger than fiction.*
>
> *— Predestination (2014) —*

#### ⤷ Preset┆**[Intro to Data Modeling](https://preset.io/events/intro-to-data-modeling/)**

📺 | ✍ [Shreesham Mukherjee](https://www.linkedin.com/in/shreesham/)

#### ⤷ [Is Kimball's Dimensional Modelling dead in 2022? Is OBT ("one big table") the way to go?](https://www.reddit.com/r/dataengineering/comments/uhohlv/is_kimballs_dimensional_modelling_dead_in_2022_is/)

🤖 | Reddit discussion

#### ⤷ Paypal┆[The next generation of Data Platforms is the Data Mesh](https://medium.com/paypal-tech/the-next-generation-of-data-platforms-is-the-data-mesh-b7df4b825522)

📖 | ✍ [Jean-Georges Perrin](https://medium.com/@jgperrin)

#### ⤷ [Data Entropy: More Data, More Problems?](https://towardsdatascience.com/data-entropy-more-data-more-problems-fa889a9dd0ec)

📖 | ✍ [Salma Bakouk](https://medium.com/@salmabakouk)

#### ⤷ Airbnb┆[Experiment Reporting Framework](https://medium.com/airbnb-engineering/experiment-reporting-framework-4e3fcd29e6c0)

📖 | ✍ [AirbnbEng](https://medium.com/@airbnbeng)

---

### *🔥 Catch up*

> *…Next Saturday night, we're sending you back to the future!*
>
> *— Dr. Emmett Brown, Back to the Future (1985) —*

#### google cloud

⚡The BigQuery Data Transfer Service can now [transfer data from Azure Blob Storage](https://cloud.google.com/bigquery/docs/blob-storage-transfer-intro) into BigQuery. [📖]

⚡BigQuery support for [change data capture (CDC)](https://cloud.google.com/bigquery/docs/change-data-capture) by processing and applying streamed changes in real-time to existing. [📖]

⚡BigQuery user can use [cached results](https://cloud.google.com/bigquery/docs/cached-results#cross-user-caching) from the same query issued by other users in the same project when using Enterprise or Enterprise Plus edition.

#### dbt

⚡[About dbt clone command](https://docs.getdbt.com/reference/commands/clone) [📖]

* Additional [article](https://docs.getdbt.com/blog/to-defer-or-to-clone) from dbt’s engineer.

#### mlflow

⚡[Release of MLflow 2.8.0](https://github.com/mlflow/mlflow/releases) [📖]

---

> *Hasta la vista, baby.*
>
> *— T800, Terminator 2 (Judgment Day, 1991) —*

I apologize, but I can't resist quoting from movies.

[![](https://substackcdn.com/image/fetch/$s_!d5-q!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F454858d9-527a-4e98-bca7-d07e38948717_1490x368.png)](https://substackcdn.com/image/fetch/$s_!d5-q!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F454858d9-527a-4e98-bca7-d07e38948717_1490x368.png)

---

Thanks for reading this far! Subscribe for free to receive a weekly curated list of cooling resource on data engineering.
