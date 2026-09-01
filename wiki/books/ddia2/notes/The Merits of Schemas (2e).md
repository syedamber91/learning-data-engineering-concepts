---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 5
chapter_title: Encoding and Evolution
topic: Formats for Encoding Data
type: subtopic
tags: [ddia2, schemas, asn1, code-generation, documentation]
sources:
  - raw/ch05.md
---
# The Merits of Schemas
> Schema-driven binary encodings give you the flexibility of schemaless JSON *plus* guarantees and tooling. The catch is that the data isn't readable until you decode it.

## The Idea
Protocol Buffers and Avro both use a schema to describe a binary encoding format, and **their schema languages are much simpler than XML Schema or JSON Schema**, which support more detailed validation rules — "this string must match this regular expression," "this integer must be between 0 and 100." Being simpler to implement and use, protobuf and Avro have gained support across a fairly wide range of programming languages.

## How It Works
**These ideas are not new.** They have a lot in common with **ASN.1**, a schema definition language **first standardized in 1984**, used to define various network protocols; its binary encoding **DER is still used to encode SSL certificates (X.509)**. ASN.1 supports schema evolution using tag numbers, similar to Protocol Buffers. **However, it is also very complex and badly documented, so ASN.1 is probably not a good choice for new applications.**

Many data systems also implement **proprietary binary encodings**. Most relational databases have a network protocol for sending queries and getting responses; those protocols are generally specific to one database, and the vendor provides a driver — using ODBC or JDBC APIs — that decodes responses into in-memory data structures.

So although textual formats are widespread, schema-based binary encodings are a viable option with a number of nice properties:
- **They can be much more compact** than the "binary JSON" variants, since they can **omit field names** from the encoded data.
- **The schema is a valuable form of documentation**, and because the schema is **required for decoding, you can be sure it is up to date** — whereas manually maintained documentation easily diverges from reality.
- **Keeping a database of schemas lets you check forward and backward compatibility of schema changes before anything is deployed.**
- **For users of statically typed languages, generating code from the schema enables type checking at compile time.**

## Trade-offs & Pitfalls
- The book's summary: **schema evolution allows the same kind of flexibility that schemaless/schema-on-read JSON databases provide, while also giving better guarantees about your data and better tooling.** That is a strong claim — it says you don't have to choose between flexibility and safety.
- Still, **keep the number of concurrent schema formats to a minimum to keep operations simple.**
- The standing cost, noted in the chapter summary: **data must be decoded before it is human-readable**, which is a real operational loss compared to being able to `cat` a JSON file.

## Examples & Systems
ASN.1 and DER for X.509 certificates; ODBC/JDBC drivers as decoders for proprietary database wire protocols.

## Since the 1st Edition
Substantively unchanged from the 1st edition's [[The Merits of Schemas]] — the same ASN.1 history, the same four advantages, the same closing comparison with schema-on-read. The one added note is the advice to minimise the number of concurrent schema formats.

## Related
- up: [[Formats for Encoding Data (2e)]] · chapter: [[Ch 05 - Encoding and Evolution (2e)]]
- [[When to Use Which Model (2e)]] — the schema-on-read comparison this answers
- [[Protocol Buffers (2e)]] and [[Avro (2e)]] — the two formats being defended
- 1st edition: [[The Merits of Schemas]] — the same subtopic
