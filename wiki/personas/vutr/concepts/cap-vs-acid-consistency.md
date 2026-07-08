---
persona: vutr
kind: concept
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: cap-vs-acid-consistency
topics:
- data-architecture-warehouse-lake-lakehouse-mesh-lambda-kappa
---

The CAP theorem forces you into CP or AP because partition tolerance is non-negotiable, and PACELC extends it: when there's no partition, you still trade Latency against Consistency. ACID consistency (transactions don't violate constraints) and CAP consistency (linearizability across nodes) are two different things that somehow share a name and confuse us.

*See also: [[data-lake]] · [[data-warehouse]] · [[kappa-architecture]] · [[lambda-architecture]] · [[data-mesh]] · [[medallion-architecture]]*
