---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 4
chapter_title: Encoding and Evolution
topic: Formats for Encoding Data
type: subtopic
tags: [ddia, json, xml, binary-encoding, data-interchange]
sources:
  - raw/ch04.md
---
# JSON, XML, and Binary Variants
> Textual formats win at cross-organization interchange despite fuzzy datatypes; their binary cousins (MessagePack etc.) save little space because they must still carry field names.

## The Idea
Once data leaves a single language runtime, you need a format many languages can read. JSON and XML are the default answers (CSV a weaker third): universally supported, human-readable, and — crucially — a *neutral ground* that separate organizations can agree on. The chapter's point is that for interchange between parties, agreeing on *any* format matters more than that format's elegance or efficiency.

## How It Works
All three are textual: values are written out as characters, with field names repeated in every record. Binary variants (MessagePack, BSON, BJSON, UBJSON, BISON, Smile for JSON; WBXML, Fast Infoset for XML) re-encode the same data model in bytes. In MessagePack, for instance, a lead byte packs the value's type into its top bits and a small count/length into its bottom bits — `0x83` means "map of 3 entries", `0xa8` means "8-byte string" — so strings need no terminators or escaping. But because there is no schema, every field name (`userName`, `favoriteNumber`, `interests`) must still be embedded in the bytes. The book's example record shrinks only from 81 bytes (compact JSON) to 66 bytes (MessagePack).

## Trade-offs & Pitfalls
- **Number ambiguity.** XML and CSV can't tell a number from a digit string without an external schema. JSON separates strings from numbers but not integers from floats, and specifies no precision — integers above 2^53 get silently mangled by IEEE 754 doubles (why Twitter's API ships each 64-bit tweet ID twice: as a number and as a string).
- **No binary strings.** Raw byte sequences must be smuggled in as Base64, a hack that inflates size by a third and depends on a schema to signal the interpretation.
- **Schemas optional and heavy.** XML Schema and JSON Schema exist and are powerful, but complex; many JSON tools skip them, forcing apps to hardcode interpretation logic.
- **CSV is underspecified.** No schema at all, murky escaping of commas/newlines, and parsers that ignore the RFC. Column changes must be handled by hand.
- **Binary variants rarely pay off.** Modest size/parse gains for total loss of human readability; none has displaced textual JSON/XML.

## Examples & Systems
JSON (browser-native via JavaScript), XML, CSV, MessagePack, BSON, Smile, WBXML, Fast Infoset; Twitter's dual tweet-ID workaround.

## Related
- up: [[Formats for Encoding Data]] · chapter: [[Ch 04 - Encoding and Evolution]]
- [[Thrift and Protocol Buffers]] — schemas let field names be dropped entirely
- [[The Merits of Schemas]] — why schema-driven beats schema-optional
- [[Dataflow Through Services - REST and RPC]] — where JSON dominates in practice
