---
persona: vutr
kind: concept
sources:
- raw/amazon-s3-gfs-hdfs-distributed-file-systems-additional/i-spent-8-hours-reading-the-paper-523.md
last_updated: '2026-07-15'
qc: passed
slug: hdfs-client-read-write-and-lease
topics:
- amazon-s3-gfs-hdfs-and-distributed-file-systems
---

HDFS implements a **single-writer, multiple-reader** model: once a file is closed after being written, its content cannot be changed or removed — the only way back in is reopening it for an *append*. A file can have many concurrent readers, but only one client at a time may hold the write **lease** for it. The lease-holding client keeps its exclusivity by periodically renewing via heartbeat to the NameNode. Two limits bound the lease's lifetime: while the *soft limit* holds, the writer has exclusive access outright; if the soft limit expires and the client hasn't closed the file or renewed, another client can take over the lease; if the *hard limit* also expires with no renewal, HDFS assumes the original client has quit and closes the file on the writer's behalf. The lease only constrains writes — reads are unaffected by who holds it.

For **writes**, when a new block is needed the NameNode allocates a unique block ID and picks the DataNodes to host its replicas, forming them into a pipeline chosen to minimize total network distance from client to the last DataNode in the chain. Bytes the application writes are first buffered client-side, then pushed into the pipeline once a packet buffer (typically 64KB) fills — and critically, the *next* packet can enter the pipeline before the previous one's acknowledgment has come back, which is what keeps the pipeline saturated rather than round-tripping packet by packet. HDFS only guarantees a new reader can see the written data once the file is *closed* — not incrementally as blocks are written. To guard against corruption, the client computes a checksum for each block at write time and sends it alongside the data; the DataNode stores that checksum as separate metadata.

For **reads**, the client fetches block-replica locations from the NameNode ordered by distance, trying the closest first and falling back to the next replica in that order if a read fails. Reading a file that's still being written is explicitly supported: since the NameNode doesn't yet know the final length of the last (in-progress) block, the client asks one of the replicas directly for the current length before starting to read. On every read, the DataNode returns both the block's data and its stored checksums; the client recomputes and compares, and if they don't match it reports the corruption to the NameNode and retries against a different replica.

*See also: [[hdfs]] · [[hdfs-datanode-handshake-and-heartbeat]] · [[hdfs-block-placement-and-replication-management]] · [[gfs-lease-and-write-pipeline]]*
