---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 10
chapter_title: Consistency and Consensus
topic: Consensus
type: subtopic
tags: [ddia2, raft, paxos, epoch, state-machine-replication, epaxos, unclean-leader-election]
sources:
  - raw/ch10.md
---
# Consensus in Practice
> Consensus is essentially "single-leader replication done right." Two rounds of quorum voting — one to elect a leader, one per log entry — and the epoch number is what makes it safe.

## The Idea
Five formulations are equivalent, **but which is most useful in practice?** **Most consensus systems provide shared logs** — the abstraction equivalent to total order broadcast. **Raft, Viewstamped Replication, and Zab provide shared logs out of the box. Paxos provides single-value consensus, but in practice most Paxos systems use the extension Multi-Paxos, which also provides a shared log.**

## How It Works
**Using shared logs.** **A shared log is a good fit for database replication**: if every log entry is a write and every replica processes the same writes in the same order using deterministic logic, **all replicas end up in a consistent state.** **This is state machine replication**, the principle behind event sourcing, and shared logs are also useful for stream processing.

**A shared log can also implement serializable transactions**: if every entry is a deterministic transaction executed as a stored procedure and every node executes them in the same order, **the transactions will be serializable.**

> **Sharded databases with strong consistency often maintain a separate log per shard**, which **improves scalability but limits the consistency guarantees** — consistent snapshots, foreign-key references — **they can offer across shards.** Serializable cross-shard transactions are possible but require additional coordination.

**A shared log easily adapts to the other forms of consensus:**
- **Single-value consensus and CAS** — decide the value that appears first in the log.
- **Many instances of single-value consensus** — say one per theatre seat — **include the seat number in log entries and decide the first entry containing that seat number.**
- **Atomic fetch-and-add** — put the number to add in a log entry, and **the current counter value is the sum of all entries so far.** **A simple counter on log entries generates fencing tokens** — in ZooKeeper this sequence number is `zxid`.

**From single-leader replication to consensus.** **Single-value consensus is easy with a "dictator" node, and a shared log is easy if a single leader is the only node allowed to append.** **The question is fault tolerance if that node fails.**

**Traditionally, databases with single-leader replication didn't solve this — they left failover to a human administrator**, which **means significant downtime, since there is a limit to how fast humans react, and it doesn't satisfy termination.** **For consensus we require the algorithm to automatically choose a new leader.** (**Not all consensus algorithms have a leader, but the commonly used ones do.**)

**This is not straightforward.** All nodes must agree who the leader is, or two could each believe they are leader and make inconsistent decisions. **So it seems we need consensus to elect a leader, and a leader to solve consensus. How do we break out of this conundrum?**

**Consensus algorithms don't require that there is only one leader at any one time.** **They make a weaker guarantee: they define an epoch number** — **ballot number in Paxos, view number in Viewstamped Replication, term number in Raft** — **and guarantee that within each epoch, the leader is unique.**

**When a node believes the leader is dead** because it hasn't heard from it for some timeout, **it may start a vote to elect a new leader, given a new epoch number greater than any previous one.** **If a conflict arises between two leaders in two epochs — perhaps the previous leader wasn't dead after all — the leader with the higher epoch prevails.**

**Before appending the next log entry, a leader must first check there isn't another leader with a higher epoch** that might append a different entry. **It does this by collecting votes from a quorum — typically but not always a majority — and a node votes yes only if it is not aware of any leader with a higher epoch.**

**So there are two rounds of voting: once to choose a leader, and a second time on the leader's proposal for the next log entry. The quorums for those two votes must overlap**: if a proposal vote succeeds, **at least one node that voted for it must also have participated in the most recent successful leader election.** **If the proposal vote passes without revealing any higher-numbered epoch, the leader can conclude no higher-epoch leader has been elected and can safely append.**

**These two rounds look superficially similar to 2PC but are very different protocols.** **In consensus algorithms any node can start an election and it requires only a quorum to respond; in 2PC only the coordinator can request votes, and it requires a yes from every participant.**

**Subtleties.** This basic structure is common to Raft, Multi-Paxos, Viewstamped Replication, and Zab, with **every new log entry synchronously replicated to a quorum before being confirmed to the client** — ensuring it isn't lost if the leader fails. **But the devil is in the details.** When a new leader is elected, **the algorithm must ensure it honors log entries already appended by the old leader.** **Raft does this by allowing a node to become leader only if its log is at least as up-to-date as those of a majority of its followers. Paxos allows any node to become leader but requires it to bring its log up to date before appending new entries.**

> **Consistency versus availability in leader election.** **It's essential that the new leader is up to date with any confirmed log entries before processing writes or linearizable reads** — **a stale leader might write new values to entries already written by the old leader, violating the append-only property.** **In some cases you might weaken the consensus properties to recover more quickly, or at all.** **Kafka offers unclean leader election, allowing any replica to become leader even if not up to date.** Also, **in databases with asynchronous replication you cannot guarantee any follower is up to date when the leader fails.** **Dropping the up-to-date requirement may improve performance and availability, but you are on thin ice, since the theory of consensus no longer applies** — things work fine without faults, **but the problems of Chapter 9 can easily cause data loss or corruption.**

**For databases using consensus for replication, replicating writes to a quorum isn't all that's required.** **To guarantee linearizable reads, they must also go through a quorum vote**, confirming the node that believes itself leader really is still up to date. **Linearizable reads in etcd work like this.**

**Most consensus algorithms in standard form assume a fixed set of nodes** — nodes may go down and come back, **but the voting set is fixed when the cluster is created.** **In practice you often need to add or remove nodes, so algorithms have been extended with reconfiguration features** — especially useful **when adding new regions or migrating from one location to another** by adding the new nodes then removing the old.

## Trade-offs & Pitfalls
**Pros.** **Consensus algorithms are a huge breakthrough for distributed systems.** **Consensus is essentially "single-leader replication done right," with automatic failover on leader failure, ensuring no committed data is lost and split brain is not possible** — even in the face of all the problems of Chapter 9. **Any system that provides automatic failover but does not use a proven consensus algorithm is likely to be unsafe.** **Using a proven algorithm is not a guarantee of whole-system correctness — plenty of other places harbour bugs — but it's a good start.**

**Cons.**
- **Consensus systems always require a strict majority** — three nodes to tolerate one failure, five to tolerate two.
- **Every operation requires communication with a quorum, so you can't increase throughput by adding more nodes** — **in fact every node you add makes the algorithm slower.**
- **If a network partition cuts off some nodes, only the majority portion can make progress**; the others are blocked.
- **They generally rely on timeouts to detect failed nodes.** In environments with highly variable delays, especially across regions, **tuning these is difficult: too large and recovery takes a long time; too small and lots of unnecessary elections occur, giving terrible performance as the system spends more time choosing leaders than doing useful work.**
- **Some algorithms are particularly sensitive to network problems.** **Raft has unpleasant edge cases**: if everything works except one consistently unreliable link, **leadership can continually bounce between two nodes, or the leader is continually forced to resign, so the system effectively never makes progress.** **The original Raft algorithm was extended with a pre-vote phase to address this.** **Paxos also depends on leaders and can have similar issues; Egalitarian Paxos (EPaxos) and derivatives use a leaderless protocol more robust against poorly performing nodes or connections.**

## Examples & Systems
Raft, Multi-Paxos, Viewstamped Replication, Zab; ZooKeeper's `zxid` as a fencing token; etcd's quorum-checked linearizable reads; Kafka's unclean leader election; Raft's pre-vote phase; EPaxos.

## Since the 1st Edition
The epoch-number mechanism, the two rounds of voting, the 2PC contrast, and the pros-and-cons list all come from the 1st edition's [[Fault-Tolerant Consensus]]. **Added:** the **shared-log-as-the-practical-formulation** framing with the per-shard-log caveat; **how Raft and Paxos differ in bringing a new leader up to date**; the **consistency-versus-availability box** with **Kafka's unclean leader election** as a worked example; **reconfiguration** for adding and removing nodes; and **Raft's pre-vote phase and EPaxos** as responses to the leader-thrashing edge cases the 1st edition described but had no fixes for.

## Related
- up: [[Consensus (2e)]] · chapter: [[Ch 10 - Consistency and Consensus (2e)]]
- [[The Many Faces of Consensus (2e)]] — why shared logs are the chosen formulation
- [[Coordination Services (2e)]] — the packaged product
- [[Handling Node Outages (2e)]] — manual failover, the thing consensus replaces
- 1st edition: [[Fault-Tolerant Consensus]] — the same material
