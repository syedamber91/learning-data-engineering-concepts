---
persona: vutr
kind: concept
sources:
- raw/data-pipeline-design-framework-additional/data-engineering-system-design-9.md
last_updated: '2026-07-15'
qc: passed
slug: ai-models-as-data-consumers-and-serving-layers
topics:
- data-pipeline-design-framework
---

Vu Trinh splits AI's relationship to the serving layer into two distinct roles that require different design responses. In the first, an AI model is simply a customer — like a dashboard or an API consumer — and most of the standard serving-layer questions still apply, but with a shifted center of gravity: the pipeline now has to account for model versioning, testing, and deployment (ideally alongside AI engineers); the data being served is more often unstructured than a nested table field — a PDF, an image, a video; and lookups are no longer just point-lookups or history scans but approximate-nearest-neighbor search, which typically means adding a vector database alongside the OLAP system.

In the second role, the AI model *is* the serving layer — a chat interface where a business user asks a question in natural language and the system parses it, generates SQL, executes it, and produces a report or chart. He treats this as meaningfully more complicated and lists four requirements for a reliable answer: enough context, provided through system prompts, MCP-connected documents, or a semantic layer that acts as both an information repository and a guardrail (he links to his own separate piece on learning the semantic layer for this); enough tools, meaning permission to actually run queries, build dashboards, or execute code; coordination across agents when a job needs several working together, which introduces its own failure modes — memory overflow, missing permissions, an agent idling with no clear cause; and consistency, since an LLM is fundamentally a probabilistic text generator and can produce a different daily report from the same question asked twice — addressed, in his telling, through feedback loops, guideline adjustment, and something he calls "harness engineering," a term he admits he isn't fully sure he understands correctly himself.

His closing frame generalizes past data engineering specifically: making an AI model a serving layer isn't a uniquely data-team challenge, and the same mindset — deliver insight in a timely, accurate, and safe manner — applies regardless of field.

*See also: [[data-grain-and-serving-storage-shape]] · [[safe-writes-and-schema-evolution-in-serving]]*
