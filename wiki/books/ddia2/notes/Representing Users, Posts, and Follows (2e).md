---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 2
chapter_title: Defining Nonfunctional Requirements
topic: Case Study - Social Network Home Timelines
type: subtopic
tags: [ddia2, relational-schema, polling, join, case-study]
sources:
  - raw/ch02.md
---
# Representing Users, Posts, and Follows
> Three tables, one join query, and a number that ends the discussion: 400 million lookups per second.

## The Idea
Start with the obvious design. Keep everything in a relational database with three tables — `users`, `posts`, and `follows`. The main read operation the network must support is the **home timeline**: recent posts by the people a user follows (ignoring ads, suggested posts from non-followed accounts, and other extensions).

## How It Works
The timeline is a single SQL query:

```sql
SELECT posts.*, users.* FROM posts
  JOIN follows ON posts.sender_id = follows.followee_id
  JOIN users   ON posts.sender_id = users.id
  WHERE follows.follower_id = current_user
  ORDER BY posts.timestamp DESC
  LIMIT 1000
```

To execute it, the database uses `follows` to find everyone `current_user` follows, looks up recent posts by those users, and sorts by timestamp for the most recent 1,000.

Because posts are supposed to be timely — followers should see a post within five seconds — one approach is for the client to repeat this query every five seconds while the user is online. That is **polling**.

## Trade-offs & Pitfalls
The arithmetic is the whole point:
- 10 million users online at once, polling every five seconds → **2 million timeline queries per second**. Polling less frequently helps, but this is still a lot.
- Each query is expensive on its own: for a user following 200 people, it must fetch recent posts by each of those 200 and merge the lists. 2 million queries/sec × 200 followed accounts = **400 million lookups per second**.
- And that is the *average* case. Some users follow tens of thousands of accounts; for them the query is very expensive and hard to make fast.

Two independent problems are stacked here — polling generates far more queries than there are actual updates, and each query does work proportional to how many accounts the user follows. The next subtopic attacks both.

## Examples & Systems
A conventional relational database with `users` / `posts` / `follows` tables; client-side polling as the delivery mechanism.

## Since the 1st Edition
The 1st edition presented essentially this same query and the same "expensive join" analysis, but compressed into a page inside [[Describing Load]]. What is new is the explicit polling analysis — separating the cost of *asking repeatedly* from the cost of *each answer* — and the online-user count that makes the polling cost concrete.

## Related
- up: [[Case Study - Social Network Home Timelines (2e)]] · chapter: [[Ch 02 - Defining Nonfunctional Requirements (2e)]]
- [[Materializing and Updating Timelines (2e)]] — the design that replaces this one
- [[Normalization, Denormalization, and Joins (2e)]] — the modelling trade-off underneath this schema
