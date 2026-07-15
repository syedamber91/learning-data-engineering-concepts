---
persona: vutr
kind: concept
sources:
- raw/big-tech-case-studies-batch-1-spotify-twitter-facebook-discord-notion/how-did-facebook-design-their-real.md
last_updated: '2026-07-15'
qc: passed
slug: backfill-processing-strategies
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

The notes list three reasons a real-time system eventually needs to reprocess old data: testing an application against historical events, generating historical values for a newly added metric, and reproducing a bug — and Facebook's real-time paper lays out three architectural answers to that need, each with a different cost.

Stream only keeps everything in the streaming layer: the data transport must retain events long enough to let the stream application replay its own input for reprocessing, so the retention window of the message bus effectively becomes the backfill window. Two separate systems runs one pipeline for batch and a wholly different one for streaming — the notes flag this as the option that's hardest to keep consistent, since any drift between the batch and stream codebases becomes drift between the historical and real-time views of the same data. Stream processing systems that can also run in a batch environment — the notes name Spark Streaming and Flink as examples — write one piece of processing logic that executes in both modes, collapsing the consistency problem at the cost of needing an engine capable of both.

Facebook's actual implementation blends elements of this last option without fully committing to a single unified engine: it reads historical data out of Hive using the standard MapReduce framework, and different stream processing systems adapt to that batch environment in different ways. Puma applications can run as Hive UDFs and UDAFs (user-defined functions and aggregation functions), so the same Puma application code runs unchanged whether it's processing a live Scribe stream or a batch of historical Hive rows. Stylus takes a different tack: building a Stylus application produces two separate binaries, one for streaming and one for batch. The batch binary for a stateless processor runs inside Hive as a custom mapper; the batch binary for a general stateful processor runs as a custom reducer, keyed on an aggregation key plus the event timestamp — reproducing, in MapReduce's grouping model, the same state semantics the stream binary would apply live.

*See also: [[persistent-message-bus-data-transfer]] · [[stream-state-saving-mechanisms]] · [[state-and-output-processing-semantics]]*
