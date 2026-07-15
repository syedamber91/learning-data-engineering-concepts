---
persona: vutr
kind: entity
sources:
- raw/llms-ai-agents-and-vector-databases-additional/everything-you-need-to-know-about-bee.md
last_updated: '2026-07-15'
qc: passed
slug: llm
topics:
- llms-ai-agents-and-vector-databases
---

A Large Language Model sits at the bottom of a nesting doll: Artificial Intelligence is the broad field of simulating human intelligence, Machine Learning is the subfield where a system derives its own logic from input/output examples rather than being hand-coded, Deep Learning narrows further to unstructured data (video, text, image, audio) processed through neural networks, and an LLM is a deep learning model that generates the next text sequence from statistical patterns learned in training — in plain terms, an engine that keeps predicting the next token of a sentence like "Batman is driving \_\_\_."

The core claim worth sitting with is that an LLM doesn't know facts; it is a probability distribution over language. It hasn't "learned" that Hanoi is the capital of Vietnam — it has absorbed, from billions of sentences, that when the sequence "The capital of Vietnam is..." appears, "Hanoi" is the highest-probability continuation. This is explained through conditional probability: a plain distribution (like a fair die, where every outcome is equally likely) becomes a conditional one once you restrict to a subset of the sample space — the probability of picking a 42-year-old man, not just any 42-year-old. An LLM's conditioning event is the preceding context (which may itself come from a user's chat message): the model forms a conditional distribution over the next word given that context, samples a word from it, appends the word to the context, and repeats. Because that "pick" is a sample from a distribution rather than a lookup, the same prompt asked twice can yield different answers — LLM non-determinism is a direct consequence of the sampling mechanism, not a bug bolted on top of it.

Before this architecture became practical, language models were RNN-based and processed text sequentially, one token at a time, like a person reading a long sentence word by word — by the time the model reached the end, it had often "forgotten" the beginning, losing long-range context, and because everything had to be processed in strict order, models could not be scaled up cheaply. The 2017 Transformer paper broke that constraint (see [[transformer-attention-and-parallelism]]), and everything that followed — bigger pretraining runs, [[llm-training-pipeline|fine-tuning]], [[rag|RAG]], and the [[ai-agent|agent]] pattern of an LLM in a loop with tools — builds on the Transformer, not on a fresh breakthrough unique to the 2020s.

*See also: [[transformer-attention-and-parallelism]] · [[llm-training-pipeline]] · [[rag]] · [[ai-agent]]*
