---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 8
chapter_title: The Trouble with Distributed Systems
topic: Knowledge, Truth, and Lies
type: subtopic
tags: [ddia, byzantine-fault-tolerance, security, blockchain]
sources:
  - raw/ch08.md
---
# Byzantine Faults
> When nodes may deliberately lie — sending fake or corrupted responses — you are in Byzantine territory; this book assumes honest-but-unreliable nodes, which is realistic for single-organization datacenters but not for aerospace or blockchains.

## The Idea
[[Fencing Tokens]] stop a node that errs *innocently* — one that has not yet learned its lease expired. They are useless against a node that wants to cheat: it can simply forge a higher token. This book's standing assumption is that nodes are unreliable but honest: they may be slow, silent, or stale, but when they do respond, they report their genuine best knowledge and follow the protocol. Drop that assumption — allow nodes to claim receipt of messages they never got, or send arbitrary corrupted responses — and you have a *Byzantine fault*. Reaching agreement among mutually distrustful participants is the Byzantine Generals Problem.

## How It Works
The problem generalizes the Two Generals Problem (two commanders coordinating an attack via messengers who may be lost or delayed — the consensus kernel revisited in Ch 9). In the Byzantine version, *n* generals must agree while some unknown subset are traitors sending contradictory or false messages while evading detection. (The name comes from "byzantine" as a byword for convoluted intrigue — Lamport reportedly picked a safely historical nationality.) A system is Byzantine fault-tolerant if it keeps operating correctly despite malfunctioning, protocol-violating nodes or attacker interference. It matters in two real settings: aerospace, where radiation can corrupt memory or CPU registers into arbitrary behavior and a failure means a crashed aircraft, so flight control systems must tolerate Byzantine faults with hardware support; and multi-organization systems where participants may try to defraud one another — Bitcoin and other blockchains are essentially machinery for mutually distrusting parties to agree whether a transaction happened without a central authority.

## Trade-offs & Pitfalls
For datacenter systems, BFT is usually the wrong tool: all nodes belong to one organization, radiation is negligible, the protocols are complex, and hardware-supported variants are impractical for server-side data systems. BFT cannot save you from software bugs if every node runs the same code — most algorithms need a supermajority (more than two-thirds functioning; at most 1 faulty of 4), so you would need four independent implementations and hope only one is buggy. Nor does it protect against compromise: an attacker who takes one node can likely take them all, since they run the same software — so authentication, access control, encryption, and firewalls remain the real defenses. Web servers face genuinely arbitrary client behavior but respond with server-side authority (input validation, sanitization, escaping against SQL injection and XSS), not BFT protocols. **Weak forms of lying** are worth guarding against cheaply: packets corrupted despite TCP/UDP checksums argue for application-level checksums; public-facing inputs need range checks and size limits against denial of service; NTP clients query multiple servers and discard outliers, robustly detecting one misconfigured server.

## Examples & Systems
Flight control systems; Bitcoin and peer-to-peer blockchains; the Two Generals and Byzantine Generals problems; TCP/UDP checksum escapes; multi-server NTP outlier rejection.

## Related
- up: [[Knowledge, Truth, and Lies]] · chapter: [[Ch 08 - The Trouble with Distributed Systems]]
- [[The Truth Is Defined by the Majority]] — sibling: defenses that assume honesty
- [[System Model and Reality]] — sibling: Byzantine as the harshest node-failure model
- [[Fault-Tolerant Consensus]] — Ch 9 consensus in the non-Byzantine setting
- [[Consensus]] — the agreement problem the generals dramatize
