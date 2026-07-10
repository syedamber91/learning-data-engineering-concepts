---
persona: alex
kind: concept
sources:
- vutr/data-locality-and-speculative-execution
last_updated: '2026-07-10'
qc: passed
slug: data-locality-and-speculative-execution
topics:
- spark
learner: alex
source_note: data-locality-and-speculative-execution
mastery: mastered
---

Wait, so it's actually one bouncer doing two different jobs, not two separate bouncers. The TaskSetManager is like someone assigning seats at a busy restaurant who also keeps an eye on tables that are taking forever to order.

For the seating part: the DAGScheduler is the host who already knows where all the ingredients are stored — which fridge has the cached stuff, which prep station has the shuffle output — so it tells the TaskSetManager "this order should ideally go to the cook standing right next to that fridge" (PROCESS_LOCAL), or if not that exact cook, at least someone in the same kitchen (NODE_LOCAL), same building (RACK_LOCAL), or whatever, worst case, anyone free (ANY). And here's the clever bit — delay scheduling — the TaskSetManager doesn't instantly give the order to a random free cook the second the ideal cook is busy. It holds the order for a short beat, betting the ideal cook frees up, and only downgrades to a farther-away cook once that beat runs out. It's a timed bet against wasted cook time versus wasted walking time.

Then completely separately — but still the same manager — once an order IS being cooked, they're also watching the clock on it. If one cook is taking way too long, not because the recipe is hard but because maybe their stove is broken (that's the hardware example), the manager doesn't yell at them or pull the order. They quietly hand the exact same order to a second free cook and let both race it out. First one done wins, the slow one's plate gets tossed. Not a diagnosis — a race as insurance.

*Source: [[data-locality-and-speculative-execution]] (vutr)*
