---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 10
chapter_title: Batch Processing
type: topic
tags: [ddia, batch-processing, unix, pipelines]
sources:
  - raw/ch10.md
---
# Batch Processing with Unix Tools
The chapter opens by distinguishing three styles of system: *services* (online — a client waits for a response, so latency and availability dominate), *batch processing systems* (offline — a job crunches a large bounded input and is measured by throughput, often scheduled daily), and *stream processing* (near-real-time, sitting between the two). Before scaling up to [[MapReduce]] and [[Hadoop]], the chapter grounds every big idea of batch processing in something you can run on a laptop: a pipeline of Unix commands over a web-server log. Batch computing is far older than computers themselves — Hollerith punch-card tabulation for the 1890 US census and IBM card-sorting machines of the 1940s–50s did mechanically what MapReduce does in software — and the Unix design habits from the 1970s turn out to transfer almost unchanged to thousand-machine clusters.

## Subtopics
- [[Simple Log Analysis]] — a five-command pipeline (`awk | sort | uniq -c | sort | head`) versus a custom in-memory script, and why sorting beats hash tables once the working set outgrows RAM.
- [[The Unix Philosophy]] — do one thing well, uniform byte-stream interfaces, separated logic and wiring, and immutable inputs that invite experimentation.

## Key Takeaways
- Throughput, not response time, is the success metric of a batch job — nobody is sitting there waiting.
- A chain of stock Unix tools can chew through gigabytes in seconds; GNU `sort` spills to disk and parallelizes across cores, so the pipeline scales past memory without any code changes — the same sequential-I/O, merge-sorted-segments trick as [[SSTables and LSM-Trees]].
- Choose in-memory aggregation when the *distinct-key* working set fits in RAM; choose sort-then-scan when it doesn't. This exact fork reappears inside every distributed engine.
- Composability comes from a uniform interface (newline-separated bytes on stdin/stdout), which is precisely the role [[HDFS]] files play for MapReduce.
- The one thing Unix tools cannot do is span machines — the gap the rest of the chapter fills.

## Related
- [[Ch 10 - Batch Processing]] — parent chapter MOC
- [[MapReduce and Distributed Filesystems]] — the same pattern distributed across a cluster
- [[Materialization of Intermediate State]] — pipes versus temp files, replayed at datacenter scale
- [[Batch and Stream Processing]] — Chapter 12's retrospective on where these ideas lead
