---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 9
chapter_title: The Trouble with Distributed Systems
topic: Knowledge, Truth, and Lies
type: subtopic
tags: [ddia2, byzantine, bft, blockchain, checksums, input-validation]
sources:
  - raw/ch09.md
---
# Byzantine Faults
> Fencing tokens stop a node acting in error. They do nothing against a node that deliberately sends a fake token. The book's standing assumption is that nodes are unreliable but honest.

## The Idea
**In this book we assume nodes are unreliable but honest.** They may be slow or never respond because of a fault, and their state may be outdated because of a GC pause or network delays, **but we assume that if a node does respond, it is telling the "truth" — to the best of its knowledge, it is playing by the rules of the protocol.**

**Distributed systems problems become much harder if nodes may "lie"** — send arbitrary faulty or corrupted responses, for example **casting multiple contradictory votes in the same election.** **Such behavior is a Byzantine fault, and reaching consensus in this untrusting environment is the Byzantine Generals Problem.**

> **The Byzantine Generals Problem** generalizes the **two generals problem**, in which two army generals at different camps must agree on a battle plan but can communicate only by messenger, and **the messengers sometimes get delayed or lost, like packets in a network.** In the Byzantine version, **n generals must agree while hampered by traitors in their midst**: most are loyal and send truthful messages, **but traitors may deceive and confuse the others with fake or untrue messages, and it is not known in advance who the traitors are.**
>
> **Byzantium was an ancient Greek city that became Constantinople, now Istanbul.** **There isn't any historic evidence that the generals of Byzantium were any more prone to intrigue than those elsewhere** — the name derives from *byzantine* in the sense of **excessively complicated, bureaucratic, devious**, used in politics long before computers. **Lamport wanted a nationality that would not offend any readers, and was advised that calling it The Albanian Generals Problem was not such a good idea.**

## How It Works
**A system is Byzantine fault-tolerant if it continues to operate correctly even if some nodes are malfunctioning and not obeying the protocol, or if malicious attackers are interfering.** This is relevant in specific circumstances:
- **Aerospace.** **Data in memory or a CPU register could be corrupted by radiation**, making a node respond in arbitrarily unpredictable ways. **Since a system failure would be very expensive** — an aircraft crashing, a rocket colliding with the ISS — **flight control systems must tolerate Byzantine faults.**
- **Multiple participating parties.** **Some participants may attempt to cheat or defraud others**, so it is not safe to trust another node's messages. **The consensus mechanisms underlying Bitcoin and other blockchain-based systems can be considered a way of getting mutually untrusting parties to agree on whether a transaction happened, without a central authority.**

## Trade-offs & Pitfalls
**In the kinds of systems this book discusses, we can usually safely assume there are no Byzantine faults.** In a datacenter **all nodes are controlled by your organization** (so they can hopefully be trusted), and **radiation levels are low enough that memory corruption is not a major problem** (although datacenters in orbit are being considered). **Multitenant systems have mutually untrusting tenants, but they are isolated via firewalls, virtualization, and access control policies — not Byzantine fault tolerance.** **Protocols for Byzantine fault tolerance are quite expensive**, and fault-tolerant embedded systems rely on hardware-level support; **in most server-side data systems the cost makes them impracticable.**

**Web applications do need to expect arbitrary and malicious behavior from clients under end-user control** — which is why **input validation, sanitization, and output escaping** matter, to prevent SQL injection and cross-site scripting. **But we typically don't use Byzantine fault-tolerant protocols here; we simply make the server the authority on what client behavior is allowed.** **In peer-to-peer networks, where there is no such central authority, Byzantine fault tolerance is more relevant.**

**A software bug could be regarded as a Byzantine fault, but if you deploy the same software to all nodes, a Byzantine fault-tolerant algorithm cannot save you.** **Most such algorithms require a supermajority of more than two-thirds of nodes to be functioning correctly** — so to use this against bugs **you would need four independent implementations of the same software and hope a given bug appears in only one.** **Similarly, protocols can't realistically protect against security compromises**: **if an attacker can compromise one node, they can probably compromise all of them, because the nodes are probably running the same software.** **Traditional mechanisms — authentication, access control, encryption, firewalls — continue to be the main protection against attackers.**

**Weak forms of lying.** Although we assume nodes are generally honest, **it can be worth guarding against weak forms of "lying" from hardware issues, software bugs, and misconfiguration.** **These are not full Byzantine fault tolerance — they would not withstand a determined adversary — but they are simple and pragmatic steps toward better reliability:**
- **Network packets do sometimes get corrupted** by hardware issues or bugs. **Usually caught by TCP and UDP checksums, but sometimes they evade detection.** **Checksums in the application-level protocol** are usually sufficient protection; **TLS-encrypted connections also offer protection against corruption.**
- **A publicly accessible application must carefully sanitize user input** — escaping characters to prevent SQL injection, checking values are in a reasonable range, **limiting string sizes to prevent denial of service through large memory allocations.** An internal service behind a firewall may get away with less strict checks, **but basic checks in protocol parsers are still a good idea.**
- **NTP clients can be configured with multiple server addresses**, contacting all of them, estimating errors, and **checking that a majority agree on a time range.** **As long as most servers are OK, a misconfigured one reporting incorrect time is detected as an outlier and excluded** — **making NTP more robust than using a single server.**

## Examples & Systems
Aerospace flight control; Bitcoin and blockchain consensus; TLS and application-level checksums; multi-server NTP with outlier rejection.

## Since the 1st Edition
Very close to the 1st edition's [[Byzantine Faults]] — the same Byzantine Generals framing with the same Albanian anecdote, the same aerospace and blockchain use cases, the same "same software means BFT can't help with bugs" argument, and the same three weak-lying defences. **Added:** the passing note that **datacenters in orbit are being considered**, which slightly undercuts the radiation argument for the future.

## Related
- up: [[Knowledge, Truth, and Lies (2e)]] · chapter: [[Ch 09 - The Trouble with Distributed Systems (2e)]]
- [[System Model and Reality (2e)]] — Byzantine faults as one node-failure model
- [[Distributed Locks and Leases (2e)]] — fencing, which assumes honesty
- 1st edition: [[Byzantine Faults]] — the same subtopic
