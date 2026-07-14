---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 10
chapter_title: Batch Processing
topic: MapReduce and Distributed Filesystems
type: subtopic
tags: [ddia, mpp-databases, data-lake, fault-tolerance]
sources:
  - raw/ch10.md
---
# Comparing Hadoop to Distributed Databases
> [[Hadoop]] rediscovered algorithms MPP databases had for a decade — its real novelty is being a general-purpose "distributed Unix" that tolerates any data format, any processing model, and frequent task deaths.

## The Idea
Nothing in the [[MapReduce]] paper's parallel joins was new: massively parallel processing (MPP) databases — Gamma, Teradata, Tandem NonStop SQL — had implemented them years earlier. The decisive difference is scope. MPP databases parallelize *analytic SQL* over a tightly integrated engine; Hadoop pairs [[HDFS]] with MapReduce into something closer to a general-purpose operating system that runs arbitrary programs. Three design axes separate them.

## How It Works
**Diversity of storage.** Databases demand a data model up front; HDFS files are just bytes — records, text, images, sensor readings, genome sequences. Hadoop legitimized dumping raw data first and deciding how to process it later (the "data lake"; the *sushi principle*: raw data is better). Interpretation shifts to the consumer — schema-on-read — which suits organizations where producers and consumers are different teams. Speedy indiscriminate collection beats careful up-front modelling in practice, and Hadoop often plays the ETL role: raw dumps in, [[MapReduce]] cleanup, load into an MPP warehouse (see [[Data Warehousing]]).

**Diversity of processing models.** An MPP database is monolithic — storage layout, planner, scheduler, execution co-tuned — and SQL fits analysts and tools like Tableau. But ML training, relevance ranking, and image analysis don't decompose into SQL; they need code. On one shared cluster over the same files, Hadoop can host SQL (Hive), MapReduce, and later engines side by side — even the random-access OLTP store HBase and the MPP-style Impala coexist on HDFS without moving data.

**Designing for frequent faults.** An MPP database usually aborts a whole query on a node crash and retries it — fine for second-to-minute queries — and prefers keeping data in memory. MapReduce retries at individual-task granularity and eagerly spills to disk: right for huge, hours-long jobs, and, more deeply, right for Google's environment, where batch tasks run at low priority on mixed-use clusters and get preempted whenever production services need resources. A one-hour Google task faces roughly a 5% termination risk — an order of magnitude above hardware failure rates. Task-level recovery exists to enable aggressive resource overcommitment, not because disks are flaky.

## Trade-offs & Pitfalls
- Raw-first collection transfers the data-quality burden downstream; "available now" beats "clean later" only if consumers can cope.
- MapReduce's disk-heavy conservatism is wasted where preemption is rare — open-source schedulers (YARN, Mesos, Kubernetes) mostly lack general priority preemption, which is exactly why [[Beyond MapReduce]] engines choose differently.

## Examples & Systems
Gamma, Teradata, Tandem NonStop SQL (MPP pioneers); Hive, HBase, Impala; Google's Borg-style preemptive scheduling versus YARN's CapacityScheduler.

## Related
- up: [[MapReduce and Distributed Filesystems]] · chapter: [[Ch 10 - Batch Processing]]
- [[High-Level APIs and Languages]] — the later convergence of both camps
- [[Transaction Processing or Analytics]] — the OLTP/OLAP split this comparison extends
- [[MapReduce Job Execution]] — the task-granular retry machinery referenced here
