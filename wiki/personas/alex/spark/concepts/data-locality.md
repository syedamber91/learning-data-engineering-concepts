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
mastery: familiar
---

Alex: So Spark would rather run the work where the data already is than move the data, because moving data is expensive. It has a ranked wishlist of how close the data is, from same-process (PROCESS_LOCAL) all the way down to anywhere (ANY), and it waits a moment for a good spot before dropping to a worse one. And separately, if a task is dragging, Spark runs a second copy elsewhere and takes the faster one so a single slow machine doesn't hold everything up. That preferred spot comes from the RDD's fifth property.

```mermaid
graph TD
    A[PROCESS_LOCAL: same JVM] --> B[NODE_LOCAL: same node, different process]
    B --> C[NO_PREF: no locality preference]
    C --> D[RACK_LOCAL: same rack]
    D --> E[ANY: anywhere]
```

*Source: [[data-locality]] (vutr)*
