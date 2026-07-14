---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 10
chapter_title: Batch Processing
topic: Beyond MapReduce
type: subtopic
tags: [ddia, pregel, graph-processing, iterative-algorithms]
sources:
  - raw/ch10.md
---
# Graphs and Iterative Processing
> "Repeat until converged" algorithms like PageRank don't fit single-pass [[MapReduce]]; the Pregel (bulk synchronous parallel) model gives each vertex durable state and per-iteration message passing instead.

## The Idea
Chapter 2 treated graphs as OLTP data (see [[Graph-Like Data Models]]) — find a few matching vertices fast. Batch graph processing analyzes the *whole* graph offline, as recommendation engines and ranking systems do; PageRank, estimating a page's popularity from inbound links, is the canonical example. Careful with names: dataflow engines arrange *operators* in a DAG while the data stays tuple-shaped; in graph processing the *data itself* is a graph.

## How It Works
Many graph algorithms walk edges repeatedly — e.g., transitive closure ("list every place inside North America") — until no edges remain to follow or a metric converges. You can drive that with an external scheduler rerunning a MapReduce job per iteration, but it's grossly inefficient: MapReduce rereads the entire input and rewrites a complete output every round even when only a sliver of the graph changed.

The *bulk synchronous parallel* (BSP) model — popularized by Google's Pregel paper — fixes this. As mappers conceptually "send a message" to a reducer keyed by destination, in Pregel a vertex sends messages to other vertices, usually along edges. Each iteration calls a function per vertex with all messages sent to it in the previous round — but unlike MapReduce, a vertex *remembers its state in memory across iterations*, so it processes only new messages; quiet regions of the graph do no work. It resembles the actor model (see [[Message-Passing Dataflow]]) with fault-tolerant, durable vertex state and communication in fixed rounds: the framework guarantees every message sent in iteration *n* is delivered exactly once in iteration *n+1*, even over networks that drop or duplicate (see [[Unreliable Networks]]).

**Fault tolerance and parallelism.** Message passing (rather than direct queries between vertices) allows batching; the only waiting is the barrier between rounds. Recovery comes from periodically checkpointing all vertex state; a crash rolls the computation back to the last checkpoint, or with deterministic logic plus logged messages only the lost partition is recomputed. Vertices address each other by vertex ID, so the framework may partition arbitrarily — in practice it hashes vertex IDs with no attempt to co-locate chatty neighbours.

## Trade-offs & Pitfalls
- Cross-machine chatter dominates: intermediate message traffic often exceeds the graph itself, throttling distributed graph jobs.
- If the graph fits on one machine, a single-machine (even single-threaded) algorithm frequently beats the cluster; disk-based single-node frameworks like GraphChi extend that reach. Distribute only when you must — efficient parallel graph processing remains open research.

## Examples & Systems
PageRank; Apache Giraph, Spark's GraphX, Flink's Gelly (all Pregel implementations); GraphChi for single-machine processing.

## Related
- up: [[Beyond MapReduce]] · chapter: [[Ch 10 - Batch Processing]]
- [[Materialization of Intermediate State]] — why per-iteration MapReduce jobs waste I/O
- [[Reduce-Side Joins and Grouping]] — the mapper-as-message-sender idea Pregel extends
