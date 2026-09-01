---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 2
chapter_title: Defining Nonfunctional Requirements
type: topic
tags: [ddia2, maintainability, legacy, technical-debt]
sources:
  - raw/ch02.md
---
# Maintainability
Software does not wear out or suffer material fatigue, so it does not break the way mechanical objects do. But an application's requirements frequently evolve, the environment it runs in changes — dependencies, the underlying platform — and it may have bugs needing fixes. It is widely recognised that **the majority of the cost of software is not in its initial development but in its ongoing maintenance**: fixing bugs, keeping systems operational, investigating failures, adapting to new platforms, modifying for new use cases, repaying technical debt, and adding features.

Maintenance can be complex, especially for legacy systems. A system that has run successfully for a long time may use outdated technologies few engineers understand today — mainframes and COBOL are the book's examples — and institutional knowledge of how and why it was designed a certain way may have left with the people who had it. Fixing other people's mistakes may be necessary. Because computer systems are often intertwined with the human organisations they support, **maintaining them is as much a people problem as a technical one**.

Every system we create today will one day become a legacy system, if it is valuable enough to survive. To minimise the pain for whoever maintains it next, design with maintenance in mind. The book cannot predict which decisions will cause future headaches, but it commits to three widely applicable principles.

## Subtopics
- [[Operability - Making Life Easy for Operations (2e)]] — make it easy for the organisation to keep the system running smoothly.
- [[Simplicity - Managing Complexity (2e)]] — make it easy for new engineers to understand the system, using well-understood consistent patterns and avoiding unnecessary complexity.
- [[Evolvability - Making Change Easy (2e)]] — make it easy for engineers to change the system later, adapting and extending it for unanticipated use cases.

## Key Takeaways
- Maintenance dominates lifetime cost, so maintainability is not a nice-to-have appended after performance and reliability — it is where most of the money goes.
- Legacy is a destination, not a category of other people's systems.
- The three principles are not independent: evolvability depends on simplicity and good abstractions, and operability depends on the system exposing what operators need.
- There are no easy answers to achieving any of them. The one approach the chapter endorses is **building applications out of well-understood building blocks that provide useful abstractions** — which is precisely what the rest of the book supplies.

## Since the 1st Edition
Structurally unchanged: the same three principles under the same three names, with the same definitions. This is the most stable part of the chapter between editions. The individual subtopics have been updated (see each), but the framing survived a decade intact.

## Related
- chapter: [[Ch 02 - Defining Nonfunctional Requirements (2e)]]
- [[Operations in the Cloud Era (2e)]] — who is doing the operating, and how that changed
- [[Ch 05 - Encoding and Evolution (2e)]] — evolvability made concrete at the data-format level
- 1st edition: [[Maintainability]] — the same three-way split
