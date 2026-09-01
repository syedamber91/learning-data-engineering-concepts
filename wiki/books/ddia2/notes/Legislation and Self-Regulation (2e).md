---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 14
chapter_title: Doing the Right Thing
topic: Privacy and Tracking
type: subtopic
tags: [ddia2, gdpr, data-minimization, self-regulation, retention]
sources:
  - raw/ch14.md
---
# Legislation and Self-Regulation
> "Data you don't have is data that can't be leaked, stolen, or compelled by governments to be handed over."

## The Idea
**Data protection laws might be able to help preserve individuals' rights.** **For example, the GDPR states that personal data must be "collected for specified, explicit and legitimate purposes and not further processed in a manner that is incompatible with those purposes" and be "adequate, relevant and limited to what is necessary in relation to the purposes for which [it is] processed."**

**However, this principle of data minimization runs directly counter to the philosophy of big data, which is to maximize data collection, to combine the collected data with other datasets, and to experiment and explore in order to generate new insights.** **Exploration means using data for unforeseen purposes, which the GDPR states is the opposite of the "specified and explicit" purposes for which the data must have been collected.**

## How It Works
**While this regulation has had some effect on the online advertising industry, it has been weakly enforced and does not seem to have led to much of a change in culture and practices across the wider tech industry.**

**Companies that collect lots of data about people broadly oppose regulation as being a burden and a hindrance to innovation. To some extent, that opposition is justified.** **For example, sharing medical data creates clear risks to privacy but also potential opportunities: how many deaths could be prevented if data analysis were able to help us achieve better diagnostics or find better treatments?** **Overregulation may prevent such breakthroughs. It is difficult to balance the potential opportunities with the risks.**

**Fundamentally, we need a culture shift in the tech industry with regard to personal data.** **We should stop regarding users as metrics to be optimized, and remember that they are humans who deserve respect, dignity, and agency.** **We should self-regulate our data collection and processing practices in order to establish and maintain the trust of the people who depend on our software.** **And we should take it upon ourselves to educate end users about how their data is used rather than keeping them in the dark.**

**We should allow each individual to maintain their privacy — their control over their own data — and not steal that control from them through surveillance.** **Our individual right to control our data is like the natural environment of a national park: if we don't explicitly protect and care for it, it will be destroyed. It will be the tragedy of the commons, and we will all be worse off for it.** **Ubiquitous surveillance is not inevitable. We are still able to stop it.**

## Trade-offs & Pitfalls
- The concrete first step is a retention policy, not a policy document: **we should not retain data forever, but purge it as soon as it is no longer needed, and minimize what we collect in the first place.** **Data you don't have is data that can't be leaked, stolen, or compelled by governments to be handed over.**
- **Overall, culture and attitude changes will be necessary.** Law alone has demonstrably not been enough.
- The book grants the industry's objection real weight rather than dismissing it — the medical-research example is a genuine cost of overregulation, and the balance is stated as difficult, not obvious.
- **As people working in technology, if we don't consider the societal impact of our work, we're not doing our job.**

## Examples & Systems
GDPR purpose limitation and data minimization; medical data sharing as the case for not overregulating; retention limits as the practical control.

## Since the 1st Edition
The argument carries over, but with a verdict the 1st edition could not deliver. Published as the GDPR was coming into force, the 1st edition could only describe what the regulation required. The 2nd assesses its record: **some effect on the online advertising industry**, but **weakly enforced** and **not much of a change in culture and practices across the wider tech industry** — which is why the emphasis shifts here from legislation toward self-regulation and a culture shift.

## Related
- up: [[Privacy and Tracking (2e)]] · chapter: [[Ch 14 - Doing the Right Thing (2e)]]
- [[Consent and Freedom of Choice (2e)]] — the GDPR's consent conditions
- [[Remembering the Industrial Revolution (2e)]] — the historical case that safeguards are worth their cost
- [[Data as Assets and Power (2e)]] — why holding less data is a security control, not just a courtesy
