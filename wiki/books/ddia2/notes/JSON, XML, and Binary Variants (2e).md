---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 5
chapter_title: Encoding and Evolution
topic: Formats for Encoding Data
type: subtopic
tags: [ddia2, json, xml, csv, json-schema, messagepack, base64]
sources:
  - raw/ch05.md
---
# JSON, XML, and Binary Variants
> Widely known, widely supported, and vague about exactly the things that break silently: number precision and binary data.

## The Idea
Moving to standardized encodings readable by many languages, **JSON and XML** are the obvious contenders. **CSV** is another popular language-independent format, but supports only tabular data without nesting. All three are textual and thus somewhat human-readable, though the syntax is a perennial topic of debate.

## How It Works
Beyond superficial syntax, the book lists concrete problems:
- **XML is often criticised for being too verbose and unnecessarily complicated.**
- **Number encoding is ambiguous.** In XML and CSV you cannot distinguish a number from a string of digits except via an external schema. JSON distinguishes strings from numbers but **not integers from floating-point**, and specifies no precision. Integers greater than 2⁵³ cannot be represented exactly in an IEEE 754 double, so they become inaccurate when parsed in a language using floats, such as JavaScript. The real-world example: **X uses a 64-bit number to identify each post, so its API returns post IDs twice — once as a JSON number and once as a decimal string** — to work around incorrect parsing by JavaScript applications.
- **No binary strings.** JSON and XML support Unicode character strings well but not sequences of bytes without a character encoding. People work around this by encoding binary data as text with **Base64**, using the schema to indicate the value should be interpreted that way. It works, but is somewhat hacky and **increases data size by about a third**.
- **Schema languages are heavyweight.** XML Schema and JSON Schema are powerful and thus quite complicated to learn and implement. Since correct interpretation of data — numbers, binary strings — depends on schema information, applications not using them may need to **hardcode the appropriate encoding/decoding logic instead**.
- **CSV has no schema at all**, so the application defines the meaning of each row and column, and an added row or column must be handled manually. CSV is also quite vague — what happens if a value contains a comma or newline? Its escaping rules have been formally specified, but **not all parsers implement them correctly**.

**JSON Schema** has become widely adopted for modelling data exchanged between systems or written to storage. You find it in web services as part of the **OpenAPI** specification, in schema registries such as **Confluent's Schema Registry** and **Red Hat's Apicurio Registry**, and in databases — PostgreSQL's `pg_jsonschema` validator extension and MongoDB's `$jsonSchema` validator syntax. It offers standard primitive types (`string`, `number`, `integer`, `object`, `array`, `boolean`, `null`) plus a separate **validation specification** that overlays constraints on fields — a `port` field with a minimum of 1 and a maximum of 65,535, say.

JSON Schemas can have **open or closed content models**. An open model permits any field not defined in the schema to exist with any datatype; a closed model allows only explicitly defined fields. Open is enabled when `additionalProperties` is `true`, **which is the default** — so JSON Schemas are usually a definition of what *isn't* permitted (invalid values on defined fields) rather than what is. Open models are powerful but can be complex: to define a map from integer IDs to strings, since JSON objects always use string keys, you constrain with `patternProperties` (`"^[0-9]+$"` → `{"type": "string"}`) plus `additionalProperties: false`.

**Binary encodings.** JSON is less verbose than XML but both use a lot of space compared to binary formats, which spawned a profusion of binary encodings for JSON (**MessagePack, CBOR, BSON, BJSON, UBJSON, BISON, Hessian, Smile**) and for XML (**WBXML, Fast Infoset**). These have been adopted in niches, being more compact and sometimes faster to parse, but **none is as widely adopted as the textual versions**. Some extend the datatype set — distinguishing integers from floats, adding binary strings — but otherwise keep the JSON/XML data model unchanged. Crucially, **since they don't prescribe a schema they must include all object field names within the encoded data**.

The book's worked example encodes `{"userName": "Martin", "favoriteNumber": 1337, "interests": ["daydreaming", "hacking"]}` in MessagePack: the first byte `0x83` marks an object (top four bits `0x80`) with three fields (bottom four bits `0x03`); `0xa8` marks a string (`0xa0`) of eight bytes (`0x08`); then eight bytes of `userName` in ASCII, with no end marker or escaping needed since the length was given; then seven bytes for the six-letter `Martin` with prefix `0xa6`. **The result is 66 bytes against 81 for whitespace-stripped textual JSON** — and all binary JSON encodings are similar in this regard. It is not clear whether such a small space reduction, plus perhaps a parsing speedup, is worth losing human-readability.

## Trade-offs & Pitfalls
- **JSON Schema's power is also its liability.** It supports conditional if/else logic, named types, and references to remote schemas — which makes for a very powerful schema language and for **unwieldy definitions**. It can be challenging to resolve remote schemas, reason about conditional rules, or **evolve schemas in a forward- or backward-compatible way**. Similar concerns apply to XML Schema.
- **Despite the flaws, these formats are good enough for many purposes** and will likely remain popular, especially as data interchange formats between organisations. As long as people agree on the format, it often doesn't matter how pretty or efficient it is — **the difficulty of getting different organizations to agree on anything outweighs most other concerns.**

## Examples & Systems
MessagePack, CBOR, BSON and the rest of the binary-JSON family; WBXML and Fast Infoset for XML; OpenAPI, Confluent Schema Registry, Apicurio, `pg_jsonschema`, MongoDB `$jsonSchema` as JSON Schema consumers.

## Since the 1st Edition
The 1st edition's [[JSON, XML, and Binary Variants]] covered the same flaws — verbosity, number ambiguity with the same X/Twitter 2⁵³ example, Base64 for binary, CSV vagueness — and the same binary-variant survey with the same MessagePack byte-by-byte walkthrough. **The substantial addition is JSON Schema**: its adoption across web services, registries, and databases; the validation specification; **open versus closed content models with `additionalProperties` defaulting to open**; the integer-keyed-map example; and the warning that its power makes forward/backward-compatible evolution hard. The 1st edition treated schema languages as a brief aside here.

## Related
- up: [[Formats for Encoding Data (2e)]] · chapter: [[Ch 05 - Encoding and Evolution (2e)]]
- [[Protocol Buffers (2e)]] — the same record in 33 bytes instead of 66
- [[The Merits of Schemas (2e)]] — why the schema-driven formats win on evolution
- 1st edition: [[JSON, XML, and Binary Variants]] — the same subtopic, without JSON Schema
