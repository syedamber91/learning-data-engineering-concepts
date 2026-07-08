---
persona: vutr
kind: topic
sources:
- persona-snapshot
last_updated: '2026-07-08'
qc: passed
topic: data-engineering-career-roadmap-and-learning-philosophy
---

Related: [[three-biggest-mistakes]] · [[recommended-learning-order]] · [[fundamentals-that-never-become-obsolete]] · [[nine-se-skills-for-des]] · [[data-foundation-supports-business]] · [[senior-boring-signal]] · [[learn-only-tools-is-wrong]] · [[problem-first-tool-selection]] · [[why-before-what-learning-strategy]]

## Comparisons
The roadmap is really a single argument playing out across every entity. [[three-biggest-mistakes]] is the negative image of the [[recommended-learning-order]]: 'moving too fast with tools' violates putting Data Modeling first, the 'technical box' violates business communication, and 'Data Modeling is not my duty' is the exact opposite of leading the order with it.

[[recommended-learning-order]] and [[fundamentals-that-never-become-obsolete]] answer different questions. The order is *sequence* — what to touch and when, with Cloud and AI deliberately last. The fundamentals are *durability* — what survives regardless of which tool in that sequence you happen to hold. Learn the sequence, but anchor on what would not change.

[[nine-se-skills-for-des]] and [[senior-boring-signal]] both describe maturity but from opposite ends: the nine SE skills are the concrete craft (testing, CI/CD, observability), while the 'boring' senior signals (modeling, security, governance) are where that craft points once you stop chasing novelty. Both bend toward [[data-foundation-supports-business]] — the check that decides whether any of it produced business value or just garbage.

## Open questions
- If Cloud should be one of the last things you learn yet 'most JDs ask you to have Cloud experience,' how do you get hired early without becoming the 'Cloud user, not data engineer' the source warns against?
- The order lists eleven-plus items ending in AI, but 'Using AI is not optional anymore' — how do you reconcile learning AI *last* with using it *now*?
- The source says decision-making stays human and implementation is increasingly AI-assisted, but does not say where the line falls for a *junior* who has few decisions to make yet — how does an early-career DE avoid being the replaceable implementer?
- 'Columnar always performs better than row format for analytical reads' is stated as a fundamental — the source does not address the write/OLTP side, so how universal is the claim meant to be?
- How do you concretely 'expose for feedback' and materialize learning when your day job gives you no production system to deploy to?

## Synthesis
Vu's whole roadmap resolves to one move: learn things that would not change. [[recommended-learning-order]] front-loads Data Modeling and defers Cloud and AI precisely because [[fundamentals-that-never-become-obsolete]] outlast any tool, which is why [[learn-only-tools-is-wrong]] is the core warning of the AI era. His [[three-biggest-mistakes]] are just this principle violated in reverse, and [[problem-first-tool-selection]] plus [[why-before-what-learning-strategy]] are the working habits that keep you anchored to [[data-foundation-supports-business]] — because no matter how fancy the pipeline, if the foundation can't support the business, everything you built is garbage.

## Related topics
- [[dbt]] — The roadmap front-loads data modeling as a fundamental, and Vu's insistence that dbt modeling is not data modeling is the same warning against confusing tools with the durable craft.
- [[storage-models-nsm-dsm-pax-and-column-store]] — The roadmap cites 'columnar always performs better for analytical reads' as a fundamental that never becomes obsolete — the core claim of the storage-models note.
- [[data-pipeline-design-framework]] — Problem-first tool selection and clarifying-questions-before-tools are the working habits the pipeline-design framework enacts before reaching for Spark or Kafka.
- [[history-of-data-engineering]] — The learning philosophy of anchoring on fundamentals that outlast tools is grounded in the field's history of reinvented abstractions.
- [[llms-ai-agents-and-vector-databases]] — The roadmap defers AI to last yet insists 'using AI is not optional,' and both notes stress that data-modeling decision-making stays human.
