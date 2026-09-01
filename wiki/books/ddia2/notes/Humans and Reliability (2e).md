---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 2
chapter_title: Defining Nonfunctional Requirements
topic: Reliability and Fault Tolerance
type: subtopic
tags: [ddia2, human-error, blameless-postmortem, sociotechnical, operations]
sources:
  - raw/ch02.md
---
# Humans and Reliability
> Configuration changes by operators are the leading cause of outages. Blaming the operator is the least useful possible response.

## The Idea
Humans design and build software systems, and the operators who keep them running are also human. Unlike machines, humans don't just follow rules — being creative and adaptive is one of their strengths. That same characteristic brings unpredictability and sometimes mistakes that lead to failures, despite best intentions. One study of large internet services found that **configuration changes by operators were the leading cause of outages**, while hardware faults (servers or network) played a role in only **10–25%** of cases.

## How It Works
It is tempting to label these problems "human error" and hope to solve them by controlling human behaviour with tighter procedures and rule compliance. The book rejects this squarely: **blaming people for mistakes is counterproductive.** What we call human error is not the cause of an incident but a *symptom* of a problem with the **sociotechnical system** in which people are trying their best to do their jobs. Complex systems also often show emergent behaviour, where unexpected interactions between components lead to failures.

Technical measures that reduce the impact of human mistakes:
- Thorough testing — both handwritten tests and property testing over lots of random inputs.
- Rollback mechanisms for quickly reverting configuration changes.
- Gradual rollouts of new code.
- Detailed and clear monitoring, plus observability tools for diagnosing production issues.
- Well-designed interfaces that encourage the right thing and discourage the wrong thing.

**Blameless postmortems.** Increasingly organisations adopt this culture: after an incident, the people involved are encouraged to share full details of what happened without fear of punishment, so others can learn to prevent similar problems. The process may reveal a need to change business priorities, invest in neglected areas, change incentives, or raise another systemic issue with management.

## Trade-offs & Pitfalls
- All of these measures cost time and money, and in everyday business reality organisations often prioritise revenue-generating work over resilience. Given a choice between more features and more testing, many understandably choose features. **Then, when a preventable mistake inevitably occurs, blaming the person who made it makes no sense — the problem is the organisation's priorities.**
- When investigating an incident, **be suspicious of simplistic answers**. "Bob should have been more careful deploying that change" is unproductive — but so is "we must rewrite the backend in Haskell." Management should instead learn the details of how the sociotechnical system works from the people who work with it daily, and improve it from that feedback.

## Examples & Systems
**How important is reliability?** The book's answer is a warning rather than a platitude. In many applications a temporary outage of minutes or hours is tolerable, but permanent data loss or corruption would be catastrophic — consider a parent storing all their photos and videos of their children in your photo application, and whether they would even know how to restore from backup. The harder example is the **Post Office Horizon scandal**: between 1999 and 2019, hundreds of people managing Post Office branches in Britain were convicted of theft or fraud because the accounting software showed shortfalls in their accounts. Many of those shortfalls turned out to be software bugs, and many convictions were eventually overturned. What enabled probably the largest miscarriage of justice in British history was an assumption in English law that computers operate correctly — and hence that computer-produced evidence is reliable — unless there is evidence to the contrary. Software engineers may laugh at the idea that software could be bug-free, but that is little solace to people who were wrongfully imprisoned, declared bankruptcy, or died by suicide following a wrongful conviction. Reliability can be deliberately sacrificed to reduce development cost — when prototyping for an unproven market, say — but we should be conscious when we cut corners and keep the potential consequences in mind.

## Since the 1st Edition
The 1st edition's [[Human Errors]] carried the same outage statistic and a similar list of mitigations. New in the 2nd edition: the explicit **sociotechnical systems** framing, **blameless postmortems** as a named practice, the "be suspicious of simplistic answers" guidance (with both the blame-the-operator and rewrite-in-Haskell strawmen), and property testing. The 1st edition's separate [[How Important Is Reliability]] subtopic is folded in here as a sidebar, and its examples are replaced by the far heavier **Post Office Horizon** case — an ongoing scandal that had not fully surfaced when the 1st edition was written.

## Related
- up: [[Reliability and Fault Tolerance (2e)]] · chapter: [[Ch 02 - Defining Nonfunctional Requirements (2e)]]
- [[Operability - Making Life Easy for Operations (2e)]] — designing systems that make operators' lives easier
- [[Ch 14 - Doing the Right Thing (2e)]] — the wider consequences of software that harms people
- 1st edition: [[Human Errors]] and [[How Important Is Reliability]] — the two notes this one merges
