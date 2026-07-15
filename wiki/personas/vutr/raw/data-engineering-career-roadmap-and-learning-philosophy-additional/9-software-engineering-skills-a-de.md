---
title: "9 software engineering skills a DE should have and how to learn them effectively."
channel: vutr
author: "Vu Trinh"
published: 2026-06-16
url: https://vutr.substack.com/p/9-software-engineering-skills-a-de
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Data Quality"]
tags: [https, auto, image, fetch, good, substackcdn]
---

# 9 software engineering skills a DE should have and how to learn them effectively.

*Make your work more reliable*

> Source: [Open post](https://vutr.substack.com/p/9-software-engineering-skills-a-de)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[data-quality|Data Quality]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=200848238)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!f2YV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5bb42302-88ea-4d9c-97b9-04c51027458e_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!f2YV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5bb42302-88ea-4d9c-97b9-04c51027458e_2000x1429.png)

---

# Intro

In recent years, people have called for applying software engineering best practices to data engineering. From CI/CD and testing to environment separation and observability.

The motivation is understandable: if software engineering best practices could ensure software quality, we hope they could do the same for data quality.

I think that’s a great idea.

But now, we have to expand our technical breadth even more. That journey might be confusing.

To clear the mist, I wrote this article to list skills/areas of software engineering that a data engineer must equip themselves with, along with an approach to learning them effectively. Hope this makes your roadmap a bit clearer.

Before jumping into those skills, let's first understand what software engineering is.

> *This article is written purely based on my experience and observations. If you find I miss anything, feel free to let me know.*

---

# What is software engineering?

I have a confession.

For the first few years of my career as a data engineer, I thought software engineering just meant creating working code.

And there's nothing more to say about it; I was wrong. That thought makes me focus only on the writing code aspect and ignore everything else.

[![](https://substackcdn.com/image/fetch/$s_!f6OL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F587c2410-a14a-42e5-bd02-c8e9fc5cfeb5_1248x414.png)](https://substackcdn.com/image/fetch/$s_!f6OL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F587c2410-a14a-42e5-bd02-c8e9fc5cfeb5_1248x414.png)

Software engineering is the discipline of building systems that keep working. Even when requirements change, when bugs arise, and when the guy who originally created them has left the company. Software engineering makes us think about maintainability, reliability, testability, productivity, and scalability.

For data engineers, seeing software engineering as more than coding is crucial. It is no exaggeration to say that software engineering practice is 90% about what works reliably, especially in contexts where even a small mistake could make people lose trust in the data we provide.

The rest of this article covers the specific software engineering skills I believe we should all have.

---

# Writing code that other people (and future you) can understand

> *I said coding is not software engineering, but listing it as the first thing to learn here. ¯\\_(ツ)\_/¯*

(Saying this might get me into a lot of trouble →) Writing code is easy.

But writing understandable code is hard. It needs time.

Writing understandable code means expressing your logic clearly enough that another engineer (or even you, six months from now) can understand, modify, and extend it without spending a whole day figuring out what the current code is doing.

[![](https://substackcdn.com/image/fetch/$s_!EK3M!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3a701cd4-03f3-4ec3-a1d7-ab4f756f0588_934x370.png)](https://substackcdn.com/image/fetch/$s_!EK3M!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3a701cd4-03f3-4ec3-a1d7-ab4f756f0588_934x370.png)

I don’t think I need to discuss much about why we must write understandable code here; a very high chance that you’ve already faced a situation where you inherit someone’s code and a week later you still don’t fully understand it, or have the courage to adjust something with 100% sure it won’t break.

Writing understandable code makes you a less selfish person.

Also, it makes you become better at writing code. To do it, you must first clear your thought process, which will make you better at reasoning and expressing things.

—

## How to learn?

And to achieve it, start simple. Give variables meaningful names, create functions that do one thing and modules that have a clear purpose, and add comments where code is not enough. Then, pay attention to design patterns ([Python-general](https://python-patterns.guide/) or [data-pipeline-specific](https://www.startdataengineering.com/post/code-patterns/)) and follow up your programming language best practices or your company’s practices.

[![](https://substackcdn.com/image/fetch/$s_!suIq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe4347e9-6e2e-41a4-9404-363bece2a5eb_904x570.png)](https://substackcdn.com/image/fetch/$s_!suIq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbe4347e9-6e2e-41a4-9404-363bece2a5eb_904x570.png)

To me, the best way to learn is by participating in the coding review process on both sides: having your code reviewed and reviewing someone’s code. This allows you to get feedback from others while learning from how they write code.

Another effective approach is to read open-source code, or even better, contribute to some open-source project. To enable collaboration, those projects must be understandable enough: you will learn a lot by the way they organize the code, naming the variable, expressing if-else, or handling edge cases.

Read it and “steal“ some of their method, if you can, contribute to the project, and you will have a code review session from the project’s maintainers, who have a lot of experience in writing understandable code.

---

# Version Control

> It’s more than Git.

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * ***200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=200848238)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

---

At some point in your career, you will get a Slack message that says something like: “Hey, did something change in the pipeline? The numbers are weird.”

And you will have no idea.

Because the change happened in a config file that someone edited directly on the server, in a SQL query that lives in a shared Google Doc, or in an environment variable that was updated in the console with no audit log.

—

[![](https://substackcdn.com/image/fetch/$s_!jgHZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd38fb6e4-f825-4ce7-ab97-ec218b2ab9c9_410x332.png)](https://substackcdn.com/image/fetch/$s_!jgHZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd38fb6e4-f825-4ce7-ab97-ec218b2ab9c9_410x332.png)

Version control is the practice of tracking every change to an artifact, such as your project codebase, a variable store, a Docker image registry, or a technical document.

Who changed what and when?

So that you can collaborate safely: review changes, debug, or roll back when something goes wrong.

Most data engineers know Git at the surface level. What I want to say here is that discipline is broader than just Git: if something changes and it could break production, it should be tracked.

It might not have the full functionality of Git (where you write code, stage changes, commit, push, and merge), but it must at least have a mechanism to track who did what, when, and what the historical value is.

## How to learn?

For Git, I don’t think it needs to be complicated.

[![](https://substackcdn.com/image/fetch/$s_!MMUD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F664a4b8c-5077-43ce-918a-23274f526a82_1014x376.png)](https://substackcdn.com/image/fetch/$s_!MMUD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F664a4b8c-5077-43ce-918a-23274f526a82_1014x376.png)

A free GitHub account, a toy project, then invite a friend to work on it, and make sure you guys can collaborate smoothly on the code-modifying aspect. That will give you 70% of Git.

The less 30% is to actually understand how Git works behind the scenes and apply it in a real project.

> For the part “to actually understand how Git works“, you can read my article here:

Then, practice applying version control to things beyond code. This is more about mindset and your willingness (after suffering a lot from real-world incidents).

For example, if a configuration file from a third-party app is sensitive to change, can we version control it, e.g., can we integrate GitHub here?

[![](https://substackcdn.com/image/fetch/$s_!LqK2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9309f610-a773-489b-ad04-7ee4bbc8f402_758x450.png)](https://substackcdn.com/image/fetch/$s_!LqK2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9309f610-a773-489b-ad04-7ee4bbc8f402_758x450.png)

This document is wrong. Someone adjust it. Can we see who did it and contact him/her to correct or ask for the reason?

The processing job fails due to insufficient resources. Can we know who adjusted the worker’s resource, the reason for the adjustment, and the previous resource’s value?

Just keep in mind: if something changes and it could break production, it should be tracked.

---

# Environment separation

> *I don’t know if it has a better name :d*

I tested a new transformation by running it directly against the production database.

It was supposed to be a safe and quick check. However, it causes a downward trend in the end-user dashboard (it was not supposed to be like that).

—

In software engineering, the development flow is something like this: you develop a new feature or fix a bug on your laptop, test it locally, make sure it runs, then merge it into “develop”, where you can break things freely. Next, the code goes to “staging” as a “final rehearsal”; finally, it comes to “production”.

[![](https://substackcdn.com/image/fetch/$s_!zKTj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1440a33d-1a13-4663-bc55-5d3451d8fbde_1510x660.png)](https://substackcdn.com/image/fetch/$s_!zKTj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1440a33d-1a13-4663-bc55-5d3451d8fbde_1510x660.png)

This process allows the software engineer to mitigate the risk and control the quality.

—

We should do the same in data engineering.

Environment separation is the practice of maintaining distinct, isolated setups for different stages of your development workflow (typically dev, staging, and production). Each has its own infrastructure, credentials, configuration, and especially, datasets.

The goal is the same: to mitigate the risk and control the quality.

Another benefit I realize is that you stop being afraid to make changes.

When dev and prod are the same, with every change you test carefully, move slowly, hold your breath, or even delay the process. One wrong move and you’ve corrupted important things.

[![](https://substackcdn.com/image/fetch/$s_!QLbY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a283db8-5605-43ca-804e-a97211e956c8_1150x514.png)](https://substackcdn.com/image/fetch/$s_!QLbY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a283db8-5605-43ca-804e-a97211e956c8_1150x514.png)

When they’re separated, you are braver.

You break things in dev. You have final validation in staging and can deploy to prod with confidence because you’ve already seen it work.

It also makes debugging cleaner. When something breaks in production, you can reproduce it in dev without touching live data. You can isolate the problem, fix it, verify it, and then deploy the fix.

## How to learn?

First, understand why environments need to be separated, what goes wrong when they aren't, before you think about how to implement it.

However, that’s only 40% of the story.

Implementing environment separation in data engineering is about cost management, synchronization, and the use of relevant datasets.

If the production environment costs us $1000/month, will three environments cost us $3000/month?

How do you keep 2 or 3 environment configurations and infrastructure in sync?

How do you ensure that the test data represent real-world properties?

—

Start simple here.

Learn how to manage environment-specific configuration without hardcoding it. Environment variables, environment-specific config files, or secrets managers. The goal is code that runs identically across all environments, with only the underlying configuration details changing.

[![](https://substackcdn.com/image/fetch/$s_!19ft!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb7d91fcd-86ac-46c9-a389-b5007c3d687e_432x476.png)](https://substackcdn.com/image/fetch/$s_!19ft!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb7d91fcd-86ac-46c9-a389-b5007c3d687e_432x476.png)

For infrastructure, we can rely on Infrastructure as Code (IaC) (e.g., Terraform) to ensure reproducibility and version control. Also, we can have control of the resource for each environment. For example, dev workers only need 4 CPUs and 8GB of RAM, while production workers get 16 CPUs and 32 GB of RAM.

[![](https://substackcdn.com/image/fetch/$s_!eRAz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9532e2bb-4a89-41ca-be67-b5dd9cc4aa1f_906x662.png)](https://substackcdn.com/image/fetch/$s_!eRAz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9532e2bb-4a89-41ca-be67-b5dd9cc4aa1f_906x662.png)

For the test dataset, we need to invest in data profiling and sampling to ensure we generate test data with the same properties as the production data (via profiling) without the burden of copying the whole production dataset (via sampling).

[![](https://substackcdn.com/image/fetch/$s_!pbKR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2bdee7dd-5cc9-456e-9ea7-3ca280a2b16d_678x474.png)](https://substackcdn.com/image/fetch/$s_!pbKR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2bdee7dd-5cc9-456e-9ea7-3ca280a2b16d_678x474.png)

The security aspect also needs to be considered here, as production datasets might contain sensitive information (e.g., customers’ email addresses). This information must not be exposed carelessly. Data masking is one mechanism we can apply here.

---

# API

I thought the API was my colleague's backend engineer's problem.

Building a data pipeline is enough for me.

Then I joined a company where 3/4 of the data lived behind third-party APIs. Not from an OLTP database anymore.

Just endpoints, rate limits, and pagination.

—

An Application Programming Interface (API) is a defined way for two systems to talk to each other. In practice, as a data engineer, you’ll encounter them in two directions: calling API endpoints to pull data in, and (occasionally) building APIs to expose something out (most of the time it’s your produced data)

[![](https://substackcdn.com/image/fetch/$s_!PrQA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb5f7dcbb-8950-4334-ad2c-ba4cdb005fe0_1004x336.png)](https://substackcdn.com/image/fetch/$s_!PrQA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb5f7dcbb-8950-4334-ad2c-ba4cdb005fe0_1004x336.png)

For the first scenario, it means writing (Python) code that makes HTTP requests, handles authentication, deals with rate limits, manages pagination, and handles API errors.

In the latter scenario, you will design endpoints that other systems, e.g., an application, can use to fetch data.

—

Data lives everywhere.

It lives in Stripe, in Salesforce, in the company product’s own backend, in SaaS tools that don’t have a native connector.

I used to work for a company where 70% of the data came from third-party APIs.

[![](https://substackcdn.com/image/fetch/$s_!XMIo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff30b42c5-7c16-458c-9260-0bb4f88cd37f_648x532.png)](https://substackcdn.com/image/fetch/$s_!XMIo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff30b42c5-7c16-458c-9260-0bb4f88cd37f_648x532.png)

If you can’t work effectively with APIs, especially HTTP requests, a large portion of the data is extremely hard for you to access.

On the other hand, knowing how to expose data through an API gives you a versatile tool to expose data under your control. (Or if you think again and want to switch to a software engineer instead, knowing how to design APIs would get you a backend job.)

## How to learn?

At first, I was tempted to use a Python package to make an API request.

Actually, that’s the right way to do it.

However, those packages usually abstract every detail of an API call.

To understand it on your own, start by consuming APIs manually before writing any code. Use a tool like Postman to send requests, inspect responses, and understand authentication flows.

Also, get comfortable reading API documentation.

Then write the code.

Python’s `requests` library is the right starting point. Build something real: pull data from a public API, e.g., GitHub. Check for pagination and handle it; the goal is to ensure you pull all the data.

If you could, try hitting a rate-limited endpoint to see what happens, then figure out how to handle it (back-off retry is the common approach here).

Also, express logic to handle all possible errors from that API.

[![](https://substackcdn.com/image/fetch/$s_!h8vC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F47a2dbe2-5b8d-455e-b8b5-7ce834818616_1264x274.png)](https://substackcdn.com/image/fetch/$s_!h8vC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F47a2dbe2-5b8d-455e-b8b5-7ce834818616_1264x274.png)

For designing and building APIs, I recommend starting with FastAPI (the most common Python API library at the moment) and following its best practices.

Following its best practices is key here, as FastAPI is very well documented for creating robust API endpoints.

FastAPI is Python; it’s easy to get running, and it forces you to think about request/response structure, async execution, data validation (with Pydantic), and documentation from the beginning. Build a simple endpoint that serves data from your warehouse. See what breaks when someone (at first, it’s you) actually uses it.

---

# Testing

Testing is the practice of writing a piece code that automatically verifies your … code does what it is supposed to do.

[![](https://substackcdn.com/image/fetch/$s_!he74!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9a22c88c-740b-4a39-a8aa-5a8693452659_852x958.png)](https://substackcdn.com/image/fetch/$s_!he74!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9a22c88c-740b-4a39-a8aa-5a8693452659_852x958.png)

> *Are there tests for … tests?*

For data engineers, testing has many layers.

[![](https://substackcdn.com/image/fetch/$s_!B6cb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa84b3ea1-2f42-4d87-8145-19c07607c9b3_1220x240.png)](https://substackcdn.com/image/fetch/$s_!B6cb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa84b3ea1-2f42-4d87-8145-19c07607c9b3_1220x240.png)

Unit tests usually verify that individual transformation or source-pulling logic behaves correctly.

[![](https://substackcdn.com/image/fetch/$s_!dr7d!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdc7788c7-ca35-469d-a0ff-c23a0ae777d3_660x174.png)](https://substackcdn.com/image/fetch/$s_!dr7d!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdc7788c7-ca35-469d-a0ff-c23a0ae777d3_660x174.png)

Integration tests verify that the pieces work together. In the data engineering context, “the pieces” usually refer to the data pipeline.

Data quality tests check if the data meets expectations/assumptions, e.g, not nullable nulls, unique value, or referential constraint (e.g., primary/foreign keys)

—

I used to think tests slow me down.

In fact, from my countless incidents, tests make you go faster, more specifically, they make you go faster by making things safer.

Without tests, every deployment is a manual verification exercise. You check things by hand, miss edge cases, and only find out something broke when a stakeholder tells you.

With tests, you find the problem automatically (as long as you write good tests)

## How to learn?

First, if you think testing is a waste of time, get out of that thought right away. This is the hardest part

[![](https://substackcdn.com/image/fetch/$s_!L1BB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8c5af7c3-1415-432c-8e2d-d4ad32f1d606_204x56.png)](https://substackcdn.com/image/fetch/$s_!L1BB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8c5af7c3-1415-432c-8e2d-d4ad32f1d606_204x56.png)

Then, start small with pytest here. Write unit tests for your transformation logic, define the input and expected output, and consider edge cases. Don’t aim to cover all the cases at first; you can add later. When you do this more and more, you will naturally know which kinds of cases should be added in different scenarios.

Next, try dbt tests if you use dbt. The built-in tests: not null, unique, accepted values, and relationships, help you cover major cases with almost no effort. Also, dbt lets you define custom tests with SQL.

Then, learn how to integrate these tests with CI pipelines. This won’t take you much time, as you simply configure the CI steps to run the same commands you already run on your laptop.

---

# CI/CD

Continuous Integration and Continuous Delivery (CI/CD) is a practice that automates the building, testing, and deployment of software changes, ensuring faster, less human-intervention, and more reliable deployment.

[![](https://substackcdn.com/image/fetch/$s_!WV0_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3743a258-4d62-4da9-a78b-ae4c39dc479f_1112x454.png)](https://substackcdn.com/image/fetch/$s_!WV0_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3743a258-4d62-4da9-a78b-ae4c39dc479f_1112x454.png)

If you don’t have it, you have to build the Docker, test, and deploy the changes manually. Just imagine how awful it would be if your team had 5 members; you would have 5 different ways to handle that process.

Let’s dive into more details.

Continuous Integration means code change will trigger a set of checks: tests run, code is linted, and builds are verified. If something fails, the pipeline stops and tells you.

[![](https://substackcdn.com/image/fetch/$s_!CcST!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa9ab649f-e2d0-432e-8613-1724dd683aed_1334x524.png)](https://substackcdn.com/image/fetch/$s_!CcST!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa9ab649f-e2d0-432e-8613-1724dd683aed_1334x524.png)

Continuous Deployment means that once those checks pass, the deployment happens automatically: a set of predefined commands is executed to deploy your change (to develop, staging, or production environments)

For a data engineer, the full flow looks something like this: a dbt model changes → a pull request is opened → tests run automatically → the change is reviewed → it merges → the updated models deploy to staging, then production.

## How to learn?

GitHub Actions is the right starting point here. Write a simple pipeline that tests the code change (from the test you defined when learning testing). If it passes, build a Docker image and then push it to a registry.

That’s your first CI/CD pipeline.

Also, reading the CI/CD pipelines from other repositories in your company (or open-source repos) helps here. How does the worked pipeline look? What kind of mandatory tests are there? Are there any templates you can reuse?

---

# Observability

Observability is the practice of instrumenting the systems so you can understand what’s happening under the hood (without waiting for somebody to break it). It has three pillars: logs, metrics, and alerts.

* **Logging** tells what happened. The informativeness of the logs depends largely on how the service outputs them, or how you define what logs in your own developed services

  [![](https://substackcdn.com/image/fetch/$s_!peSH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F83043963-afd5-4d16-8a6f-5902b871beec_1078x570.png)](https://substackcdn.com/image/fetch/$s_!peSH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F83043963-afd5-4d16-8a6f-5902b871beec_1078x570.png)
* **Metrics** are the aggregated signals: row counts, pipeline duration, failure rates, data freshness, CPU utilization, or disk usage.

  [![](https://substackcdn.com/image/fetch/$s_!59YO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc2939afc-8b43-4764-b260-c84dc53427a1_752x416.png)](https://substackcdn.com/image/fetch/$s_!59YO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc2939afc-8b43-4764-b260-c84dc53427a1_752x416.png)
* **Alerts** are the rules you define that turn those signals into notifications. For example, if the row count drops by more than 20% compared to yesterday, tell me.

[![](https://substackcdn.com/image/fetch/$s_!pvCa!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F63249bc7-289b-400d-8cd6-b04e1df39f38_748x394.png)](https://substackcdn.com/image/fetch/$s_!pvCa!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F63249bc7-289b-400d-8cd6-b04e1df39f38_748x394.png)

## How to learn?

If you have a bug or a service is down, whether you’re running a pet project or in a production environment, try to analyze the logs or monitoring metrics to see what happened first. Resist the temptation to Google or throw the logs/screenshot to AI.

If you’ve already spent 30 minutes and still haven't figured it out, then seek help from an external source.

—

If you’re in charge of a piece of code (e.g., building a pipeline or an application), investigate the way you log. First, pay attention to the severity, timestamps, function name, and the error details. Then you seek feedback from colleagues on whether your logging is meaningful enough to debug.

—

[![](https://substackcdn.com/image/fetch/$s_!Yqq7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a70a1f2-5a8f-43a6-ac12-a6ddbd1126e0_1142x320.png)](https://substackcdn.com/image/fetch/$s_!Yqq7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a70a1f2-5a8f-43a6-ac12-a6ddbd1126e0_1142x320.png)

For alerting, keep this in mind: not everything is worth alerting. Too many false-positive alerts will make people complacent, and when a serious incident occurs, no one will take action.

Also, an alert should be set with a clear severity and tied to the downstream impact. For example, a non-critical job failure is a Slack message. A primary key with 20% null values in the production revenue table triggers a multi-departmental alert.

—

The habit to build is: every piece of software you create, ask yourself: how can I find out what happens when something breaks?

---

# Debugging (Investigating)

> *I hesitated to write this section separately as I believed it was a part of observability. After thinking for a while, debugging is about finding, understanding, and fixing failures, while observability is more about tools to support that process. That’s why you still see two separate sections here.*

—

Debugging speed is one of the biggest advantages a data engineer can have.

If you’re a data engineer, you know that errors, failures, bugs happen ALL the time.

[![](https://substackcdn.com/image/fetch/$s_!kZ8l!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbdd9ffef-f7da-40b6-b0c2-160b04ea4b8c_546x384.png)](https://substackcdn.com/image/fetch/$s_!kZ8l!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbdd9ffef-f7da-40b6-b0c2-160b04ea4b8c_546x384.png)

The faster you find the root cause, the less downtime, stakeholder impact, and stress. It also means you learn faster: every bug you methodically trace to its root teaches you something about how your system **actually** works.

However, debugging in data engineering is more challenging, as there's another factor besides the code and the server: the data.

## How to learn?

Honestly, when it comes to learning debugging, I don’t have any advice other than exposing yourself to situations where you actually have to find and fix a bug more often.

This is because, to me, the skill is more about experience.

The more you spend time understanding bugs, the more mature the way you find them next time. You will have your own method to do this. You will develop your own mental checklist for when things break

—

Some of the small steps to get started here.

[![](https://substackcdn.com/image/fetch/$s_!tAWB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3315133e-6f05-4889-957f-6529456665be_1222x648.png)](https://substackcdn.com/image/fetch/$s_!tAWB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3315133e-6f05-4889-957f-6529456665be_1222x648.png)

Learn how to run code debugging with your IDE: setting the breakpoints to see the actual state of the variables, and how the logic is executed.

For data-specific bugs, rely on the data lineage here. If a transformation produces wrong output, work backward: Is the source data correct? Is the intermediate step correct? Is the final output the only thing wrong?

---

# Dependency management and containerization

“It works on my machine.”

I said this when a piece of code I wrote failed in production due to a mismatched dependency.

---

Dependency management is the practice of explicitly defining and pinning the external libraries and tools your code needs to run, and ensuring they use exact versions wherever your code runs.

The value is reproducibility, which makes everything else reliable.

Without it, your pipeline is implicitly coupled to your local machine. It runs on your laptop because you happen to have the right version of DuckDB installed, the right Python version, and the right system library that a package silently depends on.

Move it anywhere else, and your code cannot run until you make sure that the runtime environment is exactly the same as your laptop’s environment

—

When working with Python, you might know about virtual environments.

[![](https://substackcdn.com/image/fetch/$s_!AoT_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F81c09b9b-3ebf-44a5-9923-0b6fa6db70d1_654x516.png)](https://substackcdn.com/image/fetch/$s_!AoT_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F81c09b9b-3ebf-44a5-9923-0b6fa6db70d1_654x516.png)

Instead of installing packages globally on your machine, you create an isolated environment per project. The packages installed here don’t affect anything else, and anyone else who sets up the same environment gets the exact same packages.

First, `requirements.txt` pins your dependencies, making installs reproducible. `pyproject.toml` and tools like UV take it further, managing not just your dependencies but resolving conflicts, and making the whole thing explicit and lockable.

[![](https://substackcdn.com/image/fetch/$s_!rXNC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffbd77378-e01d-4897-aaea-8bae344787c7_1450x590.png)](https://substackcdn.com/image/fetch/$s_!rXNC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffbd77378-e01d-4897-aaea-8bae344787c7_1450x590.png)

Then, when deployed elsewhere, you literally create the same virtual environment as in your local environment, and everything will work fine.

Containerization is a higher level of dependency management.

[![](https://substackcdn.com/image/fetch/$s_!Ho7e!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F89be964d-64e3-4aa9-a820-b85227a33be2_956x446.png)](https://substackcdn.com/image/fetch/$s_!Ho7e!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F89be964d-64e3-4aa9-a820-b85227a33be2_956x446.png)

Containerized technology such as Docker doesn’t just lock your Python packages; it freezes the entire runtime environment. The Python version, OS libraries, system tools, and file structure. Everything your code needs to run is bundled into a single image that behaves identically on your laptop, in CI, in staging, and in production.

If you deploy some code in production, 90% you have to containerize it

## How to learn?

For Python dependency management, start with `venv`. It is built into Python. Create a new environment for each project, activate it before doing anything, and never install packages globally. Then learn pip.

[![](https://substackcdn.com/image/fetch/$s_!6ORG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F83ccd81b-4fc5-49c5-8a3b-49afc1a68448_198x53.png)](https://substackcdn.com/image/fetch/$s_!6ORG!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F83ccd81b-4fc5-49c5-8a3b-49afc1a68448_198x53.png)

From there, I recommend using uv. It’s a modern Python package manager written in Rust, significantly faster than others, that handles virtual environments and lock files in a single tool.

You use uv to create a virtual environment, install packages, and uv will create a lock file that captures your project’s current dependency state. Then, in other environments, you can leverage that lock file to re-create the exact runtime environment.

For containerization, the learning curve is steeper.

Start by Dockerizing something simple, a “hello world“ Python application.

Write a `Dockerfile` that includes everything to get the app running, build the image, and run it.

Then move on to run multiple Docker containers with Docker Compose. A Spark cluster is a strong candidate here.

---

# Outro

In this article, I shared 9 software engineering skills that I believe every data engineer should learn: writing understandable code, version control, environment separation, APIs, testing, CI/CD, observability, debugging, and dependency management.

Hope my work brings value here.

Thank you for reading this far. See you in my next articles.
