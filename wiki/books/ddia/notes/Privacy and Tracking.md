---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 12
chapter_title: The Future of Data Systems
topic: Doing the Right Thing
type: subtopic
tags: [ddia, surveillance, consent, data-ethics]
sources:
  - raw/ch12.md
---
# Privacy and Tracking

> When tracking serves advertisers rather than users, "data collection" is more honestly called surveillance — and privacy rights aren't destroyed but transferred to the collector.

## The Idea
Separate from what algorithms *decide* is what data collection itself *is*. When users deliberately enter data to have it processed, the system serves them: they're the customer. When activity is logged as a side effect, the service acquires interests of its own. Some tracking genuinely helps users (click-through improving search ranking, recommendations, A/B tests) — but under an advertising business model the advertiser is the real customer, tracking deepens, retention lengthens, and profiles accumulate. Kleppmann's test: substitute *surveillance* for *data* in common phrases and the book briefly becomes *Designing Surveillance-Intensive Applications*. Racing toward the Internet of Things — a poorly secured connected microphone in every room via phones, TVs, assistants, toys — we've voluntarily built surveillance infrastructure beyond totalitarian dreams; the collector just happens to be corporate.

## The Reasoning Chain
- **Not obviously benign.** "Nothing to hide" is the privilege of the non-marginalized; insurance premiums tied to car trackers and coverage tied to fitness wearables show surveillance steering life outcomes. Analysis keeps getting more intrusive — a smartwatch's motion sensor can infer typed passwords.
- **Consent is hollow.** Users can't know what data they emit or how it's processed (privacy policies obscure more than illuminate), so consent isn't meaningful; one user's data also describes non-consenting others; derived datasets merging the whole user base with external sources are exactly what no user can comprehend. The exchange is one-sided — terms set by the service. And declining means social exclusion when a service is de facto essential (smartphones, Facebook, Google): opting out is a luxury of the privileged; for everyone else surveillance is inescapable.
- **Privacy is a decision right.** "Privacy is dead" misreads the word: privacy means choosing what to reveal to whom, not secrecy. Surveillance *transfers* that right to the company, which exercises it for profit — revealing intimate attributes indirectly through ad-targeting buckets, hiding the rest lest it look creepy. Privacy settings govern only what *other users* see; the service keeps unfettered internal use. Unlike doctor–patient trust, no ethical/legal regime governs this historically unprecedented transfer.
- **Data as asset — and liability.** "Data exhaust" gets it backwards: under ad funding, behavioral data is the core asset and the app is bait; data brokers and eyeball-based startup valuations prove the market. Governments obtain it by deal, compulsion, or theft; breaches are routine; bankruptcy sells it. Hence "toxic asset" / "hazardous material": collection must be weighed against every possible future government, since installing infrastructure a police state could someday use is poor civic hygiene. Scrutinizing others while escaping scrutiny is itself power.
- **The Industrial Revolution analogy.** Industrialization brought growth plus pollution and child labor until safeguards arrived at real but worthwhile cost; data is the information age's pollution problem (Schneier), and posterity will judge our handling of it. 1995-era EU data-protection principles (specific purposes, no excessive collection) run directly against Big Data's maximize-and-explore philosophy; regulation helps but Kleppmann calls for a culture shift — users as humans not metrics, self-regulation, education, purging data promptly (solvable despite immutability), and cryptographic rather than policy-based access control. Ubiquitous surveillance is not inevitable.

## Related
- up: [[Doing the Right Thing]] · chapter: [[Ch 12 - The Future of Data Systems]]
- [[Predictive Analytics]] — what the collected data gets used to decide
- [[Combining Specialized Tools by Deriving Data]] — the derived datasets consent can't cover
- [[State, Streams, and Immutability]] — immutability vs. the duty to purge
