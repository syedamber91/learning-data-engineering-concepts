---
persona: vutr
kind: concept
sources:
- raw/meta-data-stack-and-infrastructure/how-did-meta-move-terabytes-of-data.md
last_updated: '2026-07-15'
qc: passed
slug: scribe-delivery-guarantees
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

Scribe doesn't give every consumer the same durability contract — it offers three tiers, and a category's producers and consumers pick the one that matches what the workload actually needs. Best effort prioritizes throughput and availability above all: it's a "fire-and-forget" mode where the Write Proxy routes messages to whatever host is nearest or most available (even a different data center if needed), a failed write is simply retried by the client (which can produce duplicate messages — an accepted trade-off), and a customer "must be prepared to tolerate" some data loss if a write can't be recovered. On the read side, because a category's writes are scattered across many physical shards, enforcing strict cross-shard order would cost latency and throughput, so best-effort readers instead get a configurable dial between ordering and speed.

At least once flips the priority to guaranteeing storage: a client only considers a message sent once the storage layer acknowledges it, with aggressive retries at every step of the write path until that acknowledgment arrives. Because aggressive retries risk the same duplication problem best-effort accepts outright, Scribe adds three specific mitigations for this tier: proactively initializing physical shards ahead of time (so a retry never stalls waiting on shard setup), graduated timeouts that get progressively longer at each downstream step (so an earlier step doesn't give up and retry while a later step is still processing), and conservative, smaller batch sizes, so that if duplication does happen, fewer messages are affected.

Repeatable reads is the strongest guarantee — a consumer rereading the stream sees the same data in the same order every time — and the source names it as essential for use cases like change data capture that need strict ordering. Scribe offers two ways to get there, each with an opposite trade-off: a write variant that pins a logical shard's entire traffic to one dedicated physical shard (simple, but caps throughput at what a single physical shard can handle), and a read variant where an internal "Sequenced Shard Generator" service reads all of a category's scattered metadata shards and reorders them into one new, deterministic metadata shard sized to the downstream application's chosen batch size (removes the single-shard throughput ceiling, at the cost of an extra reordering step that adds latency).

*See also: [[scribe]] · [[scribe-write-path-and-batching]] · [[scribe-read-path-and-ephemeral-cache]]*
