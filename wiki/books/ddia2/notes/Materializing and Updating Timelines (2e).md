---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 2
chapter_title: Defining Nonfunctional Requirements
topic: Case Study - Social Network Home Timelines
type: subtopic
tags: [ddia2, fan-out, materialized-view, cache, celebrity-problem]
sources:
  - raw/ch02.md
---
# Materializing and Updating Timelines
> Stop asking the question at read time. Answer it at write time instead, once per follower — and then deal with the celebrity who has 100 million of them.

## The Idea
Two changes fix the naive design. First, instead of the client polling, the **server actively pushes** new posts to followers who are currently online. Second, **precompute the query result** so a request for the home timeline is served from a cache.

Concretely: for each user, store a data structure containing their home timeline. Every time a user posts, look up all their followers and insert the post into each follower's home timeline — like delivering a message to a mailbox. On login the user simply receives this precomputed timeline, and to be notified of new posts their client just subscribes to the stream of posts being added to it.

## How It Works
- **Fan-out** is the term for one initial request causing several downstream requests; the fan-out factor is the multiplier. Here, one post fans out to all the poster's followers.
- The arithmetic now runs the other way: at 5,800 posts/sec with an average fan-out of 200, that is just over **1 million home-timeline writes per second** — a lot, but a significant saving against 400 million per-sender lookups per second.
- Load spikes are absorbed by **enqueueing** deliveries. If a special event spikes the post rate, timeline delivery can lag a little; timelines still *load* fast, because they are served from cache regardless.
- This precompute-and-update pattern is **materialization**, and the timeline cache is a **materialized view**. It speeds up reads and pays for it with more work on writes.

## Trade-offs & Pitfalls
The write cost is modest for most users, but a social network has to handle two extremes:
- **A user following a very large number of active accounts** has a high rate of writes into their materialized timeline. The book's answer is pragmatic: that user is not going to read all of it anyway, so it is acceptable to **drop some of their timeline writes** and show only a sample of posts from the accounts they follow.
- **A celebrity with millions of followers** posting is the opposite case, and here dropping writes is *not* acceptable. One solution is to handle celebrity posts separately: store them apart rather than inserting them into millions of timelines, and merge them with the materialized timeline at read time. Even with such optimisations, the book notes that handling celebrities on a social network can require a lot of infrastructure.

The general shape — a hybrid where most content is fanned out on write and a minority is merged on read — is the standard answer, and it exists purely because the follower distribution has a long tail.

## Examples & Systems
The timeline cache as a materialized view; a per-user subscription stream for push delivery; a queue to smooth fan-out during load spikes.

## Since the 1st Edition
The 1st edition described the fan-out-on-write approach and mentioned that the hybrid (celebrities merged at read time) is what Twitter moved to. The 2nd edition adds the push/subscribe delivery model, names materialization explicitly and links it to the book's wider treatment of materialized views and derived data, and adds the "drop writes for users who follow too many accounts" case, which the 1st edition did not discuss.

## Related
- up: [[Case Study - Social Network Home Timelines (2e)]] · chapter: [[Ch 02 - Defining Nonfunctional Requirements (2e)]]
- [[Systems of Record and Derived Data (2e)]] — the timeline is derived data, rebuildable from posts and follows
- [[Materialized Views and Data Cubes (2e)]] — the analytics-side version of the same idea
- [[Skewed Workloads and Relieving Hot Spots (2e)]] — the celebrity problem generalised to sharding
