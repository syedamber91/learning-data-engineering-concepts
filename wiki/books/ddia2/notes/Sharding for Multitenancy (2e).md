---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 7
chapter_title: Sharding
type: topic
tags: [ddia2, multitenancy, saas, cell-based-architecture, gdpr, data-residency]
sources:
  - raw/ch07.md
---
# Sharding for Multitenancy
SaaS products and cloud services are often **multitenant**, where each **tenant** is a customer. Multiple users may have logins on the same tenant, but **each tenant has a self-contained dataset separate from other tenants'**. In an email marketing service, each business that signs up is a separate tenant, since one business's newsletter sign-ups and delivery data are separate from another's.

Sharding is sometimes used to implement multitenancy: **either each tenant gets a separate shard, or multiple small tenants are grouped into a larger shard.** These may be physically separate databases or separately manageable portions of a larger logical database.

## Key Takeaways
The seven advantages the book lists:
- **Resource isolation.** If one tenant performs a computationally expensive operation, other tenants on different shards are less likely to see their performance affected.
- **Permission isolation.** If there is a bug in your access control logic, **you are less likely to accidentally give one tenant access to another's data** when the datasets are stored physically separately.
- **Cell-based architecture.** You can shard not just storage but **the services running your application code**: services and storage for a set of tenants are grouped into a self-contained **cell**, and different cells run largely independently. This gives **fault isolation** — a fault in one cell stays in that cell, and tenants in other cells are unaffected.
- **Per-tenant backup and restore.** Backing up each tenant's shard separately makes it possible to **restore one tenant's state without affecting others** — useful when a tenant accidentally deletes or overwrites important data.
- **Regulatory compliance.** GDPR and CCPA give individuals the right to access and request deletion of personal information. **If each person's data is stored in a separate shard, this becomes simple data export and deletion operations on their shard.**
- **Data residence.** If a tenant's data must be stored in a particular jurisdiction under data residency laws, **a region-aware database can assign that tenant's shard to a particular region.**
- **Gradual schema rollout.** Schema migrations can be rolled out **one tenant at a time**, reducing risk by letting you detect problems before they affect everyone — **though this can be difficult to do transactionally.**

The three main challenges:
- **It assumes each individual tenant is small enough to fit on a single node.** If one tenant is too big for a machine, you must **additionally shard within that tenant**, which returns you to sharding for scalability.
- **Many small tenants mean too much per-shard overhead.** You can group several into a bigger shard, but then you face the problem of **how to move tenants between shards as they grow.**
- **Cross-tenant features become harder**, since they require joining data across shards.

## Since the 1st Edition
Entirely new. The 1st edition did not discuss multitenancy as a sharding use case at all. Notice how much of this topic is driven by things outside the database — **GDPR/CCPA deletion rights, data residency laws, per-tenant blast radius** — which is the same pattern as [[Data Systems, Law, and Society (2e)]] in Chapter 1: legal and organisational requirements now shape data architecture directly.

## Related
- chapter: [[Ch 07 - Sharding (2e)]]
- [[Data Systems, Law, and Society (2e)]] — the compliance pressures driving several of these advantages
- [[Cloud Native System Architecture (2e)]] — multitenancy as a cloud-native property
- [[Storage and Indexing for OLTP (2e)]] — an embedded database instance per tenant
