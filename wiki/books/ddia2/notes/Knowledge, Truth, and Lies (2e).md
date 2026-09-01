---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 9
chapter_title: The Trouble with Distributed Systems
type: topic
tags: [ddia2, knowledge, system-model, truth, quorum]
sources:
  - raw/ch09.md
---
# Knowledge, Truth, and Lies
So far this chapter has explored **how distributed systems are different from single-machine programs**: there is no shared memory, only message passing over an unreliable network with variable delays, **and the systems may suffer partial failures, unreliable clocks, and processing pauses.**

**The consequences are profoundly disorienting if you're not used to distributed systems. A node in the network cannot know anything for sure about other nodes — it can only make guesses based on the messages it receives (or doesn't receive).** A node can find out another's state only by exchanging messages with it, **and if a remote node doesn't respond there is no way of knowing its state, because problems in the network cannot reliably be distinguished from problems at a node.**

**Discussions of these systems border on the philosophical:** What do we know to be true or false in our system? How sure can we be of that knowledge, if the mechanisms for perception and measurement are unreliable? Should software systems obey the laws we expect of the physical world, such as cause and effect?

**Fortunately we don't need to go as far as figuring out the meaning of life.** In a distributed system we can **state the assumptions we are making about the behavior — the system model — and design the system so that it meets those assumptions.** **Algorithms can be proved to function correctly within a certain system model. This means reliable behavior is achievable, even if the underlying system model provides very few guarantees.**

## Subtopics
- [[The Majority Rules (2e)]] — a node cannot trust its own judgment; quorums decide.
- [[Distributed Locks and Leases (2e)]] — zombies, delayed requests, and fencing tokens.
- [[Byzantine Faults (2e)]] — when nodes lie, when that matters, and cheap partial defences.
- [[System Model and Reality (2e)]] — timing and node-failure models; safety versus liveness.
- [[Formal Methods and Randomized Testing (2e)]] — how you check that any of this is actually true.

## Key Takeaways
- **The epistemological framing is the point of the topic.** Everything a node "knows" about another node is an inference from messages, and **the absence of a message is not evidence of anything in particular.**
- **Making software well behaved in an unreliable system model is possible but not straightforward** — which is what makes explicit system models, safety/liveness distinctions, and formal verification worth the effort.
- The three practical devices this topic supplies — **quorums, fencing tokens, and stated system models** — are what the next chapter's consensus algorithms are built from.

## Since the 1st Edition
The 1st edition's [[Knowledge, Truth, and Lies]] had the same framing and covered the majority rule, fencing tokens, Byzantine faults, and system models. **The 2nd edition restructures it into five subtopics**, promoting **[[Distributed Locks and Leases (2e)]]** from a section within the majority discussion to its own subtopic (with new material on fencing across multiple replicas), and **adding [[Formal Methods and Randomized Testing (2e)]] entirely** — the 1st edition's short "Formal methods" mention becomes a full treatment of model checking, fault injection, and deterministic simulation testing.

## Related
- chapter: [[Ch 09 - The Trouble with Distributed Systems (2e)]]
- [[Ch 10 - Consistency and Consensus (2e)]] — algorithms built on these foundations
- [[Detecting Concurrent Writes (2e)]] — the happens-before relation as another form of knowledge
- 1st edition: [[Knowledge, Truth, and Lies]] — the same topic
