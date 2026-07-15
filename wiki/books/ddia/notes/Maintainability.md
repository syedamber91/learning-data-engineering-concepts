---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 1
chapter_title: Reliable, Scalable, and Maintainable Applications
type: topic
tags: [ddia, maintainability, legacy-systems, design-principles]
sources:
  - raw/ch01.md
---
# Maintainability
> Most of software's lifetime cost is maintenance, not initial development — so design for the humans who will operate, understand, and change the system for years.

The bulk of a system's cost arrives after launch: fixing bugs, keeping it operational, investigating failures, porting to new platforms, adapting to new use cases, paying down technical debt, adding features. Yet engineers widely dislike maintaining "legacy" systems — other people's mistakes, obsolete platforms, software bent into shapes it was never meant for — and every legacy system is unpleasant in its own particular way, defying general advice. Kleppmann's response is preventive: design software now so it doesn't *become* painful legacy later. Three principles guide that: **operability** (easy for operations teams to keep it running), **simplicity** (easy for new engineers to understand — which is about internal complexity, not a simple UI), and **evolvability** (easy to change for unanticipated future needs — also called extensibility, modifiability, or plasticity). As with [[Reliability]] and [[Scalability]], none of these has a silver-bullet solution; they are mindsets applied throughout design.

## Subtopics
- [[Operability - Making Life Easy for Operations]] — what good ops teams do, and how systems can make routine work easy.
- [[Simplicity - Managing Complexity]] — accidental vs. essential complexity, and abstraction as the chief weapon against the big ball of mud.
- [[Evolvability - Making Change Easy]] — agility at the data-system level, since requirements never stop changing.

## Key Takeaways
- Maintenance dominates total software cost; optimizing only for initial delivery is optimizing the minority.
- "Legacy" is not an age, it's a design outcome — avoidable with deliberate choices today.
- Simplicity here means less internal complexity for engineers, explicitly not a simpler user interface.
- The three principles compound: simple systems are easier to operate and easier to evolve.

## Related
- chapter: [[Ch 01 - Reliable, Scalable, and Maintainable Applications]]
- [[Reliability]] — good operations practices directly prevent failures
- [[Scalability]] — distribution decisions trade against simplicity
- [[Thinking About Data Systems]] — maintainability as one of the three framing concerns
- [[data-engineering-career-roadmap-and-learning-philosophy]] — vutr's own definition of software engineering as "building systems that keep working... even when the guy who created them has left" is a data-engineering-specific restatement of this note's maintainability framing; see that topic's [[nine-software-engineering-skills-for-des]] entity for the nine skills he derives from it.
