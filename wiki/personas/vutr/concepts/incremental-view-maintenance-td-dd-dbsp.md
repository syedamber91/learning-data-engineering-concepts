---
persona: vutr
kind: concept
sources:
- raw/olap-cost-and-multi-engine-comparison/quick-insights-on-materialized-views.md
last_updated: '2026-07-15'
qc: passed
slug: incremental-view-maintenance-td-dd-dbsp
topics:
- olap-cost-and-multi-engine-comparison
---

The naive way to keep a materialized view current is to recompute the whole defining query from scratch whenever a source table changes — correct, but increasingly expensive and increasingly slow as the underlying data grows. Incremental View Maintenance (IVM) is the alternative discipline: refresh only the slice of the view that the change actually affects. vutr names three modern lineages of IVM technique, and is candid that the math underneath them is dense enough that he only aims to convey their general shape rather than their full formal detail.

Timely Dataflow (TD), from the Naiad paper, isn't itself an IVM technique — it's the general-purpose computational substrate other systems are built on top of, designed to deliver batch-processor throughput, stream-processor latency, and iterative computation all in one framework (before Naiad, per the notes, applications needed three separate systems to get all three). Every message in TD carries a logical timestamp, and its four-method API (send a message, receive a message, request a notification at a given timestamp, receive that notification) centers on the notification pair as the key mechanism: a node can ask the system to fire a callback "when timestamp t is complete," and the runtime tracks, across the entire distributed cluster, whether any more messages tagged with that timestamp could still arrive — only firing once it's certain none will. That completeness tracking runs entirely separate from the data stream itself, which is what lets multiple points in time be processed concurrently. TD was built for deeply nested iterative algorithms like graph processing, which vutr notes is more power than most SQL materialized views need, since they rarely contain a loop — but the piece IVM systems actually inherit from TD is narrower and non-negotiable: the notification guarantee that tells the system when a given version of a view is complete and safe to emit.

Differential Dataflow (DD) is a programming model built directly on top of TD, and it answers a sharper question: given that we already know when a computation is complete, how do we compute as little as possible as the input changes? DD tracks data as multiple versions, ordered using TD's timestamps, and reuses prior computation across versions rather than recomputing from scratch — the ordering TD provides is precisely what makes that reuse safe.

DBSP takes a different route from the other two, borrowing its formal grounding from Digital Signal Processing rather than building upward from a dataflow substrate. Its framing: a database is a stream of snapshots, changes to the database are a stream of deltas, and a view is a query applied to each snapshot — so maintaining a view incrementally reduces to computing the stream of view-deltas directly from the stream of database-deltas. DBSP formalizes this with four operators (lift, delay, and two operators for recursive programs) that, per vutr's notes, are functionally complete for all relational SQL operations — meaning the theory guarantees any standard SQL query can be mechanically converted into an incremental version, not just a hand-picked subset.

vutr is explicit that he could not find published material on how cloud data warehouses — BigQuery, Snowflake, or Redshift specifically — actually implement incremental materialized-view maintenance internally; that mapping from the TD/DD/DBSP theory to any one vendor's real implementation is left as an open gap rather than something the notes resolve.

*See also: [[materialized-view-tradeoffs-and-streaming-convergence]]*
