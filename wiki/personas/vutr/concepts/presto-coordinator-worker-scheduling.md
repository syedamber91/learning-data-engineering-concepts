---
persona: vutr
kind: concept
sources:
- raw/history-of-data-engineering-and-hadoop-ecosystem/8-minutes-to-understand-presto.md
last_updated: '2026-07-15'
qc: passed
slug: presto-coordinator-worker-scheduling
topics:
- history-of-data-engineering
---

Presto's query planning starts with a logical planner that turns the syntax tree into an intermediate representation: a tree of plan nodes, each one a physical or logical operation taking input from its children. The query optimizer then derives a physical plan from that logical one, applying transformation rules such as predicate and limit pushdown, column pruning, and decorrelation. It leans on the connector's Data Layout API for this — data location, partitioning scheme, indexes, and sort/group order — so it can pick the most efficient layout for a given query (for example, leveraging partitioning while ignoring sort order when sorting doesn't help). Predicate pushdown itself is negotiated with the connector: the optimizer decides when it's worth pushing a filter down to the data source rather than applying it after the fact.

Parallelism happens at two levels. Inter-node parallelism is the optimizer deciding which plan stages can run across multiple workers at once; a stage can have many tasks executing the same logic on a subset of input data, and a shuffle happens whenever data has to move between stages — shuffles increase latency and burn CPU and memory, so the optimizer has to weigh how many of them a plan requires. Intra-node parallelism, by contrast, parallelizes sections of a single stage across threads on one worker, and is cheaper: those threads can share in-memory structures like hash tables or dictionaries directly, with less overhead than shipping data across the network.

Executing a query then requires two scheduling decisions. Stage scheduling chooses between an all-at-once policy, which schedules every stage concurrently and favors latency-sensitive cases like interactive analytics, and a phased policy, which runs stages in topological order — a hash join, for instance, won't schedule probe-phase tasks until the build phase has finished — favoring memory efficiency for batch workloads. Task scheduling categorizes stages as leaf (reading data from a connector, placed with network and connector constraints in mind) or intermediate (processing other stages' results, placeable on any worker, and eligible to run only once all upstream tasks finish).

Splits — chunks of external data — are enumerated lazily: the coordinator sets up tasks for the workers first, then asks connectors to enumerate splits in small batches and assigns them as they arrive, rather than eagerly loading a full split list. This buys several things at once: queries with filters or a LIMIT that don't need to process all the data can be canceled early; the time to first result is decoupled from the total time to enumerate every split, which matters when a connector like Hive can take a while just to list all partitions and files; lazy enumeration avoids holding every split's metadata in memory, so a Hive connector can handle millions of splits; and the coordinator assigns splits to whichever worker task has the shortest queue, which keeps queues small and absorbs variation in split size and worker performance.

At execution time, a thread loops over a split, and the unit of data it operates on is a page — a columnar encoding of a sequence of rows. Workers exchange data between each other through in-memory buffered shuffles over HTTP, where a worker stores its produced data in memory and other workers pull it by polling; the engine tunes parallelism to keep output and input buffer utilization within a target range, since full output buffers stall a split's execution and hog memory, while underused input buffers add processing overhead for no benefit. For writing results, Presto uses an adaptive approach that increases writer concurrency dynamically.

*See also: [[presto]] · [[presto-resource-management-and-fault-tolerance]] · [[presto-columnar-execution-optimizations]]*

## Related in the other wiki
- [[Parallel Query Execution]] — DDIA's general account of MPP query engines decomposing a query into parallel stages across partitions is the same shape as this note's inter-node/intra-node parallelism split, worked out at Presto's own level of mechanical detail.
