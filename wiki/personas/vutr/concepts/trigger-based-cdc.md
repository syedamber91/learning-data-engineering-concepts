---
persona: vutr
kind: concept
sources:
- raw/change-data-capture-cdc-and-data-sourcing-additional/everything-you-need-to-know-about-741.md
last_updated: '2026-07-15'
qc: passed
slug: trigger-based-cdc
topics:
- change-data-capture-cdc-and-data-sourcing
---

Trigger-based CDC solves query-based CDC's biggest blind spot by using database triggers — stored procedures the database fires in the background on `INSERT`, `UPDATE`, and `DELETE` events. When a change occurs, the trigger writes a record of that change (operation type plus affected data) into a separate shadow table in the same database. A CDC process then periodically reads new entries from that shadow table.

Because triggers fire on every mutation type, this approach can track any data change, including deletes — the one thing query-based CDC structurally cannot see. Triggers are also immediate: they capture changes the instant they happen, though how fast that change actually reaches downstream systems still depends on how often the process reads the shadow table. And triggers are a standard, widely-supported relational database feature, so availability isn't usually a problem.

The cost shows up on the source, not downstream. Every transaction on a tracked table now incurs at least two writes — one to the original table, one from the trigger into the shadow table — which becomes a real problem for high-throughput databases. Managing a large number of triggers across many tables also gets complex to maintain, and you still need a separate process to read the shadow table; triggers alone aren't the whole pipeline.

*See also: [[query-based-cdc]] · [[log-based-cdc]] · [[outbox-pattern-and-dual-write-problem]] · [[cdc-operational-considerations]]*
