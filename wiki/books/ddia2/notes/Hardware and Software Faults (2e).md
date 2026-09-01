---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 2
chapter_title: Defining Nonfunctional Requirements
topic: Reliability and Fault Tolerance
type: subtopic
tags: [ddia2, hardware-faults, software-faults, redundancy, raid, availability-zones]
sources:
  - raw/ch02.md
---
# Hardware and Software Faults
> Hardware faults are frequent, mostly independent, and fixable with redundancy. Software faults are rarer, highly correlated, and the ones that take the whole system down.

## The Idea
Hardware comes to mind first when thinking about system failure, and the book gives real numbers rather than hand-waving.

## How It Works
**Hardware failure rates:**
- Roughly **2–5% of magnetic hard drives fail per year**. In a storage cluster with 10,000 disks, expect on average one disk failure per day. Recent data suggests disks are getting more reliable, but failure rates remain significant.
- Roughly **0.5–1% of SSDs fail per year**. Small numbers of bit errors are corrected automatically, but uncorrectable errors occur roughly once per year per drive, even in fairly new drives with little wear — a **higher error rate than magnetic hard drives**.
- Other components (power supplies, RAID controllers, memory modules) also fail, less frequently than hard drives.
- Roughly **1 in 1,000 machines has a CPU core that occasionally computes the wrong result**, likely from manufacturing defects. Sometimes an erroneous computation causes a crash; sometimes the program simply returns a wrong answer.
- RAM can be corrupted by random events such as cosmic rays or by permanent physical defects. Even with **ECC** memory, more than 1% of machines encounter an uncorrectable error in a given year, typically crashing the machine and requiring the module to be replaced. Certain pathological memory access patterns can also flip bits with high probability.
- An entire datacenter can become unavailable (power outage, network misconfiguration) or be permanently destroyed (fire, flood, earthquake). A solar storm — inducing large currents in long-distance wires when the sun ejects charged particles — could damage power grids and undersea network cables. Rare, but catastrophic for a service that cannot tolerate losing a datacenter.

At small scale these are rare enough to ignore if you can easily replace faulty hardware. **At large scale, hardware faults happen often enough that they become part of normal system operation.**

**Tolerating hardware faults through redundancy.** The first response is component-level redundancy: RAID configurations so a failed disk does not lose data, dual power supplies and hot-swappable CPUs, datacenter batteries and diesel generators. This can keep a machine running uninterrupted for years. Redundancy is most effective when component faults are **independent** — one fault not changing the likelihood of another — but experience shows significant correlations between component failures, and whole racks or datacenters still go down more often than we would like. So cloud systems tend to focus less on individual-machine reliability and more on making services highly available by **tolerating faulty nodes at the software level**. Cloud providers expose **availability zones** to identify which resources are physically co-located, since co-located resources are more likely to fail together. The book's fault-tolerance techniques are designed to survive the loss of entire machines, racks, or availability zones, generally by letting a machine in one datacenter take over when one in another fails or becomes unreachable. This also brings an operational benefit: a single-server system needs planned downtime to reboot for OS security patches, whereas a multi-node fault-tolerant system can be patched by restarting one node at a time — a **rolling upgrade**.

**Software faults.** Hardware failures are weakly correlated but mostly independent; software faults are often **very highly correlated**, because many nodes run the same software and therefore have the same bugs. They are harder to anticipate and cause many more system failures than uncorrelated hardware faults. Examples:
- A bug causing every node to fail simultaneously under particular circumstances. On **30 June 2012 a leap second** caused many Java applications to hang at once due to a Linux kernel bug, taking down several internet services. Because of a firmware bug, **all SSDs of certain models suddenly fail after exactly 32,768 hours** (under four years) of operation, rendering their data unrecoverable.
- A runaway process consuming a shared limited resource — CPU time, memory, disk space, network bandwidth, threads. A process using too much memory on a large request may be killed by the OS; a bug in a client library could produce far higher request volume than anticipated.
- A dependency service that slows down, becomes unresponsive, or returns corrupted responses.
- Emergent behaviour from interaction between systems that does not appear when each is tested in isolation.
- **Cascading failures**, where a problem in one component overloads and slows another, which brings down a third.

## Trade-offs & Pitfalls
- These bugs often lie dormant for a long time until triggered by unusual circumstances. What is revealed then is that the software was making an assumption about its environment — usually true, and eventually not.
- **There is no quick solution to systematic software faults.** Lots of small things help: carefully thinking about assumptions and interactions, thorough testing, process isolation, allowing processes to crash and restart, avoiding feedback loops such as retry storms, and measuring/monitoring/analysing behaviour in production.

## Examples & Systems
RAID, dual power supplies, hot-swappable CPUs, batteries and diesel generators (component redundancy); availability zones (correlated-failure grouping); rolling upgrades (operational payoff); the 2012 leap second and the 32,768-hour SSD firmware bug (correlated software faults).

## Since the 1st Edition
The 1st edition split this into [[Hardware Faults]] and [[Software Errors]]; the 2nd merges them into one subtopic precisely so the *contrast* — independent versus correlated — is the point rather than an aside. The failure statistics are substantially updated and expanded: SSD failure and uncorrectable-error rates, the 1-in-1,000 miscomputing CPU core, the ECC uncorrectable-error rate, Rowhammer-style pathological access patterns, and solar storms are all new. Availability zones and rolling upgrades are new here too. The 32,768-hour SSD bug is a post-2017 incident.

## Related
- up: [[Reliability and Fault Tolerance (2e)]] · chapter: [[Ch 02 - Defining Nonfunctional Requirements (2e)]]
- [[Humans and Reliability (2e)]] — the third fault category, and the largest in practice
- [[Byzantine Faults (2e)]] — what to do about nodes that lie rather than stop
- 1st edition: [[Hardware Faults]] and [[Software Errors]] — the two notes this one merges
