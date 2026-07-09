---
persona: alex
kind: concept
sources:
- vutr/shuffle-writes-to-disk
last_updated: '2026-07-09'
qc: passed
slug: 007-shuffle-writes-to-disk
topics:
- spark
learner: alex
source_note: shuffle-writes-to-disk
mastery: learning
---

*What Alex understood:* Alex: So even though Spark is famous for being in-memory, the shuffle step actually writes to disk. And the default is 200 shuffle partitions no matter the data size, so I should tune that. And reduceByKey is better than groupByKey because it cuts the data down before the shuffle instead of after.

## Follow-up questions

**Alex:** Why is it better that reduceByKey reduces data before the shuffle instead of after?

**vutr:** vutr: Because the shuffle is the expensive part where data gets written to disk and moved around. reduceByKey reduces the data before the shuffle, so there's simply less data to write and move. groupByKey reduces after, so more data goes through the shuffle. Less data before the shuffle = less disk writing.

**Alex:** Does the 200 default change automatically if my data is really big?

**vutr:** vutr: No. The default of 200 is applied regardless of data size, so it must be tuned by you. It doesn't adjust itself to how big your data is.
