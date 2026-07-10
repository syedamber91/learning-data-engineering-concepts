---
persona: alex
kind: concept
sources:
- vutr/page-cache-sequential-io-and-zero-copy
last_updated: '2026-07-10'
qc: passed
slug: 002-page-cache-sequential-io-and-zero-copy
topics:
- kafka
learner: alex
source_note: page-cache-sequential-io-and-zero-copy
mastery: mastered
---

*What Alex understood:* Okay, let me try to rebuild this. The whole thing rests on one flip in my head: I assumed disk is just always slower than RAM, but that's only true when you're jumping around randomly — like flipping to random pages in a book. If you read or write straight through, front to back, the disk actually keeps up or even beats memory. So Kafka bends over backwards to only ever go front-to-back.

For writing, a partition is just a giant log split into ~1GB chunk files, and Kafka only ever writes to the *end* of the current chunk — like always adding a new line at the bottom of a notebook, never inserting in the middle. That's automatically sequential. For reading, each consumer walks the log in order, and messages don't even have real IDs, just an offset (a position number). To find the next message you take your current position and add the current message's length — like knowing the next word starts right after this one ends — so Kafka doesn't have to keep a big lookup table mapping IDs to locations.

The caching part is the sneaky bit: Kafka refuses to hold messages in its own Java memory. Instead it dumps everything to the OS's page cache — the OS grabbing spare RAM to remember recent disk data. Kafka does this partly to dodge Java's garbage collector getting sluggish with tons of objects, and partly to keep its own code simple. And if the machine needs that RAM back, the kernel just reclaims it, so it's a free loan.

Then zero-copy: I originally thought it meant literally no copying, but it actually means no *wasteful* copying. Normally sending a file out means bouncing it disk → cache → app → socket → network card, four copies and four trips across the user/kernel border. `sendfile()` lets the OS hand the data straight from the file to the network card, skipping the detour into Kafka's own memory — down to two crossings. And it only works because the message bytes are stored in the exact same format the consumer wants, so nothing needs unpacking on the way out.

## Follow-up questions

**Alex:** If Kafka never keeps messages in its own memory and just trusts the page cache, what happens the moment a consumer asks for old messages that have already been evicted from the cache because the kernel reclaimed that RAM — does the broker just eat a slow random disk seek, and doesn't that break the 'everything is sequential/fast' promise?

**vutr:** Your instinct about the mechanism is right — the note explains that the page cache exists precisely to hide disk-seek latency for hot data, and it's explicit that the kernel can reclaim those pages whenever an application needs the RAM, so eviction of cold/old data is a real, intended consequence of this design, not a bug. What the note does NOT do is walk through the performance of that specific miss — it doesn't say the broker 'eats a slow random disk seek' or quantify the penalty for reading evicted, cold historical data. So the honest answer is: yes, evicted data must come from disk again, and the note frames the page cache as an optimization for *frequently used* data — but the exact behavior and cost of that cold-read case is beyond what the note states, so I've put the precise 'does it break the fast promise' part in gaps.

**Alex:** You said zero-copy works because the on-disk format is identical end to end and the bytes never enter Kafka's application memory — but if the bytes never pass through Kafka, how can the broker do anything that needs to actually look inside a message on the read path, like filtering or transforming it, without giving up sendfile()?

**vutr:** The note gives the key constraint even though it doesn't frame it as filtering: zero-copy via sendfile() works *because* Kafka keeps the on-disk data format identical from producer to broker to consumer, which is exactly what lets the bytes ship untouched and avoids decompressing/recompressing. The clear implication is that sendfile() is available only on the pure pass-through path where the broker does NOT need to look inside the message. Any operation that required inspecting or transforming message contents would mean copying the data up into the application (the ordinary four-copy path), forfeiting sendfile() — because by definition the bytes would then have to enter user space. But the note never describes a read-path filtering or transformation feature, so I can't tell you how Kafka handles that specific case; I've placed that in gaps.
