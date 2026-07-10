---
persona: alex
kind: concept
sources:
- vutr/zookeeper-to-kraft-metadata-management
last_updated: '2026-07-10'
qc: passed
slug: zookeeper-to-kraft-metadata-management
topics:
- kafka
learner: alex
source_note: zookeeper-to-kraft-metadata-management
mastery: mastered
---

Okay let me try to say this back. So the old Kafka was like a restaurant where the kitchen (the brokers) does the cooking, but there's a totally separate front-desk company (ZooKeeper) whose only job is keeping the seating chart of who sits where. You have to hire that whole second company, pay them, and make sure they never call in sick — just to remember bookkeeping. KRaft says 'why not just let the kitchen keep its own seating chart?' So they move the metadata inside Kafka.

And the way they keep it from getting messed up is kind of clever: they pick one boss — the controller quorum leader — and say only the boss is allowed to *write* into the seating chart. If any broker wants to change something, it can't just scribble on its own copy, it has to go ask the boss. That's the 'single-owner write path.' But everyone gets to *read*, because the boss photocopies every change and mails it out to every broker, so they all keep a local copy. One pen, many photocopies. Raft is basically the rule for electing that boss and making sure the copies stay in sync.

Then the wild part is what this makes possible. The seating chart stores which partition lives on which broker. Normally moving a partition to another broker means physically hauling gigabytes of data across the network. But in AutoMQ the broker doesn't actually hold the data on its own disk at all — it's stateless, the data lives in shared storage. So 'moving' a partition is just changing one line in the seating chart: this partition now belongs to that broker. No hauling. The AutoBalancer sits right on the controller and reads the log directly as changes happen, so it reacts fast, instead of standing outside squinting at the cluster like Cruise Control does. But I noticed the actual traffic *numbers* don't go through KRaft — those ride a separate internal topic. KRaft is only for the membership-and-mapping stuff.

*Source: [[zookeeper-to-kraft-metadata-management]] (vutr)*
