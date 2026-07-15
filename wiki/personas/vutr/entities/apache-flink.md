---
persona: vutr
kind: entity
sources:
- raw/flink-additional/apache-flink-overview.md
- raw/flink-additional/i-spent-8-hours-understanding-which.md
last_updated: '2026-07-15'
qc: passed
slug: apache-flink
topics:
- flink
---

Straight from its homepage, quoted by Vu: Apache Flink is "a framework and distributed processing engine for stateful computations over unbounded and bounded data streams." The distinction that matters against Spark is philosophical: Spark treats bounded data as the first-class citizen and aligns stream data into micro-batches, while for Flink everything is a stream — batch is just a special case. Users express processing logic through Flink's APIs, then deploy the resulting application on a cluster environment such as YARN or Kubernetes. If the source is Kafka, Google Cloud Pub/Sub, or Amazon Kinesis and the goal is to consume it, apply logic, and route the result somewhere else, Flink is the tool Vu reaches for.

A typical Flink setup has four components, all JVM processes: the **Dispatcher** exposes a REST interface for submitting applications and runs a dashboard on job executions; the **JobManager** is the per-application master that converts the submitted logical dataflow graph into a physical graph of parallelizable tasks, then coordinates execution (including checkpointing); the **ResourceManager** is provider-specific (YARN, Kubernetes) and manages TaskManager slots, requesting more TaskManager processes from the provider when the JobManager needs more than are currently idle; and **TaskManagers** are the workers, each offering a fixed number of slots that cap how many tasks it can run concurrently. Vu draws the analogy directly to Spark's own cluster model: JobManager ~ Spark's Driver, ResourceManager ~ Spark's Cluster Manager, TaskManagers ~ Spark's executors.

The submission flow: a TaskManager registers its slots with the ResourceManager on startup; an application (a logical dataflow graph plus a JAR of dependencies) is submitted to the Dispatcher, which starts a JobManager; the JobManager converts the logical plan to a physical one and requests the needed slots from the ResourceManager, which offers idle TaskManager slots or asks the resource provider to spin up more TaskManagers; once slots are granted, the JobManager distributes physical-graph tasks to them and TaskManagers begin executing.

A single TaskManager can run multiple tasks at once — subtasks of the same operator (each handling a data partition), tasks from different operators, or even tasks from different applications entirely — executed in a multi-threaded model within one JVM (**slot sharing**). This is a deliberate resource-utilization trade: packing more tasks into shared slots uses hardware more efficiently, but tasks sharing a TaskManager can't isolate their resource use from each other. Users who prioritize isolation over utilization can configure one task slot per TaskManager instead.

*See also: [[flink-memorysegments]] · [[chandy-lamport-checkpointing]] · [[watermark]] · [[windowing-triggers-and-late-events]] · [[flink-networking-and-flow-control]] · [[flink-state-management-and-backends]]*
