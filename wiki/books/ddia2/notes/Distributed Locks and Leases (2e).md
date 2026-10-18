---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 9
chapter_title: The Trouble with Distributed Systems
topic: Knowledge, Truth, and Lies
type: subtopic
tags: [ddia2, fencing-token, lease, zombie, stonith, conditional-write]
sources:
  - raw/ch09.md
---
# Distributed Locks and Leases
> You cannot prevent a zombie from believing it still holds the lease. You can only make sure its writes are rejected — and a monotonically increasing token is how.

## The Idea
**Locks and leases in distributed applications are prone to misuse and are a common source of bugs.** A **lease** is a lock that times out and can be reassigned if the old owner stops responding — crashed, paused too long, or disconnected. **Use leases when a system requires there to be only one of something:**
- **Only one node may be leader for a database shard**, to avoid split brain.
- **Only one transaction or client may update a particular resource**, to prevent corruption by concurrent writes.
- **Only one node should process a given input file** in a big processing job, to avoid wasted duplicate effort.

**It is worth thinking carefully about what happens if several nodes simultaneously believe they hold the lease.** **In the third case the consequence is only wasted computational resources — not a big deal. In the first two, the consequence could be lost or corrupted data, which is much more serious.**

## How It Works
**Two ways this corrupts data**, both real:

**Pause.** You want a file in a storage service accessible by only one client at a time. Clients must obtain a lease from a lock service (**often implemented using a consensus algorithm**) before accessing it. **If the client holding the lease is paused for too long, its lease expires.** Another client obtains the lease and starts writing. **When the paused client comes back, it believes it still has a valid lease and continues writing — split brain, and the writes clash and corrupt the file.** **The bug is not theoretical; HBase used to have this problem.**

**Delayed request.** No pause at all, just a crash. **Just before client 1 crashes it sends a write request, but the request is delayed for a long time in the network** — recall that packets can be delayed by a minute or more. **By the time it arrives, client 1's lease has timed out, client 2 has acquired it and issued its own write. The result is the same corruption.**

**Fencing off zombies.** **A zombie is a former leaseholder that has not yet found out it lost the lease and is still acting as if it were current.** **Since we cannot rule out zombies entirely, we must instead ensure they can't do any damage** — **fencing off the zombie.**

**Some systems try to fence by shutting the zombie down** — disconnecting it from the network, shutting down the VM via the cloud provider's management interface, or physically powering down the machine. **This is sometimes called shoot the other node in the head (STONITH)**, terminology the book says it prefers not to use. **In any case it is not particularly effective**: **it does not protect against the large network delays** of the second scenario; **all the nodes could shut one another down**; and **by the time a zombie has been detected and shut down it may be too late and data may already be corrupted.**

**The robust solution — fencing tokens — protects against both zombies and delayed requests.** **Every time the lock service grants a lock or lease, it also returns a fencing token: a number that increases every time a lock is granted.** **Every write request to the storage service must include the client's current fencing token.**

Client 1 acquires the lease with token **33**, then pauses and the lease expires. Client 2 acquires it with token **34** and writes, including the token. **Later client 1 revives and writes with token 33 — but the storage service remembers it has already processed a write with a higher token, so it rejects the request.** **A client that has just acquired the lease must immediately make a write, and once that completes, any zombies are fenced off.** The operation resembles optimistic concurrency control, **except that fencing is permanent while concurrency control failures can be retried.**

> **Other names for fencing tokens:** in **Chubby**, Google's lock service, they are **sequencers**; in **Kafka** they are **epoch numbers**; in consensus algorithms the **ballot number (Paxos)** or **term number (Raft)** serves a similar purpose.

**Implementations:** with **ZooKeeper** you can use the transaction ID `zxid` or node version `cversion`; with **etcd** the revision number plus lease ID; **Hazelcast's FencedLock API** explicitly generates a token.

**The storage service needs some way to check whether a write is based on an outdated token.** **Alternatively it is sufficient for the service to support a write that succeeds only if the object hasn't been written by another client since the current client last read it** — an atomic CAS. **Object storage services support such a check**: **Amazon S3 calls it conditional writes, Azure Blob Storage calls it conditional headers, Google Cloud Storage calls it request preconditions.**

## Trade-offs & Pitfalls
**Fencing with multiple replicas.** **If your clients need to write to only one storage service that supports conditional writes, the lock service is somewhat redundant** — the lease assignment could have been implemented directly on that storage service. **But once you have a fencing token, you can use it with multiple services or replicas and ensure the old leaseholder is fenced off on all of them.**

Imagine a **leaderless replicated key-value store with LWW conflict resolution**, where the client writes directly to each replica and each independently accepts or rejects based on a client-assigned timestamp. **Put the writer's fencing token in the most significant bits of the timestamp.** Then **any timestamp generated by the new leaseholder is greater than any from the old one, even if the old leaseholder's writes happened later.**

Client 2 with token 34 produces timestamps starting `34…`, greater than client 1's `33…`. **Client 2 writes to a quorum but can't reach replica 3, so zombie client 1's later write may succeed at replica 3 even though replicas 1 and 2 ignore it. This is not a problem**: a subsequent quorum read prefers client 2's greater timestamp, and **read repair or anti-entropy will eventually overwrite client 1's value.**

**It is not safe to assume that only one node is holding a lease at any one time. Fortunately, with a bit of care you can use fencing tokens to prevent zombies and delayed requests from doing any damage.**

## Examples & Systems
HBase's historical locking bug; Chubby sequencers, Kafka epoch numbers, Paxos ballot numbers, Raft terms; ZooKeeper `zxid`/`cversion`, etcd revisions, Hazelcast FencedLock; S3 conditional writes, Azure conditional headers, GCS request preconditions.

## Since the 1st Edition
The 1st edition covered fencing tokens inside [[Knowledge, Truth, and Lies]], including the paused-client corruption scenario and the ZooKeeper `zxid` suggestion. **The 2nd edition promotes it to a full subtopic and adds substantially**: the **delayed-request scenario** as a second, distinct failure mode that STONITH cannot fix; **conditional writes on object storage** (S3, Azure, GCS) as an alternative to explicit token checking, with the observation that **a single conditional-write store makes the lock service redundant**; the etcd and Hazelcast implementations; and the entire **fencing with multiple replicas** section showing how to embed a token in LWW timestamps.

## Related
- up: [[Knowledge, Truth, and Lies (2e)]] · chapter: [[Ch 09 - The Trouble with Distributed Systems (2e)]]
- [[Process Pauses (2e)]] — the lease-renewal bug this fixes
- [[Handling Node Outages (2e)]] — fencing named as the split-brain guard
- [[Preventing Lost Updates (2e)]] — compare-and-set as the retryable cousin
- 1st edition: [[Knowledge, Truth, and Lies]] — where fencing tokens lived
