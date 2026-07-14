---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 2
chapter_title: Data Models and Query Languages
type: topic
tags: [ddia, data-models, relational, document-databases]
sources:
  - raw/ch02.md
---
# Relational Model Versus Document Model
> The oldest fight in databases — tables with joins versus self-contained nested documents — replayed from the 1970s hierarchical era through today's NoSQL wave, and settled as "it depends on your relationships."

Codd's relational model organized data as unordered collections of tuples and, against early doubts about efficiency, dominated for decades because it hid storage details behind a clean interface and generalized far beyond its business-processing origins. The 2010s NoSQL movement re-opened the question, driven by scale, open-source preference, specialized queries, and schema frustration. The chapter's arc: object-oriented code sits awkwardly on tables (the impedance mismatch), which makes JSON documents attractive for tree-shaped, one-to-many data — but as soon as data needs [[Many-to-One and Many-to-Many Relationships]], documents struggle exactly the way IBM's hierarchical IMS did in the 1970s, a problem the relational model (automatic query optimizers, easy joins) and the CODASYL network model (manual access paths) fought over once already. The verdict today is convergence: pick by data shape, and expect hybrid databases. Key axes of comparison are schema-on-read versus schema-on-write, storage locality, and join support; [[Denormalization]] is the escape hatch when joins are unavailable, at the cost of application-maintained consistency.

## Subtopics
- [[The Birth of NoSQL]] — where the nonrelational challenge came from and the forces driving it (scale, open source, specialized queries, schema flexibility).
- [[The Object-Relational Mismatch]] — the awkward translation layer between objects and tables that ORMs soften but never remove; JSON's locality appeal.
- [[Many-to-One and Many-to-Many Relationships]] — why IDs beat duplicated strings, why normalization needs joins, and why interconnection grows over time.
- [[Are Document Databases Repeating History]] — IMS's hierarchical model, the CODASYL network model's access paths, and the relational answer: the query optimizer.
- [[Relational Versus Document Databases Today]] — schema-on-read vs schema-on-write, data locality, and the two camps converging on hybrids.

## Key Takeaways
- Data models shape not just storage but how you *think* about the problem; each layer hides the one below via a clean model.
- Documents win for self-contained trees loaded whole (no shredding, good locality); relations win when data is interconnected and needs joins.
- "Schemaless" really means schema-on-read — an implicit schema interpreted by reading code, analogous to dynamic typing — versus the relational schema-on-write.
- The document model's weaknesses (weak joins, awkward many-to-many) are the hierarchical model's 1970s weaknesses returning; document databases chose foreign-key-like *document references* rather than CODASYL-style access paths.
- A once-built query optimizer benefits every application; hand-tuned access paths made code fast but brittle.
- Convergence is the trend: relational systems added XML/JSON support, document stores added joins — hybrid models complement each other.

## Related
- chapter: [[Ch 02 - Data Models and Query Languages]]
- [[Query Languages for Data]] — declarative vs imperative, the querying half of the same story
- [[Graph-Like Data Models]] — the model of choice once many-to-many dominates
- [[Data Structures That Power Your Database]] — Ch 3 implements what these models promise
- [[The Merits of Schemas]] — Ch 4's case for explicit schemas
