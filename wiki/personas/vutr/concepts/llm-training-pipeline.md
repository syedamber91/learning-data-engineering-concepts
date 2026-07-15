---
persona: vutr
kind: concept
sources:
- raw/llms-ai-agents-and-vector-databases-additional/everything-you-need-to-know-about-bee.md
last_updated: '2026-07-15'
qc: passed
slug: llm-training-pipeline
topics:
- llms-ai-agents-and-vector-databases
---

Turning a [[transformer-attention-and-parallelism|Transformer architecture]] into a usable product is described as a three-stage pipeline, and the data engineer's job changes shape at each stage.

**Pre-training** is named as the most computationally expensive and time-consuming phase: the model is fed a massive, general-purpose corpus (OpenAI and Google are named as literally training on data from the whole internet) so it develops broad understanding rather than task-specific skill. This step is only practical because Transformers are faster to train and more hardware-efficient than their sequential predecessors (see [[transformer-attention-and-parallelism]]). The output of pre-training is called a base model — described bluntly as "a giant autocomplete machine."

**Fine-tuning** takes that base model and continues training it on a much smaller, more specific dataset, with the goal of improving performance on particular tasks and instruction-following. Fine-tuning is good at reshaping behavior but explicitly called out as inefficient for teaching new, rapidly changing facts, because it inherits the same dependency on slow, quality-sensitive training data that pre-training has — which is the gap [[rag]] is built to fill instead (see [[rag]]).

**Reinforcement Learning from Human Feedback (RLHF)** is the final named stage, aligning the model with complex human values or safety guidelines — the given example is why ChatGPT answers politely rather than bluntly.

Across all three stages, the source is explicit that a data engineer's involvement doesn't stop after pre-training: fine-tuning and RLHF both need collected, stored, and served data too, and "the quality of the input dataset will determine the reliability and behavior of the resulting model" — meaning the data-quality discipline that applies to a company's internal analytics pipelines applies just as directly to whatever dataset an organization uses to fine-tune or align a model for its own purposes.

*See also: [[transformer-attention-and-parallelism]] · [[llm]] · [[rag]]*
