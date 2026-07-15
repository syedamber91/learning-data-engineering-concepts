---
persona: vutr
kind: concept
sources:
- raw/change-data-capture-cdc-and-data-sourcing-additional/everything-you-need-to-know-about-741.md
last_updated: '2026-07-15'
qc: passed
slug: log-based-cdc
topics:
- change-data-capture-cdc-and-data-sourcing
---

Log-based CDC reads changes directly from the database's transaction log rather than querying tables or firing triggers. That log is called different things in different systems — the redo log in Oracle, the Write-Ahead Log (WAL) in PostgreSQL, the binary log (binlog) in MySQL — but the underlying principle is the same everywhere: write-ahead logging, where every data change must be durably recorded in the log *before* it's applied to the database's actual data files. That rule exists so the DBMS can recover after a crash — replaying the log lets it reapply committed transactions that never made it from memory to disk — which is exactly why the log is the definitive, complete record of every committed change and the ideal source for CDC to tap into. A CDC tool with a log-based reader taps this stream of log records, parses them, and propagates them downstream.

Because it reads from log files instead of executing queries against live tables, log-based CDC gives the source the lowest performance impact of the three approaches while still capturing every type of change (including deletes) and shipping it with near real-time latency. The cost is complexity: it typically requires specific database configuration (e.g., enabling logical replication in Postgres), elevated permissions to access the transaction log, and — because consuming a change log is really consuming a real-time stream — real streaming infrastructure (message queue, producer/consumer, a destination that can accept a stream). Each DBMS also implements its own proprietary log format, so you end up depending on the CDC tool's connector to correctly interpret that specific format; you will rarely build a log reader from scratch, instead relying on an available connector such as the [[debezium|Debezium Connector for PostgreSQL]].

A typical log-based CDC pipeline, at the conceptual level, has five stages: (1) a transaction commits against the source database (e.g., Postgres, MySQL); (2) as part of normal durability, the database writes that transaction to its native transaction log before finalizing the change in the data files; (3) a log reader — usually a CDC connector, not something you build — continuously monitors the log for new records; (4) a log publisher, also handled by the connector, publishes each new log record to a message broker; (5) the broker (e.g., Apache Kafka) stores the log records reliably and decouples producers from consumers, so the source can generate hundreds of changes a minute without downstream consumers needing to keep up in lockstep — they can, for instance, just query all the changes from the last hour. Downstream consumers then subscribe to the relevant topics and process the change events however they need. Given its minimal source impact and low latency, this is why log-based CDC is the most widely adopted approach for continuous change synchronization.

*See also: [[query-based-cdc]] · [[trigger-based-cdc]] · [[debezium]] · [[cdc-operational-considerations]] · [[write-ahead-log]]*
