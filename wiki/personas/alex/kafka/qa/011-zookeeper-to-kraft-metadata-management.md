---
persona: alex
kind: concept
sources:
- vutr/zookeeper-to-kraft-metadata-management
last_updated: '2026-07-10'
qc: passed
slug: 011-zookeeper-to-kraft-metadata-management
topics:
- kafka
learner: alex
source_note: zookeeper-to-kraft-metadata-management
mastery: mastered
---

*What Alex understood:* Okay let me try to say this back. So the old Kafka was like a restaurant where the kitchen (the brokers) does the cooking, but there's a totally separate front-desk company (ZooKeeper) whose only job is keeping the seating chart of who sits where. You have to hire that whole second company, pay them, and make sure they never call in sick — just to remember bookkeeping. KRaft says 'why not just let the kitchen keep its own seating chart?' So they move the metadata inside Kafka.

And the way they keep it from getting messed up is kind of clever: they pick one boss — the controller quorum leader — and say only the boss is allowed to *write* into the seating chart. If any broker wants to change something, it can't just scribble on its own copy, it has to go ask the boss. That's the 'single-owner write path.' But everyone gets to *read*, because the boss photocopies every change and mails it out to every broker, so they all keep a local copy. One pen, many photocopies. Raft is basically the rule for electing that boss and making sure the copies stay in sync.

Then the wild part is what this makes possible. The seating chart stores which partition lives on which broker. Normally moving a partition to another broker means physically hauling gigabytes of data across the network. But in AutoMQ the broker doesn't actually hold the data on its own disk at all — it's stateless, the data lives in shared storage. So 'moving' a partition is just changing one line in the seating chart: this partition now belongs to that broker. No hauling. The AutoBalancer sits right on the controller and reads the log directly as changes happen, so it reacts fast, instead of standing outside squinting at the cluster like Cruise Control does. But I noticed the actual traffic *numbers* don't go through KRaft — those ride a separate internal topic. KRaft is only for the membership-and-mapping stuff.

## Follow-up questions

**Alex:** If only the leader can write metadata and every broker must go through it, doesn't the leader become a bottleneck or a single point of failure — what happens to writes the moment that leader broker dies, before a new one is elected?

**vutr:** You've caught the real tension in a single-writer design, and the note answers part of it. The leader is deliberately the only writer — that's the point, it prevents conflicting edits to the metadata. What protects you from the leader simply being a single point of failure is that it isn't a lone server: it's a *quorum*. Raft does two jobs here, and the first is exactly the one you're worried about — it *elects a leader for the quorum*. So the metadata is replicated across the quorum via Raft, and if the current leader dies, Raft's job is to elect a new one from the remaining quorum members, which already hold replicated copies of the metadata. That's precisely why the note frames KRaft as *enhancing resilience* and *removing* the failure points ZooKeeper introduced, rather than adding one. What the note does not spell out is the fine-grained behavior of in-flight writes during that election window — how long the gap is, or whether a write is rejected versus retried while a new leader is being chosen. So the mechanism that saves you from a permanent single point of failure is clear; the exact moment-to-moment handling of writes mid-election is not something I can pin down from the note.

**Alex:** You said load metrics ride a separate internal Kafka topic instead of KRaft — but that internal topic itself needs partition/broker mappings that live in KRaft. Isn't that circular, where the metrics channel depends on the very metadata system it's supposed to be kept separate from?

**vutr:** This is a sharp catch about a possible circular dependency, and I have to be honest about the boundary of what the note tells me. The note is explicit about the *division of labor*: KRaft carries the membership and mapping changes — including, by its own definition, the mapping between topic/partition and data and between partitions and brokers — while load metrics travel over a separate internal Kafka topic between broker and controller. Since that internal topic is a Kafka topic, its own partition/broker placement would logically be described by the same kind of mapping KRaft manages. But the note never actually addresses whether that creates a bootstrapping or circularity problem, or how the metrics topic is brought up relative to KRaft. So while your inference about where the mapping lives is consistent with what the note says metadata contains, the resolution of the circularity you're pointing at is genuinely beyond what the note covers.
