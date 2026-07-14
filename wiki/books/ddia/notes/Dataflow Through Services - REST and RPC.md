---
book: Designing Data-Intensive Applications
part: Part I – Foundations of Data Systems
chapter: 4
chapter_title: Encoding and Evolution
topic: Modes of Dataflow
type: subtopic
tags: [ddia, rest, rpc, microservices, web-services]
sources:
  - raw/ch04.md
---
# Dataflow Through Services: REST and RPC
> Networks make remote calls fundamentally unlike local ones — REST embraces that; RPC's location transparency hides it — and service evolution reduces to backward-compatible requests plus forward-compatible responses.

## The Idea
The second mode of [[Dataflow]]: clients send requests to servers exposing an API (a *service*). This spans browsers fetching pages, Ajax/native apps consuming JSON APIs, and — most importantly for evolution — service-oriented / microservices architectures, where a server is itself a client of other services. The whole point of decomposing by service is that each team can deploy its service independently, which *guarantees* old and new versions run simultaneously and forces encoding compatibility across API versions. Unlike a database's arbitrary queries, a service exposes only the inputs/outputs its business logic permits — a form of encapsulation.

## How It Works
**Web services** (services spoken over HTTP) come in two rival philosophies:
- **REST** — not a protocol but a design philosophy leaning on HTTP itself: URLs identify resources; HTTP mechanisms handle caching, auth, and content negotiation; formats stay simple. Definition formats like OpenAPI/Swagger can document RESTful APIs. Dominant for public and cross-organization APIs, and paired culturally with microservices.
- **SOAP** — an XML-based protocol that runs over HTTP while avoiding HTTP's features, accompanied by the sprawling WS-* standards. Its WSDL descriptions enable code generation but aren't human-readable, making SOAP heavily tool-dependent and interop-fragile; it persists in large enterprises but has faded elsewhere.

**Why RPC's core abstraction fails.** RPC (a 1970s idea behind EJB, RMI, DCOM, CORBA) tries to make a network call look like a local function call — *location transparency*. But: networks fail unpredictably and outside your control; a timeout means you *cannot know* whether the request executed; retries can execute an action twice unless the protocol builds in deduplication ([[Idempotence]]); latency is orders of magnitude higher and wildly variable; you can't pass memory references, only encoded bytes; and cross-language type mismatches (JavaScript's 2^53 problem again) leak through. So don't pretend a remote service is a local object.

**Modern RPC** accepts the difference: gRPC (Protocol Buffers) supports streams of requests/responses; Finagle (Thrift) and Rest.li (JSON/HTTP) use futures/promises for async failure handling and parallel fan-out; frameworks add service discovery (see [[Request Routing]]). Binary RPC outperforms JSON-over-REST, but REST wins on debuggability (curl, a browser), universal language support, and tooling ecosystem — hence RPC mostly lives *inside* organizations, REST at their edges.

## Trade-offs & Pitfalls
Evolvability assumption: servers upgrade before clients, so requests need only **backward** compatibility, responses only **forward** compatibility. Each RPC scheme inherits the rules of its encoding (Thrift/gRPC/Avro per their formats; SOAP via XML schema evolution, with pitfalls; REST usually schemaless JSON where adding optional parameters or new response fields is deemed compatible). Across organizational boundaries you can't force client upgrades, so compatibility must hold nearly forever — providers end up running multiple API versions side by side, versioned via URL path, `Accept` header, or per-API-key version settings stored server-side.

## Examples & Systems
REST/RESTful APIs, SOAP + WSDL + WS-*, OpenAPI/Swagger, EJB, Java RMI, DCOM, CORBA, gRPC, Finagle, Rest.li, Avro RPC, Ajax, OAuth-guarded public APIs, Stripe-style per-key versioning.

## Related
- up: [[Modes of Dataflow]] · chapter: [[Ch 04 - Encoding and Evolution]]
- [[Thrift and Protocol Buffers]] — encodings whose compatibility rules RPC inherits
- [[Request Routing]] — service discovery's cousin in partitioned systems
- [[Message-Passing Dataflow]] — the asynchronous alternative to request/response
- [[Unreliable Networks]] — deeper dive into why networks defeat RPC
