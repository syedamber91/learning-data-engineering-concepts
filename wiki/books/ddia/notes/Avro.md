---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 4
chapter_title: Encoding and Evolution
topic: Formats for Encoding Data
type: subtopic
tags: [ddia, avro, schema-resolution, writer-reader-schema]
sources:
  - raw/ch04.md
---
# Avro
> Avro drops field tags entirely — the bytes are just values in schema order — and gets its evolvability from a library-level *resolution* step that reconciles the writer's schema with the reader's schema by field name.

## The Idea
Apache Avro began in 2009 as a [[Hadoop]] subproject because Thrift didn't suit Hadoop's needs. It takes the schema idea further than [[Thrift and Protocol Buffers]]: the encoded data contains *no* field identifiers and *no* datatype markers at all. That makes it the most compact format in the chapter (32 bytes for the running example) — but it means the bytes are meaningless without knowing exactly which schema wrote them.

## How It Works
Avro has two schema languages: Avro IDL for humans and a JSON form for machines. Encoding concatenates values in schema-declared order — a string is a length prefix plus UTF-8 bytes, an integer is a varint (like Thrift CompactProtocol) — with nothing marking what each value is. Decoding walks the schema in parallel with the bytes.

The central mechanism is the **writer's schema / reader's schema split**. The encoder uses whatever schema version it was built with (writer's schema); the decoder expects its own version (reader's schema). They need not be identical, only *compatible*: the Avro library resolves differences side by side — matching fields **by name** (so field order doesn't matter), ignoring writer-only fields, and filling reader-expected-but-missing fields from the reader schema's declared defaults.

**Evolution rules:** you may add or remove only fields that have a default value. Adding a defaultless field breaks backward compatibility (new readers can't fill it in for old data); removing one breaks forward compatibility (old readers can't fill it in for new data). Nullability is explicit: `null` is a valid default only inside a union type such as `union { null, long }` — deliberate verbosity that prevents null bugs. There are no `optional`/`required` markers. Renames work via reader-side aliases, and union branches can be added — both backward- but not forward-compatible.

**How does the reader learn the writer's schema?** Context-dependent: a big file embeds the schema once in its header (object container files, the Hadoop case); a database stores a version number per record plus a schema-version registry (LinkedIn's Espresso); a network connection negotiates the schema at setup (Avro RPC). A schema-version database doubles as documentation and a pre-deploy compatibility checker.

## Trade-offs & Pitfalls
No tags means friendliness to **dynamically generated schemas**: dump a relational database by generating an Avro record per table, column names becoming field names — regenerate on any schema change and name-based resolution keeps old readers working. With tag-based formats an administrator would have to curate column→tag mappings and never reuse tags. Code generation is optional; container files are self-describing, so dynamic languages (and tools like Apache Pig) can open them like JSON. The cost: you can never decode Avro bytes without schema access.

## Examples & Systems
Apache Avro, Hadoop object container files, LinkedIn Espresso, Avro RPC, Apache Pig.

## Related
- up: [[Formats for Encoding Data]] · chapter: [[Ch 04 - Encoding and Evolution]]
- [[Thrift and Protocol Buffers]] — the tag-based contrast
- [[Dataflow Through Databases]] — Espresso applies Avro's [[Schema Evolution]] to storage
- [[MapReduce and Distributed Filesystems]] — the Hadoop batch world Avro was built for
