---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 5
chapter_title: Encoding and Evolution
topic: Formats for Encoding Data
type: subtopic
tags: [ddia2, serialization, pickle, java-serialization, security]
sources:
  - raw/ch05.md
---
# Language-Specific Formats
> Java's `Serializable`, Python's `pickle`, Ruby's `Marshal`. Two lines of code and four deep problems, one of which is remote code execution.

## The Idea
Many programming languages have built-in support for encoding in-memory objects into byte sequences: **Java's `java.io.Serializable`, Python's `pickle`, Ruby's `Marshal`**, plus third-party libraries such as **Kryo** for Java. They are convenient, letting in-memory objects be saved and restored with minimal additional code.

## How It Works
The four problems the book lists:
- **Language lock-in.** The encoding is often tied to a particular programming language, and reading the data in another language is difficult. Storing or transmitting data this way commits you to your current language for potentially a long time and precludes integrating with other organisations' systems, which may use different languages.
- **Security.** To restore data in the same object types, decoding must be able to **instantiate arbitrary classes** — frequently a source of security problems. If an attacker can get your application to decode an arbitrary byte sequence, they can instantiate arbitrary classes, which often allows terrible things such as **remotely executing arbitrary code**.
- **Versioning as an afterthought.** These libraries are intended for quick and easy encoding, so they often neglect the inconvenient problems of forward and backward compatibility.
- **Efficiency as an afterthought.** Both CPU time to encode/decode and the size of the encoded structure. Java's built-in serialization is **notorious for its bad performance and bloated encoding**.

## Trade-offs & Pitfalls
The book's verdict is unusually blunt: **it is generally a bad idea to use your language's built-in encoding for anything other than very transient purposes.** The convenience is real but is paid for in every dimension that matters once data leaves the process.

## Examples & Systems
`java.io.Serializable`, Kryo (Java); `pickle` (Python); `Marshal` (Ruby).

## Since the 1st Edition
Essentially unchanged from the 1st edition's [[Language-Specific Formats]] — the same four problems in the same order, the same examples, and the same conclusion. One of the most stable sections in the book.

## Related
- up: [[Formats for Encoding Data (2e)]] · chapter: [[Ch 05 - Encoding and Evolution (2e)]]
- [[JSON, XML, and Binary Variants (2e)]] — the language-independent alternatives
- 1st edition: [[Language-Specific Formats]] — the same subtopic
