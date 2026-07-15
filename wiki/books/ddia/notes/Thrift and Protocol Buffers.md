---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 4
chapter_title: Encoding and Evolution
topic: Formats for Encoding Data
type: subtopic
tags: [ddia, protobuf, thrift, field-tags, schema-evolution]
sources:
  - raw/ch04.md
---
# Thrift and Protocol Buffers
> Numeric field tags replace field names in the byte stream, making the encoding compact and making [[Schema Evolution]] a matter of simple rules: never change a tag, never reuse one, and keep new fields optional.

## The Idea
Thrift (Facebook) and Protocol Buffers (Google), both open-sourced 2007–08, share one principle: require a schema, then use it to strip redundancy from the encoding. Instead of writing `userName` into every record, the schema assigns each field a small integer *tag* (1, 2, 3…), and only the tag goes on the wire. A code-generation tool turns the schema (written in an IDL) into classes in your language of choice, which the application calls to encode/decode.

## How It Works
An encoded record is just its fields concatenated. Each field carries its tag number, a datatype annotation, and (where needed) a length. Unset fields are simply omitted. The book's 81-byte JSON example becomes:
- **Thrift BinaryProtocol**: 59 bytes — full type byte, 2-byte tag, lengths.
- **Thrift CompactProtocol**: 34 bytes — type and tag squeezed into one byte, and variable-length integers (each byte's top bit says "more bytes follow", so −64..63 fits in one byte, 1337 in two).
- **Protocol Buffers**: 33 bytes — same varint idea with slightly different bit packing.

`required` vs `optional` changes nothing in the bytes; it only enables a runtime presence check useful for catching bugs.

**Evolution rules (the heart of it):**
- *Rename freely* — names never appear in the data. *Never change a tag* — that corrupts the meaning of all existing data.
- *Adding a field*: give it a fresh tag. Old code hits an unknown tag and skips it (the type annotation says how many bytes to jump) → **forward compatibility**. New code still understands old tags → **backward compatibility** — but only if the new field is optional or defaulted, since old writers never wrote it and a `required` check would fail.
- *Removing a field*: the mirror image — only optional fields may go, and the tag number is retired forever, because old data containing it may still exist.
- *Datatype changes*: sometimes possible, but risky — widen i32 to i64 and old code reading new data truncates values that no longer fit in 32 bits.

## Trade-offs & Pitfalls
Protobuf has no list type; a `repeated` marker just repeats the tag, which neatly allows upgrading an `optional` field to `repeated` (old code sees the last element; new code sees a 0/1-element list). Thrift's dedicated `list` type can't evolve that way but supports nested lists. Hand-assigned tags make these formats awkward for dynamically generated schemas — [[Avro]]'s differentiator.

## Examples & Systems
Apache Thrift (also BinaryProtocol/CompactProtocol/DenseProtocol variants), Protocol Buffers, gRPC (protobuf-based RPC), Finagle (Thrift-based).

## Related
- up: [[Formats for Encoding Data]] · chapter: [[Ch 04 - Encoding and Evolution]]
- [[Avro]] — tag-free alternative resolving schemas by field name
- [[The Merits of Schemas]] — the broader case for schema-driven binary formats
- [[Dataflow Through Services - REST and RPC]] — gRPC carries these bytes between services
