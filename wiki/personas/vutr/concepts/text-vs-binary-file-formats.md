---
persona: vutr
kind: concept
sources:
- raw/parquet-file-format/file-formats-for-data-engineers.md
last_updated: '2026-07-15'
qc: passed
slug: text-vs-binary-file-formats
topics:
- parquet
---

Every file on disk is a sequence of 0s and 1s; what distinguishes a "text-based" format from a "binary" one is how those bits get interpreted. Text-based formats rely on a character-encoding dictionary (ASCII, Unicode) mapping binary numbers to displayable characters — every letter, digit, and symbol gets a unique numerical code. That makes them human-readable and editable in any text editor, but it's inefficient for numbers specifically: storing `256` as text means storing the binary codes for three separate characters ('2', '5', '6'), which takes more space and forces an extra parse-then-convert step. A binary format stores the number's direct mathematical representation instead — `256` as a 16-bit integer is stored directly as `00000001 00000000` — more compact and faster for a CPU to consume, at the cost of no longer being human-legible (strings inside a binary file are typically still UTF-8 encoded, but other types are raw).

CSV and JSON are the text-based end of this spectrum, and both share the same core weakness for analytics: they're row-oriented, so reading one column still means reading and parsing every field of every row. CSV has no built-in schema or type enforcement (the reading system carries that burden), and its lack of a real standard creates brittleness — delimiter conflicts, inconsistent quoting, and encoding drift are all named failure modes. It is splittable when uncompressed (each line is an independent record), but a non-splittable compression codec like Gzip turns the whole file into one continuous stream a processing engine can't divide. JSON adds native types and nested/repeated structure that CSV lacks, at the cost of verbosity (every record repeats its key names) and parser overhead (nested objects need recursive descent, with cost scaling by nesting depth); a standard JSON array is also effectively one big document that can't be split mid-structure, unless it's written as NDJSON — one self-contained object per line, the JSON analogue of a CSV row.

[[apache-avro|Avro]] is the pivot to binary. It decouples its JSON-defined schema from its binary data, and further decouples the writer's schema from the reader's schema so the two only need to be compatible, not identical — genuine schema evolution that CSV and JSON can't offer natively. Its 16-byte sync markers make it splittable the way NDJSON is, without needing a line-oriented convention. But Avro is still row-oriented, so it inherits CSV/JSON's core analytical weakness even though it solves their schema and compactness problems.

Parquet is the direct answer to that one remaining weakness — it exists specifically because analytics workloads only need a subset of columns most of the time, and query performance depends mainly on how much data gets skipped, which a row-oriented format (however compact or schema-safe) structurally cannot do. The progression CSV → JSON → Avro → Parquet reads as a move from human-legibility toward machine efficiency, and, within the machine-efficient formats, from row-locality (fast per-record write and read) toward column-locality (fast analytical scan) — a trade [[pax-hybrid-layout|Parquet's hybrid layout]] tries to have both sides of, at the cost of write throughput.

*See also: [[apache-avro]] · [[parquet-origin]] · [[pax-hybrid-layout]]*
