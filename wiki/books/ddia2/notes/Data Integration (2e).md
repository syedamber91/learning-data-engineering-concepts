---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 13
chapter_title: A Philosophy of Streaming Systems
type: topic
tags: [ddia2, data-integration, trade-offs, specialized-tools]
sources:
  - raw/ch13.md
---
# Data Integration
**A recurring theme in this book: for any given problem there are several solutions, each with its own pros, cons, and trade-offs.** Storage engines: log-structured, B-trees, column-oriented. Replication: single-leader, multi-leader, leaderless. **For a problem such as "I want to store some data and look it up again later," there is no one right solution, but many approaches each appropriate in different circumstances.**

**A software implementation typically has to pick one particular approach.** **It's hard enough to get one code path robust and performing well; trying to satisfy too many use cases with many features is likely to lead to poor implementations of those features, compared to specialized tools.** **So the most appropriate choice of tool also depends on circumstances** — **every piece of software, even a so-called "general-purpose" database, is designed for a particular usage pattern.**

**The first challenge is figuring out the mapping between software products and the circumstances that fit them.** **Vendors are understandably reluctant to tell you the workloads for which their software is poorly suited** — **but the previous chapters have equipped you with questions to ask that help you read between the lines.**

**Even with a perfect understanding of that mapping, there is another challenge.** **In complex applications data is used in various ways, and one piece of software is unlikely to suit all of them. So you inevitably end up cobbling together several pieces of software.**

## Subtopics
- [[Combining Specialized Tools by Deriving Data (2e)]] — dataflow reasoning, and why total ordering doesn't scale forever.
- [[Batch and Stream Processing (2e)]] — the tools for making data end up in the right form in the right places.

## Key Takeaways
- **The problem is not choosing the right tool — it's that you will need several, and they must be kept consistent.**
- **The chapter's answer is to designate systems of record and derive everything else from them, in a defined order** — which turns a multi-system consistency problem into a single-leader replication problem.
- **This topic is the setup for the whole chapter**: data integration is the problem, unbundling is the architecture, and correctness is what you must not lose along the way.

## Since the 1st Edition
Essentially unchanged from the 1st edition's [[Data Integration]] — the same framing and the same two subtopics. One of the most stable topics in the book, because the argument is about the shape of the problem rather than about any particular technology.

## Related
- chapter: [[Ch 13 - A Philosophy of Streaming Systems (2e)]]
- [[Keeping Systems in Sync (2e)]] — the concrete version of this problem
- [[Systems of Record and Derived Data (2e)]] — the vocabulary
- 1st edition: [[Data Integration]] — the same topic
