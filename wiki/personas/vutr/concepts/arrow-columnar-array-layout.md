---
persona: vutr
kind: concept
sources:
- raw/apache-arrow-additional/apache-arrow-for-data-engineers.md
- raw/apache-arrow-additional/i-spent-6-hours-learning-apache-arrow.md
last_updated: '2026-07-15'
qc: passed
slug: arrow-columnar-array-layout
topics:
- apache-arrow
---

Arrow represents a single column of values as an **array**: a logical sequence of values, all sharing the same type, with a defined length — and, like everything in Arrow, immutable. A **chunked array** is simply a list of arrays strung together (see [[arrow-table-and-chunked-arrays]]). A **slot** is one logical value within an array. Underneath all of this sits the **buffer**: a sequential virtual address space of fixed length where any byte is reachable via a pointer offset — the physical container the array's data actually lives in.

The second post adds a layer of vocabulary underneath "data type" itself: a **physical layout** describes an array's underlying memory structure without regard to what the values mean, while the **data type** is the application-level value a physical layout is put to use representing — a Decimal128 value, for instance, is stored as 16 bytes in a fixed-size binary physical layout, while a timestamp might sit in a 64-bit fixed-size layout. Data types split further into **primitive types**, which have no child types (fixed bit-width values, variable-size binary, null), and **nested types**, whose structure depends on one or more child types (Map, Struct, and similar composite shapes).

Every array carries the same core metadata regardless of type: its length (a 64-bit signed integer), its null count (also 64-bit), its data type, an optional dictionary for dictionary-encoded arrays, and a sequence of buffers. Almost every array type carries a **validity bitmap** buffer encoding which slots are null; some types add an **offset buffer** to locate where each slot's data starts; and every type has a **value buffer** holding the actual data. More complex types add further buffers still — a Size Buffer for ListView layouts, a Types Buffer for Union layouts — which both posts name but don't work through mechanically.

Two worked examples make the buffer layout concrete. A **fixed-size primitive array** is the simplest case: every value occupies the same slot width, so an integer column like `[1, 2, Null, 3, 4]` just lays its values end to end in the value buffer, with the validity bitmap marking the null. A **variable-size binary array** needs the offset buffer to do real work. Given the column `["vu", null, null, "trinh"]`, the offset buffer is `[0, 2, 2, 2, 7]` — one more entry than the array's length. To read slot *i*, take `offset[i]` as the start position in the data buffer and compute the value's length as `offset[i+1] - offset[i]`. Working through it: slot 0 starts at offset 0 with length `2 - 0 = 2`, giving `"vu"`; slot 1 starts at offset 2 with length `2 - 2 = 0`, a null; slot 2 starts at offset 2 with length `2 - 2 = 0`, also null; slot 3 starts at offset 2 with length `7 - 2 = 5`, giving `"trinh"`. The not-null values are packed contiguously in the data buffer, and the offset buffer is what lets a reader locate each one without scanning. Offsets must increase monotonically even across null slots — every value stays well-defined and addressable through its offset — and a null slot can still have a positive slot length with undefined content sitting in that space; by convention the first offset is 0 and the last equals the length of the values array.

This buffer-level design is what the higher performance argument for Arrow ultimately rests on — see [[simd-memory-alignment]] for how contiguous, aligned buffers translate into CPU cache efficiency and SIMD-friendly processing.

*See also: [[arrow-table-and-chunked-arrays]] · [[simd-memory-alignment]] · [[apache-arrow]]*
