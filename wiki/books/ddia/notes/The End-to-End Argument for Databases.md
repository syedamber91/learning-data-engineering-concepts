---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 12
chapter_title: The Future of Data Systems
topic: Aiming for Correctness
type: subtopic
tags: [ddia, end-to-end-argument, idempotence, duplicate-suppression]
sources:
  - raw/ch12.md
---
# The End-to-End Argument for Databases

> No layer below the application can fully suppress duplicates (or corruption); correctness needs an identifier — or checksum — carried from end user to database.

## The Idea
Using a strongly consistent database does not make an application correct: a buggy app writes bad data with perfect serializability, and immutable append-only data aids recovery but isn't a cure. Kleppmann's deeper example is duplicate execution. [[Exactly-Once Semantics]] means the *final effect* is as if no fault occurred despite retries — typically via [[Idempotence]], which itself needs operation-ID metadata and [[Fencing Tokens]] on failover. The reasoning chain: each layer's deduplication covers only its own scope, so only the endpoints can finish the job.

## How It Works
The argument builds through the layers:
1. **TCP** deduplicates and reorders packets — but only within one connection. A client that sends `COMMIT` and loses the connection before the reply doesn't know if the transaction committed; retrying on a new connection is a *new* transaction to the database. A non-idempotent transfer can execute twice ($22 instead of $11) — which is why the classic textbook transfer transaction isn't how real banks work.
2. **[[Two-Phase Commit]]** lets a coordinator resolve in-doubt transactions across reconnections, breaking the TCP–transaction 1:1 coupling — still insufficient, because the *user's* browser sits beyond it: a timed-out POST gets manually resubmitted ("submit this form again?" → yes), a fresh request to the web server, a fresh transaction to the database.
3. **The fix**: generate an operation ID at the true endpoint (a UUID in the client, or a hash of form fields), pass it through every hop, and enforce a uniqueness constraint on it in the database — relational databases maintain uniqueness correctly even at weak [[Isolation Levels]], unlike application-level check-then-insert, which [[Write Skew and Phantoms]] breaks. The request-ID table doubles as an event log: balance updates could be derived downstream from the request event, edging toward [[Event Sourcing]].
This instantiates Saltzer/Reed/Clark's 1984 end-to-end argument: a function can only be implemented completely with the endpoints' knowledge; lower layers offer at best a performance optimization. Same logic for integrity (Ethernet/TCP/TLS checksums miss software bugs and disk corruption — end-to-end checksums needed) and encryption (WiFi passwords and TLS each guard one hop; only end-to-end encryption guards them all).

## Trade-offs & Pitfalls
- Low-level mechanisms remain worthwhile — they make higher-level faults rare — just never sufficient.
- The uncomfortable conclusion: applications must implement their own fault-tolerance measures, and application code gets this wrong far more often than battle-tested infrastructure. Transactions were a beautiful abstraction (many failure modes collapsed into commit-or-abort), but they're expensive across heterogeneous systems, and abandoning them pushes the complexity back to the app. Kleppmann's call: we need a new abstraction that provides end-to-end correctness cheaply at scale — we haven't found it yet.

## Examples & Systems
The double money transfer; browser POST retry; Post/Redirect/Get's limits; the `requests` table with a unique `request_id`; TCP/Ethernet/TLS as partial layers.

## Related
- up: [[Aiming for Correctness]] · chapter: [[Ch 12 - The Future of Data Systems]]
- [[Fault Tolerance]] — stream processing's exactly-once machinery, one layer in this stack
- [[Atomic Commit and Two-Phase Commit (2PC)]] — why even 2PC can't cover the last hop
- [[Enforcing Constraints]] — where the end-to-end request ID meets a uniqueness check
- [[State, Streams, and Immutability]] — immutability as the recovery-friendly baseline
