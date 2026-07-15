---
persona: vutr
kind: entity
sources:
- raw/parquet-file-format/i-spent-8-understanding-how-parquet.md
- raw/parquet-file-format/the-overview-of-parquet-file-format.md
last_updated: '2026-07-15'
qc: passed
slug: definition-repetition-levels
topics:
- parquet
---

Parquet encodes nested and repeated (semi-structured) data using a technique called record shredding, borrowed directly from Google's Dremel paper (the query engine behind BigQuery). Two integer values accompany every leaf-level value: a definition level and a repetition level.

The **definition level** answers "how many of the optional/repeated fields along this value's path are actually present in this record?" — concretely, the maximum level at which the path is defined. Worked example for a field `Person.Info.Name` (three levels: Person, Info, Name): if `Name` has a value, its definition level is 3; if `Name` is null but `Info` is present, the definition level is 2 (the path is only defined as far as `Info`); if both `Info` and `Name` are null but `Person` is present, it's 1; if `Person` itself is null, it's 0.

The **repetition level** answers "at which repeated field in this value's path did the value repeat?", with level 0 marking the start of a new record. Worked example from a Google-paper-style schema where `Forward` is a repeated field nested inside `Links`: definition level for `Forward` ranges 0-2 (0 if `Links` is null, 1 if `Forward` is null but `Links` isn't, 2 if `Forward` is defined), and repetition level ranges 0-1 (0 for a new record, 1 if the value is a repeat within the same record). Walking the paper's four sample values (20, 40, 60, 80): value 20 gets repetition 0 / definition 2 (new record, `Forward` defined); values 40 and 60 get repetition 1 / definition 2 (repeats within the same record); value 80 gets repetition 0 / definition 2 (start of a new record).

Once every value has been shredded down to a (value, definition level, repetition level) triple, the two integer level-streams are themselves encoded using [[rle-bit-packing-hybrid]] — the same scheme used for dictionary indices. This is what lets a strictly flat, columnar physical layout still faithfully reconstruct arbitrarily nested and repeated logical structures on read.

*See also: [[rle-bit-packing-hybrid]] · [[parquet-physical-and-logical-types]] · [[parquet-write-read-process]]*
