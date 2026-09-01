---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 11
chapter_title: Batch Processing
topic: Batch Processing Models
type: subtopic
tags: [ddia2, mapreduce, mapper, reducer, functional-programming, hadoop]
sources:
  - raw/ch11.md
---
# MapReduce
> Four steps, two of which you write. The other two — parsing records and sorting — the framework does for you, and the sort is the one that matters.

## The Idea
**The pattern is very similar to the web server log analysis example:**
1. **Read a set of input files and break it into records.** In the log example each record is one line (`\n` is the separator). **In Hadoop's MapReduce the input is stored in a DFS like HDFS or an object store like S3**, in formats such as **Apache Parquet** (columnar) or **Apache Avro** (row-based).
2. **Call the mapper function to extract a key and value from each input record.** In the Unix example the mapper is `awk '{print $7}'`, **extracting the URL as the key and leaving the value empty.**
3. **Sort all the key-value pairs by key.** In the log example this is the first `sort`.
4. **Call the reducer function to iterate over the sorted pairs.** **If there are multiple occurrences of the same key, the sorting has made them adjacent, so it is easy to combine those values without keeping a lot of state in memory.** In the Unix example the reducer is `uniq -c`.

**Steps 2 and 4 are where you write your custom code.** **Step 1 is handled by the input format parser. Step 3, the sort, is implicit — you don't write it, because the mapper's output is always sorted before it reaches the reducer.**

## How It Works
**Mapper.** **Called once for every input record**, its job is to **extract the key and value.** **For each input it may generate any number of key-value pairs, including none.** **It keeps no state from one record to the next, so each record is handled independently** — **so there can be many mappers running in parallel on different parts of the input.**

**Reducer.** **The framework takes the mappers' key-value pairs, collects all values belonging to the same key, and calls the reducer with an iterator over that collection.** **The reducer produces output records**, and **reducers for different keys can also run in parallel.**

**In the log example there was a second `sort` ranking URLs by request count.** **In MapReduce, a second sorting stage means writing a second MapReduce job with the first job's output as input.** **Viewed like this: the mapper's role is to prepare the data into a form suitable for sorting, and the reducer's role is to process the data that has been sorted.**

> **MapReduce and functional programming.** **The programming model comes from functional programming**: **Lisp introduced `map` and `reduce` (or `fold`) as higher-order functions on lists**, and they have reached mainstream languages including Python, Rust, and Java. **Many common data processing operations, including those offered by SQL, can be implemented on top of MapReduce.** **The functional principle of avoiding mutable state enables parallel execution**: since **every call to the mapper and reducer depends only on the data the framework explicitly passes**, the framework is **free to run independent calls in parallel on different nodes** — **and if a task fails, to call the mapper or reducer again with the same input on another node.**

## Trade-offs & Pitfalls
- **Implementing a complex job using the raw MapReduce APIs is actually quite laborious** — **any join algorithms would need to be implemented from scratch.**
- **MapReduce is also quite slow compared to more modern batch processors.** **One reason is that its file-based I/O prevents job pipelining** — processing output data in a downstream job before the upstream job is complete.

## Examples & Systems
Hadoop MapReduce; Parquet and Avro as input formats; Lisp's `map` and `fold` as the ancestry.

## Since the 1st Edition
The four steps, the mapper/reducer contract, and the functional-programming box all carry over from the 1st edition's MapReduce material. **The framing changed completely, though.** The 1st edition presented MapReduce as *the* batch processing model and devoted substantial space to its join algorithms and workflow patterns; **the 2nd edition presents it as historically influential but largely obsolete, and states its two weaknesses — laborious APIs and no job pipelining — as the motivation for dataflow engines.**

## Related
- up: [[Batch Processing Models (2e)]] · chapter: [[Ch 11 - Batch Processing (2e)]]
- [[Dataflow Engines (2e)]] — what replaced it, and why
- [[Simple Log Analysis (2e)]] — the same four stages in Unix
- [[Shuffling Data (2e)]] — the implicit sort in step 3
- 1st edition: [[MapReduce]] — the same subtopic

## In the vutr data-engineering wiki
- [[spark-origin-and-mapreduce-limitations]] — vutr's account of why Spark was built to replace exactly this model — the independent confirmation of the 2nd edition's much blunter verdict that MapReduce is now largely obsolete.
