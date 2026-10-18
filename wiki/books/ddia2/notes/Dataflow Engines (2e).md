---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 11
chapter_title: Batch Processing
topic: Batch Processing Models
type: subtopic
tags: [ddia2, spark, flink, dataflow, dryad, operators]
sources:
  - raw/ch11.md
---
# Dataflow Engines
> The key move: handle an entire workflow as one job, rather than breaking it into independent subjobs. Six advantages follow from that one decision.

## The Idea
**To fix some of MapReduce's problems, several new execution engines were developed — the best known being Spark and Flink.** **They are designed differently but have one thing in common: they handle an entire workflow as one job, rather than breaking it into independent subjobs.**

**Since they explicitly model the flow of data through several processing stages, they are known as dataflow engines.** **Like MapReduce they support a low-level API repeatedly calling a user-defined function on one record at a time, but they also offer higher-level operators such as join and group by.** **They parallelize work by sharding inputs and copy the output of one task over the network to become another's input.** **Unlike MapReduce, operators need not take the strict roles of alternating map and reduce, but can be assembled in more flexible ways.**

**These dataflow APIs generally use relational-style building blocks**: joining datasets on a field, grouping tuples by key, filtering by a condition, and aggregating by counting, summing, or other functions. **Internally these are implemented using shuffle algorithms.**

## How It Works
**The style is based on research systems like Dryad and Nephele**, and offers **six advantages over MapReduce:**
- **Expensive work such as sorting needs to be performed only where required**, rather than always happening by default between every map and reduce stage.
- **Several consecutive operators that don't change sharding — such as map or filter — can be combined into a single task**, reducing data copying overheads.
- **Because all joins and data dependencies are explicitly declared, the scheduler has an overview of what data is required where and can make locality optimizations** — placing a consuming task on the same machine as the producing task **so data can be exchanged through a shared memory buffer rather than copied over the network.**
- **Intermediate state between operators can usually be kept in memory or written to local disk**, requiring **less I/O than writing to a distributed filesystem or object store**, where it must be replicated to several machines and written to disk on each. **MapReduce already does this for mapper output; dataflow engines generalize it to all intermediate state.**
- **Operators can start executing as soon as their input is ready** — **no need to wait for the entire preceding stage to finish.**
- **Existing processes can be reused to run new operators, reducing startup overheads** compared to MapReduce, which **launches a new JVM for each task.**

## Trade-offs & Pitfalls
**You can use dataflow engines to implement the same computations as MapReduce workflows, and they usually execute significantly faster because of these optimizations.**

The corresponding cost, covered in [[Distributed Job Orchestration (2e)]], is **fault tolerance**: keeping intermediate state off the DFS means it must be **recomputed from lineage (Spark) or restored from a checkpoint (Flink)** rather than simply re-read.

## Examples & Systems
Spark and Flink; Dryad and Nephele as the research ancestry.

## Since the 1st Edition
The 1st edition covered dataflow engines under "Beyond MapReduce," with a similar list of advantages and the same Dryad/Nephele lineage. **The change is status**: what the 1st edition presented as the emerging alternative, **the 2nd presents as the mainstream**, with MapReduce demoted to background.

## Related
- up: [[Batch Processing Models (2e)]] · chapter: [[Ch 11 - Batch Processing (2e)]]
- [[MapReduce (2e)]] — the model this improves on
- [[Distributed Job Orchestration (2e)]] — the fault-tolerance consequence
- [[Shuffling Data (2e)]] — how the operators are implemented
- 1st edition: [[Beyond MapReduce]] — where the 1st edition covered dataflow engines

## In the vutr data-engineering wiki
- [[rdd-fundamentals-and-properties]] — vutr's mechanical breakdown of the lineage-based recomputation this section names as Spark's answer to MapReduce's forced disk materialization.
- [[jobs-stages-tasks-dag-and-dependencies]] — how Spark's DAGScheduler draws stage boundaries at shuffle points — the mechanism behind this section's claim that dataflow engines sort only where needed.
