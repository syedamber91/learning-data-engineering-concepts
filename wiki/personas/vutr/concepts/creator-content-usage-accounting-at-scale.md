---
persona: vutr
kind: concept
sources:
- raw/big-tech-case-studies-batch-2-apple-github-pinterest-canva/groupby-32-canva-scaling-to-count.md
last_updated: '2026-07-15'
qc: passed
slug: creator-content-usage-accounting-at-scale
topics:
- big-tech-case-studies-batch-2-apple-github-pinterest-canva
---

Canva runs a creator payment program — three years old by the time of vutr's GroupBy #32 — that pays creators based on how often their content gets used. The curated teaser, quoting Canva engineer Sangzhuoyang Yu, gives the growth shape of the problem directly: usage of creator content has doubled every 18 months since the program launched, and Canva now pays creators based on billions of content usages every month. That usage data spans more than one content type — "templates but also images, videos, and so on" — so the count has to hold across formats, not just one.

The framing vutr's post captures is that this is fundamentally a counting-at-scale problem before it is a payments problem: "building and maintaining a service to track this data for payment is challenging." The teaser also states that Canva went through more than one design to get there — "the various architectures we've experimented with and the lessons we learned along the way" — but names none of them. What's grounded here is the shape of the problem (multi-format usage events, billions per month, usage doubling every 18 months) and the acknowledgment that the current architecture is not the first one Canva tried; the architectures themselves, and what specifically failed about the earlier ones, are outside what vutr's captured post reproduces.

*See also: [[rockstorewidecolumn]] · [[cloudkit]] · [[github-merge-queue]]*
