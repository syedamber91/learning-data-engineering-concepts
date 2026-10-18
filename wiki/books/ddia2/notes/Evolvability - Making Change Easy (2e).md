---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 2
chapter_title: Defining Nonfunctional Requirements
topic: Maintainability
type: subtopic
tags: [ddia2, evolvability, agility, irreversibility, refactoring]
sources:
  - raw/ch02.md
---
# Evolvability: Making Change Easy
> Agility, but for a system of several applications and services rather than for a single codebase — plus one addition the 1st edition didn't make: minimise irreversibility.

## The Idea
It is extremely unlikely that a system's requirements will remain unchanged. They are far more likely to be in constant flux: you learn new facts, unanticipated use cases emerge, business priorities change, users request features, new platforms replace old ones, legal or regulatory requirements change, and growth forces architectural change.

## How It Works
- Organisationally, **Agile** working patterns provide a framework for adapting to change, and the Agile community has developed technical tools and processes that help in a frequently changing environment — **test-driven development (TDD)** and **refactoring** among them.
- This book looks for ways of increasing agility at the level of **a system consisting of several applications or services with different characteristics** — a level above where TDD and refactoring operate. Because this system-level agility is such an important idea, the book gives it its own word: **evolvability**.
- The ease of modifying a data system and adapting it to changing requirements is closely linked to its **simplicity and its abstractions**. Loosely coupled, simple systems are usually easier to modify than tightly coupled, complex ones.

## Trade-offs & Pitfalls
- **Irreversibility is the major factor that makes change difficult in large systems.** The book's example: migrating from one database to another. If you cannot switch back to the old system when problems appear with the new one, the stakes are far higher than if you can easily go back. Irreversible actions therefore need to be taken very carefully, and **minimising irreversibility improves flexibility**.
- This reframes a lot of migration practice: the value of dual-writing, shadow reads, and feature flags is not that they are careful, but that they keep the action reversible.

## Examples & Systems
Database migration as the canonical irreversible-change hazard; TDD and refactoring as the code-level agility tools this operates above.

## Since the 1st Edition
The core — evolvability as system-level agility, its dependence on simplicity and abstraction — comes straight from the 1st edition's [[Evolvability - Making Change Easy]]. **Irreversibility is the new material**, and it is a genuinely useful addition: it gives evolvability a concrete, checkable test ("can we undo this?") where the 1st edition offered mainly a disposition.

## Related
- up: [[Maintainability (2e)]] · chapter: [[Ch 02 - Defining Nonfunctional Requirements (2e)]]
- [[Simplicity - Managing Complexity (2e)]] — the precondition for evolvability
- [[Ch 05 - Encoding and Evolution (2e)]] — evolvability at the level of stored and transmitted data
- 1st edition: [[Evolvability - Making Change Easy]] — the same subtopic, without irreversibility
