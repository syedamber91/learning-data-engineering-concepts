---
persona: vutr
kind: concept
sources:
- raw/amazon-s3-gfs-hdfs-distributed-file-systems-additional/amazon-s3-for-data-engineers.md
last_updated: '2026-07-15'
qc: passed
slug: object-storage-durability-erasure-coding
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

S3's famous eleven-nines (99.999999999%) durability figure rests on two distinct mechanisms working together: end-to-end data integrity checking, and redundant storage via erasure coding.

For integrity, S3 computes a checksum when an object is uploaded (clients may choose the algorithm and can supply their own pre-calculated checksum for S3 to compare against). If the client-provided and S3-calculated checksums don't match, S3 rejects the upload outright as corrupted in transit; if they match, the checksum is stored as immutable object metadata. On download, the client can independently recompute the checksum and compare it against the stored value to confirm nothing was corrupted at rest or in transit.

For redundancy, S3 uses **erasure coding** rather than naive full-copy replication. An object is split into X primary fragments; Y additional parity fragments are mathematically generated from them (e.g., via Reed-Solomon codes); the X+Y fragments are then distributed across storage nodes, and the original data can be reconstructed from the surviving fragments as long as no more than Y fragments are lost. The efficiency argument is explicit in Vu's numbers: naive N-way replication costs N times the original storage (3-way replication = 300% overhead), while a typical erasure-coding configuration like (X=4, Y=2) needs only 150% of the original size for a comparable loss tolerance. Amazon tunes its own X/Y configuration to hit the eleven-nines target; Google Cloud Storage uses the same erasure-coding approach for its own durability guarantee.

*See also: [[amazon-s3]] · [[s3-strong-consistency]] · [[s3-atomicity-and-conditional-writes]] · [[gfs-replica-management-and-fault-tolerance]]*
