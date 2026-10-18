---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 11
chapter_title: Batch Processing
type: topic
tags: [ddia2, unix, log-analysis, nginx, pipeline]
sources:
  - raw/ch11.md
---
# Batch Processing with Unix Tools
To build intuition for batch processing, the chapter starts on **a single machine with standard Unix tools.**

A web server appends a line to a log file on every request. In NGINX's default access log format one line looks like:

```
216.58.210.78 - - [27/Jun/2025:17:55:11 +0000] "GET /css/typography.css HTTP/1.1" 200 3377 "https://martin.kleppmann.com/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
```

Interpreting it needs the log format definition: `$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"`. **So: on 27 June 2025 at 17:55:11 UTC the server received a request for `/css/typography.css` from IP 216.58.210.78. The user was not authenticated (`$remote_user` is `-`), the status was 200, the response was 3,377 bytes, the browser was Chrome 137, and it loaded the file because it was referenced from `https://martin.kleppmann.com/`.**

> **Log parsing might seem contrived, but it is a critical part of the operations of many modern technology companies** — used for everything from ad pipelines to payment processing. **Indeed, it was a driving force behind the rapid adoption of MapReduce and the "big data" movement.**

## Subtopics
- [[Simple Log Analysis (2e)]] — the six-command pipeline for the five most popular pages.
- [[Chain of Commands Versus Custom Program (2e)]] — the Python equivalent, and the execution-flow difference.
- [[Sorting Versus In-Memory Aggregation (2e)]] — which approach scales, and why.

## Key Takeaways
- The Unix pipeline is **not a toy example** — it establishes the three components that reappear in every distributed batch framework: **storage accessed through a filesystem interface, a scheduler allocating CPU, and programs connected by pipes.**
- **The single-machine limitation is the whole motivation for the rest of the chapter**: datasets too large for memory or local disk are what distributed batch processing frameworks exist for.
- **The Unix philosophy of composing small tools that read and write streams is exactly the model dataflow engines generalise** — the chapter deliberately introduces it first so that MapReduce and Spark read as extensions rather than novelties.

## Since the 1st Edition
The 1st edition's [[Batch Processing with Unix Tools]] opened identically, with the same NGINX log format and the same three subtopics. **Updated:** the example log line and dates are refreshed, and the 1st edition's longer essay on **the Unix philosophy** — uniform interfaces, separation of logic and wiring, transparency and experimentation — is compressed, with the pipeline-versus-framework analogy moved into [[Batch Processing in Distributed Systems (2e)]].

## Related
- chapter: [[Ch 11 - Batch Processing (2e)]]
- [[Batch Processing in Distributed Systems (2e)]] — the same components, distributed
- 1st edition: [[Batch Processing with Unix Tools]] — the same topic
