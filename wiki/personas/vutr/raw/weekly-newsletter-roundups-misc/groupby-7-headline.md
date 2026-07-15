---
title: "GroupBy #7: The rise of data engineer, levels of abstractions, data modeling"
channel: vutr
published: 2023-10-31
url: https://vutr.substack.com/p/groupby-7-headline
paid: false
topics: ["Data Engineering", "Apache Spark", "Apache Flink", "Databricks", "BigQuery", "Data Modeling", "Streaming"]
tags: [https, auto, engineering, good, apache, substackcdn]
---

# GroupBy #7: The rise of data engineer, levels of abstractions, data modeling

*Plus: Release of Apache Flink 1.18, Making the Global Interpreter Lock Optional in CPython, ....*

> Source: [Open post](https://vutr.substack.com/p/groupby-7-headline)

## Topics

[[data-engineering|Data Engineering]] · [[apache-spark|Apache Spark]] · [[apache-flink|Apache Flink]] · [[databricks|Databricks]] · [[bigquery|BigQuery]] · [[data-modeling|Data Modeling]] · [[streaming|Streaming]]

---

*This is **vutrinh’s GroupBy**, a weekly send of cool resource on data engineering. Not subscribed yet? Here you go:*

[Subscribe now](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!d5-q!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F454858d9-527a-4e98-bca7-d07e38948717_1490x368.png)](https://substackcdn.com/image/fetch/$s_!d5-q!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F454858d9-527a-4e98-bca7-d07e38948717_1490x368.png)

[![](https://substackcdn.com/image/fetch/$s_!5dZL!,w_5760,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c05d076-a581-43f3-b6c0-7fdc929f5470_1300x900.png)](https://substackcdn.com/image/fetch/$s_!5dZL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c05d076-a581-43f3-b6c0-7fdc929f5470_1300x900.png)

---

> *👋 Hi, my name is Vu Trinh, a data engineer currently working at a mobile game company. I enjoy reading **good stuff** (related to data and engineering), and this newsletter is my effort on the journey to seek the "good stuff" across the entire Internet.*
>
> *Hope this issue finds you well.*

---

### *💣 Catch up with the world*

> *…Next Saturday night, we're sending you back to the future!*
>
> *— Dr. Emmett Brown, Back to the Future (1985) —*

* [BigQuery DataFrames](https://cloud.google.com/python/docs/reference/bigframes/latest) (Bigframes) is a Python API that you allow user to analyze data and perform machine learning tasks in BigQuery. [📖]

  + A [video](https://www.youtube.com/watch?v=hs-dJ5t5LGA) for a closer look at this exciting new library. [📺]
* [Meta contributes new features to Python 3.12](https://engineering.fb.com/2023/10/05/developer-tools/python-312-meta-new-features/) [📖]
* [AWS Glue for Apache Spark announces native connectivity for Google BigQuery](https://aws.amazon.com/about-aws/whats-new/2023/10/aws-glue-apache-spark-connectivity-google-bigquery/) [📖]
* BigQuery [custom data masking](https://cloud.google.com/bigquery/docs/user-defined-functions#custom-mask) now supports an expanded list of functions, including SHA hash functions with salt. [📖]
* [Announcing the Release of Apache Flink 1.18](https://flink.apache.org/2023/10/24/announcing-the-release-of-apache-flink-1.18/) [📖]
* [PEP 703 (Making the Global Interpreter Lock Optional in CPython) acceptance](https://discuss.python.org/t/pep-703-making-the-global-interpreter-lock-optional-in-cpython-acceptance/37075) [📖]

---

### *⚙ Engineering*

*we can validate it somehow*

> *Engineering is the practice of using natural science, mathematics, and the engineering design process to solve technical problems, increase efficiency and productivity, and improve systems.* — *wikipedia —*

* [The Rise of the Data Engineer](https://medium.com/free-code-camp/the-rise-of-the-data-engineer-91be18f1e603) [📖]

  + An article from 2017 but still relevant.
* [Revolutionizing Real-Time Streaming Processing: 4 Trillion Events Daily at LinkedIn](https://engineering.linkedin.com/blog/2023/revolutionizing-real-time-streaming-processing--4-trillion-event) [📖]
* [How does Grab’s Real-time Data Ingestion Work for Millions of RPM?](https://medium.com/javarevisited/how-does-grabs-real-time-data-ingestion-work-for-millions-of-rpm-7928a44d41c8) [📖]
* [Accelerating Spark: Databricks Photon Runtime](https://blog.devgenius.io/accelerating-spark-databricks-photon-runtime-9a7a53824d1b) [📖]
* [Bring Your Own Algorithm to Anomaly Detection](https://medium.com/pinterest-engineering/bring-your-own-algorithm-to-anomaly-detection-bdc0eef3fa79)[📖]
* [We have used too many levels of abstractions and now the future looks bleak](https://unixsheikh.com/articles/we-have-used-too-many-levels-of-abstractions-and-now-the-future-looks-bleak.html) [📖]

---

### *✏ Data*

*the paradox, the strange, the reality*

> *The one thing that this job has taught me is that truth is stranger than fiction.*
>
> *— Predestination (2014) —*

* [Data Modeling Best Practices to Unlock the Value of your Time-series Data](https://aws.amazon.com/blogs/database/data-modeling-best-practices-to-unlock-the-value-of-your-time-series-data/) [📖]
* [Your Org Don't Have Bad Data?](https://koopingshung.substack.com/p/your-org-dont-have-bad-data) [📖]
* [Data Modeling Fundamentals](https://medium.com/@seckindinc/data-modeling-fundamentals-dba245b7dc9f) [📖]
* [Unlocking the Secrets of Slowly Changing Dimension (SCD): A Comprehensive View of 8 Types](https://chengzhizhao.com/unlocking-the-secrets-of-slowly-changing-dimension-scd-a-comprehensive-view-of-8-types/#google_vignette) [📖]

---

> *Hasta la vista, baby.*
>
> *— T800, Terminator 2 (Judgment Day, 1991) —*

I apologize, but I can't resist quoting from movies.

[![](https://substackcdn.com/image/fetch/$s_!d5-q!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F454858d9-527a-4e98-bca7-d07e38948717_1490x368.png)](https://substackcdn.com/image/fetch/$s_!d5-q!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F454858d9-527a-4e98-bca7-d07e38948717_1490x368.png)

---

Thanks for reading this far! Subscribe for free to receive a weekly curated list of cooling resource on data engineering.
