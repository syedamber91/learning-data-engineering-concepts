---
persona: vutr
kind: concept
sources:
- raw/amazon-s3-gfs-hdfs-distributed-file-systems-additional/i-spent-8-hours-reading-the-paper.md
last_updated: '2026-07-15'
qc: passed
slug: gfs-lease-and-write-pipeline
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

GFS needs a consistent mutation order applied identically across every replica of a chunk, and it gets that with a **lease** mechanism rather than having the master arbitrate every write. The master grants a chunk lease to one replica — the **primary** — which then picks the serial order for all mutations to that chunk; every replica, primary and secondary alike, must apply mutations in that order. This design choice exists specifically to minimize the master's management overhead: once a lease is granted, the master is out of the loop for ordering decisions on that chunk. The lease defaults to a 60-second timeout, extendable on the primary's request, and the master can revoke it early in some cases (e.g., to halt mutations on a file being renamed); if the master loses contact with the primary, it can grant a new lease to a different replica once the old one expires.

The write path Vu walks through the paper's own figure has seven steps, and it deliberately separates *control* flow from *data* flow: (1) the client asks the master which chunkserver holds the current lease and where the other replicas are; (2) the master replies with the primary's identity and the secondaries' locations; (3) the client pushes the actual data to all replicas, in any order — critically, none of the replicas apply it as a mutation yet, they just hold it; (4) once all replicas have acknowledged receiving the data, the client sends the *write request* to the primary; (5) the primary forwards the write request to all secondaries; (6) the secondaries reply to the primary confirming completion; (7) the primary replies to the client. If a write is too large, the GFS client code itself splits it into multiple such write operations.

Separately from this control flow, **data** is pushed along a linear chain of chunkservers in a pipelined fashion — not via some network topology like a tree — which is what lets GFS use network bandwidth efficiently: each machine forwards bytes to the next in the chain as soon as it has them, rather than the client fanning data out to every replica itself.

*See also: [[gfs]] · [[gfs-record-append]] · [[gfs-consistency-model]] · [[gfs-replica-management-and-fault-tolerance]]*
