---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 13
chapter_title: A Philosophy of Streaming Systems
topic: Aiming for Correctness
type: subtopic
tags: [ddia2, end-to-end-argument, idempotence, duplicate-suppression, request-id]
sources:
  - raw/ch13.md
---
# The End-to-End Argument for Databases
> TCP deduplicates packets. Transactions deduplicate at commit. Neither stops a user hitting "submit" twice on a flaky connection — and only an end-to-end request ID does.

## The Idea
**Just because an application uses a data system with strong safety properties such as serializable transactions, that does not mean the application is free from data loss or corruption.** **If an application has a bug causing it to write incorrect data or delete data, serializable transactions aren't going to save you.** **This is an argument in favor of immutable and append-only data, because it is easier to recover from such mistakes if you remove faulty code's ability to destroy good data.** **Although immutability is useful, it is not a cure-all.**

## How It Works
**Exactly-once execution of an operation.** **If something goes wrong while processing a message you can either give up (dropping it, incurring data loss) or try again — and if you try again, there is the risk that processing actually succeeded the first time and you just didn't get a confirmation, so the message is processed twice.**

**Processing twice is a form of data corruption: it is undesirable to charge a customer twice for the same service or to increment a counter twice.** **Exactly once means arranging the computation so the final effect is the same as if no faults had occurred, even if the operation was retried.** **One of the most effective approaches is to make the operation idempotent** — **but doing this for an operation that is not naturally idempotent requires effort and care**: **you may need additional metadata such as the set of operation IDs that have updated a value, and fencing when failing over between nodes.**

**Duplicate suppression.** **The same pattern occurs in many places.** **TCP uses sequence numbers on packets to order them and determine whether any were lost or duplicated; lost packets are retransmitted and duplicates removed by the TCP stack before handing data to the application.**

**But this deduplication works only within a single TCP connection.** **Imagine the connection is a client's connection to a database executing a money transfer transaction.** **In many databases a transaction is tied to a client connection.** **If the client suffers a network interruption and connection timeout after sending `COMMIT` but before hearing back, it does not know whether the transaction committed or aborted.**

```sql
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance + 11.00 WHERE account_id = 1234;
UPDATE accounts SET balance = balance - 11.00 WHERE account_id = 4321;
COMMIT;
```

**The client can reconnect and retry — but now it is outside the scope of TCP duplicate suppression.** **Since this transaction is not idempotent, $22 could be transferred instead of the desired $11.** **So even though code like this is a standard example for transaction atomicity, it is not correct, and real banks do not work like this.**

**2PC breaks the one-to-one mapping between a TCP connection and a transaction**, since a coordinator must be able to reconnect after a fault and resolve an in-doubt transaction. **Is that sufficient to ensure execution only once? Unfortunately not.**

**Even suppressing duplicates between database client and server, we still must worry about the network between the end-user device and the application server.** **If the client is a web browser it probably uses an HTTP POST.** **On a weak cellular connection the user may succeed in sending the POST but lose signal before receiving the response.** **The user is shown an error and may retry manually** — **browsers warn "Are you sure you want to submit this form again?" and the user says yes, because they want the operation to happen.** (**The Post/Redirect/Get pattern avoids this warning in normal operation, but doesn't help if the POST times out.**) **From the web server's point of view the retry is a separate request; from the database's, a separate transaction. The usual deduplication mechanisms don't help.**

**Uniquely identifying requests.** **To make a request idempotent through several hops of network communication, it is not sufficient to rely on a database transaction mechanism. You need to consider the end-to-end flow.**

**Generate a unique identifier for each request — a UUID — and include it as a hidden form field in the client application, or calculate a hash of all relevant form fields to derive the request ID.** **If the browser submits twice, both requests have the same ID.** **Pass that ID all the way through to the database and check that you only ever execute one request with a given ID:**

```sql
ALTER TABLE requests ADD UNIQUE (request_id);
BEGIN TRANSACTION;
INSERT INTO requests
  (request_id, from_account, to_account, amount)
  VALUES('0286FDB8-D7E1-423F-B40B-792B3608036C', 4321, 1234, 11.00);
UPDATE accounts SET balance = balance + 11.00 WHERE account_id = 1234;
UPDATE accounts SET balance = balance - 11.00 WHERE account_id = 4321;
COMMIT;
```

**This relies on a uniqueness constraint on `request_id`.** **If a transaction attempts to insert an existing ID, the `INSERT` fails and the transaction aborts, preventing it taking effect twice.** **Relational databases can generally maintain a uniqueness constraint correctly even at weak isolation levels — whereas an application-level check-then-insert may fail under nonserializable isolation.**

**Besides suppressing duplicates, the `requests` table acts as a kind of event log**, useful for event sourcing or CDC. **The account balance updates don't have to happen in the same transaction as the event insertion, since they are redundant and could be derived downstream — as long as the event is processed exactly once, again enforced using the request ID.**

## Trade-offs & Pitfalls
**The end-to-end argument**, articulated by Saltzer, Reed, and Clark in 1984: **"The function in question can completely and correctly be implemented only with the knowledge and help of the application standing at the endpoints of the communication system. Therefore, providing that questioned function as a feature of the communication system itself is not possible. (Sometimes an incomplete version of the function provided by the communication system may be useful as a performance enhancement.)"**

**Here the function was duplicate suppression.** **TCP suppresses duplicates at the connection level and some stream processors provide exactly-once semantics at the message level, but that is not enough to prevent a user submitting a duplicate request if the first times out.** **By themselves, TCP, database transactions, and stream processors cannot rule out these duplicates — the solution requires a transaction identifier passed all the way from the end-user client to the database.**

**The argument also applies to integrity checking.** **Checksums in Ethernet, TCP, and TLS detect corruption of packets in the network, but not corruption from software bugs at the sending or receiving ends, or on the disks where data is stored.** **To catch all possible sources you also need end-to-end checksums.**

**And to encryption.** **Your home WiFi password protects against people snooping your WiFi traffic but not attackers elsewhere on the internet; TLS between client and server protects against network attackers but not compromises of the server.** **Only end-to-end encryption and authentication protect against all these.**

**The low-level features are still useful, since they reduce the probability of problems at higher levels** — **HTTP requests would often get mangled without TCP putting packets in order.** **We just need to remember they are not by themselves sufficient for end-to-end correctness.**

**Applying end-to-end thinking in data systems.** **The application itself needs to take end-to-end measures such as duplicate suppression.** **That is a shame, because fault-tolerance mechanisms are hard to get right.** **Low-level mechanisms like TCP work quite well, so the remaining higher-level faults occur fairly rarely.** **It would be really nice to wrap up the high-level fault-tolerance machinery in an abstraction so application code needn't worry — but it seems we have not yet found the right one.**

**Transactions have long been seen as a useful abstraction**, collapsing a wide range of issues down to commit or abort. **That is a huge simplification of the programming model, but it is not enough.** **Transactions are expensive, especially across heterogeneous storage technologies** — **and when we refuse to use distributed transactions because they are too expensive, we end up reimplementing fault-tolerance mechanisms in application code.** **Reasoning about concurrency and partial failure is difficult and counterintuitive, so most application-level mechanisms do not work correctly, and the consequence is lost or corrupted data.**

**For these reasons it is worth exploring fault-tolerance abstractions that make it easy to provide application-specific end-to-end correctness properties while maintaining good performance and operational characteristics at scale.**

## Examples & Systems
The money-transfer transaction as the canonical non-idempotent operation; the `requests` table with a uniqueness constraint as the fix; Post/Redirect/Get.

## Since the 1st Edition
Essentially unchanged from the 1st edition's [[The End-to-End Argument for Databases]] — the same money-transfer example, the same request-ID solution with the same UUID, the same Saltzer/Reed/Clark quotation, and the same conclusion about the missing abstraction. Very stable, because the argument is from 1984 and the problem it describes is unsolved.

## Related
- up: [[Aiming for Correctness (2e)]] · chapter: [[Ch 13 - A Philosophy of Streaming Systems (2e)]]
- [[Exactly-Once Message Processing Revisited (2e)]] — the same pattern inside the database
- [[Enforcing Constraints (2e)]] — the uniqueness constraint this relies on
- [[Fault Tolerance (Stream Processing) (2e)]] — idempotence in stream processors
- 1st edition: [[The End-to-End Argument for Databases]] — the same subtopic
