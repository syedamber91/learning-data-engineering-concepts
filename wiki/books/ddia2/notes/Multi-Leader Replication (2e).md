---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 6
chapter_title: Replication
type: topic
tags: [ddia2, multi-leader, active-active, topologies, version-vectors]
sources:
  - raw/ch06.md
---
# Multi-Leader Replication
Single-leader replication has one major downside: **all writes must go through the one leader**. If you can't connect to it — a network interruption between you and it, for instance — **you can't write to the database at all**.

The natural extension is to **allow more than one node to accept writes**. Replication still works the same way: each node processing a write forwards that change to all the others. This is a **multi-leader** configuration (also **active/active** or **bidirectional** replication), in which **each leader simultaneously acts as a follower to the other leaders**.

As with single-leader there is a synchronous/asynchronous choice, but the book dispatches the synchronous case quickly: with leaders A and B, if writes are synchronously replicated from A to B and the network between them is interrupted, **you can't write to A until the connection is restored** — which makes synchronous multi-leader replication **very similar to single-leader replication** (as if B were the leader and A merely forwarded requests). So the chapter treats it as equivalent and **focuses entirely on asynchronous multi-leader replication**, in which any leader can process writes even when cut off from the others.

## Subtopics
- [[Geographically Distributed Operation (2e)]] — a leader per region, and the topologies that connect them.
- [[Sync Engines and Local-First Software (2e)]] — the same architecture taken to the extreme: every device is a leader.
- [[Dealing with Conflicting Writes (2e)]] — the price of admission, and the four ways to pay it.

## Key Takeaways
- **Multi-leader replication is less common than single-leader but widely supported**: MySQL, Oracle, SQL Server, and YugabyteDB, and as an external add-on in Redis Enterprise, EDB Postgres Distributed, and pglogical.
- **Because it is a retrofitted feature in many databases, there are often subtle configuration pitfalls and surprising interactions with other database features** — autoincrementing keys, triggers, and integrity constraints can all be problematic. For this reason **multi-leader replication is often considered dangerous territory that should be avoided if possible.**
- **Replication topologies** describe the paths writes take. With two leaders only one topology is plausible. With more, the general case is **all-to-all** (every leader sends to every other), but restricted forms are also used: **circular** (each node receives from one node and forwards to one other) and **star** (a designated root forwards to all others, generalizable to a tree). *(A star network topology is unrelated to a star schema.)* In circular and star topologies a write may pass through several nodes, so nodes must forward changes they receive — and **to prevent infinite replication loops each node has a unique identifier and each write is tagged with the identifiers of every node it has passed through**; a node receiving a change tagged with its own identifier ignores it.
- **Topology failure modes differ.** In circular and star topologies, **one node failing can interrupt the flow of replication messages between other nodes**, leaving them unable to communicate until it is fixed; reconfiguration around the failure would usually have to be done manually. **A densely connected topology such as all-to-all has better fault tolerance** because messages can travel along different paths.
- **But all-to-all has its own problem: message overtaking.** Some network links may be faster than others, so replication messages can arrive out of order. Client A inserts a row on leader 1 and client B updates that row on leader 3; **leader 2 may receive the update first — an update to a row that does not exist — and only later the insert.** This is a **causality** problem, the same shape as consistent prefix reads. **Simply attaching a timestamp to every write is not sufficient**, because clocks cannot be trusted to be sufficiently in sync. **Version vectors** can order these events correctly — but **many multi-leader systems don't use good ordering techniques**, leaving them vulnerable. The book's advice: be aware of these issues, read the documentation carefully, and **thoroughly test your database to ensure it really provides the guarantees you believe it has.**

## Since the 1st Edition
The 1st edition's [[Multi-Leader Replication]] covered the same model, the same three topologies, the loop-prevention tagging, and the overtaking problem. **New:** YugabyteDB, EDB Postgres Distributed, and pglogical in the system roster; the explicit dismissal of synchronous multi-leader as equivalent to single-leader; and — the big structural change — the 1st edition's use cases were "multi-datacenter operation," "clients with offline operation," and "collaborative editing," which the 2nd edition reorganises into [[Geographically Distributed Operation (2e)]] and the substantially expanded [[Sync Engines and Local-First Software (2e)]].

## Related
- chapter: [[Ch 06 - Replication (2e)]]
- [[Single-Leader Replication (2e)]] — what this relaxes
- [[Detecting Concurrent Writes (2e)]] — version vectors, promised here
- [[Problems with Replication Lag (2e)]] — the causality problem in its single-leader form
- 1st edition: [[Multi-Leader Replication]] — the same topic
