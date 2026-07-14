---
persona: vutr
kind: concept
sources:
- raw/olap-cost-and-multi-engine-comparison/12-i-analyzed-the-pricing-models.md
- raw/olap-cost-and-multi-engine-comparison/22-i-analyzed-the-pricing-models.md
last_updated: '2026-07-15'
qc: passed
slug: cloud-warehouse-compute-pricing-abstractions
topics:
- olap-cost-and-multi-engine-comparison
---

Every cloud warehouse hides its physical hardware behind a proprietary compute unit, and once you see the pattern across five vendors it stops looking like five different pricing models and starts looking like one model wearing five costumes. Microsoft Fabric measures Capacity Units (CU) per SKU (an F4 SKU grants 4 CU/second, or 345,600 CU-seconds a day), its predecessor Azure Synapse measures Data Warehousing Units (DWU) on a purchased Dedicated SQL pool, AWS Redshift measures node-hours (provisioned dc2/RA3) or Redshift Processing Units (RPU, serverless), Google BigQuery measures slots, Databricks measures DBUs, and Snowflake measures credits consumed by T-shirt-sized Virtual Warehouses (X-Small to XX-Large, with Gen2 warehouses launched in 2025 offering more capacity per warehouse and promising 2x performance per size). Underneath, the billing formula is always the same shape: consumed units × rate.

Billing granularity converges too: Snowflake and Databricks bill per second with a 60-second minimum; Synapse bills hourly, but with a sting — if you changed pool size mid-hour, the *entire* hour is billed at the highest tier you touched during it (using DW100c from 1:00–1:45 then DW200c from 1:46–1:52 means the whole hour bills at the DW200c rate), and pausing only saves money if you pause for a complete billing hour. Every vendor also offers a discount track for pre-committing to usage — 1- or 3-year reservations on Synapse pools, Fabric SKUs, Redshift nodes, and Snowflake/BigQuery/Databricks capacity — trading flexibility for a lower rate.

The rate half of the equation is genuinely multi-dimensional, not a single number. Region moves it (Fabric F2 is $0.36/hr in East US 2 vs $0.40/hr in West US). Cloud provider moves it for Databricks, whose DBU rate differs across AWS, GCP, and Azure. Plan/edition tier moves it: Snowflake has Standard/Enterprise/Business Critical/Virtual Private Snowflake, Databricks has Premium/Enterprise (Enterprise trades a higher DBU rate for stricter governance and compliance), and BigQuery has Standard/Enterprise/Enterprise Plus, where the edition doesn't just change the rate — Standard can't even set a *minimum* slot count per reservation, a capability reserved for Enterprise and up. Workload type moves it too: Databricks SQL, Lakeflow, and model-serving each get separate DBU rates, and serverless variants of a workload carry a higher DBU rate than the equivalent self-managed one, because Databricks folds the infrastructure cost into it.

That last point exposes a genuine vendor-specific quirk: Databricks is the only one of the five that bills you on two separate invoices for the same compute — a software invoice for DBUs consumed, and a separate cloud-provider invoice for the underlying VM instances — unless you pick the serverless offering, which folds VM cost into the DBU rate. Snowflake, by contrast, is billed entirely through Snowflake; you never see a separate AWS/GCP/Azure line for the Virtual Warehouse's VMs.

BigQuery's reservation model for the capacity pricing tier is its own small system: baseline slots are always provisioned and always billed (guaranteeing your critical workload never waits on slot allocation, but only configurable on Enterprise and up); idle slots are commitment-purchased slots sitting unused by their owning reservation, borrowable by other reservations but preemptable the moment the original owner needs them back; and autoscaling slots fill the gap between a reservation's baseline and its configured max, rounding *up* to the nearest 50-slot increment and — critically — billing for the slots actually provisioned by the scale-up, not the slots actually used, with no commitment discount available on this portion at all.

Two worked examples pin the abstraction to real numbers. BigQuery, Standard edition, no commitment, US-central-1, 200 max slots at a $0.04/slot-hour rate, run 240 hours in a month (8 hrs/day): 0.04 × 200 × 240 = $1,920. Databricks, Premium plan, AWS, SQL Pro Compute, US East, at $0.55/DBU-hour: 3 X-Small instances (6 DBU/hour capacity each) run 5 hours/day for 30 days consume 3 × 6 × 5 × 30 = 2,700 DBUs, so the DBU invoice alone is 2,700 × 0.55 = $1,485 — before adding the separate AWS instance-cost invoice. Snowflake Gen2, AWS, one Small warehouse (2.7 credit/hour) run 120 hours plus one Medium (5.4 credit/hour) run 60 hours: (2.7 × 120) + (5.4 × 60) = 648 credits for the month, still needing to be multiplied by the edition/region credit rate to reach a dollar figure.

*See also: [[cloud-warehouse-storage-pricing-dimensions]] · [[olap-cost-control-client-side-practices]] · [[microsoft-fabric-and-synapse-analytics]] · [[redshift-managed-storage-and-elastic-compute]] · [[virtual-warehouse-isolation-and-shared-tenancy-economics]]*
