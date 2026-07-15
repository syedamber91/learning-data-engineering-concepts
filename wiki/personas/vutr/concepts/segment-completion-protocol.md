---
persona: vutr
kind: concept
sources:
- raw/druid-pinot-real-time-olap/a-glimpse-of-apache-pinot-the-real.md
last_updated: '2026-07-15'
qc: passed
slug: segment-completion-protocol
topics:
- apache-pinot-druid-and-real-time-olap
---

Pinot's segment-completion protocol solves a specific consensus problem created by real-time ingestion: every replica of a segment consumes independently from Kafka. Each replica starts from the same beginning offset with the same end criteria — flush after a configured number of records, or after a configured amount of time — and in theory, independent consumers reading the same offset and partition with the same record count would end up with identical data. In practice, they can diverge, because each consumer relies on its own local clock, and clocks drift.

Pinot resolves this by making the controller the single arbiter rather than letting replicas decide unilaterally when to commit. When a server finishes consuming for its segment, it reports its current Kafka offset to the controller and polls for instructions. The controller replies with one of six instructions:

- **HOLD** — do nothing, poll again later.
- **DISCARD** — drop local data and fetch the controller's authoritative copy; used when another replica has already committed a different version of the segment.
- **CATCHUP** — consume up to a given Kafka offset, then poll again.
- **KEEP** — flush the current segment to disk and load it, used when the server's offset already matches the already-committed copy.
- **COMMIT** — flush the current segment and attempt to commit it; if the commit fails, resume polling, otherwise load the segment.
- **NOTLEADER** — the controller being contacted isn't the current cluster leader; look up the actual leader and poll again.

The controller manages these replies with its own state machine: it waits until either enough replicas have been contacted or a fixed amount of time has passed since the first poll, then picks whichever replica has the largest offset to be the "committer," and directs the remaining replicas to catch up to it. The explicit design goal, per the source, is to minimize network transfer between controller and servers while still guaranteeing that every replica ends up holding identical data once the segment is flushed.

The source describes segments moving from `OFFLINE` to `CONSUMING` when real-time Kafka ingestion begins, and separately describes Helix/the controller marking a segment `ONLINE` once it has been fetched and loaded (segment load) or uploaded (data upload) — but it never states a `CONSUMING`→`ONLINE` transition explicitly. It's a reasonable inference that this protocol is what makes such a transition safe (see [[pinot-cluster-components]]) — the protocol is the missing piece between "servers are independently reading a Kafka topic" and "the resulting immutable segment is the same no matter which replica produced it" (see [[immutable-segment]]) — but the source itself leaves the exact `CONSUMING`→`ONLINE` handoff as an open question rather than a stated fact.

*See also: [[apache-pinot]] · [[pinot-cluster-components]] · [[immutable-segment]]*
