---
persona: vutr
kind: concept
sources:
- raw/dbt-and-dimensional-modeling/etl-and-elt.md
- raw/dbt-and-dimensional-modeling/why-is-dbt-so-popular.md
- raw/dbt-and-dimensional-modeling/how-to-learn-dbt-cheap-and-fast.md
last_updated: '2026-07-15'
qc: passed
slug: elt-vs-etl
topics:
- dbt
- history-of-data-engineering
---

ETL has existed since the 1970s, when data warehousing began, and it covers everything that happens between a data source (an operational database, a third-party API) and the warehouse: extract the needed data, transform it — cleaning, filtering, combining, reshaping to a target schema — and only then load it, already clean and structured, into the destination. Vu's point is that this ordering was not an aesthetic choice; it was forced by the economics of the era. Warehouse systems were expensive in both storage and processing, companies had to buy and provision their own servers and vendor licenses, disks were not cheap, networks were slow, and compute and storage were tightly coupled — scaling one meant scaling both. Columnar storage was not yet the norm, and row-oriented databases were poorly suited to analytics workloads. Given all of that, loading only a small, carefully curated subset made sense; raw data never touched the warehouse at all.

ETL's costs were the mirror image of its cause: setting up a pipeline demanded defining transformation logic up front, standing up and managing complex environments like Spark clusters, and going through a full code-test-deploy cycle — putting the whole process out of reach for anyone but a data engineer. Worse, because the source data was never preserved downstream, any change in business requirements meant going all the way back to the source system and re-running extract, transform, and load from scratch. The pipeline itself could become a bottleneck as data grew in volume and complexity.

ELT reverses the order — extract, *load*, then transform — and Vu is careful that this is not merely swapping two letters: it reflects a real shift in economics and architecture. The trigger was the rise of the cloud data warehouse: pay-as-you-go pricing, cheaper storage, faster networks, and columnar storage/processing as the default made a high-performance, cost-efficient warehouse a few clicks away rather than months of procurement. Once that was true, there was no longer a reason to transform data before loading it — you could dump it from the source with minimal processing and transform it later, directly inside the warehouse, using SQL.

The benefits Vu lists follow directly from what ETL was straining against: transformation logic now runs inside the warehouse using SQL, which is accessible to data analysts and data scientists, not just engineers, removing the DE-as-bottleneck failure mode. Keeping raw data in the warehouse means transformation logic can evolve as analytical needs change, instead of having to be fully specified up front — a real fit for agile-style iteration. And because the raw data itself is preserved, backfills and logic changes can be run against what's already sitting in the warehouse, without going back and re-burdening the source system — a form of isolation between the analytics layer and the systems of record. The one cost Vu names honestly is that storage grows, since you're keeping data you might once have discarded — but he treats that as a reasonable trade against everything ELT buys back.

He is explicit that this is not a story of ELT fully replacing ETL: there remain cases where ETL is still necessary, and he does not enumerate which ones. What he does commit to is a direction of travel — ELT will keep growing as the lakehouse paradigm brings warehouse-grade capability directly onto the data lake, cloud platforms increasingly let a warehouse query object storage directly, and open table formats (Hudi, Delta Lake, Iceberg) mature; he points to AWS's own S3 tabular-data storage type, built on Iceberg and Parquet, as one concrete sign of that direction. The same shift — cheap storage, powerful in-warehouse SQL, transformation moving from "outside" to "inside" — is also, in his account, the precondition for [[dbt]]'s rise: once transformation could happen in SQL inside the warehouse, a tool to manage that SQL transformation (test it, modularize it, document it) became necessary, and that tool was dbt.

*See also: [[dbt]] · [[dbt-origin-and-adoption]] · [[democratization-of-transformation]] · [[dimensional-modeling]] · [[star-schema]] · [[scd-type-2]] · [[scd-type-1-and-3]]*

## Open questions
- Which specific cases still make ETL necessary rather than ELT, now that transformation has largely moved inside the warehouse? Vu says such cases exist but does not name them.

## Related in the other wiki
- [[Data Warehousing]] — DDIA's ETL description (periodic dumps or continuous streams, reshaped and cleaned before loading) is the classic pattern Vu contrasts against ELT's load-then-transform reordering, and DDIA's own note that "ETL introduces its own freshness lag and pipeline maintenance burden" is the cost this concept's ELT era was built to remove.
