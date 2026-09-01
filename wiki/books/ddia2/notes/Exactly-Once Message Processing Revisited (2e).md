---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 8
chapter_title: Transactions
topic: Distributed Transactions
type: subtopic
tags: [ddia2, exactly-once, idempotence, message-id, kafka-streams, deduplication]
sources:
  - raw/ch08.md
---
# Exactly-Once Message Processing Revisited
> You don't need distributed transactions for exactly-once. A table of processed message IDs, and transactions within one database, does the job.

## The Idea
An important use case for distributed transactions is **ensuring an operation takes effect exactly once even if a crash occurs during processing and it must be retried.** If you can atomically commit across a message broker and a database, **you can acknowledge the message if and only if it was successfully processed and the resulting database writes committed.**

**However, you don't actually need distributed transactions to achieve exactly-once semantics.**

## How It Works
An alternative requiring **only transactions within the database**:

1. **Assume every message has a unique ID**, and the database has a **table of message IDs that have been processed.** When you start processing a message, **begin a database transaction and check the message ID.** If it is already present, **you know the message has already been processed, so acknowledge it to the broker and drop it.**
2. **If the ID is not present, add it to the table.** Then process the message, which may produce **additional writes to the database within the same transaction.** When finished, **commit.**
3. **Once the database transaction is successfully committed, acknowledge the message to the broker.**
4. **Once the acknowledgment succeeds**, you know the broker won't retry, **so you can delete the message ID from the database** — in a separate transaction.

**Every crash point is covered:**
- **Crash before committing the database transaction** → the transaction aborts and the broker retries.
- **Crash after committing but before acknowledging** → the broker retries, **but the retry sees the message ID in the database and drops it.**
- **Crash after acknowledging but before deleting the ID** → you have an old message ID lying around, **which does no harm besides taking up a little storage space.**
- **A retry arriving before the database transaction is aborted** — possible if communication between processor and database is interrupted — **is stopped by a uniqueness constraint on the message ID table**, preventing two concurrent transactions from inserting the same ID.

## Trade-offs & Pitfalls
- **Thus achieving exactly-once processing requires only transactions within the database — atomicity across database and message broker is not necessary for this use case.** **Recording the message ID makes the message processing idempotent**, so processing can be safely retried without duplicating its side effects. **A similar approach is used in stream processing frameworks such as Kafka Streams.**
- **Internal distributed transactions are still useful here, for scalability.** They would allow **the message IDs to be stored on one shard and the main data on other shards**, ensuring atomicity of the commit across those shards. So the two techniques compose rather than compete.
- The pattern's requirement is a **unique ID per message** and a **uniqueness constraint** — both cheap, both easy to forget, and the whole guarantee rests on them.

## Examples & Systems
Kafka Streams as a framework using this approach for exactly-once semantics.

## Since the 1st Edition
**Entirely new as a subtopic.** The 1st edition described exactly-once processing via distributed transactions in its Chapter 9 XA discussion and separately discussed idempotence in the stream processing chapter, **but never brought the two together to show that the message-ID table replaces the need for heterogeneous distributed transactions.** Placing this at the end of the transactions chapter is a deliberate rhetorical move: after several pages establishing that XA is painful, the book shows you mostly don't need it.

## Related
- up: [[Distributed Transactions (2e)]] · chapter: [[Ch 08 - Transactions (2e)]]
- [[Distributed Transactions Across Different Systems (2e)]] — the approach this replaces
- [[Idempotence (2e)]] — the cross-cutting concept note
- [[Fault Tolerance (Stream Processing) (2e)]] — the same problem in Chapter 12
- [[Durable Execution and Workflows (2e)]] — exactly-once across service calls
