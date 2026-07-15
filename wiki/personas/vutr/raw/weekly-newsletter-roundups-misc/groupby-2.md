---
title: "GroupBy #2"
channel: vutr
author: "Vu Trinh"
published: 2023-09-15
url: https://vutr.substack.com/p/groupby-2
paid: false
topics: ["Data Engineering", "Apache Iceberg", "Databricks", "Delta Lake", "Data Warehouse", "Data Lake", "Lakehouse", "Data Quality", "ETL"]
tags: [https, auto, paper, good, lake, image]
---

# GroupBy #2

*Lakehouse, Apache Iceberg, Delta Lake; my mini-research on how these formats exist and a little bit of AI paradox.*

> Source: [Open post](https://vutr.substack.com/p/groupby-2)

## Topics

[[data-engineering|Data Engineering]] · [[apache-iceberg|Apache Iceberg]] · [[databricks|Databricks]] · [[delta-lake|Delta Lake]] · [[data-warehouse|Data Warehouse]] · [[data-lake|Data Lake]] · [[lakehouse|Lakehouse]] · [[data-quality|Data Quality]] · [[etl|ETL]]

---

### Databricks’s Lakehouse proposal paper

I'm not sure if **Databricks** was the first to introduce the 'Lakehouse' concept, but this paper is an ideal starting point for anyone who wants to hop on the 'Lakehouse' train.

The paper highlights some challenges with current [data lakes](https://en.wikipedia.org/wiki/Data_lake) and [data warehouses](https://en.wikipedia.org/wiki/Data_warehouse) and suggests: 'Why not combine the best of both worlds?'

(The paper might make you lose your reading mood a little bit, but trust me, it's not filled with mathematical equations like you might imagine).

<https://www.cidrdb.org/cidr2021/papers/cidr2021_paper17.pdf>

*The image below is from this paper.*

[![](https://substackcdn.com/image/fetch/$s_!nHta!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F77d263ae-d28f-42bd-85cd-1f7d0314e4b3_2018x818.png)](https://substackcdn.com/image/fetch/$s_!nHta!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F77d263ae-d28f-42bd-85cd-1f7d0314e4b3_2018x818.png)

### Databricks’s Delta Lake paper

Not surprised at all if you think I'm a **Databricks** fanboy.

If you've already given it a try on the [paper](https://www.cidrdb.org/cidr2021/papers/cidr2021_paper17.pdf) above, you'll know that you can't simply put a query engine on top of your data lake and expect to achieve the performance and management features in a data warehouse.

There must be something in between. Inspite of talking specifically about Delta Lake, this paper still gives readers a clear picture of the challenges and motivations behind the creation of the 'open table format.'

By the way, I’m not Databricks’s fan.

<https://www.vldb.org/pvldb/vol13/p3411-armbrust.pdf>

### Apache Iceberg under the hood

You curios about open table format (OTF) but don’t want to read paper.

I have something for you.

An blog-style-for-anti-paper-reader article from Dremio aimed at introducing Apache Iceberg, another famous OTF. Even if you don’ interested in Iceberg (because you don’t want to betray Delta Lake), the OTF concept, it’s brief history, and current solution’s limitation will worth your time.

<https://www.dremio.com/resources/guides/apache-iceberg-an-architectural-look-under-the-covers/>

---

Subscribe to **SELECT \*** receive cool content that could make your life as a data engineer less boring.

---

### My mini-research on OTF

If you read to this point, you might have some care about OTF.

I’ve made a mini-research-without-any-academic-methodology (just typing randomly on Google search bar) to make my self clearer on the reason behind the rise of OTF like Iceberg,Hudi or Delta Lake.

You can treat my research as a begin point for your self-research journey on OTF and lakehouse.

Hope this help (\*cross finger\*)

<https://www.linkedin.com/posts/vutr27_why-hudi-iceberg-delta-lake-activity-7108049246410481664-mTa2?utm_source=share&utm_medium=member_desktop>

[![](https://substackcdn.com/image/fetch/$s_!BsR0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F14269f30-1ea0-4e51-9712-70a3a97dde9d_1192x1138.png)](https://substackcdn.com/image/fetch/$s_!BsR0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F14269f30-1ea0-4e51-9712-70a3a97dde9d_1192x1138.png)

### “Data debt is an infection”

If you really care how your data engineering effort might help deliver business value (in the end, someone from the company hires you to make the company better in someway), data quality (is it good or bad?) will be one of the first thing to consider.

Couldn't agree agree more with **Chad Sanderson** in his linkedin post on the harsh truths about data quality.

“Good AI requires good data” , Tech debt vs data debt and author’s advice.

Short but powerful message.

You can join the conversation here:

<https://www.linkedin.com/posts/chad-sanderson_dataengineering-activity-7105215278111760385-FOoD?utm_source=share&utm_medium=member_desktop>

### AI makes your data team work less, doesn’t it?

In the world where “AI assistant“ like GPT or Github Copilot, it's widely believed that AI will replace people.

Data team will be less overload thanks to the helping of “virtual friend“ in writing SQL for reporting or generating Python code for ETL pipeline.

Less work to do, so less people the data team will need?

Hmm, that may not the case. This short article from **Tomasz Tunguz** will make you think again.

<https://www.linkedin.com/pulse/paradox-ai-data-teams-how-automation-increase-demand-tomasz-tunguz/?utm_source=substack&utm_medium=email>

*The image below is from this article.*

[![The Paradox of AI and Data Teams: How Automation Will Increase Demand for Data Professionals](https://substackcdn.com/image/fetch/$s_!e0ZI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe88ae677-e6c0-49cc-b667-d57b7e596cba_1080x720.png "The Paradox of AI and Data Teams: How Automation Will Increase Demand for Data Professionals")](https://substackcdn.com/image/fetch/$s_!e0ZI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe88ae677-e6c0-49cc-b667-d57b7e596cba_1080x720.png)

---

Thanks for reading **SELECT \***! Subscribe for free to receive new posts weekly.

---

###
