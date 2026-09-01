---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 14
chapter_title: Doing the Right Thing
topic: Predictive Analytics
type: subtopic
tags: [ddia2, accountability, credit-scoring, explainability, recourse]
sources:
  - raw/ch14.md
---
# Responsibility and Accountability
> A credit score summarizes "How did you behave in the past?" Predictive analytics asks "Who is similar to you, and how did people like you behave in the past?"

## The Idea
**Automated decision making opens the question of responsibility and accountability.** **If a human makes a mistake, they can be held accountable, and the person affected by the decision can appeal.** **Algorithms make mistakes too, but who is accountable if they go wrong?**

**When a self-driving car causes an accident, who is responsible? If an automated credit scoring algorithm systematically discriminates against people of a particular race or religion, is there any recourse? If a decision by your ML system comes under judicial review, can you explain to the judge how the algorithm made its decision?**

**People should not be able to evade their responsibility by blaming an algorithm.**

## How It Works
**Credit rating agencies are a classic example of collecting data to make decisions about people.** **A bad credit score makes life difficult, but at least a credit score is normally based on relevant facts about a person's actual borrowing history, and any errors in the record can be corrected** (although the agencies normally do not make this easy).

**Scoring algorithms based on machine learning, however, typically use a much wider range of inputs and are much more opaque, making it harder to understand how a particular decision has come about and whether someone is being treated in an unfair or discriminatory way.**

**Drawing parallels to others' behavior implies stereotyping people — for example, based on where they live (a close proxy for race and socioeconomic class).** **What about people who get put in the wrong bucket?** **Furthermore, if a decision is incorrect because of erroneous data, recourse is almost impossible.**

## Trade-offs & Pitfalls
- **Much data is statistical in nature, which means that even if the probability distribution on the whole is correct, individual cases may well be wrong.** **If the average life expectancy in your country is 80 years, that doesn't mean you're expected to drop dead on your 80th birthday.** **Similarly, the output of a prediction system is probabilistic and may well be wrong in individual cases.**
- **A blind belief in the supremacy of data for making decisions is not only delusional but also positively dangerous.** **We will need to figure out how to avoid reinforcing existing biases, how to make algorithms accountable and transparent, and how to fix them when they inevitably make mistakes.**
- The same power cuts both ways. **Analytics can reveal financial and social characteristics of people's lives.** **This power could be used to focus aid and support to help those who need it most** — **on the other hand, it is sometimes used by predatory businesses seeking to identify vulnerable people and sell them risky products such as high-cost loans or worthless college degrees.**

## Examples & Systems
Credit rating agencies as the auditable baseline; ML-based scoring as the opaque successor; self-driving car liability.

## Since the 1st Edition
Carried over largely intact, with judicial-review explainability added to the list of accountability questions — reflecting how much more central algorithmic explainability has become since the 1st edition.

## Related
- up: [[Predictive Analytics (2e)]] · chapter: [[Ch 14 - Doing the Right Thing (2e)]]
- [[Bias and Discrimination (2e)]] — where the wrong decision comes from
- [[Trust, but Verify (2e)]] — the technical analogue: auditability as a design goal
