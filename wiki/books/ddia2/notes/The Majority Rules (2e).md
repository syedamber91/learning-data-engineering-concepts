---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 9
chapter_title: The Trouble with Distributed Systems
topic: Knowledge, Truth, and Lies
type: subtopic
tags: [ddia2, quorum, majority, asymmetric-fault, consensus]
sources:
  - raw/ch09.md
---
# The Majority Rules
> A node that is working perfectly can be declared dead by everyone else — and it has to accept that verdict. Its own judgment doesn't count.

## The Idea
Three scenarios, each memorable:

**The asymmetric fault.** A node **can receive all messages sent to it, but its outgoing messages are dropped or delayed.** It is working perfectly and receiving requests, **but the other nodes cannot hear its responses.** After a timeout they declare it dead. **The situation unfolds like a nightmare — the semi-disconnected node is dragged to the graveyard, kicking and screaming "I'm not dead!" — but since nobody can hear its screaming, the funeral procession continues with stoic determination.**

**The slightly less nightmarish version.** The node **notices its messages aren't being acknowledged and realizes there must be a network fault.** **Nevertheless it is wrongly declared dead, and it's unable to do anything about it.**

**The pause.** A node **pauses for one minute**; no requests processed, no responses sent. The others wait, retry, grow impatient, and declare it dead. **Then the pause ends and its threads continue as if nothing happened** — **the supposedly dead node suddenly raises its head out of the coffin, in full health, and starts cheerfully chatting with bystanders.** **At first it doesn't even realize a minute has passed and that it was declared dead — from its perspective hardly any time has passed.**

## How It Works
**The moral is that a node cannot necessarily trust its own judgment of a situation.** **A distributed system cannot exclusively rely on a single node, because a node may fail at any time, potentially leaving the system stuck and unable to recover.**

**Instead, many distributed algorithms rely on a quorum** — voting among the nodes — where **decisions require a minimum number of votes from several nodes in order to reduce dependence on any one node.**

**That includes decisions about declaring nodes dead. If a quorum of nodes declares another node dead, then it must be considered dead, even if that node still very much feels alive. The individual node must abide by the quorum decision and step down.**

**Most commonly the quorum is an absolute majority of more than half the nodes**, although other kinds are possible. A majority quorum **allows the system to continue working if a minority of nodes are faulty** — with three nodes one faulty node is tolerable, with five nodes two. **It is also safe, because there can be only one majority in the system — there cannot be two majorities with conflicting decisions at the same time.**

## Trade-offs & Pitfalls
- The safety argument — **only one majority can exist at a time** — is the whole reason majorities are used rather than any other threshold. It is what makes split brain impossible *by construction* rather than by detection.
- The uncomfortable corollary is that **correctness requires a healthy node to defer to a wrong verdict.** A node that decides it knows better than the quorum is exactly the failure mode fencing tokens exist to contain.

## Examples & Systems
Three-node clusters tolerating one fault; five-node clusters tolerating two.

## Since the 1st Edition
This is the 1st edition's "The Truth Is Defined by the Majority" section, **renamed to The Majority Rules** and promoted to a named subtopic. The three scenarios, the quorum argument, and the single-majority safety property are unchanged.

## Related
- up: [[Knowledge, Truth, and Lies (2e)]] · chapter: [[Ch 09 - The Trouble with Distributed Systems (2e)]]
- [[Distributed Locks and Leases (2e)]] — containing the node that doesn't accept the verdict
- [[Writing to the Database When a Node Is Down (2e)]] — quorums for reads and writes
- [[Consensus (2e)]] — where quorums are used to agree, not just to detect
- 1st edition: [[Knowledge, Truth, and Lies]] — where this material lived
