---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
type: concept
tags: [ddia2, concept, cloud, architecture, object-storage]
sources:
  - raw/ch01.md
  - raw/ch04.md
  - raw/ch11.md
---
# Separation of Storage and Compute

The defining cloud-era architecture: persist data in a shared object store (S3 and friends) and run stateless, elastically scaled compute against it, instead of coupling disks to the machines that query them.

It is why cloud data warehouses can scale query capacity independently of data volume ([[Cloud Data Warehouses (2e)]]), why distributed filesystems gave way to object stores in batch processing ([[Distributed Filesystems (2e)]]), and it recurs as a theme throughout the 2nd edition where the 1st assumed local disks.

## Appears In
- [[Cloud Native System Architecture (2e)]]
- [[Cloud Versus Self-Hosting (2e)]]
- [[Setting Up New Followers (2e)]]
