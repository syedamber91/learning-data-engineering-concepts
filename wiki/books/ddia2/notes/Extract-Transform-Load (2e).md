---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 11
chapter_title: Batch Processing
topic: Batch Use Cases
type: subtopic
tags: [ddia2, etl, elt, airflow, data-mesh, data-contract, pipelines]
sources:
  - raw/ch11.md
---
# Extract–Transform–Load
> Embarrassingly parallel work, robust schedulers, and jobs you can inspect and rerun. ETL is what batch processing is best at.

## The Idea
**ETL and ELT extract data from a production database, transform it, and load the results into a downstream system.** **Batch jobs are often used for such workloads, especially when the downstream system is a data warehouse.**

## How It Works
**The parallel nature of batch jobs makes them a great fit for data transformation, much of which involves "embarrassingly parallel" workloads** — **filtering data, projecting fields, and many other common warehouse transformations can all be done in parallel.**

**Batch environments also come with robust workflow schedulers**, making it easy to **schedule, orchestrate, and debug ETL pipeline jobs.** **When a failure occurs, schedulers often retry to mitigate transient issues**, and **a job that fails repeatedly is marked as failed, helping developers see which job in their pipeline stopped working.** **Schedulers like Airflow even come with built-in source, sink, and query operators for MySQL, PostgreSQL, Snowflake, Spark, Flink, and dozens of other systems** — **a tight integration that simplifies data integration.**

**Batch jobs are also easy to troubleshoot and fix when things go awry, which is invaluable when debugging pipelines.** **Failed files can be inspected to see what went wrong, and jobs can be fixed and rerun.** **If an input file lacks a field a transformation intends to use, data engineers can easily spot that it's missing and update either the transformation logic or the job that produced the input.**

## Trade-offs & Pitfalls
- **Ownership has changed.** **Pipelines used to be managed by a single data engineering team, as it was considered unfair to ask product teams to write and manage complex batch pipelines.** **Recently, improvements in processing models and metadata management have made it much easier for engineers across an organization to contribute to and manage their own pipelines.** **Data mesh, data contract, and data fabric practices provide standards and tools to help teams safely publish their data for consumption by anybody in the organization.**
- **Pipelines and analytical queries now share not only processing models but execution engines.** **Many batch ETL jobs run on the same systems as the analytical queries reading their output** — **it is not uncommon to see both pipeline transformations and analytical queries run as SparkSQL, Trino, or DuckDB queries.** **Such an architecture further blurs the line between application engineering, data engineering, analytics engineering, and business analysis.**

## Examples & Systems
Airflow's built-in operators for MySQL, PostgreSQL, Snowflake, Spark, Flink; SparkSQL, Trino, DuckDB as shared execution engines; data mesh, data contracts, and data fabric as organisational practices.

## Since the 1st Edition
**New as a subtopic.** The 1st edition introduced ETL in its storage chapter and returned to it in the derived-data discussion, **but never treated it as a batch processing use case with its own operational characteristics.** **Data mesh, data contracts, and data fabric are all post-2017 practices** and appear here for the first time.

## Related
- up: [[Batch Use Cases (2e)]] · chapter: [[Ch 11 - Batch Processing (2e)]]
- [[Data Warehousing (2e)]] — where ETL is introduced
- [[Distributed Job Orchestration (2e)]] — the schedulers this relies on
- [[Analytics (2e)]] — what runs on the output
