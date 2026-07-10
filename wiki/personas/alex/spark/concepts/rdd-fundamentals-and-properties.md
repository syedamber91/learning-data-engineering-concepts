---
persona: alex
kind: concept
sources:
- vutr/rdd-fundamentals-and-properties
last_updated: '2026-07-10'
qc: passed
slug: rdd-fundamentals-and-properties
topics:
- spark
learner: alex
source_note: rdd-fundamentals-and-properties
mastery: mastered
---

Wait, so... an RDD isn't actually the data sitting there in memory -- it's more like a recipe card that says "here's how you'd make this batch of data," plus a record of which earlier recipe cards you started from. Every card has five things stapled to it: the list of partitions (the batches it's chopped into, so different workers can each grab their own batch), a function for "how do I cook this specific batch," a dependencies list (which earlier cards this one was built from), and two optional extras -- a partitioner for key-value stuff, and hints about where each batch's ingredients already live so you don't have to ship them across the kitchen.

And because nobody's allowed to scribble on an existing card and change it -- you can only write a brand-new card that says "take card #4 and do X to it" -- two things fall out for free. First, since nobody edits a shared card, there's nothing to lock or fight over when two cooks reach for it at the same time, because nothing changes underneath either of them. Second, if a batch literally gets destroyed because a node dies, Spark doesn't need a spare copy in a fridge somewhere -- it just walks back through the stack of cards to the original ingredients and re-cooks that exact batch, because every card in the chain is still sitting there unchanged and in order.

On top of that, Spark doesn't even start cooking when you write a card -- map and filter just add more cards to the stack, describing a change, not doing it. It only actually cooks anything once you call an action, which means by then it's holding the whole stack of cards at once and can rearrange or combine steps before doing any real work, instead of being forced to cook each card the instant it's written.

*Source: [[rdd-fundamentals-and-properties]] (vutr)*
