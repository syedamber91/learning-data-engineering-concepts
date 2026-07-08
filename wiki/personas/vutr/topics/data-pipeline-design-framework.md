---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: data-pipeline-design-framework
---

Related: [[sink]] · [[source]] · [[middle-steps]] · [[dead-letter-queue]] · [[checkpointing]] · [[semantic-schema-change]] · [[idempotency]] · [[missing-data-vs-duplicates]] · [[clarifying-questions-before-tools]]

## Comparisons
Design flows sink-first, source-last in intent but the [[source]] carries the most risk because it's the part you don't control, while the [[sink]] is where you define purpose, output shape, and atomicity. In the [[middle-steps]], bad-data routing splits by processing mode: a [[dead-letter-queue]] for streams versus a dedicated dataset for batch. Failure handling and correctness are two separate concerns — [[checkpointing]] recovers from crashes, whereas [[idempotency]] makes reruns safe. Detection difficulty also ranks unevenly: [[missing-data-vs-duplicates]] shows absence is silent, and worse still is a [[semantic-schema-change]], where nothing structural breaks and only a weird dashboard trend reveals it.

## Open questions
- How do you operationally cross-check the [[source]] to surface [[missing-data-vs-duplicates]] before it reaches the sink?
- What monitoring catches a [[semantic-schema-change]] earlier than a human noticing a weird dashboard trend?
- Where exactly do you draw the line on "don't over-engineer the freshness" for a given [[sink]] staleness tolerance?
- How do you negotiate a data-quality contract and schema-change notification with a [[source]] team you don't control?

## Synthesis
My framework runs from the [[sink]] backward — business purpose first — then interrogates the [[source]] as the one part I don't control, and finally hardens the [[middle-steps]] against failure and reruns. Correctness rests on two pillars: [[idempotency]] so reruns produce the same result, and honest routing of bad data via a [[dead-letter-queue]]. But the quiet killers are detection problems — [[missing-data-vs-duplicates]] and especially a [[semantic-schema-change]] — which is why [[clarifying-questions-before-tools]] matters more than reaching for Spark or Kafka.
