---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: change-data-capture-cdc-and-data-sourcing
---

Related: [[query-based-cdc]] · [[trigger-based-cdc]] · [[log-based-cdc]] · [[write-ahead-log]] · [[read-replica]] · [[secrets-manager]] · [[silent-drift-from-hard-deletion]] · [[pull-model-consumption]]

## Comparisons
The three CDC flavors sit on a clean impact-versus-complexity spectrum. [[query-based-cdc]] is the simplest to reason about but the weakest guarantee — it needs an updated_timestamp and silently misses DELETEs. [[trigger-based-cdc]] catches every mutation but taxes the source with a double write into a shadow table. [[log-based-cdc]] is the gentlest on the source because it reads the [[write-ahead-log]] instead of touching the tables, at the cost of the most complexity. Reading from a log via logical replication is gentler on the source than periodic bulk exports, and pairing it with a [[read-replica]] keeps the master fully untouched.

## Open questions
- If [[query-based-cdc]] structurally cannot see DELETEs, how much of the [[silent-drift-from-hard-deletion]] problem is really just a symptom of choosing the wrong CDC type?
- When is the highest-complexity [[log-based-cdc]] actually worth it over the simpler options, versus over-engineering for a low-throughput source?
- Given that even a Kafka consumer is [[pull-model-consumption]], where exactly does polling latency compound across a multi-hop pipeline?
- How do teams operationalize cross-checking against the source to catch missing data before the months-later manual reconciliation?

## Synthesis
The source is the one part of the pipeline you don't fully control, so the CDC choice is really a choice about how lightly you can touch it — [[log-based-cdc]] reading the [[write-ahead-log]] off a [[read-replica]] is the gentlest, while [[query-based-cdc]] is simplest but blind to deletes. That blindness feeds directly into [[silent-drift-from-hard-deletion]], the failure mode that stays invisible until a manual reconciliation. Underneath it all, consumption is a [[pull-model-consumption]] even in Kafka, and the operational discipline — [[secrets-manager]] plus least privilege — is what keeps the whole thing safe to run.
