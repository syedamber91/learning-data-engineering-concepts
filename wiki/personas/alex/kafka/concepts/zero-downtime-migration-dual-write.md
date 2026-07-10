---
persona: alex
kind: concept
sources:
- vutr/zero-downtime-migration-dual-write
last_updated: '2026-07-10'
qc: passed
slug: zero-downtime-migration-dual-write
topics:
- kafka
learner: alex
source_note: zero-downtime-migration-dual-write
mastery: mastered
---

Okay, let me try to say this back. The old way, MirrorMaker 2, is basically like moving houses where you have to stop *everyone* — nobody can send mail or receive mail — while the moving truck finishes its last trip. And you can't even predict how long the truck takes, because it depends on how much stuff there is and how bad traffic is. On top of that, the moving company loses track of where each person's mailbox pointer was, so people re-read old letters. That's the downtime and the reprocessing problem.

The AutoMQ way is smarter because nobody stops. The trick is data flows *both directions at once* — that's the 'dual write.' So while I'm slowly moving people from the old house to the new house one small group at a time, anything anyone does in the new house also gets copied back to the old house. That means the old house always has the complete, true picture, so if the move goes wrong I can just tell everyone 'go back' and nothing is lost.

The part I think is the real cleverness: the same worker (the partition leader) plays two roles. As a Fetcher it's like a vacuum sucking new letters out of the old system, only ever grabbing *new* stuff since last time so it never double-grabs. As a Router it's like a mail-forwarder pushing new-house letters back to the old house — and to keep letters in order it bundles them per sender, because the system already promises one sender's letters stay in order. And consumers get frozen when they first arrive at the new house on purpose, so they don't read the same letter twice while half their group is still back at the old house. Only when the *whole* group has moved does it copy their 'read up to here' bookmark and unfreeze them.

*Source: [[zero-downtime-migration-dual-write]] (vutr)*
