---
title: "Batch vs Streaming"
area: "Data Pipelines"
topic: "Processing Paradigms"
tags: [batch, streaming, latency, throughput]
---

# Batch vs Streaming

*Part of [[processing-paradigms-moc|Processing Paradigms]] · [[data-pipelines-moc|Data Pipelines]]*

**In one line:** Batch processing handles a big pile of data on a schedule; streaming processes each piece of data the moment it arrives.

**Picture this:** Batch is doing all your laundry once a week in full loads — efficient, but your clean shirt isn't ready until laundry day. Streaming is washing each item by hand as you take it off — always up to date, but more constant effort.

**How it actually works:** A *batch* job wakes up (say, every night), reads a bounded chunk of data, processes it all at once, and stops. It favours *throughput* — moving huge volumes cheaply. A *streaming* job runs forever, reacting to events one by one (a click, a payment) within seconds. It favours *latency* — fresh results right now.

**In the real world:** A bank runs *batch* overnight to produce daily statements. Uber uses *streaming* to update your driver's location on the map every second — waiting until midnight would be useless. Many companies use both: streaming for live dashboards, batch for heavy nightly reports.

**Why you'd use it (and when not to):** Choose batch when data can wait and volume is huge (monthly billing). Choose streaming when freshness matters (fraud alerts). Streaming costs more to build and run, so don't reach for it when "tomorrow morning" is good enough.

**Connects to:** [[idempotency]] · [[dags-schedulers]]
