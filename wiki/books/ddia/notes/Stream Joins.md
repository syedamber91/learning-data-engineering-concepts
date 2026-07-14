---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 11
chapter_title: Stream Processing
topic: Processing Streams
type: subtopic
tags: [ddia, joins, stream-enrichment, time-dependence]
sources:
  - raw/ch11.md
---
# Stream Joins
> All stream joins keep state from one input and probe it with events from the other — and because that state changes over time, the join's answer depends on event ordering.

## The Idea
Batch pipelines lean heavily on joins, and streams inherit the need. But new events can arrive at any moment, so the batch tactic of sorting both inputs first is unavailable. Three join shapes cover the territory, distinguished by whether each input is an activity stream or a database changelog.

## How It Works
**Stream-stream (window join).** To compute search click-through rates you must pair search events with click events sharing a session ID — a click may lag its search by seconds or weeks, may never come, or may even arrive first. The processor indexes recent events from *both* streams (say, the last hour, keyed by session), checks the opposite index on each arrival, and emits matched or timed-out results. Embedding search details in the click event is no substitute: it misses the searches nobody clicked. **Stream-table (enrichment).** Activity events carrying a user ID get augmented with profile data. Querying a remote database per event is slow and overloads it; instead the processor keeps a local copy — an in-memory hash table or on-disk index, like a map-side hash join ([[Map-Side Joins]]) — kept current by subscribing to the table's [[Change Data Capture]] changelog. Conceptually it's a stream-stream join where the table side has an infinite window and newer versions overwrite older. **Table-table (materialized view maintenance).** Twitter timelines: joining tweet events with follow/unfollow events maintains a per-user cache equivalent to a `SELECT … JOIN … GROUP BY` over the two tables — a stream of changes to the [[Materialized Views]] of the join.

## Trade-offs & Pitfalls
State ordering matters (follow-then-unfollow ≠ unfollow-then-follow), and a partitioned log only orders *within* a partition — never across streams. So which profile version joins an event that arrives near a profile update? If cross-stream ordering is undetermined, the join is nondeterministic: reruns on identical input can differ. Warehouses call this the *slowly changing dimension* problem and fix it by versioning the joined record (each tax-rate change gets a new ID stored in the invoice) — deterministic, but it defeats [[Log Compaction]], since every version must be kept.

## Examples & Systems
Search/click analysis mirrors ad-click attribution (Google's Photon); Twitter's fan-out service is the canonical table-table case; tax-rate-at-time-of-sale illustrates time-dependent enrichment.

## Related
- up: [[Processing Streams]] · chapter: [[Ch 11 - Stream Processing]]
- [[Reduce-Side Joins and Grouping]] — the batch joins these generalize
- [[Reasoning About Time]] — window choice and ordering underpin join semantics
- [[Describing Load]] — the Twitter timeline problem joined here
- [[Fault Tolerance]] — recovering the join state these operators accumulate
