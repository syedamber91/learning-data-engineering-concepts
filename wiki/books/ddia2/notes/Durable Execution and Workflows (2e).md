---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 5
chapter_title: Encoding and Evolution
topic: Modes of Dataflow
type: subtopic
tags: [ddia2, workflow, durable-execution, temporal, exactly-once, determinism, bpmn]
sources:
  - raw/ch05.md
---
# Durable Execution and Workflows
> You can't wrap "charge the credit card" and "deposit into the bank" in a database transaction. Durable execution frameworks are the answer, and they buy exactly-once semantics with a write-ahead log of every RPC you make.

## The Idea
Service-based architectures have multiple services responsible for different portions of an application. Consider a payment processing application that charges a credit card and deposits the funds into a bank account: it would likely have separate services for fraud detection, credit card integration, and bank integration.

Processing a single payment requires many service calls — the payment processor invokes fraud detection, then the credit card service to debit the card, then the banking service to deposit the funds. **That sequence of steps is a workflow, and each step is a task.** Workflows are typically defined as a **graph of tasks**, written in a general-purpose programming language, a domain-specific language, or a markup language such as **Business Process Execution Language (BPEL)**.

> Different engines use different names for tasks: **Temporal** calls them **activities**; others say **durable functions**. The names differ, the concept is the same.

## How It Works
Workflows are executed by a **workflow engine**, which determines when and on which machine to run each task, what to do if a task fails (if the machine crashes mid-task), how many tasks may run in parallel, and more. Engines are typically composed of an **orchestrator** — responsible for scheduling tasks — and an **executor** — responsible for running them. Execution begins when a workflow is **triggered**: the orchestrator triggers it if a time-based schedule is defined (hourly, say), and external sources such as a web service or even a human can also trigger executions. Once triggered, executors run the tasks.

There are many kinds of engines for different use cases:
- **Airflow, Dagster, Prefect** integrate with data systems and orchestrate ETL tasks.
- **Camunda, Orkes** provide a graphical notation such as **BPMN** so non-engineers can define and execute workflows.
- **Temporal, Restate** provide **durable execution**.

**Durable execution** frameworks have become a popular way to build service-based architectures requiring transactionality. In the payment example we want to process each payment **exactly once**: a failure mid-workflow could produce a credit card charge with no corresponding bank deposit. In a service-based architecture you can't simply wrap the two tasks in a database transaction — and you may be interacting with third-party payment gateways you have limited control over.

Durable execution frameworks provide **exactly-once semantics for workflows**. If a task fails, the framework **re-executes it but skips any RPC calls or state changes the task made successfully before failing**: it pretends to make the call and instead **returns the results from the previous call**. This is possible because the framework **logs all RPCs and state changes to durable storage, like a write-ahead log**.

## Trade-offs & Pitfalls
The book is careful to list the real costs:
- **External services must still provide an idempotent API.** The third-party payment gateway is outside the framework's log, so developers **must remember to use unique IDs** for these APIs to prevent duplicate execution.
- **Code changes become brittle.** Because the framework logs each RPC call in order, it **expects subsequent executions to make the same RPC calls in the same order** — so you might introduce undefined behaviour simply by **reordering function calls**. Rather than modifying an existing workflow's code, it is safer to **deploy a new version separately**, so re-executions of existing invocations keep using the old version and only new invocations use the new code.
- **Nondeterminism is a hazard.** Because frameworks expect to replay all code deterministically — same inputs, same outputs — **calling random number generators or system clocks is problematic**. Frameworks often provide their own deterministic implementations of such library functions, **but you have to remember to use them**. Some also provide static analysis tools, such as Temporal's **Workflow Check**, to detect introduced nondeterminism.
- The book flags the general point: **making code deterministic is a powerful idea but tricky to do robustly** — a theme it returns to in the distributed-systems chapter.

## Examples & Systems
Airflow, Dagster, Prefect (ETL orchestration); Camunda, Orkes (BPMN graphical workflows); Temporal, Restate (durable execution); BPEL and BPMN as definition languages; Temporal's Workflow Check for determinism analysis.

## Since the 1st Edition
Entirely new. The 1st edition had no treatment of workflow engines, durable execution, or exactly-once semantics across service calls. Its inclusion here — in the encoding chapter, alongside REST and message brokers — frames durable execution as a **fourth mode of dataflow** rather than a niche tool, which is a genuinely new organising claim.

## Related
- up: [[Modes of Dataflow (2e)]] · chapter: [[Ch 05 - Encoding and Evolution (2e)]]
- [[Dataflow Through Services - REST and RPC (2e)]] — the calls a workflow is made of
- [[Exactly-Once Message Processing Revisited (2e)]] — the same guarantee in the transactions chapter
- [[Formal Methods and Randomized Testing (2e)]] — where determinism returns
- [[Microservices and Serverless (2e)]] — the architecture creating this problem
