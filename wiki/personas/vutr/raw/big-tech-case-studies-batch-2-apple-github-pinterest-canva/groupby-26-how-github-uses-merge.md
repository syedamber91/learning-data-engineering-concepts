---
title: "GroupBy #26: How GitHub uses merge queue to ship hundreds of changes every day, Data governance in the age of generative AI, \"Good Enough\" Data Models"
channel: vutr
author: "Vu Trinh"
published: 2024-03-12
url: https://vutr.substack.com/p/groupby-26-how-github-uses-merge
paid: false
topics: ["Data Engineering", "dbt", "Apache Spark", "Databricks", "BigQuery", "Data Modeling", "Data Quality", "Data Governance"]
tags: [https, blog, substack, engineering, github, good]
---

# GroupBy #26: How GitHub uses merge queue to ship hundreds of changes every day, Data governance in the age of generative AI, "Good Enough" Data Models

*Plus: Why the 100x analyst doesn’t exist, What Is Trustworthy AI?*

> Source: [Open post](https://vutr.substack.com/p/groupby-26-how-github-uses-merge)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-spark|Apache Spark]] · [[databricks|Databricks]] · [[bigquery|BigQuery]] · [[data-modeling|Data Modeling]] · [[data-quality|Data Quality]] · [[data-governance|Data Governance]]

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

[![](https://substackcdn.com/image/fetch/$s_!urFD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3ed9e59a-5fd0-440f-b495-f66e7da380de_1400x1000.png)](https://substackcdn.com/image/fetch/$s_!urFD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3ed9e59a-5fd0-440f-b495-f66e7da380de_1400x1000.png)

---

# 📈 Career

> *Don't let comfort hold you back.*

#### 📖┆[Hard and soft skills for developers coding in the age of AI](https://github.blog/2024-03-07-hard-and-soft-skills-for-developers-coding-in-the-age-of-ai/)

✍ [Sara Verdi](https://github.blog/author/saraverdi/)

> *While AI revolutionizes software development, it still relies on developers to pilot its use. In this blog, we’ll cover the skills that developers need to have for navigating this new AI-powered coding frontier.*

#### 📖┆[The Best Piece of Software Engineering Advice - Confessions of a Data Guy](https://www.confessionsofadataguy.com/the-best-piece-of-software-engineering-advice/)

✍ [Daniel Beach](https://github.com/danielbeach)

> *You don’t need to be the smartest person in the room. In fact, you shouldn’t be.*

#### 📖┆[Why the 100x analyst doesn’t exist](https://mikkeldengsoe.substack.com/p/the-100x-analyst)

✍ [Mikkel Dengsøe](https://substack.com/profile/6080775-mikkel-dengse)

> *Much has been written about the 10x – heck, 100x – engineer. The mystical creature that ships features in hours instead of months and perseveres where others back down. Corny as it may sound, I think it’s a pretty good representation of how the world works. But does the 10x analyst exist? I believe so. How about the 100x analyst? I’m not sure.*

#### 📖┆[How to Build a Modern Data Team? Seven tips for success](https://medium.com/everestengineering/how-to-build-a-modern-data-team-seven-tips-for-success-a4d97e427d45)

✍ [Martin Chesbrough](https://medium.com/@martin.chesbrough?source=post_page-----a4d97e427d45--------------------------------)

> *I spend my time with clients of Everest Engineering to help them build data platforms, data products and data teams. Learning from them let me share the 7 things that I think are important.*

---

# 🚀 Engineering

> *I have to believe in a world outside my own mind. — Memento (2000)*

#### 📖┆[Load Balancing: Handling Heterogeneous Hardware](https://www.uber.com/en-SG/blog/load-balancing-handling-heterogeneous-hardware/)

✍ [Uber Engineering Blog](https://www.uber.com/en-SG/blog/engineering/?uclick_id=15b6739c-0acd-406e-bdf6-884992beefa0)

> *This blog post describes Uber’s journey towards utilizing hardware efficiently via better load balancing. The work described here lasted over a year, involved engineers across multiple teams, and delivered significant efficiency savings. The article covers the technical solutions and our discovery process to get to them–in many ways, the journey was harder than the destination.*

#### 📖┆[PERF IS NOT ENOUGH](https://motherduck.com/blog/perf-is-not-enough/)

✍ [Jordan Tigani](https://motherduck.com/authors/jordan-tigani/)

> *Performance in general, and general-purpose benchmarking in particular, is a poor way to choose a database. You’re better off making decisions based on ease of use, ecosystem, velocity of updates, or how well it integrates with your workflow. At best, performance is a point-in-time view of the time it will take to complete certain tasks; at worst, however, it leads you to optimize for the wrong things.*

#### 📖┆[What if we rotate pairs every day?](https://martinfowler.com/articles/rotate-pairs-experiment.html)

✍ [Gabriel Robaina](https://www.linkedin.com/in/gabriel-robaina/) + Kieran Murphy

> *We developed a lightweight methodology to help teams reflect on the benefits and challenges of pairing and how to solve them. Initial fears were overcome and teams discovered the benefits of frequently rotating pairs. We learned that pair swapping frequently greatly enhances the benefits of pairing. Here we share the methodology we developed, our observations, and some common fears and insight shared by the participating team members.*

#### 📖┆[Keeping repository maintainer information accurate](https://github.blog/2024-03-04-keeping-repository-maintainer-information-accurate/)

✍ [Zack Koppert](https://github.blog/author/zkoppert/)

> *Discover how keeping repository maintainer information accurate through CODEOWNERS files and automating maintenance with tools like cleanowners fosters efficient collaboration and sustainable software projects.*

#### 📖┆[Simplify PySpark testing with DataFrame equality functions](https://www.databricks.com/blog/simplify-pyspark-testing-dataframe-equality-functions)

✍ [Haejoon Lee](https://www.databricks.com/blog/author/haejoon-lee) + [Allison Wang](https://www.databricks.com/blog/author/allison-wang) + [Amanda Liu](https://www.databricks.com/blog/author/amanda-liu)

> *Introducing PySpark DataFrame equality test functions: a new set of test functions in Apache Spark. Discover how easy it is to validate data transformations with the new functions through hands-on examples.*

#### 📖┆[How GitHub uses merge queue to ship hundreds of changes every day](https://github.blog/2024-03-06-how-github-uses-merge-queue-to-ship-hundreds-of-changes-every-day/)

✍ [Will Smythe](https://github.blog/author/willsmythe/) + [Lawrence Gripper](https://github.blog/author/lawrencegripper/)

> *Here's how merge queue transformed the way GitHub deploys changes to production at scale, so you can do the same for your organization.*

#### 📖┆[Python Upgrade Playbook](https://eng.lyft.com/python-upgrade-playbook-1479145d52f4)

✍ [Aneesh Agrawal](https://medium.com/@aneeshusa)

> *In this post, we’ll cover how Lyft upgrades Python at scale — 1500+ repos spanning 150+ teams — and the latest iteration of the tools and strategy we’ve built to optimize both the overall time to upgrade and the work required from our engineers. We’ve successfully used (and evolved) this playbook over multiple upgrades, from Python 2 to Python 3.10 and hope you find it useful!*

#### 📖┆[Building Scalable, Real-Time Chat to Improve Customer Experience](https://www.uber.com/en-SG/blog/building-scalable-real-time-chat/?uclick_id=15b6739c-0acd-406e-bdf6-884992beefa0)

✍ [Uber Engineering Blog](https://www.uber.com/en-SG/blog/engineering/?uclick_id=15b6739c-0acd-406e-bdf6-884992beefa0)

> *With millions of support interactions (known internally as contacts) being raised by Uber customers every week, our goal is to resolve these contacts within a predefined service level agreement (SLA). Contacts created by customers are resolved either via automation or with help from a customer support agent.*

#### 📖┆[The 14 pains of building your own billing system](https://arnon.dk/the-14-pains-of-billing/?utm_source=newsletter.programmingdigest.net&utm_medium=referral&utm_campaign=pains-of-building-your-own-billing-system)

✍ [Arnon Shimoni](https://www.linkedin.com/in/arnon-shimoni/)

> *I’ve seen them likened to an octopus, and I fully agree. They touch finance, product, experience, customer support, customers, legal, compliance, sales, and sometimes more.*

---

# ✏ Data

> *The one thing that this job has taught me is that truth is stranger than fiction. — Predestination (2014)*

#### 📖┆["Good Enough" Data Models](https://practicaldatamodeling.substack.com/p/good-enough-data-models)

✍ [Joe Reis](https://substack.com/@joereis)

> *Data modeling along the spectrum of perfect vs "good enough"*

#### 📖┆[The Root Cause of All Problems in Data - Revisited](https://sqlpatterns.com/p/the-root-cause-of-all-problems-in)

✍ [Ergest Xheblati](https://substack.com/@ergestx)

> *What about a people and process problem? What does that mean? Does it have to do with people’s unwillingness to adopt data driven decisions or do we lack a good methodology for being data driven?*

#### 📖┆[Data Quality within Lakehouses](https://piethein.medium.com/data-quality-within-lakehouses-0c9417ce0487)

✍ [Piethein Strengholt](https://piethein.medium.com/?source=post_page-----0c9417ce0487--------------------------------)

> *A deep dive into data quality using bronze, silver, and gold layered architectures.*

#### 📖┆[How to measure a data platform?](https://substack.timodechau.com/p/how-to-measure-a-data-platform)

✍ [Timo Dechau](https://substack.com/profile/29441309-timo-dechau)

> *Product analytics for data products*

#### 📖┆[dbt’s Model Groups & Access for Dummies](https://faithfacts.substack.com/p/dbts-model-groups-and-access-for)

✍ [Faith Lierheimer](https://substack.com/profile/11412853-faith-lierheimer)

> *Welcome to another edition of “Faith takes you on the ride while she learns how to do her job.” Today, we learn about a handful of dbt’s model governance features.*

#### 📖┆[Making friends with the truth](https://roundup.getdbt.com/p/making-friends-with-the-truth)

✍ [Jason Ganz](https://substack.com/profile/73769889-jason-ganz)

> *So how can we become data driven?*

---

# 🤖 AI┆ML┆Data Science

> *You know, Burke, I don’t know which species is worse. — Ripley, Aliens (1986)*

#### 📖┆[Supporting Diverse ML Systems at Netflix](https://netflixtechblog.com/supporting-diverse-ml-systems-at-netflix-2d2e6b6d205d)

✍ [Netflix Technology Blog](https://netflixtechblog.medium.com/?source=post_page-----2d2e6b6d205d--------------------------------)

> *In this article, we cover a few key integrations that we provide for various layers of the Metaflow stack at Netflix, as illustrated above. We will also showcase real-life ML projects that rely on them, to give an idea of the breadth of projects we support. Note that all projects leverage multiple integrations, but we highlight them in the context of the integration that they use most prominently. Importantly, all the use cases were engineered by practitioners themselves.*

#### 📖┆[The Inevitability of AI in Every Facet of Your Business: 11 Deep Thoughts With Lasting Impact](https://www.thdpth.com/p/the-inevitability-of-ai-in-every)

✍ [Sven Balnojan PhD](https://substack.com/profile/229923-sven-balnojan-phd)

> *I want to share a collection of thoughts, quote from leaders in data & AI, and a few thoughts I have on them, to get you thinking. I have no clear answer to any of the questions they raise, and I keep coming back to them, revising my opinion over time.*

#### 📖┆[Risk-Aware Product Decisions in A/B Tests with Multiple Metrics](https://engineering.atspotify.com/2024/03/risk-aware-product-decisions-in-a-b-tests-with-multiple-metrics/)

✍ [Mårten Schultzberg](https://www.linkedin.com/in/m%C3%A5rtenschultzberg/) + [Sebastian Ankargren](https://www.linkedin.com/in/sebastianankargren/) + [Mattias Frånberg](https://www.linkedin.com/in/mattias-fr%C3%A5nberg-6b631432/)

> *We summarize the findings in our recent paper, Schultzberg, Ankargren, and Frånberg (2024), where we explain how Spotify’s decision-making engine works and how the results of multiple metrics in an A/B test are combined into a single product decision.*

#### 📖┆[User Action Sequence Modeling for Pinterest Ads Engagement Modeling](https://medium.com/pinterest-engineering/user-action-sequence-modeling-for-pinterest-ads-engagement-modeling-21139cab8f4e)

✍ [Pinterest Engineering](https://medium.com/@Pinterest_Engineering?source=post_page-----21139cab8f4e--------------------------------)

> *In this blog post, we will mainly discuss how we adopt the user sequence features and the followup optimization:-Designed the sequence features-Leveraged Transformer for sequence modeling- Improved the serving efficiency by half precision inference. We will also share how to improve the model stability by Resilient Batch Norm.*

#### 📖┆[Think Vs Compute (Part 2)](https://koopingshung.substack.com/p/think-vs-compute-part-2)

✍ [Koo Ping Shung](https://substack.com/profile/7906875-koo-ping-shung)

> *So in this issue, this is a refinement further on what is thinking vs compute over here, or at least the differences between humans and machines. Hopefully by understanding the current differences I can work on how to incorporate them together, moving towards the vision of machine+human.*

#### 📖┆[Evolving from Rule-based Classifier: Machine Learning Powered Auto Remediation in Netflix Data Platform](https://netflixtechblog.com/evolving-from-rule-based-classifier-machine-learning-powered-auto-remediation-in-netflix-data-039d5efd115b)

✍ [Netflix Technology Blog](https://netflixtechblog.comhttps//netflixtechblog.medium.com/?source=post_page-----039d5efd115b--------------------------------)

> *This is the first of the series of our work at Netflix on leveraging data insights and Machine Learning (ML) to improve the operational automation around the performance and cost efficiency of big data jobs.*

#### 📖┆[What Is Trustworthy AI?](https://blogs.nvidia.com/blog/what-is-trustworthy-ai/)

✍ [Nikki Pope](https://blogs.nvidia.com/blog/author/nikkipope/)

> *Trustworthy AI is an approach to AI development that prioritizes safety and transparency for the people who interact with it.*

#### 📖┆[Data governance in the age of generative AI](https://aws.amazon.com/blogs/big-data/data-governance-in-the-age-of-generative-ai/)

✍ [Krishna Rupanagunta](https://www.linkedin.com/in/krishna-rupanagunta/) + [Raghvender Arni](https://www.linkedin.com/in/rarni/) + [Imtiaz Sayed](https://www.linkedin.com/in/contacttaz/)

> *In this post, we discuss the data governance needs of generative AI application data pipelines, a critical building block to govern data used by LLMs to improve the accuracy and relevance of their responses to user prompts in a safe, secure, and transparent manner. Enterprises are doing this by using proprietary data with approaches like Retrieval Augmented Generation (RAG), fine-tuning, and continued pre-training with foundation models.*

---

# 🔥 Catch up

> *…Next Saturday night, we're sending you back to the future! — Dr. Emmett Brown, Back to the Future (1985)*

#### 📖┆BigQuery┆The [INFORMATION\_SCHEMA.WRITE\_API\_TIMELINE\*](https://cloud.google.com/bigquery/docs/information-schema-write-api) **views, containing per minute aggregated BigQuery Storage Write API ingestion statistics, are GA.**

#### 📖┆BigQuery[Duet AI in BigQuery](https://cloud.google.com/bigquery/docs/write-sql-duet-ai#generate_python_code) can now assist with Python code generation and code completion.

---

# 💠 Previously on Dimension

> *Dimension is my sub-newsletter where I note down things I learn from people smarter than me in the data engineering field.*

Here are the 3 latest articles:

### ***Published on 2024, February 24:***

### ***Published on 2024, March 2:***

### ***Published on 2024, March 9:***

Let me here your voice, for example:

'Your newsletter is so terrible, I can't handle it anymore.'

[Leave a comment](https://vutr.substack.com/p/groupby-26-how-github-uses-merge/comments)

---

## “Hasta la vista, baby” -T800, Terminator 2: Judgment Day (1991)

Thanks for scrolling this far! There's a convenient subscribe box here if you want me to annoy you every week. 😄
