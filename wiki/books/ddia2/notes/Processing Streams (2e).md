---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 12
chapter_title: Stream Processing
type: topic
tags: [ddia2, stream-processing, operator, unbounded]
sources:
  - raw/ch12.md
---
# Processing Streams
Having covered where streams come from and how they are transported, **what can you do with a stream once you have it? Broadly, three options:**
1. **Write the event data to a database, cache, search index, or similar storage system**, from where other clients query it. **A good way of keeping a database in sync with changes elsewhere — especially if the stream consumer is the only client writing to it.** **This is the streaming equivalent of the batch use cases.**
2. **Push the events to users** — email alerts, push notifications, or streaming to a real-time dashboard. **Here a human is the ultimate consumer.**
3. **Process one or more input streams to produce one or more output streams**, possibly through a pipeline of several stages before ending at option 1 or 2.

**The rest of the chapter is about option 3.** **A piece of code that processes streams like this is an operator or a job**, closely related to Unix processes and MapReduce jobs, **with a similar dataflow pattern: a stream processor consumes input streams read-only and writes its output to a different location append-only.** **The patterns for sharding and parallelization are also very similar**, and **basic mapping operations such as transforming and filtering records work the same.**

**The one crucial difference is that a stream never ends**, and this has many implications. **Sorting does not make sense with an unbounded dataset, so sort-merge joins cannot be used.** **Fault-tolerance mechanisms must also change**: **with a batch job running a few minutes, a failed task can simply restart from the beginning, but with a stream job running for several years, restarting from the beginning after a crash may not be viable.**

## Subtopics
- [[Uses of Stream Processing (2e)]] — CEP, stream analytics, materialized views, and search on streams.
- [[Reasoning About Time (2e)]] — the surprisingly tricky question of what "the last five minutes" means.
- [[Stream Joins (2e)]] — three join types, and why joins become time-dependent.
- [[Fault Tolerance (Stream Processing) (2e)]] — exactly-once semantics without the luxury of finishing.

## Key Takeaways
- **"A stream never ends" is the single premise from which every difference follows** — no sorting, no restart-from-scratch, no way to know a window is complete.
- **Everything else transfers from batch processing**: sharding, parallelization, mapping, filtering, and the read-only-input/append-only-output dataflow shape.
- The four subtopics correspond to **what you compute, when you compute it, what you join it against, and what happens when it breaks** — which is a reasonable checklist for designing any stream job.

## Since the 1st Edition
The 1st edition's [[Processing Streams]] had the same three options, the same operator/job framing, and the same four subtopics. Substantively stable; the changes are in the subtopics, most notably the incremental view maintenance material added to [[Uses of Stream Processing (2e)]].

## Related
- chapter: [[Ch 12 - Stream Processing (2e)]]
- [[Batch Processing Models (2e)]] — the bounded-input counterpart
- [[Transmitting Event Streams (2e)]] — where the streams come from
- 1st edition: [[Processing Streams]] — the same topic
