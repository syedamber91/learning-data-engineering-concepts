---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 3
chapter_title: Data Models and Query Languages
topic: Relational Versus Document Models
type: subtopic
tags: [ddia2, orm, impedance-mismatch, n-plus-1, json, one-to-many]
sources:
  - raw/ch03.md
---
# The Object-Relational Mismatch
> Objects and tables don't line up, so something has to translate. ORMs do it with less boilerplate and more surprises.

## The Idea
Much application development is done in object-oriented languages, which produces a standing criticism of the SQL data model: storing data in relational tables requires an awkward translation layer between application objects and the database's tables, rows, and columns. The disconnect is called an **impedance mismatch** — a term borrowed from electronics, where every circuit has an impedance on its inputs and outputs, power transfer is maximised when they match, and a mismatch causes signal reflections and other troubles.

## How It Works
**Object-relational mapping (ORM)** frameworks such as ActiveRecord and Hibernate reduce the boilerplate, but are often criticised:
- ORMs are complex and cannot completely hide the differences, so developers still end up thinking about **both** representations.
- They are generally used only for OLTP application development; data engineers preparing data for analytics work with the underlying relational representation, so the relational schema design still matters even when an ORM is used.
- Many work only with relational OLTP databases, so organisations with search engines, graph databases, and NoSQL systems may find support lacking.
- Some auto-generate relational schemas that are awkward for people querying the relational data directly, and inefficient on the underlying database. Customising the ORM's schema and query generation can be complex enough to negate the benefit of using it.
- **They make it easy to accidentally write inefficient queries — the N+1 query problem.** Say you display a list of user comments: one query returns N comments, each with its author's ID. To show author names, you look each ID up in the users table. In handwritten SQL you would do that join in the query and return the author name alongside each comment; with an ORM you may end up issuing a separate users query per comment, giving **N+1 queries** in total. To avoid it you must tell the ORM to fetch author information at the same time as the comments.

ORMs also have real advantages: for data well suited to a relational model some translation is inevitable, and ORMs cut the boilerplate for simple, repetitive cases (complicated queries may still need handling outside the ORM); some help with caching query results, reducing database load; and some help with schema migrations and other administrative work.

**The document model for one-to-many relationships.** Not all data suits a relational representation. The book's example is a résumé — a LinkedIn profile. The profile has a `user_id`; `first_name` and `last_name` appear exactly once per user so they are columns on a `users` table. But most people have had several jobs, may have several periods of education, and any number of pieces of contact information. One way to represent these **one-to-many** relationships is separate `positions`, `education`, and `contact_info` tables with foreign keys back to `users`. Another — perhaps more natural, and mapping more closely to an object structure in application code — is a single JSON document with `positions` and `education` as arrays and `contact_info` as a nested object.

## Trade-offs & Pitfalls
- The JSON representation has **better locality**: fetching a profile from the multi-table schema needs either multiple queries (one per table, by `user_id`) or a messy multiway join, whereas in JSON everything relevant is in one place, making the query both faster and simpler.
- The one-to-many relationships imply a **tree structure**, and JSON makes that tree explicit.
- A one-to-many relationship is sometimes called **one-to-few**, since a résumé has a small number of positions. If you genuinely have a large number of related items — comments on a celebrity's social media post, of which there could be many thousands — embedding them all in the same document may be too unwieldy, and the relational approach is preferable.
- Schema flexibility is often cited as a further document advantage, but the book notes there are also problems with JSON as a data *encoding* format, taken up in the encoding chapter.

## Examples & Systems
ActiveRecord and Hibernate as the named ORMs; a LinkedIn-style résumé as the one-to-many worked example.

## Since the 1st Edition
The 1st edition's [[The Object-Relational Mismatch]] introduced impedance mismatch, ORMs, and the same résumé example. **New in the 2nd edition:** the detailed pros-and-cons list for ORMs — particularly the **N+1 query problem**, the analytics/data-engineering objection, and the schema-generation critique — none of which the 1st edition spelled out. The 1st edition also discussed the historical hierarchical/network models at length here; that material has moved up into [[Relational Versus Document Models (2e)]] as a compressed history.

## Related
- up: [[Relational Versus Document Models (2e)]] · chapter: [[Ch 03 - Data Models and Query Languages (2e)]]
- [[Normalization, Denormalization, and Joins (2e)]] — the next question the résumé example raises
- [[When to Use Which Model (2e)]] — where locality and schema flexibility are settled
- 1st edition: [[The Object-Relational Mismatch]] — the same subtopic
