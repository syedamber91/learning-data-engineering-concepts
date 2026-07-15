---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 12
chapter_title: The Future of Data Systems
topic: Unbundling Databases
type: subtopic
tags: [ddia, write-path, read-path, offline-first, reads-as-events]
sources:
  - raw/ch12.md
---
# Observing Derived State

> A derived dataset is where the eager write path meets the lazy read path — and that boundary can be pushed anywhere, even onto the end user's device.

## The Idea
Why maintain derived datasets at all? To read them later. Kleppmann splits the data's journey in two: the **write path** — everything precomputed eagerly when data arrives (batch/stream stages updating indexes, views, models), like eager evaluation — and the **read path** — work done only when someone asks, like lazy evaluation. A search index, cache, or materialized view is precisely the meeting point, and its position encodes a trade-off: no index means cheap writes but grep-like scans on read; precomputing results for every possible query is infinite write-side work; caching common queries sits between. Caches, [[Secondary Indexes]], and [[Materialized Views]] all just *shift the boundary*, doing more write-path work to save read-path effort — the same analysis as the Twitter timeline example in [[Describing Load]], closing the book's loop.

## How It Works
- **Stateful, offline-capable clients.** The stateless-browser assumption is historical, not necessary. Single-page apps and mobile apps hold real state, enabling *offline-first* designs: work against an on-device database, sync in the background. Then device state is a cache of server state; the pixels are a materialized view onto client model objects, themselves a replica of datacenter state.
- **Pushing state changes to clients.** Plain HTTP reads a point-in-time snapshot that silently goes stale (RSS polling barely improves it). Server-sent events and WebSockets keep a channel open so servers push changes — extending the write path to the end user. Offline devices are just lagging log consumers: like a [[Log-Based Message Broker]] consumer reconnecting at its offset, a device catches up on missed events.
- **End-to-end event streams.** Elm and React/Flux/Redux already manage client state as event streams akin to [[Event Sourcing]]; letting servers inject state-change events into the same pipeline yields sub-second dataflow from one user's interaction to another user's screen. Instant messaging and games prove it works; the blocker is that request/response is baked into databases, libraries, and protocols. Building this needs publish/subscribe dataflow as the default mindset.
- **Reads are events too.** Stream processors keep queryable state anyway; go further and represent read requests as events routed through the processor, making serving a request literally a stream–table join against the queried partition. This enables reconstructing what a user *saw* before deciding (causal provenance — e.g. did the displayed shipping estimate drive the purchase?), at extra storage/I/O cost.

## Trade-offs & Pitfalls
Reads-as-events shine for **multi-partition** queries: Storm's distributed RPC computes cross-partition unions (who saw a tweeted URL); fraud scoring joins a purchase against several differently partitioned reputation databases. But for single-partition lookups the machinery is overkill, and MPP databases already do multi-partition joins — use them unless you're beyond off-the-shelf limits.

## Examples & Systems
Full-text search index as the canonical boundary; offline-first mobile apps; EventSource/WebSockets; Elm, React/Flux/Redux; Storm distributed RPC; fraud-prevention reputation joins.

## Related
- up: [[Unbundling Databases]] · chapter: [[Ch 12 - The Future of Data Systems]]
- [[Describing Load]] — Twitter's fan-out as the original boundary-shifting example
- [[State, Streams, and Immutability]] — state/log duality underpinning replayable views
- [[Request Routing]] — routing read events to the right partition
- [[Enforcing Constraints]] — multi-partition writes, the twin of multi-partition reads
