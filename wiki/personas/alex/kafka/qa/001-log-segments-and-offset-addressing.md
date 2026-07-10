---
persona: alex
kind: concept
sources:
- vutr/log-segments-and-offset-addressing
last_updated: '2026-07-10'
qc: passed
slug: 001-log-segments-and-offset-addressing
topics:
- kafka
learner: alex
source_note: log-segments-and-offset-addressing
mastery: mastered
---

*What Alex understood:* Wait, so Kafka messages don't wear name tags at all? Let me try it back. Each partition is like one long diary written across volumes of roughly 1GB each, and a message's 'address' is just how deep into the diary it sits — that's the offset. There's no ID card stapled to each message, because keeping a lookup table from IDs to physical locations would cost too much at the speed Kafka was built to run. And the offsets aren't 1, 2, 3 — they jump around, because to get the next message's address you take where you are and add the size of the message you just read, exactly like stepping through an array element by element. Writing is boring on purpose: everything gets glued onto the end of the newest volume, only one volume is open for writing at a time, and when it fills up you seal it and start a fresh one — which is why the disk only ever writes forward in a straight line, and why the broker can glue on whole chunks of messages at once instead of one at a time. Reading still needs a shortcut, though, so the broker keeps a table of contents: one index mapping offsets to 'which volume, what position inside it,' and a second mapping timestamps to offsets, both memory-mapped so checking them feels like reading RAM instead of disk. When I ask to read from offset X, the broker looks X up in the index, jumps to that spot in the right segment file, and streams from there — then I do the plus-length math myself to ask for the next one, so my reading is always front-to-back, and saying 'I've got offset X' automatically means I've got everything before it. And because the bytes on disk are the exact same bytes sent over the network, the broker can shovel the file straight out without unpacking and repacking anything. The catch is the volumes live on that one broker's own disk — so more storage means more machines, and moving a partition means physically trucking its volumes to another broker.

## Follow-up questions

**Alex:** You said Kafka skipped message IDs specifically to avoid the cost of maintaining an index that maps IDs to locations — but then it keeps TWO index files per partition anyway. Isn't that the exact same overhead sneaking back in through the side door? What did Kafka actually save?

**vutr:** Sharp catch — and the note addresses it head-on: 'no message ID' does not mean 'no index at all.' The correction is that Kafka indexes *offsets*, not IDs. What Kafka refused to pay for is the overhead of maintaining index structures that map every message's *ID* to its actual physical location — a real cost at the throughput Kafka was built for at LinkedIn. What it keeps instead are two offset-based index files per partition: one mapping offsets to segment files and positions within the file, and one mapping timestamps to message offsets. And these are handled with memory-mapped file techniques, so the broker reads them as if they were located directly in memory. So the saving is the elimination of the per-message ID-to-location mapping; the offset indexes that remain are what let the broker quickly find the segment and position for a requested offset without that cost.

**Alex:** The next offset is current offset + current message's length, so there are 'holes' between valid offsets. What happens if a consumer asks the broker to start at an offset that lands in one of those holes — in the middle of a message? Does the broker snap to the nearest real message, or does the fetch just fail?

**vutr:** (the wiki does not cover this — see open questions)
