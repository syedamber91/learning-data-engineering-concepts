---
title: "GroupBy #24: Enabling near real-time data analytics on the data lake at Grab, Aligning Velox and Apache Arrow at Meta."
channel: vutr
author: "Vu Trinh"
published: 2024-02-27
url: https://vutr.substack.com/p/groupby-24-enabling-near-real-time
paid: false
topics: ["Data Engineering", "Apache Spark", "Data Lake"]
tags: [https, engineering, substack, blog, medium, apache]
---

# GroupBy #24: Enabling near real-time data analytics on the data lake at Grab, Aligning Velox and Apache Arrow at Meta.

*Plus: Leveraging Spark 3 and NVIDIA’s GPUs to Reduce Cloud Cost at Paypal, You Inherited a Failed Data Project. What Do You Do?*

> Source: [Open post](https://vutr.substack.com/p/groupby-24-enabling-near-real-time)

## Topics

[[data-engineering|Data Engineering]] · [[apache-spark|Apache Spark]] · [[data-lake|Data Lake]]

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

[![](https://substackcdn.com/image/fetch/$s_!y8z6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd00c2b0b-1ef7-4bf8-99e8-dd2c2a077678_1400x1000.png)](https://substackcdn.com/image/fetch/$s_!y8z6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd00c2b0b-1ef7-4bf8-99e8-dd2c2a077678_1400x1000.png)

---

# 📈 Career

> *Don't let comfort hold you back.*

#### 📖┆[A Hallmark of a ML Practitioner](https://koopingshung.substack.com/p/a-hallmark-of-a-ml-practitioner)

✍ [Koo Ping Shung](https://substack.com/profile/7906875-koo-ping-shung)

> *As we move along in the Knowledge Economy, knowledge, skills and experience will become more important as they provide the fuel for the company to move forward with new ideas and innovations. It is the reason why I constantly ponder on the questions, “How can we measure skills, proficiency, and competencies?” Or “What makes someone a practitioner and not a paper theorist?”*

---

# 🚀 Engineering

> *I have to believe in a world outside my own mind. — Memento (2000)*

#### 📖┆[Unit Testing for Data Engineers](https://dataengineeringcentral.substack.com/p/unit-testing-for-data-engineers-43b?ref=blef.fr)

✍ [Daniel Beach](https://substack.com/profile/21715962-daniel-beach)

> *Maybe you've gone your entire career without writing a single test, or you're in a place that writes them but you can't quite figure out what value they bring. Maybe you simply don’t like them.*

#### 📖┆[HOW DISCORD MOVED ENGINEERING TO CLOUD DEVELOPMENT ENVIRONMENTS](https://discord.com/blog/how-discord-moved-engineering-to-cloud-development-environments)

✍ [Denbeigh Stevens](https://www.linkedin.com/in/denbeigh-stevens/)

> *This blog post focuses on how we transitioned all backend and infrastructure development to a Linux-based Cloud Development Environment, thanks to the team over at Coder.*

#### 📖┆[Enabling near real-time data analytics on the data lake](https://engineering.grab.com/enabling-near-realtime-data-analytics)

✍ [Shi Kai Ng](https://engineering.grab.com/authors#shikai-ng) + [Shuguang Xiang](https://engineering.grab.com/authors#shuguang-xiang)

> *The introduction of the Hudi format, which supports fast writes by allowing Avro and Parquet files to co-exist on a Merge On Read (MOR) table, opens up the possibility of having a data lake with minimal data latency. The concept of a commit timeline further allows data to be served with Atomicity, Consistency, Isolation, and Durability (ACID) guarantees.*

#### 📖┆[Governance as Code: An Innovative Approach to Software Architecture Verification](https://medium.com/agoda-engineering/governance-as-code-an-innovative-approach-to-software-architecture-verification-d93f95443662)

✍ [Agoda Engineering](https://medium.com/@agoda.eng?source=post_page-----d93f95443662--------------------------------)

> *Governance as Code (GaC) technology is an innovative technology in software architecture that enables automatic verification of a software system’s architectural consistency. In this article, we will delve into the details of this technology and its implementation and encourage you to consider how it could be applied, at least in part, within your organization.*

#### 📖┆[Leveraging Spark 3 and NVIDIA’s GPUs to Reduce Cloud Cost by up to 70% for Big Data Pipelines](https://medium.com/paypal-tech/leveraging-spark-3-and-nvidias-gpus-to-reduce-cloud-cost-by-up-to-70-for-big-data-pipelines-e0bc02ec4f88)

✍ [Ilay Chen](https://medium.com/@ilaychen5?source=post_page-----e0bc02ec4f88--------------------------------)

> *At PayPal, hundreds of thousands of Apache Spark jobs run on an hourly basis, processing petabytes of data and requiring a high volume of resources. To handle the growth of machine learning solutions, PayPal requires scalable environments, cost awareness and constant innovation. This blog explains how Apache Spark 3 and GPUs can help enterprises potentially reduce Apache Spark’s jobs cloud costs by up to 70% for big data processing and AI applications.*

#### 📖┆[Aligning Velox and Apache Arrow: Towards composable data management](https://engineering.fb.com/2024/02/20/developer-tools/velox-apache-arrow-15-composable-data-management/)

✍ [Pedro Pedreira](https://engineering.fb.com/author/pedro-pedreira/)

> *We’ve partnered with Voltron Data and the Arrow community to align and converge Apache Arrow with Velox, Meta’s open source execution engine.*

#### 📖┆[Why Apache Spark RDD is immutable?](https://luminousmen.com/post/why-apache-spark-rdd-is-immutable)

✍ [Kirill Bobrov](https://www.linkedin.com/in/luminousmen/)

> *Every now and then, when I find myself on the interviewing side of the table, I like to toss in a question about Apache Spark’s RDD and its immutable nature. It’s a simple question, but the answers can reveal a deep understanding — or lack thereof — of distributed data processing principles.*

#### 📖┆[Let's build a distributed Postgres proof of concept](https://notes.eatonphil.com/distributed-postgres.html)

✍ [Phil Eaton](https://twitter.com/eatonphil)

> *By the end of this post, in around 600 lines of code, we'll have a distributed "Postgres implementation" that will accept writes (CREATE TABLE, INSERT) on the leader and accept reads (SELECT) on any node. All nodes will contain the same data.*

#### 📖┆[Coming of age in the fifth epoch of distributed computing, accelerated by machine learning](https://cloud.google.com/blog/topics/systems/the-fifth-epoch-of-distributed-computing/)

✍ [Amin Vahdat](https://www.linkedin.com/in/vahdat/)

> *A look back on the brief history of computing suggests that we have worked through four such major transitions, each defining an ‘epoch’ of computing. We offer a historical taxonomy that points to a manifest need to define and to drive a fifth epoch of computing, one that is data-centric, declarative, outcome-oriented, software-defined, and centered on proactively bringing insights to people.*

#### 📖┆[The journey of building a comprehensive attribution platform](https://engineering.grab.com/attribution-platform)

✍ [Kang Huang](https://engineering.grab.com/authors#kang-huang) + [Suvi Murugan](https://engineering.grab.com/authors#suvi-murugan) + [Sharathbabu Siddaramappa](https://engineering.grab.com/authors#sharathbabu-s)

> *In this blog, we delve into the technical intricacies, software architecture, challenges, and solutions involved in crafting a state-of-the-art engineering solution for the attribution platform.*

#### 📖┆[Designing serverless stream storage](https://blog.schmizz.net/designing-serverless-stream-storage)

✍ [Shikhar Bhushan](https://hashnode.com/@shikhrr)

> *I have alluded to "hypothetical S2" (Stream Store), a true counterpart to S3 for data in motion. As I work on making S2 real, I wanted to share the design and how it shaped up.*

---

# ✏ Data

> *The one thing that this job has taught me is that truth is stranger than fiction. — Predestination (2014)*

#### 📖┆[You Inherited a Failed Data Project. What Do You Do?](https://joereis.substack.com/p/you-inherited-a-failed-data-project)

✍ [Joe Reis](https://substack.com/profile/3531217-joe-reis)

> *What do you do if you’re dropped into the middle of a failed data project? Here’s what I would do (and I’m sure Gordon would have similar advice).*

#### 📖┆[Breaking Down the Modern Data Stack: Practical Insights for Leveraging Analytics Progress](https://www.thdpth.com/p/modern-data-stack-in-a-nutshell-a)

✍ [Sven Balnojan](https://substack.com/profile/229923-sven-balnojan)

> *How can each of us profit from the progress in analytics? How can you make the most of the advances the modern data stack brings?*

#### 📖┆[Data will not tell you what to do](https://mikkeldengsoe.substack.com/p/data-will-not-tell-you-what-to-do)

✍ [Mikkel Dengsøe](https://substack.com/profile/6080775-mikkel-dengse)

> *Data may give you a conclusive answer that changing the color of a button from yellow to green increases the conversion rate by 0.15ppts but will tell you nothing about the other ideas that would have had ten times more impact.*

#### 📖┆[Do Not Create That New Report!](https://pub.towardsai.net/do-not-create-that-new-report-ceaa26fc0ed5)

✍ [Deepak Chopra | Talking Data Science](https://medium.com/@deepakchopra2911)

> *Embracing a focused reporting approach in the data-driven era to overcome the pitfalls of excessive reporting and enable efficient and effective decision-making.*

#### 📖┆[Data ownership: A practical guide](https://medium.com/@mikldd/data-ownership-a-practical-guide-ae306d49866f)

✍ [Mikkel Dengsøe](https://medium.com/@mikldd)

> *A toolkit for defining and activating ownership across the data team, upstream teams, and business stakeholders.*

---

# 🤖 AI┆ML┆Data Science

> *You know, Burke, I don’t know which species is worse. — Ripley, Aliens (1986)*

#### 📖┆[LLMs shouldn’t write SQL](https://benn.substack.com/p/llms-shouldnt-write-sql)

✍ [Benn Stancil](https://substack.com/@benn)

> *There's no direct path from a business question to a useful query.*

#### 📖┆[What is LLMOps? Key Components & Differences to MLOPs](https://lakefs.io/blog/llmops/)

✍ [The lakeFS Team](https://www.linkedin.com/company/lakefs-treeverse/)

> *Keep reading to learn what LLMOps is all about, see how it differs from MLOps, and learn a few best practices for the smooth delivery of an LLM-powered app.*

#### 📖┆[Unlocking AI Assisted Development Safely: From Idea to GA](https://medium.com/pinterest-engineering/unlocking-ai-assisted-development-safely-from-idea-to-ga-4d68679161ef)

✍ [Pinterest Engineering](https://medium.com/@Pinterest_Engineering?source=post_page-----4d68679161ef--------------------------------)

> *At Pinterest we are continuously looking for ways to improve our developer experience, and we have recently shipped AI-assisted development for everyone while balancing safety, security, and cost. In this blog post, we share our journey of unlocking AI-assisted development, from the initial idea to the General Availability (GA) stage. Join us as we delve into the opportunities, challenges, and successes we encountered along the way.*

#### 📖┆[How AI code generation works](https://github.blog/2024-02-22-how-ai-code-generation-works/)

✍ [Jeimy Ruiz](https://github.com/ruizjeimy)

> *In this post, we’ll dive into the inner workings of AI code generation, exploring how it functions, its capabilities and benefits, and how developers can use it to enhance their development experience while propelling your enterprise forward in today’s competitive landscape.*

#### 📖┆[Building a Large-Scale Recommendation System: People You May Know](https://www.linkedin.com/blog/engineering/recommendations/building-a-large-scale-recommendation-system-people-you-may-know?utm_source=substack&utm_medium=email)

✍ [Parag Agrawal](https://www.linkedin.com/in/paragagrawalcmu)

> *In this blog, we cover how we built our large-scale recommendation system and scaled its scoring mechanism over the last two years to handle more than a billion items while still ensuring high relevance and low serving latency in the recommendations shared with members.*

#### 📖┆[How Good is Google Gemini 1.5 With a Massive 1 Million Context Window?](https://pub.towardsai.net/how-good-is-google-gemini-1-5-with-a-massive-1-million-context-window-b386d285845d)

✍ [Dipanjan (DJ) Sarkar](https://djsarkar.medium.com/)

> *Taking Google’s new Large Language Model on a test drive!*

#### 📖┆[Building an LLM from scratch](https://bclarkson-code.github.io/posts/llm-from-scratch-scalar-autograd/post.html)

✍ [Ben Clarkson](https://bclarkson-code.github.io/about.html)

> *I’m building a modern language model with all the bells and whistles completely from scratch: from vanilla python to functional coding assistant. Borrowing (shamelessly stealing) from computer games, I’ve built a tech tree of everything that I think I’ll need to implement to get a fully functional language model.*

#### 📖┆[Open Sourcing FlyteInteractive: Saving thousands of AI engineering hours in developing ML interactively](https://www.linkedin.com/blog/engineering/open-source/open-sourcing-flyteinteractive)

✍ [Byron (Pin-Lun) Hsu](https://www.linkedin.com/in/byronhsu1230/overlay/about-this-profile/)

> *When we recognized existing inefficiencies in the current development platform, we took steps towards ensuring that we could fulfill our ambitious goals. As part of this effort to improve machine learning (ML) developer productivity at LinkedIn, we developed FlyteInteractive.*

---

# 💠 Previously on Dimension

> *Dimension is my sub-newsletter where I note down things I learn from people smarter than me in the data engineering field.*

Here are the 3 latest articles:

### ***Published on 2024, February 10:***

### ***Published on 2024, February 17:***

### ***Published on 2024, February 24:***

Let me here your voice, for example:

'Your newsletter is so terrible, I can't handle it anymore.'

[Leave a comment](https://vutr.substack.com/p/groupby-24-enabling-near-real-time/comments)

---

## “Hasta la vista, baby” -T800, Terminator 2: Judgment Day (1991)

Thanks for scrolling this far! There's a convenient subscribe box here if you want me to annoy you every week. 😄
