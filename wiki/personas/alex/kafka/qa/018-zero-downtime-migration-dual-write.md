---
persona: alex
kind: concept
sources:
- vutr/zero-downtime-migration-dual-write
last_updated: '2026-07-10'
qc: passed
slug: 018-zero-downtime-migration-dual-write
topics:
- kafka
learner: alex
source_note: zero-downtime-migration-dual-write
mastery: mastered
---

*What Alex understood:* Okay, let me try to say this back. The old way, MirrorMaker 2, is basically like moving houses where you have to stop *everyone* — nobody can send mail or receive mail — while the moving truck finishes its last trip. And you can't even predict how long the truck takes, because it depends on how much stuff there is and how bad traffic is. On top of that, the moving company loses track of where each person's mailbox pointer was, so people re-read old letters. That's the downtime and the reprocessing problem.

The AutoMQ way is smarter because nobody stops. The trick is data flows *both directions at once* — that's the 'dual write.' So while I'm slowly moving people from the old house to the new house one small group at a time, anything anyone does in the new house also gets copied back to the old house. That means the old house always has the complete, true picture, so if the move goes wrong I can just tell everyone 'go back' and nothing is lost.

The part I think is the real cleverness: the same worker (the partition leader) plays two roles. As a Fetcher it's like a vacuum sucking new letters out of the old system, only ever grabbing *new* stuff since last time so it never double-grabs. As a Router it's like a mail-forwarder pushing new-house letters back to the old house — and to keep letters in order it bundles them per sender, because the system already promises one sender's letters stay in order. And consumers get frozen when they first arrive at the new house on purpose, so they don't read the same letter twice while half their group is still back at the old house. Only when the *whole* group has moved does it copy their 'read up to here' bookmark and unfreeze them.

## Follow-up questions

**Alex:** You said the Fetcher can start at `latest` or a `timestamp`, and that a fresh partition might get 'internally truncated' so its start lines up with the source offset — but if AutoMQ starts fetching at `latest`, doesn't that skip every message written *before* the migration began? How does the offset stay 'preserved' if we deliberately started partway through the log?

**vutr:** Good catch, and the note is honest about the nuance. The starting point is a *choice* you make at setup: `earliest` means start from the first message's offset (so you copy the whole history), while `latest` or a `timestamp` means you intentionally start from the current end or some point in time. So when you pick `latest`, you are indeed choosing not to carry the old history — that's a deliberate setup decision, not a bug. The truncation the note mentions is about aligning a *fresh* AutoMQ partition's start so it matches the chosen source offset. What Kafka Linking preserves is offsets going forward from that agreed starting point, so consumers don't reprocess as they migrate — it doesn't claim to invent history you told it to skip.

**Alex:** During the producer phase you said everything a migrated producer sends to AutoMQ is forwarded back to Kafka so Kafka stays the source of truth — but the Fetcher is *also* pulling from Kafka into AutoMQ. So a message a producer sends to AutoMQ goes back to Kafka, and then wouldn't the Fetcher immediately pull that same message *back* into AutoMQ again, creating a loop or a duplicate?

**vutr:** Honestly, the note doesn't spell out a loop-prevention mechanism for that exact case. It tells us the two roles clearly — Fetcher pulls Kafka→AutoMQ, Router forwards AutoMQ→Kafka — and that during the producer phase Kafka stays the single source of truth while forwarded writes go back to Kafka. But it never explains how a message a producer sends *to* AutoMQ, then routed back to Kafka, is kept from being re-fetched into AutoMQ as if it were new source data. That's a genuine seam the note leaves open, so I won't invent a tagging or filtering rule it doesn't state.
