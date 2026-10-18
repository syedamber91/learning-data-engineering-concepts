---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 12
chapter_title: Stream Processing
type: topic
tags: [ddia2, events, producers, consumers, topics, polling]
sources:
  - raw/ch12.md
---
# Transmitting Event Streams
**In batch processing the inputs and outputs of a job are files. What does the streaming equivalent look like?**

**When the input is a file, the first processing step is usually to parse it into a sequence of records.** **In a streaming context a record is more commonly known as an event, but it is essentially the same thing: a small, self-contained, immutable object containing the details of something that happened at a point in time.** **An event usually contains a timestamp indicating when it happened according to a time-of-day clock.**

**The thing that happened might be a user action** — viewing a page, making a purchase — **or it might originate from a machine**, such as a periodic temperature sensor measurement or a CPU utilization metric. **In the Unix tools example, each line of the web server log is an event.**

**An event may be encoded as a text string, JSON, or a binary form**, which lets you **store it** — appending to a file, inserting into a relational table, writing to a document database — **and send it over the network to another node to process it.**

**In batch processing a file is written once and potentially read by multiple jobs.** **Analogously, an event is generated once by a producer (publisher, sender) and potentially processed by multiple consumers (subscribers, recipients).** **In a filesystem a filename identifies a set of related records; in a streaming system, related events are usually grouped into a topic or stream.**

## Subtopics
- [[Messaging Systems (2e)]] — the traditional approach, and the questions that distinguish implementations.
- [[Log-Based Message Brokers (2e)]] — the hybrid of database durability and messaging latency.

## Key Takeaways
- **In principle a file or database is sufficient to connect producers and consumers**: the producer writes every event to the datastore, and **each consumer periodically polls to check for events since it last ran.** **This is essentially what a batch process does when processing a day's worth of data at the end of every day.**
- **But when moving toward continual processing with low delays, polling becomes expensive if the datastore isn't designed for it.** **The more often you poll, the lower the percentage of requests returning new events, and thus the higher the overheads.** **It is better for consumers to be notified when new events appear.**
- **Databases have traditionally not supported this kind of notification well.** **Relational databases commonly have triggers, which can react to a change, but they are very limited in what they can do and have been somewhat of an afterthought in database design.** **So specialized tools were developed for delivering event notifications.**

## Since the 1st Edition
Essentially unchanged from the 1st edition's [[Transmitting Event Streams]] — the same event definition, the same producer/consumer/topic vocabulary, and the same polling-versus-notification argument. Its two subtopics are also the same, though both have gained substantial new material.

## Related
- chapter: [[Ch 12 - Stream Processing (2e)]]
- [[Event-Driven Architectures (2e)]] — the same systems from the encoding chapter
- [[Databases and Streams (2e)]] — where the events can come from
- 1st edition: [[Transmitting Event Streams]] — the same topic
