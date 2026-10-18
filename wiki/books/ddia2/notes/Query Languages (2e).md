---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 11
chapter_title: Batch Processing
topic: Batch Processing Models
type: subtopic
tags: [ddia2, sql, query-optimizer, trino, hive, pig, gremlin]
sources:
  - raw/ch11.md
---
# Query Languages
> With the physical problem of running batch jobs at scale more or less solved, attention turned to the programming model — and SQL won.

## The Idea
**Execution engines have matured: the infrastructure is now robust enough to store and process many petabytes on clusters of over 10,000 machines.** **With physically operating batch processes at that scale considered more or less solved, attention has turned to improving the programming model.**

**MapReduce, dataflow engines, and cloud data warehouses have all embraced SQL as the lingua franca for batch processing.** **It's a natural fit: legacy data warehouses used SQL, analytics and ETL tools already support it, and all developers and analysts know it.**

## How It Works
**Besides requiring less code than handwritten MapReduce jobs, query language interfaces allow interactive use** — writing analytical queries and running them from a terminal or GUI. **This is an efficient and natural way for business analysts, product managers, sales and finance teams, and others to explore data in a batch environment**, and **SQL support has made distributed batch systems suitable for exploratory queries.**

**High-level query languages don't just make humans more productive; they improve job execution efficiency at a machine level.** **Query engines convert SQL into batch jobs**, and **the translation from query to syntax tree to physical operators allows the engine to optimize.** **Engines such as Hive, Trino, Spark, and Flink have cost-based query optimizers that analyze the properties of join inputs and automatically decide which algorithm is most suitable** — **and may even change the order of joins so the amount of intermediate state is minimized.**

**Other languages remain in use for niche needs.** **Apache Pig** was a language based on relational operators letting pipelines be specified **step by step rather than as one big SQL query**; **DataFrames have similar characteristics, and Morel is a more modern language influenced by Pig.** **Other users adopt JSON query languages such as `jq`, JMESPath, or JSONPath.** **Many graph processing frameworks also support batch computation through query languages such as Apache TinkerPop's Gremlin.**

## Trade-offs & Pitfalls
> **Batch processing and cloud data warehouses converge.** **Historically warehouses ran on specialized hardware appliances supporting SQL over relational data**, while **batch frameworks like MapReduce set out to provide greater scalability and flexibility by supporting logic in a general-purpose language and arbitrary data formats.** **Over time the two have become much more similar.** **Modern batch frameworks support SQL and achieve good performance on relational queries using columnar formats such as Parquet and optimized execution engines**; **meanwhile warehouses have grown more scalable by moving to the cloud and implementing many of the same scheduling, fault tolerance, and shuffling techniques**, many using distributed filesystems as well. **And just as batch systems adopted SQL, cloud warehouses have adopted alternative processing models** — **BigQuery offers a DataFrames library, Snowflake's Snowpark integrates with Pandas**, and **Airflow, Prefect, and Dagster integrate with cloud warehouses.**
>
> **But not all batch jobs are easily expressed in SQL**, including **iterative graph algorithms such as PageRank, complex ML tasks, and AI data processing over nonrelational and multimodal data such as images, video, and audio.** **And cloud warehouses struggle with certain workloads too**: **row-by-row computation is less efficient with column-oriented storage**, and **warehouses tend to be more expensive — it can be more cost-efficient to run large jobs in Spark or Flink instead.**
>
> **Ultimately the decision often comes down to cost, convenience, ease of implementation, and availability.** **Most large enterprises have many data processing systems, giving them flexibility; smaller companies often get by with just one.**

## Examples & Systems
Hive, Trino, Spark, Flink (cost-based optimizers); Apache Pig and Morel; `jq`, JMESPath, JSONPath; Apache TinkerPop's Gremlin.

## Since the 1st Edition
The 1st edition covered "declarative query languages on MapReduce" briefly inside its MapReduce topic, mentioning Hive, Pig, Cascading, and Crunch, and made the point that declarative languages allow optimizer choice of join algorithm. **The 2nd edition promotes this to a full subtopic**, states that **SQL has become the lingua franca**, and adds the **batch-processing-and-warehouses-converge box** — including where each still struggles — which is a genuinely new architectural argument.

## Related
- up: [[Batch Processing Models (2e)]] · chapter: [[Ch 11 - Batch Processing (2e)]]
- [[Cloud Data Warehouses (2e)]] — the other half of the convergence
- [[DataFrames (2e)]] — the other high-level model
- [[Joins and Grouping (2e)]] — the algorithms optimizers now choose between
