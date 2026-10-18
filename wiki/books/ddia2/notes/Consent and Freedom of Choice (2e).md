---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 14
chapter_title: Doing the Right Thing
topic: Privacy and Tracking
type: subtopic
tags: [ddia2, consent, gdpr, network-effects, dark-patterns]
sources:
  - raw/ch14.md
---
# Consent and Freedom of Choice
> Consent must be "freely given, specific, informed, and unambiguous" — and the user must be able to "refuse or withdraw consent without detriment."

## The Idea
**We might assert that users voluntarily choose to use services that track their activity, agreeing to the terms of service and privacy policy and consenting to data collection.** **We might even claim that users are receiving a valuable service in return for the data they provide, and that the tracking is necessary in order to provide the service.** **Undoubtedly, social networks, search engines, and various other free online services are valuable to users — but this argument has problems.**

## How It Works
**First, we should ask why the tracking is necessary.** **Some forms of tracking directly feed into improving features for users** — **tracking the click-through rate on search results can help improve a search engine's result ranking and relevance, and tracking which products customers tend to buy together can help an online shop suggest related products.** **However, when tracking user interaction for content recommendations, or to build user profiles for advertising purposes, it is less clear whether this is genuinely in the user's interest. Is it necessary only because the ads pay for the service?**

**Second, most users have little knowledge of what data they are feeding into our databases or how it is retained and processed — and most privacy policies do more to obscure than to illuminate.** **Without understanding what happens to their data, users cannot give meaningful consent.** **Often, data from one user also says things about other people who are not users of the service and who have not agreed to any terms.** **The derived datasets we discussed in the last few chapters — in which data from the entire user base may have been combined with behavioral tracking and external data sources — are precisely the kinds of data that users cannot meaningfully understand.**

**Moreover, data is extracted from users through a one-way process, not a relationship with true reciprocity or a fair value exchange.** **There is no dialogue, no option for users to negotiate how much data they provide and what service they receive in return.** **The relationship between the service and the user is asymmetric and one-sided; the terms are set by the service, not by the user.**

**In the European Union, the GDPR requires that consent must be "freely given, specific, informed, and unambiguous" and that the user must be able to "refuse or withdraw consent without detriment" — otherwise, it is not considered "freely given."** **Any request for consent must be written "in an intelligible and easily accessible form, using clear and plain language," and "silence, pre-ticked boxes or inactivity [do not] constitute consent."**

**Consent is not the only basis for lawful processing of personal data under the GDPR.** **There are also several other bases, including to comply with other legislation or to protect somebody's life.** **In addition, the legitimate interest basis permits certain uses of data (e.g., for fraud prevention)** — which fraudsters would presumably not consent to. **Nevertheless, consent is the most frequently used basis for personal data processing in internet services.**

## Trade-offs & Pitfalls
- **You might argue that a user who does not consent to surveillance can simply choose not to use a service. But this choice is not free either.** **If a service is so popular that it is "regarded by most people as essential for basic social participation," then it is not reasonable to expect people to opt out of using it — its use is effectively mandatory.**
- **Especially when a service has network effects, there is a social cost to people choosing not to use it.**
- **These platforms are designed specifically to engage users. Many use game mechanics and tactics common in gambling to keep users coming back.**
- **Declining to engage is an option for only the small number of people who are privileged enough to have the time and knowledge to understand its privacy policy, and who can afford to potentially miss out on social participation or professional opportunities.** **For people in a less privileged position, there is no meaningful freedom of choice; surveillance becomes inescapable.**

## Examples & Systems
Search click-through and market-basket tracking as genuinely user-serving; the GDPR's consent conditions and its legitimate-interest basis; the smartphone/social-network/search norm as effectively mandatory participation.

## Since the 1st Edition
Argument unchanged. The GDPR discussion is now written with hindsight rather than anticipation — the 1st edition was published as the regulation came into force, whereas the 2nd can assess it (see [[Legislation and Self-Regulation (2e)]]).

## Related
- up: [[Privacy and Tracking (2e)]] · chapter: [[Ch 14 - Doing the Right Thing (2e)]]
- [[Surveillance (2e)]] — what is being consented to
- [[Legislation and Self-Regulation (2e)]] — whether the law has actually helped
