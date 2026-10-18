---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 2
chapter_title: Defining Nonfunctional Requirements
topic: Maintainability
type: subtopic
tags: [ddia2, operability, automation, monitoring, observability]
sources:
  - raw/ch02.md
---
# Operability: Making Life Easy for Operations
> "Good operations can often work around the limitations of bad (or incomplete) software, but good software cannot run reliably with bad operations."

## The Idea
Human processes are at least as important for reliable operations as software tools — the quotation above is the book's headline claim for this subtopic. Operability is what a *system* can do to make those human processes easier.

## How It Works
In large-scale systems of many thousands of machines, manual maintenance would be unreasonably expensive, so **automation is essential**. But automation is a two-edged sword:
- There will always be edge cases — rare failure scenarios — requiring manual intervention. Since the cases that *cannot* be handled automatically tend to be the most complex ones, greater automation requires a **more skilled** operations team to resolve them.
- An automated system that goes wrong is often **harder to troubleshoot** than one relying on an operator to perform some actions manually.

So more automation is not always better for operability, though some amount is important; the sweet spot depends on the specifics of the application and organisation.

Good operability means making routine tasks easy so the operations team can focus on high-value activities. Data systems can help by:
- Allowing monitoring tools to check key metrics, and supporting observability tools that give insight into runtime behaviour (a variety of commercial and open source tools exist).
- **Avoiding dependency on individual machines**, so machines can be taken down for maintenance while the system as a whole keeps running.
- Providing good documentation and an easy-to-understand operational model — "if I do X, Y will happen."
- Providing good default behaviour, while giving administrators freedom to override defaults.
- **Self-healing where appropriate**, but also giving administrators manual control over system state when needed.
- Exhibiting predictable behaviour, minimising surprises.

## Trade-offs & Pitfalls
- The automation paradox is the load-bearing insight: automating the easy 95% raises the skill floor for the remaining 5%, because that 5% is now the only thing humans ever see, and it is the hardest part.
- "Self-healing where appropriate, but also giving administrators manual control" is a design requirement, not a hedge — an automated recovery you cannot override is a new failure mode.

## Examples & Systems
Monitoring and observability tooling; rolling maintenance enabled by not depending on individual machines.

## Since the 1st Edition
Carried over from the 1st edition's [[Operability - Making Life Easy for Operations]] with the same quotation and a very similar checklist. The main additions are the explicit **automation-is-two-edged** argument (more automation demanding a more skilled team, and automated failures being harder to troubleshoot) and the link to observability tooling, which the 1st edition did not have as a named discipline. The surrounding context also changed: [[Operations in the Cloud Era (2e)]] now precedes this in the book and covers who operators are today.

## Related
- up: [[Maintainability (2e)]] · chapter: [[Ch 02 - Defining Nonfunctional Requirements (2e)]]
- [[Operations in the Cloud Era (2e)]] — the changing shape of the operations role
- [[Humans and Reliability (2e)]] — why making operators' lives easier is a reliability measure
- 1st edition: [[Operability - Making Life Easy for Operations]] — the same subtopic
