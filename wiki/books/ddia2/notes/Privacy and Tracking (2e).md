---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 14
chapter_title: Doing the Right Thing
type: topic
tags: [ddia2, privacy, tracking, behavioral-data, advertising]
sources:
  - raw/ch14.md
---
# Privacy and Tracking

**Besides the problems of predictive analytics — that is, using data to make automated decisions about people — there are ethical problems with data collection itself.** **What is the relationship between the organizations collecting data and the people whose data is being collected?**

**When a system stores only data that a user has explicitly entered, because they want the system to store and process it in a certain way, the system is performing a service for the user; the user is the customer.** **But when a user's activity is tracked and logged as a side effect of other things they are doing, the relationship is less clear.** **The service no longer just does what the user tells it to do; it takes on interests of its own, which may conflict with the user's interests.**

**Tracking behavioral data has become increasingly important for user-facing features of many online services.** **Tracking which search results are clicked helps improve the ranking of search results; providing recommendations ("people who liked X also liked Y") helps users discover interesting and useful things; A/B tests and user flow analysis can help indicate how a UI might be improved.** **Those features require some amount of tracking of user behavior, and users benefit from them.**

**However, depending on a company's business model, tracking often doesn't stop there.** **If the service is funded through advertising, the advertisers are the actual customers, and the users' interests take second place.** **Tracking data becomes more detailed, analyses become further-reaching, and data is retained for a long time in order to build up detailed profiles of each person for marketing purposes.**

**The user is given a free service and is coaxed into engaging with it as much as possible.** **The tracking of the user primarily serves not that individual but rather the needs of the advertisers who are funding the service.** **This relationship can be appropriately described with a word that has more sinister connotations: surveillance.**

## Subtopics
- [[Surveillance (2e)]]
- [[Consent and Freedom of Choice (2e)]]
- [[Privacy and Use of Data (2e)]]
- [[Data as Assets and Power (2e)]]
- [[Remembering the Industrial Revolution (2e)]]
- [[Legislation and Self-Regulation (2e)]]

## Key Takeaways
- The test is not *whether* data is collected but *for whom*: data the user asked you to keep is a service; data collected as a side effect serves someone else.
- Some tracking genuinely improves the product for the user. The problem is that the same infrastructure scales seamlessly past that point, and the business model decides where it stops.
- "Who is the customer?" is the sharpest single question. If advertisers pay, the user is not the customer.

## Since the 1st Edition
The structure and argument carry over from the 1st edition's [[Privacy and Tracking]] section, expanded into six subsections here with updated examples (car telematics affecting insurance premiums; a verdict on GDPR's actual enforcement record).

## Related
- up: [[Ch 14 - Doing the Right Thing (2e)]]
- [[Predictive Analytics (2e)]] — what the collected data is then used to decide
- 1st edition: [[Privacy and Tracking]] — the same topic, as a section
