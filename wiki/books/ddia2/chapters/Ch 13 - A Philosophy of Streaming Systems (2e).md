---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 13
chapter_title: A Philosophy of Streaming Systems
type: chapter-moc
tags: [ddia2, data-integration, unbundling, dataflow, correctness, auditing, moc]
sources:
  - raw/ch13.md
---
# Ch 13 – A Philosophy of Streaming Systems
Chapter 2 set the goal of applications that are **reliable, scalable, and maintainable**, and those themes have run through every chapter — fault-tolerance algorithms for reliability, sharding for scalability, evolution and abstraction for maintainability.

**This chapter brings all these ideas together and builds on the streaming/event-driven architecture ideas from Chapter 12 to develop a philosophy of application development that meets those goals.** **It is more opinionated than previous chapters, presenting a deep dive into one particular philosophy rather than comparing multiple approaches.**

## Map
- [[Data Integration (2e)]] — no one tool fits every use, so you must combine them
  - [[Combining Specialized Tools by Deriving Data (2e)]] — reasoning about dataflows, derived data versus distributed transactions, and the limits of total ordering
  - [[Batch and Stream Processing (2e)]] — maintaining derived state, reprocessing for evolution, and unifying the two
- [[Unbundling Databases (2e)]] — the Unix and relational philosophies, reconciled
  - [[Composing Data Storage Technologies (2e)]] — federated reads, unbundled writes, and the meta-database of everything
  - [[Designing Applications Around Dataflow (2e)]] — application code as a derivation function, and the separation of Church and state
  - [[Observing Derived State (2e)]] — write path, read path, pushing state to clients, and reads as events
- [[Aiming for Correctness (2e)]] — why ACID isn't the last word
  - [[The End-to-End Argument for Databases (2e)]] — why a serializable database still can't stop a duplicate payment
  - [[Enforcing Constraints (2e)]] — uniqueness via log sharding, and multishard requests without atomic commit
  - [[Timeliness and Integrity (2e)]] — the two things "consistency" conflates, and coordination-avoiding systems
  - [[Trust, but Verify (2e)]] — auditing, designing for auditability, and cryptographic integrity checks

## Chapter Summary
**No one single tool can efficiently serve all possible use cases, so applications must compose several pieces of software.** **The data integration problem is solved by using batch processing and event streams to let data changes flow among systems**: **certain systems are designated as systems of record, and other data is derived from them through transformations**, maintaining **indexes, materialized views, machine learning models, statistical summaries, and more.** **Making these derivations asynchronous and loosely coupled helps prevent a problem in one area from spreading to unrelated areas, increasing robustness and fault tolerance.**

**Expressing dataflows as transformations from one dataset to another also helps evolve applications.** **To change a processing step — altering the structure of an index or cache — just rerun the new transformation code on the whole input to rederive the output; and if something goes wrong, fix the code and reprocess to recover.**

**These processes are quite similar to what databases already do internally**, which is why the chapter recasts dataflow applications as **unbundling the components of a database and building an application by composing loosely coupled components.** **Derived state can be updated by observing changes in the underlying data, and observed by downstream consumers — and this dataflow can be taken all the way to the end-user device, building UIs that dynamically update and continue to work offline.**

**On correctness:** **strong integrity guarantees can be implemented scalably with asynchronous event processing, by using end-to-end request identifiers to make operations idempotent, and by checking constraints asynchronously.** **Clients can either wait until the check has passed, or go ahead without waiting and risk having to apologize.** **This approach is much more scalable and robust than the traditional approach of distributed transactions, and it fits with how many business processes work in practice.**

**And because we cannot fully trust that every component is free from corruption, we should periodically check the integrity of our data — auditing — and design systems that make that auditing feasible.**

## Since the 1st Edition
This is the 1st edition's Chapter 12, "The Future of Data Systems," **renamed to A Philosophy of Streaming Systems** — a more honest title, since the chapter is a synthesis of the book's argument rather than a forecast. **The renaming also reflects a scope change: the 1st edition's Chapter 12 ended with a long section on "Doing the Right Thing" covering ethics, bias, surveillance, and privacy. That material is now a full chapter of its own**, [[Ch 14 - Doing the Right Thing (2e)]].

**Retained essentially intact:** the data integration argument, the limits of total ordering, the batch/stream unification, the federation-versus-unbundling framing, the spreadsheet and VisiCalc analogy, the write path/read path model, the end-to-end argument with the duplicate-payment example, uniqueness constraints via log sharding, the multishard payment example, the timeliness/integrity distinction, loosely interpreted constraints and compensating transactions, and the trust-but-verify auditing discussion.

**Updated:** the federated-database examples now name **Trino, Hoptimator, and Xorq** alongside PostgreSQL's foreign data wrappers; the lambda architecture is described as having **"fallen out of use"** rather than as a live proposal, with the **kappa architecture** named as its successor; and the local-first material links to the substantially expanded [[Sync Engines and Local-First Software (2e)]] in Chapter 6.

## Related
- home: [[Home (2e)]] · previous: [[Ch 12 - Stream Processing (2e)]] · next: [[Ch 14 - Doing the Right Thing (2e)]]
- [[Ch 12 - Stream Processing (2e)]] — the machinery this philosophy is built on
- [[Systems of Record and Derived Data (2e)]] — the vocabulary introduced in Chapter 1
- 1st edition: [[Ch 12 - The Future of Data Systems]] — the chapter this one revises and renames
