---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 12
chapter_title: The Future of Data Systems
type: topic
tags: [ddia, ethics, privacy, algorithmic-accountability]
sources:
  - raw/ch12.md
---
# Doing the Right Thing

The book's closing argument steps outside engineering: every system is built for a purpose, but its consequences reach further, and the engineers who build it share responsibility for them. Many datasets are about people — behavior, interests, identity — and deserve to be handled with humanity and respect; a technology is neither good nor bad in itself, but how it is used and whom it affects is an ethical question engineers cannot delegate. Codes like the ACM's software engineering ethics exist yet are rarely applied, and cavalier attitudes toward privacy and downstream harm are common. The two subtopics develop the argument concretely: automated decision-making that can imprison people in algorithmic verdicts, and data collection that has quietly become mass surveillance.

## Subtopics
- [[Predictive Analytics]] — algorithmic decisions about credit, insurance, employment; bias laundering, opaque models, accountability gaps, and poverty-reinforcing feedback loops.
- [[Privacy and Tracking]] — when logging user activity becomes surveillance; the emptiness of consent, privacy as a transferred (not eroded) right, and data as toxic asset and instrument of power.

## Key Takeaways
- Data-driven decisions extrapolate the past: feed a model biased data and it amplifies the bias — "fair because an algorithm did it" is an illusion, and moral imagination remains a human job.
- Being wrongly classified by opaque systems can systematically exclude a person from jobs, credit, travel, and insurance — an "algorithmic prison" with no presumption of innocence and little appeal.
- Probabilistic outputs are wrong in individual cases even when the distribution is right; accountability, transparency, and recourse must be designed in, not bolted on.
- Behavioral tracking funded by advertising inverts the relationship: the user stops being the customer, and "data" reads honestly as "surveillance."
- Consent without understanding is not meaningful, and opting out of essential services is not freedom; privacy is the *right to choose* what to reveal — a right currently being transferred wholesale to corporations.
- Kleppmann's Industrial Revolution analogy: data is the pollution of the information age; like environmental regulation, protections (purging data, cryptographic access control, self-regulation, treating users as humans rather than metrics) will cost something and be worth it.

## Related
- chapter: [[Ch 12 - The Future of Data Systems]] · part: [[Part III - Derived Data]]
- [[Thinking About Data Systems]] — Ch 1's framing of what we're responsible for building
- [[Observing Derived State]] — the same dataflow machinery, aimed at people
- [[Aiming for Correctness]] — correctness toward systems; this topic is correctness toward humans
