---
persona: alex
kind: concept
sources:
- vutr/rdd-fundamentals-and-properties
last_updated: '2026-07-10'
qc: passed
slug: 002-rdd-fundamentals-and-properties
topics:
- spark
learner: alex
source_note: rdd-fundamentals-and-properties
mastery: mastered
---

*What Alex understood:* Wait, so... an RDD isn't actually the data sitting there in memory -- it's more like a recipe card that says "here's how you'd make this batch of data," plus a record of which earlier recipe cards you started from. Every card has five things stapled to it: the list of partitions (the batches it's chopped into, so different workers can each grab their own batch), a function for "how do I cook this specific batch," a dependencies list (which earlier cards this one was built from), and two optional extras -- a partitioner for key-value stuff, and hints about where each batch's ingredients already live so you don't have to ship them across the kitchen.

And because nobody's allowed to scribble on an existing card and change it -- you can only write a brand-new card that says "take card #4 and do X to it" -- two things fall out for free. First, since nobody edits a shared card, there's nothing to lock or fight over when two cooks reach for it at the same time, because nothing changes underneath either of them. Second, if a batch literally gets destroyed because a node dies, Spark doesn't need a spare copy in a fridge somewhere -- it just walks back through the stack of cards to the original ingredients and re-cooks that exact batch, because every card in the chain is still sitting there unchanged and in order.

On top of that, Spark doesn't even start cooking when you write a card -- map and filter just add more cards to the stack, describing a change, not doing it. It only actually cooks anything once you call an action, which means by then it's holding the whole stack of cards at once and can rearrange or combine steps before doing any real work, instead of being forced to cook each card the instant it's written.

## Follow-up questions

**Alex:** If losing a partition just means Spark replays the lineage to rebuild it, why does the note say Spark keeps data in memory "for as long and as much as possible" at all -- wouldn't it be simpler to never cache anything and just always recompute from the original data through the lineage graph whenever it's needed?

**vutr:** The note doesn't hand you a side-by-side cost comparison, but its own opening argument is the answer: it says MapReduce leaned on disk to exchange intermediate data between tasks, and that was durable but slow for anything iterative -- machine learning passes, interactive queries, the exact workloads where you touch the same data over and over. Spark's whole reason for existing, per the note, is an in-memory data-sharing engine that avoids that repeated slow regeneration. So in-memory caching is the default, everyday execution path -- it's what makes repeated access to the same RDD fast. Lineage-based recomputation is framed as a fault-tolerance mechanism, something that kicks in specifically when a partition is lost to a node failure, not as a replacement for holding data in memory during normal operation. Always recomputing from lineage instead of caching would mean re-deriving the same partitions repeatedly for every access, which is precisely the disk-bound, slow-for-iterative-work pattern the note says Spark was built to get away from.

**Alex:** The partitioner is optional and only applies to key-value RDDs -- so if I run a plain non-key-value transformation with no partitioner at all, does lineage-based recovery still know how to reconstruct a lost partition, or does something about "which partition is which" break without a partitioner?

**vutr:** The note keeps these as two separate properties, and that separation is the answer: "list of partitions" is its own always-present property, independent of the partitioner. The partitioner is described narrowly -- "for key-value RDDs, specifies how data is partitioned, e.g. a hash partitioner" -- so it's about how key-value data gets mapped or grouped across partitions, not about whether partitions exist or are tracked at all. Since every RDD carries a list of partitions and dependencies regardless of whether it has a partitioner, the note's lineage mechanism -- walking dependencies and reapplying recorded transformations to the original data -- doesn't rely on a partitioner being present. A non-key-value RDD with no partitioner still has its partitions list and its dependency chain, which per the note is exactly what lineage-based reconstruction needs.
