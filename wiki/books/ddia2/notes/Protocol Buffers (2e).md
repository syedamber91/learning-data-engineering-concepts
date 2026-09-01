---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 5
chapter_title: Encoding and Evolution
topic: Formats for Encoding Data
type: subtopic
tags: [ddia2, protobuf, thrift, field-tags, schema-evolution, idl]
sources:
  - raw/ch05.md
---
# Protocol Buffers
> Field *tags*, not field names, go into the bytes. Everything protobuf can and cannot do about schema evolution follows from that single decision.

## The Idea
**Protocol Buffers (protobuf)** is a binary encoding library developed at Google, similar to **Apache Thrift** (originally from Facebook) — most of what this section says applies to Thrift too. It **requires a schema** for any encoded data, described in the Protocol Buffers **interface definition language (IDL)**:

```protobuf
syntax = "proto3";
message Person {
  string user_name      = 1;
  int64  favorite_number = 2;
  repeated string interests = 3;
}
```

A code generation tool takes the schema and produces classes implementing it in various languages; your application calls the generated code to encode or decode records. **The schema language is very simple compared to JSON Schema**: it defines each record's fields and their types but supports no other restrictions on possible values.

## How It Works
Encoding the example record takes **33 bytes** (against 66 in MessagePack and 81 in textual JSON). Each field has a type annotation and, where required, a length indication; strings are UTF-8 as before. **What's absent is field names** — the encoded data contains **field tags**, the numbers 1, 2, and 3 from the schema definition. Field tags are aliases: a compact way of saying which field you mean without spelling out the name.

Protobuf saves further space by **packing the field type and tag number into a single byte** and by using **variable-length integers**: 1337 encodes in two bytes, with the top bit of each byte indicating whether more bytes follow (the least significant seven bits go in the first byte, simplifying reconstruction as bytes are read). So numbers from −64 to 63 take one byte, −8,192 to 8,191 take two, and bigger numbers take more.

There is **no explicit list or array datatype**. The `repeated` modifier indicates a field holds a list, and in the binary encoding list elements are simply **repeated occurrences of the same field tag** within the record.

**Field tags and schema evolution.** An encoded record is just the concatenation of its encoded fields, each identified by tag number and annotated with a datatype; an unset field is simply omitted. From that everything follows:
- **You can change a field's name** freely, since encoded data never refers to names. **You cannot change a field's tag**, since that would invalidate all existing encoded data.
- **Adding a field** is fine provided it gets a new tag number. Old code reading data from new code hits an unrecognised tag and can simply **ignore that field** — and the datatype annotation tells the parser how many bytes to skip **while preserving the unknown field**, avoiding the silent data loss described at the start of the chapter. That is forward compatibility.
- **Backward compatibility** holds as long as each field has a unique tag number, since tags keep their meaning. Reading old data missing a newly added field fills in a **default value** — the empty string for a string, 0 for a number.
- **Removing a field** mirrors adding one, with the two compatibility concerns reversed. **You can never reuse a tag number**, because data written somewhere may still include the old tag and must be ignored by new code. Tag numbers used in the past can be **reserved in the schema definition** so they aren't forgotten.

## Trade-offs & Pitfalls
- **Changing a field's datatype** is possible for some types — check the documentation — but risks **truncation**. Changing a 32-bit integer to a 64-bit one lets new code read old data easily (the parser fills missing bits with 0s), but **old code reading new data still uses a 32-bit variable**, so a decoded 64-bit value that doesn't fit gets truncated.
- Tag numbers are the format's strength and its constraint: they buy compactness and safe evolution, and they must be assigned and reserved by hand — which is precisely the weakness [[Avro (2e)]] attacks.

## Examples & Systems
Protocol Buffers and Apache Thrift; protobuf IDL as the schema language also used by gRPC service definitions.

## Since the 1st Edition
The 1st edition's [[Thrift and Protocol Buffers]] covered both in parallel, including Thrift's BinaryProtocol versus CompactProtocol byte layouts. The 2nd edition **retitles the subtopic to Protocol Buffers and demotes Thrift to a sentence**, reflecting protobuf's dominance, and drops the Thrift protocol comparison. The evolution rules, variable-length integer encoding, `repeated` handling, and the 33-byte figure carry over.

## Related
- up: [[Formats for Encoding Data (2e)]] · chapter: [[Ch 05 - Encoding and Evolution (2e)]]
- [[Avro (2e)]] — the same job without tag numbers
- [[Dataflow Through Services - REST and RPC (2e)]] — protobuf as a service IDL for gRPC
- 1st edition: [[Thrift and Protocol Buffers]] — the same subtopic, covering both
