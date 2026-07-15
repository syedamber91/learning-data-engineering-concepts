---
persona: vutr
kind: concept
sources:
- raw/llms-ai-agents-and-vector-databases-additional/my-ds-colleague-spent-one-year-learning.md
last_updated: '2026-07-15'
qc: passed
slug: multi-agent-design-patterns
topics:
- llms-ai-agents-and-vector-databases
---

Once a system commits to a team of specialist agents rather than one super-agent (see [[agent-orchestration-layer]]), four named patterns describe how that team can be organized.

**The Coordinator** (the Manager) puts one agent in charge: it analyzes an incoming request, splits it into sub-tasks, sends work out to specialists — a researcher agent, a coder agent — and combines their individual answers into a final result.

**Sequential** organization is for linear work: the output of the first agent becomes the input to the next, chaining agents in a fixed pipeline rather than routing work dynamically.

**Iterative Refinement** (the Quality Loop) pairs a creator agent with a critic agent: the creator produces content, the critic reviews it, and the two go back and forth until the output is judged good enough.

**Human-in-the-Loop** (the Safety Check) is the pattern for high-stakes actions: the agent pauses mid-task and asks a person for approval before proceeding, rather than acting autonomously all the way through. This same HITL idea also appears as one of an agent's "Executing Actions" tools alongside API wrappers and code execution — as a pattern it can gate an entire multi-agent workflow, and as a tool it can gate a single risky action within one agent's turn.

The source lists these as four distinct common patterns for organizing a multi-agent team, without framing them as explicitly combinable or giving a worked example of combining them.

*See also: [[agent-orchestration-layer]] · [[ai-agent]] · [[agentic-problem-solving-loop]]*
