---
persona: alex
kind: concept
sources:
- vutr/tiered-storage-kip-405
last_updated: '2026-07-10'
qc: passed
slug: 012-tiered-storage-kip-405
topics:
- kafka
learner: alex
source_note: tiered-storage-kip-405
mastery: mastered
---

*What Alex understood:* Okay, let me try to say it back. Original Kafka is like a storage locker where the shelf and the security guard come bolted together — if you want more shelf space, you're forced to hire another whole guard, even though you didn't need one. That's the compute-and-storage-glued-together thing, and it's wasteful, especially on the cloud where copying stuff between zones costs money each time. So KIP-405 splits the shelving into two. The local tier is the broker's own fast disk holding only the newest data, like the front counter where you keep this week's packages. The remote tier is a giant warehouse — S3, HDFS, whatever — holding the old stuff for months. The trick that makes it work is that each tier has its OWN retention rule: the front counter can throw things out after a few hours because a copy already went to the warehouse. A background copier moves segments from local to remote, but only once a segment is fully 'settled' — its end offset has to be below the LastStableOffset, meaning everything under it is decided and definitely there, so you never ship half-baked data. The leader broker does this copying in order, oldest first. And reads are kept in separate lanes: if you want recent data it's served straight from local, but if you want old data a separate pool of threads fetches it from remote, so a slow warehouse trip doesn't jam up the fast counter. The big honest catch is that the broker is still NOT stateless — it still owns the hot local data and still replicates to other brokers, so cluster changes still shove data around. It just carries way less of it, so recovery is quicker. It loosens the coupling, doesn't delete it.

## Follow-up questions

**Alex:** You said a segment only becomes eligible to copy to remote once its end offset is below the LastStableOffset — but what happens to a message that's between the LSO and the newest offset when the leader broker suddenly dies? It was never copied to remote, so does the new leader just lose it, or is that exactly what the follower replication is quietly protecting?

**vutr:** Good instinct, and you've spotted the seam correctly. Data above the LastStableOffset hasn't been copied to remote yet — only segments whose end offset is below the LSO are eligible. What protects that recent, not-yet-tiered data is exactly the replication path you guessed: followers replicate segments from the leader's LOCAL storage, and before they fetch they build auxiliary state — leader epoch state and producer-ID snapshots. The note says this follower fetch protocol keeps messages consistent and ordered across replicas 'even through broker replacements or failures.' So the hot local data isn't relying on the remote copy for durability; it relies on being replicated to follower brokers. That's also part of why the note is so firm that the broker stays stateful — the local tier still needs full broker-to-broker replication to survive a leader dying.

**Alex:** If local retention is set to just hours and a slow backfill consumer is chewing through old data via the remote thread pool, what stops it from being served corrupt or misordered data — like, how does the system guarantee the remote copy lines up perfectly with what local used to hold, given they're two totally separate storage systems?

**vutr:** The consistency of what gets copied is anchored on that same LSO rule: a segment is only tiered once its end offset is below the LastStableOffset, which the note defines as the offset where all lower offsets 'have been decided and are always present.' So only fully-settled, ordered data ever leaves for remote — you never tier something still in flux. On the serving side, the two tiers are deliberately isolated: remote reads go through a dedicated thread pool so they can't block local reads, and consumers read remote messages directly. And because the leader copies segments in sequence from earliest to latest, the remote log preserves the same offset ordering the local log had.
