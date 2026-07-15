---
title: "How to become a senior data engineer?"
channel: vutr
author: "Vu Trinh"
published: 2026-05-19
url: https://vutr.substack.com/p/how-to-become-a-senior-data-engineer
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "BigQuery", "Data Modeling", "Data Warehouse", "Orchestration", "Change Data Capture", "Data Quality", "Data Governance"]
tags: [https, auto, good, substackcdn, image, fetch]
---

# How to become a senior data engineer?

*Technical skill is only a small part of the seniority.*

> Source: [Open post](https://vutr.substack.com/p/how-to-become-a-senior-data-engineer)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[bigquery|BigQuery]] · [[data-modeling|Data Modeling]] · [[data-warehouse|Data Warehouse]] · [[orchestration|Orchestration]] · [[change-data-capture|Change Data Capture]] · [[data-quality|Data Quality]] · [[data-governance|Data Governance]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+** deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=197174467)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!YDq2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F94f7bbbf-7e94-4e65-8bbc-5ca7713a3784_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!YDq2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F94f7bbbf-7e94-4e65-8bbc-5ca7713a3784_2000x1429.png)

---

# Intro

The inconsistency in some companies’ evaluation systems often leads people to think that the title of software engineer is losing its value. This is even more common in data engineering, given that it is still a relatively new field compared to software engineering.

Lack of best practices and the heavy dependence on a company’s business may make data engineers look very different between Company A and Company B. That’s why one might be a senior DE at Company A, yet only receive a junior offer from Company B.

Saying that does not mean the title is meaningless. No one wants to be stuck at junior forever. It’s not only about salary; it’s also about being trusted and contributing more value.

—

In this week's article, I share my notes that will help you to become more senior. You won’t see anything like “learning tool X or Y”; instead, I want to deliver the mindsets that I distilled from my own experience and learned from “way-more-senior” colleagues than me.

> ***Note:** It’s my note, so you might not find it comprehensive.*

---

# Business value is 1st priority

The company hires data engineers to build a robust data foundation so business users can derive insights from it.

When we begin our journey, we rarely realize this. (If you did, congratulations.)

[![](https://substackcdn.com/image/fetch/$s_!kQ41!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2f75e962-6f20-4d24-8a33-9882487d32bb_1688x514.png)](https://substackcdn.com/image/fetch/$s_!kQ41!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2f75e962-6f20-4d24-8a33-9882487d32bb_1688x514.png)

Any company hires an employee, assuming he is good at “X,” so he can help the company with that. For data engineers, we are hired because we’re good at “data engineering,” ***and*** the company believes we can leverage that to build the data foundation.

That “and“ is very important.

You’re not hired solely for your ability to debug Spark.

You’re hired because you can operate Spark at the scale the company needs to help produce business reports on time.

Thus, every single task you do, every decision you make, must output some business value (directly or indirectly). This is even more true for data engineers, as we work in the (data) department, which is very close to the business decision-making process. (If the company is actually doing that by leveraging data)

—

Business value is the number one priority. But how would you know what value you could help create? This falls back to the question: What is the true responsibility of a data engineer? To answer this, I always suggest reading the first chapter of the book [Fundamentals of Data Engineering: Plan and Build Robust Data Systems](https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/).

> *Data engineering is the development, implementation, and maintenance of systems and processes that take in raw data and produce high-quality, consistent information that supports downstream use cases, such as analysis and machine learning. Data engineering is the intersection of security, data management, DataOps, data architecture, orchestration, and software engineering. — [Joe Reis](https://www.oreilly.com/search/?query=author:%22Joe%20Reis%22&sort=relevance&highlight=true), [Matt Housley](https://www.oreilly.com/search/?query=author:%22Matt%20Housley%22&sort=relevance&highlight=true)*
>
> *A data engineer manages the data engineering lifecycle, beginning with getting data from source systems and ending with serving data for use cases, such as analysis or machine learning — [Joe Reis](https://www.oreilly.com/search/?query=author:%22Joe%20Reis%22&sort=relevance&highlight=true), [Matt Housley](https://www.oreilly.com/search/?query=author:%22Matt%20Housley%22&sort=relevance&highlight=true).*

—

[![](https://substackcdn.com/image/fetch/$s_!db1q!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff44162f4-d09a-4b5d-ac2f-9c38463375c3_1072x624.png)](https://substackcdn.com/image/fetch/$s_!db1q!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff44162f4-d09a-4b5d-ac2f-9c38463375c3_1072x624.png)

The more business-value-oriented you are, the more chances you have to grow and contribute. A signal that tells you you’re going the right path: you focus more on the “boring“ things: data modeling, data security, or data governance.

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+** deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=197174467)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

---

# Seeking the ambiguous but important problems

I used to measure my success, satisfaction, contributions, and the quality of my sleep by the number of tasks I finished. The more tasks I do in a day, the better I feel.

[![](https://substackcdn.com/image/fetch/$s_!J_bQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F529c1cad-56f1-447c-a6ec-6bb7366a3f80_582x266.png)](https://substackcdn.com/image/fetch/$s_!J_bQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F529c1cad-56f1-447c-a6ec-6bb7366a3f80_582x266.png)

It took me a few years to actually stop doing that.

Finishing tasks is not wrong; you’re even praised for doing that. But you have to slow down a bit, because there's something more important than finishing a task.

[![](https://substackcdn.com/image/fetch/$s_!hCXI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe7367156-d1c8-4038-b2ee-cab2538e4e7b_618x418.png)](https://substackcdn.com/image/fetch/$s_!hCXI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe7367156-d1c8-4038-b2ee-cab2538e4e7b_618x418.png)

—

At first, your “world” is small.

It is a Jira ticket, a Python or SQL script, a nightly bug, or a Spark job. You are looking at the ground, ensuring every detail works as expected.

However, to become more senior, you need to go to a “higher place” to understand two things:

[![](https://substackcdn.com/image/fetch/$s_!CZVx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F050969a6-4337-47bd-aae0-325e2fee20b2_1430x678.png)](https://substackcdn.com/image/fetch/$s_!CZVx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F050969a6-4337-47bd-aae0-325e2fee20b2_1430x678.png)

* **Why you’re doing this**: Some tasks bring value, and some don’t.
* **The bigger picture**: you’re not just coding a pipeline that someone else designed forever. You have to step up to design and plan things.

When you do that, you prepare yourself for bigger problems, which means you have a greater chance to make a larger impact. But to do that, you must look beyond the details and draw the bigger picture.

When looking at the “higher place”, the problem isn’t always as straightforward as it appears in your Jira ticket. The problem is shifting more to the business side than the technical side. They are not about how to debug your Spark job or how to reduce the execution time of an Airflow task; it will be more vague:

* Why don’t users trust our data?
* Finance says revenue is $1M, while marketing says it’s $1.2M—both pulled from the data warehouse. Why is there a discrepancy?
* Is there a way to improve Spark and Airflow development productivity in our team?
* The data trend is dropping, but the pipeline ran successfully. Why is that?

It’s more vague than ‘how to run your Spark job’ because the problems happen at a larger scale. They no longer live only in your IDE; they involve your whole team, multiple other teams, or even the entire company. This also explains why, when you solve these problems, you provide more value.

[![](https://substackcdn.com/image/fetch/$s_!pncZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa2cf7b46-87d1-494c-9986-55c91b26bf7e_1464x696.png)](https://substackcdn.com/image/fetch/$s_!pncZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa2cf7b46-87d1-494c-9986-55c91b26bf7e_1464x696.png)

When it involves more people, you have to communicate, and human language is not binary like your code; it’s fuzzy. That makes understanding and solving the problem even harder.

All these problems have two things:

* It’s hard to grab all the aspects of the problems at the first sign: why it happens and how to solve it.
* If you solve it, a very high chance that you’re making a big impact (→ pay rise, promotion, recognition, … )

To become a more senior data engineer, you must embrace these vague problems. Humans’ minds are usually scared of unknown things (e.g., ghosts). That’s why you might be afraid of these problems at first and feel more “safe“ with a clear-ticket task. But to grow, you must force yourself to the more “foggy path”.

—

Willing to handle these problems is just the first step.

You also need to learn and practice the problem-solving skill: understanding the problems (the hardest part), breaking them down, planning, prioritizing, executing, and gathering feedback.

---

# Learn to scale the technical understanding fast

After six years as a data engineer, I’ve realized that learning tools is not wrong, but learning only tools is wrong because tools can become obsolete, especially in this era, where everything is moving so fast.

You know what never becomes obsolete? The fundamentals.

The data engineering fundamentals will never change:

* The really “big“ data will be processed across multiple machines.
* Columnar format is always the winner in the analytical-heavy read workloads.
* Spark abstractions such as DataFrame or Dataset will always be compiled into RDD.
* …

The fundamentals help you scale your technical understanding faster (e.g., you can apply your understanding of OLAP systems to different services from different vendors), which is very important.

[![](https://substackcdn.com/image/fetch/$s_!uJxt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7973bfb4-203d-40f4-9fbc-8ca8076c4016_1150x640.png)](https://substackcdn.com/image/fetch/$s_!uJxt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7973bfb4-203d-40f4-9fbc-8ca8076c4016_1150x640.png)

This is because the more senior you are, the higher the chance you will be involved in more design and decision-making tasks (e.g., designing an end-to-end data pipeline). Having the technical breadth will give you more choices and a bigger picture.

But to achieve that breadth, you can’t learn every single tool or concept one by one; you need a better way to scale your learning. Only learning fundamentals will help you do that.

---

# Trade-off thinking

And knowing the tools/concepts alone might not be enough to choose solutions to your problems. When you choose a solution, ensure it can actually solve your problem, and anticipate its disadvantages.

[![](https://substackcdn.com/image/fetch/$s_!64d4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19e5215e-e0a7-481d-9a2b-f2f6968ac8de_1296x414.png)](https://substackcdn.com/image/fetch/$s_!64d4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19e5215e-e0a7-481d-9a2b-f2f6968ac8de_1296x414.png)

That’s how system design looks in the real world

A key here is that you can’t choose the right solution every single time.

That’s why I recommend making the “reversible “decision anytime you can. It is a choice that allows you to change your mind later without serious consequences (e.g., massive costs, data loss, or downtime).

[![](https://substackcdn.com/image/fetch/$s_!CZbc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F28c32779-acf2-4e75-a2f6-995c7b6c2892_772x478.png)](https://substackcdn.com/image/fetch/$s_!CZbc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F28c32779-acf2-4e75-a2f6-995c7b6c2892_772x478.png)

An example is: you writing a script that fetches data from an API, transforms it, and loads it directly into a production database. Two weeks later, you realize you missed a field and reach out to the source to backfill; however, the source only retains data for 7 days.

To make it more reversible, you can first land the raw data in a landing area (e.g., S3 object storage), and then, when you change your logic, reapply it to the raw data there.

---

# Simplifying

I was responsible for building a data pipeline that delivered daily insights to users.

A real-time pipeline on Google Cloud, using Pub/Sub for handling CDC logs, a PostgreSQL database, and Dataflow for data processing.

[![](https://substackcdn.com/image/fetch/$s_!4NeM!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9376e002-9904-45e2-8add-e502702e2bbe_1124x536.png)](https://substackcdn.com/image/fetch/$s_!4NeM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9376e002-9904-45e2-8add-e502702e2bbe_1124x536.png)

The results:

* The team had more things to manage: Debezium, Pub/Sub, Dataflow, and BigQuery.
* The billing was high, especially with Dataflow, as we didn’t have much experience working with it.

Given the requirement to refresh the dashboard daily, we could have used a simple batch pipeline orchestrated by Airflow to dump data from the PostgreSQL database and load it into BigQuery.

—

The lesson here is to keep everything simple.

[![](https://substackcdn.com/image/fetch/$s_!zCB1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F10cd0944-c8d2-4cd2-81af-7405f8664f50_1306x718.png)](https://substackcdn.com/image/fetch/$s_!zCB1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F10cd0944-c8d2-4cd2-81af-7405f8664f50_1306x718.png)

Simplifying things but still ensuring your solutions meet the requirements is extremely hard. Choosing the right tools, adding components only when needed, and providing well-designed abstractions all take a lot of time to get right. (and sometimes you need the gut feeling)

Take your time, learn from others.

Keep in mind: simplicity gives you a better chance of creating scalable, understandable, and maintainable solutions.

---

# Anticipating the failures

Failure **WILL** surely happen in one form or another: bugs in your code, failed machines, bad designs, low-quality data, or your AI model generates bad code.

The key is to create a solution that is resilient and easy to investigate when it fails, instead of building never-fail one (impossible):

[![](https://substackcdn.com/image/fetch/$s_!6pyt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F582b9d49-0d19-4382-b030-7eecf9326de0_1332x578.png)](https://substackcdn.com/image/fetch/$s_!6pyt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F582b9d49-0d19-4382-b030-7eecf9326de0_1332x578.png)

* When the failures happen, will you know about it? → Observability: logging, monitoring, alerting
* What happens when the pipeline fails? → Fault-tolerance: can be the pipeline self-heal, is there any corrupt data in my sink when a retry happens (idempotency).
* When the volume data increases, how do you deal with it? → Resource estimation
* When bad records appear, what will you do? → Data Quality.

Foreseeing and planning for the failures.

To me, this skill can only be learned if you’ve already gone through real-life failures.

---

# Communication

When you solve a problem as a data engineer, you rarely solve it alone. You have to collaborate with many stakeholders from different technical backgrounds, including your teammates, software engineers, data analysts, data scientists, and C-level executives.

You need to collaborate effectively. To do that, you need to communicate well.

Communication is bidirectional.

[![](https://substackcdn.com/image/fetch/$s_!Xi8Q!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5edb2cb8-7488-4315-8fee-aa05a8526d8d_378x156.png)](https://substackcdn.com/image/fetch/$s_!Xi8Q!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5edb2cb8-7488-4315-8fee-aa05a8526d8d_378x156.png)

* **Input**: You must gather and analyze information from stakeholders with different perspectives, sympathize with their pain points. Input also comes from others: feedback on your work, and retrospectives on areas you need to improve.
* **Output**: Then, you negotiate with the stakeholders about the requirement and the timeline. Next, you have to express your solution clearly, from talking to writing. You also provide feedback for others.

Communication seems straightforward at first, but it takes time to master.

The first things you can do are pay attention to other ideas, focus entirely on what someone is saying, ask if you don’t understand (you’re not the only one in the room), try to express your idea clearly, care more about writing a document, and don’t react to failure by blaming.

If you want to learn communication, you will find out the way as you work with other people.

That’s it, no excuse. Even if you’re very introverted, there is no other way.

---

# Making the team better

As you become more senior, doing your own tasks is not enough. Although these tasks could provide significant value, the way you do your job must also have a positive impact on others. And, there are two ways you can do that:

[![](https://substackcdn.com/image/fetch/$s_!s6x8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb6ad98ed-92eb-406e-b36f-d4ac9982f02b_1348x438.png)](https://substackcdn.com/image/fetch/$s_!s6x8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb6ad98ed-92eb-406e-b36f-d4ac9982f02b_1348x438.png)

* **Help form best practices**: Airflow DAG or Spark job template, data modeling guideline, or any “best way” to do a thing. This might take you a little bit more time, but in return, you will boost all your teammates’ performance.
* **Mentoring**: actively help and guide junior members (or any member who needs it). Sharing your knowledge and experience, helping them move faster, is a way you create impact (and the “senior aura”:d). When you teach someone, you force yourself to understand that piece deeper.

---

# Enjoying what you’re doing

[![](https://substackcdn.com/image/fetch/$s_!CCce!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7bac038d-ab16-46fe-8b60-bbfea99cef78_494x444.png)](https://substackcdn.com/image/fetch/$s_!CCce!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7bac038d-ab16-46fe-8b60-bbfea99cef78_494x444.png)

> *Not for the “love what you do“ and “do what you love“ in self-help books.*

All the things I've mentioned so far can only be done if you actually enjoy what you’re doing. Only that feeling makes you eager to contribute more to the business, seek “big” problems, or leave your comfort zone to host a discussion with 15 stakeholders.

People love their jobs for many reasons, such as great culture, mouth-watering benefits, or cool workers. But for me in data engineering, the number-one factor is the business domain. This is because data engineers, as you might know, have to understand the nature of the data to work with it effectively. And the data reflects what happened with your company's business.

Thus, to understand the data, you must understand the business, and to do that, you must have at least some interest in it. You can’t immerse yourself in accounting if you don’t like numbers. You can try, but you’ll become exhausted. And when you’re exhausted, you stop caring about everything, including the effort required to become a senior.

If you could, make sure you want to become a senior at a company whose business interests you.

Everything will be easier.

---

# Outro

In this article, I share my insights on becoming a more senior data engineer. It includes business value as the 1st priority, seeking ambiguous problems, scaling technical understanding, trade-off thinking, simplifying, anticipating failures, communication, and enjoying what you’re doing.

This is my observation and what I’m applying as I aim to become more senior. It might change over time, and when that happens, see you in an updated article

Thank you for reading this far.
