---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 11
chapter_title: Batch Processing
topic: Batch Processing with Unix Tools
type: subtopic
tags: [ddia2, awk, sort, uniq, pipeline, log-analysis]
sources:
  - raw/ch11.md
---
# Simple Log Analysis
> Six commands, gigabytes in seconds, and every step maps onto a stage of MapReduce.

## The Idea
To find the five most popular pages on your website:

```bash
cat /var/log/nginx/access.log |
  awk '{print $7}' |
  sort |
  uniq -c |
  sort -r -n |
  head -n 5
```

## How It Works
Step by step:
- **`cat`** reads the log file. (**Strictly unnecessary** — the input file could be an argument to `awk` — **but the linear pipeline is more apparent written like this.**)
- **`awk '{print $7}'`** splits each line into whitespace-separated fields and outputs **only the seventh, which happens to be the requested URL.**
- **`sort`** alphabetically sorts the URLs. **The reason is to ensure that if a URL was requested n times, the sorted file contains it repeated n times in a row.**
- **`uniq -c`** filters out repeated lines by **checking whether two adjacent lines are the same**, and `-c` makes it **also output a counter: for every distinct URL, how many times it appeared.**
- **`sort -r -n`** sorts by the number at the start of each line — the request count — **numerically (`-n`) and in reverse (`-r`)**, largest first.
- **`head -n 5`** outputs just the first five lines.

The output:

```
4189 /favicon.ico
3631 /2016/02/08/how-to-do-distributed-locking.html
2124 /2020/11/18/distributed-systems-and-elliptic-curves.html
1369 /
 915 /css/typography.css
```

## Trade-offs & Pitfalls
- **It looks obscure if you're unfamiliar with Unix tools, but it is incredibly powerful**: **it will process gigabytes of log files in a matter of seconds**, and **you can easily modify the analysis** — to omit CSS files change the awk argument to `$7 !~ /\.css$/ {print $7}`; to count top client IPs change it to `{print $1}`.
- **Many data analyses can be done in a few minutes using a combination of `awk`, `sed`, `grep`, `sort`, `uniq`, and `xargs`, and they perform surprisingly well.**
- The pipeline is worth memorising because **each stage maps directly onto MapReduce**: `awk` is the mapper, `sort` is the implicit shuffle, `uniq -c` is the reducer.

## Examples & Systems
NGINX access logs; `awk`, `sort`, `uniq`, `head`.

## Since the 1st Edition
Essentially unchanged from the 1st edition's [[Simple Log Analysis]] — the same six-command pipeline, the same step-by-step explanation, and the same modification examples. Only the sample output URLs and dates differ.

## Related
- up: [[Batch Processing with Unix Tools (2e)]] · chapter: [[Ch 11 - Batch Processing (2e)]]
- [[MapReduce (2e)]] — the same four stages, distributed
- [[Chain of Commands Versus Custom Program (2e)]] — the alternative
- 1st edition: [[Simple Log Analysis]] — the same subtopic
