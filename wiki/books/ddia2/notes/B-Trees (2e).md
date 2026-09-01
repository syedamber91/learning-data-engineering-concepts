---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 4
chapter_title: Storage and Retrieval
topic: Storage and Indexing for OLTP
type: subtopic
tags: [ddia2, b-tree, pages, page-split, wal, copy-on-write]
sources:
  - raw/ch04.md
---
# B-Trees
> Introduced in 1970, called "ubiquitous" within ten years, and still the standard index implementation in almost every relational database.

## The Idea
The log-structured approach is popular but not the only form of key-value storage. **The most widely used structure for reading and writing database records by key is the B-tree.** Like SSTables, B-trees keep key-value pairs sorted by key, allowing efficient lookups and range queries — but that is where the similarity ends, because the design philosophy is very different. Log-structured indexes break the database into **variable-size segments**, typically several megabytes or more, written once and then immutable. B-trees break the database into **fixed-size blocks or pages** and **may overwrite a page in place**. A page is traditionally 4 KiB, though PostgreSQL now uses 8 KiB and MySQL 16 KiB by default.

## How It Works
- Each page is identified by a **page number**, letting one page refer to another — like a pointer, but on disk. If all pages are in one file, page number × page size gives the byte offset. These references build a tree of pages.
- One page is the **root**; every lookup starts there. It holds several keys and references to child pages, each child responsible for a continuous key range, with the keys between references marking the boundaries. (This structure is sometimes called a **B+ tree**, but the book doesn't distinguish it from other variants.)
- Looking up key 251: follow the reference between boundaries 200 and 300, arriving at a page that further subdivides 200–300, and so on until reaching a **leaf page** containing individual keys, which either holds each key's value inline or references the page where the value lives.
- The number of child references in one page is the **branching factor** — in practice typically several hundred, depending on the space needed for page references and range boundaries.
- **Updating** an existing key means finding its leaf page and overwriting that page on disk with a version containing the new value. **Adding** a key means finding the page whose range encompasses it and inserting. If there isn't enough free space, the page **splits** into two half-full pages and the parent is updated with the new subdivision. Inserting key 334 into a full 333–345 page splits it into 333–337 (containing 334) and 337–345, with the parent gaining references to both children and a boundary of 337. If the parent lacks space for the new reference it may split too, **and splits can continue all the way to the root** — when the root splits, a new root is made above it. Deleting keys, which may require merging nodes, is more complex.
- This keeps the tree **balanced**: a B-tree with n keys always has depth O(log n). Most databases fit in a tree three or four levels deep, so few page references are followed. **A four-level tree of 4 KiB pages with branching factor 500 stores up to 250 TB.**

**Making B-trees reliable.** The basic write operation overwrites a page in place, assuming the overwrite doesn't change the page's location so all references to it stay intact — in stark contrast to log-structured indexes, which only append and eventually delete but never modify in place. Overwriting several pages at once, as in a page split, is **dangerous**: a crash after only some pages are written leaves a **corrupted tree** — an orphan page that is not a child of any parent, for instance. If the hardware can't atomically write an entire page you can also get a partially written page, known as a **torn page**.

The standard defence is an additional on-disk structure: a **write-ahead log (WAL)**, an append-only file to which every B-tree modification must be written *before* it is applied to the tree's pages. After a crash the log restores the B-tree to a consistent state. In filesystems the equivalent mechanism is **journaling**. For performance, implementations typically don't write every modified page to disk immediately but buffer pages in memory for a while; the WAL is what makes that safe. **As long as data has been written to the WAL and flushed with `fsync`, it is durable.**

## Trade-offs & Pitfalls
**B-tree variants** developed over the decades:
- Instead of overwriting pages and keeping a WAL, some databases (LMDB) use **copy-on-write**: a modified page is written to a different location and a new version of the parent pages is created pointing at it. This is also useful for concurrency control, which reappears in snapshot isolation.
- **Key abbreviation** saves space: especially in interior pages, keys need only enough information to act as boundaries between ranges. Packing more keys per page raises the branching factor and lowers the number of levels.
- Some implementations try to **lay out leaf pages sequentially on disk** to speed up in-order range scans and reduce seeks — but maintaining that order is difficult as the tree grows.
- **Sibling pointers** between leaf pages allow scanning keys in order without jumping back through parents.

## Examples & Systems
PostgreSQL (8 KiB pages), MySQL (16 KiB pages), LMDB (copy-on-write); filesystem journaling as the WAL analogue.

## Since the 1st Edition
Very close to the 1st edition's [[B-Trees]] — the same 1970 origin, page structure, split algorithm, branching factor, WAL, and variants. **Updated details:** the current default page sizes for PostgreSQL and MySQL (the 1st edition mostly said 4 KiB), and the worked capacity figure is now a four-level tree of 4 KiB pages with branching factor 500 storing 250 TB (the 1st edition's example gave 256 TB from slightly different parameters). Fractal trees, mentioned in the 1st edition's variant list, are dropped.

## Related
- up: [[Storage and Indexing for OLTP (2e)]] · chapter: [[Ch 04 - Storage and Retrieval (2e)]]
- [[Log-Structured Storage (2e)]] — the append-only rival
- [[Comparing B-Trees and LSM-Trees (2e)]] — which one wins, and on what axis
- [[Snapshot Isolation and Repeatable Read (2e)]] — where copy-on-write pays off again
- 1st edition: [[B-Trees]] — the same subtopic
