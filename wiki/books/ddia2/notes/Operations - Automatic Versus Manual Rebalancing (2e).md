---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 7
chapter_title: Sharding
topic: Sharding of Key-Value Data
type: subtopic
tags: [ddia2, rebalancing, autoscaling, cascading-failure, operations]
sources:
  - raw/ch07.md
---
# Operations: Automatic Versus Manual Rebalancing
> Automatic rebalancing plus automatic failure detection is a recipe for a cascading failure: a slow node gets declared dead, the cluster moves load off it, and the extra load makes more nodes look dead.

## The Idea
Does the splitting of shards and rebalancing happen **automatically or manually**? Some systems decide entirely without human interaction; others leave sharding to be explicitly configured by an administrator. **There is also a middle ground** — **Couchbase and Riak generate a suggested shard assignment automatically but require an administrator to commit it** before it takes effect.

## How It Works
**Fully automated rebalancing can be convenient**: less operational work for normal maintenance, and such systems **can even autoscale** to adapt to workload changes. **Cloud databases such as DynamoDB are promoted as being able to automatically add and remove shards to adapt to big increases or decreases in load within a matter of minutes.**

## Trade-offs & Pitfalls
- **Automatic shard management can be unpredictable.** Rebalancing is expensive — it requires rerouting requests and moving a large amount of data. **If not done carefully it can overload the network or the nodes and harm the performance of other requests.** The system must keep processing writes throughout; **if it is near its maximum write throughput, the shard-splitting process might not even be able to keep up with incoming writes.**
- **The dangerous interaction is with automatic failure detection.** Say one node is overloaded and temporarily slow to respond. **The other nodes conclude it is dead and automatically rebalance the cluster to move load away from it. This puts additional load on other nodes and the network, making the situation worse** — with **a risk of a cascading failure** where other nodes become overloaded and are also falsely suspected of being down.
- **For that reason, it can be good to have a human in the loop.** It is slower than a fully automatic process, but **it can help prevent operational surprises.**
- **Manual rebalancing is also useful preemptively**, ahead of a surge in traffic from a known event — **Cyber Monday holiday sales, or ticket sales for the World Cup.**

## Examples & Systems
Couchbase and Riak (suggest-then-commit); DynamoDB (fully automatic, minutes-scale autoscaling).

## Since the 1st Edition
The 1st edition's [[Automatic or Manual Rebalancing]] made the same argument, including the cascading-failure interaction with automatic failure detection and the recommendation for a human in the loop. **Added:** DynamoDB's minutes-scale autoscaling as a concrete example of how far automation has come, the note that shard splitting may be unable to keep up at maximum write throughput, and the preemptive-rebalancing use case with the Cyber Monday and World Cup examples.

## Related
- up: [[Sharding of Key-Value Data (2e)]] · chapter: [[Ch 07 - Sharding (2e)]]
- [[Principles for Scalability (2e)]] — the same autoscaling-versus-predictability caution
- [[Handling Node Outages (2e)]] — the failure detection this interacts badly with
- 1st edition: [[Automatic or Manual Rebalancing]] — the same subtopic
