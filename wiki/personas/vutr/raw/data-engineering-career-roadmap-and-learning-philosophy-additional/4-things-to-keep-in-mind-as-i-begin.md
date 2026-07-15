---
title: "4 Things To Keep In Mind As I Begin The Data Engineering Journey Again"
channel: vutr
author: "Vu Trinh"
published: 2025-06-03
url: https://vutr.substack.com/p/4-things-to-keep-in-mind-as-i-begin
paid: true
topics: ["Data Engineering", "Apache Spark", "Apache Flink", "Snowflake", "Databricks", "BigQuery", "Data Modeling", "Lakehouse"]
tags: [https, auto, good, substackcdn, image, fetch]
---

# 4 Things To Keep In Mind As I Begin The Data Engineering Journey Again

*To break into the field quickly and grow more efficiently.*

> Source: [Open post](https://vutr.substack.com/p/4-things-to-keep-in-mind-as-i-begin)

## Topics

[[data-engineering|Data Engineering]] · [[apache-spark|Apache Spark]] · [[apache-flink|Apache Flink]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[bigquery|BigQuery]] · [[data-modeling|Data Modeling]] · [[lakehouse|Lakehouse]]

---

> *My ultimate goal is to help you break into the data engineering field and become a more impactful data engineer. To take this a step further and dedicate even more time to creating in-depth, practical content, I’m excited to introduce a paid membership option.*
>
> *This will allow me to produce even higher-quality articles, diving deeper into the topics that matter most for your growth and making this whole endeavor more sustainable.*
>
> *I’m offering a limited-time 50% discount on the annual plan to celebrate this new milestone.*
>
> [Upgrade subscription](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!ZxnO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff57a73a6-160b-49f6-b6db-c144c7f17f51_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!ZxnO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff57a73a6-160b-49f6-b6db-c144c7f17f51_2000x1429.png)

---

## Intro

I started sharing what I’ve learned about data engineering two years ago. Fortunately, many of you have supported me. I have exposed my ideas to thousands of readers, learned from talented people, and, luckily, some folks have reached out to me for help.

“How would I enter the field? “

“How would I learn to become a data engineer? “

During the conversations, I realized I was in the same situation as they were. I started the journey at zero with a non-CS background. I’ve gone through the journey with many mistakes and lessons.

Sometimes, I wish I could know something sooner.

I thought it would be a good idea to share these things with all of you.

---

## #1 Aware of the data engineer’s responsibilities

It was the first day of my first data job in 2019.

I met the team’s members, arranged a place to sit, and got a laptop to code on. Then, I was assigned to hand over a Docker deployment of a POC. Back then, I didn’t even know what Docker and POC meant.

[![](https://substackcdn.com/image/fetch/$s_!HXkr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b1efd2f-2ba1-48a1-91dc-187a7c0c11b1_644x238.png)](https://substackcdn.com/image/fetch/$s_!HXkr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0b1efd2f-2ba1-48a1-91dc-187a7c0c11b1_644x238.png)

Turns out it was a POC of a simple “data” project with a few Docker containers that run HDFS, Spark, and Elasticsearch. I spent days to learn the Docker concept (why don’t just use the VM) and how to run those containers.

Like a robot, I didn’t care why I needed to do this; if those containers are up and running, I’m happy.

[![](https://substackcdn.com/image/fetch/$s_!CgRT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F22d34b42-1b1d-4290-99e3-1dfc1ab0e5e6_662x186.png)](https://substackcdn.com/image/fetch/$s_!CgRT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F22d34b42-1b1d-4290-99e3-1dfc1ab0e5e6_662x186.png)

In my second job, the situation was quite the same; the difference is that I had more chances to work with real-life data.

Write a lambda function to load data from S3 to Redshift.

Write a SQL transformation on Redshift.

Oh, S3 is suck. Let’s move to the GCP (the bosses tell me to do it; don’t ask me why because I don’t know).

I did a thing just because I had a task and wanted to complete it.

It was dangerous, and it harmed my reasoning ability. I waited for someone to give me a task. I finished it, and I felt awesome.

[![](https://substackcdn.com/image/fetch/$s_!J_bQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F529c1cad-56f1-447c-a6ec-6bb7366a3f80_582x266.png)](https://substackcdn.com/image/fetch/$s_!J_bQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F529c1cad-56f1-447c-a6ec-6bb7366a3f80_582x266.png)

But over time, the task became less interesting than it used to be, and I felt less satisfied. I asked for more tasks. I stayed up late to complete them. The feeling of satisfaction increased a little bit, but it soon faded away. I asked myself, “Why am I doing this? “

[![](https://substackcdn.com/image/fetch/$s_!hCXI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe7367156-d1c8-4038-b2ee-cab2538e4e7b_618x418.png)](https://substackcdn.com/image/fetch/$s_!hCXI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe7367156-d1c8-4038-b2ee-cab2538e4e7b_618x418.png)

This happened to me because I didn’t know exactly how to create value. I self-created the equation: task completed = value created.

[![](https://substackcdn.com/image/fetch/$s_!NNhJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04b8c120-c6fb-468b-91f8-39b21b6284a0_338x192.png)](https://substackcdn.com/image/fetch/$s_!NNhJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04b8c120-c6fb-468b-91f8-39b21b6284a0_338x192.png)

I was stuck for a while before realizing the solution was easy: being aware of the data engineer's responsibilities.

[![](https://substackcdn.com/image/fetch/$s_!fw2m!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F574f789e-bab7-4cae-b0fb-d35748982aee_484x342.png)](https://substackcdn.com/image/fetch/$s_!fw2m!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F574f789e-bab7-4cae-b0fb-d35748982aee_484x342.png)

Although it was straightforward, it was hard to find them online back then; even the definition of data engineering could have 10 different results on the internet.

It was not until 2022, when [Joe Reis and Matt Housley released the book Fundamentals of Data Engineering](https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/), that I was enlightened.

From the book, the data engineering is:

> *Data engineering is the development, implementation, and maintenance of systems and processes that take in raw data and produce high-quality, consistent information that supports downstream use cases, such as analysis and machine learning. -[Source](https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/)-*

…and the data engineer is:

> *A data engineer manages the data engineering lifecycle, beginning with getting data from source systems and ending with serving data for use cases, such as analysis or machine learning. -[Source](https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/)-*

For me, this is the most important thing you should equip yourself with. It will help you identify how your work could create value, which things matter, how to identify a problem and solve it proactively, what you should learn, why you should learn a thing, and more.

Here is my recommendation: read the [first two chapters of the Fundamentals of Data Engineering](https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/) and do anything else to ensure you understand a data engineer’s responsibilities.

If you’re prepared to enter the field, this will help you be aware of what you should learn and why you should learn it. You will be more motivated than if you were unquestioningly learning a tool or a concept.

If you feel stuck in your data engineer career, this will help you reflect on your contribution to your organization and guide you to seek more opportunities to create more impact as a data engineer.

---

## #2 Not every company has “big data”

I consumed a lot of materials from big tech companies on how they manage their data. PBs of data, hundreds of compute node clusters, fancy and self-built solutions.

[![](https://substackcdn.com/image/fetch/$s_!JmJ9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fce310f8c-0b98-40b3-bd9e-58646d9c0f22_422x358.png)](https://substackcdn.com/image/fetch/$s_!JmJ9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fce310f8c-0b98-40b3-bd9e-58646d9c0f22_422x358.png)

I was fascinated. I was excited about the chance to manage a Spark cluster with 20 nodes or write a Flink job that processes data with 0.47-millisecond latency.

[![](https://substackcdn.com/image/fetch/$s_!XECP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa2bb8351-a35d-4797-aa32-dc7abe368f48_330x298.png)](https://substackcdn.com/image/fetch/$s_!XECP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa2bb8351-a35d-4797-aa32-dc7abe368f48_330x298.png)

But here is the fact:

Not every company operates at the scale of big tech companies like Netflix, Google, or Amazon. **Companies vary in their data maturity and how much data they need to process.**

[![](https://substackcdn.com/image/fetch/$s_!yV1K!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7bce4aed-e29a-418e-a80d-f54128f2877a_1382x448.png)](https://substackcdn.com/image/fetch/$s_!yV1K!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7bce4aed-e29a-418e-a80d-f54128f2877a_1382x448.png)

You might work in a company with a few GBs of data, or most of the data is managed via Excel. If a company hires you as a data engineer, you will help them store, manage, and serve the data efficiently to support their business.

[![](https://substackcdn.com/image/fetch/$s_!ZZDB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe157998-f56e-4cb5-af3a-46f715c95ef3_980x516.png)](https://substackcdn.com/image/fetch/$s_!ZZDB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe157998-f56e-4cb5-af3a-46f715c95ef3_980x516.png)

That’s it.

They don’t care if you can debug a process-10Tbs-data-in-15-minutes pipeline or not.

They don’t care if you can learn and implement a fancy real-time analytics pipeline or a trendy lakehouse.

If you don’t help them leverage the data in the way they want, you fail.

I used to think that only a company with a large amount of data would allow me to learn more.

I was wrong. Yes, big companies can give you opportunities to work with unique challenges. It would be more exciting. However, saying that does not mean you have nothing to learn in a smaller-scale company.

You might not build a whole new database or tweak very low-level details to save two milliseconds, but there are tons of other problems that need you to resolve:

* This table’s column is empty. Why?
* There is no data modeling. What should I do?
* The DAs found it hard to find a table. How could I help?
* …

Becoming a data engineer does not necessarily mean working with advanced tools and technologies or handling enormous amounts of data. We do something to get data from the source system, store and manage it reliably, and when someone needs it, they can seamlessly use it. This ultimate goal should be achieved with the tools and the solutions that suit the organization's context and needs.

[![](https://substackcdn.com/image/fetch/$s_!g1rr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdcffa243-d8b9-4782-8769-f17c6ca23608_818x258.png)](https://substackcdn.com/image/fetch/$s_!g1rr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdcffa243-d8b9-4782-8769-f17c6ca23608_818x258.png)

Keeping this in mind will help you focus solely on value creation, no matter how big your company is.

---

## #3 Technical Skill

I used to have a repo with many docker-compose files to get various tools up and running. That was fun, but it didn’t get me any further.

I realized that if I want to learn something new, I need to:

* Focus on the fundamentals (1)
* To be aware of the “right way” (2)
* To have a feedback loop (3)

The reason we need (1) is straightforward. Deploying a thing is cool, but keeping it operating reliably is another story. Understanding the fundamentals could help you manage the solution most efficiently, detect and resolve a bug faster, make wiser decisions, and learn faster.

This will take you more time, and the speed at which you add new tools to your resume will slow down, but trust me, it’s totally worth it.

Based on the experience of learning many tools and systems for both my daily job and my writing, here is a list of things you could apply:

[![](https://substackcdn.com/image/fetch/$s_!PwPQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F09103a03-8c91-4b36-8083-c6cc1e3d46ca_628x260.png)](https://substackcdn.com/image/fetch/$s_!PwPQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F09103a03-8c91-4b36-8083-c6cc1e3d46ca_628x260.png)

* Asking “What problems does this […] solve? “. The […] could be a tool, a skill, or a service. The more detailed you can answer, the quicker you will understand the fundamentals of things you want to learn. Let's try with Spark:

  + What problems does Spark solve?

    - Efficient distributed data processing → MapReduce could do that
    - It was not intuitive to write a MapReduce job → Spark has a friendlier API → You could dive more into DataFrame, Dataset here.
    - But MapReduce was quite slow → Spark processes data in-memory → You could dive more into RDD, shuffling here.
    - Spark must also ensure fault-tolerance like MapReduce → Data Lineage
    - MapReduce has a limited used case → Spark can support ML, real-time processing, …
* Don’t just read the theory. Read the theory and validate what you learned with a bit of hands-on. Do these incrementally. This will enforce your learning and make the process less boring.
* Be aware of the shared fundamentals. When you learn Snowflake, you know it separates compute and storage behind the scenes. That’s cool. But if you noticed that this pattern is also applied to Databricks and BigQuery, you could learn things faster, as you only need to learn more about what these systems do differently. The more time you focus on the fundamentals, the more shared fundamentals you detect. You will have a broader view and less bias.

**The second thing is being aware of the right way to do something**. From coding a pipeline, managing a cluster, debugging a piece of code, or writing SQL, there will always be a set of best practices to do a thing. Following these in the tools document, well-known frameworks, and your company standards. This will help you save time, make the most of the tool you’re using, and collaborate more easily.

[![](https://substackcdn.com/image/fetch/$s_!ZBR1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F93c7ecb8-af03-4b76-aad9-6deba67c4e7d_442x366.png)](https://substackcdn.com/image/fetch/$s_!ZBR1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F93c7ecb8-af03-4b76-aad9-6deba67c4e7d_442x366.png)

**Finally, you must have a feedback loop**. Don’t isolate your learn process, even if you have to learn alone. We need a way to tell if we’re going in the right direction. This will help you learn faster and way more efficiently. In a time when AI is dominating, asking “it“ to give you feedback is not a bad choice.

[![](https://substackcdn.com/image/fetch/$s_!cZj-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffc3ec0d5-d229-4626-bbd7-924f376e0020_1660x748.png)](https://substackcdn.com/image/fetch/$s_!cZj-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffc3ec0d5-d229-4626-bbd7-924f376e0020_1660x748.png)

“Hey, act like a Google staff data engineer with 20 years of experience, help me to provide feedback on this… or that."

It’s fine.

But for me, human-human conversation is always my choice, no matter whether it happens in any form. If you have friends or colleagues who are more experienced in your work, ask them for feedback. (Just don’t ring their phone at 3 AM)

If you’re alone, expose yourself even more, share your learning on the Internet, make a minor contribution to an open-source project, join forums or Slack channels, or take courses/programs from reliable individuals or organizations.

You might be shy about how amateur you are or resist the feeling of doing something wrong. But trust me, things will get better if you keep asking for feedback.

---

## #4 Only technical skills won’t get you far

From junior to middle, from middle to senior, from senior to staff or manager, when you climb a ladder, it’s not only because you know how to build a complex data pipeline or you can write a Spark job with a blindfold. You got promoted and recognized because you have positively impacted the organization.

To make an impact, technical skills alone are not enough.

The two things I found critical are:

* Problem solving
* Communication

Problem solving is not only about the way you solve a problem. It’s how you identify the problem, break it down into smaller ones, prioritize the ones that matter, and solve them most efficiently given the current constraints and context.

[![](https://substackcdn.com/image/fetch/$s_!G7Um!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb212bdf6-3ce6-4cbd-85ba-ac62dc3019ae_758x222.png)](https://substackcdn.com/image/fetch/$s_!G7Um!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb212bdf6-3ce6-4cbd-85ba-ac62dc3019ae_758x222.png)

This sounds obvious and straightforward, as you might have heard of something like “A problem defined is half-solved,” but in reality, things are complicated than that.

At the beginning of your career, a problem is often well defined. Your boss assigns you a specific task with a measurable outcome. You must detect and resolve a data discrepancy so the dashboard can show a reasonable trend. An out-of-memory Spark job. An incorrect indentation of a Python code block. You have a clue on how to reason about it, or even know how to solve it.

However, waiting for a well-defined problem won’t help you grow.

I have had the chance to work with many colleagues of greater seniority than I am, and one thing I realized they all have in common is the ability to solve problems proactively.

They don’t wait for someone to define the problem for them; they seek and bring it to light. This requires that they understand both business and technical language so they can sit down, listen to business users, empathize with their problems, analyze the situation, define the problem clearly, and translate it to technical details.

[![](https://substackcdn.com/image/fetch/$s_!SZRc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F066f109f-83a6-4250-876a-51ab5b1d8801_712x270.png)](https://substackcdn.com/image/fetch/$s_!SZRc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F066f109f-83a6-4250-876a-51ab5b1d8801_712x270.png)

This is hard because a vague problem is not fun at all. You can’t imagine it. You can’t put it in your head, carry it around, and try to solve it in your free time. It doesn’t have any shape or structure.

However, most of the impacted problems are vague. Because they have a larger scope, involve more people, require knowledge from different areas, and have many affected factors.

For me, the seven-step framework from the book [Bulletproof Problem Solving](https://www.amazon.com/Bulletproof-Problem-Solving-Changes-Everything/dp/1119553024) is a good place to start. You don’t need to tackle a big, organization-level problem at first. You can improve your problem-solving skills by tackling issues systematically and learning proactively from senior colleagues.

And when your time comes, you take your shot. The willingness to proactively look for pain points, solve them, and create value is also crucial here. This brings us back to the first point of this discussion: you should know about your responsibilities.

[![](https://substackcdn.com/image/fetch/$s_!Ry5a!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffe6cec16-1dbc-43fc-855d-895169579dfc_708x246.png)](https://substackcdn.com/image/fetch/$s_!Ry5a!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffe6cec16-1dbc-43fc-855d-895169579dfc_708x246.png)

—

When you solve a problem as a data engineer, you rarely solve it alone. You have to collaborate with many stakeholders from different technical backgrounds, from your teammates, software engineers, data analysts, and data scientists, to business users or even C-level executives.

You need to collaborate effectively. To do that, you must learn to communicate.

Communication is bidirectional.

[![](https://substackcdn.com/image/fetch/$s_!TFdp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fca2d9e8d-638b-4d5a-80e5-2002894936f5_710x166.png)](https://substackcdn.com/image/fetch/$s_!TFdp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fca2d9e8d-638b-4d5a-80e5-2002894936f5_710x166.png)

* **Input**: You must gather and analyze information from many stakeholders with different perspectives on a subject you’re working on.
* **Output**: Then, you have to express what you’re doing or what you gonna to do clearly, in many forms, from talking to writing.

Again, like problem solving, communication seems straightforward at first glance, but it takes time to master. The first things you can do are pay attention to other ideas, entirely focus on what someone is saying, ask if you don’t understand (you’re not the only one in the room), try to express your idea clearly, and care more about writing a document. If you want to learn communication, you will find out the way as you work with other people.

---

## Outro

In this article, I shared everything I wish I could tell myself six years ago when I first started as a data engineer. The biggest lesson? Understanding the responsibilities of a data engineer. I also mentioned shifting the mindset that only big companies with massive datasets can help you grow. Then, I walked through how I'd approach learning technical skills if I had to start again. And finally, I highlighted two often-overlooked skills that make a huge difference: problem-solving and communication.

Thank you for reading this far. Your support means a lot to me. See you in my next article.
