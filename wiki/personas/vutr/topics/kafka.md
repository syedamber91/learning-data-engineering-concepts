---
persona: vutr
kind: topic
sources:
- persona-snapshot
- substack/vutr/kafka-tiered-storage
last_updated: '2026-07-09'
qc: passed
topic: kafka
---

Related: [[tiered-storage]]

## Comparisons
Local broker disk (hot) vs object storage (cold) — see [[tiered-storage]].

## Open questions
- What is the read-latency penalty for a fetch that hits a tiered segment?

## Synthesis
Tiered storage extends Kafka's write-optimized design: keep [[tiered-storage]] cold segments in object storage so brokers hold only hot data.
