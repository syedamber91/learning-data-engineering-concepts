---
persona: vutr
kind: concept
sources:
- raw/bigquery-internals/bigquery-processing-engine-shuffle.md
- raw/bigquery-internals/everything-you-need-to-know-about.md
- raw/bigquery-internals/i-spent-4-hours-figuring-out-how.md
last_updated: '2026-07-15'
qc: passed
slug: disaggregated-shuffle-service
topics:
- bigquery-internals
---

Dremel's shuffle is directly inspired by MapReduce's shuffle step — after a worker's `map` output is written to temporary storage, data belonging to the same key is redistributed so it lands on one worker for the `reduce` phase — but Google rebuilt where that intermediate data physically lives, and that single change ripples through the rest of Dremel's design. In the traditional MapReduce approach, shuffle data is written directly from the mapper's own temporary storage to the reducer: compute and the shuffle's temporary storage are tightly coupled on the same machine. Google's Dremel paper names this coupling as the actual bottleneck at Google's scale: the quadratic scaling of shuffle operations as the number of producers and consumers grows can't be efficiently mitigated while they're coupled, and the coupling causes resource fragmentation, stranding, and poor isolation. Concretely, mapper/reducer scaling isn't predictable at large data volumes — grouping a dataset with a million distinct keys can produce roughly a million output "buckets," and compute and temporary storage simply can't be sized independently of each other when they share a machine.

Google's fix, in its own words, was to separate shuffle's RAM-and-disk needs into "a distributed transient storage system" — an in-memory shuffle layer that acts like a queue, with multiple workers publishing shuffle output into it and multiple downstream workers consuming from it. Google states three direct wins from this: reduced shuffle latency, shuffles an order of magnitude larger than before, and resource cost cut by more than 20%. Vu supplements the paper (which stops short of the mechanism) with a video source explaining *why*: temporary storage can now scale independently of compute; fault tolerance improves because a failed worker's replacement doesn't lose intermediate data (it's already durably held in the separate shuffle layer, not on the dead worker's local disk); and execution becomes more flexible because the number of workers for a stage can be decided at runtime based on the actual size of the intermediate shuffle output, rather than fixed in advance.

That last point is what makes the disaggregated shuffle layer load-bearing for the rest of Dremel's dynamic execution model (see [[dremel-query-engine]]): because shuffle output is held externally rather than on a worker's own disk, it can double as a **checkpoint of query execution state**. Workers become stateless — all the state that matters survives in the shuffle layer — so the centralized scheduler is free to add or remove workers between stages without losing anything, and the Query Master can check shuffle statistics to decide the next stage's worker count dynamically. The same visibility into shuffle statistics is how Dremel detects and reacts to **data skew**: if one shuffle partition grows disproportionately, the Query Master instructs the producing workers to hash again, splitting the overloaded partition's data into two new partitions consumed by a freshly assigned repartition worker, after which the original overloaded partition is discarded. Vu is careful to flag that "partition" here means how data is routed through the shuffle, distinct from BigQuery's storage-level table partitioning (see [[partitioning-and-clustering-bigquery]]).

Vu's shuffle-specific post also notes, without detailing, that Uber and Facebook/Meta hit similar shuffle-coupling problems running Spark and addressed them the same way — by separating the shuffle layer from the worker — pointing to Uber's and Facebook's own external engineering posts rather than working through their mechanisms himself.

*See also: [[dremel-query-engine]] · [[partitioning-and-clustering-bigquery]]*
