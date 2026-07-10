---
persona: alex
kind: concept
sources:
- vutr/kafka-iceberg-zero-etl
last_updated: '2026-07-10'
qc: passed
slug: 017-kafka-iceberg-zero-etl
topics:
- kafka
learner: alex
source_note: kafka-iceberg-zero-etl
mastery: mastered
---

*What Alex understood:* Wait, so let me get this straight. Normally Kafka is like a mail sorting room that only sees sealed envelopes — it moves your messages around super fast but has no clue what's inside, it's just bytes to it. So if you want to actually *study* all that mail later, you have to build your own little factory next door (Spark or Flink) that opens every envelope, copies it onto nice paper, and files it into your library (the Iceberg lakehouse). And you have to run one factory per mail-stream, babysit them all, deal with torn letters, and keep the library shelves tidy. That's the ETL tax.

Zero-ETL says: what if the mail room itself is already storing everything in the big shared warehouse (object storage) instead of its own closet? Then it's cheap to ALSO hand you that same mail as an organized library — same data, two doors. AutoMQ does this with a foreman (Coordinator) on partition 0 who's the only one allowed to say "this batch is officially filed," so the workers don't step on each other and clutter the records. The workers turn records into Parquet and ship them to S3. The Schema Registry is like a bouncer at the door — if a message doesn't match the expected format it's rejected before it even gets in, and if the format legitimately changes, the broker looks up the new version and updates the library shelves to match, no downtime.

And Bufstream is the greedy-smart version: instead of keeping mail in the closet AND copying it to the library (two copies = double rent), it just keeps ONE copy in library form and serves live readers straight from it, row by row. That's why the storage bill collapses from ~$42k to ~$4.6k. The catch is the letters arrive a beat slower — like 260ms — because writing to the shared warehouse in batches is slower than a local closet, and if you want them faster you batch smaller and pay more in trips.

## Follow-up questions

**Alex:** You said the Coordinator sits on partition 0 and centralizes all the commits so workers don't conflict — but if it's a single point funneling every commit, doesn't that partition-0 Coordinator become a bottleneck (or a single point of failure) when the topic has a huge number of partitions all trying to commit at once?

**vutr:** Good instinct on why the Coordinator is centralized: the note says commits are centralized *specifically* so independent workers don't create commit conflicts and metadata inflation — many workers each committing to the Iceberg catalog independently would collide and bloat the metadata, so funneling commits through one Coordinator per Table Topic (bound to partition 0) is the deliberate fix for that. However, on whether that Coordinator then becomes a throughput bottleneck or single point of failure at high partition counts, the note does not say — it describes the Coordinator's role (tracking sync progress, managing table commits) but gives no detail on its scaling limits or failure/failover behavior. That is a genuine gap in this note.

**Alex:** For Bufstream's single-copy trick, consumers are served 'row by row' from the same Iceberg table — but Iceberg is a batch/columnar format that only becomes visible once the metadata pointer flips after manifests are written. So how does a live consumer poll for a brand-new message that's still sitting in an intake file and hasn't been committed to Iceberg yet — wouldn't it either not see it or have to wait for the whole batch?

**vutr:** The note is explicit that Bufstream serves consumers 'row by row from the same table,' and its write path lands messages first in intake files, and only with the archive format set to iceberg does the background process rewrite those intake files into Iceberg — writing data files, then manifests, manifest lists, metadata files, and finally updating the catalog's current-metadata pointer. So the note establishes there are two stages (intake files, then committed Iceberg) and that consumers are served from the table, but it does NOT explain the mechanism by which a live consumer sees a just-produced message that is still in an intake file and not yet committed past the metadata pointer. How the low-latency read of uncommitted intake data is reconciled with Iceberg's commit-visibility model is not covered here.
