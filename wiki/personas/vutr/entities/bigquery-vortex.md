---
persona: vutr
kind: entity
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
slug: bigquery-vortex
topics:
- lsm-tree-storage-engines
---

BigQuery Vortex (2024) is a real-world LSM applied to fragments: a Write-Optimized Store (WOS, hot) that ages into a Read-Optimized Store (ROS, cold). It shows the LSM pattern reappearing in the OLAP world, much like Hudi 1.0's LSM Timeline for its metadata table.
