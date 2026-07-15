---
title: "GroupBy #18: Uber - GC Tuning for Improved Presto Reliability, How Meta is advancing GenAI"
channel: vutr
author: "Vu Trinh"
published: 2024-01-16
url: https://vutr.substack.com/p/groupby-18-uber-gc-tuning-for-improved
paid: false
topics: ["Data Engineering", "Apache Spark", "Databricks", "Data Modeling", "Streaming", "Data Quality"]
tags: [https, auto, engineering, good, substack, image]
---

# GroupBy #18: Uber - GC Tuning for Improved Presto Reliability, How Meta is advancing GenAI

*Plus: Python 3.13 gets a JIT, Removing data transfer fees when moving off Google Cloud*

> Source: [Open post](https://vutr.substack.com/p/groupby-18-uber-gc-tuning-for-improved)

## Topics

[[data-engineering|Data Engineering]] · [[apache-spark|Apache Spark]] · [[databricks|Databricks]] · [[data-modeling|Data Modeling]] · [[streaming|Streaming]] · [[data-quality|Data Quality]]

---

*This is **GroupBy**, the place where I share with you guys the resources I learn from people smarter than me in data engineer field.*

*Not subscribed yet? Here you go:*

[Subscribe now](https://vutr.substack.com/subscribe?)

![](https://substackcdn.com/image/fetch/$s_!D8N-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fvutr.substack.com%2Fimg%2Fsubstack.png)

Get more from Vu Trinh in the Substack app

Available for iOS and Android

[Get the app](https://substack.com/app/app-store-redirect?utm_campaign=app-marketing&utm_content=author-post-insert&utm_source=vutr)

[![](https://substackcdn.com/image/fetch/$s_!-6_Z!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F63801439-3ec4-47ba-815c-d630c4f3c93e_1300x900.png)](https://substackcdn.com/image/fetch/$s_!-6_Z!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F63801439-3ec4-47ba-815c-d630c4f3c93e_1300x900.png)

I used to spend more than 2 hours creating a landing image for newsletters, but now I just want it to be simple.

---

> *👋 Hi, my name is Vu Trinh, a data engineer.*
>
> *I enjoy reading **good stuff** (related to data and engineering), and this newsletter is my effort on the journey to seek the "good stuff" across the entire Internet.*
>
> *Hope this issue find you well.*

---

# 🥷 Can things be both random and purposeful?

> *My mistakes, thoughts, experiences and lessons learned*

In 2023, more than 10 DE folks DM me asking for help.

(Although I didn't post any career advice content)

I spent a quite amount of time helping them.

(Hope it could really help)

Most of them were having trouble in their first steps on the Data Engineer journey.

"How should I start as a Data Engineer?"

"What skills should I have?"

I saw myself 5 years ago in these questions.

So, I think it would be helpful to share my experience as a Data Engineer publicly…

… to help someone out there struggle a little less on their journey.

> *This is just my sharing. My experience is not enough to give you advice.*

## My 3 biggest mistakes

> *so far as a data engineer*

### **Moving too fast with tools**

* Root cause: The pressure of getting a job or wanting to get things done as fast as possible.
* How I gradually improved:

  + Spend my free time learning the fundamentals: asking "How" questions.
  + Don't just blindly use the tool/technology: asking "Why" questions.

### **Isolating myself in a technical box**

* Root cause: Communication problem between tech and business.
* How I gradually improved:

  + Research company business operations.
  + Put myself in their position.

### **"Data Modeling is not my duty"**

* Root cause: Didn't realize the importance of data modeling.
* How I gradually improved: Learn and practice basic data modeling.

---

# 🎯 Side Project

> *40+ hours of debugging and you still want some more?*

## 📖┆[Frontpage Slickdeals Data Analysis with Pandas and Plotly Express](https://towardsdatascience.com/frontpage-slickdeals-analytics-with-pandas-and-plotly-express-b5e5bbdf072d)

✍ [Chengzhi Zhao](https://chengzhizhao.medium.com/)

> *In this article, we are going to exploring a dataset from Slickdeals and perform data analysis with Pandas and Plotly Express. I hope this article can provide some interesting examples from collecting raw data, as well as some insights on how to use Pandas and Plotly Express to perform data analysis and visualization.*

---

# 🚀 Engineering

> *I have to believe in a world outside my own mind. — Memento (2000)*

## 📖┆**[Uber: GC Tuning for Improved Presto Reliability](https://www.uber.com/en-SG/blog/uber-gc-tuning-for-improved-presto-reliability/)**

[![Image](https://substackcdn.com/image/fetch/$s_!ZmYx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F64a4ac0d-fb52-4149-9ff1-3e905f646842_1306x761.png "Image")](https://substackcdn.com/image/fetch/$s_!ZmYx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F64a4ac0d-fb52-4149-9ff1-3e905f646842_1306x761.png)

[Presto at Uber](https://www.uber.com/en-SG/blog/uber-gc-tuning-for-improved-presto-reliability/)

✍ [Cristian Velazquez, Vineeth Karayil Sekharan](https://www.uber.com/blog/)

> *GC tuning done on Presto is an example of how improving garbage collection can improve a system’s overall performance and reliability.*

## 📖┆[Microsoft Fabric - a better understanding of the underlying architecture and concepts](https://piethein.medium.com/microsoft-fabric-a-better-understanding-of-the-underlying-architecture-and-concepts-847407b2524f)

✍ [Piethein Strengholt](https://piethein.medium.com/?source=post_page-----847407b2524f--------------------------------)

> *In this article we will discuss Microsoft Fabric, look at the main architectural concepts and discuss what concerns at every layer.*

## 📖┆[Rebuilding Netflix Video Processing Pipeline with Microservices](https://netflixtechblog.com/rebuilding-netflix-video-processing-pipeline-with-microservices-4e5e6310e359)

[![](https://substackcdn.com/image/fetch/$s_!b5rl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1229c941-5ea9-45de-9fc7-939a7d3d5932_2000x1148.png)](https://substackcdn.com/image/fetch/$s_!b5rl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1229c941-5ea9-45de-9fc7-939a7d3d5932_2000x1148.png)

[source](https://netflixtechblog.com/rebuilding-netflix-video-processing-pipeline-with-microservices-4e5e6310e359)

✍ [Netflix Technology Blog](https://netflixtechblog.medium.com/)

> *This is the first blog in a multi-part series on how Netflix rebuilt its video processing pipeline with microservices, so we can maintain our rapid pace of innovation and continuously improve the system for member streaming and studio operations.*

## 📖┆**[Sliding window rate limits in distributed systems](https://engineering.grab.com/frequency-capping)**

✍ [Naveen Kumar Jakuva Premkumar](https://engineering.grab.com/authors#naveen-kumar), [Abdullah Al Mamun](https://engineering.grab.com/authors#abdullah-mamun)

> *Like many other companies, Grab uses marketing communications to notify users of promotions or other news. If a user receives these notifications from multiple companies, it would be a form of information overload and they might even start considering these communications as spam. Over time, this could lead to some users revoking their consent to receive marketing communications altogether. Hence, it is important to find a rate-limited solution that sends the right amount of communications to our users.*

## 📖┆[Python 3.13 gets a JIT](https://tonybaloney.github.io/posts/python-gets-a-jit.html)

✍ [Anthony Shaw](https://twitter.com/anthonypjshaw)

> *In late December 2023 (Christmas Day to be precise), CPython core developer Brandt Bucher submitted a little pull-request to the Python 3.13 branch adding a JIT compiler.*

---

# ✏ Data

> *The one thing that this job has taught me is that truth is stranger than fiction. — Predestination (2014)*

## 📖┆[Why Data Quality Is More Important Than Ever in an AI-Driven World](https://dataproducts.substack.com/p/why-data-quality-is-more-important)

✍ [Mikiko Bazeley](https://substack.com/profile/12037315-mikiko-bazeley)

> *Is there really a difference when it comes to delivering incredible experiences and new features with the God-tier models on the market? Isn’t all data “good data” for the purposes of machine learning at this point?*

## 📖┆[Long-Chain Marketing: How Data Engineering & Data Management Create Value For The Business](https://vinvashishta.substack.com/p/long-chain-marketing-how-data-engineering)

✍ [Vin Vashishta](https://substack.com/profile/16324927-vin-vashishta)

> *You'll learn how to transition from data management to knowledge management. I’ll explain why this transformation is essential to meet business needs, like connecting investments in marketing with the returns they create. You’ll learn how to justify the value of curating datasets to the rest of the business.*

## 📖┆[Synthetic Data In A Nutshell](https://www.thdpth.com/p/synthetic-data-in-a-nutshell)

✍ [Sven Balnojan](https://substack.com/profile/229923-sven-balnojan)

> *Synthetic data is…. fake. That’s it. It's made-up stuff, not worth a penny. And yet, it looks like this is when synthetic data is at the breach of going from “theoretically useful” to practical reality.*

## 📖┆[Metadata Management Challenges](https://www.dbta.com/Columns/DBA-Corner/Metadata-Management-Challenges-162115.aspx)

✍ [Craig S. Mullins](https://www.dbta.com/Authors/Craig-S.-Mullins-3535.aspx)

> *Is there really a difference when it comes to delivering incredible experiences and new features with the God-tier models on the market? Isn’t all data “good data” for the purposes of machine learning at this point?*

---

# 🤖 AI┆ML┆Data Science

> *You know, Burke, I don’t know which species is worse. — Ripley, Aliens (1986)*

## 🎙️┆[How Meta is advancing GenAI](https://engineering.fb.com/2024/01/11/ml-applications/meta-advancing-genai/)

🎤 [Pascal Hartig](https://engineering.fb.com/author/pascal-hartig/)

> *What's going on with generative AI (GenAI) at Meta? And what does the future have in store?*

## 📖┆[What we do on the data science team](https://medium.com/agoda-engineering/what-we-do-on-the-data-science-team-ba2bbb218728)

✍ [Agoda Engineering](https://medium.com/@agoda.eng?source=post_page-----ba2bbb218728--------------------------------)

> *Data science stands at the heart of Agoda's operational strategy, transforming complex data into actionable insights. It’s a key player in our pursuit of technological advancement and business efficiency. In this blog, our data science manager, Aviel Makmal, shares insights into his role as a data science manager.*

---

# 🔥 Catch up

> *…Next Saturday night, we're sending you back to the future! — Dr. Emmett Brown, Back to the Future (1985)*

**📖┆[Google Cloud | Document AI Custom Extractor, powered by gen AI, is now GA](https://cloud.google.com/blog/products/ai-machine-learning/document-ai-custom-extractor-powered-by-generative-ai-is-now-ga)**

**📖┆[Google Cloud | Removing data transfer fees when moving off Google Cloud](https://cloud.google.com/blog/products/networking/eliminating-data-transfer-fees-when-migrating-off-google-cloud)**

**📖┆[Databricks | Announcing Ray Autoscaling support on Databricks and Apache Spark™](https://www.databricks.com/blog/announcing-ray-autoscaling-support-databricks-and-apache-sparktm)**

---

# ⚡Tech news

> *Tech in general*

💥 **[Google Cuts Hundreds of Jobs in Engineering and Other Divisions](https://www.nytimes.com/2024/01/11/technology/google-layoffs.html) - The New York Times**

💥 **[Amazon’s Twitch to Cut 500 Employees, About 35% of Staff](https://www.bloomberg.com/news/articles/2024-01-09/amazon-s-twitch-to-cut-500-employees-about-35-of-staff) - Bloomberg**

💥 **[Discord is laying off 17 percent of employees](https://www.theverge.com/2024/1/11/24034705/discord-layoffs-17-percent-employees) - The Verge**

Let me here your voice, for example:

'Your newsletter is so terrible, I can't handle it anymore.'

[Leave a comment](https://vutr.substack.com/p/groupby-18-uber-gc-tuning-for-improved/comments)

---

# “Hasta la vista, baby”

# -T800, Terminator 2: Judgment Day (1991)

Thanks for scrolling this far! There's a convenient subscribe box here if you want me to annoy you every week. 😄
