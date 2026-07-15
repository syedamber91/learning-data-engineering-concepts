---
persona: vutr
kind: entity
sources:
- raw/lakehouse-architecture-and-practical-builds/data-architecture-101.md
last_updated: '2026-07-15'
qc: passed
slug: kappa-architecture
topics:
- data-architecture-warehouse-lake-lakehouse-mesh-lambda-kappa
---

Kappa was introduced, in Vu's account, specifically to address Lambda's dual-codebase problem: instead of treating data as hot (stream) and cold (batch), Kappa treats everything as a single stream. Even historical data is "replayed" and pushed through the same stream-processing code — his concrete example is re-consuming a Kafka message from an earlier offset and running it through the same processing logic used for live data. The payoff is a single codebase instead of two; the cost, which Vu states as directly as the payoff, is that the approach "requires experience in operating and maintaining stream systems such as Kafka, Flink, or Spark Micro Batching" — you trade a maintenance-burden problem for an expertise-requirement problem.

Like [[lambda-architecture]], Vu classifies Kappa as a pattern rather than a full architecture — see [[architecture-vs-pattern]] — because it answers the specific question of how to process and serve data, not the whole ingestion-to-serving blueprint.

*See also: [[data-lake]] · [[data-warehouse]] · [[lambda-architecture]] · [[data-mesh]] · [[medallion-architecture]] · [[lakehouse]]*

## Related in the other wiki
- [[Batch and Stream Processing]] — DDIA's "unification instead" alternative — replaying history through one stream-processing codebase via log replay and exactly-once semantics — describes the same idea this note names as Kappa.
