---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 7
chapter_title: Transactions
topic: The Slippery Concept of a Transaction
type: subtopic
tags: [ddia, transactions, atomicity, error-handling]
sources:
  - raw/ch07.md
---
# Single-Object and Multi-Object Operations
> Atomicity and isolation matter both for a single key-value write and — much more importantly — for keeping several related objects in sync within one transaction.

## The Idea
Multi-object transactions group writes to several rows, documents, or index entries so they either all take effect or none do. The motivating example: an email app that stores an unread-count as [[Denormalization]] alongside the inbox. Without isolation, a reader can see the new message but a stale counter (a dirty read of half a transaction); without atomicity, a mid-transaction error leaves the counter permanently out of sync with the mailbox.

## How It Works
- Relational databases scope a transaction to a TCP connection: everything between BEGIN and COMMIT belongs together. (Fragile — if the connection drops after a commit request but before the acknowledgment, the client can't tell whether it committed; see [[The End-to-End Argument for Databases]].)
- Many NoSQL stores have multi-put APIs but no transaction semantics: some keys may succeed while others fail.
- Even single-object writes need atomicity (don't store half of a 20 KB JSON document after a network cut, don't splice old and new bytes after a power failure) and isolation (don't let readers see a partial write). Storage engines deliver this per object via a crash-recovery log ([[Write-Ahead Log]]) and per-object locks.
- Richer single-object primitives — atomic increment, compare-and-set — remove read-modify-write races, but calling them "lightweight transactions" or "ACID" is marketing: a transaction properly means grouping operations across multiple objects.

## Trade-offs & Pitfalls
Cases that genuinely need multi-object transactions: foreign-key/graph references that must stay valid together; denormalized data across documents (document models often force this — see [[Relational Versus Document Databases Today]]); [[Secondary Indexes]] that must update in step with the base record. Skipping transactions is possible but pushes error handling and concurrency reasoning onto the application.

Retry-on-abort is the core error-handling pattern, with caveats: if the commit succeeded but its acknowledgment was lost, a retry executes twice (need app-level dedup — see [[Idempotence]]); retrying under overload amplifies the overload (bound retries, back off exponentially); only transient errors (deadlock, failover) are worth retrying, not constraint violations; side effects outside the database (sent emails) happen anyway — coordinating them needs [[Two-Phase Commit]]. Leaderless stores ([[Leaderless Replication]]) instead run "best effort": they won't undo partial work, so recovery is the app's job. Popular ORMs (ActiveRecord, Django) don't retry aborts at all — the exception just surfaces to the user.

## Examples & Systems
Unread-counter email example; 20 KB JSON document write; multi-put key-value APIs; Rails ActiveRecord and Django ORM abort behavior.

## Related
- up: [[The Slippery Concept of a Transaction]] · chapter: [[Ch 07 - Transactions]]
- [[The Meaning of ACID]] — definitions of atomicity and isolation used here
- [[Read Committed]] — the isolation level that prevents the dirty read shown here
- [[Preventing Lost Updates]] — where compare-and-set and atomic ops reappear
- [[Atomic Commit and Two-Phase Commit (2PC)]] — committing across multiple systems
