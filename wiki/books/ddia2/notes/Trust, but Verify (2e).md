---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 13
chapter_title: A Philosophy of Streaming Systems
topic: Aiming for Correctness
type: subtopic
tags: [ddia2, auditing, auditability, merkle-tree, certificate-transparency, integrity-checking]
sources:
  - raw/ch13.md
---
# Trust, but Verify
> System models treat faults as binary — this can happen, that can't. Reality is probabilistic. At large enough scale, even very unlikely things do happen.

## The Idea
**All the discussion of correctness, integrity, and fault tolerance has assumed that certain things might go wrong but other things won't — the system model.** **We assume processes can crash, machines can lose power, and the network can arbitrarily delay or drop messages. We might also assume that data written to disk is not lost after `fsync`, that data in memory is not corrupted, and that the CPU's multiplication instruction always returns the correct result.**

**These assumptions are quite reasonable, as they are true most of the time, and it would be difficult to get anything done if we had to constantly worry about our computers making mistakes.** **Traditionally, system models take a binary approach: some things can happen, others can never.** **In reality it is more a question of probabilities: some things more likely, others less.** **The question is whether violations happen often enough that we may encounter them in practice.**

**We have seen that data can become corrupted in memory, on disk, and on the network.** **Maybe this is something we should be paying more attention to? If you are operating at large enough scale, even very unlikely things do happen.**

## How It Works
**Maintaining integrity in the face of software bugs.** **Besides hardware issues there is always the risk of software bugs, which would not be caught by lower-level network, memory, or filesystem checksums.** **Even widely used database software has bugs** — **past versions of MySQL have failed to correctly maintain uniqueness constraints, and PostgreSQL's serializable isolation level has exhibited write skew anomalies** — **even though both are robust, well-regarded databases battle-tested by many people for many years. In less mature software the situation is likely much worse.**

**Despite considerable efforts in careful design, testing, and review, bugs still creep in.** **Although rare, and eventually found and fixed, there is still a period during which such bugs can corrupt data.**

**With application code we must assume many more bugs**, since most applications don't receive anywhere near the review and testing database code does. **Many applications don't even correctly use the features databases offer for preserving integrity, such as foreign-key or uniqueness constraints.**

**ACID consistency is based on the idea that the database starts in a consistent state and a transaction transforms it to another consistent state** — **but this makes sense only if we assume the transaction is free from bugs.** **If the application uses the database incorrectly — using a weak isolation level unsafely — the integrity of the database cannot be guaranteed.**

**Don't just blindly trust what they promise.** **With both hardware and software not always living up to our ideals, data corruption seems inevitable sooner or later.** **So we should at least have a way of finding out if data has been corrupted so we can fix it and track down the source. Checking the integrity of data is known as auditing.**

**Auditing is not just for financial applications** — **but auditability is very important in finance precisely because everyone knows mistakes happen, and we all recognize the need to detect and fix problems.**

**Mature systems consider the possibility of unlikely things going wrong and manage that risk.** **Large-scale storage systems such as HDFS and Amazon S3 do not fully trust disks: they run background processes that continually read back files, compare them to other replicas, and move files from one disk to another, mitigating the risk of silent corruption.**

**If you want to be sure your data is still there, you have to read it and check.** **Most of the time it will still be there, but if it isn't you want to find out sooner rather than later.** **By the same argument, it is important to try restoring from your backups from time to time — otherwise you may find out your backup is broken when it is too late and you have already lost data. Don't just blindly trust that it is all working.**

**HDFS and S3 still assume disks work correctly most of the time — a reasonable assumption, but not the same as assuming they always work correctly.** **Not many systems currently have this kind of "trust, but verify" approach of continually auditing themselves.** **Many assume correctness guarantees are absolute and make no provision for rare data corruption.** **In the future we may see more self-validating or self-auditing systems that continually check their own integrity rather than rely on blind trust.**

**Designing for auditability.** **If a transaction mutates several objects, the underlying reason can be difficult to tell after the fact.** **Even capturing the transaction logs, the insertions, updates, and deletions do not necessarily give a clear picture of why those mutations were performed** — **the invocation of the application logic that decided on them is transient and cannot be reproduced.**

**Event-based systems provide better auditability.** **In event sourcing, user input is a single immutable event and any resulting state updates are derived from it.** **The derivation can be made deterministic and repeatable, so running the same log through the same version of the derivation code produces the same state updates.**

**Being explicit about dataflow makes the provenance of data much clearer, which makes integrity checking much more feasible.** **For the event log we can use hashes to check the storage has not been corrupted.** **For any derived state we can rerun the batch and stream processors to check whether we get the same result, or even run a redundant derivation in parallel.**

**A deterministic, well-defined dataflow also makes it easier to debug and trace execution to determine why a system did something.** **If something unexpected occurred, it is valuable to be able to reproduce the exact circumstances — a kind of time-travel debugging capability.**

## Trade-offs & Pitfalls
**The end-to-end argument again.** **If we cannot fully trust that every component is free from corruption — every piece of hardware fault-free and every piece of software bug-free — then we must at least periodically check the integrity of our data.** **If we don't check, we won't find out about corruption until it is too late and it has caused downstream damage, at which point it will be much harder and more expensive to track down.**

**Checking is best done end to end.** **The more systems included in an integrity check, the fewer opportunities for corruption to go unnoticed.** **If we can check that an entire derived data pipeline is correct end to end, then any disks, networks, services, and algorithms along the path are implicitly included.**

**Continuous end-to-end integrity checks give increased confidence about correctness, which in turn allows you to move faster.** **Like automated testing, auditing increases the chances bugs will be found quickly and reduces the risk that a change or a new storage technology will cause damage.** **If you are not afraid of making changes, you can much better evolve an application to meet changing requirements.**

**Tools for auditable data systems.** **At present, not many data systems make auditability a top-level concern.** **Some applications implement their own — logging all changes to a separate audit table — but guaranteeing the integrity of the audit log and the database state is still difficult.** **A transaction log can be made tamper-proof by periodically signing it with a hardware security module, but that does not guarantee the right transactions went into the log in the first place.**

**Blockchains such as Bitcoin and Ethereum are shared append-only logs with cryptographic consistency checks**: **the transactions they store are events, and smart contracts are basically stream processors.** **Their consensus protocols ensure all nodes agree on the same sequence of events.** **The difference from Chapter 10's consensus protocols is that blockchains are Byzantine fault-tolerant — they still work if some participating nodes have corrupted data, because the replicas continually check one another's integrity.**

**For most applications blockchains have too high an overhead to be useful.** **However, some of their cryptographic tools can be used in a lighter-weight context.** **Merkle trees are trees of hashes that can efficiently prove that a record appears in a dataset.** **Certificate transparency uses cryptographically verified append-only logs and Merkle trees to check the validity of TLS/SSL certificates — avoiding the need for a consensus protocol by having a single leader per log.**

**Integrity-checking and auditing algorithms like those of certificate transparency and distributed ledgers might become more widely used in data systems in general in the future.** **Some work will be needed to make them as scalable as systems without cryptographic auditing and to keep the performance penalty low, but they are nevertheless interesting.**

## Examples & Systems
HDFS and S3 background integrity scans; MySQL uniqueness-constraint bugs and PostgreSQL serializable write skew as real database defects; Merkle trees; certificate transparency; Bitcoin and Ethereum as Byzantine fault-tolerant append-only logs.

## Since the 1st Edition
Essentially unchanged from the 1st edition's [[Trust, but Verify]] — the same probabilistic-versus-binary framing of system models, the same real database bugs, the same HDFS/S3 self-auditing examples, the same designing-for-auditability argument, and the same discussion of Merkle trees and certificate transparency. Notably, the 1st edition's slightly warmer treatment of blockchains as an emerging idea is trimmed to a more measured "too high an overhead to be useful" for most applications.

## Related
- up: [[Aiming for Correctness (2e)]] · chapter: [[Ch 13 - A Philosophy of Streaming Systems (2e)]]
- [[System Model and Reality (2e)]] — the assumptions being questioned
- [[Byzantine Faults (2e)]] — the fault model blockchains tolerate
- [[State, Streams, and Immutability (2e)]] — auditability as an advantage of immutable events
- 1st edition: [[Trust, but Verify]] — the same subtopic
