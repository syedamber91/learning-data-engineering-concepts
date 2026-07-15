---
title: "GroupBy #23: Meta loves Python, How Uber Serves Over 40 Million Reads Per Second from Online Storage Using an Integrated Cache"
channel: vutr
author: "Vu Trinh"
published: 2024-02-20
url: https://vutr.substack.com/p/groupby-23-meta-loves-python-how
paid: false
topics: ["Data Engineering", "dbt", "BigQuery", "Data Modeling", "Data Warehouse", "Lakehouse", "Streaming"]
tags: [https, engineering, medium, source, substack, blog]
---

# GroupBy #23: Meta loves Python, How Uber Serves Over 40 Million Reads Per Second from Online Storage Using an Integrated Cache

*Plus: Why Data is an Incomplete Representation of Reality, An algorithm for high-performance engineering teams.*

> Source: [Open post](https://vutr.substack.com/p/groupby-23-meta-loves-python-how)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[bigquery|BigQuery]] · [[data-modeling|Data Modeling]] · [[data-warehouse|Data Warehouse]] · [[lakehouse|Lakehouse]] · [[streaming|Streaming]]

---

*This is **GroupBy**, where I share the resources I learn from people smarter than me in the data engineering field.*

*Not subscribed yet? Here you go:*

[Subscribe now](https://vutr.substack.com/subscribe?)

![](https://substackcdn.com/image/fetch/$s_!D8N-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fvutr.substack.com%2Fimg%2Fsubstack.png)

Get more from Vu Trinh in the Substack app

Available for iOS and Android

[Get the app](https://substack.com/app/app-store-redirect?utm_campaign=app-marketing&utm_content=author-post-insert&utm_source=vutr)

> *👋 Hi, my name is Vu Trinh, a data engineer.*
>
> *I enjoy reading **good stuff** (related to data and engineering), and this newsletter is my effort on the journey to seek the "good stuff" across the entire Internet.*
>
> *Hope this issue find you well.*

---

## Referral Program

I’m launching a referral program to grow the community by giving you guys valuable gifts whenever you reach a referral milestone. The condition is simple: you refer friends to subscribe to my newsletter, and you will receive a gift based on the number of friends you refer. Here are the reward milestones:

[![](https://substackcdn.com/image/fetch/$s_!lf_-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4c72d52-a2c4-4e24-9714-04e72a4dc087_756x361.png)](https://substackcdn.com/image/fetch/$s_!lf_-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4c72d52-a2c4-4e24-9714-04e72a4dc087_756x361.png)

Now, let’s refer friends and claim exciting rewards ;)

[Refer a friend](https://vutr.substack.com/leaderboard?&referrer_token=1xrjxy&utm_source=post)

---

[![](https://substackcdn.com/image/fetch/$s_!kbCi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff3f2fd65-f4d7-4e33-bd2b-11449e48a327_1400x1000.png)](https://substackcdn.com/image/fetch/$s_!kbCi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff3f2fd65-f4d7-4e33-bd2b-11449e48a327_1400x1000.png)

I love flower recently or maybe I’m too lazy to think for other idea for [image generating](https://www.canva.com/ai-image-generator/).

---

# 📈 Career

> *Don't let comfort hold you back.*

#### 📖┆[Table Selection in Software Engineering](https://luminousmen.com/post/table-selection-in-software-engineering)

✍ [Kirill Bobrov](https://www.linkedin.com/in/luminousmen/)

> *In the world of poker, there is a strategy that goes beyond just playing the game well – it's about choosing the right table. The idea here is clear: why struggle against the best when you can excel among the rest? This can also be applied to navigating career in software engineering. Why not play smart by picking your battles - or in this case, the company, project and team that aligns with your strengths and goals.*

#### 📖┆[An algorithm for high-performance engineering teams](https://atomic.engineering/an-algorithm-for-high-performance-engineering-teams-3be015341e5e)

✍ [Jacob Bennett](https://jacobistyping.medium.com/)

> *Great teams don’t start great. They become great through focused effort.*

#### 📖┆[How to grow from a mid-level to senior Data Engineer](https://seattledataguy.substack.com/p/how-to-grow-from-mid-level-to-senior)

✍ [SeattleDataGuy](https://substack.com/@seattledataguy) + [Gregor Ojstersek](https://substack.com/@gregorojstersek)

> *How to grow from mid to senior level? That is a common question that a lot of engineers are asking and trying to get to know more about. There are a lot of different ways to get there and in this article, Gregor Ojstersek, CTO and Author of Engineering Leadership newsletter will walk us through from a perspective of a manager.*

#### 📖┆[Will GenAI Replace Data Engineers? No - And Here’s Why.](https://medium.com/@barrmoses/will-genai-replace-data-engineers-no-and-heres-why-708b0a27da6b)

✍ [Barr Moses](https://barrmoses.medium.com/)

> *While I can’t in good conscience say ‘not in a million years’ (I’ve seen enough sci-fi movies to know better), I can say with a pretty high degree of confidence “I don’t think so.” At least, not anytime soon. Here’s why.*

---

# 🚀 Engineering

> *I have to believe in a world outside my own mind. — Memento (2000)*

#### 🎙️ ┆[Meta loves Python](https://engineering.fb.com/2024/02/12/developer-tools/meta-loves-python/)

🎤[Pascal Hartig](https://engineering.fb.com/author/pascal-hartig/)

> *Meta engineer Pascal Hartig (@passy) is joined on the Meta Tech Podcast by Itamar Oren and Carl Meyer, two software engineers at Meta, to discuss their teams’ contributions to the latest Python release, including new hooks that allow for custom JITs like Cinder, Immortal Objects, improvements to the type system, faster comprehensions, and more.*

#### 📖┆[How Uber Serves Over 40 Million Reads Per Second from Online Storage Using an Integrated Cache](https://www.uber.com/en-SG/blog/how-uber-serves-over-40-million-reads-per-second-using-an-integrated-cache/)

✍ [Uber Engineering Blog](https://www.uber.com/en-SG/blog/engineering/data/?uclick_id=15b6739c-0acd-406e-bdf6-884992beefa0)

> *Docstore is Uber’s in-house, distributed database built on top of MySQL®. Storing tens of PBs of data and serving tens of millions of requests/second, it is one of the largest database engines at Uber used by microservices from all business verticals. Since its inception in 2020, Docstore users and use cases are growing, and so are the request volume and data footprint.*

#### 📖┆[Ten years of Building Open Source Standards: From Parquet to Arrow to OpenLineage](https://sympathetic.ink/2024/01/24/Ten-years-of-Building-Open-Source-Standards-From-Parquet-to-Arrow-to-OpenLineage.html)

✍ [Julien Le Dem](https://twitter.com/intent/user?screen_name=J_)

> *Over the last decade, I have been lucky enough to contribute to a few successful open source projects in the data ecosystem. In this post, I will share the story of how these projects came to be and what made their success possible. I will describe the ideation process and early growth of the Apache Parquet columnar format and show how that led to the creation of its in-memory alter-ego Apache Arrow. I will end by showing how this experience enabled the success of OpenLineage, an LF AI & Data project that brings observability to the data ecosystem. Along the way, I will talk about the key elements that catalyzed their growth, from project focus to governance and community.*

#### 📖┆**[Microservices vs. Monolithic Approaches in Data](https://towardsdatascience.com/microservices-vs-monolithic-approaches-in-data-8d9d9a064d06)**

✍ *[Hugo Lu](https://medium.com/@hugolu87)*

> *The Microservice vs. Monolith debate rages in software, but is reduced to a gentle simmer in the data world.*

#### 📖┆[(Almost) Every infrastructure decision I endorse or regret after 4 years running infrastructure at a startup](https://cep.dev/posts/every-infrastructure-decision-i-endorse-or-regret-after-4-years-running-infrastructure-at-a-startup/)

✍ [Jack Lindamood](https://cep.dev/about/)

> *I’ve led infrastructure at a startup for the past 4 years that has had to scale quickly. From the beginning I made some core decisions that the company has had to stick to, for better or worse, these past four years. This post will list some of the major decisions made and if I endorse them for your startup, or if I regret them and advise you to pick something else.*

#### 📖┆[SQL - Cursors and Their Usage in Databases](https://blog.stackademic.com/sql-cursors-and-their-usage-in-databases-681734044773)

✍ [Ihor Lukianov](https://lukianovihor.medium.com/)

> *An introduction to working with the cursor in PostgreSQL and MS SQL Server*

#### 📖┆[Back Market’s journey towards data self-service](https://engineering.backmarket.com/back-markets-journey-towards-data-self-service-89b278d6617a)

✍ [Thibault Latrace](https://medium.com/@thibault.latrace)

> *Like many other scale-ups, Back Market wishes to foster a data-informed culture within the company to make strategic decisions using data. Intuition, gut feeling, and experience shouldn’t be neglected but we believe critical company decisions should be backed up with quantitative facts*

#### 📖┆[Sequential A/B Testing Keeps the World Streaming Netflix](https://netflixtechblog.com/sequential-a-b-testing-keeps-the-world-streaming-netflix-part-1-continuous-data-cba6c7ed49df)

✍ [Netflix Technology Blog](https://netflixtechblog.comhttps//netflixtechblog.medium.com/?source=post_page-----cba6c7ed49df--------------------------------)

> *In this blog post, we will develop a statistical procedure to do just that, and describe the impact of these developments at Netflix. The key idea is to switch from a “fixed time horizon” to an “any-time valid” framing of the problem.*

#### 📖┆[From Silos to Standardization: Leveraging DBT for a Democratized Data Framework](https://medium.com/uc-engineering/from-silos-to-standardization-leveraging-dbt-for-a-democratized-data-framework-f444dcd07cd9)

✍ [UC Blogger](https://medium.com/@ucblogger?source=post_page-----f444dcd07cd9--------------------------------)

> *Urban Company’s growth over the last few years has resulted in an increased volume and reliance on data to fulfill product & business use-cases. Data-driven decisions across teams have played a pivotal role in this journey; but it came with its own set of challenges related to scalability, ownership, discoverability, cost, etc. The main goal of this blog is to dive deep into the issues faced by different teams and our journey towards solving them with a centralized solution known as the Common Computation Framework(CCF).*

#### 📖┆[A dataframe is a bad abstraction](https://medium.com/@cautaerts/a-dataframe-is-a-bad-abstraction-8b2d84fa373f)

✍ [Niels Cautaerts](https://medium.com/@cautaerts?source=post_page-----8b2d84fa373f--------------------------------)

> *Trading away robustness for simplicity can backfire long term*

#### 📖┆[Open Source Data Engineering Landscape 2024](https://alirezasadeghi1.medium.com/open-source-data-engineering-landscape-2024-8a56d23b7fdb)

✍ [Alireza Sadeghi](https://alirezasadeghi1.medium.com/?source=post_page-----8a56d23b7fdb--------------------------------)

> *Having closely followed data engineering trends in my role as a senior data engineer and consultant, I’d like to present the open source data engineering landscape at the beginning of 2024. This includes identifying key active projects and prominent tools, empowering readers to make informed decisions when navigating this dynamic technological landscape.*

#### 📖┆[Building a Data Platform in 2024](https://towardsdatascience.com/building-a-data-platform-in-2024-d63c736cccef)

✍ [Dave Melillo](https://data-dave.medium.com/)

> *How to build a modern, scalable data platform to power your analytics and data science projects (updated)*

#### 📖┆[How a POC became a production-ready Hudi data lakehouse through close team collaboration](https://medium.com/leboncoin-tech-blog/how-a-poc-became-a-production-ready-hudi-data-lakehouse-through-close-team-collaboration-c7f33eb746a8)

✍ [leboncoin tech](https://medium.com/@leboncoin_tech?source=post_page-----c7f33eb746a8--------------------------------)

> *How to build a modern, scalable data platform to power your analytics and data science projects (updated)*

#### 📖┆[Is the "Modern Data Stack" Still a Useful Idea?](https://roundup.getdbt.com/p/is-the-modern-data-stack-still-a)

✍ [Tristan Handy](https://substack.com/profile/1135298-tristan-handy)

> *This article explains how they were able to turn a POC into a production-ready data lakehouse that is now used by 5 teams at Leboncoin and Adevinta (the group that owns the company), thanks to close collaboration between the Data Platform team and the Customer Relationship Management (CRM) Feature team.*

#### 📖┆[The problem was the product](https://benn.substack.com/p/the-problem-was-the-product)

✍ [Benn Stancil](https://substack.com/@benn)

> *How the modern data stack got lost.*

---

# ✏ Data

> *The one thing that this job has taught me is that truth is stranger than fiction. — Predestination (2014)*

#### 📖┆[Why Data is an Incomplete Representation of Reality [Thoughts]](https://artificialintelligencemadesimple.substack.com/p/why-data-is-an-incomplete-representation)

✍ [Devansh](https://substack.com/profile/8101724-devansh)

> *In this article, I want to explore the limitations of data. While data can be an incredibly important tool, there are other kinds of intelligences that aren’t encoded properly into our datasets. Acknowledging this is critical to understanding what Data/AI can and can’t do.*

#### 📖┆[Understanding Data Modelling in Data Mesh](https://piethein.medium.com/understanding-data-modelling-in-data-mesh-bf0dfcfd0583)

✍ [Piethein Strengholt](https://piethein.medium.com/?source=post_page-----bf0dfcfd0583--------------------------------)

> *This article aims to address the intriguing topic of data modelling within the context of a data mesh. Specifically, it will clarify whether enterprise data models persist in a data mesh framework.*

#### 📖┆[Data warehousing essentials: A guide to data warehousing](https://www.theseattledataguy.com/data-warehousing-essentials-a-guide-to-data-warehousing/#page-content)

✍ [Ben Rogojan](https://www.theseattledataguy.com/data-science-consultants/#page-content)

> *Data warehouses and data lakes play a crucial role for many businesses. It gives businesses access to the data from all of their various systems. As well as often integrating data so that end-users can answer business critical questions. But if we take a step back and only focus on the data warehouse, what is it anyway? And why do companies invest so much into data warehouses?*

---

# 🤖 AI┆ML┆Data Science

> *You know, Burke, I don’t know which species is worse. — Ripley, Aliens (1986)*

#### 📖┆[Engineering Practices for LLM Application Development](https://martinfowler.com/articles/engineering-practices-llm.html)

✍ [David Tan](https://www.linkedin.com/in/davified/) + [Jessie Wang](https://www.linkedin.com/in/jessie-sj-wang/)

> *In this article, we'll delve into the project's technical architecture, the challenges we encountered, and the practices that helped us iteratively and rapidly build an LLM-based AI Concierge.*

#### 📖┆[Do large language models understand the world?](https://www.amazon.science/blog/do-large-language-models-understand-the-world)

✍ [Matthew Trager](https://www.amazon.science/author/matthew-trager) + [Stefano Soatto](https://www.amazon.science/author/stefano-soatto)

> *Similarly, today’s critics often argue that since LLMs are able only to process “form” — symbols or words — they cannot in principle achieve understanding. Meaning depends on relations between form (linguistic expressions, or sequences of tokens in a language model) and something external, these critics argue, and models trained only on form learn nothing about those relations. But is that true? In this essay, we will argue that language models not only can but do represent meanings.*

#### 📖┆[How To Explain Gradient Descent to Your Mom: Complete Tutorial](https://pub.towardsai.net/how-to-explain-gradient-descent-to-your-mom-complete-tutorial-e48971410c05)

✍ [Igor Novikov](https://pub.towardsai.nethttps//squirrelfm.medium.com/?source=post_page-----e48971410c05--------------------------------)

> *Gradient descent is at the core of most AI/ML techniques. It sounds strange and kinda scary.*

#### 📖┆[Fixing security vulnerabilities with AI](https://github.blog/2024-02-14-fixing-security-vulnerabilities-with-ai/)

✍ [Tiferet Gazit](https://github.com/tiferet)

> *In November 2023, we announced the launch of code scanning autofix, leveraging AI to suggest fixes for security vulnerabilities in users’ codebases. This post describes how autofix works under the hood, as well as the evaluation framework we use for testing and iteration.*

#### 📖┆[Experiment Faster and with Less Effort](https://doordash.engineering/2024/02/13/experiment-faster-and-with-less-effort/)

✍ [Yicong ("Nicole") Lin](https://www.linkedin.com/in/yicongnicolelin/) + [Yixin Tang](https://www.linkedin.com/in/yixint/)

> *We introduce a new framework that has demonstrated significant improvements in the first two of these dimensions: velocity and toil. Because DoorDash conducts thousands of experiments annually that contribute billions in gross merchandise value, it is critical to our business success that we quickly and accurately test the maximum number of hypotheses possible.*

---

# 🔥 Catch up

> *…Next Saturday night, we're sending you back to the future! — Dr. Emmett Brown, Back to the Future (1985)*

#### 📖┆Google Cloud | Gemini [is in the town](https://cloud.google.com/blog/products/ai-machine-learning/gemini-on-vertex-ai-expands/):

* Creating a [remote model](https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model#remote_service_type) based on the `gemini-pro` Vertex AI large language model (LLM).
* Using the `ML.GENERATE_TEXT` function with a remote model based upon `gemini-pro` to perform generative natural language tasks on text stored in BigQuery tables.
* Use the BigQuery DataFrames `GeminiTextGenerator` class in the `bigframes.ml.llm` module to create estimator-like Gemini text generator models.

#### 📖┆[Column-Level Lineage now available in dbt Cloud](https://docs.getdbt.com/blog/dbt-explorer)

#### 📖┆[DuckDB 0.10.0 release note](https://github.com/duckdb/duckdb/releases)

#### 📖┆[DuckDB now can read data from S3 express one](https://duckdb.org/docs/guides/import/s3_express_one)

---

# 💠 Previously on Dimension

> *Dimension is my sub-newsletter where I note down things I learn from people smarter than me in the data engineering field.*

Here are the 3 latest articles:

### ***Published on 2024, February 3:***

### ***Published on 2024, February 10:***

### ***Published on 2024, February 17:***

Let me here your voice, for example:

'Your newsletter is so terrible, I can't handle it anymore.'

[Leave a comment](https://vutr.substack.com/p/groupby-23-meta-loves-python-how/comments)

---

## “Hasta la vista, baby” -T800, Terminator 2: Judgment Day (1991)

Thanks for scrolling this far! There's a convenient subscribe box here if you want me to annoy you every week. 😄
