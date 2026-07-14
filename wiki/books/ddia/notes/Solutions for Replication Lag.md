---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 5
chapter_title: Replication
topic: Problems with Replication Lag
type: subtopic
tags: [ddia, transactions, eventual-consistency, system-design]
sources:
  - raw/ch05.md
---
# Solutions for Replication Lag

> Design for the worst-case lag; if stale reads hurt users, push the stronger guarantee into the database (transactions) rather than patching it in application code.

## The Idea

The practical question for any eventually consistent system: what happens to the user experience if lag stretches to minutes or hours? If the honest answer is "nothing breaks," eventual consistency is fine. If users would be harmed, the system needs a stronger guarantee — such as read-after-write — designed in from the start. The trap is *pretending replication is synchronous when it is actually asynchronous*: everything works in testing, then fails in production when lag spikes.

## How It Works

Two layers where the fix can live:

- **Application layer**: the techniques from [[Reading Your Own Writes]] and [[Monotonic Reads]] — leader-directed reads, replica pinning, tracked timestamps. These work but scatter subtle distributed-systems reasoning across app code, where it is complex and easy to get wrong.
- **Database layer**: this is precisely why **transactions** exist — a mechanism by which the database provides stronger guarantees so applications can stay simple. Single-node transactions are decades old and well understood.

## Trade-offs & Pitfalls

- In the shift to distributed (replicated + partitioned) systems, many databases *abandoned* transactions, arguing they are too costly for performance and availability and that [[Eventual Consistency]] is unavoidable at scale. Kleppmann's verdict: partially true but **overly simplistic** — the rest of the book builds the more nuanced picture, returning to transactions in Chapter 7 ([[The Slippery Concept of a Transaction]]) and to consensus-backed guarantees in Chapter 9.
- Application-level fixes are per-anomaly patches; each new read path re-opens the same class of bugs.
- Stronger database guarantees cost latency and availability — the recurring theme quantified later in [[The Cost of Linearizability]].

## Examples & Systems

- Read-scaled follower fleets behind web applications are the setting for all these mitigations.
- The NoSQL generation (Dynamo-style stores) exemplifies the "transactions are too expensive" position; Chapters 7 and 9 present the counter-arguments and alternative mechanisms (Part III explores derived-data alternatives).

## Related

- up: [[Problems with Replication Lag]] · chapter: [[Ch 05 - Replication]]
- [[The Slippery Concept of a Transaction]] — the database-level answer developed in Ch 7
- [[Consistency Guarantees]] — the menu of stronger models in Ch 9
- [[Reading Your Own Writes]] — the app-level patch this note argues to lift into the DB
- [[The Cost of Linearizability]] — what the strongest guarantee costs
