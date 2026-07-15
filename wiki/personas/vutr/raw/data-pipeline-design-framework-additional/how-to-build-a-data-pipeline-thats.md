---
title: "How to build a data pipeline that’s suck"
channel: vutr
author: "Vu Trinh"
published: 2025-11-25
url: https://vutr.substack.com/p/how-to-build-a-data-pipeline-thats
paid: true
topics: ["Data Engineering", "Apache Spark", "Data Modeling", "Streaming", "Data Quality"]
tags: [https, auto, pipeline, substackcdn, image, fetch]
---

# How to build a data pipeline that’s suck

*In the world where your chance of working at a big tech company is measured by how bad your data pipeline is.*

> Source: [Open post](https://vutr.substack.com/p/how-to-build-a-data-pipeline-thats)

## Topics

[[data-engineering|Data Engineering]] · [[apache-spark|Apache Spark]] · [[data-modeling|Data Modeling]] · [[streaming|Streaming]] · [[data-quality|Data Quality]]

---

> *This Black Friday, I’m offering 50% off the yearly package. Grab it now — the deal will close soon.*
>
> [Upgrade subscription](https://vutr.substack.com/subscribe?)
>
> *I will publish a paid article every Tuesday. I wrote these with one goal in mind: to offer my readers, whether they are feeling overwhelmed when beginning the journey or seeking a deeper understanding of the field, 15 minutes of practical lessons and insights on nearly everything related to data engineering.*

[![](https://substackcdn.com/image/fetch/$s_!PuFl!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf8aac58-9af9-4c71-b1c3-35dd20043d77_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!PuFl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf8aac58-9af9-4c71-b1c3-35dd20043d77_2000x1428.png)

---

## Intro

Over the last six years as a data engineer, I’m unsure how to build a robust data pipeline that runs successfully every time. That depends on many factors. However, there are some things that I know very well: to build a data pipeline that actually suck.

Just imagine a parallel world where the more failed data pipelines you build, the higher the chance you’ll get a raise, promotion, or better job. In this article, I will outline my to-do list that actually takes a data pipeline to another level (in a terrible way).

> ***Disclaimer**: If you read and follow what I write in this article and you lose your job, that’s not my responsibility. If you want serious advice, do the opposite of what is discussed here. If you want serious advice and don’t have time, scroll to the `Outro` section, where I summarize the key points.*

## Make it as complicated as possible.

The first thing you need to do is make the data pipeline as complicated as possible. Ignore what the business user wants and your current company status is; that doesn’t mean anything.

[![](https://substackcdn.com/image/fetch/$s_!l_M0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F36b7515b-1088-479c-93af-aab5d5141f51_548x528.png)](https://substackcdn.com/image/fetch/$s_!l_M0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F36b7515b-1088-479c-93af-aab5d5141f51_548x528.png)

Imagine you’re working for the world's biggest company.

If your pipeline only runs on 20GB of data, make it ready for 20PB. Your processing logic must always be run in parallel on multiple machines (Spark must always be your choice).

[![](https://substackcdn.com/image/fetch/$s_!cXNK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1d0fa6c1-89ca-4dca-94c3-a98f93a12c83_1190x766.png)](https://substackcdn.com/image/fetch/$s_!cXNK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1d0fa6c1-89ca-4dca-94c3-a98f93a12c83_1190x766.png)

If your business users can wait a day for data to arrive, they know nothing about it. The data must come at the speed of Flash; let’s bring stream processing pipelines to the table.

[![](https://substackcdn.com/image/fetch/$s_!bTX3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e224d36-efa9-4806-a21d-1f9d38aea6be_1202x334.png)](https://substackcdn.com/image/fetch/$s_!bTX3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e224d36-efa9-4806-a21d-1f9d38aea6be_1202x334.png)

> *I’m offering 50% off the yearly package. Grab it to continue learning super helpful tips and tricks to destroy your pipeline. The deal will close soon.*
>
> [Upgrade subscription](https://vutr.substack.com/subscribe?)

Next, scroll through LinkedIn, Twitter, Google, Meta, Uber, or Netflix to see which tools are getting attention or have just been released in the last few days.

[![](https://substackcdn.com/image/fetch/$s_!JpOw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b6306be-9231-48dc-b708-7e02c8f0e8cd_524x270.png)](https://substackcdn.com/image/fetch/$s_!JpOw!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b6306be-9231-48dc-b708-7e02c8f0e8cd_524x270.png)

Then, you use those tools right away in your pipeline. That has two benefits: you are following the trend, and if these tools have bugs or lack integrations, no one will help you; the pipeline will fail, that’s what we want.

[![](https://substackcdn.com/image/fetch/$s_!Vb72!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fff294d39-5017-4107-bdfb-485149c83eec_708x254.png)](https://substackcdn.com/image/fetch/$s_!Vb72!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fff294d39-5017-4107-bdfb-485149c83eec_708x254.png)

The tool with large community support and widespread adoption must be avoided at all costs. The disadvantages of these tools are that they’re well battle-tested and ready for production, and they also offer more integration options.

That makes your pipeline simpler and more likely to run successfully; we don’t want that. You must also try to increase the number of tools you use in a pipeline. More tools will add to the pipeline’s complexity.

[![](https://substackcdn.com/image/fetch/$s_!5zgZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0397ef94-5ec8-4df9-bfec-c62f16f6705f_506x300.png)](https://substackcdn.com/image/fetch/$s_!5zgZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0397ef94-5ec8-4df9-bfec-c62f16f6705f_506x300.png)

Besides business users, you must also ignore your teammates. Choose your preferred language in all cases. Java, Rust, Python, Go, SQL; you don’t need to adapt.

Even if a Python script can handle the pipeline, ignore it; even if most of your teammates are data scientists and familiar with SQL, ignore it. Trust yourself and always go with your choice (Java, for example).

[![](https://substackcdn.com/image/fetch/$s_!mq9a!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6444175f-6466-432f-b104-f246a8f5c5bb_1276x450.png)](https://substackcdn.com/image/fetch/$s_!mq9a!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6444175f-6466-432f-b104-f246a8f5c5bb_1276x450.png)

One more thing, also ignore what you’re team already has: frameworks, guidelines, existing infrastructures, etc. Don’t even think about it. That decreases the chance your pipeline will fail. Build everything from your own, trust your instinct, make your own rules, and don’t reuse anything.

## Keeping the secret

> *Like, if someone knows about that secret, you will die*

Develop the pipeline as if you’re keeping a secret. Only you know what the pipeline actually does. No design, no document, no code comment, no pull request message.

[![](https://substackcdn.com/image/fetch/$s_!xcCb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5a929edb-3598-4c59-afdf-6b6581d76b24_910x376.png)](https://substackcdn.com/image/fetch/$s_!xcCb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5a929edb-3598-4c59-afdf-6b6581d76b24_910x376.png)

When you write code, encoding your variable with only symbols you know (a, b, c). You must aim for the variable names that might be forgotten in the future; that ensures even you won’t understand when you re-read it.

[![](https://substackcdn.com/image/fetch/$s_!Phi_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2de08420-0cc8-4cf5-8a44-c0b5d5101bf9_736x452.png)](https://substackcdn.com/image/fetch/$s_!Phi_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2de08420-0cc8-4cf5-8a44-c0b5d5101bf9_736x452.png)

At runtime, you must also keep the secret.

[![](https://substackcdn.com/image/fetch/$s_!epmj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F39ca1d1d-3336-4776-b53b-1c5caabb1a7b_650x280.png)](https://substackcdn.com/image/fetch/$s_!epmj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F39ca1d1d-3336-4776-b53b-1c5caabb1a7b_650x280.png)

Don’t look at the pipeline when it runs, don’t monitor it, don’t care how many resources it’s using. You should be careful about logging and error handling as well, as the goal is to keep the secret. Don’t log anything; when an error happens (sure it will happen), just let it happen silently, no messages, no stack traces.

Remember, if anyone understands or knows how to operate or debug your pipeline, you will die.

## Save your pipeline’s code in the Google Drive.

As you keep the secret from everyone, you must save the pipeline logic in Google Drive or local folders. Git just for the losers. Why do we need to expose our code to others?

[![](https://substackcdn.com/image/fetch/$s_!LKB0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ffb64d2-3543-4170-8231-10293e57dc80_638x392.png)](https://substackcdn.com/image/fetch/$s_!LKB0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6ffb64d2-3543-4170-8231-10293e57dc80_638x392.png)

Zipping and copying the entire pipeline’s codebase when deploying to production is a better approach. No version control and CI/CD pipelines. If we want to fix something, we code on the laptop, zip it, and copy it again.

Wait a minute, if things need to be fixed, it means the pipeline has failed; we achieve our goal.

We don’t care about bug fixing, collaborating, rolling back, or deploying a new version.

## Your data pipeline will fail, great!

In a world where the failure of your data pipeline is the ultimate goal, we can comfortably skip fault tolerance. That’s only for the success pipeline (success is bad in this article, remember?)

[![](https://substackcdn.com/image/fetch/$s_!oVdJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffeeb5fdb-4454-4d77-a98a-7fc48c765ff9_608x402.png)](https://substackcdn.com/image/fetch/$s_!oVdJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffeeb5fdb-4454-4d77-a98a-7fc48c765ff9_608x402.png)

Will the pipeline self-heal, or must we retry it manually? Skip

The retry mechanism, such as backoff? Skip

Does retrying too much put pressure on the source? Skip

Does retrying too often cause corruption in the sink? (The pipeline inserts new data every run; retry will cause duplicated data) Skip

Where do the intermediate data go? (Your pipeline has three steps: A, B, C if it fails at C, where does the data from A and B go?) Skip

Do the failed pipelines need to be rerun from the beginning, or can they be restarted from where they failed? Skip

And tons of other things.

Handling pipeline failures is one of the most crucial tasks when building a reliable pipeline. However, we’re living in a world where your career ladder is based on how miserable your data pipeline is, so that we can skip all these things.

## Keep things in one place.

Don’t break your code into classes or functions.

To me, it’s acceptable to have a giant function with your whole logic go there. A function that can do multiple things is the best thing that can happen in your life. That’s also a way to keep secrets from each other.

[![](https://substackcdn.com/image/fetch/$s_!FlnX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdef667dc-e4c7-43cd-b922-524679f692c3_546x396.png)](https://substackcdn.com/image/fetch/$s_!FlnX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdef667dc-e4c7-43cd-b922-524679f692c3_546x396.png)

Your teammates will read your function and give up in 10 seconds. An effective encryption method.

Don’t break the pipeline into smaller tasks.

[![](https://substackcdn.com/image/fetch/$s_!Hf3p!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb70e5b96-acfe-40eb-9ed9-c55fa5c8fa47_1000x440.png)](https://substackcdn.com/image/fetch/$s_!Hf3p!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb70e5b96-acfe-40eb-9ed9-c55fa5c8fa47_1000x440.png)

That’s only for those who have time. The ideal pipeline will only have one task. All the logic will be handled by these tasks, from pulling data from the source to 10 transformation steps. It’s even better if all of these are packed in a single function. I quoted myself here.

> *A function that can do multiple things is the best thing that can happen in your life.*

From the above section, you don’t need to handle pipeline failures, so keeping everything in one place is not the problem here.

If the pipeline fails, it fails as a whole.

We don’t need to identify the failed steps

We don’t need to retry, backfill, or test them in isolation.

Speaking about testing, we don’t need that either.

## Remember: Don’t test

When building a robust data pipeline, we don’t test it only with simple tests that check whether it runs; we use more advanced tests, such as unit tests, integration tests, or pre-running the pipeline in the dev environment.

[![](https://substackcdn.com/image/fetch/$s_!ZNEP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa5af905e-4e23-453a-a07c-b9d012d59e27_916x318.png)](https://substackcdn.com/image/fetch/$s_!ZNEP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa5af905e-4e23-453a-a07c-b9d012d59e27_916x318.png)

However, we want our pipelines to fail. Just don’t do all of them. The time when you stop writing the pipeline’s code is when the pipeline finishes and is ready to be deployed.

## The harder you can run your pipeline in different environments, the better.

Because we don’t need to test, we also don’t need the ability to run the pipeline smoothly in different environments (dev, staging, prod…). You hardcode everything from environment variables, source/sink configs, to database passwords. Just put all of them in your code.

Dynamic variables are confusing.

[![](https://substackcdn.com/image/fetch/$s_!Wnn2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F030b3c3b-1b91-4a70-a9b4-44786effc52d_728x428.png)](https://substackcdn.com/image/fetch/$s_!Wnn2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F030b3c3b-1b91-4a70-a9b4-44786effc52d_728x428.png)

You can save costs by not storing the config with a third-party vendor. The pipeline will be simpler; you don’t need two separate places, one to store non-credential configs, one to store credential ones. You also do hackers a favor by giving them your API keys or database passwords for free.

## No data quality

The next thing you need to ignore is the quality of your data. In the normal world, every data pipeline’s step must have a goal: landing data in object storage, cleaning/standardizing data, loading data into facts/dims, or some giant tables. In a mature company, a data pipeline goal is derived from the data model:

[![](https://substackcdn.com/image/fetch/$s_!g8yv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c27e7b1-7f47-40f3-8888-26d3c7f50532_1340x546.png)](https://substackcdn.com/image/fetch/$s_!g8yv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c27e7b1-7f47-40f3-8888-26d3c7f50532_1340x546.png)

* Can my transformation reuse any tables? → Look at the data model
* What table’s fields do I need to prepare? → Look at the data model
* What is the relationship between table A and B? → Look at the data model
* Why do I need to process this table? → Look at the data model

In our world, we don’t want the pipeline to be successful, so we don’t care about the data model. The best case is you’re working at a company where you’re the first member of the data team, no infrastructure, no framework, and no data modeling.

[![](https://substackcdn.com/image/fetch/$s_!e-z-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F59f8e6cf-5502-4523-86f6-86c7d75e86fa_1142x410.png)](https://substackcdn.com/image/fetch/$s_!e-z-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F59f8e6cf-5502-4523-86f6-86c7d75e86fa_1142x410.png)

The worst case is when you join a company with a well-established data model; you must remind yourself that you must not follow the data model, it’s evil, and it prevents your pipeline from failing.

Just write random code that doesn’t follow any guideline (trust your instinct, remember?). Feel free to miss a field or add one that no one uses, ignore the data type (in short, ignore the schema), join the two tables without a random pair of keys that seem to have some common, skip the tables that you can reuse, and rewrite everything by yourself (Reusability is for the weak).

[![](https://substackcdn.com/image/fetch/$s_!8iaS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d1dd6c2-e3e8-4856-961f-c3582e039d09_1018x484.png)](https://substackcdn.com/image/fetch/$s_!8iaS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d1dd6c2-e3e8-4856-961f-c3582e039d09_1018x484.png)

We also don’t need to check for data quality (we want the pipeline to fail; high data quality doesn’t contribute to that). Duplicated, stale, constraint-violated (primary/foreign key), and not reflecting what happens in the real-world data is what we want.

[![](https://substackcdn.com/image/fetch/$s_!_L8M!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F93d701cd-ef8b-41d8-b4f2-46e39a0b5ce6_984x374.png)](https://substackcdn.com/image/fetch/$s_!_L8M!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F93d701cd-ef8b-41d8-b4f2-46e39a0b5ce6_984x374.png)

That will save us a lot of time because ensuring data quality is a time-consuming process.

There are cases when you don’t even know that your data is in a bad state.

For example, there is an incident from the source that will drop data from some stores, just a small amount, and all the tests pass. Still, your business users are always weirded out by the number on the dashboard; the issue can only be detected by visualizing the trend and using statistical methods to spot drops (this approach is usually called anomaly detection).

That said, in the real world, ensuring data quality is an art. The challenge is to cover all the potential issues that could affect your data.

Luckily, we don’t need a data quality check here, fewer tasks to do, more chance the pipeline will destroy somebody’s dashboard or machine learning models.

## Outro

In this article, I list out my experiences to “help” you build a data pipeline that will fail miserably. As you can see, building a failed data pipeline is easy; the key is to be arrogant, selfish, and irresponsible at the same time.

In contrast, building a robust, reliable, and business-oriented data pipeline takes more effort and time. There are more things I need to learn. However, I’m pretty sure that we must do the following things to build that kind of pipeline:

* Respect the business requirement, give feedback, and educate the business user if needed. The purpose is to deliver a result that contributes to the business goal.
* Keep it as simple as possible.

  + Use mature tools. They’re battle-tested, ready for production, and provide more integration options.
  + Keep the number of tools involved minimal; add more tools only when you actually need them. More tools mean you need to operate/maintain/monitor more, which adds complexity.
  + Don’t run anything on a multi-node processing framework (e.g., Spark) when you can process it on a single machine (e.g., Polars, DuckDB)
  + Consistency: follow what your team has: from the frameworks, guidelines, templates, data modeling,…
  + Reusability: Don’t reinvent things, check if you can reuse anything: from intermediate tables, code functions, processing clusters, …
* Make sure everyone knows what you’re doing: writing a document, writing understandable code, and giving a clear message when errors happen.
* Version control your pipeline and make sure it can be automatically deployed or rolled back to older versions.
* Ensure your pipeline can be fault-tolerant. When it fails, what happens next?
* Modularize your pipeline. That helps debugging, testing, and backfilling more seamlessly.
* If it is possible, you should test everything. At least, make sure your pipeline can run in the dev environment before deploying to production.
* Make your pipeline agile; store the config and credentials separately, don’t hard-code them. This allows you to run your pipeline on different environments more easily.

  + For credentials, store them in a place that prevents unauthorized access.
* Check the quality of your data. If your company has a data model, great, based on it to define the checking rules (not null, unique, …). Working proactively with business teams to cover other bad things that could happen with your data.

—

Thank you for reading this far. See you in my next article.
