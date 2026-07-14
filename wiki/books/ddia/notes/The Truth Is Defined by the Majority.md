---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 8
chapter_title: The Trouble with Distributed Systems
topic: Knowledge, Truth, and Lies
type: subtopic
tags: [ddia, quorum, fencing-tokens, leases, split-brain]
sources:
  - raw/ch08.md
---
# The Truth Is Defined by the Majority
> No node can trust its own sense of being alive or in charge — declarations of death, leadership, and lock ownership belong to the quorum, and fencing tokens enforce the quorum's verdict on shared resources.

## The Idea
Three nightmare scenarios motivate this rule. A node with an asymmetric network fault receives everything but its outgoing messages vanish — peers declare it dead while it protests unheard. A node that *notices* its messages go unacknowledged still cannot overturn the verdict. And a node frozen by a minute-long stop-the-world GC pause is buried by its peers, then wakes and resumes chatting as if nothing happened, initially unaware any time passed. Moral: a node's self-assessment is worthless as system truth. Since relying on any single node risks the whole system when that node fails, distributed algorithms use a [[Quorum]]: decisions require a minimum number of votes, usually an absolute majority. If the quorum says a node is dead, it is dead — however alive it feels — and it must step down. Majorities tolerate failures (3 nodes survive 1 down, 5 survive 2) and stay safe because only one majority can exist at once: no two conflicting decisions.

## How It Works
Systems often need exactly-one semantics — one partition leader (else [[Split Brain]]), one lock holder per resource, one owner per username. The trap: a node that *was* the chosen one may have been deposed during a network hiccup or GC pause without knowing it. If it keeps acting on its stale belief, it can corrupt the system. Kleppmann's Figure 8-4 scenario (a real historical HBase bug): client 1 holds a lease on a file, pauses long enough for the lease to expire, client 2 acquires it and writes — then client 1 wakes and writes too, corrupting the file. The fix is *fencing*: every lease grant carries a [[Fencing Tokens|fencing token]] — a number the lock service increments on each grant. Every write to the storage service must include the current token. Client 1 wakes with token 33, but storage has already seen 34 from client 2, so the stale write is rejected. With [[ZooKeeper]] as lock service, the transaction ID `zxid` or node version `cversion` serve as tokens, being guaranteed monotonically increasing.

## Trade-offs & Pitfalls
Fencing only works if the *resource itself* checks tokens and rejects any write bearing an older token than one already processed — client-side lease checks are provably insufficient, since the whole failure mode is a client with a false belief. For resources without native token support, workarounds exist (e.g., embedding the token in a filename), but some server-side check is mandatory. Server-side validation is a virtue anyway: clients are run by people whose priorities differ from the service operator's, so services should protect themselves from accidentally abusive clients.

## Examples & Systems
The HBase lease-expiry corruption bug; ZooKeeper zxid/cversion as fencing tokens; the GC-pause "return from the dead" scenario; majority quorums (3/1, 5/2 fault tolerance).

## Related
- up: [[Knowledge, Truth, and Lies]] · chapter: [[Ch 08 - The Trouble with Distributed Systems]]
- [[Process Pauses]] — how a leader sleeps through its own deposition
- [[Leader Election]] — choosing the single chosen one
- [[Limitations of Quorum Consistency]] — quorum subtleties from Ch 5
- [[Membership and Coordination Services]] — ZooKeeper as the lock/lease service
- [[Byzantine Faults]] — sibling: what if the node lies deliberately
