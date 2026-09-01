---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 8
chapter_title: Transactions
topic: Distributed Transactions
type: subtopic
tags: [ddia2, xa, heterogeneous, in-doubt, heuristic-decisions, exactly-once]
sources:
  - raw/ch08.md
---
# Distributed Transactions Across Different Systems
> XA works by being the lowest common denominator across every vendor — which is exactly why it can't detect cross-system deadlocks, can't work with SSI, and leaves locks held forever when the coordinator's log is lost.

## The Idea
**Distributed transactions and 2PC have a mixed reputation.** On one hand they provide an important safety guarantee that would be hard to achieve otherwise; on the other **they are criticized for causing operational problems, killing performance, and promising more than they can deliver.** **Many cloud services choose not to implement distributed transactions because of the operational problems they engender.** Much of the performance cost is **the additional `fsync` operations required for crash recovery and the additional network round trips.**

**But two quite different things are often conflated:**
- **Database-internal distributed transactions** — internal transactions among nodes of one distributed database, where **all participating nodes run the same database software.** YugabyteDB, TiDB, FoundationDB, Spanner, VoltDB, Cassandra, and MySQL Cluster's NDB engine have these.
- **Heterogeneous distributed transactions** — participants are **two or more different technologies**: databases from different vendors, or even non-database systems such as message brokers. **Atomic commit must hold even though the systems may be entirely different under the hood.**

**Database-internal transactions don't have to be compatible with anything else**, so they can use any protocol and apply technology-specific optimisations — **and can often work quite well.** **Transactions spanning heterogeneous technologies are a lot more challenging**, and are this subtopic's subject.

## How It Works
**Exactly-once message processing.** Heterogeneous transactions allow diverse systems to be integrated powerfully. **A message from a queue can be acknowledged as processed if and only if the database transaction for processing it committed** — implemented by **atomically committing the message acknowledgment and the database writes in one transaction**, even though the broker and the database are unrelated technologies on different machines.

**If either the message delivery or the database transaction fails, both are aborted**, so the broker may safely redeliver later. **Thus the message is effectively processed exactly once, even if it requires a few retries** — the abort discards any side effects of the partially completed transaction. **This is exactly-once semantics.**

**But it works only if all affected systems can use the same atomic commit protocol.** If a side effect is sending an email and **the email server does not support 2PC, the email could be sent two or more times** if processing fails and retries. **Only if all side effects are rolled back on abort can the processing step be safely retried as if nothing had happened.**

**XA transactions.** **X/Open XA (eXtended Architecture) is a standard for implementing 2PC across heterogeneous technologies**, introduced in **1991** and widely implemented — supported by **PostgreSQL, MySQL, Db2, SQL Server, Oracle** and by message brokers **ActiveMQ, HornetQ, MSMQ, IBM MQ**.

**XA is not a network protocol — it is merely a C API for interfacing with a transaction coordinator**, with bindings in other languages (in Java EE, via the **Java Transaction API (JTA)**, supported by many **JDBC** database drivers and **JMS** broker drivers).

**XA assumes your application uses a network driver or client library to talk to the participants.** If the driver supports XA, **it calls the XA API to find out whether an operation is part of a distributed transaction** and sends the necessary information to the server; **it also exposes callbacks through which the coordinator can ask the participant to prepare, commit, or abort.**

**The coordinator implements the XA API.** The standard doesn't specify how, but **in practice the coordinator is often simply a library loaded into the same process as the application** issuing the transaction, not a separate service. It tracks participants, collects prepare responses via driver callbacks, and **uses a log on the local disk for the commit/abort decision.**

**If the application process crashes, or its machine dies, the coordinator goes with it.** Participants with prepared-but-uncommitted transactions are **stuck in doubt.** Since the coordinator's log is on the application server's local disk, **that server must be restarted and the coordinator library must read the log to recover each transaction's outcome** before it can use the driver callbacks to resolve them. **The database server cannot contact the coordinator directly, since all communication must go via its client library.**

## Trade-offs & Pitfalls
**Holding locks while in doubt.** Why does being stuck in doubt matter so much — can't the rest of the system get on with its work? **The problem is locking.** Transactions usually acquire **row-level exclusive locks** on rows they modify, and for serializable isolation a 2PL database also acquires **shared locks on rows read**. **The database cannot release those locks until the transaction commits or aborts — so under 2PC a transaction holds its locks throughout the time it is in doubt.** If the coordinator crashed and takes 20 minutes to restart, **the locks are held for 20 minutes. If the coordinator's log is lost, they are held forever** — or until an administrator intervenes. **While the locks are held no other transaction can modify those rows**, and depending on isolation level may not even read them, **which can make large parts of your application unavailable.**

**Recovering from coordinator failure.** In theory a restarted coordinator cleanly recovers from its log. **In practice, orphaned in-doubt transactions do occur** — the log lost or corrupted by a software bug — **and these cannot be resolved automatically, so they sit forever in the database holding locks and blocking other transactions.** **Even rebooting your database servers won't fix it**, since a correct 2PC implementation **must preserve in-doubt locks across restarts** or risk violating atomicity.

**The only way out is manual.** An administrator **must examine the participants of each in-doubt transaction, determine whether any has already committed or aborted, and apply the same outcome to the others** — **potentially a lot of manual effort, most likely under high stress and time pressure during a serious production outage** (otherwise, why would the coordinator be in such a bad state?).

**Many XA implementations have an emergency escape hatch: heuristic decisions**, letting a participant unilaterally decide to abort or commit an in-doubt transaction without the coordinator. **To be clear, *heuristic* here is a euphemism for probably breaking atomicity**, since it violates 2PC's system of promises. **They are intended only for catastrophic situations, not regular use.**

**Problems with XA.** **A single-node coordinator is a single point of failure for the entire system**, and making it part of the application server is problematic because **its logs on local disk become a crucial part of the durable system state — as important as the databases themselves.**

**In principle the coordinator could be highly available and replicated. But that still doesn't solve XA's fundamental problem: it provides no way for the coordinator and participants to communicate directly.** They can communicate only via the application code that invoked the transaction and the drivers it calls. **So even a replicated coordinator leaves the application code as a single point of failure.** Solving this would require **totally redesigning how application code is run to make it replicated or restartable — which could perhaps look similar to durable execution — but no tools seem to take this approach in practice.**

**And because XA must be compatible with a wide range of data systems, it is necessarily a lowest common denominator.** **It cannot detect deadlocks across different systems**, which would require a standardized protocol for exchanging lock-wait information, **and it does not work with SSI**, which would require a protocol for identifying conflicts across systems.

**These problems are somewhat inherent in transactions across heterogeneous technologies. But keeping several heterogeneous data systems consistent is still a real and important problem, so a different solution is needed.**

## Examples & Systems
PostgreSQL, MySQL, Db2, SQL Server, Oracle; ActiveMQ, HornetQ, MSMQ, IBM MQ; JTA, JDBC, JMS.

## Since the 1st Edition
Carried over from the 1st edition's Chapter 9 material on distributed transactions and XA — the same in-doubt lock problem, the same heuristic-decisions euphemism, and the same lowest-common-denominator critique. **Added:** the explicit **database-internal versus heterogeneous** distinction as the organising frame (the 1st edition made it, but the 2nd builds a whole separate subtopic on the internal side), the note that **many cloud services simply don't implement distributed transactions**, and the observation that fixing XA's application-code single point of failure **would look like durable execution** — connecting it to Chapter 5's new material.

## Related
- up: [[Distributed Transactions (2e)]] · chapter: [[Ch 08 - Transactions (2e)]]
- [[Database-Internal Distributed Transactions (2e)]] — the version that escapes these problems
- [[Exactly-Once Message Processing Revisited (2e)]] — how to get the guarantee without XA
- [[Durable Execution and Workflows (2e)]] — the architecture XA would need
- 1st edition: [[Distributed Transactions in Practice]] — the closest predecessor
