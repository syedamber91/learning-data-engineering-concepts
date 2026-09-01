---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 9
chapter_title: The Trouble with Distributed Systems
type: chapter-moc
tags: [ddia2, distributed-systems, faults, networks, clocks, system-models, moc]
sources:
  - raw/ch09.md
---
# Ch 09 – The Trouble with Distributed Systems
Making a system reliable means ensuring it keeps working when things go wrong — **but anticipating all the possible faults and handling them is not easy.** It is very tempting to focus on the happy path and neglect faults, since they introduce a lot of edge cases. **If you want your system to be reliable in the presence of faults, you have to radically change your mindset and focus on what could go wrong, even though it may be unlikely.** It doesn't matter if the chance is one in a million: **in a large enough system, one-in-a-million events happen every day.** Experienced operators will tell you **anything that can go wrong will go wrong.**

**Working with distributed systems is fundamentally different from writing software on a single computer** — the main difference being that **things can go wrong in lots of new and exciting ways.** This chapter turns the pessimism up to maximum and explores what may go wrong: problems with networks, and clocks and timing issues. **The consequences are disorienting**, so it also explores how to think about the state of a distributed system and how to reason about fault tolerance.

## Map
- [[Faults and Partial Failures (2e)]] — why a single computer is either working or broken, and a distributed system is neither
- [[Unreliable Networks (2e)]] — asynchronous packet networks and the six ways a request/response can go wrong
  - [[The Limitations of TCP (2e)]] — "reliable" delivery, and what it still doesn't tell you
  - [[Network Faults in Practice (2e)]] — the studies, the cows, the beavers, the sharks
  - [[Fault Detection (2e)]] — the few explicit signals you get, and why you can't count on them
  - [[Timeouts and Unbounded Delays (2e)]] — how long should the timeout be, and queueing as the cause of variability
  - [[Synchronous Versus Asynchronous Networks (2e)]] — circuits, packet switching, and latency as a cost/benefit trade-off
- [[Unreliable Clocks (2e)]] — durations versus points in time, and why each machine disagrees
  - [[Monotonic Versus Time-of-Day Clocks (2e)]] — the two clocks, and which one to use for what
  - [[Clock Synchronization and Accuracy (2e)]] — drift, NTP, leap seconds, VMs, and untrusted devices
  - [[Relying on Synchronized Clocks (2e)]] — LWW's silent data loss, confidence intervals, and Spanner's TrueTime
  - [[Process Pauses (2e)]] — the lease-renewal bug, and eight reasons a thread stops for 15 seconds
- [[Knowledge, Truth, and Lies (2e)]] — what a node can actually know about the rest of the system
  - [[The Majority Rules (2e)]] — a node cannot trust its own judgment; quorums decide
  - [[Distributed Locks and Leases (2e)]] — zombies, delayed requests, and fencing tokens
  - [[Byzantine Faults (2e)]] — nodes that lie, when it matters, and weak forms of lying
  - [[System Model and Reality (2e)]] — timing and node-failure models, safety versus liveness
  - [[Formal Methods and Randomized Testing (2e)]] — model checking, fault injection, deterministic simulation

## Chapter Summary
The catalogue of problems: **a packet may be lost or arbitrarily delayed, and so may the reply — so if you don't get a reply you have no idea whether the message got through.** **A node's clock may be significantly out of sync despite NTP, may jump forward or back, and relying on it is dangerous because you most likely don't have a good measure of your clock's confidence interval.** **A process may pause for a substantial amount of time at any point in its execution**, be declared dead by others, and then come back to life unaware anything happened.

**Partial failures** — some parts of the system broken unpredictably while others work fine — **are the defining difficulty**, and they are **nondeterministic**: anything involving multiple nodes may sometimes work and sometimes unpredictably fail, and **you may not even know whether something succeeded.** **But if a system can tolerate partial failures, powerful possibilities open up**: rolling upgrades, and more generally **building a reliable system from unreliable components.**

The chapter's constructive half is about **knowing what you can know.** A node can learn another's state only by exchanging messages, and **if a remote node doesn't respond there is no way of knowing its state, because network problems cannot reliably be distinguished from node problems.** The answers: **quorums** rather than any single node's judgment; **fencing tokens** so that a zombie's delayed write is rejected rather than trusted; **system models** (partially synchronous, crash-recovery being the most useful combination) that state the assumptions an algorithm depends on; **safety and liveness** as the two kinds of property, where safety must hold in all situations and liveness may be conditioned on the network eventually recovering; and **formal methods and randomized testing** — model checking, fault injection, and deterministic simulation testing — to check that implementations actually behave.

## Since the 1st Edition
This is the 1st edition's Chapter 8, and its spine is intact: partial failures, unreliable networks, unreliable clocks, process pauses, and knowledge/truth/lies with the same fencing-token solution and the same system-model taxonomy.

**Genuinely new:** [[The Limitations of TCP (2e)]] as its own subtopic (the 1st edition assumed TCP knowledge); **[[Formal Methods and Randomized Testing (2e)]] as a full subtopic** covering TLA+/model checking, **Jepsen and chaos engineering**, and **deterministic simulation testing** with FoundationDB, TigerBeetle, Antithesis, and MadSim — none of which the 1st edition discussed; **Amazon ClockBound** alongside Spanner's TrueTime; the **"power of determinism" box** tying event sourcing, workflow engines, and state machine replication together; and modern GC discussion (ZGC, Shenandoah, Go's collector, and non-GC languages Swift/Rust/Mojo).

**Renamed and restructured:** the 1st edition's [[Knowledge, Truth, and Lies]] subtopic "The Truth Is Defined by the Majority" becomes [[The Majority Rules (2e)]], and its fencing-token material is expanded into a full [[Distributed Locks and Leases (2e)]] subtopic including **fencing with multiple replicas**. The 1st edition's "Monotonic Versus Time-of-Day Clocks" and clock material carry over largely unchanged. **Dropped:** the 1st edition's speculation about combining circuit and packet switching is compressed, and its detailed treatment of the fictitious bounded-delay network is trimmed.

## Related
- home: [[Home (2e)]] · previous: [[Ch 08 - Transactions (2e)]] · next: [[Ch 10 - Consistency and Consensus (2e)]]
- [[Ch 10 - Consistency and Consensus (2e)]] — the algorithms that work despite all of this
- [[Reliability and Fault Tolerance (2e)]] — the quality this chapter's faults threaten
- 1st edition: [[Ch 08 - The Trouble with Distributed Systems]] — the chapter this one revises
