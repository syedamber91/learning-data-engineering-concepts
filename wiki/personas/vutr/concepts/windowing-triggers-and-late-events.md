---
persona: vutr
kind: concept
sources:
- raw/flink-additional/apache-flink-overview.md
- raw/flink-additional/batch-and-stream-processing.md
last_updated: '2026-07-15'
qc: passed
slug: windowing-triggers-and-late-events
topics:
- flink
---

Aggregation and joins are, at bottom, a search for records sharing a key. Batch processing gets its search scope for free — the system already knows the full boundary of the data it's processing — but an unbounded stream has no natural boundary at all. **Windowing** manufactures one, usually by carving the infinite stream into finite chunks using a time notion (e.g., "everything in the last hour" is one window).

Vu names the same three window types consistently across his writing: **Fixed/Tumbling** windows are non-overlapping and of fixed size (e.g., hourly); **Sliding** windows are also fixed size but defined with a slide period, so they overlap (e.g., a 30-minute window starting every 5 minutes); **Session** windows are grouped per key by an inactivity gap rather than a clock. His worked session example, with a 10-minute inactivity gap: a homepage click at 10:00 opens a new session window, provisionally ending at 10:10; a product-page click at 10:05 falls inside the gap, so the window expands and its end resets to 10:15; a cart-add at 10:08 does the same, resetting the end to 10:18; then 17 minutes pass with no activity (10:08 → 10:25), which exceeds the 10-minute gap, so the window that started at 10:00 closes; the checkout click at 10:25 arrives after the gap and opens a brand-new session window ending at 10:35.

Windowing only decides *which* events belong together — a **trigger** decides *when* the computation for a window actually runs and its result is emitted. Vu's own analogy: windowing is collecting salad ingredients in a bowl, while triggering is deciding when to stop mixing and serve. He names four trigger types: an **event-time trigger**, which fires on watermark progress (a 10-minute fixed window covering 1:05–1:15 fires once the watermark passes 1:15 — not because 1:15 itself arrived, but because the watermark is exactly the system's answer to "has all data with event time before 1:15 arrived?"); a **processing-time trigger**, firing at a specific point in processing time; a **data-arriving-characteristics trigger**, firing on counts, bytes, punctuation, or pattern matches in the data itself; and a **composite trigger** that combines the others.

Data that logically belongs to a window (its event time falls inside the window) but physically arrives after the watermark has already passed that window's end is, by default, dropped as a **late event**. Most streaming frameworks instead let you configure a grace period — "wait another 2 minutes" — during which such late data is still folded into the window's result. The late boundary sits relative to the watermark, not the window itself: for a 1:05–1:15 window with 1 minute of allowed lateness, the late boundary is 1:16, and data with event time in 1:05–1:15 is accepted if it arrives after the watermark passes 1:15 but before the watermark passes 1:16.

*See also: [[watermark]] · [[apache-flink]] · [[dataflow-model]] · [[dataflow-triggers-and-refinement-modes]] · [[flink-state-management-and-backends]]*

## Related in the other wiki
- [[Reasoning About Time]] — DDIA's own four window shapes (tumbling, hopping, sliding, session) and its straggler-handling discussion cover almost the same ground as this note's tumbling/sliding/session windows and late-event grace period, from the book's more general vantage point.
