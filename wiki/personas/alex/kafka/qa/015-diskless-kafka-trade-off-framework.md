---
persona: alex
kind: concept
sources:
- vutr/diskless-kafka-trade-off-framework
last_updated: '2026-07-10'
qc: passed
slug: 015-diskless-kafka-trade-off-framework
topics:
- kafka
learner: alex
source_note: diskless-kafka-trade-off-framework
mastery: mastered
---

*What Alex understood:* Okay let me try to rebuild this. The old Kafka is like a warehouse where every worker keeps their own copy of the inventory on a shelf right next to them (local disk), and to stay safe they photocopy every new item and mail it to two other warehouses in different neighborhoods. In the cloud, the mailing — the cross-AZ traffic — is the killer cost, way more than the workers' salaries. Vu's example was literally $272 for the machines but $4,050 for the mailing. Diskless says: stop keeping shelves and stop mailing. Dump everything into one giant shared vault (object storage) that's already super-durable on its own — eleven nines — so nobody has to photocopy anything. Brokers become interchangeable temp workers who own no data.

But the vault is slow to write to. So now there's a fork. WarpStream and Bufstream go 'pure': they wait until your batch is actually safe in the vault before saying 'got it,' which is why you wait up to ~1 second. To not do a PUT for every tiny message they hold a buffer (~250ms / 8MiB) — bigger buffer, cheaper but slower. AutoMQ cheats the wait: it scribbles your message into a small fast notebook (a 10GB WAL on EBS) first, acks you immediately, then copies it to the vault later in the background. So AutoMQ gets speed but has to touch a disk again.

The other big split is leaders. Leaderless (WarpStream/Bufstream) means any worker takes any write, so they can always use a nearby worker and dodge cross-AZ — but the data ends up smeared across tons of little files and they need a separate ledger (like DynamoDB) to track it all. AutoMQ keeps the boss/leader idea but does a trick: a nearby worker drops temp files in the shared vault and just phones the real leader to stitch them in, so you still avoid the big cross-AZ bill and only pay for a tiny phone call. The punchline: it's not about cheapest, it's whether you can live with ~1s latency. If yes, 5–10x cheaper. If no, pay for a WAL design.

## Follow-up questions

**Alex:** For AutoMQ's same-AZ trick — the nearby broker writes temp files to shared object storage and then RPCs the real leader to append them. But if the real leader is in another zone, isn't that RPC itself crossing zones? Why doesn't that RPC traffic bring back the same cross-AZ bill the whole design was trying to kill?

**vutr:** You've spotted exactly the residual cost the note flags. AutoMQ doesn't claim to remove cross-AZ traffic completely — the note says its same-AZ scheme kills 'nearly 100% of cross-AZ cost, minus small RPC traffic.' The bulk that was expensive was the message DATA itself: every produced batch getting replicated to followers in two other AZs. In AutoMQ's design the data payload goes into shared object storage (durable on its own, no broker replication), and what actually crosses to the leader is just the RPC — a control message telling the leader to append temp files it can read from that shared storage. So yes, the RPC can cross a zone, but it carries coordination, not the full data stream, which is why the note treats it as a small residual rather than a reintroduction of the old bill.

**Alex:** WarpStream and Bufstream both wait for object storage before acking, but Bufstream's p99 is 500ms while WarpStream's end-to-end p99 is ~1s — almost double. If they're using the same 'wait for S3' strategy, where does WarpStream's extra latency actually come from?

**vutr:** The note doesn't give a mechanism-level breakdown of why WarpStream's end-to-end p99 (~1s) is higher than Bufstream's (500ms). It reports both numbers and tells us they share the 'ack only after the batch lands in object storage and metadata is committed' strategy with a ~250ms/8MiB buffer, but it never isolates what accounts for WarpStream's extra latency specifically. I won't invent a cause. One thing the note does note about WarpStream's architecture — its consistent-hashing cache assignment 'effectively falls back to the leader idea, with extra complexity' — but the text does not tie that complexity to the latency delta, so I'm treating the precise source as unstated.
