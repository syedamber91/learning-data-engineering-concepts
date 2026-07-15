---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 1
chapter_title: Reliable, Scalable, and Maintainable Applications
topic: Maintainability
type: subtopic
tags: [ddia, evolvability, agility, changing-requirements]
sources:
  - raw/ch01.md
---
# Evolvability: Making Change Easy
> Requirements never stop changing, so the ability to reshape a data system — agility at the system level, not just the code level — is a first-class design goal.

## The Idea
It is close to impossible that a system's requirements stay fixed forever. They churn constantly: new facts are learned, unanticipated use cases appear, business priorities shift, users demand features, platforms are replaced, laws and regulations change, and growth itself forces architectural rework. A system that is hard to change becomes a liability no matter how well it performs today. Kleppmann names the property of being easy to adapt **evolvability**, deliberately choosing a distinct word for agility at the level of a whole data system.

## How It Works
At the organizational level, Agile working patterns provide the frame for adapting to change, and the Agile community's technical toolkit — test-driven development (TDD) and refactoring — supports building software in fast-changing environments. But those techniques are usually discussed at a small, local scale: a few source files inside one application. The book's concern is bigger: how do you gain the same agility across a *data system* composed of several applications or services with different characteristics?

The section's provocation makes the gap concrete: how would you "refactor" Twitter's home-timeline architecture from the read-time-merge design to the write-time fan-out design (the migration described in [[Describing Load]])? That is not a rename-and-extract-method operation — it's a live rearchitecting of data flows under production load, and it's the kind of change evolvable systems must permit.

Evolvability is tightly coupled to the previous principle: the ease of modifying a data system tracks its simplicity and the quality of its abstractions. Simple, well-understood systems bend; complex ones break. This coupling is why [[Simplicity - Managing Complexity]] and evolvability are presented as a pair.

## Trade-offs & Pitfalls
- Local agility (TDD, refactoring within a codebase) does not automatically confer system-level agility — the harder problem sits between services, in data models and contracts. Chapter 4's treatment of [[Schema Evolution]] ([[Formats for Encoding Data]]) is the book's first deep dive into making change safe at that boundary.
- Optimizing purely for today's requirements bakes in assumptions that tomorrow invalidates — the same trap as scaling architectures built on wrong load assumptions.
- Alternative names — extensibility, modifiability, plasticity — describe the same property; the book standardizes on evolvability.

## Examples & Systems
- Twitter's approach-1 → approach-2 timeline migration as a system-scale refactoring.
- TDD and refactoring as the Agile community's local-scale tools.

## Related
- up: [[Maintainability]] · chapter: [[Ch 01 - Reliable, Scalable, and Maintainable Applications]]
- [[Simplicity - Managing Complexity]] — simplicity is evolvability's precondition
- [[Describing Load]] — the Twitter migration referenced here
- [[Formats for Encoding Data]] — Ch 4: schema evolution makes data change safe
