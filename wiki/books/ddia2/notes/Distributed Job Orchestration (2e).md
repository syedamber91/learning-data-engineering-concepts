---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 11
chapter_title: Batch Processing
topic: Batch Processing in Distributed Systems
type: subtopic
tags: [ddia2, yarn, kubernetes, scheduler, gang-scheduling, airflow, spot-instances]
sources:
  - raw/ch11.md
---
# Distributed Job Orchestration
> On one machine the kernel decides what runs where. In a cluster that's the orchestrator's job — and the hard part is allocating limited resources among jobs with competing needs.

## The Idea
**When you execute a Unix batch job, something must actually run the `awk`, `sort`, `uniq`, and `head` processes**: transfer data between them, allocate memory, schedule instructions fairly on the CPU, enforce memory and I/O boundaries. **On a single machine the kernel does this. In a distributed environment, this is the role of a job orchestrator.**

Batch frameworks **send a request to an orchestrator's scheduler**, containing metadata such as: **the number of tasks; memory, CPU, and disk needed per task; a job identifier; access credentials; job parameters such as input and output data; required hardware details such as GPUs or disk types; and the location of the job's executable code.**

## How It Works
**Orchestrators such as Kubernetes and Hadoop YARN combine this with cluster metadata using three components:**

**Task executors.** **A daemon such as YARN's NodeManager or Kubernetes's kubelet runs on each node**, responsible for **running job tasks, sending heartbeats to signal liveness, and tracking task status and resource allocation.** On a task-start request it **retrieves the executable code and runs a command to start the task**, then **monitors the process until it finishes or fails and updates the status.** **Many executors also work with the OS to provide security and performance isolation** — **YARN and Kubernetes use Linux cgroups** — **preventing tasks from accessing data without permission or hurting other tasks' performance by using excessive resources.**

**Resource manager.** **Stores metadata about each node** — available CPUs, GPUs, memory, disks; task statuses; network location; node status — **providing a global view of the cluster's state.** **Its centralized nature can lead to scalability and availability bottlenecks.** **YARN uses ZooKeeper and Kubernetes uses etcd to store cluster state.**

**Scheduler.** **Receives requests to start, stop, or check jobs** — for instance to start a job with 10 tasks using a specific Docker image on nodes with a specific GPU — and **uses the request plus the resource manager's state to determine which tasks run on which nodes**, then informs the executors.

> **Scheduling sometimes requires application-specific schedulers** taking particular requirements into account, such as autoscaling read replicas past a query threshold. **The centralized scheduler and application-specific schedulers work together.** **YARN calls its subschedulers ApplicationMasters; Kubernetes calls them operators.**

**Resource allocation.** Schedulers must **optimally allocate limited resources among jobs with competing needs, balancing fairness and efficiency.** The book's example: **a five-node cluster with 160 CPU cores receives two job requests, each wanting 100 cores.**
- **Run 80 tasks for each job**, starting the remaining 20 each as earlier tasks complete.
- **Run all of one job's tasks, starting the second only when 100 cores are free** — **gang scheduling**.
- **If the second request arrives much later, the scheduler has incomplete information**: allocate all 100 to the first job, **or hold some back in anticipation of a future job that might never come?**

**Even this simple example shows difficult trade-offs.** **Under gang scheduling, if the scheduler reserves cores until all 100 are simultaneously available, nodes sit idle, utilization drops, and a deadlock might occur if other jobs also reserve cores.**

**Scheduling workflows.** **The Unix example chained several commands; the same pattern arises in distributed batch processes** — **the output of one job becomes the input to one or more others, and each job may have several inputs produced by other jobs. This is a workflow, or directed acyclic graph (DAG) of jobs.**

> **Note the terminology clash:** in durable execution, "workflow" means **a sequence of steps typically performing RPCs.** **In batch processing it means a sequence of batch processes, each taking input data and producing output data, normally not making RPCs to external services.** **Durable execution engines typically process less data per request, though the line is fuzzy.**

**Reasons for a multi-job workflow:** **output needed by several other jobs maintained by different teams** — best written to a location all can read; **transferring data between processing tools** — a Spark job outputs to HDFS, a Python script triggers a Trino query that processes those files and outputs to S3; and **pipelines internally requiring multiple stages** — if one stage shards by one key and the next by a different key, the first can output data sharded as the second requires.

**In Unix the pipe uses only a small in-memory buffer**, and **if it fills, the producer waits until the consumer reads — a form of backpressure.** **Spark, Flink, and others support a similar model where one task's output passes directly to another, over the network if on different machines.** **But it is more typical for a job to write its output to a distributed filesystem or object store and for the next to read from there** — **decoupling the jobs so they can run at different times.** **If a job has several inputs, a workflow scheduler typically waits until all producing jobs complete successfully.**

**Orchestration schedulers such as YARN's ResourceManager or Spark's built-in scheduler do not manage entire workflows — they schedule per job.** **To handle dependencies, workflow schedulers such as Airflow, Dagster, and Prefect exist**, with **management features useful for large collections of batch jobs.** **Workflows of 50 to 100 jobs are common, and in a large organization many teams run jobs reading one another's output across many systems — tool support is important for managing such complex dataflows.**

## Trade-offs & Pitfalls
**Handling faults.** **Long-running jobs with many parallel tasks are likely to experience at least one task failure**, from hardware faults or network interruptions.

**Another reason a task might not finish is that the scheduler intentionally preempts (kills) it.** **Preemption is particularly useful with multiple priority levels** — cheap low-priority tasks running on spare capacity, **at risk of being preempted at any moment if a higher-priority task arrives.** **These cheaper VMs are spot instances on EC2, spot virtual machines on Azure, and preemptible instances on Google Cloud.**

**Since batch processing is often not time-sensitive, it is well suited to low-priority tasks and spot instances, reducing cost by using spare resources that would otherwise be idle and increasing cluster utilization.** **But those tasks are more likely to be killed, because preemptions occur more frequently than hardware faults.**

**Since batch jobs regenerate their output from scratch, task failures are easier to handle than in online systems**: **delete the partial output from the failed execution and reschedule the task on another machine.** **Rerunning the entire job for a single task failure would be wasteful, so MapReduce and its successors keep parallel tasks independent, allowing retry at the granularity of an individual task.**

**Fault tolerance is trickier when one task's output becomes another's input.** **MapReduce solves this by always writing intermediate data back to the DFS and waiting for the writing task to complete before allowing reads** — **which works even where preemption is common, but means a lot of writes to the DFS, which can be inefficient.** **Spark keeps intermediate data in memory (spilling to local disk if it won't fit) and writes only the final result to the DFS, tracking how the intermediate data was computed so it can recompute it if lost.** **Flink uses a different approach based on periodically checkpointing a snapshot of tasks.**

## Examples & Systems
Kubernetes and YARN; NodeManager and kubelet; Linux cgroups; ZooKeeper and etcd for cluster state; ApplicationMasters and operators; Airflow, Dagster, Prefect; EC2 spot instances, Azure spot VMs, GCP preemptible instances.

## Since the 1st Edition
**Substantially new.** The 1st edition discussed MapReduce job execution and workflow schedulers (Oozie, Azkaban, Luigi, Airflow, Pinball) inside its MapReduce topic, but **had no systematic treatment of orchestration as a layer** — no executor/resource-manager/scheduler decomposition, no resource allocation trade-offs, no gang scheduling, and no spot instances. **The fault-handling material carries over** (task-granularity retry, MapReduce writing intermediates to HDFS versus Spark's lineage-based recomputation and Flink's checkpointing) but is relocated here from the 1st edition's "Materialization of Intermediate State" discussion.

## Related
- up: [[Batch Processing in Distributed Systems (2e)]] · chapter: [[Ch 11 - Batch Processing (2e)]]
- [[Durable Execution and Workflows (2e)]] — the other meaning of "workflow"
- [[Dataflow Engines (2e)]] — where the fault-tolerance strategies differ
- [[Coordination Services (2e)]] — ZooKeeper and etcd holding cluster state
