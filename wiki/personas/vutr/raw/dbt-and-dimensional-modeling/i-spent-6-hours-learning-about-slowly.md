---
title: "I spent 6 hours learning about Slowly Changing Dimension (SCD)"
channel: vutr
author: "Vu Trinh"
published: 2025-08-19
url: https://vutr.substack.com/p/i-spent-6-hours-learning-about-slowly
paid: true
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Spark", "Data Modeling", "Data Warehouse"]
tags: [https, type, auto, dimension, table, substackcdn]
---

# I spent 6 hours learning about Slowly Changing Dimension (SCD)

*Everything you need to know*

> Source: [Open post](https://vutr.substack.com/p/i-spent-6-hours-learning-about-slowly)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-spark|Apache Spark]] · [[data-modeling|Data Modeling]] · [[data-warehouse|Data Warehouse]]

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=170508804)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

[![](https://substackcdn.com/image/fetch/$s_!kco1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F542a6916-476e-405f-bbe1-1bfbfa25f2ac_2000x1428.png)](https://substackcdn.com/image/fetch/$s_!kco1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F542a6916-476e-405f-bbe1-1bfbfa25f2ac_2000x1428.png)

---

## Intro

We, data engineers, capture, store, process, and serve data (with the hope) to help our companies leverage that data to get business advantages. Throwing data into the data warehouse is not enough. The key is that the data must accurately reflect real-world information, specifically how the company’s business operates.

To achieve this, we must first understand that information is not static; it constantly changes over time. Managing data changes is crucial. In this article, we delve into Slowly Changing Dimensions (SCD), a set of techniques for handling and controlling changes in data warehouses.

---

## Overview

Dimensional modeling was first introduced in Ralph Kimball's 1996 book, The Data Warehouse Toolkit (1st edition). Companies have widely adopted it to organize analytic data. The approach aims for simplicity, which aligns with how most business users think.

They naturally think about their operations in terms of measurable metrics and the contexts in which those metrics are observed. For example, a retail manager might want to analyze sales performance by product category, across different regions, over the last three months. This way of thinking is inherently dimensional: products, regions, and time are all distinct perspectives or dimensions through which performance can be evaluated.

This approach organizes data in star schemas. Named for its resemblance to a star, the schema consists of a central fact table surrounded by multiple-dimensional tables.

## Fact

The fact table is the central table in the star schema. It stores the performance measurements resulting from an organization’s business process events. Kimball encourages us to store the low-level measurements to achieve more flexibility.

[![](https://substackcdn.com/image/fetch/$s_!fXEn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feb0701d9-afa8-416e-8a5c-d617a45adab1_1116x590.png)](https://substackcdn.com/image/fetch/$s_!fXEn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feb0701d9-afa8-416e-8a5c-d617a45adab1_1116x590.png)

Each row in a fact table corresponds to a physical measurement event. The data on each row is at a specific level of detail, referred to as the grain; all rows in a fact table must be at the same grain level.

A fact’s row contains:

* **Foreign Keys**: Links to the related dimension tables.
* **Measures**: Numerical values, such as revenue, quantity sold, or profit.

## Dimension

Dimension tables provide descriptive context for the facts. They describe the “who, what, where, when, how, and why.” Each table focuses on a business dimension, such as product, country, or date.

[![](https://substackcdn.com/image/fetch/$s_!6lV-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F504495ea-97bf-4820-876a-8aeb99f8d519_1256x690.png)](https://substackcdn.com/image/fetch/$s_!6lV-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F504495ea-97bf-4820-876a-8aeb99f8d519_1256x690.png)

They play a crucial role in the data warehousing system because they provide a context for measurements. A skyrocketing revenue number alone does not give insight into the business. Each dimension table has a single primary key. This key is “distributed“ to the fact tables as a foreign key.

## Dimension’s primary key

Kimball suggests that the dimensions’ primary key should not be the same as the key used in the operational database. This decouples the way our data warehouse manages the primary key compared with how the source system manages it.

[![](https://substackcdn.com/image/fetch/$s_!e7Et!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F62a82f54-fc2f-447b-b7e4-d3dc7b17a35e_830x410.png)](https://substackcdn.com/image/fetch/$s_!e7Et!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F62a82f54-fc2f-447b-b7e4-d3dc7b17a35e_830x410.png)

Dimension primary keys are recommended to be the surrogate keys. In the past, it was the standard practice to use monotonically increasing integers for the surrogate key. However, there is an alternative approach that uses the cryptographic hashing functions to calculate a surrogate key from the data.

The surrogate key plays a crucial role in dimension table history tracking. We will examine this in more detail when we delve into each SCD later.

## Slowly Changing Dimension (SCD)

Recalled that dimension tables describe the “who, what, where, when, how, and why.” Although these descriptive contexts are quite static (users don’t change their names), they could indeed change in the real world; a store changes location, a product is rebranded with a new category, or a customer’s name is misspelled.

Kimball introduced several techniques to deal with these changes.

## Type 1: Overwriting

> *Note: There is an **SCD type 0** in which dimension records are not allowed to be changed. I think there’s nothing much to discuss about this type, so I won’t spend a section on it.*

In this type, if there is a change in a dimension record, the system detects the affected row and overwrites it with the new value. When consuming the dimension table, the users always observe the latest state of the records.

[![](https://substackcdn.com/image/fetch/$s_!PgiA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d63371c-c60b-42af-b211-df91ecefd289_686x298.png)](https://substackcdn.com/image/fetch/$s_!PgiA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d63371c-c60b-42af-b211-df91ecefd289_686x298.png)

This could be useful when you don’t care about keeping track of history. On the downside, you can guess it!

Given that a user first lived in Vietnam in July and then moved to Singapore in August, SCD type 1 will overwrite the record’s country column. The measurement of the user in Vietnam disappears. The breakdown of total sales by country will yield different results as the purchase of this user in Vietnam is no longer present.

[![](https://substackcdn.com/image/fetch/$s_!2_4D!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa45ed3c8-c64d-4360-89f3-0cadcb44a8c8_556x304.png)](https://substackcdn.com/image/fetch/$s_!2_4D!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa45ed3c8-c64d-4360-89f3-0cadcb44a8c8_556x304.png)

## Type 2: Adding new rows

> *The most used one*

Beginning with these types, changes are tracked.

If there is a change in a dimension record, the system will insert a new row with the changes. The new record will have a different surrogate key (the primary key) compared to the original record. Fact rows can refer to the other version of the dimension table record by using the desired foreign key.

---

> *With only **$7/month (billed annually)**, you can access all the materials you need to grow from junior → senior DE.*
>
> * *This article and **200+**deep-dive data engineering articles*
> * ***[practice-spark](https://spark.vutrinh.net/problems)***: **65 LeetCode-style problems** to practice **Spark SQL/DataFrame**
> * ***[learn-spark/dbt/airflow](https://learn.vutrinh.net/#tool)**: **CLI tools** to master **Spark/dbt/Airflow***
>
> [Upgrade with 7$/month](https://vutr.substack.com/subscribe?coupon=c08a9839&utm_content=170508804)
>
> * *If you’re a student with an education email, use this **[50% ANNUAL DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)***
> * *If you’re a **Vietnamese user**, please DM me for an upgrade due to payment issues. As compensation for the inconvenience, you’ll get **50% OFF** the annual plan.*

When applying Type 2, the dimensions record must include two columns: one indicating when the record is effective and one indicating when it expires. I will refer to them as `start\_date` and `end\_date` in this article.

[![](https://substackcdn.com/image/fetch/$s_!u2ya!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2326abd3-da6a-4fcb-933c-7d190551e988_1166x564.png)](https://substackcdn.com/image/fetch/$s_!u2ya!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2326abd3-da6a-4fcb-933c-7d190551e988_1166x564.png)

When the new row is added, the previously associated row is marked as “expired”. The previous row’s `end\_date` will be set to the prior date of the new row’s `start\_date` to ensure there will be no gap between them. The latest row will now have the `end\_date` of 9999-12-31.

This helps when loading the data; data engineers can determine which surrogate key to use for fact records that fall within the associated valid date range. The pre-calculated metrics won’t be affected here, as historical fact rows still refer to the historical dimension with the associated valid date range. The new fact row will have a foreign key pointing to the new dimension row.

[![](https://substackcdn.com/image/fetch/$s_!bmVr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F105d2e75-4ec7-4b95-a179-0a0757e7a034_646x390.png)](https://substackcdn.com/image/fetch/$s_!bmVr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F105d2e75-4ec7-4b95-a179-0a0757e7a034_646x390.png)

Compared to type 1, the report result will surely be different if the user purchases the product first in Vietnam and then buys it again when moving to Singapore. The sale of that user will be reported separately in Vietnam and Singapore in July and August.

[![](https://substackcdn.com/image/fetch/$s_!8leF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F93a243ca-6a94-4b0e-9d60-b53b3099c897_512x328.png)](https://substackcdn.com/image/fetch/$s_!8leF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F93a243ca-6a94-4b0e-9d60-b53b3099c897_512x328.png)

## Type 3: Adding new columns

Implementing type 2 means one thing: your fact rows can only refer to one version of the dimension record. In July, the user will live in Vietnam, and in Singapore in August.

There are cases when fact rows need to be observed in both past and current contexts. The SCD type 3 can help. It tracks changes by adding a new column(s); the number of columns indicates how far back we want to check the history. In most cases, one more column is sufficient to keep track of the current and previous versions.

[![](https://substackcdn.com/image/fetch/$s_!R4T3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7296e0d0-1f28-4fe5-884d-95ad788b48c9_810x670.png)](https://substackcdn.com/image/fetch/$s_!R4T3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7296e0d0-1f28-4fe5-884d-95ad788b48c9_810x670.png)

When joining with dimension tables, fact rows don’t need to use different foreign keys for different versions; users simply need to choose the version of the dimension to observe by selecting the desired column. The ability to let fact rows be observed by multiple versions of dimensions gives Type 3 a less-known name: alternate realities.

[![](https://substackcdn.com/image/fetch/$s_!hHqj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7343386d-8dae-4b05-8438-52999a0cc186_1118x600.png)](https://substackcdn.com/image/fetch/$s_!hHqj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7343386d-8dae-4b05-8438-52999a0cc186_1118x600.png)

Compared to type 2, this type has the advantage that we can keep track of the history of a small set of columns. However, given the fact that we’re living in this time, the disk is not as expensive as it was in the past, the storage-saving advantage of type 3 seems to be negligible.

One additional point is that this type requires schema evolution when we decide to track the history of a column that was not planned to be tracked when the table was first created.

### Some of my thoughts

I need to confess here that I am having trouble thinking of a case where we need to implement type 3, given that its strength is to allow a fact row to refer to different versions of the dimension.

My intuition is that two real-life events that occur in different contexts at different times should be observed within their respective contexts only. I also looked on the Internet for some examples, [but people are just as curious as I am](https://www.reddit.com/r/dataengineering/comments/ydwjky/real_examples_of_type_3_scd/). Kimball also stated that this type is infrequently used, as it is only required to support observing two views of a real-world event simultaneously.

I read somewhere on the Internet that part of the reason Type 3 was introduced back then was that SQL systems at that time didn’t support window functions. Nowadays, the previous state of the dimension could be achieved by using the `LAG` window function on the type 2 dimension, where the user can partition by the dimension’s key and order by the `start\_date`.

Comment if you have the chance to use Type 3 in real life; I’m really curious about which scenario it could help with.

## Type 4: Separating

I found there is an inconsistency in how this type could be implemented. The way people describe it on the internet differs from how I read it in the Data Warehouse Toolkit book. I will refer to the approach from the Data Warehouse Toolkit book, approach A, and the approach I found on the Internet, approach B.

### Approach A

Kimball suggests that Type 4 will split frequently changing attributes (columns) into a separate dimension table, referred to as a mini-dimension.

[![](https://substackcdn.com/image/fetch/$s_!Ig_B!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fccdc9de9-57b8-42d2-ab1d-758668d3e6c3_904x464.png)](https://substackcdn.com/image/fetch/$s_!Ig_B!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fccdc9de9-57b8-42d2-ab1d-758668d3e6c3_904x464.png)

The key here is that the mini-dimension table only stores **unique combinations of column values**. For example, instead of having a row for every single customer, the mini-dimension has a row for each distinct profile (e.g., "Age 25-34, VIP account, Income $50k-$75k).

[![](https://substackcdn.com/image/fetch/$s_!_dqi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0918b7cb-b38b-4afe-bb36-e0d6286bbef9_598x532.png)](https://substackcdn.com/image/fetch/$s_!_dqi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0918b7cb-b38b-4afe-bb36-e0d6286bbef9_598x532.png)

Kimball suggests converting continuous values in a mini-dimension table, such as income or age, into predefined bands. This reduces the number of rows, as many changes could be in the same bands.

A fact table now requires an additional foreign key to reference the new mini-dimension table.

[![](https://substackcdn.com/image/fetch/$s_!OA0r!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fedb9859b-9059-448c-8d2e-59c1f818679a_876x498.png)](https://substackcdn.com/image/fetch/$s_!OA0r!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fedb9859b-9059-448c-8d2e-59c1f818679a_876x498.png)

If users need the exact data value instead of the value band, Kimball suggests including the raw data value in the fact tables.

### Approach B

With this approach, Type 4 is similar to Type 2, except for one key difference: the latest changes and historical changes are kept in two separate tables. When changes occur, the current table is updated by overwriting the record, and the previous version is ingested into the history table.

[![](https://substackcdn.com/image/fetch/$s_!9fKn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb3480e5d-0e07-47a9-89cc-5a7416f3abc8_888x616.png)](https://substackcdn.com/image/fetch/$s_!9fKn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb3480e5d-0e07-47a9-89cc-5a7416f3abc8_888x616.png)

The current table doesn’t need to maintain the `start\_date` and `end\_date` columns to specify the valid range of the record, given that all records in this table are in the latest state. The history still needs to keep the `start\_date` and `end\_date` columns to preserve the history.

This approach is particularly helpful when you only need the latest status, such as the most recent user email or the latest phone number in marketing. The current table provides a performance boost, as it is significantly smaller than the historical one, which only retains the latest changes. If users need historical analysis, they can refer to the historical table.

### Some of my thoughts

Regarding the inconsistency in how Type 4 is handled, I asked for help on [Reddit](https://www.reddit.com/r/dataengineering/comments/1mm9e5d/im_confused_about_the_scd_type_4_and_i_need_help/) and [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7360163438980968449/), and it appears that there is no official reason for this. However, a Reddit member said one thing that makes sense to me:

> *In the end, these are just labels (type n). Do what works for your requirements, and don't worry about the naming — [source](https://www.reddit.com/r/dataengineering/comments/1mm9e5d/comment/n81m5ih/)*

At first, I obsessed over finding the correct approach; then, I soon realized, as the Reddit member said, that they’re just labels.

That’s why I listed both approaches here, because that’s how I see this type. You may not find the SCD type 4 explanation in this format elsewhere, as most Internet resources tend to follow approach B. However, to me:

* I already notice the difference in this type’s definition.
* I can’t explain why that is
* I can’t ignore one of them, as I believe they could best fit specific scenarios.

Perhaps I don’t know the whole story or understand it completely. If you’re interested, feel free to discuss, leave a comment, or DM me. I am sure that some of you will be confused as I am.

## A break

Let’s take a break for a bit and summarize what we’ve learned here. All the above types are the basic ones; the first overwrites the data, while the following two types track changes by adding new rows and columns. Type 2 is the dominant one, thanks to its straightforwardness and the ability to keep history as long as we want, without changing the schema.

The following types, from 5 to 7, are categorized as the hybrid approaches as they are implemented by combining the basic types. I will briefly discuss them, as I don’t think these types are widely adopted in real life.

## Type 5: Mini-Dimension and Type 1 Outrigger

Type 5 combines **Type 4 (approach A)** with **Type 1 (Overwrite)**. The primary goal is to enable historical analysis of a group of attributes while also providing an easy way to access the current value of those attributes without joining a separate table.

The base dimension table will contain the reference key that points to the view or table presenting the latest changes of the mini-dimension table.

[![](https://substackcdn.com/image/fetch/$s_!sXsc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F518549bc-2413-41c7-8ac7-e6dc62976948_872x502.png)](https://substackcdn.com/image/fetch/$s_!sXsc!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F518549bc-2413-41c7-8ac7-e6dc62976948_872x502.png)

I will refer to the example straight from the Data Warehouse Toolkit book: Imagine we have a `Customer` dimension table and a separate `Demographic Mini-Dimension` table that holds information such as income and age. In type 4, the fact rows require two foreign keys that point to both `Customer` and `Demographic Mini-Dimension`.

In some cases, users only need the latest changes in the mini dimensions tables; the type 4 requires the fact table to be joined to both `Customer` and `Demographic Mini-Dimension` to achieve that. Type 5 addresses this by adding a Type 1 outrigger to the base Customer dimension. This outrigger is simply a set of columns (or a single foreign key) that points to the current change in the `Demographic Mini-Dimension`.

Whenever a customer's demographic profile changes, we add a new row in the Demographic Mini-Dimension (Type 4) and also overwrite the outrigger columns in the Customer table with the new values (Type 1). This allows for a quick lookup of current values directly from the Customer table.

## Type 6: Type 1 + Type 2 + Type 3

> *The `Type 6` was suggested for this approach because both the sum and product of 1,2,3 equal 6.*

Type 6 is a hybrid of **Type 1 (Overwrite), Type 2 (New Row)**, and **Type 3 (Previous Value)**. This technique stores the full history of a dimension in separate rows (Type 2) but also includes columns in each row that hold both the original value, the current value, and the "as-was" value from when the record was created.

This allows for both historical and current analysis within a single table.

Imagine an `Employee` dimension table where employees change departments. With a Type 6 approach, when an employee changes departments, a new row (**Type 2**) is created for that employee.

[![](https://substackcdn.com/image/fetch/$s_!wqvI!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa1b52c47-8f67-4dbe-b69d-fd8effa379ec_1116x600.png)](https://substackcdn.com/image/fetch/$s_!wqvI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa1b52c47-8f67-4dbe-b69d-fd8effa379ec_1116x600.png)

The old row is closed out with an end date. Both the old and new rows will have a column for the Current Department and the Historical Department. The Current Department column on all rows for that employee's history is overwritten (**Type 1**) with the new department name.

This allows a user to query historical sales and view the department to which the employee was assigned at that time (using the Historical Department column) and their current department (using the Current Department column).

## Type 7: Dual Type 1 and Type 2 Dimensions

This type is a variant of type 6. The table is now divided into two parts: history and current. The dimension table now contains a surrogate key for each unique row version and a [durable key (it could be a natural key if it’s durable)](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/natural-durable-supernatural-key/) that uniquely identifies the entity (e.g., an employee).

[![](https://substackcdn.com/image/fetch/$s_!oVXr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f196266-9c97-4aa8-922e-e436b73ba4fb_814x640.png)](https://substackcdn.com/image/fetch/$s_!oVXr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f196266-9c97-4aa8-922e-e436b73ba4fb_814x640.png)

The surrogate key is different for any new rows; however, the durable key is never changed for the same entity. Type 6 is still being implemented here; however, the columns to track current values will be managed in the current table.

---

## Outro

In this article, we revisit the basics of dimensional data modeling, which include fact and dimension tables. Then we learn that, to manage and align with what happens in the real world, there must be ways to handle changes in dimension tables.

We then explore some techniques guided by Kimball for this purpose: overwriting records (type 1), adding new rows (type 2), adding new columns (type 3), the confused type 4 (mini-dimension / current+history table), the type 5 that combined type 4 and 1, the type 6 is a mix of type 1, 2, 3 and finally, type 7 with

Based on my experience and research, type 2 is the most widely adopted one, thanks to its capability to retain the whole history of changes, and it does not require modifying the table’s schema. Saying that does not mean others are useless; there surely are some cases where those types will fit better than type 2. The key is knowing what works best for your needs.

Thank you for reading this far. See you next time.

---

## Reference

*[1] Ralph Kimball, Margy Ross, [The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling](https://www.amazon.com/Data-Warehouse-Toolkit-Definitive-Dimensional/dp/1118530802) (3rd Edition)*
