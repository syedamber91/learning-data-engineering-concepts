---
persona: vutr
kind: concept
sources:
- raw/big-tech-case-studies-batch-1-spotify-twitter-facebook-discord-notion/how-did-facebook-design-their-real.md
last_updated: '2026-07-15'
qc: passed
slug: state-and-output-processing-semantics
topics:
- big-tech-case-studies-uber-netflix-linkedin-meta-doordash-spotify-twitter
---

The notes on Facebook's real-time paper draw a distinction that's easy to collapse into a single "exactly-once" buzzword but that the paper insists on splitting in two: a stream processor performs three activities — processing input, generating output, and saving checkpoints — and how it orders those activities defines two separate kinds of semantics, not one.

State semantics answer whether each input event is counted at least once, at most once, or exactly once, and the distinction comes down entirely to *ordering* between saving the in-memory state and saving the offset. At-least-once state semantics save the in-memory state first, then the offset — if the processor crashes between the two, it will reprocess the event on restart because the offset wasn't advanced, so the event gets counted again. At-most-once state semantics reverse the order: save the offset first, then the state — a crash between the two means the offset already moved on, so that event's state update is silently lost. Exactly-once state semantics require saving the in-memory state and the offset atomically, so there's no window where a crash can produce either duplication or loss.

Output semantics layer the same logic onto the emitted value rather than the internal state, and depend additionally on when the output itself gets checkpointed relative to state and offset. At-least-once output semantics emit the output first, then checkpoint offset and state — a crash after emitting but before checkpointing means the same output can be emitted again on replay. At-most-once output semantics checkpoint offset and state first, then emit — a crash in that gap loses the output entirely. Exactly-once output semantics checkpoint offset, state, and emit the output atomically together.

Stateless processors — like the Filter and Joiner nodes in the notes' trending-topics example application — only have output semantics to worry about, since there's no internal state to reconcile; stateful processors, like the Scorer and Ranker nodes in that same example, carry both. And Facebook doesn't pick one semantics tier globally: the notes give Puma as a concrete instance, guaranteeing at-least-once state and output semantics, checkpointed to HBase.

*See also: [[persistent-message-bus-data-transfer]] · [[stream-state-saving-mechanisms]] · [[twitter-lambda-to-kappa-pipeline]]*

## Related in the other wiki
- [[Exactly-Once Semantics]] — DDIA's concept of exactly-once processing is the target this note's six state/output combinations are all approximations of or deliberate departures from.
