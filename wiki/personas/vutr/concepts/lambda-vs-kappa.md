---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: lambda-vs-kappa
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Lambda runs parallel batch and stream paths and reconciles them, while Kappa collapses everything onto a single streaming path. The case studies split cleanly: [[uber-lambda-kafka]] and [[linkedin-kafka-beam]] deliberately kept Lambda, whereas [[twitter-kappa-migration]] pivoted to Kappa and stabilized latency at ~10s with better throughput and 95%+ correctness match.

*See also: [[doordash-flink-iceberg]] · [[linkedin-kafka-beam]] · [[netflix-iceberg-maestro]] · [[uber-lambda-kafka]] · [[twitter-kappa-migration]] · [[meta-velox-tectonic]]*

## Related in the other wiki
- [[Batch and Stream Processing]] — DDIA's discussion of lambda's dual-codebase costs and the unification alternative is the conceptual backdrop for the production choices (Uber/LinkedIn vs Twitter) this note surveys.
