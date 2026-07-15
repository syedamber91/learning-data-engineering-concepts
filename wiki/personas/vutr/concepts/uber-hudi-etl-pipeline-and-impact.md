---
persona: vutr
kind: concept
sources:
- raw/uber-data-infrastructure-case-studies/how-did-uber-build-their-data-infrastructure.md
- raw/uber-data-infrastructure-case-studies/i-spent-5-hours-understanding-how.md
last_updated: '2026-07-15'
qc: passed
slug: uber-hudi-etl-pipeline-and-impact
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Uber's actual incremental-ETL implementation runs Hudi and Spark on top of Piper, Uber's internal workflow tool (Vu describes it as "think Airflow"). Rather than have every team hand-roll this, Uber built a Spark ETL framework — the Sparkle framework in later material ([[sparkle-etl-framework]]) — using Hudi's own incremental ingestion tool, DeltaStreamer, which Uber originally contributed to and which many other organizations now use (DeltaStreamer supports ingesting from sources like Kafka). The framework abstracts the pipeline down to three user-supplied inputs: a **table definition** (DDL schema plus Hudi format), **DeltaStreamer YAML configs** (declaring, among other things, `hoodie.datasource.recordkey.field` — the primary key Hudi uses for deduplication via upsert — and `hoodie.datasource.write.operation`, one of the write types in Hudi's operation taxonomy), and the **transformation logic** itself, expressed as SQL executed via Spark SQL, or as Scala/Java for more advanced cases; DeltaStreamer reads the target table's latest Hudi-metadata checkpoint to know where to resume the incremental read.

The measured impact of migrating batch ETL to this incremental model was a 50% reduction in pipeline run time overall. For the Dimensional Driver Table specifically, Uber used 59.06% less CPU core and 73.01% less memory than the old batch approach, and the same pipeline that used to take roughly 3.7 hours now finishes in 39 minutes.

Three secondary benefits ride along with the incremental design. **Data consistency**: because Uber replicates data redundantly across multiple data centers for availability, and strong cross-DC consistency is business-critical, Hudi's metadata lets Uber replicate only the incrementally changed files across data centers after computing a table in the primary center — rather than re-shipping whole tables. **Data quality**: Uber layers the write-audit-publish (WAP) pattern on top of Hudi, running SQL-based data quality checks on data before it's allowed into the production dataset ([[uber-data-quality-standardization]] describes the checks Uber runs generally). **Observability**: DeltaStreamer emits its own metrics — the number of Hudi commits currently in progress, and total records inserted/updated/deleted — giving Uber visibility into the incremental pipeline as it runs.

*See also: [[uber-hudi-query-and-write-taxonomy]] · [[sparkle-etl-framework]] · [[marmaray]] · [[uber-data-quality-standardization]]*
