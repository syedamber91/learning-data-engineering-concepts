---
book: Designing Data-Intensive Applications (2nd Edition)
edition: 2
chapter: 3
chapter_title: Data Models and Query Languages
topic: Graph-Like Data Models
type: subtopic
tags: [ddia2, graphql, oltp, api, untrusted-queries]
sources:
  - raw/ch03.md
---
# GraphQL
> Deliberately the least powerful query language in the chapter — because its queries arrive from a user's phone, and anything expensive is a denial-of-service vector.

## The Idea
**GraphQL** is by design **much more restrictive** than the other languages in this chapter. It is intended for OLTP queries, and its purpose is to let client software running on a user's device — a mobile app or a JavaScript web frontend — request a JSON document with a particular structure containing exactly the fields needed to render its UI.

## How It Works
The book's example is a group chat application like Discord or Slack. The query requests all channels the user can access, with each channel's name and its 50 most recent messages; for each message, the timestamp, content, and the sender's name and profile picture URL; and if the message is a reply, the sender name and content of the message replied to (perhaps rendered in a smaller font above the reply for context):

```graphql
query ChatApp {
  channels {
    name
    recentMessages(latest: 50) {
      timestamp
      content
      sender { fullName imageUrl }
      replyTo { content sender { fullName } }
    }
  }
}
```

The **response is a JSON document mirroring the structure of the query** — exactly the attributes requested, no more and no less. The advantage is that the server does not need to know which attributes the client needs to render its interface; the client simply asks. If the UI changed to show the profile picture of a `replyTo` sender, the client just adds `imageUrl` to the query with **no server-side change**.

The server's database can store data in a more normalized form and perform the necessary joins: it might store a message with the sender's user ID and the ID of the message being replied to, then resolve those IDs when the query arrives. **But only joins explicitly declared in the GraphQL schema can be requested by the client.**

## Trade-offs & Pitfalls
- **Duplication is a deliberate design choice.** The sender's name and image URL are embedded directly in each message object, so a user sending several messages has that information repeated. It would be possible to reduce this, but GraphQL accepts a larger response to make rendering the UI simpler. The `replyTo` field is the same: the content and sender name are duplicated rather than returning the replied-to message's ID, because otherwise the client would need an extra request whenever that ID is not among the 50 messages returned.
- **The restrictions exist because queries come from untrusted sources.** GraphQL does not allow anything expensive to execute, since users could — perhaps unintentionally — cause a denial-of-service condition by running many expensive queries. In particular it **does not allow recursive queries** (unlike Cypher, SPARQL, SQL, or Datalog), and it does not allow arbitrary search conditions such as "find people born in the US now living in Europe" unless the service owners specifically choose to offer that search.
- **The flexibility has an operational cost.** GraphQL lets developers change client-side queries rapidly without changing server-side APIs, but organisations adopting it often need tooling to convert queries into requests to internal services, which commonly use REST or gRPC. Authorization, rate limiting, and performance are additional concerns.
- Despite the name, **GraphQL can be implemented on top of any type of database** — relational, document, or graph — and its responses merely *look* like a document database's.

## Examples & Systems
A Discord/Slack-style group chat as the worked example; REST and gRPC as the internal services GraphQL usually fronts.

## Since the 1st Edition
Entirely new. GraphQL existed in 2017 but did not appear in the 1st edition. Its inclusion here is notable for *where* it sits: alongside Cypher, SPARQL, and Datalog, framed as the query language whose defining characteristic is **what it refuses to do**.

## Related
- up: [[Graph-Like Data Models (2e)]] · chapter: [[Ch 03 - Data Models and Query Languages (2e)]]
- [[Dataflow Through Services - REST and RPC (2e)]] — the services GraphQL sits in front of
- [[When to Use Which Model (2e)]] — document-shaped responses and their locality logic
