---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 13
chapter_title: A Philosophy of Streaming Systems
topic: Unbundling Databases
type: subtopic
tags: [ddia2, write-path, read-path, websockets, offline-first, reads-as-events]
sources:
  - raw/ch13.md
---
# Observing Derived State
> Indexes, caches, and materialized views all do the same thing: shift the boundary between how much work happens at write time and how much at read time.

## The Idea
**Dataflow systems give you a process for creating derived datasets and keeping them up to date. Call that the write path**: whenever information is written, it may go through multiple stages of batch and stream processing until every derived dataset incorporates it.

**But why create the derived dataset? Because you want to query it later. That is the read path**: when serving a request, you read from the derived dataset, perhaps process further, and construct the response.

**Together they encompass the whole journey of the data, from collection to consumption.** **The write path is the precomputed portion — done eagerly as soon as data comes in, regardless of whether anyone has asked to see it.** **The read path happens only when someone asks.** **If you know functional programming: the write path is similar to eager evaluation and the read path to lazy evaluation.**

**The derived dataset is where the two paths meet.** **It represents a trade-off between the amount of work done at write time and the amount done at read time.**

## How It Works
**Materialized views and caching.** **A full-text search index is a good example: the write path updates the index, the read path searches it.** **Writes update index entries for all terms in the document; reads search for each query word and apply Boolean logic.**

**Without an index, a search query would scan all documents like `grep`** — very expensive at scale. **No index means less work on the write path but a lot more on the read path.**

**At the other extreme, you could precompute results for all possible queries** — **less read work, no Boolean logic — but the write path would be far more expensive, and the set of possible queries is infinite (or at least exponential in the number of terms), so precomputing all of them is impossible.**

**In between: precompute results for a fixed set of the most common queries, serving those quickly and the rest from the index.** **This is a cache of common queries — though we could also call it a materialized view, since it must be updated when new documents appear that should be included.**

**So an index is not the only possible boundary between the paths.** **The role of caches, indexes, and materialized views is simple: they shift the boundary between read path and write path, letting us do more work at write time by precomputing results in order to save effort at read time.** **This was exactly the topic of the social network home timeline case study — including how the boundary might be drawn differently for celebrities than for ordinary users. After 500 pages, we have come full circle.**

**Stateful, offline-capable clients.** **In the past, web browsers were stateless clients useful only with an internet connection.** **Now single-page JavaScript web apps have stateful capabilities including client-side UI interaction and persistent local storage, and mobile apps store a lot of state on the device without needing a server round trip for most interactions.**

**Persistent local state enables applications where users work offline and sync in the background when a connection is available.** **Since mobile devices sometimes have slow and unreliable connections, it's a big advantage if the UI doesn't wait for synchronous network requests and apps mostly work offline.**

**Moving away from stateless clients talking to a central database opens a world of new opportunities.** **We can think of the on-device state as a cache of state on the server: the pixels on the screen are a materialized view of model objects in the client app, and the model objects are a local replica of state in a remote datacenter.**

**Pushing state changes to clients.** **Load a typical web page and if the data subsequently changes on the server, the browser doesn't find out until you reload.** **The browser reads at one point in time assuming the data is static; it does not subscribe to updates.** **So the state in the browser is a stale cache not updated unless you explicitly poll.** (**HTTP-based feed protocols like RSS are really just a basic form of polling.**)

**More recent protocols moved beyond request/response.** **Server-sent events (the EventSource API) and WebSockets provide channels by which a browser keeps an open TCP connection and the server actively pushes messages** — **an opportunity for the server to inform the client about changes to state it has stored locally, reducing staleness.**

**In terms of the model, actively pushing state changes all the way to client devices means extending the write path all the way to the end user.** **A client still needs a read path for its initial state, but thereafter it can rely on a stream of state changes.** **The stream processing and messaging ideas are thus not restricted to running in a datacenter — we can extend them all the way to end-user devices.**

**Devices will be offline some of the time and unable to receive notifications — but we already solved that problem**: **a consumer of a log-based broker can reconnect after failing or becoming disconnected and ensure it doesn't miss messages that arrived while it was gone.** **The same technique works for individual users, where each device is a small subscriber to a small stream of events.**

**End-to-end event streams.** **Tools for stateful clients and UIs such as React and Elm already update the rendered UI in response to state changes.** **It would be very natural to extend this model to also allow a server to push state change events into the client-side event pipeline.**

**State changes could then flow through an end-to-end write path: from the interaction on one device that triggers the change, through event logs and derived data systems and stream processors, all the way to the user interface on another device** — **propagated with fairly low delay, say under one second end to end.**

**Some applications, such as instant messaging and online games, already have such a "real-time" architecture.** **Why don't we build all applications this way?** **The challenge is that the assumption of stateless clients and request/response interactions is deeply ingrained in our databases, libraries, frameworks, and protocols.** **Many datastores support read and write operations returning a single response; far fewer support operations returning a stream of responses over time.** **Extending the write path to the end user would require fundamentally rethinking how we build many of these systems, moving from request/response toward publish/subscribe dataflow** — **effort, but with the advantage of making UIs more responsive and providing better offline support.**

## Trade-offs & Pitfalls
**Reads are events too.** **When a stream processor writes derived data to a store and that store is queried, the store acts as the boundary between write and read paths, allowing random-access reads that would otherwise require scanning the whole event log.**

**Usually the datastore is separate from the streaming system — but stream processors also maintain state for aggregations and joins.** **This state is normally hidden inside the processor, but some frameworks allow it to be queried by outside clients, turning the processor into a kind of simple database.**

**Take that further.** **In the model so far, writes go through an event log while reads are transient network requests going directly to the nodes holding the data.** **Reasonable, but not the only possibility: you can represent read requests as streams of events too, sending both reads and writes through a stream processor that responds to read events by emitting the result to an output stream.**

**When both are events routed to the same operator, we are in fact performing a stream–table join between the stream of read queries and the database.** **Each read event is sent to the shard holding the relevant data, just as batch and stream processors copartition inputs on the same key when joining.** **This correspondence between serving requests and performing joins is quite fundamental: a one-off read passes through the join operator, which then immediately forgets it; a subscribe request is a persistent join with past and future events on the other side.**

**Recording a log of read events also has benefits for tracking causal dependencies and data provenance.** **The log would let you reconstruct what the user saw before making a decision** — **in an online shop, the predicted shipping date and inventory status shown likely affect whether they buy, so analyzing that connection requires recording the result of the user's query.** **Writing read requests to durable storage thus enables better tracking of causal relationships, but incurs additional storage and I/O costs.** **Optimizing to reduce that overhead is still an open research problem — but if you already log read requests for operational purposes, it's not a big change to make that log the source of the requests instead.**

**Multishard data processing.** **For single-shard queries, sending them through a stream is perhaps overkill.** **But the idea opens the possibility of distributed execution of complex queries combining data from several shards, using the message routing, sharding, and joining infrastructure stream processors already provide.**

**Storm's distributed RPC supports this** — **it has been used to compute the number of people who have seen a URL on a social network, the union of the follower sets of everyone who posted it, which requires combining results from many shards.** **Another example is fraud prevention: assessing whether a purchase is fraudulent by examining reputation scores for the user's IP address, email address, billing address, and shipping address — each reputation database itself sharded, so collecting scores requires a sequence of joins with differently sharded datasets.** **Data warehouse query execution graphs have similar characteristics.**

**If you need this kind of multishard join, it is probably simpler to use a database providing the feature than to implement it with a stream processor.** **But treating queries as streams provides an option for large-scale applications running against the limits of conventional off-the-shelf solutions.**

## Examples & Systems
Server-sent events and WebSockets; React and Elm; Storm's distributed RPC; the fraud-prevention multishard join.

## Since the 1st Edition
Essentially unchanged from the 1st edition's [[Observing Derived State]] — the same write-path/read-path model, the same search-index trade-off, the same push-to-client discussion, the same reads-as-events idea, and the same multishard examples. **Updated:** the offline-capable-clients section now points at the substantially expanded [[Sync Engines and Local-First Software (2e)]] in Chapter 6 rather than making the local-first argument here.

## Related
- up: [[Unbundling Databases (2e)]] · chapter: [[Ch 13 - A Philosophy of Streaming Systems (2e)]]
- [[Case Study - Social Network Home Timelines (2e)]] — the boundary shift, from Chapter 2
- [[Sync Engines and Local-First Software (2e)]] — offline-capable clients in full
- [[Stream Joins (2e)]] — the stream–table join reads-as-events becomes
- 1st edition: [[Observing Derived State]] — the same subtopic
