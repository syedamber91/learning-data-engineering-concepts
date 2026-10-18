---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 14
chapter_title: Doing the Right Thing
topic: Privacy and Tracking
type: subtopic
tags: [ddia2, surveillance, iot, sensors, thought-experiment]
sources:
  - raw/ch14.md
---
# Surveillance
> "In our surveillance-driven organization we collect real-time surveillance streams and store them in our surveillance warehouse."

## The Idea
**As a thought experiment, try replacing the word *data* with *surveillance*, and observe whether common phrases still sound so good.** **How about this: "In our surveillance-driven organization we collect real-time surveillance streams and store them in our surveillance warehouse. Our surveillance scientists use advanced analytics and surveillance processing in order to derive new insights."**

**This thought experiment is unusually polemic for this book, *Designing Surveillance-Intensive Applications*, but strong words are needed to emphasize this point.**

## How It Works
**In our attempts to make software "eat the world," we have built the greatest mass surveillance infrastructure ever seen.** **We are rapidly approaching a world in which every inhabited space contains at least one internet-connected microphone, in the form of smartphones, smart TVs, voice-controlled assistant devices, baby monitors, and even children's toys that use cloud-based speech recognition.** **Many of these devices have a terrible security record.**

**What is new compared to the past is that digitization has made it easy to collect large amounts of data about people.** **Surveillance of our location and movements, our social relationships and communications, our purchases and payments, and our health data has become almost unavoidable.** **A surveillance organization may end up knowing more about a person than that person knows about themselves — for example, identifying illnesses or economic problems before that individual is aware of them.**

**Even the most totalitarian and repressive regimes of the past could only dream of putting a microphone in every room and forcing every person to constantly carry a device capable of tracking their location and movements.** **Yet the benefits that we get from digital technology are so great that we now voluntarily accept this state of total surveillance.** **The difference is just that the data is being collected by corporations to provide us with services, rather than government agencies seeking control.**

## Trade-offs & Pitfalls
- **Not all data collection necessarily qualifies as surveillance, but examining it as such can help us understand our relationship with the data collector.**
- **Why are we seemingly happy to accept surveillance by corporations?** **Perhaps you feel you have nothing to hide — in other words, you are totally in line with existing power structures, you are not a marginalized minority, and you needn't fear persecution. Not everyone is so fortunate.**
- **Or perhaps it's because the purpose seems benign — it's not overt coercion and conformance, merely better recommendations and more personalized marketing.** Combined with predictive analytics, **that distinction seems less clear.**
- **When surveillance is used to make decisions that hold sway over important aspects of life, such as insurance coverage or employment, it starts to appear less benign.**

## Examples & Systems
**Behavioral data on car driving, tracked by cars without drivers' consent, affecting their insurance premiums**; **health insurance coverage that depends on people wearing a fitness tracking device**; **the movement sensor in a smartwatch or fitness tracker used to work out what you are typing (e.g., passwords) with fairly good accuracy.** **Sensor accuracy and algorithms for analysis are only going to get better.**

## Since the 1st Edition
The thought experiment and the mass-surveillance-infrastructure argument carry over verbatim in spirit. **New:** the car-telematics-to-insurance-premium example, reflecting how much further ambient sensing has spread since the 1st edition.

## Related
- up: [[Privacy and Tracking (2e)]] · chapter: [[Ch 14 - Doing the Right Thing (2e)]]
- [[Consent and Freedom of Choice (2e)]] — why "they agreed" doesn't excuse it
- [[Data as Assets and Power (2e)]] — who wants what the infrastructure collects
