---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 2
chapter_title: Data Models and Query Languages
topic: Query Languages for Data
type: subtopic
tags: [ddia, declarative, css, query-languages]
sources:
  - raw/ch02.md
---
# Declarative Queries on the Web
> CSS versus DOM-walking JavaScript makes the case for declarative languages in a domain everyone knows — the browser.

## The Idea
The declarative-beats-imperative argument isn't database-specific. Styling a web page provides a vivid parallel: the same "highlight the selected navigation item" task can be expressed as a declarative pattern (CSS/XSL) or as imperative DOM-manipulation code (JavaScript), and the comparison strongly favors the declarative form for the same reasons SQL beat imperative query APIs.

## How It Works
Picture a nested navigation list for an ocean-life site where the currently viewed section's `<li>` carries a marker class. To give that section's title a highlighted background:

- **CSS:** a selector such as `li.current > p { background: gold; }` states *which* elements get the style — every `<p>` directly inside a marked `<li>` — and nothing about how the browser should find them.
- **XSL:** an equivalent XPath-based template (matching something like `li[@class='current']/p`) does the same declaratively for XML documents.
- **Imperative JavaScript:** loop over every `<li>` element, test its class name, loop over its children, test each child's node type and tag, and manually set a style attribute on matches.

The imperative version is longer, harder to read, and — crucially — broken in two deeper ways. First, it doesn't *undo* itself: when the marker class moves to a different item, the manually-set background stays until a full reload, whereas the browser automatically re-evaluates CSS rules and removes styles the moment they stop matching. Second, it locks in implementation choices: to exploit a newer, faster API you must rewrite the code, while browser vendors can silently speed up CSS matching without breaking any stylesheet.

## Trade-offs & Pitfalls
The lesson transfers directly to databases: declarative queries state the *pattern* of desired results, freeing the engine to reorder execution, pick indexes, reclaim disk space by moving records, and parallelize — none of which is safe under imperative code that might depend on ordering or specific APIs. Historical contrast: IMS and CODASYL were queried imperatively, typically COBOL iterating one record at a time. Imperative styles remain reasonable for genuinely procedural, one-off logic — the browser example shows *awkwardness*, not impossibility.

## Examples & Systems
CSS selectors, XSL/XPath templates, the JavaScript core DOM API; by analogy, SQL versus the imperative query interfaces of IMS and CODASYL.

## Related
- up: [[Query Languages for Data]] · chapter: [[Ch 02 - Data Models and Query Languages]]
- [[MapReduce Querying]] — a middle ground between declarative and imperative
- [[The Cypher Query Language]] — declarative style applied to graphs
- [[Are Document Databases Repeating History]] — the imperative IMS/CODASYL heritage
