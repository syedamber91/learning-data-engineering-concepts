---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 2
chapter_title: Defining Nonfunctional Requirements
type: topic
tags: [ddia2, case-study, fan-out, materialized-view, social-network]
sources:
  - raw/ch02.md
---
# Case Study: Social Network Home Timelines
The chapter grounds its abstractions in one worked problem: implement a social network in the style of X (formerly Twitter), where users post messages and follow other users. The book is upfront that this is a huge simplification of how such a service actually works, but it makes the issues of large-scale systems concrete.

The numbers that drive everything:
- **500 million posts per day** — 5,800 posts per second on average.
- Spikes as high as **150,000 posts per second**.
- The average user **follows 200 people and has 200 followers** — but with a very wide range: most people have a handful of followers, and a few celebrities (Barack Obama is the example) have over 100 million.
- Assume **10 million users online simultaneously**, and a five-second freshness target: after somebody posts, their followers should see it within five seconds.

## Subtopics
- [[Representing Users, Posts, and Follows (2e)]] — the obvious relational schema, the home-timeline query, and the arithmetic that shows it cannot work.
- [[Materializing and Updating Timelines (2e)]] — precompute instead: fan-out on write, the materialized timeline cache, and the two extreme cases it breaks on.

## Key Takeaways
- The case study exists to demonstrate that **the naive design fails on arithmetic, not on taste**. Polling the query every five seconds for 10 million online users means 2 million timeline queries per second; each fetches recent posts from 200 followed accounts, giving 400 million lookups per second.
- The fix is a **read/write trade**: precompute each user's timeline so reads are cheap, and pay for it with more work on every write.
- The trade is worth it here — 5,800 posts/sec × fan-out 200 gives just over 1 million timeline writes per second, versus 400 million lookups — but it is a trade, not a free win.
- The distribution matters more than the average. Both problems the design hits (users following tens of thousands of accounts, celebrities with millions of followers) are tail cases invisible in the "average user follows 200" figure.
- Load spikes can be absorbed by **enqueueing** the deliveries: timelines take a bit longer to update, but they remain fast to *load*, since reads come from a cache regardless.

## Since the 1st Edition
The 1st edition used the same Twitter example, but as a short illustration inside its [[Describing Load]] subtopic, and it framed the choice as two approaches to the timeline (query on read versus fan-out on write) with the note that Twitter had moved between them. The 2nd edition promotes it to a topic of its own, adds the push-versus-poll dimension, names the result as a **materialized view** connecting it to the rest of the book, and treats the celebrity case as a genuinely unsolved infrastructure problem rather than a footnote.

## Related
- chapter: [[Ch 02 - Defining Nonfunctional Requirements (2e)]]
- [[Understanding Load (2e)]] — the general lesson this case study is teaching
- [[Materialized Views and Data Cubes (2e)]] — the same technique in an analytics setting
- 1st edition: [[Describing Load]] — the example's original, smaller home
