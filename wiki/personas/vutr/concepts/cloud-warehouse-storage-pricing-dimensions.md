---
persona: vutr
kind: concept
sources:
- raw/olap-cost-and-multi-engine-comparison/12-i-analyzed-the-pricing-models.md
- raw/olap-cost-and-multi-engine-comparison/22-i-analyzed-the-pricing-models.md
- raw/olap-cost-and-multi-engine-comparison/saving-cloud-data-warehouse-cost.md
last_updated: '2026-07-15'
qc: passed
slug: cloud-warehouse-storage-pricing-dimensions
topics:
- olap-cost-and-multi-engine-comparison
---

Storage cost looks like a single $/TB/month number until you actually try to compute your bill, at which point it turns out to be several independent axes stacked on top of each other — and vutr's pricing-model deep dive is really an argument that you have to identify all of them before you can predict what you'll be charged.

The first axis is whether storage is billed separately from compute at all. Redshift's legacy dc2 generation bundles storage into the node price, because data lives directly on the compute node's SSDs — so if you need more storage, you must buy more compute, "which might not be cost-efficient, as you might be charged for the unused CPUs and RAM on those instances." The RA3 generation (and serverless) breaks that coupling: data moves into Redshift Managed Storage, billed per GB independent of compute, at the same rate whether the block currently happens to be cached on local SSD or resting in S3.

The second axis is region, which shifts the same nominal service's rate outright: Azure Synapse's dedicated-pool storage runs $23/TB/month in East US vs $27.752/TB/month in West US; BigQuery's active logical storage rate is $0.023/GB in Tokyo vs $0.02/GB in Singapore.

The third axis is allocation granularity. Synapse's Dedicated SQL pool sells storage in 1TB blocks and rounds up — store 750GB and you're billed for a full terabyte. Fabric's OneLake, by contrast, bills per GB with no rounding, but splits that per-GB rate into three separately-priced storage classes: regular OneLake storage, BCDR (Business Continuity and Disaster Recovery) storage, and OneLake cache.

The fourth axis, unique to BigQuery among the vendors covered, is data temperature: a table's data sits in Active storage by default, and if it goes 90 consecutive days without modification it's automatically moved to Long-term storage at roughly half the Active rate — touching it again (any modification) snaps it straight back to the Active rate. This is the same "if it isn't touched, it's worth less" logic Medium applied manually to its Snowflake pipelines and that vutr generalizes as a lever any team can pull: "some data from 2 or 5 years ago might barely bring value and be less frequently accessed... you can consider offloading data to lower-cost storage classes."

The fifth axis, also specific to BigQuery, is logical vs. physical volume: you choose whether you're billed on the data's size before compression (logical) or after (physical), where the physical rate runs 1.5–2x the logical rate — meaning physical billing only pays off if your uncompressed-to-compressed ratio beats that same 1.5–2x multiplier. Because temperature and volume-model are independent choices, a full BigQuery storage estimate is actually the sum of four separately-rated numbers: active-physical, long-term-physical, active-logical, and long-term-logical volume, each at its own regional rate.

The sixth axis is retention: cloud warehouses keep a table's snapshot history around for a configurable window to support time-travel queries (and, per vutr's practices post, "fail-safe" recovery from an accidental delete) — the billed storage includes that history, not just the live table, so shortening the retention window is a direct and controllable cost lever, traded directly against how far back you can recover or query.

Underneath every one of these axes sits the same physical fact repeated across vendors: warehouse data is written as immutable, compressed, columnar-or-hybrid files, so the *choice* of compression scheme is itself a cost knob — Snowflake and Redshift let you pick a scheme per column, trading storage size against decompression CPU ("there is no free lunch here"), while BigQuery instead removes that choice and gives you the logical/physical billing choice described above in its place.

*See also: [[cloud-warehouse-compute-pricing-abstractions]] · [[olap-cost-control-client-side-practices]] · [[microsoft-fabric-and-synapse-analytics]] · [[redshift-managed-storage-and-elastic-compute]]*
