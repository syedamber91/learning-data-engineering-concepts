---
persona: vutr
kind: entity
sources:
- raw/olap-cost-and-multi-engine-comparison/12-i-analyzed-the-pricing-models.md
last_updated: '2026-07-15'
qc: passed
slug: microsoft-fabric-and-synapse-analytics
topics:
- olap-cost-and-multi-engine-comparison
---

Microsoft Fabric, introduced in 2023, is Microsoft's unified analytics platform: rather than billing separately for each analytics tool (Synapse for warehousing, Power BI for reporting, and so on), it bills a single shared compute pool that every workload — engineering, science, warehousing, reporting — draws from. It sits alongside the older Azure Synapse Analytics, which per vutr's reading of Microsoft's own documentation is now the platform Microsoft recommends *migrating away from*: Fabric keeps receiving ongoing optimizations and new features, while Synapse remains supported but frozen.

Synapse's Dedicated SQL pool bills hourly by Data Warehousing Units (DWU): a higher pool tier carries more DWU and a higher $/hour rate, and that rate is itself region-dependent (DW100c costs $1.20/hour in East US 2 but $1.51/hour in Central US). Pausing the pool only saves money if it's paused for a complete billing hour, and — a specific gotcha vutr calls out — if the pool's tier changed partway through an hour (say, from DW100c to DW200c), the *entire* hour is billed at whichever tier was highest during it. Synapse also offers a Serverless mode that instead bills purely by data processed, at a flat $5/TB regardless of region.

Fabric replaces the DWU model with Capacity Units (CU): a customer purchases a specific SKU (F2, F64, and so on), and each SKU grants a fixed number of CU-seconds — an F4 SKU's 4 CU/second works out to 345,600 CU-seconds a day — that every task (a warehouse query, a Spark transform, anything) draws down from as it runs. SKU rates are region-dependent here too (F2 costs $0.36/hour in East US 2 vs $0.40/hour in West US), and Fabric adds three explicit mechanisms for handling load beyond the raw CU budget: bursting lets a capacity briefly consume more than its SKU technically allows; smoothing spreads that burst's CU-second cost across the following 24 hours rather than billing it all at once; and throttling progressively caps usage if bursting continues without relief.

Storage follows the same split. Synapse's Dedicated SQL pool stores data in Azure Storage, billed separately from compute at a flat rate per TB per month, rounded up to the nearest terabyte (750GB of usage bills as a full 1TB) and varying by region ($23/TB/month in East US vs $27.752/TB/month in West US) — the billed volume includes the warehouse's own data files, the last 7 days of incremental backups, and a geo-redundant copy if that's enabled. Fabric instead stores data in OneLake, built on Azure Data Lake Storage Gen2, capable of holding any file type but defaulting warehouse data to Delta Lake-Parquet format; OneLake bills per GB/month with no terabyte rounding, split across three separately-rated storage classes — regular OneLake storage, BCDR (Business Continuity and Disaster Recovery) storage, and OneLake cache — with the East US regular-storage rate at $0.026/GB/month.

*See also: [[cloud-warehouse-compute-pricing-abstractions]] · [[cloud-warehouse-storage-pricing-dimensions]]*
