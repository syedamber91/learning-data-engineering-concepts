---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 8
chapter_title: Transactions
topic: Distributed Transactions
type: subtopic
tags: [ddia2, 2pc, coordinator, in-doubt, commit-point, three-phase-commit]
sources:
  - raw/ch08.md
---
# Two-Phase Commit
> Two points of no return: a participant that votes yes can never abort, and a coordinator that decides can never change its mind. Those two promises are what make it atomic — and what makes coordinator failure so painful.

## The Idea
**2PC is an algorithm for achieving atomic transaction commit across multiple nodes**, a classic in distributed databases. It is used internally in some databases and exposed to applications as **XA transactions** (supported by the Java Transaction API) or **WS-AtomicTransaction** for SOAP web services.

2PC introduces a component absent from single-node transactions: a **coordinator** (or **transaction manager**), **often implemented as a library within the same application process** requesting the transaction, though it can be a separate process or service. Examples: **Narayana, JOTM, BTM, MSDTC.**

The database nodes are **participants**. When the application is ready to commit, the coordinator begins **phase 1** by sending a **prepare** request to each participant asking whether they can commit. **If all reply yes, the coordinator sends a commit request in phase 2. If any replies no, it sends an abort request to all nodes.**

The book's analogy: **a traditional Western marriage ceremony.** The officiant asks each partner individually whether they want to marry the other, and typically receives "I do" from both; after both acknowledgments **the officiant pronounces them married — the transaction is committed — and broadcasts the happy fact to all attendees. If either does not say yes, the ceremony is aborted.**

## How It Works
**Why does this ensure atomicity when one-phase commit across several nodes doesn't?** Prepare and commit requests can be lost just as easily. **The answer is in the detail:**

1. **The application requests a globally unique transaction ID** from the coordinator.
2. **It begins a single-node transaction on each participant**, attaching that global ID. All reads and writes happen inside these single-node transactions. **If anything goes wrong at this stage, the coordinator or any participant can abort.**
3. **When ready to commit, the coordinator sends a prepare request to all participants**, tagged with the global ID. **If any request fails or times out, the coordinator sends an abort to all participants.**
4. **On receiving prepare, a participant makes sure it can definitely commit under all circumstances.** This includes **writing all transaction data to disk** — "a crash, a power failure, or running out of disk space is not an acceptable excuse for refusing to commit later" — **and checking for conflicts or constraint violations.** By replying yes, **the node promises to commit without error if requested: it surrenders the right to abort, without actually committing.**
5. **When the coordinator has all the responses, it makes a definitive decision** — commit only if all voted yes. **It must write that decision to its transaction log on disk** so it knows which way it decided if it later crashes. **This is the commit point.**
6. **Once the decision is on disk, the commit or abort request goes to all participants. If this fails or times out, the coordinator must retry forever until it succeeds. There is no more going back** — a commit decision must be enforced no matter how many retries it takes. **If a participant crashed meanwhile, the transaction is committed when it recovers; having voted yes, it cannot refuse.**

**So the protocol contains two crucial points of no return: when a participant votes yes it promises it will definitely be able to commit later (though the coordinator may still choose abort), and once the coordinator decides, that decision is irrevocable.** Those promises ensure atomicity. **Single-node atomic commit lumps these two events into one: writing the commit record to the transaction log.**

Back to the marriage: **before saying "I do" you have the freedom to abort. After saying it, you cannot retract. If you faint before hearing the officiant pronounce you married, that doesn't change the fact that the transaction was committed — on regaining consciousness you can query the officiant for the status of your global transaction ID, or wait for the next retry of the commit request, since retries continued throughout your unconsciousness.**

## Trade-offs & Pitfalls
**Coordinator failure is the real problem.** If a participant or the network fails, the behaviour is clear: a failed or timed-out prepare means abort; a failed commit or abort means retry indefinitely. **But if the coordinator crashes:**

**Before sending prepare requests, a participant can safely abort. But once a participant has received prepare and voted yes, it can no longer abort unilaterally — it must wait to hear the outcome.** If the coordinator crashes or the network fails at that point, **the participant can do nothing but wait. Its transaction is in doubt, or uncertain.**

In the book's example the coordinator decided to commit and database 2 received the commit, **but the coordinator crashed before telling database 1**, which now doesn't know whether to commit or abort. **A timeout does not help**: unilaterally aborting leaves it inconsistent with database 2, which committed; unilaterally committing is unsafe because another participant may have aborted. **Without hearing from the coordinator, a participant has no way of knowing.** In principle participants could ask each other how they voted and come to an agreement, **but that is not part of the 2PC protocol.**

**The only way 2PC can complete is by waiting for the coordinator to recover.** This is why the coordinator must write its decision to disk before sending requests: **on recovery it determines the status of all in-doubt transactions by reading its log, and any transaction without a commit record is aborted. Thus the commit point of 2PC comes down to a regular single-node atomic commit on the coordinator.**

**And if the coordinator's disk fails and its log is lost, the system has no way to automatically recover** — an administrator must manually commit or abort the in-doubt transactions. **If only the most recent part of the log is lost, the recovering coordinator may believe already-committed transactions are uncommitted and try to abort them, violating atomicity.**

**Three-phase commit.** 2PC is a **blocking** atomic commit protocol because it can get stuck waiting for the coordinator. It is possible to make an atomic commit protocol **nonblocking**, but **making this work in practice is not straightforward.** **3PC has been proposed as an alternative, but it assumes a network with bounded delay and nodes with bounded response times; in most practical systems with unbounded network delay and process pauses, 3PC cannot guarantee atomicity.** **A better solution in practice is to replace the single-node coordinator with a fault-tolerant consensus protocol.**

## Examples & Systems
Narayana, JOTM, BTM, MSDTC as coordinators; XA and WS-AtomicTransaction as the application-facing standards; the marriage ceremony as the canonical analogy.

## Since the 1st Edition
Carried over from the 1st edition's [[Atomic Commit and Two-Phase Commit (2PC)]] in Chapter 9 — the same six-step protocol, the same marriage analogy, the same in-doubt discussion, and the same verdict on 3PC. **The change is location, not content**: the 2nd edition moves it out of the consistency-and-consensus chapter into transactions, where atomic commit belongs.

## Related
- up: [[Distributed Transactions (2e)]] · chapter: [[Ch 08 - Transactions (2e)]]
- [[Distributed Transactions Across Different Systems (2e)]] — what happens when 2PC spans vendors
- [[Two-Phase Locking (2e)]] — the unrelated protocol with the confusingly similar name
- [[Consensus (2e)]] — the fault-tolerant replacement for the coordinator
- 1st edition: [[Atomic Commit and Two-Phase Commit (2PC)]] — the same subtopic, one chapter later
