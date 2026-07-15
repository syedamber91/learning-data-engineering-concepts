---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 1
chapter_title: Reliable, Scalable, and Maintainable Applications
topic: Reliability
type: subtopic
tags: [ddia, human-error, operations, telemetry, sandbox-environments]
sources:
  - raw/ch01.md
---
# Human Errors
> Operator mistakes — not hardware — are the leading cause of outages, so reliable systems are designed around fallible humans rather than in spite of them.

## The Idea
Humans design, build, and operate every system, and even well-intentioned humans are unreliable. The evidence is stark: a study of large internet services found operator *configuration errors* to be the number-one cause of outages, while hardware faults (servers or network) contributed to only 10–25% of them. Reliability engineering therefore has to treat human error as a first-class fault category, and the question becomes: how do you build reliable systems out of unreliable people?

## How It Works
The best systems layer several complementary defenses:
- **Design out the error.** Good abstractions, APIs, and admin interfaces make the right action easy and the wrong one awkward. But there's a balance: interfaces that are *too* restrictive get worked around, which erases the benefit.
- **Separate mistake-making from damage-doing.** Provide full-featured, non-production sandboxes with real data where people can experiment safely without touching real users.
- **Test at every level** — unit tests through whole-system integration and manual tests. Automation especially earns its keep on corner cases that rarely occur in normal operation.
- **Make recovery fast and cheap.** Quick rollback of configuration, gradual (canary-style) code rollout so bugs hit only a small user slice, and tools to recompute data when an earlier computation proves wrong.
- **Instrument everything.** Detailed monitoring of performance metrics and error rates — what other engineering fields call *telemetry*, the same discipline that tracks a rocket after launch — gives early warning, checks assumptions, and speeds diagnosis when something does break.
- **Manage and train well** — acknowledged as crucial, though beyond the book's scope.

## Trade-offs & Pitfalls
- The restrictiveness dilemma is real: guardrails that block legitimate work get bypassed, and the bypass is usually less safe than what it replaced.
- Sandboxes only help if they are genuinely representative — full-featured and populated with real data.
- Fast rollback and gradual rollout shift the goal from "never err" (impossible) to "err small and recover quickly" — this reframing is the heart of the approach.

## Examples & Systems
- The internet-services outage study (config errors #1; hardware only 10–25%).
- Rocket telemetry as the model for production monitoring.
- Gradual rollouts and configuration rollback as standard recovery machinery.

## Related
- up: [[Reliability]] · chapter: [[Ch 01 - Reliable, Scalable, and Maintainable Applications]]
- [[Software Errors]] — bugs humans write; this note covers mistakes humans make operating
- [[Operability - Making Life Easy for Operations]] — the maintainability face of the same concern
- [[How Important Is Reliability]] — why this diligence matters even in mundane apps
