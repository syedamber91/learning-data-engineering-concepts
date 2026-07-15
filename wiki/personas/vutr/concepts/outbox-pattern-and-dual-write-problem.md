---
persona: vutr
kind: concept
sources:
- raw/change-data-capture-cdc-and-data-sourcing-additional/everything-you-need-to-know-about-741.md
last_updated: '2026-07-15'
qc: passed
slug: outbox-pattern-and-dual-write-problem
topics:
- change-data-capture-cdc-and-data-sourcing
---

The dual-write problem shows up whenever a service needs to do two things when something happens — save state and publish an event — and does them as two separate operations. Vu's example: a `UserService` saves a new user to its database, then publishes a `UserCreated` event to a broker like Kafka or RabbitMQ so an `EmailService` can send a welcome email. If the database write succeeds but the service crashes just before publishing the event, the user exists but no other service ever finds out, and the welcome email is never sent. Do the operations in either order, sequentially, and there's a window where one write can succeed while the other is lost — a classic distributed-systems inconsistency.

The Outbox Pattern closes that window by using the service's own database as a reliable, temporary holding area for messages, so the state change and the event are never separated. Concretely: when the user signs up, the service inserts the new user's row *and* inserts an event record (e.g., `{event_type: "UserCreated", payload: "..."}`) into a special "outbox" table, both within the same database transaction. Because the transaction is atomic, either both writes land or neither does — it's impossible to end up with a new user and no corresponding outbox event. A separate, independent process (the "relay") then reads unprocessed events from the outbox table and publishes them to the message broker.

This is where CDC re-enters the picture: CDC — either trigger-based or log-based — can act as that message relay. It continuously monitors the outbox table for new INSERTs, and when a new event is committed, CDC captures the change and publishes it to the broker. In other words, the outbox pattern turns "publish an event reliably" into "make sure a change lands in a table," and then hands the actual publishing off to the same mechanism ([[trigger-based-cdc]] or [[log-based-cdc]]) already used for source database replication.

*See also: [[trigger-based-cdc]] · [[log-based-cdc]] · [[incremental-extraction-strategies]]*
