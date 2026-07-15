---
persona: vutr
kind: concept
sources:
- raw/llms-ai-agents-and-vector-databases-additional/my-ds-colleague-spent-one-year-learning.md
last_updated: '2026-07-15'
qc: passed
slug: agentic-problem-solving-loop
topics:
- llms-ai-agents-and-vector-databases
---

Code is written linearly — if this, then that — but an [[ai-agent|agent]] is dynamic, and the source lays out a named 5-step loop for how it actually solves a problem instead of following a hard-coded branch for every edge case.

1. **Get the Mission** — every agentic run starts from a high-level goal: a user's booking request, a high-priority support ticket firing, or someone asking to vibe-code a web app.
2. **Scan the Scene** — before acting, the agent gathers context: it reads the request, checks its Memory for past interactions, and determines which Tools (APIs, etc.) are actually available to it (see [[agent-orchestration-layer]] for what Memory and Tools mean concretely).
3. **Think It Through** — the core "think" step, driven by the reasoning [[llm|LLM]]: the agent weighs the Mission against the Scene and devises a plan, producing a Chain of Thought.
4. **Take Action** — the orchestration layer executes the first step of that plan; the agent stops "just chatting" and acts on the world — calling an API, running code, querying a database.
5. **Observe and Iterate** — the agent observes the outcome of its action, folds that new information into its context, and loops back to step 3 to decide the next move based on what it just learned.

The loop's defining property is that step 5 feeds back into step 3 rather than terminating — the agent keeps re-thinking in light of new observations until the mission is satisfied, which is the mechanism that lets a system "engineer the how" once a goal has been defined, instead of requiring every branch to be anticipated and coded in advance (see [[agent-intelligence-ladder]] for how this loop's role changes as an agent climbs from Level 1 to more autonomous levels).

*See also: [[ai-agent]] · [[agent-orchestration-layer]] · [[agent-intelligence-ladder]]*
