---
persona: alex
kind: concept
sources:
- vutr/page-cache-sequential-io-and-zero-copy
last_updated: '2026-07-10'
qc: passed
slug: page-cache-sequential-io-and-zero-copy
topics:
- kafka
learner: alex
source_note: page-cache-sequential-io-and-zero-copy
mastery: mastered
---

Okay, let me try to rebuild this. The whole thing rests on one flip in my head: I assumed disk is just always slower than RAM, but that's only true when you're jumping around randomly — like flipping to random pages in a book. If you read or write straight through, front to back, the disk actually keeps up or even beats memory. So Kafka bends over backwards to only ever go front-to-back.

For writing, a partition is just a giant log split into ~1GB chunk files, and Kafka only ever writes to the *end* of the current chunk — like always adding a new line at the bottom of a notebook, never inserting in the middle. That's automatically sequential. For reading, each consumer walks the log in order, and messages don't even have real IDs, just an offset (a position number). To find the next message you take your current position and add the current message's length — like knowing the next word starts right after this one ends — so Kafka doesn't have to keep a big lookup table mapping IDs to locations.

The caching part is the sneaky bit: Kafka refuses to hold messages in its own Java memory. Instead it dumps everything to the OS's page cache — the OS grabbing spare RAM to remember recent disk data. Kafka does this partly to dodge Java's garbage collector getting sluggish with tons of objects, and partly to keep its own code simple. And if the machine needs that RAM back, the kernel just reclaims it, so it's a free loan.

Then zero-copy: I originally thought it meant literally no copying, but it actually means no *wasteful* copying. Normally sending a file out means bouncing it disk → cache → app → socket → network card, four copies and four trips across the user/kernel border. `sendfile()` lets the OS hand the data straight from the file to the network card, skipping the detour into Kafka's own memory — down to two crossings. And it only works because the message bytes are stored in the exact same format the consumer wants, so nothing needs unpacking on the way out.

*Source: [[page-cache-sequential-io-and-zero-copy]] (vutr)*
