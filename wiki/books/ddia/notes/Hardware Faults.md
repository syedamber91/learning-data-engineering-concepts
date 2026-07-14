---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 1
chapter_title: Reliable, Scalable, and Maintainable Applications
topic: Reliability
type: subtopic
tags: [ddia, hardware-faults, redundancy, fault-tolerance]
sources:
  - raw/ch01.md
---
# Hardware Faults
> Individual machines fail randomly and constantly at scale, so systems have shifted from hardware redundancy toward software techniques that survive the loss of whole machines.

## The Idea
Disks crash, RAM goes bad, power grids black out, and someone yanks the wrong cable — in a large datacenter this is background noise, not an anomaly. The scale math makes it unavoidable: with a mean time to failure of roughly 10–50 years per hard disk, a cluster of 10,000 disks should expect about one disk death *every single day*. Hardware faults have a redeeming property, though: they are mostly random and independent — one machine's disk dying says nothing about its neighbor's (aside from weak shared-cause correlations like rack temperature). That independence is what makes them tractable.

## How It Works
The classic defense is redundancy at the component level: RAID arrays for disks, dual power supplies and hot-swappable CPUs in servers, batteries and diesel generators backing the datacenter's power. When one part dies, its twin carries the load while a replacement is fitted. This doesn't eliminate failures, but it makes total single-machine failure rare enough that, combined with reasonably quick backup restores, it satisfied most applications for a long time; only genuinely high-availability services needed multiple machines.

Two forces changed that. Growing data and compute demands push applications onto many machines, which proportionally multiplies the fault rate. And cloud platforms like AWS routinely kill virtual machine instances without notice, because they optimize for elasticity and flexibility over the reliability of any single box. The modern answer is *software* fault-tolerance — designing the system so it keeps running when an entire machine disappears — used alongside or instead of hardware redundancy.

## Trade-offs & Pitfalls
- Hardware redundancy protects a machine, not a system: it cannot help when the platform itself withdraws your VM.
- Single-server designs need planned downtime for every OS patch or reboot; machine-tolerant systems can patch one node at a time (a rolling upgrade — see [[Ch 04 - Encoding and Evolution]]), an operational win beyond fault-tolerance.
- Redundancy budgets assume independence; correlated hardware failures (shared power, shared racks) can defeat it.

## Examples & Systems
- The 10,000-disk cluster losing ~1 disk/day (from MTTF studies of large storage fleets, e.g. Google's and Backblaze's published data).
- AWS as the canonical platform where instances vanish without warning.
- RAID, dual PSUs, hot-swap CPUs, and generator-backed datacenters as the standard redundancy toolkit.

## Related
- up: [[Reliability]] · chapter: [[Ch 01 - Reliable, Scalable, and Maintainable Applications]]
- [[Software Errors]] — the correlated, systematic counterpart to random hardware faults
- [[Handling Node Outages]] — Ch 5: replication as software machine-tolerance
- [[Replication]] — core technique for surviving machine loss
