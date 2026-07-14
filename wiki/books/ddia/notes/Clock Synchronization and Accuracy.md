---
book: Designing Data-Intensive Applications
part: Part II – Distributed Data
chapter: 8
chapter_title: The Trouble with Distributed Systems
topic: Unreliable Clocks
type: subtopic
tags: [ddia, ntp, clock-drift, leap-seconds, ptp]
sources:
  - raw/ch08.md
---
# Clock Synchronization and Accuracy
> Quartz drifts, NTP wobbles with network delay, leap seconds crash systems, and VM clocks jump — accurate time is achievable only with money, GPS hardware, and vigilance.

## The Idea
Time-of-day clocks are only useful if set from an external source, usually NTP. But the whole pipeline — local quartz, network, NTP servers — is fallible, and its failure modes are quieter and stranger than most engineers expect.

## How It Works
The catalog of failure modes:
- **Quartz drift.** A computer's crystal runs fast or slow, varying with temperature. Google budgets 200 ppm (parts per million) of drift for its servers — that is 6 ms of error between 30-second resyncs, or 17 seconds if you resync only daily. Drift bounds your best-case accuracy even when everything works.
- **Step resets.** A clock too far from the NTP server may refuse to sync or be forcibly reset — observers see time leap forward or backward.
- **Silent misconfiguration.** A node firewalled off from NTP can drift unnoticed for a long time; this genuinely happens.
- **Network limits.** NTP accuracy is capped by round-trip delay: about 35 ms minimum error over the internet in one experiment, spiking to around a second under congestion; big delays can make the client give up entirely.
- **Bad servers.** Some NTP servers report time wrong by hours. Clients defend themselves by querying several servers and discarding outliers — betting correctness on strangers' clocks is uncomfortable regardless.
- **Leap seconds.** A minute can legally have 59 or 61 seconds, breaking naive timing assumptions; leap seconds have crashed many large systems. The pragmatic fix is *smearing* — spreading the extra second across a day so no discontinuity appears — though server behavior varies.
- **Virtualized clocks.** In VMs the hardware clock is virtualized; when a CPU core is shared, each VM freezes for tens of milliseconds while others run, seen by applications as the clock lurching forward.
- **Untrusted devices.** On phones and embedded hardware, users may deliberately set clocks wrong (e.g., to cheat game timers) — assume nothing.

## Trade-offs & Pitfalls
High accuracy is buyable: MiFID II draft regulation requires high-frequency trading funds to keep clocks within 100 microseconds of UTC so flash crashes and market manipulation can be forensically reconstructed. The tools are GPS receivers, the Precision Time Protocol (PTP), and careful deployment plus monitoring — but it takes real expertise, and one misconfigured daemon or NTP-blocking firewall lets drift balloon. The trap: clock error is invisible until it costs you data.

## Examples & Systems
Google's 200 ppm drift budget; the 35 ms internet-NTP floor; hours-wrong public NTP servers; leap-second outages and Google-style smearing; MiFID II's 100 µs mandate; GPS + PTP deployments.

## Related
- up: [[Unreliable Clocks]] · chapter: [[Ch 08 - The Trouble with Distributed Systems]]
- [[Monotonic Versus Time-of-Day Clocks]] — sibling: which clock these failures poison
- [[Relying on Synchronized Clocks]] — sibling: what breaks when you trust anyway
- [[Clock Skew]] — the cross-node divergence these mechanisms produce
- [[Byzantine Faults]] — multi-server NTP outlier rejection as weak-lie defense
