---
title: "GroupBy #11: Python at Meta, Netflix Incremental Processing with Apache Iceberg, 2023 AI year in brief"
channel: vutr
author: "Vu Trinh"
published: 2023-11-28
url: https://vutr.substack.com/p/groupby-11-netflix-incremental-processing
paid: false
topics: ["dbt", "Apache Airflow", "Apache Kafka", "Apache Spark", "Apache Iceberg", "Apache Flink", "Data Warehouse", "Data Lake", "Orchestration", "Streaming", "Data Quality"]
tags: [https, generative, auto, linkedin, microsoft, google]
---

# GroupBy #11: Python at Meta, Netflix Incremental Processing with Apache Iceberg, 2023 AI year in brief

*Plus: No-cost Generative AI courses, data streaming pipeline project*

> Source: [Open post](https://vutr.substack.com/p/groupby-11-netflix-incremental-processing)

## Topics

[[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[apache-flink|Apache Flink]] · [[data-warehouse|Data Warehouse]] · [[data-lake|Data Lake]] · [[orchestration|Orchestration]] · [[streaming|Streaming]] · [[data-quality|Data Quality]]

---

*This is **GroupBy**, the place where I share with you guys the resources I learn from people smarter than me in data engineer field.*

*Not subscribed yet? Here you go:*

[Subscribe now](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!GUa4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4ce3e5b-8aa1-4ad4-9913-9db7357f81d9_1300x900.png)](https://substackcdn.com/image/fetch/$s_!GUa4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4ce3e5b-8aa1-4ad4-9913-9db7357f81d9_1300x900.png)

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

## **🌊 [Building a Data Streaming Pipeline: Leveraging Kafka, Spark, Airflow, and Docker](https://medium.com/@simardeep.oberoi/building-a-data-streaming-pipeline-leveraging-kafka-spark-airflow-and-docker-16527f9e9142)**

✍ [Simardeep Singh](https://www.linkedin.com/in/simardeep--singh/)

> *In this guide, we’ll delve deep into constructing a robust data pipeline, leveraging a combination of Kafka for data streaming, Spark for processing, Airflow for orchestration, Docker for containerization, S3 for storage, and Python as our primary scripting language.*

> *Airflow*┆*Kafka*┆*Zookeeper*┆*Kafka Connect*┆*Schema Registry*┆*Spark*

[![](https://substackcdn.com/image/fetch/$s_!XZF7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F768b7024-fb7e-404f-aff8-d0d5fb334624_1578x1348.png)](https://substackcdn.com/image/fetch/$s_!XZF7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F768b7024-fb7e-404f-aff8-d0d5fb334624_1578x1348.png)

[from author original post](https://medium.com/@simardeep.oberoi/building-a-data-streaming-pipeline-leveraging-kafka-spark-airflow-and-docker-16527f9e9142)

---

# 🐙 Learning resource

> *If the world ends up like [The Terminator](https://www.imdb.com/title/tt0088247/), we should prepare knowledge about out enemy, right? (just kidding)*

## 🆓 resources from Microsoft and Google Cloud for you to get start in the world of Generative AI:

## 💾┆From [Microsoft](https://microsoft.github.io/):

## 🎓┆[Generative AI for Beginners - A Course](https://microsoft.github.io/generative-ai-for-beginners/#/?id=generative-ai-for-beginners-a-course)

> *A [12 Lesson course teaching everything you need to know to start building Generative AI applications](https://microsoft.github.io/generative-ai-for-beginners/#/?id=%f0%9f%97%83%ef%b8%8f-lessons)*

📜┆[Introduction to Generative AI and LLMs](https://microsoft.github.io/generative-ai-for-beginners/#/01-introduction-to-genai/README?wt.mc_id=academic-105485-koreyst)

📜┆[Exploring and comparing different LLMs](https://microsoft.github.io/generative-ai-for-beginners/#/02-exploring-and-comparing-different-llms/README?wt.mc_id=academic-105485-koreyst&id=exploring-and-comparing-different-llms)

📜┆[Using Generative AI Responsibly](https://microsoft.github.io/generative-ai-for-beginners/#/03-using-generative-ai-responsibly/README?wt.mc_id=academic-105485-koreyst&id=using-generative-ai-responsibly)

📜┆[Prompt Engineering Fundamentals](https://microsoft.github.io/generative-ai-for-beginners/#/04-prompt-engineering-fundamentals/README?wt.mc_id=academic-105485-koreyst&id=prompt-engineering-fundamentals)

📜┆[Creating Advanced prompts](https://microsoft.github.io/generative-ai-for-beginners/#/05-advanced-prompts/README?wt.mc_id=academic-105485-koreyst&id=creating-advanced-prompts)

📜┆[Building Text Generation Applications](https://microsoft.github.io/generative-ai-for-beginners/#/06-text-generation-apps/README?wt.mc_id=academic-105485-koreyst&id=building-text-generation-applications)

📜┆[…](https://microsoft.github.io/generative-ai-for-beginners/#/?id=%f0%9f%97%83%ef%b8%8f-lessons)

## ☁️┆From [Google Cloud](https://cloud.google.com/blog/):

## 🎓┆[Seven new no-cost generative AI training courses to advance your cloud career](https://cloud.google.com/blog/topics/training-certifications/new-google-cloud-generative-ai-training-resources)

> *These will help you gain critical skills as generative AI becomes more widely available.*

📜┆Introduction to [Generative AI](https://www.cloudskillsboost.google/course_templates/536) and [Large Language Models](https://www.cloudskillsboost.google/course_templates/539)

📜┆[Attention Mechanism](https://www.cloudskillsboost.google/course_templates/537)

📜┆[Transformer Models and BERT Model](https://www.cloudskillsboost.google/course_templates/538)

📜┆[Introduction to Image Generation](https://www.cloudskillsboost.google/course_templates/541)

📜┆[Create Image Captioning Models](https://www.cloudskillsboost.google/course_templates/542)

📜┆[Encoder-Decoder Architecture](https://www.cloudskillsboost.google/course_templates/543)

---

# 🚀 Engineering

> *I have to believe in a world outside my own mind.* — Memento *(2000)*

## 📖┆[What is an Open Table Format? & Why to use one?](https://www.startdataengineering.com/post/what_why_table_format/)

✍ [Joseph Machado](https://www.linkedin.com/in/josephmachado1991/) | [startdataengineering](https://www.startdataengineering.com/)

> *This post will review what open table formats are, their main benefits, and some examples with Apache Iceberg. By the end of this post, you will know what OTFs are, why you use them, and how they work.*

[![Architecture Comparison](https://substackcdn.com/image/fetch/$s_!nZaF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F09a8fa30-cc84-43f3-ad8f-195e0d412ebb_7868x2086.png "Architecture Comparison")](https://substackcdn.com/image/fetch/$s_!nZaF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F09a8fa30-cc84-43f3-ad8f-195e0d412ebb_7868x2086.png)

## 📖┆**[Incremental Processing using Netflix Maestro and Apache Iceberg](https://netflixtechblog.com/incremental-processing-using-netflix-maestro-and-apache-iceberg-b8ba072ddeeb)**

✍ [Jun He](https://www.linkedin.com/in/jheua/), [Yingyi Zhang](https://www.linkedin.com/in/yingyi-zhang-a0a164111/), and [Pawan Dixit](https://www.linkedin.com/in/pawan-dixit-b4307b2/)

> *We will show how we are building a clean and efficient incremental processing solution (IPS) by using Netflix Maestro and Apache Iceberg.*

## 🎙️┆[Writing and linting Python at scale](https://engineering.fb.com/2023/11/21/production-engineering/writing-linting-python-at-scale-meta/)┆[Meta](https://engineering.fb.com/)

[🎤 Pascal Hartig](https://engineering.fb.com/author/pascal-hartig/)

> *How Meta’s Python Foundation Team works to improve the developer experience of everyone working with Python at Meta; [Fixit 2](https://engineering.fb.com/2023/08/07/developer-tools/fixit-2-linter-meta/), Meta’s recently open-sourced linter framework; and what exactly the role of production engineer at Meta entails.*

## 📖┆**[Demystify Data Backfilling](https://towardsdatascience.com/demystify-data-backfilling-cf1713d7f7a3)**

✍ [Xiaoxu Gao](https://www.linkedin.com/in/xiaoxugao/)

> *Backfill is the process of filling in missing data from the past on a new table that didn’t exist before, or replacing old data with new records.*

## 📖┆[CPython Object System Internals: Understanding the Role of PyObject](https://codeconfessions.substack.com/p/cpython-object-system-internals-understanding)

✍ [Abhinav Upadhyay](https://substack.com/@abhinavupadhyay)

> *In this article, I plan to cover a basic idea behind how objects (or the data types) are implemented and represented within CPython. If you look at the CPython code, you will see a lot of references to PyObject, it plays a central role in the implementation of objects in Cpython.*

---

# ✏ Data

> *The one thing that this job has taught me is that truth is stranger than fiction.*
>
> *— Predestination (2014)*

## 📖┆**[The Need for an Open Standard for the Semantic Layer](https://cube.dev/blog/the-need-for-an-open-standard-for-the-semantic-layer)**┆[Cube](https://cube.dev/blog)

✍ [Artyom Keydunov](https://www.linkedin.com/in/keydunov/), [Brian Bickell](https://linkedin.com/in/bbickell)

> *Unfortunately for the developers of semantic layers, there is an ever-expanding set of technologies that customers expect to integrate with. One of my colleagues recently remarked “No one said it was going to be easy” and while I agree with him, **there is something we can adopt from other areas of technology with competing implementations: standardization.***

[![](https://substackcdn.com/image/fetch/$s_!iWtR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb985301e-b283-40e3-b74d-0fb7c4826b8c_1600x761.webp)](https://substackcdn.com/image/fetch/$s_!iWtR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb985301e-b283-40e3-b74d-0fb7c4826b8c_1600x761.webp)

from [author’s article](https://cube.dev/blog/the-need-for-an-open-standard-for-the-semantic-layer)

## 📖┆[The Rise of Data Contracts](https://dataproducts.substack.com/p/the-rise-of-data-contracts)

✍ [Chad Sanderson](https://substack.com/@chadsanderson)

> *My belief is that Data Contracts are the key to building a production-grade Data Warehouse and breaking the silo between data producers and data consumers. But what exactly is a data contract and why would you need one?*

## 📖┆[Tracking/Measurement/Collection/Creation - what was the question again?](https://substack.timodechau.com/p/trackingmeasurementcollectioncreation)

✍ [Timo Dechau](https://substack.com/@timodechau)

> *Trying to define something that needs definition but has a history that can't be changed easily.*

## 📖┆**[D3: An Automated System to Detect Data Drifts](https://www.uber.com/en-SG/blog/d3-an-automated-system-to-detect-data-drifts/)**

✍ [Uber Engineer Blog](https://www.uber.com/en-SG/blog/engineering/)

> *…Many data issues are manually detected by users weeks or even months after they start. Data regressions are hard to catch because the most impactful ones are generally silent. They do not impact metrics and ML models in an obvious way until someone notices something is off, which finally unearths the data issue.*

## 📖┆**[Why is data quality harder than code quality?](https://airbyte.com/blog/data-quality-issues)**┆[Airbyte](https://airbyte.com/blog)

✍ [Ari Bajo Rouvinen](https://www.linkedin.com/in/arimbr/)

> *As a data engineer, I always feel less confident about the quality of data I handle than the quality of code I write. Code, at least, I can run it interactively and write tests before deploying to production. Data, I most often have to wait for it to flow through the system and be used to encounter data quality issues.*

---

# 🤖 AI┆ML┆Data Science

> *You know, Burke, I don’t know which species is worse.*
>
> *— Ripley, Aliens (1986)*

## 📖┆**[The 2023 AI year in brief](https://levelup.gitconnected.com/the-2023-ai-year-in-brief-7eeaab2552b5)**

✍ [Salvatore Raieli](https://salvatore-raieli.medium.com/about)

> *This article is a brief recap of the most interesting trends and events that have most defined this 2023.*

## 📖┆[Google Cloud demonstrates the world’s largest distributed training job for large language models across 50000+ TPU v5e chips](https://cloud.google.com/blog/products/compute/the-worlds-largest-distributed-llm-training-job-on-tpu-v5e/)

✍ [Rajesh Anantharaman](https://www.linkedin.com/in/anantharamanrajesh/)

> *With the boom in generative AI, the size of foundational large language models (LLMs) has grown exponentially, utilizing hundreds of billions of parameters and trillions of training tokens.*

[![https://storage.googleapis.com/gweb-cloudblog-publish/images/Screenshot_2023-11-07_at_10.21.41_PM.max-1200x1200.png](https://substackcdn.com/image/fetch/$s_!P6nd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2a2b56a8-0369-47a9-8a46-fb33c95e0aa8_1132x772.png "https://storage.googleapis.com/gweb-cloudblog-publish/images/Screenshot_2023-11-07_at_10.21.41_PM.max-1200x1200.png")](https://substackcdn.com/image/fetch/$s_!P6nd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2a2b56a8-0369-47a9-8a46-fb33c95e0aa8_1132x772.png)

*Source: [“Computation used to train notable intelligence systems”](https://ourworldindata.org/grapher/artificial-intelligence-training-computation?zoomToSelection=true&time=2015-10-01..latest&country=GPT-3+175B+%28davinci%29~GPT-2~GPT~GPT~GPT~DALL-E~Chinchilla~Minerva+%28540B%29~LaMDA~PaLM+%28540B%29~Stable+Diffusion+%28LDM-KL-8-G%29~Transformer~Whisper~LLaMA+%2865B%29~Named+Entity+Recognition+model~Part-of-sentence+tagging+model~GNMT~BERT-Large~T5-11B~T5-3B~ALBERT-xxlarge~PLUG~ConSERT~HuBERT~AlphaCode~GPT-NeoX-20B~Sparse+all-MLP~NLLB~AlexaTM+20B~PaLM+2), One World Data*

## 📖┆[From AI to sustainability, why our latest data centers use 400G networking](https://dropbox.tech/infrastructure/from-ai-to-sustainability-why-our-latest-data-centers-use-400g-networking)┆[Dropbox](https://dropbox.tech/)

✍ [Daniel Parker](https://www.linkedin.com/in/daniel-parker-708bba7/) and [Amit Chudasma](https://www.linkedin.com/in/amit-chudasma-9b645445/)

> *At Dropbox, AI-powered tools and features are quickly transforming the way our customers find, organize, and understand their data. [Dropbox Dash](https://dropbox.com/dash) brings AI-powered universal search to all your apps, browser tabs, and cloud docs, while Dropbox AI can summarize and answer questions about the content of your files.*

## 📖┆**[Wisdom of Unstructured Data: Building Airbnb’s Listing Knowledge from Big Text Data](https://medium.com/airbnb-engineering/wisdom-of-unstructured-data-building-airbnbs-listing-knowledge-from-big-text-data-7c533466a63c)**

✍ [Hongwei Harvey Li](https://www.linkedin.com/in/hwlical/)

> *How Airbnb leverages ML/NLP to extract useful information about listings from unstructured text data to power personalized experiences for guests.*

## 📖┆**[Causal Machine Learning for Creative Insights](https://netflixtechblog.com/causal-machine-learning-for-creative-insights-4b0ce22a8a96)**

✍ [Billur Engin](https://www.linkedin.com/in/billurengin/), [Yinghong Lan](https://www.linkedin.com/in/yinghong-lan-2368656b/), [Grace Tang](https://www.linkedin.com/in/tsmgrace/), [Cristina Segalin](https://www.linkedin.com/in/cristinasegalin/), [Kelli Griggs](https://www.linkedin.com/in/kelli-griggs-32990125/), [Vi Iyengar](https://www.linkedin.com/in/vi-pallavika-iyengar-144abb1b/)

> *At Netflix, we want our viewers to easily find TV shows and movies that resonate and engage. Our creative team helps make this happen by designing promotional artwork that best represents each title featured on our platform. What if we could use machine learning and computer vision to support our creative team in this process?*

---

# 🔥 Catch up

> *…Next Saturday night, we're sending you back to the future!*
>
> *— Dr. Emmett Brown, Back to the Future (1985)*

## [📖] [OneTable](https://onetable.dev/)┆[Microsoft and Google join](https://venturebeat.com/data-infrastructure/exclusive-microsoft-and-google-join-forces-on-onetable-an-open-source-solution-for-data-lake-challenges/) forces on OneTable, an open-source solution for data lake challenges

## [📖] **[Soda](https://www.soda.io/)**┆**[Releases OSS Data Contract Engine](https://www.soda.io/resources/soda-releases-oss-data-contract-engine?ref=blef.fr)**

## [📖] [Kafka](https://github.com/apache/kafka)┆**[The marriage of Parquet and Kafka](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1008%3A+ParKa+-+the+Marriage+of+Parquet+and+Kafka)**

## [📖] [Flink](https://github.com/apache/flink)┆[Now generally available for Amazon EMR on EKS](https://aws.amazon.com/about-aws/whats-new/2023/11/apache-flink-available-amazon-emr-eks/)

## [📖] **[dbt](https://github.com/dbt-labs/dbt-core)**┆**[dbt Cloud is now available for Microsoft Fabric](https://www.getdbt.com/blog/dbt-cloud-is-now-available-for-microsoft-fabric)**

---

# 🥷 It will steal 7 seconds from you

> *Random thoughts, ideas.*

I'm drowning in deadlines.

(Trying to save my annual performance review 😭)

So, I will leave you guys alone this week and will be back blabbing next time. 😁

# “Hasta la vista, baby”

# -T800, Terminator 2: Judgment Day (1991)

Thanks for scrolling this far ! Convenient subscribe box here in case you want to scroll my newsletter right in your mailbox :D
