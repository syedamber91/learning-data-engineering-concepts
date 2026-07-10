---
persona: alex
kind: concept
sources:
- vutr/consumer-group-rebalancing
last_updated: '2026-07-10'
qc: passed
slug: consumer-group-rebalancing
topics:
- kafka
learner: alex
source_note: consumer-group-rebalancing
mastery: mastered
---

Okay let me try to rebuild this. So partitions are like numbered mail routes, and consumers are the mail carriers. Rebalancing is when the routes get *reassigned* between carriers — and it only happens when the number of carriers changes, either someone new shows up or someone drops dead on the job. It's not a cleanup thing; it's a genuine handover.

The way the depot knows a carrier is gone is this Group Coordinator — one specific broker, and *which* broker depends on the group ID, so different teams report to different depots. Each carrier keeps texting 'still alive' (heartbeats) from a side thread. If the texts keep coming, cool. If they stop, the coordinator says 'you're dead' and reshuffles routes. And there are two ways to leave: if you *crash*, the depot waits a few seconds of silence before declaring you dead — and in those seconds your routes are just... unserved, nobody's on them. But if you *quit politely* and tell the depot 'I'm leaving,' it reshuffles instantly, no waiting. So a clean exit is cheaper than a crash.

Then the actual reshuffle: the coordinator does NOT compute assignments — that's the surprising bit. The first carrier who joined is the 'leader' and *it* divvies up the routes. And there are two styles of reshuffle. Eager = everyone drops ALL their routes and the whole depot freezes while new assignments go out, even carriers who'd keep the same routes. Cooperative = only the routes that actually need to move get touched; everybody else keeps delivering, and it happens in a few phased rounds so the depot never fully stops. And Sticky assignment is the 'don't move what you don't have to' rule — when C2 died only C2's partitions went to C3, C1 didn't get disturbed. And offsets are the bookmark, so whoever inherits a route starts from the last saved page, not the beginning.

*Source: [[consumer-group-rebalancing]] (vutr)*
