---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 9
chapter_title: The Trouble with Distributed Systems
topic: Knowledge, Truth, and Lies
type: subtopic
tags: [ddia2, tla-plus, model-checking, jepsen, chaos-engineering, dst, determinism]
sources:
  - raw/ch09.md
---
# Formal Methods and Randomized Testing
> Three techniques, in increasing contact with your actual code: model checking a specification, injecting faults into a running system, and deterministic simulation testing that replays the exact failure.

## The Idea
**How do we know an algorithm satisfies the required properties?** Because of concurrency, partial failures, and network delays there are **a huge number of potential states**, and we must **guarantee properties hold in every possible state without forgetting edge cases.**

**One approach is formal verification** — describing the algorithm mathematically and proving it satisfies the properties in all situations the system model allows. **Proving an algorithm correct doesn't mean its implementation will always behave correctly, but it's a very good first step**, because theoretical analysis **can uncover problems that might remain hidden for a long time in a real system and only bite when your timing assumptions are defeated by unusual circumstances.**

**It is prudent to combine theoretical analysis with empirical testing.** Techniques such as **property-based testing, fuzzing, and deterministic simulation testing** use randomization to test a system in a wide range of situations. **Amazon Web Services, FoundationDB, and TigerBeetle have successfully used combinations of these on many products.**

## How It Works
**Model checking and specification languages.** **Model checkers** verify that an algorithm behaves as expected. **A specification is written in a purpose-built language such as TLA+, Gallina, or FizzBee**, which make it easier to focus on behavior without implementation details. The checker then **verifies invariants hold across all of an algorithm's states by systematically trying everything that could happen.**

**Model checking can't actually prove invariants hold for every possible state**, since most real algorithms have an **infinite state space** — a true verification would require a formal proof, **which can be done but is typically more difficult.** Instead, checkers encourage you to **reduce the model to an approximation that can be fully verified, or limit execution to an upper bound** such as a maximum number of messages. **Bugs occurring only with longer executions would then not be found.**

**Still, model checkers strike a nice balance between ease of use and the ability to find nonobvious bugs.** **CockroachDB, TiDB, Kafka, and many others use model specifications to find and fix bugs.** **Using TLA+, researchers demonstrated the potential for data loss in viewstamped replication caused by ambiguity in the prose description of the algorithm.**

**By design, model checkers don't run your actual code** but a simplified model specifying only the protocol's core ideas. **This makes exploring the state space tractable but risks your specification and implementation going out of sync.** **It is possible to check whether they behave equivalently, but this requires instrumentation in the real implementation.**

**Fault injection.** **An effective (and sometimes scary) technique**: **inject faults into a running system's environment and see how it behaves** — network failures, machine crashes, disk corruption, paused processes, anything you can imagine going wrong.

Tests are typically run in an environment closely resembling production; **some even inject faults directly into production. Netflix popularized this with Chaos Monkey**, and production fault injection is often called **chaos engineering**.

**The system under test is deployed alongside fault injection coordinators and scripts.** **Coordinators decide what faults to execute and when; scripts inject failures into individual nodes or processes**, using tools like `kill` to pause or kill a Linux process, `umount` to unmount a disk, and firewall settings to disrupt network connections.

**The myriad of tools makes fault injection tests cumbersome to write**, so **it's common to adopt a framework like Jepsen**, which comes with OS integrations and many prebuilt fault injectors. **Jepsen has been remarkably effective at finding critical bugs in many widely used systems.**

**Deterministic simulation testing (DST).** **A popular complement to model checking and fault injection**, using a similar state-space exploration process **but testing your actual code, not a model.**

**A simulation automatically runs a large number of randomized executions.** **Network communication, I/O, and clock timing are all replaced with mocks that let the simulator control the exact order in which things happen**, including timings and failure scenarios — **exploring many more situations than handwritten tests or fault injection could.** **If a test fails it can be rerun, since the simulator knows the exact order of operations that triggered it** — **in contrast to fault injection, which lacks such fine-grained control.**

**DST requires controlling all sources of nondeterminism.** Three strategies:
- **Application-level.** Systems built from the ground up for deterministic execution. **FoundationDB, a pioneer, uses an asynchronous communication library called Flow** providing an injection point for a deterministic network simulation. **TigerBeetle** models system state as a state machine with **all mutations in a single event loop**, which combined with mock deterministic primitives runs deterministically.
- **Runtime-level.** Languages with asynchronous runtimes provide an insertion point. **A single-threaded runtime forces all asynchronous code to run sequentially. FrostDB patches Go's runtime to execute goroutines sequentially. Rust's MadSim** provides deterministic implementations of Tokio's async runtime, Amazon's S3 library, Kafka's Rust library, and others — **applications swap in deterministic libraries without changing their code.**
- **Machine-level.** **An entire machine can be made deterministic** — a delicate process requiring deterministic responses to all normally nondeterministic calls. **Tools such as Antithesis build a custom hypervisor replacing nondeterministic operations**, accounting for everything from clocks to network and storage. **Then developers can run their entire distributed system in containers within the hypervisor and get a completely deterministic distributed system.**

**DST's advantages go beyond replayability. Antithesis explores many code paths by branching a test execution into subexecutions when it discovers less common behavior.** And **because tests use mocked clocks and network calls, they can run faster than wall clock time** — **TigerBeetle's time abstraction lets simulations simulate network latency and timeouts without actually waiting for them.**

## Trade-offs & Pitfalls
**The power of determinism.** **Nondeterminism is at the core of all the distributed systems challenges in this chapter**: concurrency, network delay, process pauses, clock jumps, and crashes all happen unpredictably and vary from run to run. **Conversely, if you can make a system deterministic, that hugely simplifies things** — and the idea **arises again and again in distributed system design.** Besides DST, the book points at three earlier appearances:
- **Event sourcing** — you can **deterministically replay a log of events to reconstruct derived materialized views.**
- **Workflow engines** — rely on **workflow definitions being deterministic** to provide durable execution semantics.
- **State machine replication** — replicates data by **independently executing the same sequence of deterministic transactions on each replica**, in the variants of **statement-based replication** and **serial transaction execution using stored procedures.**

**However, making code fully deterministic requires care.** Even after removing concurrency and replacing I/O, network, clocks, and random number generators with deterministic simulations, **elements of nondeterminism may remain** — **in some languages the order of iteration over a hash table may be nondeterministic**, and **whether you run into a resource limit (memory allocation failure, stack overflow) is also nondeterministic.**

## Examples & Systems
TLA+, Gallina, FizzBee (specification languages); CockroachDB, TiDB, Kafka (users of model specifications); Chaos Monkey, Jepsen (fault injection); FoundationDB/Flow, TigerBeetle, FrostDB, MadSim, Antithesis (DST).

## Since the 1st Edition
**Almost entirely new.** The 1st edition ended [[System Model and Reality]] with a short paragraph on formal proofs and noted they are rarely used in practice. **The 2nd edition builds a full subtopic** covering model checking with named languages and industrial users, **fault injection and Jepsen**, and **deterministic simulation testing** with three implementation strategies and five named systems — plus the **power-of-determinism box** connecting DST back to event sourcing, workflow engines, and state machine replication. This is one of the clearest places where the book absorbs a decade of industrial practice that barely existed in 2017.

## Related
- up: [[Knowledge, Truth, and Lies (2e)]] · chapter: [[Ch 09 - The Trouble with Distributed Systems (2e)]]
- [[System Model and Reality (2e)]] — the properties being verified
- [[Fault Tolerance (2e)]] — chaos engineering as a reliability practice
- [[Durable Execution and Workflows (2e)]] — determinism as a runtime requirement
- [[Event Sourcing and CQRS (2e)]] — determinism as a data-model property
