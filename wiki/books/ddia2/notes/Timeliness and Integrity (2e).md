---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 13
chapter_title: A Philosophy of Streaming Systems
topic: Aiming for Correctness
type: subtopic
tags: [ddia2, timeliness, integrity, compensating-transaction, coordination-avoiding]
sources:
  - raw/ch13.md
---
# Timeliness and Integrity
> "Violations of timeliness are allowed under eventual consistency, whereas violations of integrity result in perpetual inconsistency." In most applications, integrity matters far more.

## The Idea
**In transactional systems, as soon as a transaction commits its writes are immediately visible — strict serializability.** **This is not the case when unbundling an operation across multiple stream processing stages, since log consumers are asynchronous by design.** **However, a client can wait for a message to appear on an output stream** — as the user waiting for an outgoing-payment or payment-declined event. **The correctness of the balance check does not depend on whether the user waits; the waiting only synchronously informs the user, and is decoupled from the effects of processing the request.**

**More generally, the term consistency conflates two requirements worth considering separately:**

**Timeliness** — **ensuring users observe the system in an up-to-date state.** **If a user reads from a stale copy they may observe it in an inconsistent state — but that inconsistency is temporary and will eventually be resolved simply by waiting and trying again.** **The CAP theorem uses "consistency" in the sense of linearizability, a strong way of achieving timeliness; weaker properties like read-after-write consistency can also be useful.**

**Integrity** — **absence of corruption: no data loss, and no contradictory or false data.** **If a derived dataset is maintained as a view onto underlying data, the derivation must be correct** — **a database index with missing records is not very useful.** **If integrity is violated, the inconsistency is permanent; waiting and trying again is not going to fix database corruption. Instead, explicit checking and repair is needed.** **In ACID, "consistency" is usually understood as some application-specific notion of integrity, and atomicity and durability are important tools for preserving it.**

**In slogan form: violations of timeliness are allowed under eventual consistency, whereas violations of integrity result in perpetual inconsistency.**

**In most applications, integrity is much more important than timeliness.** **Violations of timeliness can be annoying and confusing; violations of integrity can be catastrophic.** **On your credit card statement, it is not surprising if a transaction from the last 24 hours does not yet appear — banks reconcile and settle asynchronously and timeliness is not very important.** **But it would be very bad if the statement balance did not equal the sum of transactions plus the previous balance, or if a transaction was charged to you but not paid to the merchant. Those would be violations of integrity.**

## How It Works
**Correctness of dataflow systems.** **ACID transactions usually provide both timeliness (linearizability) and integrity (atomic commit), so if you approach correctness from an ACID point of view the distinction is fairly inconsequential.** **But event-based dataflow systems decouple them.** **When processing streams asynchronously there is no guarantee of timeliness unless you explicitly build consumers that wait** — a user could request a payment and then read their account before the processor has executed the request.

**However, integrity is central to streaming systems.** **Exactly-once or effectively-once semantics is a mechanism for preserving integrity: if an event is lost or takes effect twice, integrity could be violated.** **So fault-tolerant message delivery and duplicate suppression are important for maintaining integrity in the face of faults.**

**Reliable stream processing can preserve integrity without distributed transactions and atomic commit, meaning it can achieve comparable correctness with much better performance and operational robustness.** **Four mechanisms combine to achieve this:**
- **Representing the content of the write operation as a single message, easily written atomically** — an approach that fits very well with event sourcing.
- **Deriving all other state updates from that single message via deterministic derivation functions**, similarly to stored procedures.
- **Passing a client-generated request ID through all levels of processing**, enabling end-to-end duplicate suppression and idempotence.
- **Making messages immutable and allowing derived data to be reprocessed from time to time**, making it easier to recover from bugs.

**Loosely interpreted constraints.** **Enforcing a uniqueness constraint requires consensus, typically funneling all events in a shard through a single node.** **This is unavoidable for the traditional form of uniqueness constraint, and stream processing cannot get around it.** **However, many real applications have a business requirement to allow violations of what you might think of as hard constraints:**
- **If customers order more items than you have in the warehouse, you can order more stock, apologize for the delay, and offer a discount.** **This is the same as what you'd do if a forklift truck ran over some items, leaving you with fewer than you thought.** **The apology workflow already needs to be part of your business processes anyway, so a hard constraint on stock might be unnecessary.**
- **Many airlines overbook planes expecting some passengers to miss flights, and many hotels overbook rooms expecting cancellations.** **The constraint of "one person per seat" is deliberately violated for business reasons, and compensation processes — refunds, upgrades, a complimentary room at a neighboring hotel — handle demand exceeding supply.** **Even without overbooking, apology and compensation processes would be needed for cancelled flights due to weather or strikes; recovering from such issues is just a normal part of business.**
- **If someone withdraws more money than they have, the bank can charge an overdraft fee and ask them to pay it back.** **By limiting total withdrawals per day, the risk is bounded.**
- **In systems integrating data across organizations, inconsistencies will inevitably arise and correction mechanisms are necessary** — settlement of payments between banks being an example.

**In many business contexts it is therefore acceptable to temporarily violate a constraint and fix it up later by apologizing.** **This kind of corrective change is a compensating transaction.** **The cost of the apology varies but is often quite low: you can't unsend an email, but you can send a follow-up correction; if you accidentally charge a card twice you can refund one charge, at the cost of processing fees and perhaps a complaint.** **Once money has left an ATM you can't directly get it back, although in principle you can send debt collectors.**

**Whether the cost is acceptable is a business decision.** **If it is, the traditional model of checking all constraints before even writing the data is unnecessarily restrictive** — **it may well be reasonable to go ahead with a write optimistically and check the constraint after the fact.** **You can still ensure validation occurs before taking actions that would be expensive to recover from, but that doesn't imply you must validate before you even write.**

**These applications do require integrity** — **you would not want to lose a reservation or have money disappear from mismatched credits and debits.** **But they don't require timeliness on the enforcement of the constraint.**

## Trade-offs & Pitfalls
**Coordination-avoiding data systems.** Two observations combine:
- **Dataflow systems can maintain integrity guarantees on derived data without atomic commit, linearizability, or synchronous cross-shard coordination.**
- **Although strict uniqueness constraints require timeliness and coordination, many applications are fine with loose constraints that may be temporarily violated and fixed up later, as long as integrity is preserved throughout.**

**Together: dataflow systems can provide data management for many applications without requiring coordination, while still giving strong integrity guarantees.** **Such coordination-avoiding data systems have a lot of appeal; they can achieve better performance and fault tolerance than systems needing synchronous coordination.**

**Such a system could operate across multiple datacenters in a multi-leader configuration, replicating asynchronously between regions.** **Any one datacenter continues operating independently, because no synchronous cross-region coordination is required.** **It would have weak timeliness guarantees — it could not be linearizable without introducing coordination — but it can still have strong integrity guarantees.**

**Serializable transactions are still useful for maintaining derived state, but at a small scope where they work well.** **Heterogeneous distributed transactions such as XA are not required.** **Synchronous coordination can still be introduced where needed — to enforce strict constraints before an irreversible operation — but there is no need for everything to pay the cost if only a small part of an application needs it.**

**Another way of looking at coordination and constraints: they reduce the number of apologies you have to make for inconsistencies, but potentially also reduce performance and availability, and thus increase the number of apologies you have to make for outages.** **You cannot reduce the number of apologies to zero, but you can aim to find the best trade-off — the sweet spot with neither too many inconsistencies nor too many availability problems.**

## Examples & Systems
Credit card statement lag as acceptable timeliness violation; airline and hotel overbooking as deliberate constraint violation; compensating transactions.

## Since the 1st Edition
Essentially unchanged from the 1st edition's [[Timeliness and Integrity]] — the same distinction, the same slogan, the same four integrity mechanisms, the same loosely-interpreted-constraints examples, and the same coordination-avoiding conclusion with the apologies trade-off. One of the book's most durable arguments.

## Related
- up: [[Aiming for Correctness (2e)]] · chapter: [[Ch 13 - A Philosophy of Streaming Systems (2e)]]
- [[Enforcing Constraints (2e)]] — the coordination this argues you can often avoid
- [[The Cost of Linearizability (2e)]] — the price of timeliness
- [[Dealing with Conflicting Writes (2e)]] — the analogous after-the-fact repair
- 1st edition: [[Timeliness and Integrity]] — the same subtopic
