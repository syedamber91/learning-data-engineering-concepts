---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 6
chapter_title: Replication
topic: Multi-Leader Replication
type: subtopic
tags: [ddia2, conflict-resolution, lww, crdt, operational-transformation, siblings]
sources:
  - raw/ch06.md
---
# Dealing with Conflicting Writes
> Two users rename the same wiki page at the same time. Something has to give: a write, a user's attention, or your assumption that merging is easy.

## The Idea
**The biggest problem with multi-leader replication** — in a geo-distributed server database and in a local-first sync engine alike — **is that concurrent writes on different leaders can lead to conflicts that need resolving**. User 1 changes a page title from A to B while user 2 independently changes it from A to C; each change succeeds on its local leader, and the conflict is detected only when the changes replicate. **This problem does not occur in a single-leader database.**

> The two writes are called **concurrent** because **neither was aware of the other at the time it was made**. It doesn't matter whether they literally happened at the same time — if made offline they might be some time apart. **What matters is whether one write occurred in a state where the other had already taken effect.**

## How It Works
**Conflict avoidance.** Prevent conflicts from occurring at all: **if the application ensures all writes for a particular record go through the same leader**, conflicts cannot occur even in a multi-leader database. **This is not possible for a sync engine client updated offline**, but is sometimes possible in geo-replicated server systems. In an application where a user edits only their own data, route that user's requests always to the same region and use that region's leader — different users may have different "home" regions picked by geographic proximity, **but from any one user's point of view the configuration is essentially single-leader**.

**However, conflict avoidance breaks down if you allow the leader to be changed.** You may want to change a record's designated leader — a region is unavailable and traffic must be rerouted, or a user has moved closer to another region — and there is then a **risk the user writes while the change of designated leader is in progress**, producing a conflict anyway.

A second avoidance example: generating unique IDs from an autoincrementing counter across two leaders by having **one generate only odd numbers and the other only even numbers**.

**Last write wins (LWW).** Attach a timestamp to each write and always use the value with the greatest timestamp; ties broken by comparing values (for strings, taking the one earlier in the alphabet). **The term is misleading**, because when two writes are concurrent **which one is most recent is undefined, so the timestamp order of concurrent writes is essentially random**. So **the real meaning of LWW is: when the same record is concurrently written on different leaders, one write is randomly chosen to win and the others are silently discarded, even though they were successfully processed by their leaders.** This achieves eventual consistency **at the cost of data loss**. If you can avoid conflicts — only inserting records with a unique key and never updating them — LWW is no problem; but if you update existing records, or different leaders may insert the same key, **you have to decide whether lost updates are acceptable**. A second problem: **if a real-time clock is used for timestamps, the system becomes very sensitive to clock synchronization** — a node whose clock runs ahead can cause your later write to be ignored. **Using a logical clock solves this.**

**Manual conflict resolution.** Familiar from Git: edits to the same lines of the same file on two branches produce a merge conflict a human must resolve. **In a database it would be impractical for a conflict to halt replication until a human intervenes**, so databases typically **store all the concurrently written values — called siblings** — and return them all on the next read. You then resolve them however you want: automatically in application code (concatenating B and C into B/C) or by asking the user, then writing back a resolved value. **CouchDB** works this way. Its problems:
- **The API of the database changes** — a title that was a string becomes a set of strings, usually with one element, sometimes more. **This can make the data awkward to work with.**
- **Asking the user to merge is a lot of work** for the developer (building a conflict-resolution UI) and for the user (who may be confused about what they're being asked and why). Often it's better to merge automatically than to bother the user.
- **Automatic merging can surprise you if done carelessly.** Amazon's shopping cart used to merge siblings by **taking the set union of the carts** — so if a customer removed an item in one sibling but another sibling still contained it, **the removed item would unexpectedly reappear**. In the book's figure, device 1 removes Book and device 2 concurrently removes DVD, and after merging **both items are back**.
- **Concurrent resolution can create new conflicts.** If multiple nodes observe the conflict and resolve it concurrently, the resolutions may themselves be inconsistent — one node merging B and C into B/C, another into C/B — and merging *those* may yield **B/C/C/B or something similarly surprising**.

**Automatic conflict resolution.** For many applications the best answer is an algorithm that **automatically merges concurrent writes into a consistent state**, ensuring all replicas that have processed the same set of writes reach the same state **regardless of arrival order**. Combining eventual consistency with such a convergence guarantee is **strong eventual consistency**. LWW is a trivial example; more sophisticated merge algorithms exist per datatype, aiming to preserve the intended effect of all updates and avoid data loss:
- **Text** — detect which characters were inserted or deleted between versions; the merged result preserves all insertions and deletions from any sibling, and concurrent insertions at the same position are **ordered deterministically** so all nodes get the same outcome.
- **Collections** (ordered like a to-do list, unordered like a shopping cart) — merged like text by tracking insertions and deletions. **This is what fixes the Amazon cart problem**: the algorithms track that Book and DVD were deleted, so the merged result is `Cart = {Soap}`.
- **Counters** (likes on a post) — the algorithm counts increments and decrements on each sibling and adds them correctly, so the result **neither double-counts nor drops updates**.
- **Key-value mappings** — merge updates to the same key with one of the other algorithms; updates to different keys are handled independently.

**CRDTs and operational transformation.** Two algorithm families implement automatic resolution: **conflict-free replicated datatypes (CRDTs)** and **operational transformation (OT)**. They differ in design philosophy and performance but both handle all the above datatypes. Merging a concurrent prepend of `n` and append of `!` to `ice` to get `nice!`:
- **OT** records the index at which characters are inserted or deleted — `n` at index 0, `!` at index 3. The replicas exchange operations; the insertion of `n` at 0 applies as-is, but **applying `!` at index 3 to the state `nice` would give `nic!e`, which is wrong**. So each operation's index must be **transformed** to account for concurrent operations already applied — `!` becomes index 4.
- **CRDTs** give each character a **unique, immutable ID** and use those instead of indexes. Assign `1A` to `i`, `2A` to `c`, and so on; inserting the exclamation mark generates an operation containing the new character's ID (`4B`) and **the ID of the existing character after which to insert it** (`3A`). Inserting at the beginning uses nil as the preceding ID. **Concurrent insertions at the same position are ordered by character ID**, so replicas converge **without any transformation**.

Lists and arrays work the same way with list elements instead of characters, and other datatypes such as key-value maps are easily added. The two families have performance and functionality trade-offs, **but it is possible to combine the advantages of both in one algorithm**. **OT is most often used for real-time collaborative text editing, such as Google Docs; CRDTs appear in distributed databases such as Redis Enterprise, Riak, and Azure Cosmos DB.** JSON sync engines exist in both flavours — **Automerge and Yjs** (CRDT), **ShareDB** (OT).

## Trade-offs & Pitfalls
- **There are limits to automatic resolution.** If you want to enforce that a list contains no more than five items and multiple users concurrently push it over five, **your only option is to drop some items.** Nevertheless automatic resolution is sufficient for many useful apps — and if you start from wanting a collaborative offline-first or local-first app, **conflict resolution is inevitable and automating it is often the best approach.**
- **Some conflicts are subtle to detect.** A meeting room booking system inserts a new record per booking rather than updating a field, and must ensure no overlapping bookings for the same room. **Even if the application checks availability before allowing a booking, a conflict can arise if two bookings are made close enough together that both see the room as unbooked before inserting.** The book admits there is no quick ready-made answer and defers to later chapters.

## Examples & Systems
CouchDB (siblings); Amazon's shopping cart union anomaly; Google Docs (OT); Redis Enterprise, Riak, Azure Cosmos DB (CRDTs); Automerge, Yjs (CRDT sync engines); ShareDB (OT).

## Since the 1st Edition
The 1st edition's [[Handling Write Conflicts]] covered conflict avoidance, converging toward a consistent state (including LWW and its data loss), and custom conflict resolution logic, and mentioned CRDTs, mergeable persistent data structures, and OT briefly in a "what is a conflict?" coda. **The 2nd edition renames it and substantially deepens it**: automatic conflict resolution becomes a named goal with **strong eventual consistency**; the four datatype families are enumerated; and **CRDTs and OT get a full worked comparison** with the `nice!` merge example showing exactly how index transformation differs from immutable character IDs. The Amazon cart anomaly and the meeting-room example are retained.

## Related
- up: [[Multi-Leader Replication (2e)]] · chapter: [[Ch 06 - Replication (2e)]]
- [[Detecting Concurrent Writes (2e)]] — how the database knows two writes conflict
- [[Sync Engines and Local-First Software (2e)]] — the applications that need this most
- [[ID Generators and Logical Clocks (2e)]] — the fix for LWW's clock sensitivity
- 1st edition: [[Handling Write Conflicts]] — the same subtopic under its old name
