---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 14
chapter_title: Doing the Right Thing
topic: Predictive Analytics
type: subtopic
tags: [ddia2, bias, discrimination, protected-traits, proxy-variables]
sources:
  - raw/ch14.md
---
# Bias and Discrimination
> "Machine learning is like money laundering for bias."

## The Idea
**Decisions made by an algorithm are not necessarily any better or any worse than those made by a human.** **Every person is likely to have biases, even if they actively try to counteract them, and discriminatory practices can become culturally institutionalized.** **There is hope that basing decisions on data, rather than subjective and instinctive assessments by people, could be more fair and give a better chance to people who are often overlooked or disadvantaged in the traditional system.**

That hope is the thing this section takes apart.

## How It Works
**When we develop predictive analytics and AI systems, we are not merely automating a human's decision by using software to specify the rules for when to say yes or no; we are leaving the rules themselves to be inferred from data.**

**However, the patterns learned by these systems are opaque: even if the data indicates a correlation, we may not know why.** **If the input to an algorithm carries a systematic bias, the system will most likely learn and amplify that bias in its output.**

**In many countries, anti-discrimination laws prohibit treating people differently depending on protected traits such as ethnicity, age, gender, sexuality, disability, or beliefs.** **Other features of a person's data may be analyzed, but what happens if they are correlated with protected traits?** **For example, in racially segregated neighborhoods, a person's postal code or even their IP address is a strong predictor of race.**

**Put like this, it seems ridiculous to believe that an algorithm could somehow take biased data as input and produce fair and impartial output from it.** **Yet this belief often seems to be implied by proponents of data-driven decision making — an attitude that has been satirized as "machine learning is like money laundering for bias."**

## Trade-offs & Pitfalls
- **Predictive analytics systems merely extrapolate from the past; if the past is discriminatory, they codify and amplify that discrimination.**
- Removing protected traits from the input does not remove the bias, because ordinary features act as proxies for them.
- **If we want the future to be better than the past, moral imagination is required, and that's something only humans can provide. Data and models should be our tools, not our masters.**

## Examples & Systems
Postal code and IP address as proxies for race in segregated neighborhoods.

## Since the 1st Edition
Substantively the same argument as the 1st edition, with the framing shifted from "algorithms" generally to "predictive analytics and AI systems," and the emphasis that the rules themselves — not just their execution — are now inferred from data.

## Related
- up: [[Predictive Analytics (2e)]] · chapter: [[Ch 14 - Doing the Right Thing (2e)]]
- [[Responsibility and Accountability (2e)]] — what happens after a biased decision lands
- [[Feedback Loops (2e)]] — how a small bias compounds
