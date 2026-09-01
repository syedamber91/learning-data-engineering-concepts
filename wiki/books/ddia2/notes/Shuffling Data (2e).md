---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 11
chapter_title: Batch Processing
topic: Batch Processing Models
type: subtopic
tags: [ddia2, shuffle, distributed-sort, mergesort, bigquery]
sources:
  - raw/ch11.md
---
# Shuffling Data
> A distributed sort where both input and output are sharded. Joins, grouping, and aggregation are all built on it.

## The Idea
**Both the Unix example and MapReduce are based on sorting.** **Batch processors need to sort datasets petabytes in size, too large for a single machine, so they require a distributed sorting algorithm where both input and output are sharded. Such an algorithm is called a shuffle.**

> **Shuffle is not random.** **When you shuffle a deck of cards you end up with a random order. The shuffle here produces a sorted order, with no randomness.**

**Shuffling is a foundational algorithm for batch processors, used for joins and aggregations.** **MapReduce, Spark, Flink, Daft, Dataflow, and BigQuery all implement scalable and performant shuffle algorithms.**

## How It Works
Using Hadoop MapReduce for illustration, with the job's input sharded into `m1`, `m2`, `m3` — **each shard may be a separate HDFS file or object-store object, with all shards of a dataset in the same directory or under the same key prefix.**

- **The framework starts a separate map task for each input shard.** A task **reads its assigned file, passing one record at a time to the mapper callback.** **The reduce side is also sharded: the number of map tasks is determined by the number of input shards, while the number of reduce tasks is configured by the job's author** and can differ.
- **The mapper outputs key-value pairs, and the framework must ensure that if two mappers output the same key, those pairs are processed by the same reducer.** **To achieve this, each mapper creates a separate output file on its local disk for every reducer** — `m1,r2` is the file created by mapper 1 containing data destined for reducer 2. **When the mapper outputs a pair, a hash of the key typically determines which reducer file it goes to.**
- **While writing these files, the mapper also sorts the key-value pairs within each one**, using the log-structured storage techniques: **batches collected in a sorted in-memory structure, written out as sorted segment files, and smaller segments progressively merged into larger ones.**
- **After each mapper finishes, reducers connect to it and copy the appropriate file of sorted pairs to their local disk.** **Once a reduce task has its share of output from all mappers, it merges these files together preserving sort order, mergesort-style.** **Pairs with the same key are now consecutive, even if they came from different mappers**, and **the reducer function is called once per key with an iterator returning all values for that key.**
- **Records output by the reducer are sequentially written to a file, one per reduce task.** **These files become the shards of the job's output dataset and are written back to the DFS or object store.**

## Trade-offs & Pitfalls
- **MapReduce executes the shuffle between its map and reduce steps, but modern dataflow engines and cloud data warehouses are more sophisticated.** **Systems such as BigQuery have optimized their shuffle algorithms to keep data in memory and to write data to external sorting services** — **speeding up shuffling and replicating shuffled data for resilience.**
- The shuffle is where **the mapper's local disk becomes a bottleneck**, and where the choice of hash function determines whether reducers receive balanced work — the same skew problem as sharding.

## Examples & Systems
Hadoop MapReduce; Spark, Flink, Daft, Dataflow, BigQuery; BigQuery's external shuffle service.

## Since the 1st Edition
The mechanism is unchanged from the 1st edition's description inside its MapReduce topic — the same per-reducer local files, hash-based assignment, in-mapper sorting, and mergesort on the reduce side. **The 2nd edition promotes it to its own subtopic**, adds the **shuffle-is-not-random** clarification, names the **six systems implementing it**, and adds **BigQuery's in-memory and external-service shuffle optimizations** — reflecting that the shuffle has become a specialised, separately engineered component rather than an implementation detail of MapReduce.

## Related
- up: [[Batch Processing Models (2e)]] · chapter: [[Ch 11 - Batch Processing (2e)]]
- [[Joins and Grouping (2e)]] — what the shuffle is for
- [[Sorting Versus In-Memory Aggregation (2e)]] — the single-machine version
- [[Log-Structured Storage (2e)]] — the sort-and-merge technique reused
- [[Sharding by Hash of Key (2e)]] — the same hashing decision
