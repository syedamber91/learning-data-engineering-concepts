---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 1
chapter_title: Reliable, Scalable, and Maintainable Applications
topic: Reliability
type: subtopic
tags: [ddia, reliability, cost-tradeoffs, responsibility]
sources:
  - raw/ch01.md
---
# How Important Is Reliability?
> Reliability isn't reserved for nuclear plants and air traffic control — ordinary applications carry real human and business stakes, and trading reliability away should always be a deliberate choice.

## The Idea
It's tempting to file reliability under "safety-critical systems only." The chapter pushes back: mundane business and consumer applications are also expected to work. The section is short but plays a load-bearing role in the chapter — it converts reliability from an engineering nicety into an obligation, while acknowledging that the obligation has limits.

## Why It Matters
Two categories of stakes:
- **Business stakes.** Bugs in business software cost productivity — and create legal exposure when, say, figures get reported incorrectly. Ecommerce outages burn revenue directly and damage reputation, which is costlier still.
- **Human stakes.** Even a "noncritical" app holds things users deeply value. The chapter's example: a parent keeping every photo and video of their children in your photo application. If that database silently corrupted, the loss is irreplaceable — and would they even know how to restore a backup? Responsibility to users exists regardless of whether the app is labeled critical.

## Trade-offs & Pitfalls
Reliability is not an absolute. There are legitimate reasons to trade it down:
- **Development cost** — a prototype for an unproven market shouldn't be engineered like a bank ledger; speed of iteration matters more (a theme echoed in [[Approaches for Coping with Load]] regarding premature scaling).
- **Operational cost** — a service running on razor-thin margins may not afford gold-plated fault tolerance.

The pitfall isn't making these trades — it's making them *unconsciously*. Cutting corners is acceptable engineering; drifting into cut corners without noticing is not. Teams should be able to state which reliability properties they've sacrificed and why.

## Examples & Systems
- Incorrectly reported business figures as a legal-risk scenario.
- Ecommerce downtime as direct revenue and reputation loss.
- The family-photos application as the emblem of user trust in "noncritical" software.

## Related
- up: [[Reliability]] · chapter: [[Ch 01 - Reliable, Scalable, and Maintainable Applications]]
- [[Human Errors]] — the defenses this obligation pays for
- [[Hardware Faults]] — the baseline fault class every app faces
- [[Approaches for Coping with Load]] — the parallel argument about premature scaling in startups
