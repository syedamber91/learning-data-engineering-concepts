---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 10
chapter_title: Batch Processing
topic: Batch Processing with Unix Tools
type: subtopic
tags: [ddia, unix-philosophy, composability, interfaces]
sources:
  - raw/ch10.md
---
# The Unix Philosophy
> Small single-purpose programs, a uniform byte-stream interface, and separated logic/wiring make Unix tools composable — design lessons that transfer directly to distributed data systems.

## The Idea
Doug McIlroy, who invented pipes, imagined programs connected like segments of garden hose, each screwed on to transform the data one more way. The resulting design culture — captured in a 1978 statement of principles — says: make each program do one thing well; assume your output will feed some program you haven't met yet, so keep it clean and non-interactive; build and ship early, discarding clumsy parts; prefer building tools over manual labour. It reads like a 1970s draft of Agile and DevOps.

## How It Works
Three mechanisms make composition actually possible:

1. **A uniform interface.** Everything is a file descriptor — an ordered byte sequence. Real files, `stdin`/`stdout`, device nodes, and TCP sockets all present the same shape, so any output can feed any input. By convention most tools treat the bytes as newline-delimited ASCII records (an arbitrary choice — the ASCII record separator character was arguably designed for the job), and that shared convention is what lets `awk`, `sort`, `uniq`, and `head` interoperate. Field-level parsing is fuzzier (whitespace, tabs, CSV), which is the interface's weak spot.
2. **Separation of logic and wiring.** A program that reads `stdin` and writes `stdout` doesn't know or care where its data comes from or goes — the shell user decides. This is loose coupling / inversion of control in miniature, and it means your own filter slots into a pipeline beside programs written decades earlier by strangers.
3. **Transparency and experimentation.** Inputs are treated as immutable, so you can rerun endlessly without damage; you can cut a pipeline short and pipe into `less` to inspect intermediate results; you can persist a stage's output to a file and restart from there.

## Trade-offs & Pitfalls
- `stdin`/`stdout` handle one input and one output gracefully; multiple inputs/outputs or network connections get awkward, and any I/O a program opens itself escapes the shell's wiring flexibility.
- Untyped text forces every tool to re-parse (`{print $7}` instead of a named field) — low-value work that schema-aware formats eliminate downstream in [[Hadoop]].
- Outside Unix, this level of interoperability is rare: most software (even databases sharing a data model) doesn't compose, balkanizing data.
- Everything is confined to one machine — the gap [[MapReduce]] fills.

## Examples & Systems
`bash` pipelines; GNU `sort` as the exemplar "one thing, done well" (out-of-core, multithreaded — better than most language standard libraries); URLs + HTTP as another uniform interface that made cross-organization linking possible.

## Related
- up: [[Batch Processing with Unix Tools]] · chapter: [[Ch 10 - Batch Processing]]
- [[Simple Log Analysis]] — the philosophy demonstrated on real logs
- [[The Output of Batch Workflows]] — same immutability ethos in [[MapReduce]]
- [[Materialization of Intermediate State]] — pipes vs. temp files, revisited at scale
- [[Avro]] — schema-based encoding that fixes the untyped-text weakness
