---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 11
chapter_title: Batch Processing
topic: Batch Processing Models
type: subtopic
tags: [ddia2, sort-merge-join, secondary-sort, group-by, star-schema]
sources:
  - raw/ch11.md
---
# Joins and Grouping
> The shuffle brings every record with the same key to the same reducer. Once you see that, distributed joins become obvious.

## The Idea
**A typical batch join**: on the left, **a log of events describing what logged-in users did on a website** — **activity events or clickstream data** — and on the right, **a database of users.** **You can think of this as part of a star schema: the event log is the fact table, and the user database is one of the dimensions.**

**To analyse activity events using information from the user database** — finding out whether certain pages are more popular with younger or older users, using the date-of-birth field — **you need to compute a join. How, assuming both tables are so large they must be sharded?**

## How It Works
**Use the fact that the shuffle brings together all key-value pairs with the same key at the same reducer, no matter which shard they came from. Here, the user ID serves as the key.**

- **One mapper goes over the user activity events and emits page view URLs keyed by user ID.**
- **Another mapper goes over the user database row by row, extracting user ID as key and date of birth as value.**
- **The shuffle then ensures a reducer can access a particular user's date of birth and all of that user's page view events at the same time.**

**The job can even arrange records to be sorted such that reducers always see the user database record first, followed by activity events in timestamp order. This is a secondary sort.**

**The reducer's join logic is now easy**: **the first value is expected to be the date of birth, stored in a local variable; it then iterates over the activity events with the same user ID, outputting each viewed URL along with the viewer's date of birth.** **Since a reducer processes all records for a user ID in one go, it needs to keep only one user record in memory at a time, and never makes any requests over the network.** **This is a sort-merge join**, since **mapper output is sorted by key and the reducers merge the sorted lists of records from both sides.**

**Grouping works the same way.** **The next job in the workflow calculates the distribution of viewer ages per URL**: **shuffle the data using the URL as key**, and **once sorted, reducers iterate over all page views for a single URL, keeping a counter per age group and incrementing the appropriate one.** **This is how you implement a group by operation and aggregation.**

## Trade-offs & Pitfalls
- **The one-record-in-memory property is the point.** A sort-merge join scales because the reducer's memory requirement is bounded by one record from the dimension side, not by the size of either input.
- **Secondary sort is what makes that possible**: without a guarantee that the dimension record arrives first, the reducer would have to buffer events until it found one.
- **A hot key still hurts**: all records for one user go to one reducer, so a user with a disproportionate number of events creates a straggler.

## Examples & Systems
Clickstream activity events joined against a user profile database, as a fact-and-dimension pair.

## Since the 1st Edition
The sort-merge join and secondary sort come straight from the 1st edition's [[Reduce-Side Joins and Grouping]], with the same example. **Substantially compressed, though:** the 1st edition devoted several subtopics to join algorithms — **reduce-side joins, broadcast hash joins, partitioned hash joins, map-side merge joins, handling skew** — while **the 2nd edition covers only the sort-merge join and leaves algorithm selection to the query optimizer**, which is consistent with its argument that the frontier moved from mechanics to usability.

## Related
- up: [[Batch Processing Models (2e)]] · chapter: [[Ch 11 - Batch Processing (2e)]]
- [[Shuffling Data (2e)]] — the mechanism this depends on
- [[Stars and Snowflakes - Schemas for Analytics (2e)]] — the fact/dimension shape
- [[Query Languages (2e)]] — where join algorithm choice now lives
- 1st edition: [[Reduce-Side Joins and Grouping]] — the closest predecessor
