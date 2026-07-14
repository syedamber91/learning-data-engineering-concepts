---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 1
chapter_title: Reliable, Scalable, and Maintainable Applications
topic: Scalability
type: subtopic
tags: [ddia, load-parameters, fan-out, twitter, write-amplification]
sources:
  - raw/ch01.md
---
# Describing Load
> Before you can discuss growth you must pick load parameters that capture your real bottleneck — Twitter's bottleneck turned out to be fan-out, not tweet volume.

## The Idea
"What happens if load doubles?" is unanswerable until load is described with concrete numbers — *load parameters*. Which numbers matter depends entirely on the architecture: web-server requests per second, a database's read/write ratio, simultaneously active chat users, cache hit rate. Sometimes the average case dominates; sometimes a handful of extreme cases dictate everything. Choosing the wrong parameter means optimizing the wrong thing.

## How It Works
Twitter (November 2012 figures) is the worked example. Two core operations: posting a tweet (4.6k requests/sec average, peaks above 12k/sec) and reading the home timeline (300k requests/sec). Raw write volume of 12k/sec is easy; the hard part is *fan-out* — every user follows and is followed by many others. (The term comes from electronics: the number of gate inputs one output must drive; in transaction systems, the number of downstream requests needed to serve one incoming request.)

Two implementations:
1. **Read-time merge.** Insert each tweet into a global collection; assemble a timeline on demand by joining tweets from everyone the reader follows (a straightforward relational JOIN across tweets, users, and follows tables).
2. **Write-time fan-out.** Keep a per-user timeline cache, like a mailbox — effectively a precomputed [[Materialized Views]]-style result. Posting pushes the tweet into every follower's cache; reads become trivially cheap.

Twitter began with approach 1, buckled under timeline-read load, and switched to approach 2 — sensible because reads outnumber writes by nearly two orders of magnitude, so shifting work to write time pays off.

## Trade-offs & Pitfalls
Approach 2 inflates writes: at ~75 followers per average tweet, 4.6k tweets/sec becomes 345k timeline-cache writes/sec. Worse, the average conceals massive skew — some accounts exceed 30 million followers, so a single celebrity tweet can trigger 30M+ writes, all within Twitter's ~5-second delivery target. Such extreme users are the [[Hot Spots]] of this workload. The decisive load parameter is thus the *distribution of followers per user* (weighted by tweet frequency), not any simple aggregate — the section's central lesson.

## Examples & Systems
- Twitter's hybrid endgame: fan-out on write for most users, but celebrities are exempted — their tweets are fetched and merged at read time, approach-1 style. The example is revisited in [[Ch 12 - The Future of Data Systems]].

## Related
- up: [[Scalability]] · chapter: [[Ch 01 - Reliable, Scalable, and Maintainable Applications]]
- [[Describing Performance]] — the measurement half of the scalability conversation
- [[Approaches for Coping with Load]] — what to do once load is described
- [[Skewed Workloads and Relieving Hot Spots]] — Ch 6 on celebrity-style skew
- [[Evolvability - Making Change Easy]] — "refactoring" between approaches 1 and 2 as an evolvability case
