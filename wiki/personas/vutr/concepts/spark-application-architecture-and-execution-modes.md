---
persona: vutr
kind: concept
sources:
- raw/spark/the-overview-of-apache-spark.md
- raw/spark/if-youre-learning-apache-spark-this.md
- raw/spark/is-this-feature-a-revolution-in-spark.md
last_updated: '2026-07-11'
qc: passed
slug: spark-application-architecture-and-execution-modes
topics:
- spark
---

The confusion people hit first: the cluster manager has its *own* "driver" (sometimes called master) and "worker" abstractions, and these are tied to physical machines -- not to Spark processes. Keep the two layers separate. A Spark application is: **Driver** (the JVM process that manages the whole application -- handles user input, plans execution, distributes tasks), **Cluster Manager** (oversees the machines the app runs on -- YARN, Mesos, or Spark's own standalone manager), and **Executors** (processes that execute the tasks the driver assigns and report status/results back; each application gets its own executors, and a single worker node can host more than one executor).

Later framing sharpens this split further: call the driver+executors the **Spark cluster**, and the physical machines that provide resources to it the **resource cluster**. The resource cluster is managed by the cluster manager and hosts the "workers" that can run driver and executor processes. This is the same distinction as the driver/master-worker note above, just named more explicitly.

**Execution modes** are distinguished by *where the driver process lives*:

- **Cluster mode**: the driver is launched on a worker node inside the resource cluster, alongside the executors. The cluster manager owns every process involved.
- **Client mode**: the driver stays on the client machine that submitted the app. That client machine has to keep the driver process alive for the entire run.
- **Local mode**: the whole application runs on one machine, parallelism comes from threads. Used for learning Spark or testing.

**The mechanism, step by step** (cluster mode, a DataFrame-API app):

1. The user writes the app; every app must construct a `SparkSession` -- the single entry point into all of Spark's functionality.
2. The client submits the app (a pre-compiled JAR) to the cluster manager and, in the same step, requests the driver's resources.
3. The cluster manager accepts the submission and places the driver process on one of the worker nodes.
4. The `SparkSession` then asks the cluster manager to launch the executors -- the user controls how many executors and their configuration.
5. The cluster manager launches the executor processes and reports their locations back to the driver.
6. Before anything runs, the driver builds an execution plan: it starts as a **logical plan** (the intended transformations) and is refined through several steps into a **physical plan** (the concrete execution strategy) -- see [[catalyst-optimizer-phases]].
7. The driver schedules tasks onto the executors; each executor reports task status back to the driver.
8. When the app finishes, the driver exits (success or failure) and the cluster manager tears down that app's executors.
9. The client can poll the cluster manager for the application's status at any point.

**Spark Connect is the same mechanism with the driver relocated and decoupled.** Instead of a client owning a driver process (client mode) or submitting one into the resource cluster (cluster mode), Spark Connect stands up a long-running server that hosts the Spark cluster continuously and exposes a gRPC endpoint. Each client opens its own session against that server (not a `SparkSession` in the traditional sense -- calling `SparkSession` in Connect returns a different kind of object, and you use `.remote(...)` instead of `.master(...)`). For every job, the client turns its DataFrame calls into an *unresolved logical plan*, encodes it with protobuf, and ships it over gRPC; the server-side driver analyzes, optimizes, and physically plans it exactly as before, schedules it on its executors, and streams results back as Apache Arrow record batches. In the author's words: "running the Spark application in client mode, except that we don't need to manage the driver process ourselves."

The payoff is a genuinely thin client -- the Python Connect client needs no JARs or JRE, just the library -- and a driver that can be upgraded independently of every client using it. The cost is real: Connect covers less API surface (no RDD or SparkContext access), and the client cannot adjust the remote cluster's CPU/RAM at connection time -- resources are fixed when the Connect server itself is started, and every client sharing that server competes for the same pool, so one heavy job degrades everyone else's. In the author's test rig, a standalone resource cluster with 3 workers (2 CPUs / 1GB RAM each) backed a Connect server exposing port 4040 for the Spark UI and 15002 for client gRPC traffic.
