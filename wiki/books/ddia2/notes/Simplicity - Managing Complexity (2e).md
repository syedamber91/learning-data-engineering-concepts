---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 2
chapter_title: Defining Nonfunctional Requirements
topic: Maintainability
type: subtopic
tags: [ddia2, simplicity, complexity, abstraction, big-ball-of-mud, ddd]
sources:
  - raw/ch02.md
---
# Simplicity: Managing Complexity
> A project mired in complexity is a **big ball of mud**. The best tool against it is abstraction — but "simple" has no objective definition, which is why this is hard.

## The Idea
Small software projects can have delightfully simple, expressive code; as projects grow they often become very complex and hard to understand. That complexity slows down everyone who works on the system, further increasing maintenance cost. When complexity makes maintenance hard, budgets and schedules are often overrun, and there is a greater risk of introducing bugs when making a change — because when a system is harder to reason about, hidden assumptions, unintended consequences, and unexpected interactions are more easily overlooked. Conversely, reducing complexity greatly improves maintainability, so **simplicity should be a key goal**.

## How It Works
Solving a problem in the simplest way possible is easier said than done, because **whether something is simple is often subjective — there is no objective standard of simplicity**. The book's illustration: one system may hide a complex implementation behind a simple interface, while another has a simple implementation that exposes more internal detail to its users. Which one is simpler?

One attempt at reasoning about complexity splits it into **essential** and **accidental**: essential complexity is inherent in the problem domain, accidental complexity arises only from limitations of our tooling. The book flags this distinction as **also flawed**, because the boundary between essential and accidental shifts as tooling evolves.

**Abstraction** is the best tool we have. A good abstraction hides a great deal of implementation detail behind a clean, simple-to-understand façade, and a good one can be used across a wide range of applications. That reuse is not only more efficient than reimplementing similar things repeatedly — it leads to **higher-quality software**, since quality improvements in the abstracted component benefit every application using it. Examples: high-level programming languages abstract machine code, CPU registers, and system calls; SQL abstracts complex on-disk and in-memory data structures, concurrent requests from other clients, and inconsistencies after crashes. We are still using machine code when programming in a high-level language — we just aren't thinking about it.

## Trade-offs & Pitfalls
- The essential/accidental distinction is intuitive and frequently cited, and the book explicitly says it doesn't hold up. Worth knowing that this is a considered position, not an oversight.
- Abstractions for *application* code can be built with methodologies such as design patterns and **domain-driven design (DDD)**. This book is deliberately not about those application-specific abstractions — it is about **general-purpose abstractions you can build applications on top of**, such as database transactions, indexes, and event logs. If you want to use DDD, you implement it on top of the foundations this book describes.

## Examples & Systems
High-level programming languages and SQL as the two canonical good abstractions; design patterns and DDD as application-level abstraction methodologies the book positions itself beneath.

## Since the 1st Edition
Largely carried over from the 1st edition's [[Simplicity - Managing Complexity]], including the big ball of mud and the abstraction argument. Sharpened here: the 2nd edition explicitly **criticises the essential/accidental distinction** rather than simply presenting it, and adds the "no objective standard of simplicity" argument with the interface-versus-implementation example.

## Related
- up: [[Maintainability (2e)]] · chapter: [[Ch 02 - Defining Nonfunctional Requirements (2e)]]
- [[Evolvability - Making Change Easy (2e)]] — what simplicity buys you
- [[Principles for Scalability (2e)]] — the same "don't over-complicate" instinct at architecture level
- 1st edition: [[Simplicity - Managing Complexity]] — the same subtopic
