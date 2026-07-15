---
persona: vutr
kind: concept
sources:
- raw/clickhouse-internals/how-clickhouse-built-their-internal.md
last_updated: '2026-07-15'
qc: passed
slug: clickhouse-internal-data-warehouse-case-study
topics:
- clickhouse-internals
---

After launching ClickHouse Cloud in May 2022, the ClickHouse team needed to understand how customers actually used the product — usage patterns, pain points, pricing — and had been doing that analysis manually in Excel beforehand. They built an internal data warehouse with ClickHouse Cloud itself at the core, explicitly as a way to understand their own product from a customer's perspective.

**First-stage stack:** Airflow as the scheduler, AWS S3 as the intermediate data layer, Superset as the BI tool and SQL interface, and ClickHouse Cloud as the database and processing engine. Data sources spanned four groups: infrastructure/service cost and usage (AWS CUR, GCP Billing, AWS/GCP public prices), database and system metrics (Control Plane metadata, Data Plane system metrics, Galaxy observability events), customer and billing information (Salesforce CRM, M3ter billing), and marketing/event data (Segment, Marketo).

**Flow:** large fact tables are collected incrementally every hour; tables with updated existing records instead get a full-table snapshot every hour. Hourly data lands in S3 and is imported into ClickHouse via the ClickHouse S3 table function (a table-like interface for reading/writing S3 or GCS files directly). Data is first inserted into a **raw layer** preserving the source tables' structure, transformed with the help of Airflow-orchestrated ClickHouse queries, and written into **mart tables** representing business entities for internal stakeholders. Many temporary tables sit between raw and mart during transformation: transformed data first lands in a **staging table** (uniquely named per Airflow DAG run, allowing reuse) before being inserted into the target table.

**Idempotency and consistency** were solved with mechanisms native to ClickHouse itself rather than external tooling: tables use **ReplicatedReplacingMergeTree**, which keeps only the latest record per key, so the same hour's data can be inserted multiple times (as Airflow retries do) without duplication; and because ClickHouse's default eventual consistency could otherwise let a downstream step read a partially-replicated staging write, they use `insert_quorum=n` to force full replication before an insert reports success (see [[clickhouse-insert-process-and-idempotency]] for the general mechanism).

**Infrastructure:** the whole stack runs in Docker containers — separate machines for the Airflow web server, Airflow worker, and Superset. A container on the Airflow machines syncs the DAG-code/ELT-query/config repository to local machines every 5 seconds. Airflow and Superset share a Redis instance (execution state for Airflow, cached query results for Superset) and use AWS RDS for PostgreSQL as their internal database. Two fully independent environments — Preprod and Prod — each run their own ClickHouse Cloud, Airflow, and Superset, with Preprod kept consistent enough to serve as a failover if Prod becomes unavailable. The development flow is a standard branch → PR-to-Preprod → review/test-in-Preprod → PR-to-Prod pipeline. DAGs are split by design: separate DAGs load each source into S3 (e.g. M3ter → S3), while a single main DAG handles all transformation once data lands in S3, with dependencies declared within its tasks.

**Enhancement over time:** as data sources grew from 11 to 19 over a year, the original Airflow-orchestrated, hand-managed transformation approach became unsustainable for the growing number of complex business metrics and stakeholders, so the team adopted **dbt** to centralize transformation logic for batch reporting. Separately, user feedback pushed them to expose more real-time data sources in both raw and transformed form — ClickHouse's native format/library support made raw real-time exploration convenient enough that users could run SQL analysis without direct data-engineer support. dbt-defined aggregations over real-time data (also configurable in ClickHouse via materialized views) are joined with existing batch reports to enrich metrics such as "number of customers with failed queries" — combining batch-processed reporting and real-time streams in one warehouse.

**Consumption evolved too:** initially Superset's SQL client was the only way to query the warehouse, but its bugs hurt the user experience, so the team gave users direct access via ClickHouse Cloud's native SQL console instead, which users found superior for ad-hoc queries and exploration. GrowthBook was integrated directly against ClickHouse Cloud to let users run A/B tests on raw, log-level data. And a data-export job pushes warehouse data from ClickHouse Cloud into an S3 bucket that Salesforce queries, giving the sales team direct DWH access inside the CRM.

*See also: [[clickhouse-insert-process-and-idempotency]] · [[mergetree-storage-engine]] · [[clickhouse]]*
