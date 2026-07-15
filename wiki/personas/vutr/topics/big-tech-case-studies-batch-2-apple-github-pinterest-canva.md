---
persona: vutr
kind: topic
sources:
- raw/big-tech-case-studies-batch-2-apple-github-pinterest-canva
last_updated: '2026-07-15'
qc: passed
topic: big-tech-case-studies-batch-2-apple-github-pinterest-canva
---

Related: [[cloudkit]] · [[github-merge-queue]] · [[rockstorewidecolumn]] · [[creator-content-usage-accounting-at-scale]]

## Comparisons
**Four case studies, four link-teasers — and one is clearly richer than the other three.** Unlike vutr's Dimension-style deep dives (see [[kafka]], [[spark]]), these four entries come from his weekly GroupBy digest, where a case study gets a title, an author credit, and a single quoted paragraph from the original article rather than vutr's own analysis. Of the four, [[rockstorewidecolumn]] is the only one where the teaser names more than one architectural fact at once — the KVStore/Rockstorewidecolumn split, the RocksDB foundation, and (via the image caption) versioned values — giving it just enough internal structure to compare a client-facing abstraction against the storage engine underneath it. [[cloudkit]], [[github-merge-queue]], and [[creator-content-usage-accounting-at-scale]] each give a single claim instead: a dual-database pairing, a throughput number, and a growth curve, respectively.

**Storage problems vs. process problems.** [[cloudkit]] and [[rockstorewidecolumn]] are both storage-engine stories — CloudKit's Cassandra-plus-FoundationDB pairing and Pinterest's RocksDB-backed wide-column store are both about how to persist data at scale. [[github-merge-queue]] and [[creator-content-usage-accounting-at-scale]] are process/workflow stories instead — merge queue is about ordering and landing code changes, and Canva's usage-tracking challenge is about correctly counting and attributing billions of monetizable events rather than about which database holds them. None of the four teasers cross into the other pair's territory: vutr's curated text never says what Canva's usage-counting service is built on, nor what data structure sits behind GitHub's merge queue.

**Growth framing is the one thing two of these share explicitly.** Both [[cloudkit]] (via its "billions of databases" framing) and [[creator-content-usage-accounting-at-scale]] (via "doubled every 18 months" and "billions of content usages each month") are introduced through a scale number rather than a mechanism. [[github-merge-queue]]'s scale claim — "hundreds of changes every day" — is more modest in absolute terms but makes the same rhetorical move: a throughput figure standing in for an explanation of how the throughput is achieved.

## Open questions
- How exactly does CloudKit divide work between Cassandra and FoundationDB — which reads/writes go to which store, and why two databases instead of one? vutr's post names both systems but the "how each is used" explanation is in the linked Engineer's Codex article, not captured here.
- What does "billions of databases" mean structurally for CloudKit — is each iCloud user, app, or record its own database? The title asserts the scale but the captured teaser doesn't define the unit.
- What is the actual mechanism behind GitHub's merge queue — how does it batch, order, or speculatively test queued pull requests before merging? vutr's teaser states the outcome (hundreds of changes/day, transformed deploys) but not the mechanism.
- How does Rockstorewidecolumn's RocksDB foundation get adapted into a wide-column, schemaless model — what does the on-disk key/column/version encoding actually look like? The teaser names the pieces (KVStore, Rockstorewidecolumn, versioned values) but not how they fit together internally.
- What made KVStore, Pinterest's pre-existing client abstraction, insufficient on its own — why did Pinterest need a new storage service underneath it? vutr's captured post doesn't say what came before Rockstorewidecolumn or what problem forced the change.
- What architecture(s) did Canva actually try for creator-usage accounting, and why did earlier ones not hold up as usage doubled every 18 months? The teaser promises "the various architectures we've experimented with" but names none of them.
- Is Canva's usage-counting challenge closer to an exactly-once event-counting problem or a reconciliation/audit problem? vutr's captured text doesn't say whether usage events can be double-counted, lost, or need after-the-fact correction.

## Synthesis
These four case studies come from vutr's GroupBy curation practice rather than his own Dimension deep-dives, so what's grounded here is intentionally shallow: two storage-layer stories ([[cloudkit]]'s dual-database backend, [[rockstorewidecolumn]]'s RocksDB-based wide-column store) and two process/workflow stories ([[github-merge-queue]], [[creator-content-usage-accounting-at-scale]]), each introduced by a single quoted teaser and a scale claim rather than a mechanism. The pattern repeats across all four: vutr's own newsletter voice supplies curation, framing, and a scale number, while the actual "how" is deferred to the linked source — which is exactly why every one of this batch's open questions traces back to a specific missing mechanism rather than a missing topic.

## Related topics
- [[big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter]] — same genre of curated big-tech engineering-blog case studies (Netflix, Uber, LinkedIn, Meta, DoorDash, Spotify, Twitter), drawn from richer Dimension-style deep dives rather than this batch's thinner GroupBy teasers.
- [[lsm-tree-storage-engines]] — [[rockstorewidecolumn]] is built directly on RocksDB, the LSM-tree engine this topic covers in depth (memtable, SSTable flush, compaction, bloom filter).
- [[SSTables and LSM-Trees]] — DDIA's note names both RocksDB and Cassandra as concrete LSM-tree implementations, the same two systems this batch's Rockstorewidecolumn and CloudKit case studies build on.
