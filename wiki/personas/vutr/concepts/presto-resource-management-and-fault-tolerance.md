---
persona: vutr
kind: concept
sources:
- raw/history-of-data-engineering-and-hadoop-ecosystem/8-minutes-to-understand-presto.md
last_updated: '2026-07-15'
qc: passed
slug: presto-resource-management-and-fault-tolerance
topics:
- history-of-data-engineering
---

Presto is built for multitenant deployments — a single cluster handling hundreds of concurrent queries — and its CPU scheduling reflects that goal directly: Facebook designed it to maximize overall cluster throughput by prioritizing total CPU time spent processing data. Presto uses a cooperative multitasking model, scheduling concurrent tasks on every worker node; a given split can only run on a thread for a maximum time slice called a quantum, after which the thread stops processing that split whether or not it finished, so no single split can monopolize a worker's resources. If a task exceeds its quantum, the scheduler "charges" it for the thread time used, which temporarily reduces how often it gets scheduled going forward. Rather than predicting a task's resource needs up front, Presto classifies tasks by the CPU time they've already accumulated: the more CPU a task uses, the higher a queue level it moves into, and each level receives a configurable fraction of available CPU time. Less demanding queries accumulate less CPU time, stay in lower queue levels, and keep getting resources readily — which reflects an explicit expectation that users want fast responses for interactive queries while being less sensitive about how long an intensive batch job takes to return.

Memory is handled as two separate categories: user memory, which is usage a user can estimate from their own understanding of the query and data, and system memory, usage created by implementation choices like shuffle buffers. Presto enforces separate limits on user memory and on total (user plus system) memory, and kills a query outright if it requires more memory than the whole cluster or a single node's per-node limit allows — a design that gives operators flexibility to manage very different workloads side by side. When a worker's memory is exhausted, Presto halts task processing on that node and falls back on two strategies: spilling, where Presto revokes memory from eligible tasks by writing their in-memory state to disk, prioritizing the longest-running tasks first (this increases query response time, which is exactly why Facebook doesn't enable it by default — users there value the predictable latency of pure in-memory execution); and the reserved pool, where the node's memory is split into a general pool and a reserved pool, and a query promoted into the reserved pool has its usage counted against that pool instead of competing with every other query for the general one.

Fault tolerance in Presto is notably thin at the protocol level and pushed onto external mechanisms instead. If the coordinator fails, the entire cluster becomes unavailable; if a worker node crashes, every query running on it fails outright. Facebook's mitigations are all operational rather than built into Presto itself: standby coordinators ready to take over if the primary fails, multiple active Presto clusters so a failed cluster's queries can be redirected to another one, and external monitoring systems that identify failing nodes and remove them from the cluster. These reduce downtime but don't eliminate it — implementing traditional fault-tolerance techniques like checkpointing or replication inside Presto is described as challenging and resource-intensive, and at the time the underlying paper was written, Facebook was still working to improve fault tolerance specifically for long-running queries.

*See also: [[presto]] · [[presto-coordinator-worker-scheduling]] · [[presto-columnar-execution-optimizations]]*
