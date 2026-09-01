---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 10
chapter_title: Consistency and Consensus
topic: ID Generators and Logical Clocks
type: subtopic
tags: [ddia2, lamport-clock, hybrid-logical-clock, vector-clock, causality, cockroachdb]
sources:
  - raw/ch10.md
---
# Logical Clocks
> A logical clock doesn't tell you what time it is. It counts events — and that's enough to give you a total order consistent with causality, without any special hardware.

## The Idea
Time-of-day and monotonic clocks are **physical clocks**: hardware devices measuring the passing of time. **In distributed systems it is common to also use a logical clock — an algorithm that counts the events that have occurred.** **A logical timestamp doesn't tell you what time it is, but you can compare two of them to tell which is earlier and which is later.**

**The general requirements for a logical clock:**
- **Timestamps are compact (a few bytes) and unique.**
- **You can compare any two and determine which is earlier** — they are **totally ordered**.
- **The order is consistent with causality**: if operation A happened before operation B, **A's timestamp is less than B's.**

**A single-node ID generator meets these requirements. The distributed ID generators discussed earlier do not meet the causal ordering requirement.**

## How It Works
**Lamport timestamps.** A simple method **consistent with causality**, usable as a distributed ID generator — **the Lamport clock, proposed in 1978 by Leslie Lamport, in what is now one of the most-cited papers in distributed systems.**

**Important caveat up front: although Lamport clocks provide a total ordering, they do not provide linearizability** — **they are not a way of ensuring a value is up to date.** They are **merely a way of assigning IDs to events such that if A happened before B, A's ID is less than B's.**

The mechanism: **each node has a unique identifier** (in the chat example, a name; in practice a random UUID) **and keeps a count of the operations it has processed.** **A Lamport timestamp is simply a pair of (counter, node ID)** — **two nodes may sometimes have the same counter value, but including the node ID makes each timestamp unique.**

- **Every time a node generates a timestamp, it increments its counter and uses the new value.**
- **Every time a node sees a timestamp from another node, if that timestamp's counter is greater than its local counter, it increases its local counter to match.**

In the chat example, **Aaliyah hadn't seen Caleb's message when she posted, and vice versa**, so both increment from 0 and attach counter 1. **When Bryce receives them he raises his local counter to 1**, and when he replies to Aaliyah **he increments and attaches 2.**

**To compare, first compare counter values** — (2, "Bryce") is greater than (1, "Aaliyah") and (1, "Caleb"). **If counters are equal, compare node IDs lexicographically.** So the order is **(1, "Aaliyah") < (1, "Caleb") < (2, "Bryce").**

**Hybrid logical clocks.** Lamport timestamps capture ordering well but have two limitations:
- **They have no direct relation to physical time**, so **you can't use them to find all messages posted on a particular date** — you'd need to store physical time separately.
- **If two nodes never communicate, one node's counter increments are never reflected in the other's**, so **events generated around the same time on different nodes could have wildly different counter values.**

**A hybrid logical clock combines the advantages of physical time-of-day clocks with the ordering guarantees of Lamport clocks.** **Like a physical clock it counts seconds or microseconds. Like a Lamport clock, when one node sees a greater timestamp from another it moves its own local value forward to match** — so **if one node's clock runs fast, the others move theirs forward when they communicate.**

**Every time a hybrid timestamp is generated it is also incremented**, ensuring **the clock moves forward monotonically even if the underlying physical clock jumps backward** (from an NTP adjustment). **So the hybrid clock might be slightly ahead of the physical clock, and details of the algorithm keep that discrepancy as small as possible.**

**The result: you can treat a hybrid logical timestamp almost like a conventional time-of-day timestamp, with the added property that its ordering is consistent with the happens-before relation.** **It doesn't depend on any special hardware and requires only roughly synchronized clocks.** **CockroachDB uses hybrid logical clocks.**

## Trade-offs & Pitfalls
**Lamport/hybrid logical clocks versus vector clocks.** Snapshot isolation via MVCC gives each transaction an ID and makes writes by higher-ID transactions invisible. **Lamport and hybrid logical clocks are a good way of generating these transaction IDs, because they ensure the snapshot is consistent with causality.**

**But when multiple timestamps are generated concurrently, these algorithms order them arbitrarily** — **so looking at two timestamps, you generally can't tell whether they were concurrent or one happened before the other.** (In the chat example you *can* tell Aaliyah's and Caleb's were concurrent because the counters are equal — **but when counter values differ, you can't tell.**)

**If you want to determine when records were created concurrently, you need a different algorithm, such as a vector clock.** **Vector clocks keep a counter for each node and store all the counter values with each write.** **If write A has a higher counter than B for one node and B has a higher counter than A for another, then A and B must be concurrent.** **The downside is that vector clock timestamps take up much more space — potentially one integer for every node in the system.**

## Examples & Systems
Lamport clocks (1978); hybrid logical clocks in CockroachDB; vector clocks for concurrency detection.

## Since the 1st Edition
The Lamport timestamp material comes from the 1st edition's [[Ordering Guarantees]] topic, essentially unchanged including the "Lamport timestamps are not linearizable" caveat and the vector-clock comparison. **New: hybrid logical clocks** — a full explanation of the algorithm, its two motivating limitations of Lamport clocks, and its use in CockroachDB. The 1st edition did not cover them, and their addition is what makes the causally-consistent-timestamps idea practical rather than theoretical.

## Related
- up: [[ID Generators and Logical Clocks (2e)]] · chapter: [[Ch 10 - Consistency and Consensus (2e)]]
- [[Detecting Concurrent Writes (2e)]] — version vectors and the happens-before relation
- [[Linearizable ID Generators (2e)]] — where logical clocks fall short
- [[Snapshot Isolation and Repeatable Read (2e)]] — the transaction IDs these generate
- 1st edition: [[Ordering Guarantees]] — where Lamport timestamps lived
