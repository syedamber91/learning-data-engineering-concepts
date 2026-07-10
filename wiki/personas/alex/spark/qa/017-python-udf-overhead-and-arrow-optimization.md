---
persona: alex
kind: concept
sources:
- vutr/python-udf-overhead-and-arrow-optimization
last_updated: '2026-07-10'
qc: passed
slug: 017-python-udf-overhead-and-arrow-optimization
topics:
- spark
learner: alex
source_note: python-udf-overhead-and-arrow-optimization
mastery: mastered
---

*What Alex understood:* Wait, so — okay, let me try this. A normal Spark operation is like handing your grocery list to a shopper who already works in the store: they just go get the stuff, no translation needed. That's the JVM handling something like .read.load(...) itself — nothing has to leave the building.

But a Python UDF is like the store not knowing how to make my custom order, so they call in an outside chef. My order (the data) gets copied and sent out to the chef's kitchen — that's the JVM serializing the data and shipping it over IPC to a separate Python process. The chef also separately gets a copy of the recipe (the function definition) sent from the driver. The chef makes the thing, then sends it back, which means it gets copied and converted again on the way back too. So that's two translate-and-send trips, not one, and it happens for every batch — and how much gets shipped depends on how big the order is, not on how fancy the recipe is.

The reason it's so much slower isn't just the shipping, either — once the order leaves the store, none of the store's own tricks apply anymore. Catalyst can't rewrite the recipe to be smarter, and Tungsten can't skip converting things into store-format (Java objects), because the chef never touches the store's format to begin with. On top of that the chef is doing one order at a time instead of batch-cooking, which is the slowest way to do it.

Arrow fixes the shipping part, not the one-at-a-time part — both sides start speaking the same language (Arrow instead of Pickle), so nothing needs translating, just handing over directly. But the chef is still making one thing at a time. Pandas UDFs are what actually get the chef to batch-cook: they still ride on Arrow to avoid the translation cost, but Pandas is what lets the chef work through a whole tray of orders at once instead of one by one.

## Follow-up questions

**Alex:** Pandas UDFs also use Arrow to skip the serialize/deserialize step — same trick as Arrow-optimized plain UDFs. So if Arrow by itself already skips the translation, what is Pandas actually adding? Is a Pandas UDF's speed just Arrow's transfer savings with extra steps, or is something else happening?

**vutr:** No, it's not just Arrow's transfer savings with extra steps. Arrow-optimized Python UDFs already skip serialize/deserialize by having the JVM and Python process both represent data in Arrow format instead of Pickle — but they're still row-at-a-time. Pandas UDFs ride the same Arrow-based exchange, so they get that same transfer savings, but the actual difference is that Pandas does the computation itself, operating on the data in vectorized batches rather than one row at a time. It's specifically the combination of Arrow's columnar layout plus Pandas doing the computation that lets execution happen in batches — and that combination, not the Arrow transfer savings by themselves, is the real reason Pandas UDFs outperform plain Python UDFs.

**Alex:** You said the JVM literally can't run my custom Python function, so it has to hand off to a separate process — but does that apply to every bit of Python code I write, or only stuff wrapped as a UDF? Like if I write .filter() with a plain Python lambda instead of calling udf(), does that hit the same wall and force the same process hop, or is there a line where Python code stays 'built-in enough' to avoid it?

**vutr:** (the wiki does not cover this — see open questions)
