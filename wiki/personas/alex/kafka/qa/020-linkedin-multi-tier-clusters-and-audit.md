---
persona: alex
kind: concept
sources:
- vutr/linkedin-multi-tier-clusters-and-audit
last_updated: '2026-07-10'
qc: passed
slug: 020-linkedin-multi-tier-clusters-and-audit
topics:
- kafka
learner: alex
source_note: linkedin-multi-tier-clusters-and-audit
mastery: mastered
---

*What Alex understood:* Wait, so the whole point is that LinkedIn's cleverness isn't 'we bought 4,000 brokers' — it's how they organized them. Let me try it with my own picture. Imagine a school with campuses in different cities. Each campus has its own mailroom for each *kind* of mail — one for monitoring mail, one for logging mail, one for tracking mail. Students and teachers (producers and consumers) only ever walk to the mailroom on their own campus, never drive to another city. Then for the stuff that needs a whole-school view — like building the search index, which needs everyone's data — there's a central sorting facility per mail category (the aggregate cluster), and couriers haul mail from every campus mailroom to it. So the flow is producer → local cluster → aggregate cluster → consumer, and the cross-city driving is done only by the couriers, never by the students. But that means the courier service itself becomes a real system you have to run — they first used Mirror Maker, it couldn't keep up, so they built Brooklin to replace it. And because mail now takes multiple hops, you can't just *assume* it all arrived — so they count it like a bus driver counts kids: every producer keeps a tally of messages sent per time window and publishes the tally into a special auditing topic, and audit consumers reading alongside the real consumers publish their own tallies into that same topic. If the two tallies disagree, you know something's wrong, and the header metadata in every message (timestamp, physical server, service) tells you exactly which service and host to blame. The third piece is basically 'how to keep your own edited copy of the textbook in sync with the official edition': keep the internal branch close to Apache Kafka, push normal features upstream first then cherry-pick back, but land emergency production fixes internally first and upstream them later.

## Follow-up questions

**Alex:** The audit counts themselves are just Kafka messages published into an auditing topic — if the pipeline is dropping messages, what stops it from dropping the audit-count messages too, so the books balance even though data was lost?

**vutr:** The note gives the honest shape of this trade, Alex, and your instinct about the danger is right — the pipeline IS where the failure showed up. Multi-tier buys you this: local reads and writes stay cheap, and producers and consumers only ever talk to brokers in their own data center, which simplifies configuration and avoids cross-datacenter network issues for every one of those clients. The cost is stated just as plainly: you now own a replication pipeline. So the cross-datacenter problem doesn't disappear — it gets concentrated into one place that a dedicated team can operate and swap out, which is exactly what happened: when Kafka Mirror Maker hit a scaling issue replicating from local to aggregate clusters, LinkedIn replaced that one component with Brooklin, an internal tool that streams data across different data stores — without touching how any producer or consumer was configured. And critically, they didn't trust the pipeline after fixing it either: Kafka Audit exists precisely because once messages take multiple hops, completeness must be proven by comparing producer counts against audit-consumer counts, not assumed.

**Alex:** You said the win is that no client ever crosses data centers — but the data still has to cross, Brooklin just does it instead of the clients. Why is concentrating all the cross-datacenter traffic into one replication pipeline actually better, given that Mirror Maker already showed that pipeline is exactly where scaling failures happen?

**vutr:** (the wiki does not cover this — see open questions)
