---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 2
chapter_title: Defining Nonfunctional Requirements
type: topic
tags: [ddia2, reliability, fault, failure, fault-tolerance]
sources:
  - raw/ch02.md
---
# Reliability and Fault Tolerance
Everybody has an intuitive sense of reliability; the chapter makes it precise. For software, typical expectations are that the application performs the function the user expected, tolerates the user making mistakes or using it in unexpected ways, performs well enough for the required use case under the expected load and data volume, and prevents unauthorized access and abuse. If all of that together means "working correctly," then **reliability means continuing to work correctly even when things go wrong**.

To be precise about "things going wrong," the book separates two words that are usually used loosely:
- A **fault** occurs when a particular part of a system stops working correctly — a single hard drive malfunctions, a single machine crashes, an external service the system depends on has an outage.
- A **failure** occurs when the system as a whole stops providing the required service to the user — in other words, when it does not meet the SLO.

The distinction is confusing because they are the same thing at different levels. If a hard drive stops working, that drive has *failed*; if the system consists only of that drive, the system has failed too. But if the system has multiple drives, one drive failing is only a *fault* from the bigger system's point of view — and the bigger system may tolerate it by holding a copy of the data elsewhere.

## Subtopics
- [[Fault Tolerance (2e)]] — single points of failure, the bounded nature of tolerance, fault injection, and chaos engineering.
- [[Hardware and Software Faults (2e)]] — real-world failure rates, redundancy, availability zones, and why software faults are the dangerous ones.
- [[Humans and Reliability (2e)]] — operators as the leading cause of outages, and blameless postmortems as the response.

## Key Takeaways
- Fault and failure are level-relative. Naming which level you are talking about removes most confusion in incident discussions.
- A failure is defined by the SLO, which is why [[Use of Response Time Metrics (2e)]] comes before this topic rather than after it.
- Tolerating faults is generally preferred to preventing them — but not always. Where prevention is better because no cure exists, prevention wins: the book's example is security, since an attacker who has compromised a system and accessed sensitive data cannot have that undone.
- Reliability is not only for nuclear power stations and air traffic control. Bugs in business applications cost productivity and create legal risk if figures are misreported; ecommerce outages cost revenue and reputation.

## Since the 1st Edition
The 1st edition's [[Reliability]] topic made the same fault/failure distinction and the same "continuing to work correctly when things go wrong" definition. The 2nd edition sharpens the level-relativity argument, ties "failure" explicitly to the SLO (a link the 1st edition did not make, since it barely used SLOs), and restructures the subtopics: the 1st edition had four ([[Hardware Faults]], [[Software Errors]], [[Human Errors]], [[How Important Is Reliability]]); the 2nd has three, merging hardware and software into one, and folding the importance-of-reliability argument into a sidebar within the humans subtopic.

## Related
- chapter: [[Ch 02 - Defining Nonfunctional Requirements (2e)]]
- [[Ch 09 - The Trouble with Distributed Systems (2e)]] — the fault taxonomy in full
- [[Ch 06 - Replication (2e)]] — the primary fault-tolerance mechanism in this book
- 1st edition: [[Reliability]] — the same definition, differently organised
