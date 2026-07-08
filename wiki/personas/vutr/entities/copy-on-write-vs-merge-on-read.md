---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: copy-on-write-vs-merge-on-read
topics:
- iceberg
---

Iceberg's default COW rewrites data files on every update or delete, giving fast reads but slow writes; MOR instead uses delete files for fast writes and slower reads. The delete files come in two flavors: positional (faster read, slower write) and equality (no write overhead, slower read).
