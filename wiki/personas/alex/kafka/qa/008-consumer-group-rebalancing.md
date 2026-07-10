---
persona: alex
kind: concept
sources:
- vutr/consumer-group-rebalancing
last_updated: '2026-07-10'
qc: passed
slug: 008-consumer-group-rebalancing
topics:
- kafka
learner: alex
source_note: consumer-group-rebalancing
mastery: mastered
---

*What Alex understood:* Okay let me try to rebuild this. So partitions are like numbered mail routes, and consumers are the mail carriers. Rebalancing is when the routes get *reassigned* between carriers — and it only happens when the number of carriers changes, either someone new shows up or someone drops dead on the job. It's not a cleanup thing; it's a genuine handover.

The way the depot knows a carrier is gone is this Group Coordinator — one specific broker, and *which* broker depends on the group ID, so different teams report to different depots. Each carrier keeps texting 'still alive' (heartbeats) from a side thread. If the texts keep coming, cool. If they stop, the coordinator says 'you're dead' and reshuffles routes. And there are two ways to leave: if you *crash*, the depot waits a few seconds of silence before declaring you dead — and in those seconds your routes are just... unserved, nobody's on them. But if you *quit politely* and tell the depot 'I'm leaving,' it reshuffles instantly, no waiting. So a clean exit is cheaper than a crash.

Then the actual reshuffle: the coordinator does NOT compute assignments — that's the surprising bit. The first carrier who joined is the 'leader' and *it* divvies up the routes. And there are two styles of reshuffle. Eager = everyone drops ALL their routes and the whole depot freezes while new assignments go out, even carriers who'd keep the same routes. Cooperative = only the routes that actually need to move get touched; everybody else keeps delivering, and it happens in a few phased rounds so the depot never fully stops. And Sticky assignment is the 'don't move what you don't have to' rule — when C2 died only C2's partitions went to C3, C1 didn't get disturbed. And offsets are the bookmark, so whoever inherits a route starts from the last saved page, not the beginning.

## Follow-up questions

**Alex:** You said a crash costs 'a few seconds' of dead air while the coordinator waits, but a graceful leave triggers instantly. So if I tune the heartbeat interval super short to detect crashes faster, why doesn't that just make the group rebalance constantly on every tiny network hiccup — isn't there a point where fast detection actively hurts me?

**vutr:** You've spotted exactly the tension the note names. The heartbeat frequency is a tunable knob, and it is explicitly the knob between 'detect failures fast' and 'don't rebalance on every network hiccup.' So yes — pushing detection faster is not free: crank the heartbeat sensitivity too high and a transient network blip looks identical to a crash, so the coordinator declares a live consumer dead and triggers a rebalance you didn't need. That's why Kafka exposes the heartbeat frequency and related consumer configuration parameters for you to control rather than hard-coding it: you're choosing where to sit on that trade-off. The note doesn't hand you a specific millisecond value; it establishes that the trade-off is real and yours to tune.

**Alex:** With cooperative rebalancing, if a consumer keeps processing its untouched partitions while the leader is still handing out the orphaned ones, what stops two consumers from both thinking they own the *same* partition during those in-between phased rounds — how does the handover stay clean if nobody fully stops?

**vutr:** Good instinct to worry about double-ownership, and the note gives you the mechanism that keeps it clean: cooperative rebalancing runs in explicit *phases*. First the group leader notifies all consumers which partitions they will lose; then those consumers stop processing *only those* partitions and give up ownership; then — and only then — the leader assigns the orphaned partitions to their new owners. So the release happens before the reassignment: a partition is given up by its old owner in an earlier phase before the leader hands it to the new owner in a later phase, and it proceeds incrementally over a few rounds until the assignment is stable. The partitions a consumer keeps processing are precisely the ones that are *not* being reassigned, so there's no contest over those. On top of that, ownership transfer is resumable because the broker tracks position via committed offsets — the inheritor picks up from the last committed offset, so the handover has a clean, agreed starting point rather than an overlap.
