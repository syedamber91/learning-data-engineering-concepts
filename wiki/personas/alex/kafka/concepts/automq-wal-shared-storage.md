---
persona: alex
kind: concept
sources:
- vutr/automq-wal-shared-storage
last_updated: '2026-07-10'
qc: passed
slug: automq-wal-shared-storage
topics:
- kafka
learner: alex
source_note: automq-wal-shared-storage
mastery: mastered
---

Wait, so the whole trick is about WHERE the "it's safe now" moment happens. Normal Kafka says a message is safe when it's on the broker's own disk plus follower copies. AutoMQ moves the real home of the data to S3 — but S3 uploads happen later, in batches, so they put a tiny 10GB scratch disk in between. It's like a restaurant where the waiter scribbles your order on a notepad the second you say it — that scribble is the ack — and only later types it into the main computer system. The notepad can stay small because it only has to hold orders that haven't been typed in yet.

And the reason they dare to keep only ONE copy of each partition is that the notepad doesn't die with the waiter. If broker A crashes, broker B literally grabs A's EBS volume: attaches it to itself, locks it with that NVMe reservation thing so nothing else can write, pushes the not-yet-uploaded stuff to S3, and throws the volume away. So durability comes from "the disk outlives the broker, and S3 is the real store" — not from replicas. That's also why moving a partition is just a metadata edit in KRaft: there's no data sitting on the broker to copy.

The memory part: they don't trust the OS page cache — they run their own off-heap cache so Java's garbage collector never pauses things, and writes go to the WAL with Direct I/O in 4 KiB-aligned blocks through that sliding window (current block → pending → writing).

And the two WAL flavors are a money-vs-speed dial. EBS WAL is fast, but producers in one AZ still pay to talk to leaders in another AZ — that $4,050 network vs $272 machines example is wild, the cross-AZ bill is like 15x the VMs. S3 WAL fixes it by letting the producer talk to ANY broker in its own AZ, which parks the batch in S3 as a temp file and RPCs the real leader to come pick it up.

*Source: [[automq-wal-shared-storage]] (vutr)*
