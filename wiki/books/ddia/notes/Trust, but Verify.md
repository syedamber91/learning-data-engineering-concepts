---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 12
chapter_title: The Future of Data Systems
topic: Aiming for Correctness
type: subtopic
tags: [ddia, auditing, data-corruption, merkle-trees]
sources:
  - raw/ch12.md
---
# Trust, but Verify

> System models treat faults as binary (can/can't happen), but reality is probabilistic — so mature systems audit their own data instead of blindly trusting hardware, databases, or their own code.

## The Idea
Every correctness argument rests on a *system model*: processes crash, networks drop messages — but fsync'd data survives, memory doesn't corrupt, CPUs multiply correctly. Kleppmann's challenge: those "can't happen" faults are merely *unlikely*, and at scale unlikely things happen. Disks corrupt data at rest; corruption sometimes slips past TCP checksums; crash reports he collected were only explicable by random memory bit-flips; rowhammer flips bits in *healthy* DRAM via pathological access patterns and breaks OS security with it. Rare, yes — but the model deserves probabilistic humility.

## How It Works
- **Software bugs evade checksums entirely.** Even MySQL has failed to maintain a uniqueness constraint, and PostgreSQL's serializable level has exhibited write-skew anomalies — in two of the most battle-tested databases. Application code fares worse, and many apps don't even use the integrity features databases offer. [[ACID]] consistency assumes bug-free transactions; use the database incorrectly (e.g. weak [[Isolation Levels]] used unsafely) and integrity silently dissolves.
- **Auditing** = checking data integrity. Finance leads not from sloppiness but because it admits mistakes happen. HDFS and Amazon S3 don't fully trust disks: background processes continually re-read files against replicas. To know data (or a backup) is intact you must actually read and check it — before restore-time.
- **A culture of verification.** ACID culture bred blind trust in the transaction mechanism, so auditability went uninvested; then NoSQL normalized weaker guarantees on less mature storage while the blind trust remained — more dangerous still. Kleppmann hopes for *self-validating* systems that continuously check their own integrity.
- **Designing for auditability.** A transaction that mutates several rows hides its *why*; the deciding application logic is transient. Event-sourced systems fare better: user input is one immutable event, state updates derive from it deterministically and reproducibly. Explicit [[Dataflow]] makes provenance clear — hash the event log to detect tampering, re-run (or redundantly run) derivations to re-check derived state, and gain time-travel debugging of why the system did something.
- **End-to-end checks** (see [[The End-to-End Argument for Databases]]): auditing a whole derived pipeline implicitly covers every disk, network, and algorithm inside it. Like automated tests, continuous integrity checking builds confidence to change systems faster.

## Trade-offs & Pitfalls
Self-audit is rare today; app-level audit tables can't guarantee their own integrity, and hardware-signed transaction logs don't prove the *right* transactions were logged. Distributed ledgers (Bitcoin, Ethereum, Ripple, Stellar) are relevant as mutually-untrusting replicas cross-checking integrity via [[Consensus]] — though Kleppmann doubts their [[Byzantine Faults]] emphasis, calls proof-of-work extraordinarily wasteful, and notes Bitcoin's low throughput. Merkle trees — hash trees proving a record's membership in a dataset — power the sober success story, certificate transparency for TLS certificates; scaling such auditing cheaply is the open problem.

## Examples & Systems
Rowhammer; MySQL uniqueness bug and PostgreSQL serializability bug; HDFS/S3 background scrubbing; Bitcoin/Ethereum/Ripple/Stellar; Merkle trees; certificate transparency.

## Related
- up: [[Aiming for Correctness]] · chapter: [[Ch 12 - The Future of Data Systems]]
- [[System Model and Reality]] — the fault assumptions being probabilistically loosened
- [[Byzantine Faults]] — the threat model distributed ledgers over-rotate on
- [[State, Streams, and Immutability]] — immutable event logs that make audit feasible
- [[Timeliness and Integrity]] — auditing is how integrity gets *verified*, not just hoped for
