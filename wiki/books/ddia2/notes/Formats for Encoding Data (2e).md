---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 5
chapter_title: Encoding and Evolution
type: topic
tags: [ddia2, encoding, serialization, zero-copy]
sources:
  - raw/ch05.md
---
# Formats for Encoding Data
Programs usually work with data in at least two representations. **In memory**, data is kept in objects, structs, lists, arrays, hash tables, and trees — structures optimised for efficient access and manipulation by the CPU, typically using pointers. **When writing to a file or sending over a network**, it must be encoded as a self-contained sequence of bytes; since a pointer means nothing to another process, this representation often looks quite different from the in-memory one.

Translating from in-memory representation to byte sequence is **encoding** (also known as **serialization** or **marshaling**); the reverse is **decoding** (**parsing**, **deserialization**, **unmarshaling**).

> **Terminology clash.** *Serialization* is also used in the context of transactions with a completely different meaning. To avoid overloading the word, the book sticks with **encoding**, even though serialization is perhaps more common.

## Subtopics
- [[Language-Specific Formats (2e)]] — the built-in libraries, and their four deep problems.
- [[JSON, XML, and Binary Variants (2e)]] — the standardized textual formats, JSON Schema, and the binary-JSON family.
- [[Protocol Buffers (2e)]] — schema-required binary encoding built on field tags.
- [[Avro (2e)]] — schema-required binary encoding built on writer/reader schema resolution.
- [[The Merits of Schemas (2e)]] — the case for schema-driven binary encodings.

## Key Takeaways
- **Encoding is not always necessary.** A database can operate directly on compressed data loaded from disk, as vectorized query execution does. There are also **zero-copy data formats** — **Cap'n Proto** and **FlatBuffers** — designed to be used both at runtime and on disk or on the network with no explicit conversion step.
- Most systems, however, do need to convert between in-memory objects and flat byte sequences, and because this is such a common problem there is a **myriad of libraries and formats** to choose from.
- The chapter's structure follows a progression of increasing discipline: language-native (convenient, dangerous) → textual standards (interoperable, vague) → schema-driven binary (compact, evolvable, not human-readable).

## Since the 1st Edition
The framing, terminology, and terminology-clash note are all carried over from the 1st edition's [[Formats for Encoding Data]]. **New:** the acknowledgement that encoding is sometimes avoidable, naming **Cap'n Proto and FlatBuffers** as zero-copy formats and linking to the compressed-data query execution from Chapter 4.

## Related
- chapter: [[Ch 05 - Encoding and Evolution (2e)]]
- [[Modes of Dataflow (2e)]] — where these encodings get used
- [[Query Execution - Compilation and Vectorization (2e)]] — the case where no decoding happens at all
- 1st edition: [[Formats for Encoding Data]] — the same topic
