---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 1
chapter_title: Trade-Offs in Data Systems Architecture
topic: Operational Versus Analytical Systems
type: subtopic
tags: [ddia2, data-warehouse, data-lake, etl, elt, htap]
sources:
  - raw/ch01.md
---
# Data Warehousing
> A separate, read-only copy of the whole company's data that analysts can hammer without touching production — and the thirty-year drift of that idea into lakes, pipelines, and reverse ETL.

## The Idea
At first the same database served both transaction processing and analytics; SQL is flexible enough for both. In the late 1980s and early 1990s companies began pulling analytics out into a separate system — the **data warehouse**. The motivation is concrete. A large enterprise may run dozens or hundreds of OLTP systems — the customer website, point-of-sale checkouts, warehouse inventory, vehicle routing, supplier management, HR — each complex, each with its own team, each operating largely independently. Querying them directly is undesirable because the data of interest is spread across several of them (**data silos**), because OLTP-friendly schemas suit analytics badly, because analytical queries are expensive enough to degrade production, and because those systems often sit in networks users are not permitted to reach for security or compliance reasons.

## How It Works
- The warehouse holds a **read-only copy** of data from all the OLTP systems. Getting it there is **extract–transform–load (ETL)**: extract via periodic dump or continuous update stream, transform into an analysis-friendly schema, clean it, load it. Swap the last two steps and you get **ELT**, where the transformation happens inside the warehouse after loading.
- Some sources are external SaaS products — CRM, email marketing, credit card processing — where you have no database access at all, only the vendor's API. Specialist connector services (Fivetran, Singer, Airbyte) exist for exactly this.
- **From warehouse to data lake.** A warehouse typically uses a relational model queried through SQL, which suits analysts but suits data scientists poorly: feature engineering for ML, NLP over review text, computer vision over photos — these need custom code that SQL expresses badly, and many data scientists prefer Pandas, scikit-learn, R, or Spark. The answer is a **data lake**: a centralised repository holding a copy of anything that might be useful, *without imposing a file format, data model, or schema*. It might hold Avro or Parquet record files, but equally text, images, video, sensor readings, sparse matrices, feature vectors, or genome sequences. It is also usually cheaper, because it can sit on commodity object storage.
- ETL processes generalised into **data pipelines**, and the lake often became an intermediate stop on the way to the warehouse — holding data in the raw form the operational systems produced, so each consumer transforms it their own way. This is sometimes called the **sushi principle**: raw data is better.
- **Beyond the lake.** Governance, privacy, and compliance (GDPR, CCPA) pushed attention onto how analytical systems are operated — the DataOps Manifesto is one expression of this. Analytical data increasingly arrives as **streams of events** rather than files and tables, letting analytics react in seconds rather than on a daily rerun, which matters for things like blocking fraudulent or abusive activity. And analytical output increasingly flows *back* into operational systems — **reverse ETL** — for example deploying a trained ML model to production to generate recommendations, via tools like TFX, Kubeflow, or MLflow.

## Trade-offs & Pitfalls
- **HTAP** (hybrid transactional/analytical processing) promises one system for both, no ETL. But many HTAP systems are internally an OLTP system coupled to a separate analytical system behind a shared interface, so the distinction still governs how they behave.
- HTAP does not replace warehouses, and the book is precise about why: good practice gives each operational system its own database, so an enterprise ends up with potentially hundreds of them — but only *one* warehouse, precisely so an analyst can join across operational systems in a single query. HTAP helps when one application needs both large scans and low-latency record updates; fraud detection is the example given.
- A lake's freedom from schema is also its hazard: nothing is imposed, so nothing is guaranteed.

## Examples & Systems
Fivetran, Singer, and Airbyte for SaaS-API ETL; Avro and Parquet as lake file formats; Pandas, scikit-learn, R, and Spark as the data-scientist toolchain; TFX, Kubeflow, and MLflow for pushing models into production.

## Since the 1st Edition
The 1st edition's [[Data Warehousing]] note covered the warehouse, ETL, and the reasons for separation — all still here. Everything after that is new or substantially expanded: data lakes and the sushi principle, ETL generalising into pipelines, HTAP and why it doesn't replace warehouses, SaaS-API connectors as a product category, DataOps and the compliance pressure, event streams as an analytics input, and reverse ETL. This is one of the clearest cases in the book of a 2017 section being overtaken by the intervening decade of tooling.

## Related
- up: [[Operational Versus Analytical Systems (2e)]] · chapter: [[Ch 01 - Trade-Offs in Data Systems Architecture (2e)]]
- [[Cloud Data Warehouses (2e)]] — what warehouses became once they were built on object storage
- [[Extract-Transform-Load (2e)]] — ETL treated as a batch-processing workload
- [[Stars and Snowflakes - Schemas for Analytics (2e)]] — the analysis-friendly schema ETL transforms into
- 1st edition: [[Data Warehousing]] — the pre-lake, pre-HTAP version of this section
