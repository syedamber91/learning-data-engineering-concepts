---
title: "The History of Data Engineering"
channel: vutr
author: "Vu Trinh"
published: 2025-01-04
url: https://vutr.substack.com/p/the-history-of-data-engineering
paid: false
topics: ["Data Engineering", "dbt", "Apache Airflow", "Apache Kafka", "Apache Spark", "Apache Iceberg", "Apache Flink", "Snowflake", "Databricks", "Delta Lake", "BigQuery", "Data Warehouse", "Data Lake", "Lakehouse", "Orchestration", "Streaming", "Data Quality", "Data Governance", "ETL"]
tags: [https, auto, warehouse, image, analytics, media]
---

# The History of Data Engineering

*The most comprehensive one you've ever found on the internet*

> Source: [Open post](https://vutr.substack.com/p/the-history-of-data-engineering)

## Topics

[[data-engineering|Data Engineering]] · [[dbt|dbt]] · [[apache-airflow|Apache Airflow]] · [[apache-kafka|Apache Kafka]] · [[apache-spark|Apache Spark]] · [[apache-iceberg|Apache Iceberg]] · [[apache-flink|Apache Flink]] · [[snowflake|Snowflake]] · [[databricks|Databricks]] · [[delta-lake|Delta Lake]] · [[bigquery|BigQuery]] · [[data-warehouse|Data Warehouse]] · [[data-lake|Data Lake]] · [[lakehouse|Lakehouse]] · [[orchestration|Orchestration]] · [[streaming|Streaming]] · [[data-quality|Data Quality]] · [[data-governance|Data Governance]] · [[etl|ETL]]

---

> *I invite you to join my paid membership list to read this writing and 150+ high-quality data engineering articles:*
>
> [Upgrade subscription](https://vutr.substack.com/subscribe)
>
> * *If that price isn’t affordable for you, check this [DISCOUNT](https://vutr.substack.com/subscribe?coupon=c08a9839)*
> * *If you’re a student with an education email, use this [DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)*
> * *You can also claim this post for free (one post only).*
> * *Or take the [7-day trial](https://vutr.substack.com/7d8f19f0) to get a feel for what you’ll be reading.*

[![](https://substackcdn.com/image/fetch/$s_!8TZ5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F98206b96-55f2-402b-b88f-c72003163ee1_2000x1429.png)](https://substackcdn.com/image/fetch/$s_!8TZ5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F98206b96-55f2-402b-b88f-c72003163ee1_2000x1429.png)

Image created by the author.

---

## **Intro**

Have you ever wondered about the history of our field?

What drives us to sit before screens, debug data pipelines, or investigate data discrepancies? (Just kidding)

This week, we delve into the evolution of data engineering, tracing from the invention of relational databases.

---

### 1970s: Relational database

[![](https://substackcdn.com/image/fetch/$s_!L_-n!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa6a114e4-5a78-4d1e-8c25-791034b6ee0a_1052x660.png)](https://substackcdn.com/image/fetch/$s_!L_-n!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa6a114e4-5a78-4d1e-8c25-791034b6ee0a_1052x660.png)

Image created by the author.

In 1970, Edgar F. Codd defined the term "relational database model" in the "A Relational Model of Data for Large Shared Data Banks" paper.

Data is organized into structured tables. Each table represents a specific type of entity, such as 'users' or 'orders,' with rows (tuples) representing individual records and columns (attributes) defining properties of those records, like name, age, or order date.

Codd’s work eventually led to the creation of Structured Query Language (**SQL**) and the development of the first relational databases.

In 1974, IBM began developing System R, a prototype relational database management system (RDBMS) that introduced SQL as its query language.

Shortly after, Ingres, developed at the University of California, Berkeley, laid the foundation for many modern database systems.

Postgres (Post Ingres) was a project that started in the mid-1980s and later evolved into PostgreSQL.

Commercial RDBMS products began to emerge, including Oracle Database, which was released in 1979 by Larry Ellison and his team.

These developments made it easier for organizations to manage and query structured data, setting the stage for the widespread adoption of databases.

In the early days, databases were mainly used to record application transactions.

There are some realizations that there is a need for a separate system for business reports.

In the early 1970s, market research and television ratings magnate AC Nielsen offered clients a “data mart” to support sales operations.

Also, in the 1970s, Bill Inmon began discussing the Data Warehouse principles.

---

### 1980s: The beginning of the data warehouse

[![](https://substackcdn.com/image/fetch/$s_!wlY2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbec7b0cc-dcbb-41e9-85eb-cf2fd31a4e31_856x548.png)](https://substackcdn.com/image/fetch/$s_!wlY2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbec7b0cc-dcbb-41e9-85eb-cf2fd31a4e31_856x548.png)

Image created by the author.

The need for a centralized data repository to serve analytics requirements became evident.

In 1988, while working at IBM, Barry Devlin and Paul Murphy introduced the term "business data warehouse" in the article "An Architecture for a Business and Information System." They outlined a system for consolidating data from disparate sources for analytical purposes.

Bill Inmon worked extensively as a data professional from the late 1970s into the 1980s. In the late 1980s, he developed the notion of data warehouses, which he described as *"a subject-oriented, integrated, nonvolatile, and time-variant collection of data in support of management's decisions."*

Bill Inmon was also involved in the origin of ETL (Extract, Transform, Load)

In the early days, data was manually moved to the warehouse by writing programs to access the data source, find the required data, transform it, and load it into a data warehouse.

He discovered that building these programs was very time-consuming and onerous. He and his colleagues might have repeated the logic in the ETL scripts.

That's why they realized automated technologies are needed to facilitate the ETL process.

The late 1980s saw the introduction of automated ETL tools like Informatica and IBM DataStage, which revolutionized data integration workflows. By the 1990s, tools like Cognos and Microsoft SSIS enhanced these capabilities, providing scalable, user-friendly platforms for managing complex data transformations.

---

### 1990s: The Golden Age of Data Warehousing

[![](https://substackcdn.com/image/fetch/$s_!cyM-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff1ac588f-ade9-4e7d-be87-842ff40497c6_970x646.png)](https://substackcdn.com/image/fetch/$s_!cyM-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff1ac588f-ade9-4e7d-be87-842ff40497c6_970x646.png)

Image created by the author.

The 1990s marked the golden age of data warehousing.

In 1991, Bill Inmon founded Prism Solutions and introduced Prism Warehouse Manager, software for developing a data warehouse.

In 1992, he popularized best practices for building enterprise data warehouses by publishing the book Building the Data Warehouse.

In 1996, Ralph Kimball published the book The Data Warehouse Toolkit, which set the foundations of dimensional modeling.

The Kimball and Inmon approach to data warehousing differ in methodology and focus. Inmon follows a top-down design, first building a centralized enterprise data warehouse that serves as the single source of truth. Kimball emphasizes a bottom-up design, creating data marts for specific business processes later integrated into a comprehensive data warehouse.

With the rise of the data warehouse, people started to pay attention to the analytics workload.

This time, most of the database is designed for the transaction workload (e.g., row-stored), and it was not efficient for the analytics ones (e.g., need to fetch an entire row to read a subset of columns)

To optimize the analytics workload on the row-oriented database, people started building things called Data Cubes as pre-compute aggregation to speed up the queries, which needed to be specified beforehand and refreshed periodically. The analytics query will try to hit the Cube instead of the raw data to get the result.

---

### 2000s: The Big Yellow Elephant

[![](https://substackcdn.com/image/fetch/$s_!fqq6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb6b91766-95cc-4bf2-b761-16315a034bfa_1366x898.png)](https://substackcdn.com/image/fetch/$s_!fqq6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb6b91766-95cc-4bf2-b761-16315a034bfa_1366x898.png)

Image created by the author.

Big tech companies that survived the DotCom bubble in the early 2000s, such as Yahoo, Google, and Amazon, pioneered working with Big Data. Traditional data warehousing architectures struggled with the internet's scale of data growth in both volumes and formats.

Google released a paper to introduce [their giant file system](https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf) in 2003.

Following that is a paper about their famous [MapReduce programming model](https://static.googleusercontent.com/media/research.google.com/en//archive/mapreduce-osdi04.pdf) to process large amounts of data in 2004.

Doug Cutting and Mike Cafarella developed the Hadoop MapReduce and HDFS based on these two papers. Both were first developed under the Nutch (web crawler) project but moved to the new Hadoop subproject in January 2006.

Also, in 2006, Yahoo! adopted Apache Hadoop for its WebMap application.

Cloudera was founded in 2008, and HortonWorks started in 2011. They were the first companies to offer managed Hadoop services.

The birth of Hadoop (especially HDFS) and the practice of big tech companies (Google, Yahoo,...) fueled the trend of gathering data in raw format in a central repository without pre-transformation.

This time also witnessed the emergence of a relational database designed explicitly for OLAP workloads (column store) with share-nothing architecture (compute and storage tied together). Some databases that can be listed are Netezza, Paraccel (later back to Amazon Redshift), MonetDB, or Vertica.

In addition, NoSQL databases like Google BigTable (2004), Cassandra (2008), and HBase (2007) emerged to handle unstructured and semi-structured data, offering flexibility and scalability.

Also, the famous object storage from AWS S3 was launched in 2006.

---

> *I invite you to join my paid membership list to read this writing and 150+ high-quality data engineering articles:*
>
> [Upgrade subscription](https://vutr.substack.com/subscribe)
>
> * *If that price isn’t affordable for you, check this [DISCOUNT](https://vutr.substack.com/subscribe?coupon=c08a9839)*
> * *If you’re a student with an education email, use this [DISCOUNT](https://vutr.substack.com/subscribe?coupon=0b37c676)*
> * *You can also claim this post for free (one post only).*
> * *Or take the [7-day trial](https://vutr.substack.com/7d8f19f0) to get a feel for what you’ll be reading.*

---

### 2010s: The data engineers

[![](https://substackcdn.com/image/fetch/$s_!Gpsf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1aa87461-8269-4cab-b54f-5cf75f5f885a_1368x918.png)](https://substackcdn.com/image/fetch/$s_!Gpsf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1aa87461-8269-4cab-b54f-5cf75f5f885a_1368x918.png)

Image created by the author.

Although the idea of gathering all data in raw format in a central repository has existed for some time, in 2011, James Dixon, then chief technology officer at Pentaho, officially [coined the term "data lake."](https://en.wikipedia.org/wiki/Data_lake)

In the mid-2010s, many organizations tried to bypass the traditional relational data warehouse and use the data lake for all data use cases.

Facebook developed [Apache Hive in 2010](https://en.wikipedia.org/wiki/Apache_Hive) to add SQL abstraction over MapReduce. This allows for querying and analyzing data stored in databases and file systems that integrate with Hadoop. Later, Netflix also used Hive for its data warehouse architecture.

However, with this data-lake-only architecture, if it was not carefully managed, the data lake soon became a swamp due to the lack of proper data management features from the warehouse, such as data discovery, data quality and integrity guarantee, ACID constraints, and data DML support…

A two-tier architecture, in which data must be gathered in the data lake, and a subset is transformed and loaded into the data warehouse, can combine the best of both worlds.

Data-driven tech companies like Facebook and Airbnb started using the phrase "data engineer." In 2017, Maxime Beauchemin, the founder of Preset and the creator of Superset and Airflows, [released an insightful article on the emergence of data engineers](https://medium.com/free-code-camp/the-rise-of-the-data-engineer-91be18f1e603).

[This period also witnessed the downfall of Hadoop, whose market cratered in the 2010s](https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf). Many enterprises invest a lot of money in Hadoop clusters but can not all benefit from them. Developers always need to tailor the processing logic to the MapReduce paradigm. This left three leading Hadoop vendors (Cloudera, Hortonworks, and MapR) without a viable product to sell.

Cloudera rebranded Hadoop to mean the whole stack (application, Hadoop, HDFS). Moreover, Cloudera built an RDBMS called Impala on top of HDFS but did not leverage MapReduce. MapR built Drill directly on HDFS, and Meta created Presto to replace Hive. MapReduce did not back both.

Google announced that they moved their crawl processing from MapReduce to BigTable and finally announced in 2014 that MapReduce was no longer used in their technology stack.

In addition, The popularity of cloud services, especially cloud object storage such as [S3 (2006)](https://en.wikipedia.org/wiki/Amazon_S3) or [Google Cloud Storage (2010)](https://en.wikipedia.org/wiki/Google_Cloud_Storage), makes users wonder: If I could store my raw data in object storage with a pay-as-you-go pricing model and the guarantees of high scalability, availability, and durability, why do I need to buy servers and install/manage/operate the HDFS myself?

The 2010s also saw the birth of many other important data engineering technologies.

Apache Spark, first developed in 2009 and open-sourced in 2010 (<https://en.wikipedia.org/wiki/Apache_Spark>), further revolutionized data processing by offering a faster, more developer-friendly alternative to Hadoop’s MapReduce (logic doesn't need to be Map or Reduce). Its in-memory computation capabilities are ideal for iterative tasks like machine learning and real-time analytics. It started to gain popularity and gradually became the standard for data processing today.

Apache Paquet, a column-oriented file format designed for analytics workloads, was [released in 2013](https://en.wikipedia.org/wiki/Apache_Parquet). It was initially developed by Cloudera and Twitter. Since then, Parquet has become the dominant data storage format for analytics workloads. Parquet's ability to handle nested and repeated data is inspired by the approach of BigQuery's proprietary data format, Capacitor, which was first introduced in a paper about [Dremel in 2010](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/36632.pdf).

In 2014, [Airbnb started developing Airflow](https://en.wikipedia.org/wiki/Apache_Airflow), a workflow orchestration that standardized pipeline management. It allows engineers to easily define, schedule, and monitor workflows.

In 2017, AWS launched Glue, a cloud-native data integration service that helps customers develop ETL pipelines more seamlessly. AWS also leverages Spark for the ETL stack and has developed libraries and structures to help customers deal more efficiently with unstructured data.

Kafka, one of the most important technologies for the data landscape, was initially developed on LinkedIn and open-sourced in early 2011.

Flink, an accurate stream processing engine that allows for stateful stream processing, was also released in 2011. In the same year, Twitter's Apache Storm stream processing engine was open-sourced.

There is a niche where people realize a missing real-time analytics database. Apache Druid was developed in 2011 (by Metamarkets), and Apache Pinot was created in 2013 (by Linkedin) to serve real-time analytics workload. Yandex Metrica used Clickhouse in production in 2012 to provide real-time insights. ClickHouse later evolved to a more general analytics database and has been trusted by many companies.

Google also contributed significantly to this area by releasing two papers: the first (2013) described [MillWheel's](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/41378.pdf) internal stream processing, and the second (2015) described the [dataflow model](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/43864.pdf), an approach to balancing correctness, latency, and cost for unbounded data processing.

The 2010s also witnessed [the emergence of the cloud-native shared-disk architecture](https://youtu.be/5J-I8Mj8tss?list=PLSE8ODhjZXjYa_zX-KeMJui7pcN1rIaIJ) OLAP system with pioneers like Google BigQuery (2010) and Snowflake (2012). Essentially, the data is stored separately in object storage; on top of that will be the query engine. The vendor must still manage the storage layer, and the data in the storage must be in the system's proprietary format. (e.g., Capacitor format if you used BigQuery.)

Besides the paradigm-shifting (from share-nothing to shared-disk), this OLAP system also had more advanced query power processing; many workers can efficiently process and distribute data, and more importantly, users can benefit from this without needing to manage infrastructure. This also contributed to the shift from ETL to ETL when the user could keep the data source right in this system and transform it later. More storage is needed, but who cares? It is way cheaper than in the past.

Big tech companies continued to make efforts to bring data warehouse features, such as ACID, query optimization, or time traveling, to the data lake via a metadata layer on top of object storage or HDFS.

Databricks open-sourced [Delta Lake in 2019](https://venturebeat.com/ai/databricks-launches-delta-lake-an-open-source-data-lake-reliability-project/), Netflix started developing [Icebergs in 2017](https://en.wikipedia.org/wiki/Apache_Iceberg), and Uber began using [Hudi with HDFS in production in 2016](https://hudi.apache.org/docs/0.5.2/powered_by/#uber).

These innovations paved the way for Lakehouse architecture's emergence in the 2020s.

Data governance became a top priority with the introduction of regulations like GDPR in 2018. Organizations had to implement robust metadata management and compliance frameworks to ensure data privacy and security.

---

### 2020s: Lakehouse and more

[![](https://substackcdn.com/image/fetch/$s_!0Tvp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5d945850-ecc7-4706-b77f-2f9516afd0f4_1014x682.png)](https://substackcdn.com/image/fetch/$s_!0Tvp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5d945850-ecc7-4706-b77f-2f9516afd0f4_1014x682.png)

Image created by the author.

Cloud-native OLAP systems such as BigQuery, Redshift, Snowflake, or Databricks remain attractive options for people who want to build their warehouse solutions.

Vendors have continuously enhanced or added new services to help users manage their data more efficiently.

In 2022, Google added [Dataplex](https://cloud.google.com/dataplex/docs/release-notes#February_15_2022), a service that allows organizations to manage, monitor, and govern data centrally.

In 2023, Microsoft introduced [Microsoft Fabric](https://azure.microsoft.com/en-us/blog/introducing-microsoft-fabric-data-analytics-for-the-era-of-ai/), a unified analytics platform that combines all the data and analytics tools organizations need. (Imagin Azure Data Factory, Synapse Analytics, and Power BI into a single product)

Cloud vendors also focus on bringing AI and ML capabilities to their data warehouse solutions.

An important innovation at this time is the introduction of the lakehouse paradigm. In 2021, Databricks released a paper introducing this concept.

For the namesake, in Lakehouse architecture, people try to bring the data warehouse features right on top of the data lake. The lake can act as a single point for analytics access.

It is an architecture based on low-cost storage (with analytics-friendly file formats such as Parquet) with the enhancement of traditional analytical DBMS management and performance features such as ACID transactions, versioning, caching, and query optimization. The Lakehouse combines the best of both worlds.

The difference from the past effort, when people tried to bring processing right on top into the data lake, is that more efficient metadata layers were introduced. Databricks created Delta Lake, Netflix made Iceberge manage analytics data more efficiently on S3, and Uber developed Hudi to bring the capability of data upsert and incremental processing to the data lake.

Although the lakehouse's architecture is similar to the shared-disk architecture employed by cloud vendors, its openness makes it tempting.

The user now can have 100% control over their data in the object storage and which engine or tool they can use over this data. There is no hard-to-find evidence for the rise of Lakehouse:

* Most cloud data warehouses support working with Iceberg or Delta Lake data in object storage.
* In 2024, Databricks acquired Tabula, the Company Founded by the Original Creators of Apache Iceberg.
* Also, in 2024, Snowflake opened the Polaris Catalog for Iceberg, and Databricks opened the Unity Catalog.
* AWS released an S3 Table with built-in Apache Iceberg support and streamlined storing of tabular data at scale.
* ...

The 2020s also witnessed the popularity of modern data stacks such as FiveTrans, Airbyte, and especially dbt.

[Don't forget the semantic layer. Although it has existed for a while, it recently gained attention after being popularized by vendors such as LookerML (2019), CubeJS, and Airbnb Minerva.](https://airbyte.com/blog/the-rise-of-the-semantic-layer-metrics-on-the-fly)

The semantic layer is making a comeback because it helps solve some significant challenges in working with data. It creates a shared space where business teams and engineers can align on complex ideas and metrics, reducing. It’s also the go-to place for understanding where data comes from, making data lineage easier.

Decentralized data architectures, such as **data mesh**, began gaining traction. This approach emphasizes domain-oriented data ownership and empowers individual teams to manage their data as a product. Zhamak Dehghani introduced data mesh in 2019 and published a book in 2022 to provide more information about this approach. She also introduced the concept of a data product, a self-contained, discoverable, and reliable dataset designed to meet specific business or analytical needs. Big tech companies such as [Netflix have started to apply data mesh](https://netflixtechblog.com/data-movement-in-netflix-studio-via-data-mesh-3fddcceb1059).

There are more movements around the data engineering landscape worth mentioning, such as the trend of using Rust for data engineering tasks (it seems cooldown), the small data matter (DuckDB, Polars, etc.), or real-time analytics getting more adoptions (the birth of real-time analytics databases such as RisingWave, Materialized View, Pinot or Druid get more adoption or Confluent acquired Immerok to brings Apache Flink to the platform), and of course don't forget the GenAI advancements which could affect a lot to the data engineering landscape.

---

## Outro

Despite my bragging about the comprehensiveness of the article at the beginning, there is a high chance that I missed some points during my research process. So, if you find there is something to be added, feel free to let me know.

Looking back at the history of data engineering, it’s both tempting and exciting to speculate about what’s next. However, I think I’ll keep those predictions to myself.

One thing I’m certain of is that change will come quickly, and only the innovations that truly add value to the core goals of data engineering will stand the test of time.

—

I spent a lot of time researching and putting this article together, so if you found it valuable, feel free to give it a like or leave a comment to share your thoughts—whether you loved it or not!

Also, don’t forget to restack or share it to help this article reach more people. Your feedback, along with insights from other data experts, will help me improve and make this piece even better.

Thank you for reading this far.

Now, it's time to say goodbye. See you in my next articles.

---

## Reference

[1] Wikipedia, [Relational Database](https://en.wikipedia.org/wiki/Relational_database)

[2] Paul Williams, [A Short History of Data Warehousing](https://www.dataversity.net/a-short-history-of-data-warehousing/) (2012)

[3] Joe Reis, [Data Warehouse - Key Architectural Ideas, Data Storage and Queries Course](https://www.coursera.org/learn/data-storage-and-queries)

[4] Jesse Anderson, [Brief History of Data Engineering](https://www.jesse-anderson.com/2022/12/brief-history-of-data-engineering/) (2022)

[5] James Serra, [Deciphering Data Architectures: Choosing Between a Modern Data Warehouse, Data Fabric, Data Lakehouse, and Data Mesh](https://www.amazon.com/Deciphering-Data-Architectures-Warehouse-Lakehouse/dp/1098150767) (2024)

[6] Michael Stonebraker, Andy Pavlo, [What Goes Around Comes Around... And Around...](https://db.cs.cmu.edu/papers/2024/whatgoesaround-sigmodrec2024.pdf)

[7] Wikipedia, [Data engineering](https://en.wikipedia.org/wiki/Data_engineering)

---

It might take you five minutes to read, but it took me more than five days to prepare, so it would greatly motivate me if you considered subscribing to receive my writing.

[Subscribe now](https://vutr.substack.com/subscribe?)
