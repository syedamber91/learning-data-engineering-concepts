---
title: "Transactions & ACID"
area: "Databases"
topic: "Relational Databases"
tags: [transaction, acid, atomicity, consistency]
---

# Transactions & ACID

*Part of [[relational-databases-moc|Relational Databases]] · [[databases-moc|Databases]]*

**In one line:** A transaction bundles several changes so they all succeed together or all fail together — never half-done. ACID is the four-letter promise that keeps that data correct.

**Picture this:** Sending money to a friend means two steps: subtract from your account, add to theirs. If the power cuts out *between* the two steps, the money must not vanish. A transaction makes both steps count as one all-or-nothing move.

**How it actually works:** You wrap steps in "begin … commit". If anything fails, the database *rolls back* to before you started. ACID names the guarantees: **A**tomicity (all-or-nothing), **C**onsistency (rules like "balance ≥ 0" stay true), **I**solation (parallel transactions don't trip over each other), **D**urability (once committed, it survives a crash).

**In the real world:** Banks rely on this for every transfer — it's the reason an interrupted payment doesn't leave money deducted from you but never received. Online shops use it so an order, a payment, and a stock decrease all happen as one unit.

**Why you'd use it (and when not to):** Use transactions whenever multiple changes must stay consistent together. They add coordination cost, so for a single independent write — like appending one log line — they're unnecessary overhead.

**Connects to:** [[tables-keys-sql-basics]] · [[idempotency]]
