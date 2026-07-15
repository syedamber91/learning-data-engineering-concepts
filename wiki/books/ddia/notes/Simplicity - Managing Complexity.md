---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 1
chapter_title: Reliable, Scalable, and Maintainable Applications
topic: Maintainability
type: subtopic
tags: [ddia, complexity, abstraction, accidental-complexity]
sources:
  - raw/ch01.md
---
# Simplicity: Managing Complexity
> Complexity that isn't inherent in the problem — accidental complexity — is the enemy of maintainability, and abstraction is the best tool for removing it.

## The Idea
Small projects can stay delightfully clear, but growing ones slide toward the "big ball of mud" (Foote & Yoder's term): complexity that slows every person who touches the system and compounds maintenance cost. Complexity also breeds bugs — when developers can't reason about the system, hidden assumptions, unintended consequences, and unexpected interactions slip past review. Reducing complexity is therefore not aesthetics; it directly improves maintainability, and simplicity deserves to be an explicit engineering goal.

## How It Works
Recognize complexity by its symptoms: a state space that has exploded, tightly coupled modules, tangled dependencies, inconsistent naming and terminology, performance hacks, special cases patched in to work around problems elsewhere. The critical conceptual move comes from Moseley and Marks ("Out of the Tar Pit"): complexity is **accidental** when it arises from the implementation rather than from the problem the software solves as users see it. Simplifying does *not* mean cutting features — it means stripping the accidental layer while keeping the essential one.

The prime tool is **abstraction**: hide implementation detail behind a clean, understandable façade. A good abstraction pays twice — reuse across many applications is cheaper than reimplementation, and quality improvements to the shared component lift every application built on it. Canonical examples: high-level programming languages abstract away machine code, CPU registers, and syscalls (you still *use* machine code — you just never think about it); SQL abstracts on-disk and in-memory data structures, concurrent access by other clients, and post-crash inconsistencies (its query model is explored in [[Query Languages for Data]]).

## Trade-offs & Pitfalls
- **Finding good abstractions is genuinely hard.** In distributed systems especially, many excellent algorithms exist, but packaging them into abstractions that actually contain system complexity remains an open craft — a tension the whole book keeps returning to.
- Abstractions can leak or mislead; a façade that hides the wrong details creates new accidental complexity instead of removing it.
- Simplicity of *implementation* must not be confused with simplicity of the user interface — the section is explicit that these are different targets.

## Examples & Systems
- The "big ball of mud" as the named anti-pattern.
- High-level languages and SQL as archetypal successful abstractions.
- The book's own agenda: hunting for reusable, well-defined components to extract from large systems.

## Related
- up: [[Maintainability]] · chapter: [[Ch 01 - Reliable, Scalable, and Maintainable Applications]]
- [[Evolvability - Making Change Easy]] — simple systems are the easiest to change
- [[Operability - Making Life Easy for Operations]] — comprehensibility aids operations too
- [[Query Languages for Data]] — Ch 2 develops SQL, the star abstraction example
- [[Thinking About Data Systems]] — composite systems raise the abstraction question
- [[data-engineering-career-roadmap-and-learning-philosophy]] — vutr's own repeated anecdote (building a full CDC-plus-Dataflow real-time pipeline for a daily-refresh requirement, retold nearly verbatim across two articles) is a concrete, career-stakes case of choosing accidental complexity this note's abstraction-as-remedy argument warns against; see that topic's [[simplicity-over-complexity-in-pipeline-design]] concept.
