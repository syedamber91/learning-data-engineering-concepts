---
persona: alex
kind: concept
sources:
- vutr/shuffle-writes-to-disk
last_updated: '2026-07-09'
qc: passed
slug: shuffle-writes-to-disk
topics:
- spark
learner: alex
source_note: shuffle-writes-to-disk
mastery: mastered
---

So the shuffle is Spark's step for regrouping data by key across the cluster — and here's the trap: even though Spark is sold as 'in-memory,' the shuffle actually WRITES to disk, because the map side has to dump its intermediate results somewhere durable for the reduce side to fetch. On top of that, Spark always cuts the shuffled data into 200 partitions by default no matter how big the data is, so you have to tune spark.sql.shuffle.partitions to fit your actual size. And reduceByKey beats groupByKey because it shrinks the data on each node BEFORE the shuffle, so there's less to write to disk and less to send over the wire — groupByKey shuffles everything raw and only combines afterward.

```mermaid
graph LR
  A[Map tasks produce key-value data] --> B[Shuffle write: intermediate data spilled to DISK]
  B --> C[Reduce tasks fetch shuffled data over network]
  C --> D[Split into 200 partitions by default - must tune spark.sql.shuffle.partitions]
  A -. reduceByKey pre-combines on each node BEFORE shuffle .-> B
  A -. groupByKey ships all raw values, combines only AFTER shuffle .-> C
```

*Source: [[shuffle-writes-to-disk]] (vutr)*
