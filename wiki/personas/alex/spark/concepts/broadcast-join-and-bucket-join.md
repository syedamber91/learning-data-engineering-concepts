---
persona: alex
kind: concept
sources:
- vutr/broadcast-join-and-bucket-join
last_updated: '2026-07-10'
qc: passed
slug: broadcast-join-and-bucket-join
topics:
- spark
learner: alex
source_note: broadcast-join-and-bucket-join
mastery: mastered
---

Wait, so I had it backwards -- I thought broadcast join and bucket join were two different join "engines," like two different recipes. But they're not. Broadcast join is just regular hash join, except instead of both tables walking across the cluster to meet in the middle, Spark photocopies the small table and mails a full copy to every single worker's desk. Each worker builds their own little lookup table from that copy and checks their pile of the big table against it locally -- nobody has to wait on anybody else, because everyone already has the whole small table sitting right there. That's why the plan has no Exchange step: only the small table ever traveled.

And it's not magic, it's a size check -- spark.sql.autoBroadcastJoinThreshold, 10MB by default. If the table's under that, Spark just does it automatically. In the actual example, shrinking the order table to ~60MB and bumping the threshold to 65MB was enough to flip the whole plan and make it faster.

Bucket join is the one I really had wrong -- I assumed "no shuffle" meant the shuffle just... vanished. It doesn't. It's more like pre-sorting your mail into cubbies by zip code the moment it arrives at the sorting facility, instead of re-sorting the whole pile every single time a truck needs to deliver it. The sorting work still happens -- bucketBy() hashes rows into buckets when you write the table -- it just happens once, up front, instead of once per join. That's why it only works with saveAsTable(), not plain parquet: the bucket layout has to get written down in the Hive metastore so a later job actually knows "hey, these two tables are already sorted compatibly." Cost isn't gone, it's just paid at write time instead of at every join and even every matching aggregation.

*Source: [[broadcast-join-and-bucket-join]] (vutr)*
