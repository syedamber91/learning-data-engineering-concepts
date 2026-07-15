---
persona: vutr
kind: topic
sources:
- raw/weekly-newsletter-roundups-misc
last_updated: '2026-07-15'
qc: passed
topic: weekly-newsletter-roundups-misc
---

Related: [[groupby-newsletter]] · [[pet-project-retention-and-collaborative-practice]]

## Comparisons
**The newsletter's structure vs. its one substantive personal aside.** Across the eleven issues in this batch (#1, #2, #3, #6, #7, #11, #12, #21, #24, #25, #36), [[groupby-newsletter]] is almost entirely a curatorial shell: a recurring set of emoji-labeled sections, movie-quote epigraphs, and one- or two-line descriptions of other people's engineering-blog posts. The one place Vu steps out of the curator role and writes an extended first-person reflection is the pet-project note that opens issue #36, captured as [[pet-project-retention-and-collaborative-practice]]. Everything else in the batch is Vu's *selection* of what's worth reading, not his own explanation of how the underlying systems work — which is why this topic, unlike the deep-dive topics elsewhere in this wiki, has almost no synthesized systems content of its own.

**Format evolution is itself the most concrete, gradable claim the batch supports.** Issues #1–#3 (September 2023) are short, informal, and inconsistent — a handful of links with a sentence or two of framing. By #6 the newsletter has fixed sections (Engineering / Data / AI / Catch up with the world) with epigraphs from *Predestination*, *Aliens*, and *Back to the Future*, and by #21 a Career section and a "Previously on Dimension" cross-promotion box are added. Issue #36 (May 2024) breaks that template again, dropping the movie quotes and section emoji in favor of a flatter list annotated with reading times and topic tags. The batch documents this drift without ever stating why it happened — see Open questions.

**Two casual production details are the clearest window into how Vu actually assembles the newsletter.** In #12 he notes moving from "bookmarking cool stuff" plus "manually compiling it" toward "(70%) automatically compiling it using Python" — a small but concrete fact about his own workflow, not a claim about anyone else's system. In #2 he separately mentions doing "mini-research-without-any-academic-methodology" into why Iceberg, Hudi, and Delta Lake all arose, but the actual content of that research lives only in an external LinkedIn image this wiki cannot read, so nothing about its conclusions can be captured here — only that he says he did it.

## Open questions
- Why does Vu's self-introduction change between issue #6 ("a data engineer currently working at a mobile game company") and issue #11 onward ("a data engineer," with the employer detail dropped)? None of the captured issues explains the change; it isn't safe to infer a job change from this alone.
- What did Vu's own "mini-research" into the rise of Iceberg/Hudi/Delta Lake (mentioned and linked to a LinkedIn post/image in issue #2) actually conclude? The image isn't captured text, so the substance of that research is a genuine gap in this wiki, not something this topic can resolve.
- Why did issue #36 drop the fixed section structure, movie-quote epigraphs, and "Previously on Dimension" box that had been stable from #6 through #25? The batch shows the change happening but never states a reason.
- What became of "Dimension," the sister newsletter cross-promoted in issues #21–#25? It isn't mentioned again in issue #36, and none of these posts say whether it continued, merged into GroupBy, or was discontinued.

## Synthesis
This batch is Vu Trinh's own newsletter functioning as a link aggregator rather than as original technical writing: eleven issues of GroupBy, evolving in format from an unstructured handful of links (#1–#3) to a stable, ritualized template with movie-quote epigraphs and fixed sections (#6–#25) to a flatter, reading-time-tagged list (#36), with almost all of the technical substance in each issue belonging to the external authors and engineering blogs Vu links to and quotes rather than to Vu's own explanation of the underlying systems. The one place this batch yields a genuinely Vu-authored, groundable idea is his issue-#36 reflection on why pet projects fail to build lasting knowledge and what he does instead ([[pet-project-retention-and-collaborative-practice]]) — a shorter, more personal cousin of the fuller side-project framework captured elsewhere in this wiki. Treat this topic as documenting the newsletter *as an artifact* (its format, its curatorial function, its production workflow) rather than as a source of new systems-design content; the systems Vu links to here are covered, where he wrote about them himself in full, by this wiki's other topics.

## Related topics
- [[data-engineering-career-roadmap-and-learning-philosophy]] — [[pet-project-retention-and-collaborative-practice]] is a shorter, earlier cousin of that topic's [[side-project-strategy-for-job-seeking]], sharing the modeling-before-tools discipline but uniquely naming collaborative building as its own lesson.
- [[kafka]] — issue #6 links to the "Scaling Kafka to Support PayPal's Data Growth" Medium post as a curated resource; that topic's [[partition-reassignment-and-cluster-balancing]] concept is where Vu later returned to the same PayPal story with his own dedicated deep-dive (`raw/kafka/groupby-42-paypal-scaling-kafka.md`), giving a concrete before/after between curation and original synthesis.
- [[iceberg]] — issue #2 links to Databricks' original Lakehouse paper, the Delta Lake paper, and Dremio's Iceberg architecture primer, plus Vu's own (uncaptured) mini-research into why open table formats arose; that topic is where the open-table-format question is later worked through in full production depth via Netflix, DoorDash, and Walmart case studies.
