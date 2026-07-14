---
book: Designing Data-Intensive Applications
part: Part III – Derived Data
chapter: 10
chapter_title: Batch Processing
topic: Batch Processing with Unix Tools
type: subtopic
tags: [ddia, unix-tools, log-analysis, sorting]
sources:
  - raw/ch10.md
---
# Simple Log Analysis
> A handful of chained Unix commands can crunch gigabytes of web-server logs in seconds — and the *way* they do it foreshadows [[MapReduce]].

## The Idea
Every request a web server handles leaves one line in an access log (client IP, timestamp, requested path, status code, bytes sent, referrer, user agent). Rather than reaching for a dedicated analytics product, you can answer questions like "which pages get the most hits?" by composing tiny general-purpose tools. The exercise matters because the execution pattern of the pipeline is exactly the pattern that scales to distributed batch systems.

## How It Works
A ranking of the five most-requested URLs can be built like this:

```bash
awk '{print $7}' < /var/log/nginx/access.log | sort | uniq -c | sort -rn | head -5
```

Field 7 of each line is the URL, so `awk` projects it out; `sort` groups identical URLs next to each other; `uniq -c` collapses each run of duplicates into a count; the second `sort -rn` ranks by that count descending; `head` keeps the winners. Swapping the `awk` expression retargets the whole analysis — print field 1 to rank client IPs, or add a pattern filter to exclude `.css` requests.

The same job written as a small script (Ruby, Python, …) would instead keep a hash table mapping URL → counter, incrementing as it streams the file, then sort the final counts. The two designs differ fundamentally: **in-memory aggregation** vs. **sort-then-scan**.

## Trade-offs & Pitfalls
- The hash-table approach wins when the *working set* — one entry per **distinct** key, not per log line — fits in RAM. A million hits on one URL still cost a single counter.
- When distinct keys outgrow memory, sorting wins: data can be sorted in memory chunk by chunk, spilled to disk as sorted runs, and merged — the same sequential-I/O-friendly discipline as [[SSTables and LSM-Trees]].
- GNU `sort` already does this transparently, spilling to disk and using multiple cores, so the naive-looking pipeline quietly scales far beyond RAM; the disk read rate becomes the bottleneck.
- The hard ceiling: everything runs on one machine. That limit is what [[Hadoop]] and [[MapReduce]] were built to remove.

## Examples & Systems
nginx access logs as input; `awk`, `sed`, `grep`, `sort`, `uniq`, `xargs`, `head` as the toolbox; GNU Coreutils `sort` as the disk-spilling, parallel mergesort workhorse.

## Related
- up: [[Batch Processing with Unix Tools]] · chapter: [[Ch 10 - Batch Processing]]
- [[The Unix Philosophy]] — why these tools compose so well
- [[MapReduce Job Execution]] — the same four steps, distributed
- [[SSTables and LSM-Trees]] — identical spill-and-merge sorting principle
