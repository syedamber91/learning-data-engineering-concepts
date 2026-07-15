---
persona: vutr
kind: concept
sources:
- raw/iceberg-hudi-delta-open-table-formats/why-walmart-chose-apache-hudi-for.md
- raw/iceberg-hudi-delta-open-table-formats/how-do-doordash-evolve-realtime-processing.md
- raw/iceberg-hudi-delta-open-table-formats/why-do-we-need-open-table-formats.md
last_updated: '2026-07-15'
qc: passed
slug: evaluate-before-adopting
topics:
- iceberg
---

Two real production decisions in these notes make the same point from opposite directions: the "best" table format is whichever one fits your actual workload, not whichever one has the most attention.

Walmart's evaluation (detailed in [[walmart-hudi-benchmark]]) is the disciplined version of this lesson. Rather than picking by reputation, Walmart abstracted its real workloads into two categories — a batch workload dominated by inserts with rare late-arriving updates, and a streaming workload dominated by CDC-driven upserts — deployed Delta, Hudi, Iceberg, and its legacy system into isolated environments, let each reach a steady state, and only then benchmarked ingestion and query performance. The result cut against the market's attention: Delta Lake and Iceberg get more discussion, but Hudi won on Walmart's specific batch and real-time-dedup needs, while Iceberg was dropped from consideration entirely over a concrete operational problem (file-size cleanup during ingestion) that popularity metrics would never have surfaced. Walmart's own stated lessons generalize the point directly: the most popular tool isn't automatically the best fit; benchmarking has to be fair and run in isolation to mean anything; and choosing open-source-and-self-managed versus vendor-managed is itself a trade-off between control and operational burden, not a free win either way.

DoorDash's decision (detailed in [[doordash-iceberg-realtime-migration]]) shows the same evaluation discipline applied faster and more narrowly. DoorDash didn't evaluate table formats in the abstract — it evaluated Iceberg and Delta Lake specifically against its own Flink-based real-time pipeline, and picked Iceberg for reasons tied directly to that pipeline: more mature Flink integration than the more Spark-centric Delta Lake, flexible schema/partition evolution, an active community, and concurrent-write support — though DoorDash's own engineers note that last point isn't actually Iceberg-exclusive, since all three formats support concurrent writes via optimistic concurrency control (see [[occ-on-object-storage]]). That caveat matters: it shows the evaluation was specific enough to catch and discard a reason that sounded good but didn't actually differentiate the options.

Both cases cash out the same general principle the notes repeat elsewhere about the lakehouse and its formats: every architectural decision has a trade-off, and the right answer depends on the organization's actual requirements and existing tech stack, not on which format is trending. The concrete lever both companies pulled was the same one — build a real, isolated test against your own workload before adopting, rather than reasoning from a format's reputation.

*See also: [[walmart-hudi-benchmark]] · [[doordash-iceberg-realtime-migration]] · [[occ-on-object-storage]] · [[open-table-formats]] · [[copy-on-write-vs-merge-on-read]]*
