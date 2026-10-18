---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 13
chapter_title: A Philosophy of Streaming Systems
type: topic
tags: [ddia2, correctness, acid, jepsen, transactions]
sources:
  - raw/ch13.md
---
# Aiming for Correctness
**With stateless services that only read data, it's not a big deal if something goes wrong: fix the bug, restart the service, and everything returns to normal.** **Stateful systems such as databases are not so simple. They are designed to remember things forever, so if something goes wrong the effects also potentially last forever — which means they require more careful thought.**

**We want applications that are reliable and correct** — **programs whose semantics are well defined and understood, even in the face of various faults.** **For approximately four decades, the transaction properties of atomicity, isolation, and durability have been the tools of choice.** **However, those foundations are weaker than they seem: witness the confusion of weak isolation levels.**

**In some areas transactions have been abandoned entirely and replaced with models offering better performance and scalability but messier semantics.** **Consistency is often talked about but poorly defined.** **Some assert that we should "embrace weak consistency" for better availability, while lacking a clear idea of what that means in practice.**

**For a topic so important, our understanding and engineering methods are surprisingly flaky.** **It is very difficult to determine whether it is safe to run a particular application using a particular isolation level or replication configuration.** **Simple solutions often appear to work correctly when concurrency is low and there are no faults, but turn out to have many subtle bugs in more demanding circumstances.**

**Kyle Kingsbury's Jepsen experiments have highlighted the stark discrepancies between some products' claimed safety guarantees and their actual behavior in the presence of network problems and crashes.** **And even if infrastructure products were free from problems, application code would still need to correctly use the features they provide — error-prone if the configuration is hard to understand, as with weak isolation levels and quorum configurations.**

**If your application can tolerate occasionally corrupting or losing data in unpredictable ways, life is a lot simpler.** **If you need stronger assurances, serializability and atomic commit are established approaches, but they come at a cost: they typically work in only a single datacenter, ruling out geographically distributed architectures, and they limit the scale and fault-tolerance properties you can achieve.**

**The traditional transaction approach is not going away, but it is not the last word in making applications correct and resilient to faults.**

## Subtopics
- [[The End-to-End Argument for Databases (2e)]] — why a serializable database can't stop a duplicate payment.
- [[Enforcing Constraints (2e)]] — uniqueness and multishard operations without atomic commit.
- [[Timeliness and Integrity (2e)]] — separating the two things "consistency" conflates.
- [[Trust, but Verify (2e)]] — auditing, because assumptions are probabilistic rather than binary.

## Key Takeaways
- **The topic's argument is that correctness is an application-level property, not a database feature you can buy.** Even serializable transactions do not make an application correct.
- **The chapter's positive claim is that strong integrity can be achieved with asynchronous event processing** — end-to-end request IDs, idempotence, and constraint checks — **at better performance and operational robustness than distributed transactions.**
- **And because the assumptions underpinning any of it are probabilistic rather than certain, auditing is not optional.**

## Since the 1st Edition
Essentially unchanged from the 1st edition's [[Aiming for Correctness]] — the same critique of ACID's limits, the same Jepsen citation, and the same four subtopics. Stable, because it is a philosophical argument rather than a technical survey.

## Related
- chapter: [[Ch 13 - A Philosophy of Streaming Systems (2e)]]
- [[Weak Isolation Levels (2e)]] — the confusion this refers to
- [[Formal Methods and Randomized Testing (2e)]] — Jepsen in its own right
- 1st edition: [[Aiming for Correctness]] — the same topic
