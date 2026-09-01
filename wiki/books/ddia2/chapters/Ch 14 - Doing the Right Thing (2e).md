---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 14
chapter_title: Doing the Right Thing
type: chapter-moc
tags: [ddia2, ethics, privacy, surveillance, predictive-analytics, moc]
sources:
  - raw/ch14.md
---
# Ch 14 — Doing the Right Thing

The book's final chapter steps back from mechanism to consequence. **Every system is built for a purpose; every action we take has both intended and unintended consequences.** **The purpose may be as simple as making money, but the consequences may be far-reaching.** **We, the engineers building these systems, have a responsibility to carefully consider those consequences and to ensure that our decisions do not cause harm.**

**We talk about data as an abstract thing, but remember that many datasets are about people: their behavior, their interests, their identity.** **We must treat such data with humanity and respect. Users are humans too, and human dignity is paramount.**

**A technology is not good or bad in itself — what matters is how it is used and how it affects people.** **This is true of a software system like a search engine in much the same way as it is of a weapon like a gun.** **The ethical responsibility is ours to bear; it is not sufficient for software engineers to focus exclusively on the technology and ignore its consequences.**

**In contrast to much of computing, the concepts at the heart of ethics are not fixed or determinate in their precise meaning; they require interpretation, which may be subjective.** **Ethics is not going through a checklist to confirm you comply; it's a participatory and iterative process of reflection, in dialog with the people involved, with accountability for the results.**

## Map
- [[Predictive Analytics (2e)]] — using data to make automated decisions about people
  - [[Bias and Discrimination (2e)]] — why biased input cannot produce impartial output
  - [[Responsibility and Accountability (2e)]] — who answers when an algorithm is wrong
  - [[Feedback Loops (2e)]] — self-reinforcing spirals and systems thinking
- [[Privacy and Tracking (2e)]] — the ethics of collection itself
  - [[Surveillance (2e)]] — the thought experiment of swapping "data" for "surveillance"
  - [[Consent and Freedom of Choice (2e)]] — why "they agreed to the terms" doesn't hold up
  - [[Privacy and Use of Data (2e)]] — privacy as a decision right, transferred to companies
  - [[Data as Assets and Power (2e)]] — data as a toxic asset, and who else wants it
  - [[Remembering the Industrial Revolution (2e)]] — data as the pollution of the information age
  - [[Legislation and Self-Regulation (2e)]] — GDPR, data minimization, and the culture shift needed

## Chapter Summary
Two families of harm are examined. **Predictive analytics** makes automated decisions that **have a direct effect on individual people's lives** — reoffending, loan default, insurance claims. Because organizations are cautious, **if in doubt they are better off saying no**, and a person labeled risky **may suffer a large number of those "no" decisions**, a condition called **algorithmic prison**. The systems **merely extrapolate from the past; if the past is discriminatory, they codify and amplify that discrimination.**

**Privacy and tracking** concerns data collection itself. When tracking is **a side effect of other things the user is doing**, the service **takes on interests of its own, which may conflict with the user's interests** — a relationship best described as **surveillance**. Consent given under those conditions is not meaningfully free, privacy is **a decision right** that gets **transferred to the data collector**, and the accumulated data becomes **a "toxic asset"** wanted by companies, governments, and criminals alike.

The chapter closes with the Industrial Revolution analogy — **data is the pollution problem of the information age, and protecting privacy is the environmental challenge** — and a call to **stop regarding users as metrics to be optimized**, to self-regulate, to **not retain data forever, but purge it as soon as it is no longer needed**, because **data you don't have is data that can't be leaked, stolen, or compelled by governments to be handed over.**

## Since the 1st Edition
**This is the biggest structural change of the 2nd edition's back half.** In the 1st edition the ethics material was a *section* — "Doing the Right Thing" — buried at the end of Chapter 12, "The Future of Data Systems," where it followed pages of technical argument about unbundling the database. In the 2nd edition it is promoted to a **chapter of its own**, the last one in the book, and the technical material it used to share space with became [[Ch 13 - A Philosophy of Streaming Systems (2e)]].

The content is substantially expanded and updated:
- **AI is now the framing**, not just "big data." The epigraph is about feeding AI systems on the world's ugliness; the text speaks of "predictive analytics and AI systems" where the 1st edition said only predictive analytics.
- **Algorithmic price collusion** is added as a feedback-loop example — German gas stations whose pricing algorithms learned to collude, reducing competition and raising consumer prices.
- **Systems thinking** is named explicitly as the discipline for anticipating feedback loops.
- **Car telematics affecting insurance premiums without driver consent** is added to the surveillance examples.
- The GDPR discussion is updated with a verdict the 1st edition could not yet render: it **has had some effect on the online advertising industry** but **has been weakly enforced and does not seem to have led to much of a change in culture and practices across the wider tech industry.**
- The ACM Code of Ethics is cited, along with the observation that such guidelines are **rarely discussed, applied, and enforced in practice.**

## Related
- home: [[Home (2e)]] · previous: [[Ch 13 - A Philosophy of Streaming Systems (2e)]]
- 1st edition: [[Doing the Right Thing]] — the section this chapter grew out of, inside [[Ch 12 - The Future of Data Systems]]
