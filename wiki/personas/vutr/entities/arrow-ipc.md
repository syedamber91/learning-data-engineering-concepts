---
persona: vutr
kind: entity
sources:
- raw/apache-arrow-additional/apache-arrow-for-data-engineers.md
- raw/apache-arrow-additional/i-spent-6-hours-learning-apache-arrow.md
last_updated: '2026-07-15'
qc: passed
slug: arrow-ipc
topics:
- apache-arrow
---

Arrow IPC is the protocol Arrow defines for serializing and transferring data between processes, and its unit of serialized data is the Record Batch itself (see [[arrow-table-and-chunked-arrays]]). The protocol is a one-way stream of binary messages of three kinds. A **Schema message** comes first and defines the structure — a list of fields, each with a name and data type — and carries no data buffers at all. A **RecordBatch message** carries the actual buffers: its header records the length and null count for each field plus the memory offset and size of every buffer in the batch's body, which is exactly the information needed to reconstruct the arrays via pointer arithmetic instead of copying memory. A **DictionaryBatch message** supports dictionary encoding — an efficient way to store categorical data — by shipping a lookup table of unique values once; fields encoded this way then refer to dictionary indices rather than repeating the full values, saving space and processing time. (Neither post explains how the dictionary itself is built or how index-to-value lookups are resolved at read time.)

Arrow packages RecordBatches into two binary formats that trade off differently. The **Streaming format** is for an arbitrary-length sequence of batches: it must be read sequentially from start to end, has no random access, puts the schema first, and includes DictionaryBatch messages inline whenever a field is dictionary-encoded. The **File format** is for a fixed, known number of batches with random access: the file opens and closes with the magic string "ARROW1", and otherwise mirrors the streaming format's contents, but ends with a footer holding a redundant copy of the schema plus the memory offsets and sizes of every data block — that footer is what lets a reader jump straight to any Record Batch without scanning the whole file.

Because the File format is shaped like a real file with a fixed, addressable layout, Arrow IPC files can be memory-mapped — treated as a segment of virtual memory correlated byte-for-byte with the file on disk. That lets a process work with datasets larger than available RAM and lets different languages and processes share the same data without a separate copy step. This is also what makes IPC the shared boundary that [[zero-copy-data-sharing]] leans on whenever two processes on the same machine need to exchange data: one process writes into an Arrow buffer in shared memory, and the other reads directly from that region, no serialization or deserialization in between.

*See also: [[arrow-table-and-chunked-arrays]] · [[arrow-flight]] · [[apache-arrow]] · [[zero-copy-data-sharing]]*
