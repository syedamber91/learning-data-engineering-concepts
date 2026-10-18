---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 14
chapter_title: Doing the Right Thing
topic: Privacy and Tracking
type: subtopic
tags: [ddia2, data-exhaust, toxic-asset, data-brokers, power]
sources:
  - raw/ch14.md
---
# Data as Assets and Power
> "Maybe data is not the new gold, or the new oil, but rather the new uranium."

## The Idea
**Since behavioral data is a byproduct of users interacting with a service, it is sometimes called "data exhaust" — suggesting that the data is worthless waste material.** **Viewed this way, behavioral and predictive analytics can be seen as a form of recycling that extracts value from data that would have otherwise been thrown away.**

**More correct would be to view it the other way around.** **From an economic point of view, if targeted advertising is what pays for a service, then the user activity that generates behavioral data could be regarded as a form of labor.** **One could go even further and argue that the application with which the user interacts is merely a means to lure users into feeding more and more personal information into the surveillance infrastructure.** **The delightful human creativity and social relationships that often find expression in online services are cynically exploited by the data extraction machine.**

## How It Works
**Personal data is a valuable asset, as evidenced by the existence of data brokers operating in secrecy, purchasing, aggregating, analyzing, and reselling people's personal data, mostly for marketing purposes.** **Startups are valued by their user numbers, or "eyeballs" — that is, by their surveillance capabilities.**

**Because the data is valuable, many people want it.** **Of course, companies want it — that's why they collect it in the first place. But governments want it too, and they may seek to obtain it by means of secret deals, coercion, legal compulsion, or simply theft.** **When a company goes bankrupt, the personal data it has collected is one of the assets that get sold.** **And because data is difficult to secure, breaches happen disconcertingly often.**

## Trade-offs & Pitfalls
- **These observations have led critics to say that data is not just an asset, but a "toxic asset," or at least "hazardous material." Maybe data is not the new gold, or the new oil, but rather the new uranium.**
- **Even if we think that we are capable of preventing abuse of data, whenever we collect it, we need to balance the benefits with the risk of it falling into the wrong hands.** **Computer systems may be compromised by criminals or hostile foreign intelligence services, data may be leaked by insiders, the company may fall into the hands of unscrupulous management that does not share our values, or the country may be taken over by a regime that has no qualms about compelling us to hand over the data.**
- **When collecting data, we need to consider not just today's political environment, but all possible future governments.** **There is no guarantee that every government elected in the future will respect human rights and civil liberties, and as Bruce Schneier observes, "It is poor civic hygiene to install technologies that could someday facilitate a police state."**
- **"Knowledge is power," as the old adage goes. And furthermore, "To scrutinize others while avoiding scrutiny oneself is one of the most important forms of power."** **This is why totalitarian governments want surveillance: it gives them the power to control the population.** **Although today's technology companies are not overtly seeking political power, the data and knowledge they have accumulated — much of it surreptitiously, outside of public oversight — nevertheless gives them a lot of power over our lives.**

## Examples & Systems
Data brokers; "eyeballs" as startup valuation; personal data sold in bankruptcy; the police-state civic-hygiene argument.

## Since the 1st Edition
Substantively unchanged, including the data-exhaust inversion, the toxic-asset/uranium framing, and the Schneier civic-hygiene quote.

## Related
- up: [[Privacy and Tracking (2e)]] · chapter: [[Ch 14 - Doing the Right Thing (2e)]]
- [[Privacy and Use of Data (2e)]] — the right that was transferred to create the asset
- [[Legislation and Self-Regulation (2e)]] — the proposed remedy: collect less, purge sooner
