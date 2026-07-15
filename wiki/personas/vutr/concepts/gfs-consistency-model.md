---
persona: vutr
kind: concept
sources:
- raw/amazon-s3-gfs-hdfs-distributed-file-systems-additional/i-spent-8-hours-reading-the-paper.md
last_updated: '2026-07-15'
qc: passed
slug: gfs-consistency-model
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

GFS defines file-region state after a mutation along two axes: whether it's *consistent* (all clients see the same data regardless of which replica they read) and whether it's *defined* (clients see exactly what the mutation wrote, in its entirety). Definedness implies consistency, but not the reverse. A mutation that succeeds with no concurrent writers leaves the region defined (and therefore consistent). Concurrent successful mutations leave the region consistent but *undefined* — every client sees the same bytes, but those bytes may be a mix of fragments from multiple mutations rather than reflecting any single one cleanly. A failed mutation leaves the region *inconsistent* — different clients can see different data at different times.

Two mutation types get different guarantees: a `write` places data at a caller-specified offset, while a `record append` ([[gfs-record-append]]) lets GFS choose the offset and guarantees at-least-once atomic append even under concurrency. After a sequence of successful mutations, GFS still guarantees the mutated region is *defined*, and it achieves this two ways: applying every mutation to a chunk's replicas in the *same order* on all of them, and using a per-chunk **version number** to detect replicas that went stale because they missed mutations while their chunkserver was down — stale replicas are excluded from serving reads or accepting further mutations, and GFS garbage-collects them as soon as possible. Component failures that corrupt or destroy data after a successful mutation are handled separately: HeartBeat-based failure detection plus checksumming catch the failure, and GFS restores from a valid replica quickly.

The practical implication for applications, which Vu draws out explicitly: build around GFS's consistency model rather than fighting it. Typical patterns are relying on appends over overwrites, periodic checkpointing (a writer creates a file end-to-end, then renames it to a permanent name or records how much has been successfully written so readers only process up to the last checkpoint), and writing self-validating, self-identifying records with embedded checksums so a reader can detect and discard padding or duplicate fragments left behind by record append's at-least-once semantics.

*See also: [[gfs]] · [[gfs-record-append]] · [[gfs-lease-and-write-pipeline]] · [[gfs-metadata-and-operation-log]]*
