---
title: "My Uncensored Guide To Saving on Cloud Data Warehouse Costs"
channel: vutr
author: "Vu Trinh"
published: 2025-01-16
url: https://vutr.substack.com/p/saving-cloud-data-warehouse-cost
paid: false
topics: ["Data Engineering", "Snowflake", "Databricks", "BigQuery", "Data Modeling", "Data Warehouse", "Data Quality"]
tags: [https, cloud, they, warehouse, auto, some]
---

# My Uncensored Guide To Saving on Cloud Data Warehouse Costs

*If you follow and burn your billing, it's not my fault. *

> Source: [Open post](https://vutr.substack.com/p/saving-cloud-data-warehouse-cost)

## Topics

[[data-engineering|Data Engineering]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[bigquery|BigQuery]] · [[data-modeling|Data Modeling]] · [[data-warehouse|Data Warehouse]] · [[data-quality|Data Quality]]

---

> *I'm offering **an** **exclusive** **sponsorship slot** **in each issue** to keep this newsletter free for readers. If you want to feature your product in my newsletter, explore my media kit:*
>
> [View Media Kit & Sponsor Now](https://vutr.substack.com/p/media-kit)

> *I’m making my life less dull by spending time learning and researching “how it works“ in the data engineering field.*
>
> *Here is a place where I share everything I’ve learned.*
>
> *Not subscribe yet? Here you go:*
>
> [Subscribe now](https://vutr.substack.com/subscribe?)

[![](https://substackcdn.com/image/fetch/$s_!JdDK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F594da20a-6c70-4fea-91a3-37ce8c37abd2_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!JdDK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F594da20a-6c70-4fea-91a3-37ce8c37abd2_2000x1429.png)

Image created by the author.

---

## Intro

On the last day of 2024, I accidentally came across an article on the Medium Engineering blog about how they were significantly [reducing Snowflake's costs](https://medium.engineering/learnings-from-optimising-22-of-our-most-expensive-snowflake-pipelines-5ea6fcf57356).

It's an excellent article.

You won't find any sublime tricks.

These are simple practices, but they help Medium reduce costs to the point that they are spending less than the credit it committed to Snowflake.

Things don't need to be complicated to be effective.

This insight urges me to reflect on my experience working with cloud data warehousing services (in my case, BigQuery) and my journey of self-learning other solutions, such as Snowflake or Databricks.

I think writing a short article about my observations would be helpful. The text you will read is not specific to any data warehouse service. Instead, I will try to note some bullet points that can be applied broadly, no matter which service you use.

---

## The case at Medium

[![](https://substackcdn.com/image/fetch/$s_!Ee3Q!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fea5a8196-196b-4316-bc00-e56d5bbb0c54_1038x652.png)](https://substackcdn.com/image/fetch/$s_!Ee3Q!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fea5a8196-196b-4316-bc00-e56d5bbb0c54_1038x652.png)

Image created by the author.

The 2010s witnessed the emergence of the cloud-native shared-disk architecture OLAP system with pioneers like Google BigQuery (2010) and Snowflake (2012).

These innovations provide organizations with the opportunity they never had before: The ability to access modern, cloud-native OLAP systems with cutting-edge technology and reasonable pricing models.

This was indeed an attractive offer, given that organizations had to invest in servers and software licenses to acquire OLAP capabilities in the past.

The customers need a few clicks on the UI, and their tailored data warehouse will be up and running.

"You will use the resource you need, and we will charge you based on that."

This implies a vital fact: to keep the cost of a cloud data warehouse (or any cloud services) low, we must use cloud resources efficiently.

Back to the case at Medium, to reduce Snowflake's costs, they found a few wasteful points:

* Pipelines that cost them thousands of dollars a month but barely support any use cases.
* Columns are barely used.
* Some pipelines run more frequently than they need.
* Although they embrace data partitioning practices, some use cases might fail to leverage them because they confuse the system about whether it needs to prune a partition. It scans the whole table (e.g., the filter clause for the partition column is too complicated).
* Some queries can scan shorter time windows without reducing the business value.
* Some queries can run a bit slower and don't affect the business.

So, how did they resolve these problems? They cleaned what they didn't need, adjusted the queries to ensure they benefited from the data layout, adjusted some queries' schedulers, and used a smaller Snowflake warehouse size for some queries.

Very straightforward

The ultimate goal is to use resources more and more efficiently.

---

## So, how about us?

We might work in companies with a more humble data scale than big tech companies such as Medium. Still, the desire to keep cloud data warehouse costs reasonable is always there, no matter how "big" the company's data is.

No one wants to spend more than the actual value we get.

Here is the catch: cloud data warehouse vendors also want the same.

They want us to use their services efficiently. They write public content on best practices to work with the service and encourage us to follow along.

Most cloud data warehouses are composed of giant storage with a bunch of workers on top of it; they are the same if you're trying to observe them from the moon :)

Thus, I believe some high-level practices can be applied to most systems. Here are some that I observed.

### Storage

[![](https://substackcdn.com/image/fetch/$s_!D77x!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F60a61953-eed2-4e6b-910b-feb51ab30e35_1576x1000.png)](https://substackcdn.com/image/fetch/$s_!D77x!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F60a61953-eed2-4e6b-910b-feb51ab30e35_1576x1000.png)

Image created by the author.

Your storage bills will correlate with the amount of the data you store. Let's break it down:

* How much data you store: The more data you store, the higher the cost. Only store what you need and clean up things you don't touch anymore. Most cloud data warehouses support automatically expiring data assets after an interval or on a specific schedule.
* How long do you store the data? Depending on your company's requirements, some data from 2 or 5 years ago might barely bring value and be less frequently accessed. You can consider offloading data to lower-cost storage classes based on your company's needs. For example, BigQuery supports automatically offloading data in long-term storage (lower cost than active storage) when the data has not been modified for 90 consecutive days. A point you can keep an eye on is how long you want to spend time traveling your data. Cloud data warehouse keeps the table's snapshot history for some time to let the user query the table in the previous state. You can control how long you want to keep the history. The longer the history, the more cost, but it gives you the ability to further time-travel, while the shorter period will save you money but put more limitations on how far you can time-travel.
* Compression: In most cases, data is compressed before being physically written for cloud data warehouse storage. Some let users choose the compress scheme; if you used Snowflake or Redshift, select the scheme that best fits your data. A note here is that there is no free lunch here; there will be a trade-off between size-reducing and decompressing CPU overhead. BigQuery, in contrast, does not let users choose the custom scheme; however, it lets them decide where they should be charged for the data before or after compressing (logical vs physical pricing model)
* Immutable files and columnar format: cloud data warehouse writes data in immutable files; once written, the files can not be overwritten; the only way to update/delete data is by writing the delta into the new files. In addition, data is written in a columnar fashion (hybrid format indeed) where values in the same columns are stored close to each other. These two insights imply that they're not optimized for point look-up operations. Batching data for DML operations is encouraged in most cloud data warehouses.
* The choice between denormalized and normalized data. The denormalization will incur data redundancy but can help boost the query performance, while normalization reduces redundancy (thus, storage cost) but requires more "join." Most cloud data warehouses support nested and repeated fields, which can help facilitate data normalization efficiently. Knowing these techniques' trade-offs and choosing them based on your needs.
* Organized data is beneficial for later retrieval: most cloud data warehouses support techniques to optimize physical data layouts, such as partitioning (splitting a table into smaller portions), clustering (bringing related column values close together), or compacting small files. Use these options wisely; although it can help you query faster, the system will suffer lower ingestion performance (blindly writing data will be faster than clustering and writing data). Moreover, the system might handle more metadata (e.g., partition metadata) or take more resources for background optimization tasks (e.g., compacting tasks.).

### Compute

[![](https://substackcdn.com/image/fetch/$s_!BA0u!,w_2400,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe76ba2c1-6f30-4952-a0e0-b7a6b3f3d64c_1350x728.png)](https://substackcdn.com/image/fetch/$s_!BA0u!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe76ba2c1-6f30-4952-a0e0-b7a6b3f3d64c_1350x728.png)

Image created by the author.

The warehouse compute bill will generally correlate with the CPU/RAM resources. You might not work directly with CPU or RAM; the vendor will abstract low-level hardware resources with different abstractions (e.g., slot from BigQuery or warehouse size from Snowflake). Here are my observations:

* First, know your cloud data warehouse pricing model. Will your vendor charge you based on an on-demand model, or will they let you commit to the resource beforehand? Vendors have tools to help you estimate your workload and plan your resources. Always plan what you will use (that doesn't need to be super accurate)
* Actively limiting the selected data. One typical way to boost an OLAP system's performance is to limit the data scan as much as possible. Although these systems have advanced techniques for this purpose, limiting the data scan from the client side is highly recommended: avoid selecting \* and selecting the column you need.
* Also, the data must be limited for intermediate processing by using the where clause, materializing CTEs or views if they need to be refereed frequently, or restricting data before joining (filters or aggregations)
* OLAP systems are not optimized for point queries; batching DML is recommended.
* Leverage the vendor's optimization techniques efficiently. Some options are Clustering, Partitioning, Primary/Foreign Key Optimization, etc. You must understand your data to choose appropriate techniques (or don't choose anything) because there is no free lunch here; you can't apply all the available options and hope your query will magically run faster. In addition, make sure to meet the conditions the optimization will affect; for example, BigQuery partition pruning requires the filters not to be too complicated, and clustering requires clustered columns to be filtered in defined orders. It’s not rare when you partition your data, but the query still can the full table although you filter on the partition column :)
* Use vendors' profiling/observability tools to understand your workload, which queries are slow, and which ones consume all the resources.

---

## Outro

Above are my notes after a few years of working with BigQuery and self-learning other services such as Snowflake and Databricks. Although you will need to spend more time on each service’s guidelines to operate your warehouse efficiently, I hope my notes will give you a starting point.

Before saying goodbye, I want to share some random thoughts recently when I spent more time learning data modeling.

—

At the end of the day, a cloud data warehouse is ... a data warehouse.

It must allow the data professionals to execute analytics workload seamlessly and efficiently.

The way we organize the data in the data warehouse is essential.

Data modeling should be the first-class citizen.

The resource availability of the cloud data warehouse tends to make customers care less about this factor.

"Let's put our data into Databricks and throw more resources if needed."

This contrasts with what I read, in which the data modeler spent months carefully designing the data model to adapt to the resource's expense in the past when servers needed to be bought beforehand and disks were not as cheap as they are today. Based on Joe Reis, the co-author of the Fundamental of Data Engineering, [the data model is](https://joereis.substack.com/p/my-definition-of-data-modeling-for):

> *a structured representation that organizes and standardizes data to enable and guide human and machine behavior, inform decision-making, and facilitate actions.*

With careful design, I believe data modeling can guide us in many points I mentioned above in the Storage and Compute section:

* It guides us in collecting data based on requirements, allowing us to estimate how much data we store.
* It guides us when to normalize or demalize a specific table.
* It guides us in consuming data. For example, to check out the total sales in Vietnam, you must join the sale fact table with the country dimension. Knowing query patterns can help us leverage vendor optimization techniques.
* It enforces contrast, which can help us implement the data quality processes more efficiently.
* …

Since starting my career in 2019, I have witnessed the chaos of operating a cloud data warehouse.

I wonder if this is due to our belittling of data modeling compared to the past.

Would love to hear your thoughts on this.

—

Thank you for reading this far.

See you on my next pieces.

---

## Reference

[1] Raphael Montaud, [Learnings from optimising 22 of our most expensive Snowflake pipelines](https://medium.engineering/learnings-from-optimising-22-of-our-most-expensive-snowflake-pipelines-5ea6fcf57356) (2024)

---

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
