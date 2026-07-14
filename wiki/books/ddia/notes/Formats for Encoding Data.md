---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 4
chapter_title: Encoding and Evolution
type: topic
tags: [ddia, encoding, serialization, schema-evolution]
sources:
  - raw/ch04.md
---
# Formats for Encoding Data
Programs keep data in two shapes: CPU-friendly in-memory structures (objects, trees, pointers) and self-contained byte sequences for files and networks. Translating between them is *encoding* (serialization/marshalling) and *decoding* — the book prefers "encoding" to avoid clashing with transaction [[Serializability]]. This topic walks up a ladder of formats, judged mainly on one axis: how well each supports [[Schema Evolution]] — keeping *backward compatibility* (new code reads old data) and *forward compatibility* (old code reads new data) while rolling upgrades leave old and new code running side by side.

## Subtopics
- [[Language-Specific Formats]] — built-in serializers (pickle, Java serialization): convenient, but language-locked, insecure, and evolution-blind.
- [[JSON, XML, and Binary Variants]] — cross-language textual formats and why their binary re-encodings barely help.
- [[Thrift and Protocol Buffers]] — schema + numeric field tags = compact bytes and crisp evolution rules.
- [[Avro]] — tag-free encoding whose writer/reader schema resolution enables dynamic schemas.
- [[The Merits of Schemas]] — why schema-driven binary formats beat both schemaless JSON and heavyweight XML schemas.

## Key Takeaways
- Backward compatibility is easy (you know the old format); forward compatibility is the hard one — old code must deliberately *ignore* what it doesn't understand.
- Field tags (Thrift/Protobuf) and name-based resolution with defaults (Avro) are two different answers to the same question: how do bytes stay meaningful across schema versions?
- Golden rules: never change or reuse a tag number; every added field needs to be optional or carry a default.
- The example record's sizes tell the story: 81 bytes as JSON, 66 as MessagePack, 59/34 as Thrift, 33 as Protobuf, 32 as Avro — schemas buy compactness by omitting names.
- Schemas double as guaranteed-current documentation and enable pre-deploy compatibility checking.
- For cross-organization interchange, agreement trumps elegance — JSON/XML/CSV will endure there.

## Related
- [[Ch 04 - Encoding and Evolution]] — parent chapter MOC
- [[Modes of Dataflow]] — where these encodings actually travel
- [[Evolvability - Making Change Easy]] — the Chapter 1 goal encoding choices serve
- [[Relational Model Versus Document Model]] — the schema-on-read debate schemas resolve
