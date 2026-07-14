---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 2
chapter_title: Data Models and Query Languages
topic: Relational Model Versus Document Model
type: subtopic
tags: [ddia, hierarchical-model, network-model, database-history]
sources:
  - raw/ch02.md
---
# Are Document Databases Repeating History?
> Today's document databases echo IBM's 1960s hierarchical model — and the relational model won that argument once already.

## The Idea
The debate over representing many-to-many relationships is far older than NoSQL. The dominant 1970s business database, IBM's Information Management System (IMS) — built originally for Apollo-program inventory tracking and released commercially in 1968, still running on mainframes today — used a *hierarchical model*: every record nested inside exactly one parent, forming a tree strikingly similar to modern JSON documents. Like document stores, IMS handled one-to-many trees well but had no joins, forcing developers to either duplicate (denormalize) data or hand-resolve references — the very dilemmas document-database users face now. Two rival solutions emerged: the network model (initially popular, ultimately forgotten) and the relational model (which conquered everything). Their "great debate" filled the 1970s.

## How It Works
**The network (CODASYL) model** generalized the hierarchy: a record could have *multiple* parents, so a single "Greater Seattle Area" record could be linked from every resident, modeling many-to-one and many-to-many links. Links were pointer-like (though on disk), not foreign keys, and the *only* way to reach a record was to walk an *access path* from a root record along link chains — like traversing a linked list, except many-to-many data means several paths reach the same record, all of which the programmer had to track mentally. Queries moved a cursor through record lists, and even committee members likened it to navigating an n-dimensional space. Manual path selection squeezed maximum efficiency from slow 1970s hardware (tape seeks), but query code became rigid: change the access paths and you rewrite piles of handwritten navigation code.

**The relational model** instead put everything in the open: a table is just a bag of rows — no nesting, no mandatory paths. Read any rows matching any condition, look rows up by key, insert freely. The query optimizer picks the effective "access path" automatically, so developers rarely think about it; adding an index instantly benefits existing queries unchanged. The key insight: build one general-purpose optimizer and every application benefits — the general solution beats hand-coded paths in the long run.

**Document databases today** revert to hierarchy in one respect — nesting one-to-many children inside the parent record — but for many-to-one/many-to-many links they behave like relational systems: a unique identifier (*document reference*, mirroring the foreign key) resolved at read time via joins or follow-up queries. Nobody has resurrected CODASYL's access paths.

## Trade-offs & Pitfalls
Hand-optimized navigation wins on constrained hardware but destroys evolvability; declarative access wins as requirements change. Document stores inherit the hierarchy's weakness for interconnected data.

## Examples & Systems
IMS (hierarchical), CODASYL-standard network databases, relational SQL systems; comparison with graph stores continues in [[Property Graphs]].

## Related
- up: [[Relational Model Versus Document Model]] · chapter: [[Ch 02 - Data Models and Query Languages]]
- [[Many-to-One and Many-to-Many Relationships]] — the problem both eras share
- [[Query Languages for Data]] — declarative vs imperative, the other axis of the debate
- [[Graph-Like Data Models]] — how graph databases avoid CODASYL's mistakes
