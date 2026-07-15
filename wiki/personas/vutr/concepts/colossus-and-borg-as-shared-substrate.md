---
persona: vutr
kind: concept
sources:
- raw/google-infrastructure/procella-the-query-engine-at-youtube.md
- raw/google-infrastructure/i-spent-5-hours-learning-how-google.md
last_updated: '2026-07-15'
qc: passed
slug: colossus-and-borg-as-shared-substrate
topics:
- google-infrastructure
---

Two of the systems covered in these posts — [[procella|Procella]] at YouTube and BigQuery's Dremel engine — sit on the same Google-internal storage foundation: Colossus. Neither post treats this as a coincidence worth dwelling on, but naming the same storage layer underneath two very differently-branded products is itself informative about how much of "Google infrastructure" shares a substrate rather than being entirely separate stacks. Borg is a separate story: it appears only in the Procella post, as Procella's own compute layer — the BigQuery/BigLake post never names Borg (or any compute layer) as underlying Dremel, so this note treats Borg as Procella-specific rather than shared between the two.

Colossus, Google's scalable file system, has storage characteristics the Procella post calls out explicitly because they shape everything built on it: data is immutable once written, listing files or otherwise touching metadata is slower than on a local filesystem because it requires talking to Colossus's metadata servers, and every read or write goes over RPC — cheap at a large granularity, but costly and slow if a system issues many small operations against it. The BigQuery post adds the query-engine side of the same fact: Dremel "was designed to be operated on remote storage (Colossus)," and that design choice is exactly what makes BigQuery's later separation of compute, storage, and shuffle — the architecture that let Google bring the query engine closer to lakehouse-style external data in the first place — a natural extension rather than a rewrite.

Borg, Google's cluster manager, is the compute side — for Procella specifically, not for BigQuery. The Procella post introduces it with an analogy rather than a lineage claim: "imagine Kubernetes here, but Borg is the internal technology at Google." The Procella post is specific about its operational implications: a Borg master can tear down machines at any time for maintenance or upgrades, a Borg cluster mixes thousands of commodity machines with different hardware configurations and only incomplete task isolation between tenants, and the combination makes individual task performance unpredictable. A system built on Borg therefore has to treat fault tolerance as a baseline requirement, not an add-on — which is the direct motivation behind Procella's caching layers ([[procella-caching-and-affinity-scheduling]]) and its tail-latency defenses ([[procella-tail-latency-mitigation]]): both exist specifically to absorb the unpredictability Borg introduces.

*See also: [[procella]] · [[bigquery-storage-api]] · [[biglake-tables]]*
