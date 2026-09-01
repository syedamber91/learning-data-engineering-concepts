---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 11
chapter_title: Batch Processing
type: topic
tags: [ddia2, mapreduce, dataflow, programming-models]
sources:
  - raw/ch11.md
---
# Batch Processing Models
Having seen how batch jobs are **scheduled** in a distributed environment, this topic turns to how frameworks **process data.** **The two most common models are MapReduce and dataflow engines.** **Although dataflow engines have largely replaced MapReduce in practice, it is useful to understand how MapReduce works, since it influenced many modern frameworks.**

**Both have evolved to support multiple programming models** — **low-level programmatic APIs, relational query languages, and DataFrame APIs.** **A variety of options enables application engineers, analytics engineers, business analysts, and even nontechnical employees to process company data.**

## Subtopics
- [[MapReduce (2e)]] — the four steps, the two callbacks, and its functional-programming lineage.
- [[Dataflow Engines (2e)]] — Spark and Flink, and six concrete advantages.
- [[Shuffling Data (2e)]] — the distributed sort that everything else is built on.
- [[Joins and Grouping (2e)]] — what sorted data buys you.
- [[Query Languages (2e)]] — SQL as the lingua franca, and its limits.
- [[DataFrames (2e)]] — the model data scientists already know.

## Key Takeaways
- **The progression through the subtopics is a progression up the abstraction stack**: raw callbacks → dataflow operators → SQL and DataFrames. **The chapter's own framing is that operational concerns were solved first, so focus shifted to usability.**
- **[[Shuffling Data (2e)]] is the load-bearing subtopic.** Joins, grouping, and aggregation are all implemented on top of the shuffle, so understanding it explains the performance of everything above it.
- **MapReduce is included for lineage, not for use.** The book is explicit that it is largely obsolete.

## Since the 1st Edition
The 1st edition organised its computation material as [[MapReduce and Distributed Filesystems]] plus a "Beyond MapReduce" topic containing dataflow engines and graph processing. **The 2nd edition inverts the emphasis**: MapReduce is one subtopic among six, dataflow engines are presented as the mainstream, and **query languages and DataFrames are promoted to full subtopics** reflecting that usability, not scalability, is now the frontier.

## Related
- chapter: [[Ch 11 - Batch Processing (2e)]]
- [[Batch Processing in Distributed Systems (2e)]] — the storage and orchestration these models run on
- [[Batch Use Cases (2e)]] — what people do with them
