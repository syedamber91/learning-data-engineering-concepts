---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 14
chapter_title: Doing the Right Thing
topic: Privacy and Tracking
type: subtopic
tags: [ddia2, privacy, decision-right, autonomy, privacy-settings]
sources:
  - raw/ch14.md
---
# Privacy and Use of Data
> "The right to privacy is a decision right." Privacy is not secrecy — it is who gets to choose.

## The Idea
**Sometimes people claim that "privacy is dead" on the grounds that some users are willing to post all sorts of things about their lives to social media, sometimes mundane and sometimes deeply personal.** **However, this claim is false and rests on a misunderstanding of the word privacy.**

**Having privacy does not mean keeping everything secret; it means having the freedom to choose what to reveal to whom, what to make public, and what to keep secret.** **The right to privacy is a decision right: it enables each person to decide where they want to be on the spectrum between secrecy and transparency in each situation.** **It is an important aspect of a person's freedom and autonomy.**

**For example, someone who suffers from a rare medical condition might be very happy to provide their private medical data to researchers if it might help the development of treatments for their condition.** **However, this person must have a choice over who may access this data and for what purpose.** **If information about their condition could hinder their access to medical insurance or employment, this person would probably be much more cautious about sharing their data.**

## How It Works
**When data is extracted from people through surveillance infrastructure, privacy rights are not necessarily eroded but rather transferred to the data collector.** **Companies that acquire data essentially say, "Trust us to do the right thing with your data," which means that the right to decide what to reveal and what to keep secret is transferred from the individual to the company.**

**The companies in turn choose to keep much of the outcome of this surveillance secret, because to reveal it would be perceived as creepy and would harm their business model** — which relies on knowing more about people than other companies do. **Intimate information about users is revealed only indirectly — for example, in the form of tools for targeting advertisements to specific groups of people (such as those suffering from a particular illness).**

**Even if particular users cannot be personally reidentified from the bucket of people targeted by a particular ad, they have lost their agency about the disclosure of some intimate information.** **It is not the user who decides what is revealed to whom on the basis of their personal preferences — it is the company that exercises the privacy right with the goal of maximizing its profit.**

## Trade-offs & Pitfalls
- **Many companies want to avoid being perceived as creepy, avoiding the question of how intrusive their data collection actually is and instead focusing on managing user perceptions.**
- **Even these perceptions are often managed poorly — something may be factually correct, but if it triggers painful memories, the user may not want to be reminded about it.** **With any kind of data, we should expect the possibility that it is wrong, undesirable, or inappropriate in some way, and we need to build mechanisms for handling those failures.** **Whether something is "undesirable" or "inappropriate" is of course down to human judgment; algorithms are oblivious to such notions unless we explicitly program them to respect human needs. As engineers of these systems, we must be humble, accepting and planning for such failings.**
- **Privacy settings that allow a user to control which aspects of their data other users can see are a starting point for handing back some control.** **However, regardless of the setting, the service itself still has unfettered access to the data and is free to use it in any way permitted by the privacy policy.** **Even if the service promises not to sell the data to third parties, it usually grants itself unrestricted rights to process and analyze the data internally, often going much further than what is overtly visible to users.**
- **This kind of large-scale transfer of privacy rights from individuals to corporations is historically unprecedented.** **Surveillance has always existed, but it used to be expensive and manual, not scalable and automated.** **Trust relationships have always existed — between a patient and their doctor, or a defendant and their attorney — but in these cases the use of data has been strictly governed by ethical, legal, and regulatory constraints.**

## Examples & Systems
Rare-medical-condition data sharing as the illustration of privacy-as-choice; illness-targeted ad audiences as indirect disclosure; the doctor/attorney relationship as the regulated counterexample.

## Since the 1st Edition
Substantively unchanged — this is one of the 1st edition's most quoted passages and it survives intact, including the "privacy is a decision right" definition and the anniversary-reminder example of factually-correct-but-unwanted data.

## Related
- up: [[Privacy and Tracking (2e)]] · chapter: [[Ch 14 - Doing the Right Thing (2e)]]
- [[Consent and Freedom of Choice (2e)]] — the mechanism by which the right is transferred
- [[Data as Assets and Power (2e)]] — what the transferred right is worth
