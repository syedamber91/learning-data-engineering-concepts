---
persona: alex
kind: concept
sources:
- vutr/tiered-storage-kip-405
last_updated: '2026-07-10'
qc: passed
slug: tiered-storage-kip-405
topics:
- kafka
learner: alex
source_note: tiered-storage-kip-405
mastery: mastered
---

Okay, let me try to say it back. Original Kafka is like a storage locker where the shelf and the security guard come bolted together — if you want more shelf space, you're forced to hire another whole guard, even though you didn't need one. That's the compute-and-storage-glued-together thing, and it's wasteful, especially on the cloud where copying stuff between zones costs money each time. So KIP-405 splits the shelving into two. The local tier is the broker's own fast disk holding only the newest data, like the front counter where you keep this week's packages. The remote tier is a giant warehouse — S3, HDFS, whatever — holding the old stuff for months. The trick that makes it work is that each tier has its OWN retention rule: the front counter can throw things out after a few hours because a copy already went to the warehouse. A background copier moves segments from local to remote, but only once a segment is fully 'settled' — its end offset has to be below the LastStableOffset, meaning everything under it is decided and definitely there, so you never ship half-baked data. The leader broker does this copying in order, oldest first. And reads are kept in separate lanes: if you want recent data it's served straight from local, but if you want old data a separate pool of threads fetches it from remote, so a slow warehouse trip doesn't jam up the fast counter. The big honest catch is that the broker is still NOT stateless — it still owns the hot local data and still replicates to other brokers, so cluster changes still shove data around. It just carries way less of it, so recovery is quicker. It loosens the coupling, doesn't delete it.

*Source: [[tiered-storage-kip-405]] (vutr)*
