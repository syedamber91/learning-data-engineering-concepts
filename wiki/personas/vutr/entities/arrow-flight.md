---
persona: vutr
kind: entity
sources:
- raw/apache-arrow-additional/apache-arrow-for-data-engineers.md
- raw/apache-arrow-additional/i-spent-6-hours-learning-apache-arrow.md
last_updated: '2026-07-15'
qc: passed
slug: arrow-flight
topics:
- apache-arrow
---

Arrow Flight is Arrow's answer to the hardest of the three data-exchange scenarios Vu walks through: moving data between two processes on two different machines (see [[zero-copy-data-sharing]]). Without Flight, that exchange normally goes through JSON — verbose and redundant because every record repeats its attribute keys, which burns network bandwidth, and lacking a rich type system, which risks data-integrity problems when converting to and from richer formats.

Flight is a high-performance RPC framework that organizes the exchange as a network stream of Record Batches instead. Rather than paying JSON's serialization cost, data travels over the wire in its native, compressed Arrow format, and the receiver gets a stream of bytes already laid out in the exact memory shape it needs for processing — no re-serialization on arrival. Because the schema travels with the Arrow type system intact, Flight also preserves data integrity end to end. And because the underlying format is columnar, Flight can shrink the bandwidth bill further by transferring only the columns a query actually needs, rather than whole records.

Vu positions Flight as the client-server RPC layer Arrow provides so that systems can build robust, application-specific data-exchange services on top of it — the same zero-copy principle that Arrow IPC applies at the process/file boundary (see [[arrow-ipc]]), extended across the network.

*See also: [[arrow-table-and-chunked-arrays]] · [[arrow-ipc]] · [[apache-arrow]] · [[zero-copy-data-sharing]]*
