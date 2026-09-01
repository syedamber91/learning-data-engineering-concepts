---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 11
chapter_title: Batch Processing
topic: Batch Processing with Unix Tools
type: subtopic
tags: [ddia2, python, hash-table, execution-flow]
sources:
  - raw/ch11.md
---
# Chain of Commands Versus Custom Program
> The Python version is readable and which you prefer is partly taste. The interesting difference isn't syntax — it's execution flow, and it only shows up on a large file.

## The Idea
The same job in Python:

```python
from collections import defaultdict

counts = defaultdict(int)
with open('/var/log/nginx/access.log', 'r') as file:
    for line in file:
        url = line.split()[6]
        counts[url] += 1

top5 = sorted(((count, url) for url, count in counts.items()), reverse=True)[:5]
for count, url in top5:
    print(f"{count} {url}")
```

- **`counts` is a hash table keeping a counter per URL**, each starting at 0.
- **The requested URL is the seventh whitespace-separated field** (index 6, since Python arrays are zero-indexed).
- **Increment the counter for that URL.**
- **Sort the hash table contents by counter descending and take the top five.**
- **Print them.**

## Trade-offs & Pitfalls
- **This is not as concise as the chain of Unix commands, but it's fairly readable, and which you prefer is in part a matter of taste.**
- **But besides the superficial syntactic differences there is a big difference in execution flow, which becomes apparent if you run this on a large file** — which is exactly the subject of the next subtopic.

## Examples & Systems
Python's `defaultdict` as the in-memory aggregation structure.

## Since the 1st Edition
Unchanged in substance from the 1st edition's [[Simple Log Analysis]]; the 1st edition used Ruby for the equivalent script, **while the 2nd edition uses Python** — a small but telling modernisation.

## Related
- up: [[Batch Processing with Unix Tools (2e)]] · chapter: [[Ch 11 - Batch Processing (2e)]]
- [[Sorting Versus In-Memory Aggregation (2e)]] — the difference this sets up
- [[Simple Log Analysis (2e)]] — the pipeline version
- 1st edition: [[Simple Log Analysis]] — where the 1st edition made the same comparison
