---
persona: vutr
kind: concept
sources:
- raw/change-data-capture-cdc-and-data-sourcing-additional/data-engineering-system-design-11.md
last_updated: '2026-07-15'
qc: passed
slug: source-delete-handling
topics:
- change-data-capture-cdc-and-data-sourcing
---

Updates are the easy case — a new row shows up and, with an `updated_timestamp`, you can just keep the latest version. Deletes are a different story, and Vu splits the source's delete behavior into two kinds. Soft deletion marks a removed record with a flag rather than removing it, so the pipeline can rely on that flag to skip the record downstream — deletes become visible, structured events like any other change. Hard deletion just makes the row disappear: the pipeline keeps running fine, keeps accumulating records, and slowly drifts away from the source, with nobody noticing until someone eventually does the hard work of manually reconciling against the source, often months later.

For hard deletes, Vu lists three (non-exhaustive) responses: CDC captures delete events as they happen and is the most complete and reliable option; a mechanism like SCD Type 2 can infer a deletion by noticing a record's ID is simply absent from today's snapshot compared to a prior one; or, if you have the leverage, negotiate soft deletes with the source team directly, turning a silent disappearance into an explicit flag. This is exactly why [[query-based-cdc]]'s inability to see DELETEs is such a specific, named weakness in the CDC comparison — it's the query-based mechanism running headlong into the hard-deletion failure mode described here.

*See also: [[query-based-cdc]] · [[log-based-cdc]] · [[exactly-once-and-missing-data-detection]]*
