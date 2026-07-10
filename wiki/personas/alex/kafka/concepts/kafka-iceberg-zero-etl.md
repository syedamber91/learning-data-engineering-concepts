---
persona: alex
kind: concept
sources:
- vutr/kafka-iceberg-zero-etl
last_updated: '2026-07-10'
qc: passed
slug: kafka-iceberg-zero-etl
topics:
- kafka
learner: alex
source_note: kafka-iceberg-zero-etl
mastery: mastered
---

Wait, so let me get this straight. Normally Kafka is like a mail sorting room that only sees sealed envelopes — it moves your messages around super fast but has no clue what's inside, it's just bytes to it. So if you want to actually *study* all that mail later, you have to build your own little factory next door (Spark or Flink) that opens every envelope, copies it onto nice paper, and files it into your library (the Iceberg lakehouse). And you have to run one factory per mail-stream, babysit them all, deal with torn letters, and keep the library shelves tidy. That's the ETL tax.

Zero-ETL says: what if the mail room itself is already storing everything in the big shared warehouse (object storage) instead of its own closet? Then it's cheap to ALSO hand you that same mail as an organized library — same data, two doors. AutoMQ does this with a foreman (Coordinator) on partition 0 who's the only one allowed to say "this batch is officially filed," so the workers don't step on each other and clutter the records. The workers turn records into Parquet and ship them to S3. The Schema Registry is like a bouncer at the door — if a message doesn't match the expected format it's rejected before it even gets in, and if the format legitimately changes, the broker looks up the new version and updates the library shelves to match, no downtime.

And Bufstream is the greedy-smart version: instead of keeping mail in the closet AND copying it to the library (two copies = double rent), it just keeps ONE copy in library form and serves live readers straight from it, row by row. That's why the storage bill collapses from ~$42k to ~$4.6k. The catch is the letters arrive a beat slower — like 260ms — because writing to the shared warehouse in batches is slower than a local closet, and if you want them faster you batch smaller and pay more in trips.

*Source: [[kafka-iceberg-zero-etl]] (vutr)*
