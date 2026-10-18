---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 12
chapter_title: Stream Processing
topic: Transmitting Event Streams
type: subtopic
tags: [ddia2, message-broker, jms, amqp, dead-letter-queue, acknowledgment, backpressure]
sources:
  - raw/ch12.md
---
# Messaging Systems
> Two questions distinguish every messaging system: what happens when producers outrun consumers, and what happens when nodes crash.

## The Idea
**A producer sends a message containing the event, which is pushed to consumers.** **A direct channel like a Unix pipe or TCP connection would be a simple implementation, but most messaging systems expand on this**: **pipes and TCP connect exactly one sender with one recipient, whereas a messaging system allows multiple producers to send to the same topic and multiple consumers to receive from it.**

**Within this publish/subscribe model, different systems take a wide range of approaches, and there is no one right answer.** **Two questions are particularly helpful for differentiating them:**

**What happens if producers send faster than consumers can process?** **Three options: drop messages, buffer them in a queue, or apply backpressure** (flow control, blocking the producer). **Unix pipes and TCP use backpressure**: a small fixed-size buffer, and **if it fills the sender is blocked until the recipient takes data out.** **If messages are buffered, it is important to understand what happens as the queue grows: does the system crash if the queue no longer fits in memory, or does it write to disk? How does disk access affect performance, and what happens when the disk fills up?**

**What happens if nodes crash or temporarily go offline — are any messages lost?** **As with databases, durability may require writing to disk and/or replication, which has a cost.** **If you can afford to sometimes lose messages, you can probably get higher throughput and lower latency on the same hardware.**

**Whether loss is acceptable depends on the application.** **With sensor readings and metrics transmitted periodically, an occasional missing data point is perhaps unimportant** since an updated value follows shortly — **but beware that if a large number of messages are dropped, it may not be immediately apparent that the metrics are incorrect.** **If you are counting events, reliable delivery matters more, since every lost message means incorrect counters.**

## How It Works
**Direct messaging from producers to consumers.** Some systems use direct network communication without intermediaries:
- **UDP multicast** is **widely used in the financial industry for streams such as stock market feeds, where low latency is important.** **Although UDP itself is unreliable, application-level protocols can recover lost packets** — the producer must remember packets it sent so it can retransmit on demand.
- **Brokerless libraries such as ZeroMQ and nanomsg** implement publish/subscribe over TCP or IP multicast.
- **Metrics agents such as StatsD** use **unreliable UDP messaging.** (**In the StatsD protocol, counter metrics are correct only if all messages are received; using UDP makes the metrics at best approximate.**)
- **If the consumer exposes a service, producers can make a direct HTTP or RPC request to push messages** — **the idea behind webhooks**, where a callback URL of one service is registered with another, which requests that URL whenever an event occurs.

**These work well for their designed situations but generally require application code to be aware of the possibility of message loss, and the faults they tolerate are quite limited.** **Even if protocols detect and retransmit lost packets, they generally assume producers and consumers are constantly online.** **If a consumer is offline it may miss messages sent while unreachable**, and **producer retries break down if the producer crashes, losing the buffer of messages it was supposed to retry.**

**Message brokers.** **A widely used alternative: send messages via a message broker (message queue), essentially a kind of database optimized for handling message streams.** It **runs as a server with producers and consumers connecting as clients.** **By centralizing the data in the broker, these systems more easily tolerate clients that come and go**, and **durability moves to the broker.** **Some keep messages only in memory; others write to disk so they survive a broker crash.** **Faced with slow consumers, they generally allow unbounded queueing** rather than dropping or backpressure.

**A consequence of queueing is that consumers are generally asynchronous**: **a producer normally waits only for the broker to confirm it has buffered the message, not for consumers to process it.** **Delivery happens at an undetermined future point — often within a fraction of a second, sometimes significantly later if there is a backlog.**

**Brokers compared to databases.** **Some brokers can even participate in two-phase commit using XA or JTA**, making them quite similar to databases — **but important practical differences remain:**
- **Databases keep data until explicitly deleted; some brokers automatically delete a message once successfully delivered.** **Such brokers are not suitable for long-term data storage.**
- **Since they delete quickly, most brokers assume their working set is fairly small — queues are short.** **If a broker must buffer a lot of messages because consumers are slow, each message takes longer to process and overall throughput may degrade.**
- **Databases often support secondary indexes and query languages; brokers often support subscribing to topics matching a pattern.** **Both are ways for a client to select the portion of data it wants, but databases offer much more advanced query functionality.**
- **A database query result is a point-in-time snapshot** — **if another client changes the result, the first client doesn't find out unless it repeats the query.** **Brokers don't support arbitrary queries or message updates, but they do notify clients when new messages become available.**

**This traditional view is encapsulated in JMS and AMQP and implemented in RabbitMQ, ActiveMQ, HornetQ, Qpid, TIBCO EMS, IBM MQ, Azure Service Bus, and Google Cloud Pub/Sub.** **It is possible to use databases as queues, but tuning them for good performance is not straightforward.**

**Multiple consumers.** Two main patterns:
- **Load balancing** — **each message is delivered to one of the consumers**, sharing the work. **Useful when messages are expensive to process, so you can add consumers to parallelize.** (**AMQP: multiple clients consuming from the same queue. JMS: a shared subscription.**)
- **Fan-out** — **each message is delivered to all consumers**, letting several independent consumers "tune in" to the same broadcast without affecting one another — **the streaming equivalent of several batch jobs reading the same input file.** (**JMS topic subscriptions, AMQP exchange bindings.**)

**The two can be combined** — **Kafka's consumer groups**: **each message goes to one consumer within a group (balancing load), and two separate groups each receive every message (fan-out across groups).**

**Acknowledgments and redelivery.** **Consumers may crash at any time**, so **brokers use acknowledgments: a client explicitly tells the broker when it has finished processing so the broker can remove the message.** **If the connection closes or times out without an acknowledgment, the broker assumes the message wasn't processed and delivers it again to another consumer.** (**The message may actually have been fully processed with the acknowledgment lost in the network — handling that requires an atomic commit protocol, unless the operation was idempotent or exactly-once isn't required.**)

## Trade-offs & Pitfalls
- **Combined with load balancing, redelivery reorders messages.** Consumers generally process in send order, **but if consumer 2 crashes while processing m3 while consumer 1 processes m4, the unacknowledged m3 is redelivered to consumer 1**, which then processes **m4, m3, m5** — **so m3 and m4 are not delivered in the order the producer sent them.** **Even if the broker otherwise tries to preserve order, as JMS and AMQP require, load balancing plus redelivery inevitably reorders.** **To avoid it, use a separate queue per consumer.** **Reordering doesn't matter if messages are independent, but it can matter if there are causal dependencies.**
- **Redelivery can also waste resources, starve resources, or permanently block a stream.** **The common scenario: a producer improperly serializes a message — leaving out a required key in a JSON object. If it causes a consumer to crash and restart, the consumer won't acknowledge, so the broker resends it, crashing another consumer. This loop repeats indefinitely.** **If the broker guarantees strong ordering, no further progress can be made; brokers allowing reordering can progress but waste resources on messages that will never be acknowledged.**
- **Dead letter queues (DLQs) handle this.** **Rather than retrying forever, the message is moved to a different queue to unblock consumers.** **Monitoring is usually set up on DLQs — any message there is an error** — and **an operator can permanently drop it, manually modify and reproduce it, or fix consumer code.** **DLQs are common in most queuing systems, and log-based systems such as Apache Pulsar and stream processors such as Kafka Streams now support them too.**

## Examples & Systems
UDP multicast, ZeroMQ, nanomsg, StatsD, webhooks; RabbitMQ, ActiveMQ, HornetQ, Qpid, TIBCO EMS, IBM MQ, Azure Service Bus, Google Cloud Pub/Sub; Kafka consumer groups; Pulsar and Kafka Streams DLQ support.

## Since the 1st Edition
The 1st edition's [[Messaging Systems]] covered the same two defining questions, the same direct-messaging options, the same broker-versus-database comparison, and the same load-balancing/fan-out and acknowledgment/redelivery discussion. **New: dead letter queues**, with the poison-message loop that motivates them and the note that **log-based and stream-processing systems now support them** — a practical operational concern the 1st edition did not address.

## Related
- up: [[Transmitting Event Streams (2e)]] · chapter: [[Ch 12 - Stream Processing (2e)]]
- [[Log-Based Message Brokers (2e)]] — the durable alternative
- [[Event-Driven Architectures (2e)]] — the same systems in Chapter 5
- [[Exactly-Once Message Processing Revisited (2e)]] — handling the lost-acknowledgment case
- 1st edition: [[Messaging Systems]] — the same subtopic
