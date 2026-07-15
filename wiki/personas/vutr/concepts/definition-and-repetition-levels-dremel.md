---
persona: vutr
kind: concept
sources:
- raw/bigquery-internals/lesson-learned-after-reading-bigquery.md
- raw/bigquery-internals/everything-you-need-to-know-about.md
last_updated: '2026-07-15'
qc: passed
slug: definition-and-repetition-levels-dremel
topics:
- bigquery-internals
---

Columnar storage stores every value of a single column together, which is a great fit for OLAP scans that only need a handful of columns — but it creates an immediate problem for nested and repeated (array-like) fields: how do you store, say, `Person.Info.Name` as its own independent column while still recording which ancestor records it actually belonged to, given that any of `Person`, `Info`, or `Name` might be absent? Dremel's answer is two per-value integers travelling alongside each column value: the **definition level** and the **repetition level**.

The **definition level** is, in Vu's own simplified restatement of Google's formal definition, "the maximum level at which the path is defined." Walking the three-level path `Person.Info.Name`: if `Name` itself has a value, its definition level is 3; if `Name` is NULL but `Info` is present, the definition level drops to 2 (the deepest level actually defined is `Info`); if both `Name` and `Info` are NULL but `Person` is present, it's 1; and if even `Person` is NULL, it's 0. The **repetition level** solves the parallel problem for repeated (array) fields — for example encoding `[[1,2,3],[4,5,6]]` as an independent column while preserving which values belong to which sub-array: it records at which repeated field along the value's path a repetition actually occurred, with level 0 reserved to mean "this is the start of a new record."

Applied together to Google's own worked example (nested records with a repeated `Forward` field nested inside `Links`), the definition level ranges from 0 (if `Links` itself is NULL) to 2 (if `Forward` is actually defined), while the repetition level ranges from 0 (a new record) to 1 (a repeated value within the same record). Reading four `Forward` values off two records this way: value 20 gets repetition 0 (new record) and definition 2 (defined); values 40 and 60 both get repetition 1 (repeated within that record) and definition 2; and value 80, starting the second record, resets to repetition 0 with definition 2. With this pair of integers riding along every value, Dremel can reconstruct the full hierarchical and array structure of a record while still storing and reading each field as an independent column — in particular, a nested field can be read without ever touching its ancestor fields, which is exactly the columnar win the encoding is built to preserve.

The scheme isn't free: because every child field repeats structural information about its ancestors, the deeper and wider a record's structure gets, the more redundant bookkeeping accumulates, which is why this encoding produces larger files than an ORC- or Arrow-style approach. In exchange, because Dremel never has to traverse the ancestor path just to read a nested value, the redundancy trades directly for lower I/O per read. Vu notes that Apache Parquet — designed by engineers at Twitter, who credit the approach directly to Dremel's own paper — adopted this same definition/repetition-level scheme to handle nested columns (see [[definition-repetition-levels]] for that Parquet-side adoption).

*See also: [[definition-repetition-levels]] · [[capacitor-file-format]] · [[dremel-query-engine]]*
