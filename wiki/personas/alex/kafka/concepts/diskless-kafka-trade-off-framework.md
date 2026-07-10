---
persona: alex
kind: concept
sources:
- vutr/diskless-kafka-trade-off-framework
last_updated: '2026-07-10'
qc: passed
slug: diskless-kafka-trade-off-framework
topics:
- kafka
learner: alex
source_note: diskless-kafka-trade-off-framework
mastery: mastered
---

Okay let me try to rebuild this. The old Kafka is like a warehouse where every worker keeps their own copy of the inventory on a shelf right next to them (local disk), and to stay safe they photocopy every new item and mail it to two other warehouses in different neighborhoods. In the cloud, the mailing — the cross-AZ traffic — is the killer cost, way more than the workers' salaries. Vu's example was literally $272 for the machines but $4,050 for the mailing. Diskless says: stop keeping shelves and stop mailing. Dump everything into one giant shared vault (object storage) that's already super-durable on its own — eleven nines — so nobody has to photocopy anything. Brokers become interchangeable temp workers who own no data.

But the vault is slow to write to. So now there's a fork. WarpStream and Bufstream go 'pure': they wait until your batch is actually safe in the vault before saying 'got it,' which is why you wait up to ~1 second. To not do a PUT for every tiny message they hold a buffer (~250ms / 8MiB) — bigger buffer, cheaper but slower. AutoMQ cheats the wait: it scribbles your message into a small fast notebook (a 10GB WAL on EBS) first, acks you immediately, then copies it to the vault later in the background. So AutoMQ gets speed but has to touch a disk again.

The other big split is leaders. Leaderless (WarpStream/Bufstream) means any worker takes any write, so they can always use a nearby worker and dodge cross-AZ — but the data ends up smeared across tons of little files and they need a separate ledger (like DynamoDB) to track it all. AutoMQ keeps the boss/leader idea but does a trick: a nearby worker drops temp files in the shared vault and just phones the real leader to stitch them in, so you still avoid the big cross-AZ bill and only pay for a tiny phone call. The punchline: it's not about cheapest, it's whether you can live with ~1s latency. If yes, 5–10x cheaper. If no, pay for a WAL design.

*Source: [[diskless-kafka-trade-off-framework]] (vutr)*
