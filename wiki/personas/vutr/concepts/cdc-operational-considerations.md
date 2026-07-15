---
persona: vutr
kind: concept
sources:
- raw/change-data-capture-cdc-and-data-sourcing-additional/everything-you-need-to-know-about-741.md
last_updated: '2026-07-15'
qc: passed
slug: cdc-operational-considerations
topics:
- change-data-capture-cdc-and-data-sourcing
---

CDC is not free, and each of the three types pays for itself differently. Log-based CDC is the lowest-impact method overall, but still requires reading transaction logs (binlog, WAL, redo log), and the database may need to emit more detailed log information to satisfy consumer needs. Trigger-based CDC adds write overhead directly into the application's own transactions, since a trigger fires on every tracked `INSERT`/`UPDATE`/`DELETE`. Query-based CDC creates read pressure through periodic polling, especially on large tables. Because deploying any of these touches the source database, Vu is explicit that implementing a CDC pipeline means collaborating with the teams that own the source to plan and test before going to production — sometimes that means infrastructure changes on the source side, like standing up a new read replica for the CDC process to hit.

Operating a log-based pipeline in particular demands real monitoring discipline, because it now involves multiple moving components: lag monitoring (replication lag shows how far behind the CDC process is from the live database; high lag means stale data and a bottleneck somewhere in the pipeline), alerting (for pipeline failures, lag past a threshold, or unexpected changes like a schema change entering the pipeline), and failure recovery (a documented playbook for restarting the process and bridging whatever gap accumulated while it was down).

Schema changes are their own hazard: developers can add, drop, or retype columns via `ALTER TABLE` without warning, and those changes propagate straight to consumers who may not know they're coming — causing downstream failures the CDC pipeline operator only discovers when something breaks. Vu's proposed fix is active communication with the source team so schema changes are flagged in advance, ideally as a signal an event-driven architecture can act on; he notes databases can track schema changes via triggers on DDL statements, which doubles as a notification mechanism. He also flags that Flink introduced Flink CDC 3.0 specifically to handle schema evolution.

Finally, security: the CDC tool needs permission to read the database's internal transaction logs, and those credentials must follow the principle of least privilege. Vu frames this as a collaboration, not a unilateral decision — you work with the teams responsible for the source to figure out exactly which permissions the CDC process needs, and follow the vendor's guidance for supplying those credentials to the connector securely.

*See also: [[log-based-cdc]] · [[trigger-based-cdc]] · [[query-based-cdc]] · [[schema-change-severity-and-detection]] · [[source-access-trust-boundary]]*
