---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 4
chapter_title: Encoding and Evolution
topic: Formats for Encoding Data
type: subtopic
tags: [ddia, schemas, binary-encoding, documentation]
sources:
  - raw/ch04.md
---
# The Merits of Schemas
> Schema-driven binary formats give you schemaless-style flexibility *plus* compactness, always-accurate documentation, pre-deployment compatibility checks, and compile-time type safety.

## The Idea
After surveying Thrift, Protocol Buffers, and Avro, the chapter steps back to argue that schemas are not bureaucracy — they are leverage. These schema languages are deliberately much simpler than XML Schema or JSON Schema (no regex constraints or value-range validation), which is exactly why they were easy to implement across many programming languages and why they caught on.

## How It Works
The idea has deep roots. ASN.1, standardized back in 1984, already used tag numbers for [[Schema Evolution]] much like [[Thrift and Protocol Buffers]] do; its DER encoding still underlies X.509 SSL certificates today — though ASN.1 itself is too complex and poorly documented to recommend for new work. Databases quietly do the same thing: most relational systems speak a proprietary binary protocol over the network, and the vendor's ODBC/JDBC driver is the decoder that turns responses into in-memory structures.

## Trade-offs & Pitfalls
The four concrete advantages of schema-based binary encoding:
1. **Compactness** — field names can be omitted from the data (unlike every "binary JSON" variant), because the schema supplies them.
2. **Living documentation** — since decoding *requires* the schema, it cannot drift out of date the way hand-maintained docs do.
3. **Safe evolution** — keeping a database of schema versions lets you machine-check forward and backward compatibility *before* deploying anything.
4. **Code generation** — statically typed languages get compile-time type checking and IDE support for free.

The main cost is opacity: data must be decoded before a human can read it, unlike JSON or XML. And the simplicity of these schema languages means they validate structure, not business rules.

The closing synthesis: [[Schema Evolution]] gives the same flexibility that schema-on-read ("schemaless") document databases advertise — heterogeneous record versions living side by side — while offering far stronger guarantees about the data and better tooling around it. This directly answers the schema-flexibility argument from the document-model debate in [[Relational Model Versus Document Model]].

## Examples & Systems
ASN.1 / DER / X.509 certificates; proprietary relational database wire protocols with ODBC/JDBC drivers; Protocol Buffers, Thrift, and Avro as the modern trio; XML Schema and JSON Schema as the heavyweight comparators.

## Related
- up: [[Formats for Encoding Data]] · chapter: [[Ch 04 - Encoding and Evolution]]
- [[Avro]] — schema registry and resolution in practice
- [[JSON, XML, and Binary Variants]] — the schema-optional world being improved on
- [[Relational Model Versus Document Model]] — the schema-on-read flexibility claim this rebuts
