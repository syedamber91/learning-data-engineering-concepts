---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 13
chapter_title: A Philosophy of Streaming Systems
topic: Aiming for Correctness
type: subtopic
tags: [ddia2, uniqueness-constraint, consensus, log-sharding, multishard, atomicity]
sources:
  - raw/ch13.md
---
# Enforcing Constraints
> Route every possibly-conflicting write to the same log shard and process it sequentially. That is consensus, achieved by sharding rather than by coordination.

## The Idea
**End-to-end duplicate suppression works with a request ID passed from client to database. What about other kinds of constraints?**

**Focus on uniqueness constraints**: **a username or email address must uniquely identify a user, a file storage service cannot have two files with the same name, two people cannot book the same seat.** **Other constraints are very similar** — **ensuring an account balance never goes negative, not selling more items than you have in stock, no overlapping meeting room bookings** — **and techniques that enforce uniqueness can often be used for these too.**

## How It Works
**Uniqueness constraints require consensus.** **In a distributed setting, enforcing uniqueness requires consensus**: **if several concurrent requests have the same value, the system must decide which is accepted and reject the others.**

**The most common way is to make a single node the leader in charge of all decisions.** **That works fine as long as you don't mind funneling all requests through one node — even if the client is on the other side of the world — and as long as that node doesn't fail.** **Consensus algorithms like Raft tackle safely electing a new leader if the current one fails and preventing split brain.**

**Uniqueness checking can be scaled out by sharding based on the value that needs to be unique.** **To ensure uniqueness by request ID, route all requests with the same ID to the same shard; for usernames, shard by hash of username.**

**However, asynchronous multi-leader replication is ruled out**, because **different leaders could concurrently accept conflicting writes, so the values are no longer unique.** **If you want to immediately reject writes that would violate the constraint, synchronous coordination is unavoidable.**

**Uniqueness in log-based messaging.** **A shared log ensures all consumers see messages in the same order — the total order broadcast guarantee, equivalent to consensus.** **In the unbundled approach we can use a very similar approach.**

**A stream processor consumes all messages in a log shard sequentially on a single thread.** **So if the log is sharded based on the value that needs to be unique, the processor can unambiguously and deterministically decide which of several conflicting operations came first.** For several users claiming the same username:
1. **Every request is encoded as a message and appended to a shard determined by the hash of the username.**
2. **A stream processor sequentially reads the requests, using a local database to track which usernames are taken.** **For an available name it records the name as taken and emits a success message; for a taken name it emits a rejection message.**
3. **The client watches the output stream and waits for a success or rejection corresponding to its request.**

**This algorithm is the same as the construction for achieving consensus using a shared log.** **It scales easily to large request throughput by increasing the number of shards, since each shard is processed independently.**

**It works not only for uniqueness but for many other constraints.** **Its fundamental principle is that any writes that may conflict are routed to the same shard and processed sequentially.** **The definition of a conflict may depend on the application, but the stream processor can use arbitrary logic to validate a request.**

**Multishard request processing.** **Executing an operation atomically while satisfying constraints becomes more interesting with several shards.** In the money-transfer example there are potentially three: **one containing the request ID, one the payee account, one the payer account** — **and no reason those should be in the same shard, since they are independent.**

**Traditionally, executing this transaction would require an atomic commit across all three shards, essentially forcing it into a total order with respect to all other transactions on any of them.** **With cross-shard coordination, shards can no longer be processed independently, so throughput is likely to suffer.**

**But equivalent correctness can be achieved without cross-shard transactions, using sharded logs and stream processors.** The book's worked payment example, which checks whether the source account has sufficient funds and if so atomically transfers an amount while deducting fees:
1. **The transfer request is given a unique request ID by the user's client and appended to a log shard based on the source account ID.**
2. **A stream processor reads the log and maintains a database containing the state of the source account and the IDs of requests it has already processed** — **contents entirely derived from the log.** **On a request with an unseen ID, it checks whether the source account has enough money.** **If so, it updates its local database to reserve the amount and emits events to several other logs**: **an outgoing payment event to the source account's log shard (its own input log), an incoming payment event to the destination account's shard, and an incoming payment event to the fees account's shard.** **The original request ID is included in those events.**
3. **Eventually the outgoing payment event is delivered back to the source account processor**, which **recognizes from the request ID that this is a payment it previously reserved and executes it, again updating its local state.** **It ignores duplicates based on request ID.**
4. **The destination and fees account shards are consumed by independent tasks**, which **update their local state and deduplicate based on request ID.**

**The three accounts could just as well be in the same shard — it doesn't matter.** **The only requirements are that events for any given account are processed strictly in log order with at-least-once semantics, and that the stream processors are deterministic.**

**Consider a crash while processing a payment request.** **The output messages may or may not have been emitted.** **After recovery the processor processes the same request again (at-least-once) and makes the same decision (deterministic), so it emits the same output messages with the same request ID** — **and if they are duplicates, downstream consumers ignore them.**

## Trade-offs & Pitfalls
- **Atomicity in this system comes not from transactions but from the fact that writing the initial request event to the source account log is an atomic action.** **Once that one event is in the log, all downstream events will eventually be written — possibly after crash recovery, possibly with duplicates, but they will appear eventually.**
- **With exactly-once semantics this becomes easier to implement**, since the semantics ensure the processor's local state is consistent with the messages it has processed — **so if it crashes and reprocesses, its local state is also reset to what it was before.**
- **To find out whether their transfer was approved, the user subscribes to the source account log shard and waits for the outgoing payment event.** **To explicitly notify on insufficient balance, the processor can emit a "declined payment" event.**
- **By breaking the multishard transaction into several differently sharded stages and using the end-to-end request ID, we achieve the same correctness property — every request applied exactly once to both payer and payee — even in the presence of faults, without using an atomic commit protocol.**

## Examples & Systems
Username claiming via hash-sharded log; the three-shard payment transfer as the multishard example.

## Since the 1st Edition
Essentially unchanged from the 1st edition's [[Enforcing Constraints]] — the same uniqueness-requires-consensus argument, the same username-claiming algorithm, and the same four-step multishard payment example with the same crash analysis. Very stable, since it is a construction rather than a product survey.

## Related
- up: [[Aiming for Correctness (2e)]] · chapter: [[Ch 13 - A Philosophy of Streaming Systems (2e)]]
- [[The Many Faces of Consensus (2e)]] — the shared-log construction this reuses
- [[Relying on Linearizability (2e)]] — why uniqueness needs consensus
- [[Distributed Transactions (2e)]] — the approach this replaces
- 1st edition: [[Enforcing Constraints]] — the same subtopic
