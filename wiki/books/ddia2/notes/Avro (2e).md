---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 5
chapter_title: Encoding and Evolution
topic: Formats for Encoding Data
type: subtopic
tags: [ddia2, avro, writers-schema, readers-schema, schema-registry, hadoop]
sources:
  - raw/ch05.md
---
# Avro
> Nothing in the bytes says what any field is. Decoding works only because the reader is given the writer's schema — and that constraint is what makes dynamically generated schemas easy.

## The Idea
**Apache Avro** is another binary encoding format, started in **2009 as a Hadoop subproject** because Protocol Buffers was not a good fit for Hadoop's use cases. It also uses a schema, with **two schema languages**: **Avro IDL** for human editing and a **JSON-based** one that is more machine-readable. Like protobuf's, these specify only fields and types, with no complex validation rules.

```
record Person {
  string userName;
  union { null, long } favoriteNumber = null;
  array<string> interests;
}
```

## How It Works
**The schema has no tag numbers.** Encoding the example record gives just **32 bytes — the most compact of all the encodings** in the chapter. Examining the byte sequence, **nothing identifies fields or their datatypes**: the encoding is simply values concatenated together. A string is a length prefix followed by UTF-8 bytes, but nothing in the data says it is a string — it could be an integer or anything else. Integers use a variable-length encoding.

To parse, you **go through the fields in the order they appear in the schema** and use the schema to determine each field's datatype. This means **binary data can be decoded correctly only if the reading code uses the exact same schema as the writing code**; any mismatch means incorrectly decoded data. So how does Avro support evolution?

**The writer's schema and the reader's schema.** When encoding, the application uses whatever schema version it knows about — compiled into the application, say — and that is the **writer's schema**. When decoding, the application uses **two** schemas: the writer's schema, identical to the one used for encoding, and the **reader's schema**, which may be different and defines the fields and types the application code expects. If they are the same, decoding is easy; if different, **Avro resolves the differences by comparing the two and translating the data from the writer's schema into the reader's schema**.

The specification defines resolution exactly. Fields **in a different order are no problem**, because resolution matches by **field name**. A field in the writer's schema but not the reader's is **ignored**. A field the reader expects but the writer's schema lacks is **filled in with a default value declared in the reader's schema**.

(This contrasts with Protocol Buffers, where encoding and decoding can use different schema versions directly; in Avro, decoding uses two schemas — the writer's must be identical to the encoding one, but the reader's can be older or newer.)

**Schema evolution rules.** In Avro, **forward compatibility** means the writer can use a newer schema than the reader; **backward compatibility** means the writer can use an older schema than the reader. To maintain compatibility you may **add or remove only a field that has a default value**. Adding a field with a default means a new-schema reader reading old-schema data fills in the default. Adding a field with **no** default breaks backward compatibility (new readers can't read old writers' data); removing a field with no default breaks forward compatibility (old readers can't read new writers' data).

**`null` is not a universal default in Avro.** To allow a field to be null you must use a **union type** — `union { null, long, string } field;` means the field can be a number, a string, or null — and **null can be a default only if it is the first branch**. This is more verbose than everything-nullable-by-default, but **helps prevent bugs by being explicit about what can and cannot be null**.

Changing a datatype is possible if Avro can convert the type. **Changing a field name is possible but tricky**: the reader's schema can contain **aliases** for field names, matching old writer field names against them — which makes renaming **backward compatible but not forward compatible**. Similarly, **adding a branch to a union type is backward compatible but not forward compatible**.

**But what is the writer's schema?** You can't include the whole schema with every record — it would likely dwarf the encoded data, negating the space savings. The answer depends on context:
- **Large file with many records** (millions, all one schema): include the schema **once at the beginning of the file**. Avro specifies a file format for this — **object container files**.
- **Database with individually written records**, written at different times with different schemas: include a **version number at the start of every record** and keep a list of schema versions in the database. A reader extracts the version, fetches the corresponding writer's schema, and decodes with it. **Confluent's schema registry for Kafka** and **LinkedIn's Espresso** work this way.
- **Records over a network connection**: two processes can **negotiate the schema version on connection setup** and use it for the connection's lifetime. The Avro RPC protocol works like this.

A database of schema versions is useful anyway — it acts as documentation and gives you a chance to **check schema compatibility**. The version number can be a simple incrementing integer or a hash of the schema.

## Trade-offs & Pitfalls
**Dynamically generated schemas** are Avro's distinctive advantage, and the absence of tag numbers is why. Say you want to dump a relational database's contents to a file in a binary format. With Avro you can **generate an Avro schema from the relational schema fairly easily** — a record schema per table, each column becoming a field, column name mapping to field name — and dump everything to an object container file. If the database schema changes (a column added, another removed), you just **generate a new Avro schema and export in it**; the export process needn't pay any attention to the change, since it does the conversion every run. Readers see that the record's fields changed, but **because fields are identified by name, the updated writer's schema still matches the old reader's schema**.

With Protocol Buffers, **field tags would likely have to be assigned by hand**, and every database schema change would need an administrator to update the column-name-to-tag mapping. It might be automatable, but the generator would have to be very careful never to reassign a previously used tag. **Dynamically generated schemas simply weren't a design goal of Protocol Buffers, whereas they were for Avro.**

## Examples & Systems
Avro object container files; Confluent's Schema Registry for Kafka; LinkedIn's Espresso; the Avro RPC protocol.

## Since the 1st Edition
Very close to the 1st edition's [[Avro]] — the same schema languages, 32-byte figure, writer's/reader's schema resolution, evolution rules, union-type nullability, three answers to "what is the writer's schema," and the dynamically-generated-schema argument. Details refreshed rather than restructured.

## Related
- up: [[Formats for Encoding Data (2e)]] · chapter: [[Ch 05 - Encoding and Evolution (2e)]]
- [[Protocol Buffers (2e)]] — the tag-number approach this deliberately avoids
- [[The Merits of Schemas (2e)]] — what both formats buy you
- [[Event-Driven Architectures (2e)]] — schema registries alongside message brokers
- 1st edition: [[Avro]] — the same subtopic
