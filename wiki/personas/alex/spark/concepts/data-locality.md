---
persona: alex
kind: concept
sources:
- vutr/data-locality
last_updated: '2026-07-09'
qc: passed
slug: data-locality
topics:
- spark
learner: alex
source_note: data-locality
mastery: mastered
---

Data sits in partitions across the cluster and tasks need to run near their data because moving code is cheap but moving data is expensive. The scheduler places each task at the closest locality it can get: PROCESS_LOCAL (data in the same executor process, no transfer), then NODE_LOCAL (same machine, different process, no network hop), then NO_PREF (no preference, place anywhere), then RACK_LOCAL (different machine but same rack, faster local network), then ANY (anywhere else, farthest and slowest). Nearer wins because each step out means shipping data over slower links. And if one task lags (a straggler), speculative execution launches a duplicate on another executor and takes whichever finishes first.

```mermaid
graph LR
  A["PROCESS_LOCAL<br/>data in same executor JVM — no transfer"] --> B["NODE_LOCAL<br/>same machine, different process — no network hop"]
  B --> C["NO_PREF<br/>no locality preference — place anywhere"]
  C --> D["RACK_LOCAL<br/>same rack, different machine — faster local network"]
  D --> E["ANY<br/>anywhere else — farthest, slowest transfer"]
```

*Source: [[data-locality]] (vutr)*
