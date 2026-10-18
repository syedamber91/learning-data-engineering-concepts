---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 14
chapter_title: Doing the Right Thing
type: topic
tags: [ddia2, predictive-analytics, algorithmic-prison, ethics]
sources:
  - raw/ch14.md
---
# Predictive Analytics

**Predictive analytics is a major part of why people are excited about big data and AI. It's also an area that is fraught with ethical dilemmas.**

**Using data analysis to predict the weather, or the spread of diseases, is one thing; it is another matter to predict whether a convict is likely to reoffend, whether an applicant for a loan is likely to default, or whether an insurance customer is likely to make expensive claims.** **The latter have a direct effect on individual people's lives.**

**Naturally, payment networks want to prevent fraudulent transactions, banks want to avoid bad loans, airlines want to avoid hijackings, and companies want to avoid hiring ineffective or untrustworthy people.** **From their point of view, the cost of a missed business opportunity is low, but the cost of a bad loan or a problematic employee is much higher, so it is expected for organizations to want to be cautious. If in doubt, they are better off saying no.**

**However, as algorithmic decision making becomes more widespread, someone who has (accurately or falsely) been labeled as risky by an algorithm may suffer a large number of those "no" decisions.** **Systematically being excluded from jobs, air travel, insurance coverage, property rental, financial services, and other key aspects of society is such a large constraint of an individual's freedom that it has been called "algorithmic prison."**

**In countries that respect human rights, the criminal justice system presumes innocence until proven guilty; on the other hand, automated systems can systematically and arbitrarily exclude a person from participating in society without any proof of guilt, and with little chance of appeal.**

## Subtopics
- [[Bias and Discrimination (2e)]]
- [[Responsibility and Accountability (2e)]]
- [[Feedback Loops (2e)]]

## Key Takeaways
- The asymmetry of cost — cheap "no," expensive "yes" — makes caution rational for each organization individually, and catastrophic for the individual across all of them.
- "Algorithmic prison" names the aggregate effect: exclusion without proof of guilt and without appeal.
- The distinction that matters is not prediction versus no prediction, but whether the prediction has a direct effect on an individual person's life.

## Since the 1st Edition
The argument and the "algorithmic prison" framing are carried over from the 1st edition's [[Predictive Analytics]] section, but reframed for the AI era — the text now consistently reads "predictive analytics and AI systems" rather than treating this purely as a big-data phenomenon.

## Related
- up: [[Ch 14 - Doing the Right Thing (2e)]]
- [[Privacy and Tracking (2e)]] — the other half of the chapter: collection rather than decision
- 1st edition: [[Predictive Analytics]] — the same topic, as a section
