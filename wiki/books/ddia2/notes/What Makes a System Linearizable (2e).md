---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 10
chapter_title: Consistency and Consensus
topic: Linearizability
type: subtopic
tags: [ddia2, register, cas, serializability, strict-serializability]
sources:
  - raw/ch10.md
---
# What Makes a System Linearizable?
> Once any one read has returned the new value, every later read must too. That single extra constraint is what turns "eventually" into "atomically."

## The Idea
Three clients concurrently read and write the same object **x** in a linearizable database. In distributed systems theory **x is called a register** — in practice one key in a key-value store, one row, or one document. Two operation types:
- **`Read(x) ⇒ v`** — the client requested x's value and the database returned **v**.
- **`Write(x, v) ⇒ r`** — the client requested setting x to **v**, and the database returned **r** (OK or Error).

**Because of variable network delays, a client doesn't know exactly when the database processed its request** — only that it happened sometime between sending and receiving.

x starts at 0, client C writes 1, and clients A and B poll:
- **A's first read completes before the write begins, so it must return 0.**
- **A's last read begins after the write completes, so it must return 1.**
- **Reads overlapping the write may return either 0 or 1**, since we don't know whether the write had taken effect. **These are concurrent with the write.**

**But that isn't sufficient.** If concurrent reads could return either value freely, **readers could see the value flip back and forth between old and new several times during a write — not what we expect of a system emulating a single copy.**

**So we add a constraint: there must be some point in time at which x atomically flips from 0 to 1. Thus if one client's read returns the new value, all subsequent reads must also return the new value, even if the write hasn't completed.** If A is first to read 1 and B begins a read strictly after A's returns, **B must also return 1** — the same situation as Aaliyah and Bryce.

## How It Works
Adding a third operation type — **`CAS(x, v_old, v_new) ⇒ r`**, an atomic compare-and-set — the book marks each operation with **a vertical line at the moment it appears to have taken effect**, joins the markers in sequential order, and requires the result to be **a valid sequence of reads and writes** (every read returns the value set by the most recent write). **The requirement of linearizability is that the lines joining the markers always move forward in time, never backward** — which is exactly the recency guarantee.

Four details worth noticing in the worked example:
- **B sent a read, then D sent a write of 0, then A sent a write of 1 — and B's read returns 1.** **This is OK**: the database processed D's write, then A's write, then B's read. **Not the order requests were sent, but an acceptable order, because the three requests are concurrent** — perhaps B's read was delayed in the network.
- **B's read returned 1 before A received its OK response.** **Also OK** — the response to A was just delayed.
- **The model assumes no transaction isolation**: another client may change a value at any time. C reads 1 then reads 2 because B changed it in between. **An atomic CAS can check the value hasn't been concurrently changed** — B and C's CAS requests succeed, **D's fails** because by the time it is processed x is no longer 0.
- **The final read by B is not linearizable.** It is concurrent with C's CAS updating x from 2 to 4, and **in isolation returning 2 would be fine — but A had already read 4 before B's read started, so B is not allowed to read an older value than A.**

## Trade-offs & Pitfalls
**Linearizability versus serializability.** Easily confused, since both suggest "can be arranged in a sequential order," **but they are quite different guarantees:**
- **Serializability** is a **transaction isolation level** where every transaction may read and write **multiple objects**. It guarantees transactions behave as if executed in **some serial order** — and **it is OK for that order to differ from the order they actually ran in.**
- **Linearizability** is a guarantee on **reads and writes of a single register.** It **doesn't group operations into transactions, so it does not prevent write skew.** But **it is a recency guarantee**: if one operation finishes before another starts, the later one must observe a state at least as new. **Serializability does not have that requirement — stale reads are allowed by serializability.**

**A database may provide both, a combination known as strict serializability or strong one-copy serializability (strong-1SR).** **Single-node databases are typically linearizable.** With distributed databases using optimistic methods like SSI it's more complicated: **CockroachDB provides serializability and some recency guarantees but not strict serializability**, because that would require expensive coordination between transactions; **Spanner and FoundationDB do offer strict serializability.**

**It is also possible to combine a weaker isolation level with linearizability, or a weaker consistency model with serializability — in fact the consistency model and isolation level can be chosen largely independently of each other.** (*Sequential consistency is something else again, and the book doesn't discuss it.*)

## Examples & Systems
CockroachDB (serializable, not strictly); Spanner and FoundationDB (strictly serializable).

## Since the 1st Edition
Very close to the 1st edition's [[What Makes a System Linearizable]] — the same register model, the same worked timing diagrams, and the same linearizability-versus-serializability box. **Added:** the concrete positioning of **CockroachDB, Spanner, and FoundationDB** on the strict-serializability question, and the explicit statement that **consistency model and isolation level are largely independent choices** — the 1st edition mentioned the combination but not the independence.

## Related
- up: [[Linearizability (2e)]] · chapter: [[Ch 10 - Consistency and Consensus (2e)]]
- [[Serializability (2e)]] — the guarantee this is confused with
- [[Write Skew and Phantoms (2e)]] — what linearizability does *not* prevent
- 1st edition: [[What Makes a System Linearizable]] — the same subtopic
