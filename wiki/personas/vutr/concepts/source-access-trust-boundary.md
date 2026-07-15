---
persona: vutr
kind: concept
sources:
- raw/change-data-capture-cdc-and-data-sourcing-additional/data-engineering-system-design-11.md
last_updated: '2026-07-15'
qc: passed
slug: source-access-trust-boundary
topics:
- change-data-capture-cdc-and-data-sourcing
---

Vu's mental model for the whole sourcing problem is that the source is the one part of your pipeline you don't fully control — you often don't own it, sometimes don't even know where it came from, and you usually won't know what changed or broke until it shows up downstream. Everything in "how do I access the data?" flows from first figuring out who owns the source: is it a supported product with an on-call team and a documented SLA, or a side project nobody has touched in two years? That answer determines whether you'll get advance notice before an API version is deprecated, a field is changed, or a database is migrated.

Access itself layers three separate concerns. Network reachability comes first — is the source on the public internet or inside a private network, and if private, does reaching it require sitting down with the infrastructure team? Vu flags a specific trap here: a connection that works fine over a corporate VPN locally can fail immediately in production, because the production server doesn't share that network path. Authentication answers "who am I?" to the source — static credentials (username/password, API or secret keys), service accounts scoped to a specific workload, or OAuth/token-based auth, which needs refresh logic for expiring tokens — and the operational questions that go with it: where are credentials stored (a secrets manager, never a `.env` file in the repo), how do you access them, and what happens if they expire mid-run? Authorization is the third and separate layer: being granted access doesn't mean full access — you might have table-level but not column-level access, or row-level policies filtering what you see. Vu's stated principle is to hold the fewest permissions possible, even though a broad, powerful credential feels more convenient up front — because a leaked over-privileged credential is far more dangerous than the friction of asking for narrower access.

*See also: [[pull-vs-push-source-types]] · [[cdc-operational-considerations]] · [[data-quality-contract-with-source]]*
