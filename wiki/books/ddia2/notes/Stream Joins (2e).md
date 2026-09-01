---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 12
chapter_title: Stream Processing
topic: Processing Streams
type: subtopic
tags: [ddia2, stream-join, enrichment, materialized-view, slowly-changing-dimension]
sources:
  - raw/ch12.md
---
# Stream Joins
> Three joins, distinguished by whether each input is a stream of activity events or a table changelog — and all three raise the same awkward question about *when* the join happens.

## The Idea
**Stream processing generalizes data pipelines to incremental processing of unbounded datasets, so there is exactly the same need for joins as in batch jobs.** **But the fact that new events can appear at any time makes joins on streams more challenging.** **Three types: stream–stream, stream–table, and table–table.**

## How It Works
**Stream–stream join (window join).** **You have a search feature and want to detect recent trends in searched-for URLs.** **Every search logs an event containing the query and results; every click on a result logs another event.** **To calculate click-through rate per URL you must bring together the search and click events, connected by the same session ID.**

**The click may never come if the user abandons their search, and the time between search and click may be highly variable** — often seconds, but **it could be days or weeks if a user searches, forgets the tab, and returns later.** **Because of variable network delays the click event may even arrive before the search event.** **You choose a suitable window** — joining a click with a search if they occur at most one hour apart.

**Note that embedding the search details in the click event is not equivalent to joining.** **That would tell you only about cases where the user clicked, not about searches with no clicks** — **and to measure search quality you need accurate click-through rates, requiring both.**

**To implement this the processor maintains state: all events in the last hour, indexed by session ID.** **When a search or click event occurs it is added to the appropriate index, and the processor checks the other index for a matching event.** **If there is a match, emit an event saying which result was clicked; if the search event expires without a matching click, emit an event saying which results were not clicked.**

**Stream–table join (stream enrichment).** **The batch example joined user activity events with a database of user profiles.** **It is natural to think of the activity events as a stream and perform the same join continuously**: **input a stream of activity events containing a user ID, output a stream in which the user ID has been augmented with profile information — enriching the events.**

**To perform the join the processor takes one event at a time, looks up the user ID in the database, and adds the profile information.** **The lookup could query a remote database — but such remote queries are likely slow and risk overloading it.** **Another approach: load a copy of the database into the stream processor so it can be queried locally without a network round trip. This is a hash join**, since the local copy might be an in-memory hash table if small enough, or an index on local disk.

**The difference from a batch job is that a batch job uses a point-in-time snapshot as input, whereas a stream processor is long-running and the database contents change over time — so the local copy must be kept up to date.** **This is solved by CDC: the processor subscribes to a changelog of the user profile database as well as the activity event stream.** **When a profile is created or modified, it updates its local copy** — **so we obtain a join between two streams: activity events and profile updates.**

**A stream–table join is very similar to a stream–stream join. The biggest difference is that for the table changelog stream, the join uses a window reaching back to the "beginning of time" — a conceptually infinite window — with newer versions of records overwriting older ones.** **For the stream input, the join might not maintain a window at all.**

**Table–table join (materialized view maintenance).** **The social network home timeline: iterating over everyone a user follows and merging their recent posts is too expensive, so we want a timeline cache, a per-user "inbox" written to as posts are sent, making reading a single lookup.** Maintaining it requires:
- **When user u sends a post, add it to the timeline of every user following u.**
- **When a user deletes a post or their entire account, remove it from all timelines.**
- **When u₁ starts following u₂, add u₂'s recent posts to u₁'s timeline.**
- **When u₁ unfollows u₂, remove u₂'s posts from u₁'s timeline.**

**So you need streams of events for posts (sending and deleting) and follow relationships (following and unfollowing), and the processor must maintain a database of each user's followers so it knows which timelines to update on a new post.**

**Another way of looking at it: the process maintains a materialized view for a query joining two tables** — something like `SELECT follows.follower_id AS timeline_id, array_agg(posts.* ORDER BY posts.timestamp DESC) FROM posts JOIN follows ON follows.followee_id = posts.sender_id GROUP BY follows.follower_id`. **The join of the streams corresponds directly to the join of the tables, and the timelines are effectively a cache of the query result, updated every time the underlying tables change.**

> **If you regard a stream as the derivative of a table, and a join as a product of two tables u·v, something interesting happens: the stream of changes to the materialized join follows the product rule (u·v)′ = u′v + uv′.** **Any change of posts is joined with the current followers, and any change of follows is joined with the current posts.**

## Trade-offs & Pitfalls
**Time dependence of joins.** **All three types require the processor to maintain state derived from one join input and query it when processing records from the other.** **The order of the events maintaining the state is important** — **it matters whether you first follow and then unfollow a user, or the other way round.** **In a sharded event log the ordering within a single shard is preserved, but there is typically no ordering guarantee across different streams or shards.**

**This raises the question: if events on different streams happen around a similar time, in which order are they processed?** **In the stream–table example, if a user updates their profile, which activity events are joined with the old profile and which with the new? Put another way: if state changes over time, and you join with a state, what point in time do you use?**

**Such time dependence occurs in many places.** **If you sell things you must apply the right tax rate to invoices, depending on country or state, product type, and date of sale, since rates change over time.** **When joining sales to a table of tax rates you probably want the rate at the time of the sale, which may differ from the current rate if reprocessing historical data.**

**If the ordering of events across streams is undetermined, the join becomes nondeterministic** — **you cannot rerun the same job on the same input and necessarily get the same result, since the input streams may interleave differently.**

**In data warehouses this is known as a slowly changing dimension (SCD), often addressed by using a unique identifier for a particular version of the joined record** — **every time the tax rate changes it gets a new identifier, and the invoice includes the identifier for the rate at the time of sale.** **This makes the join deterministic, but has the consequence that log compaction is not possible, since all versions of the records in the table must be retained.** **Alternatively, denormalize and include the applicable tax rate directly in every sale event.**

## Examples & Systems
Search-and-click click-through-rate measurement; user activity enrichment via CDC; the social network timeline as a table–table join; slowly changing dimensions in warehouses.

## Since the 1st Edition
Essentially unchanged from the 1st edition's [[Stream Joins]] — the same three join types with the same examples, the same product-rule aside, and the same time-dependence and slowly-changing-dimension discussion. Another very stable section.

## Related
- up: [[Processing Streams (2e)]] · chapter: [[Ch 12 - Stream Processing (2e)]]
- [[Joins and Grouping (2e)]] — the batch counterpart
- [[Change Data Capture (2e)]] — how the table side stays current
- [[Materializing and Updating Timelines (2e)]] — the timeline example in full
- 1st edition: [[Stream Joins]] — the same subtopic
