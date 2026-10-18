---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 11
chapter_title: Batch Processing
type: topic
tags: [ddia2, distributed-operating-system, storage, scheduler]
sources:
  - raw/ch11.md
---
# Batch Processing in Distributed Systems
The machine running the Unix example has **three components working together:**
- **Storage devices accessed through the operating system's filesystem interface.**
- **A scheduler determining when processes run and how to allocate CPU.**
- **A series of Unix programs whose stdin and stdout are connected by pipes.**

**These same components exist in distributed data processing frameworks. In fact, you can think of these frameworks as distributed operating systems: they have filesystems, job schedulers, and programs that send data to one another through the filesystem or other communication channels.**

## Subtopics
- [[Distributed Filesystems (2e)]] — the storage layer, layer by layer against its local counterpart.
- [[Object Stores (2e)]] — the storage layer that increasingly replaces it, and how it differs.
- [[Distributed Job Orchestration (2e)]] — the kernel analogue: executors, resource manager, scheduler, workflows, faults.

## Key Takeaways
- **The operating-system analogy is the organising idea of this topic** and it holds surprisingly precisely: block devices → data nodes, page cache → data node page caches, filesystem metadata → NameNode, VFS → the DFS protocol, kernel scheduler → job orchestrator, pipes → shuffle.
- The analogy also predicts the failure modes: **resource allocation, fairness, and preemption are scheduler problems**, and **fault tolerance is a filesystem replication problem**, which is exactly how the subtopics divide.
- **The storage layer is where the biggest change since the 1st edition happened** — the shift from HDFS to object stores, which have genuinely different APIs, performance, and consistency guarantees.

## Since the 1st Edition
The 1st edition made the same operating-system analogy but organised this material as [[MapReduce and Distributed Filesystems]], treating HDFS as the storage layer and MapReduce as the execution layer in one topic. **The 2nd edition separates storage from computation entirely** — this topic covers storage and orchestration, while [[Batch Processing Models (2e)]] covers computation — **and adds object stores and job orchestration as first-class subtopics.**

## Related
- chapter: [[Ch 11 - Batch Processing (2e)]]
- [[Batch Processing with Unix Tools (2e)]] — the single-machine version of these components
- [[Batch Processing Models (2e)]] — the computation layer
- 1st edition: [[MapReduce and Distributed Filesystems]] — the closest predecessor
