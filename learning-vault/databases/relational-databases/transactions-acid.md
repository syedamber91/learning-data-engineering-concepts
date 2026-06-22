---
title: "Transactions & ACID"
area: "Databases"
topic: "Relational Databases"
tags: [transactions, acid, databases, data-integrity, sql, relational-databases]
---

# Transactions & ACID

*Part of [[relational-databases-moc|Relational Databases]] · [[databases-moc|Databases]]*

## In one line

A **transaction** is a bundle of database changes that either all happen together or none of them happen at all — and **ACID** is the name for the four promises a database makes to keep your data trustworthy.

---

## Picture this

Imagine you're at an ATM withdrawing $200. Behind the scenes, two things must happen: your bank balance drops by $200, and the ATM spits out the cash. Now picture the power cutting out right after your balance drops but before the cash comes out. You'd lose $200 for nothing.

A transaction is the rule that says: **both steps happen, or neither does.** The ATM either completes the whole exchange or rolls everything back to where it started — as if you never touched the machine.

ACID is the four-part checklist the database runs to make sure that promise is real, not just hopeful.

---

## How it actually works

### What is a transaction?

A transaction is a sequence of database operations (INSERTs, UPDATEs, DELETEs) that the database treats as **one indivisible unit of work**. You open a transaction with `BEGIN`, do your work, then either `COMMIT` (lock it in permanently) or `ROLLBACK` (undo everything back to before you started).

### The four ACID properties

**A — Atomicity: "all or nothing"**
Every operation inside a transaction is atomic — meaning it cannot be split. If step 3 of 5 fails, the database automatically undoes steps 1 and 2. There is no such thing as a half-finished transaction in a correct ACID database. The database achieves this by writing changes to a **write-ahead log (WAL)** — a record of "what I'm about to do" — before actually changing the data. If the system crashes mid-transaction, the WAL lets the database undo the incomplete work on restart.

**C — Consistency: "valid state to valid state"**
Before the transaction starts, the data obeys all the rules you've defined (e.g., "a bank balance can never go below zero", "every order must reference a real customer"). After the transaction commits, the data must *still* obey all those rules. If your transaction would break a rule, the database refuses it and rolls back. Consistency is the property that keeps your data meaningful, not just technically stored.

**I — Isolation: "transactions don't trip over each other"**
Many users hit a database at the same time. Isolation means each transaction behaves as if it were the *only* transaction running — it doesn't see another transaction's half-finished changes. In practice, databases offer several **isolation levels** (like `READ COMMITTED` or `SERIALIZABLE`) that trade a little isolation for more speed. Full isolation (`SERIALIZABLE`) is the safest but slowest; weaker levels are often good enough and much faster.

**D — Durability: "committed means committed"**
Once you `COMMIT`, the data is permanent. Even if the server crashes one millisecond after you commit, the data will be there when the server restarts. Databases achieve this by flushing the write-ahead log to disk before reporting success — not just holding it in fast-but-volatile RAM.

---

## Worked example

**Scenario:** Alice has $500 in her account. She transfers $200 to Bob, who has $300.

Two SQL updates must happen. Without a transaction, a crash between them leaves the database broken (Alice loses $200; Bob gets nothing).

```sql
-- Start the transaction
BEGIN;

-- Step 1: deduct from Alice
UPDATE accounts
SET balance = balance - 200
WHERE account_id = 'alice';

-- Step 2: add to Bob
UPDATE accounts
SET balance = balance + 200
WHERE account_id = 'bob';

-- Only if BOTH steps succeed do we make it permanent
COMMIT;
```

**What happens if step 2 fails** (e.g., Bob's account doesn't exist)?

```sql
BEGIN;

UPDATE accounts SET balance = balance - 200 WHERE account_id = 'alice';
-- Suppose this next line raises an error: account 'bob' not found
UPDATE accounts SET balance = balance + 200 WHERE account_id = 'bob';

-- The application catches the error and issues:
ROLLBACK;
-- Alice's balance is restored to $500. No money lost.
```

Before the `COMMIT`, Alice's balance in the database is tentatively $300, but **no other user or query can see that intermediate value** (isolation). After the `ROLLBACK`, Alice's balance snaps back to $500 (atomicity). The database's constraint "balance >= 0" was never violated (consistency). And if we had committed, the change would survive a crash (durability).

---

## In the real world

**E-commerce checkout at a store like Amazon:**

When you click "Place Order," at least three things must happen at once:
1. Inventory count for the item drops by 1.
2. A new row is inserted into the `orders` table.
3. Your payment method is charged.

If step 2 succeeds but step 3 fails (your card is declined), the database must roll back the inventory deduction — otherwise the item would appear "sold" even though no purchase happened.

Amazon's order service wraps all three operations in a single transaction. The ACID guarantees mean that thousands of customers can check out simultaneously (isolation), no order is ever half-created (atomicity), and the inventory numbers stay accurate (consistency) even if a server node reboots mid-transaction (durability).

---

## Common misconceptions

**People think: "Transactions are just a way to group queries together for convenience."**
Actually: Transactions are a *guarantee*, not a convenience feature. The grouping is meaningless without the four ACID properties. A database without ACID could "group" your queries and still leave your data corrupted if a crash occurred mid-group. The magic is in atomicity and durability — not the grouping itself.

**People think: "Isolation means two transactions can never touch the same data at the same time."**
Actually: Isolation means they don't see each other's *incomplete* changes — but concurrent access to the same rows is normal and allowed. Databases use techniques like **locks** (blocking access temporarily) and **MVCC** (multiversion concurrency control, where each transaction sees a consistent "snapshot" of the data) to allow safe concurrent access without forcing transactions to queue up one after another. Full serialization *does* force queuing, which is why weaker isolation levels exist.

**People think: "ACID makes databases too slow for high-traffic apps."**
Actually: Modern databases (PostgreSQL, MySQL InnoDB, Oracle) implement ACID very efficiently. The real performance cost is usually from *poorly written transactions* (e.g., a transaction that holds a lock for 30 seconds while waiting for a network call) rather than ACID itself. Many high-traffic systems — including banking, airline booking, and e-commerce — run ACID databases at massive scale every day.

---

## How it relates & differs

| Concept | Relates to Transactions & ACID | Differs from Transactions & ACID |
|---|---|---|
| [[tables-keys-sql-basics\|Tables, Keys & SQL Basics]] | Transactions operate *on* tables and rely on primary/foreign keys to enforce consistency rules. | Tables & keys define *structure*; ACID defines *safety guarantees* during writes. |
| [[idempotency\|Idempotency]] | Both protect against partial or repeated operations causing bad data. Transactions ensure all-or-nothing; idempotency ensures re-running the same operation is safe. | Idempotency is a property of your *application logic*; ACID is a property of the *database engine*. You need both in distributed systems. |
| [[batch-vs-streaming\|Batch vs Streaming]] | Batch pipelines often wrap large bulk inserts in transactions to ensure all-or-nothing loading. | Transactions focus on short, tight units of work inside one database. Batch/streaming describes how data *moves* at a system level — often across many databases and services where ACID doesn't apply end-to-end. |

---

## Why you'd use it (and when not to)

Use transactions whenever multiple writes must stay in sync — financial transfers, order creation, inventory management, user registration (insert user + insert profile + send welcome email trigger). Without ACID, any crash or error between steps leaves your data in an inconsistent, hard-to-recover state.

When not to use them (or when to keep them tiny): Long-running transactions that hold locks for seconds or minutes can block other users and kill performance. Avoid wrapping slow external calls (API requests, file uploads) inside a transaction. Also, some ultra-high-throughput systems (certain analytics ingestion pipelines, append-only event logs) deliberately trade ACID for speed by using databases that relax or drop some guarantees — this is called **BASE** (Basically Available, Soft-state, Eventually consistent). That's a deliberate trade-off for scale, not a mistake.

---

## Check yourself

**Memory hook:** *"ACID keeps your data from becoming a mess — Atomic, Consistent, Isolated, Durable."* Think of a bank vault: you either move the whole safe, the vault stays legal, nobody else can peek inside while you're in there, and once it's locked it stays locked.

**Q1: Alice transfers $200 to Bob. The database crashes after Alice's balance is deducted but before Bob's balance is updated. What does ACID guarantee happens next?**
A: The transaction is rolled back. On restart, the database uses its write-ahead log to detect the incomplete transaction and restores Alice's original balance. No money is lost and no money is created.

**Q2: What is the difference between Atomicity and Durability?**
A: Atomicity is about the *middle* of a transaction — ensuring partial changes are never visible or permanent if something goes wrong. Durability is about the *end* — once a transaction commits, that change survives even a system crash. Atomicity prevents bad partial states; durability prevents losing good completed states.

**Q3: Two users both try to buy the last concert ticket at the exact same moment. How does Isolation protect the data?**
A: Each purchase transaction runs as if it were the only one. The database uses locks or MVCC so that only one transaction can claim the last ticket — the second transaction either waits, sees the updated (zero) inventory, and fails cleanly, or is blocked and retried. The database will never sell the same ticket twice due to isolation keeping them from seeing each other's uncommitted work.

---

## Connects to

[[tables-keys-sql-basics|Tables, Keys & SQL Basics]] · [[idempotency|Idempotency]] · [[batch-vs-streaming|Batch vs Streaming]] · [[data-quality-validation|Data Quality & Validation]] · [[indexing|Indexing]]