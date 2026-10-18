---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 14
chapter_title: Doing the Right Thing
topic: Predictive Analytics
type: subtopic
tags: [ddia2, feedback-loop, echo-chamber, systems-thinking, algorithmic-collusion]
sources:
  - raw/ch14.md
---
# Feedback Loops
> "A downward spiral due to poisonous assumptions, hidden behind a camouflage of mathematical rigor and data."

## The Idea
**Even with predictive applications that have less immediately far-reaching effects on people, such as recommendation systems, there are difficult issues that we must confront.** **When services become good at predicting the content users want to see, they may end up showing people only opinions they already agree with, leading to echo chambers in which stereotypes, misinformation, and polarization can breed.** **We are already seeing the impact social media echo chambers can have on election campaigns.**

**When predictive analytics affect people's lives, particularly pernicious problems arise because of self-reinforcing feedback loops.**

## How It Works
**Consider the case of employers using credit scores to evaluate potential hires.** **You may be a good worker with a good credit score, but suddenly find yourself in financial difficulties due to a misfortune outside of your control.** **As you miss payments on your bills, your credit score suffers, and you will be less likely to find work.** **Joblessness pushes you toward poverty, which further worsens your score, making it even harder to find employment.** **It's a downward spiral due to poisonous assumptions, hidden behind a camouflage of mathematical rigor and data.**

**As another example of a feedback loop, economists found that when gas stations in Germany introduced algorithmic prices, competition was reduced and prices for consumers went up because the algorithms learned to collude.**

**We can't always predict when such feedback loops may happen.** **However, many consequences can be predicted by thinking about the entire system — not just the computerized parts, but also the people interacting with it — an approach known as systems thinking.**

**We can try to understand how a data analysis system responds to different behaviors, structures, or characteristics.** **Does the system reinforce and amplify existing differences between people (e.g., making the rich richer or the poor poorer), or does it try to combat injustice?**

## Trade-offs & Pitfalls
- **Even with the best intentions, we must beware of the possibility of unintended consequences.**
- The loop is invisible from inside any single component; only the whole socio-technical system exhibits it. Testing the model in isolation will never surface it.
- Nobody designed the German gas stations to collude. The pricing algorithms discovered it — which is why "we didn't intend that" is not a defense.

## Examples & Systems
Recommendation-driven echo chambers and election campaigns; the credit-score/employment downward spiral; German gas-station algorithmic price collusion.

## Since the 1st Edition
The echo-chamber and credit-score-spiral examples carry over. **New in the 2nd edition:** the German gas-station algorithmic price collusion finding, and the explicit naming of **systems thinking** as the discipline for anticipating these loops — the 1st edition described the practice without giving it that name.

## Related
- up: [[Predictive Analytics (2e)]] · chapter: [[Ch 14 - Doing the Right Thing (2e)]]
- [[Bias and Discrimination (2e)]] — the initial asymmetry a loop amplifies
- [[Responsibility and Accountability (2e)]] — why "the algorithm did it" isn't an answer
