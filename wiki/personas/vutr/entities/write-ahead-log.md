---
persona: vutr
kind: entity
sources:
- raw/lsm-tree-storage-engines-additional/i-spent-the-weekend-learning-about.md
last_updated: '2026-07-15'
qc: passed
slug: write-ahead-log
topics:
- change-data-capture-cdc-and-data-sourcing
- lsm-tree-storage-engines
---

The Write-Ahead Log exists because the Memtable half of an LSM-tree is not durable: it lives in RAM, and a crashed machine loses whatever is still sitting in memory. The WAL is a separate, append-only file on disk that records every operation before it's allowed to touch the Memtable — which is where the name comes from — and Vu is explicit that this is not an LSM-only trick; it's a common durability technique shared with B-Tree engines too.

Its place in the write path is the first of four steps: (1) the operation — INSERT, UPDATE, or DELETE — is serialized and appended to the WAL, and the system confirms it's persisted before moving on; (2) only once that WAL write is confirmed does the data get ingested into the active Memtable; (3) with the write now durable in both the WAL and the Memtable, the system returns a success acknowledgement to the client — from the client's point of view, the write is done; (4) later, when the Memtable fills up and is flushed to a new [[sstable]] on disk, the WAL records covering that now-persisted data can finally be dropped, which is what keeps the WAL file from growing without bound.

The payoff shows up on crash recovery: if the machine goes down, the [[memtable]] is gone, but the data can be rebuilt by replaying the WAL, whose records essentially say "here are all the operations we intended to perform on the Memtable." Writing to the WAL is treated as an unavoidable cost paid by both storage families alike — Vu notes explicitly that this step is set aside when comparing LSM-tree and B-Tree write costs, since both engines pay it; the real difference between them is what happens after, where the LSM-tree's Memtable flush is a sequential write rather than the B-Tree's in-place page overwrite.

*See also: [[memtable]] · [[sstable]] · [[sequential-vs-random-io]] · [[b-tree]] · [[log-based-cdc]] · [[read-replica]]*

## Related in the other wiki
- [[Write-Ahead Log]] — DDIA traces the same "record before applying" principle back to B-tree crash recovery and forward to replication logs and CDC — the general form of the durability guarantee this note grounds specifically in Vu's LSM-tree write path.
