---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: acks-setting
topics:
- kafka
---

The producer acks setting trades durability against throughput and latency: acks=0 waits for nothing (highest throughput, highest data-loss risk), acks=1 waits only for leader acknowledgment (can lose data if the leader crashes before replication), and acks=all waits for every replica to confirm (safest, highest latency). DoorDash dropped their replication factor from 3 to 2 and set acks=1, cutting broker CPU utilization 30–40%.
