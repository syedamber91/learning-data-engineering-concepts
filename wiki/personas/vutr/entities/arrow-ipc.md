---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: arrow-ipc
topics:
- apache-arrow
---

Arrow IPC is how Arrow data moves between processes, in two flavors: a Streaming format for sequential access, and a File format for random access that begins and ends with the 'ARROW1' magic string. Because the File format is on-disk-shaped, IPC files can be memory-mapped.
