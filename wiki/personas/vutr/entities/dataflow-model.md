---
persona: vutr
kind: entity
sources:
- raw/flink-additional/the-stream-processing-model-behind.md
last_updated: '2026-07-15'
qc: passed
slug: dataflow-model
topics:
- flink
---

The Dataflow model is Google's stream/batch processing model, described in the 2015 paper "The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing" that Vu's post is a reading note on. Vu is careful to separate three things that get conflated: **Dataflow** is the model itself; **Apache Beam** lets users define processing logic according to that model without committing to an engine; **Google Cloud Dataflow** is the managed execution service — one destination engine for a Beam pipeline among others (Spark, Flink).

The paper's authors surveyed the processing landscape of the time and found it wanting on both sides: batch systems (MapReduce, FlumeJava, Spark) couldn't meet latency SLAs because they require a full batch before processing; streaming systems that did offer scalability and fault tolerance (MillWheel, Spark Streaming, Storm) fell short on expressiveness or correctness — many lacked exactly-once semantics, or lacked event-time windowing primitives entirely (Spark Streaming, per the paper, was then limited to tuple- or processing-time windows), and even the systems with good event-time windowing relied on ordering assumptions or offered limited triggering. Their diagnosis of the shared flaw: every one of these models assumed unbounded input would eventually become complete — an assumption today's enormous, disordered data breaks.

From that diagnosis the model makes four contributions: computing event-time-ordered results over unbounded, unordered data with a configurable balance of correctness, latency, and cost; splitting pipeline implementation into four questions — **What** results are computed, **Where** in event time they're computed, **When** they're materialized in processing time, and **How** earlier results relate to later refinements; and separating the logical abstraction of the computation from the physical execution engine, so the same pipeline definition can run anywhere. The paper's own framing, which Vu quotes: there is "nothing magical" here — the model doesn't make an expensive computation cheaper, it gives a general vocabulary for expressing parallel computation independent of any specific engine.

Terminology choice matters to the authors: they deliberately use **unbounded/bounded** rather than **streaming/batch**, because the latter pair usually implies committing to a specific execution engine.

Two core transformations operate on `(key, value)` pairs and both work over bounded or unbounded data: **ParDo**, generic per-element parallel processing via a user-supplied function (a `DoFn`) that can emit zero or more outputs per input and doesn't require its input to be unbounded; and **GroupByKey**, which groups all data sharing a key — and which, because an unbounded source never tells you when it's "done," gets redefined by systems that support it as **GroupByKeyAndWindow** once windowing enters the picture.

The paper's own design principles, as Vu lists them: never rely on any notion of completeness; stay flexible enough for use cases not yet known; make sense in the context of each targeted execution engine, not just one; encourage clarity of implementation; and support robust analysis of data in the context in which it occurred. Internally, Google implemented the model on FlumeJava with MillWheel as the underlying stream engine, with a separate reimplementation for Google Cloud Dataflow "primarily complete" at the time the paper was written — and, notably, a large share of the windowing and triggering code turned out to be shared across the batch and streaming implementations.

*See also: [[windowing-triggers-and-late-events]] · [[dataflow-triggers-and-refinement-modes]] · [[apache-beam]] · [[watermark]]*

## Related in the other wiki
- [[Reasoning About Time]] — DDIA's note on the ambiguity of event-time vs. processing-time windows credits the Dataflow model with formalizing watermarks and corrections, the same never-assume-completeness principle detailed here.
- [[Dataflow]] — DDIA's broader concept ("which process produces data that which process consumes," culminating in Ch.12's "the log is the API") is the general idea; this note is the specific, named Google model — with its own four design questions and unbounded/bounded terminology — that also happens to share the word.
