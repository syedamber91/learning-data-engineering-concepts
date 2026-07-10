---
persona: alex
kind: concept
sources:
- vutr/leader-follower-replication
last_updated: '2026-07-10'
qc: passed
slug: leader-follower-replication
topics:
- kafka
learner: alex
source_note: leader-follower-replication
mastery: mastered
---

Wait, so a Kafka topic gets chopped into partitions, and each partition is like a notebook that gets photocopied onto a few different brokers — the replication factor is how many copies exist. But only one broker holds the pen: the leader. Anyone who wants to write (producers) HAS to hand their message to the leader, no exceptions, while readers (consumers) can read from the leader or from any follower's copy. When the leader gets a message, it scribbles it into its log — which physically is a stack of roughly-1GB segment files, and it always appends to the last one — and then it sends that same message out to the followers so their copies stay complete. That completeness is the whole durability trick: if the leader's machine dies, a follower already has the full notebook, so it just gets promoted to leader. A special broker called the controller acts as the referee doing that promotion, and Kafka can even make fresh copies on other brokers later to get back up to the replication factor. Copies get dealt around the cluster round-robin, like dealing cards, so no single broker ends up holding all the hot topics.

The catch is that every copy lives on a broker's own local disk. So whenever the cluster changes shape — a broker dies, one gets added, or you want to even out load — you have to physically ship partition data across the network. It's like moving houses instead of just changing the nametag on a door. And in the cloud you pay for the same message twice: in a three-AZ setup, a producer's send crosses a zone boundary about two-thirds of the time just to reach the leader, and then the leader ships that message AGAIN to followers sitting in the other two zones. That's why AutoMQ's move makes sense to me: object storage already replicates across zones with erasure coding at eleven nines of durability, so they keep just one replica — still the leader, so Kafka's partition logic and small metadata survive without needing an extra coordinator like WarpStream — and let the object storage layer do the durability job.

*Source: [[leader-follower-replication]] (vutr)*
