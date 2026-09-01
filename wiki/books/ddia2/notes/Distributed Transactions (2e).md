---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 8
chapter_title: Transactions
type: topic
tags: [ddia2, distributed-transactions, atomic-commitment, commit-point]
sources:
  - raw/ch08.md
---
# Distributed Transactions
In a single-node transaction, **one machine executes the transaction logic**, including the concurrency control algorithms. With single-leader replication, execution happens only on the leader and followers simply apply the committed log of writes.

**But what if multiple nodes are involved?** A transaction touching multiple shards, or a **global secondary index** whose entry may live on a different node from the primary data. **That is a distributed transaction.**

**Concurrency control in distributed transactions is broadly similar to the single-node case** — serial execution on sharded databases was already covered, **2PL works in a distributed setting, and for SSI there are distributed serializability checkers.** The book doesn't go further into those.

**Achieving atomicity in a distributed transaction is a whole new challenge**, and that is what the rest of the chapter is about.

## Subtopics
- [[Two-Phase Commit (2e)]] — the classic algorithm, its system of promises, and coordinator failure.
- [[Distributed Transactions Across Different Systems (2e)]] — XA, in-doubt transactions, and why they earned a bad reputation.
- [[Database-Internal Distributed Transactions (2e)]] — the same idea, done properly, inside one system.
- [[Exactly-Once Message Processing Revisited (2e)]] — the pattern that lets you avoid all of this.

## Key Takeaways
- **On a single node, atomicity comes down to disk write ordering.** When the client asks to commit, the database **makes the writes durable (typically in a WAL) and then appends a commit record to the log.** If it crashes mid-process, the transaction is recovered from the log on restart: **if the commit record reached disk before the crash the transaction is committed; if not, its writes are rolled back.**
- **So commitment depends crucially on the order in which data is durably written: first the data, then the commit record.** The **deciding moment is when the disk finishes writing the commit record** — before it, a crash still aborts; after it, the transaction is committed even if the database crashes. **A single device — the controller of one disk drive on one node — makes the commit atomic.**
- **In a distributed transaction that single deciding device doesn't exist.** Sending a commit request to all nodes and letting each commit independently is **not sufficient**: some nodes may **detect a constraint violation or conflict** and abort while others commit; **some commit requests may be lost in the network**, timing out into aborts while others get through; and **some nodes may crash before the commit record is fully written**, rolling back on recovery while others commit.
- **The consequence is not recoverable.** If some nodes commit and others abort, **the nodes become inconsistent — and a committed transaction cannot be retracted**, because committed data becomes visible to other transactions under read committed or stronger. By the time user 1 notices its commit failed on database 1, **user 2 may already have read that data from database 2**; aborting user 1's transaction would require reverting user 2's as well, **since it was based on data retroactively declared not to have existed.**
- **The requirement is therefore all-or-nothing across nodes, and achieving it is the atomic commitment problem.**

## Since the 1st Edition
**This entire topic is new to the transactions chapter.** In the 1st edition, distributed transactions, 2PC, XA, and the atomic commitment problem lived in **Chapter 9, "Consistency and Consensus"**, alongside linearizability and consensus. **The 2nd edition moves them into Chapter 8**, which is a better fit — atomic commit is a transaction property, not a consistency model — and leaves the consensus chapter free to focus on ordering and agreement. The content of the individual subtopics is largely carried over from that relocated material, plus one entirely new subtopic ([[Database-Internal Distributed Transactions (2e)]]).

## Related
- chapter: [[Ch 08 - Transactions (2e)]]
- [[Sharding and Secondary Indexes (2e)]] — the global index case that forces this
- [[Consensus (2e)]] — the fault-tolerant replacement for a single coordinator
- [[The Meaning of ACID (2e)]] — the atomicity being extended across nodes
