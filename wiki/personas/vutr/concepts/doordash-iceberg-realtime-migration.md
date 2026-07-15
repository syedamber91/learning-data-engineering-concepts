---
persona: vutr
kind: concept
sources:
- raw/iceberg-hudi-delta-open-table-formats/how-do-doordash-evolve-realtime-processing.md
last_updated: '2026-07-15'
qc: passed
slug: doordash-iceberg-realtime-migration
topics:
- iceberg
---

DoorDash's real-time platform originally consumed events from customers, dashers, merchants, and internal applications — peaking above 30 million messages per second, roughly 5GB/s — through Kafka into Flink, which wrote Parquet to S3; Snowpipe then copied that S3 data into Snowflake for consumers, triggered off Amazon SQS notifications. That pipeline had been sized for hundreds of thousands of messages at peak; by the time DoorDash was running 30 million, three problems had become structural rather than incidental: Snowflake's cost climbed with every new user of the platform, every event was physically written twice (once by Flink to S3, once by Snowflake's own load into its native storage), and the whole design was locked to a single vendor.

DoorDash's fix was to put Iceberg directly between Flink and Snowflake rather than route through Snowpipe at all: Flink still writes Parquet to S3 exactly as before, but those files are now wrapped in Iceberg's metadata layer as they land, and Snowflake queries that Iceberg-on-S3 data directly instead of loading a second copy into its own storage. DoorDash also stood up Trino, querying the same Iceberg tables via the AWS Glue catalog, which the old Snowflake-only pipeline couldn't have supported without yet another data copy. Because a typical Flink job is just source, transform, and sink, and Flink ships an out-of-the-box Iceberg sink connector, the actual code change needed was small — swap the sink.

DoorDash's own stated reasons for Iceberg over Delta Lake, tried and set aside: more mature Flink integration (Delta is comparatively Spark-centric), flexible schema and partition evolution, a more active community, and support for concurrent table writes — though DoorDash's own engineers are explicit that concurrent writes aren't actually an Iceberg-exclusive advantage, since all three formats implement it via optimistic concurrency control (see [[occ-on-object-storage]]).

Two adoption frictions surfaced in production. First, although the Iceberg *specification* supports schema evolution, the Flink-Iceberg connector DoorDash used did not — it needs a static schema, so any schema change means stopping the Flink job, adjusting it, and restarting, a limitation DoorDash judged tolerable given everything else Iceberg bought them. Second, some queries against deeply nested fields with hundreds of key-value pairs got noticeably slower than before, because Snowflake's native VARIANT type had handled that shape well and Iceberg's flat columnar layout didn't; DoorDash's fix was to flatten those fields in Iceberg and allocate more query compute, rather than accept the regression.

The payoff, by DoorDash's own numbers: storage costs dropped 25–49% versus native Snowflake storage using only the default zstd compression, with further savings from simply eliminating the duplicate S3-then-Snowflake write; Snowpipe's freed-up resources went straight to Iceberg operations like compaction; concurrent-write support let DoorDash run multiple independent pipelines against one table (e.g., a standard sink alongside a backfill, at the same time); Iceberg's native time travel is available without Snowflake's paid retention-period upsell; and the underlying data-lake approach (S3 as the system of record, not Snowflake's proprietary storage) meant DoorDash could add Trino without a second migration. Iceberg's hidden partitioning — see [[iceberg-hidden-partitioning-and-sort-order]] — is a further concrete benefit DoorDash calls out directly, letting analysts filter on a natural timestamp column without needing to know about a separate physical partition column.

Vu's own reflection ties this back to a broader engineering habit: pick common, portable components (a lesson he attributes to *Fundamentals of Data Engineering*) so technical decisions stay reversible — DoorDash's earlier choice to land data in S3 first, rather than loading straight into Snowflake, is exactly what made this later Iceberg migration cheap to execute at all.

*See also: [[apache-iceberg]] · [[iceberg-hidden-partitioning-and-sort-order]] · [[occ-on-object-storage]] · [[evaluate-before-adopting]] · [[delta-lake]]*
